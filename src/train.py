from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

from src.preprocessing import (
    load_pede_excel, 
    build_target_at_risk_evasao,  # NOVO: target baseado em engajamento (risco de evasão)
    drop_leaky_and_id_cols, 
    train_test_split_stratified,
    TARGET_ENGAJAMENTO_COL  # Coluna usada no target (não deve ser feature)
)
from src.feature_engineering import add_engineered_features, get_feature_target_columns
from src.evaluate import evaluate_binary
from src.drift import build_baseline
from src.utils import write_json, ensure_dir

# Suprimir warnings esperados de features ausentes
warnings.filterwarnings('ignore', message='.*Skipping features without any observed values.*')
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


def build_pipeline(numeric_cols: list[str], categorical_cols: list[str]) -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler(with_mean=False)),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ],
        remainder="drop",
    )

    # Modelo baseline robusto e interpretável
    # sklearn 1.8.0+ não usa mais o parâmetro multi_class (inferido automaticamente)
    clf = LogisticRegression(
        max_iter=2000, 
        n_jobs=None,
        solver='lbfgs',  # Solver padrão mais estável
        random_state=42
    )

    model = Pipeline(steps=[("preprocess", preprocessor), ("clf", clf)])
    return model


def main():
    parser = argparse.ArgumentParser(description="Treina o modelo de risco de EVASÃO ESCOLAR e salva artefatos.")
    parser.add_argument(
        "--data-path", 
        default="database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx",
        help="Caminho do Excel PEDE (default: database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx)."
    )
    parser.add_argument("--sheet", default="PEDE2024", help="Aba do Excel (default: PEDE2024).")
    parser.add_argument("--threshold", type=float, default=5.0, help="Threshold de IEG para risco de evasão (default: 5.0).")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--outdir", default="app/model", help="Diretório para salvar artefatos (default: app/model).")
    args = parser.parse_args()

    df = load_pede_excel(args.data_path, args.sheet)

    # NOVO TARGET: baseado em engajamento (IEG < threshold = risco de evasão)
    print(f"📊 Criando target de risco de EVASÃO com threshold IEG={args.threshold}...")
    y = build_target_at_risk_evasao(df, threshold=args.threshold)
    
    # Estatísticas do target
    n_em_risco = y.sum()
    n_total = len(y)
    pct_risco = n_em_risco / n_total * 100
    print(f"   Total de alunos: {n_total}")
    print(f"   Em risco de evasão (IEG < {args.threshold}): {n_em_risco} ({pct_risco:.1f}%)")
    print(f"   Sem risco de evasão (IEG >= {args.threshold}): {n_total - n_em_risco} ({100-pct_risco:.1f}%)")
    
    X = df.copy()

    # evita vazamento + ids
    X = drop_leaky_and_id_cols(X)

    # engenharia de features
    X = add_engineered_features(X)

    # IMPORTANTE: Selecionar features CORRETAS para modelo de EVASÃO
    # AGORA IDA, Mat, Por, Ing PODEM ser features (só IEG é usado no target)
    features_modelo_evasao = [
        # Demográficas
        "Idade",
        "Gênero",
        "Ano ingresso",
        "Instituição de ensino",
        
        # Contexto acadêmico
        "Fase",
        "Turma",
        
        # NOTAS (preditoras importantes para evasão!)
        "IDA",   # Indicador de Desempenho Acadêmico
        "Mat",   # Matemática
        "Por",   # Português
        "Ing",   # Inglês
        
        # Indicadores históricos (performance passada)
        "INDE 22",
        "INDE 23",
        "INDE 2024",
        
        # Indicadores psicossociais (CRÍTICOS para evasão!)
        "IAA",   # Autoavaliação
        "IPS",   # Psicossocial
        "IPP",   # Psicopedagógico
        "IPV",   # Ponto de virada
        "IAN",   # Autoavaliação numérica
        
        # Suporte recebido
        "Nº Av",  # Número de avaliações
        
        # Features engenheiradas
        "Fase_num",
        "Tempo_programa",
        "Idade_ingresso",
    ]
    
    # Filtrar apenas features que existem no dataset
    features_existentes = [f for f in features_modelo_evasao if f in X.columns]
    print(f"\n🔧 Features selecionadas para modelo de EVASÃO: {len(features_existentes)}")
    print(f"   Numéricas: Idade, Ano ingresso, IDA, Mat, Por, Ing, INDEs, IAA, IPS, IPP, IPV, IAN, Nº Av, Fase_num, Tempo_programa, Idade_ingresso")
    print(f"   Categóricas: Gênero, Instituição de ensino, Fase, Turma")
    
    # Remover explicitamente IEG (usado no target de evasão)
    if TARGET_ENGAJAMENTO_COL in features_existentes:
        features_existentes.remove(TARGET_ENGAJAMENTO_COL)
        print(f"   ⚠️ Removida '{TARGET_ENGAJAMENTO_COL}' (usada no target de evasão)")
    
    X = X[features_existentes]

    # Separar numéricas e categóricas
    numeric_cols = [
        "Idade", "Ano ingresso", 
        "IDA", "Mat", "Por", "Ing",  # NOTAS agora são features!
        "INDE 22", "INDE 23", "INDE 2024",
        "IAA", "IPS", "IPP", "IPV", "IAN",
        "Nº Av",
        "Fase_num", "Tempo_programa", "Idade_ingresso"
    ]
    numeric_cols = [c for c in numeric_cols if c in X.columns]
    
    categorical_cols = ["Fase", "Turma", "Gênero", "Instituição de ensino"]
    categorical_cols = [c for c in categorical_cols if c in X.columns]
    
    print(f"   ✅ {len(numeric_cols)} numéricas: {numeric_cols}")
    print(f"   ✅ {len(categorical_cols)} categóricas: {categorical_cols}")

    split = train_test_split_stratified(X, y, test_size=args.test_size, random_state=args.random_state)

    print(f"\n🎯 Treinando modelo...")
    print(f"   Treino: {len(split.X_train)} amostras")
    print(f"   Teste: {len(split.X_test)} amostras")
    
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(split.X_train, split.y_train)

    # métricas
    print(f"\n📈 Avaliando modelo...")
    y_proba = model.predict_proba(split.X_test)[:, 1]
    metrics = evaluate_binary(split.y_test, y_proba, threshold=0.5)

    outdir = Path(args.outdir)
    ensure_dir(outdir)

    # salvar artefatos
    print(f"\n💾 Salvando artefatos em {outdir}...")
    joblib.dump(model, outdir / "model.joblib")
    write_json(outdir / "metrics.json", metrics)
    write_json(outdir / "feature_columns.json", {"numeric": numeric_cols, "categorical": categorical_cols})
    
    # Salvar config do modelo de EVASÃO
    model_config = {
        "model_type": "dropout_risk",
        "description": "Prediz risco de EVASÃO ESCOLAR (abandono do programa) via engajamento baixo",
        "threshold": args.threshold,
        "target_definition": f"at_risk = 1 se IEG < {args.threshold}",
        "engajamento_usado_no_target": TARGET_ENGAJAMENTO_COL,
        "features_count": len(features_existentes),
        "created_at": "2026-03-02",
        "version": "3.0",
        "interpretation": "IEG < 5.0 indica desengajamento crítico (presença baixa, participação fraca)"
    }
    write_json(outdir / "model_config.json", model_config)

    # baseline drift: usar treino (antes do split) para baseline
    baseline = build_baseline(split.X_train, numeric_cols=numeric_cols, categorical_cols=categorical_cols)
    write_json(outdir / "baseline.json", baseline)

    print("\n" + "="*60)
    print("✅ TREINO FINALIZADO COM SUCESSO")
    print("="*60)
    print(f"\n📊 MÉTRICAS DO MODELO DE EVASÃO (Conjunto de Teste):")
    print(f"   ROC-AUC: {metrics.get('roc_auc', 0):.1%}")
    print(f"   Acurácia: {metrics.get('accuracy', 0):.1%}")
    print(f"   Precisão: {metrics.get('precision', 0):.1%}")
    print(f"   Recall: {metrics.get('recall', 0):.1%}")
    print(f"   F1-Score: {metrics.get('f1', 0):.1%}")
    print(f"\n🎯 Target: Risco de Evasão (IEG < {args.threshold})")
    print(f"   Em risco de evasão: {n_em_risco} alunos ({pct_risco:.1f}%)")
    print(f"   Sem risco de evasão: {n_total - n_em_risco} alunos ({100-pct_risco:.1f}%)")
    print("\n💡 Interpretação:")
    print(f"   - IEG < {args.threshold} = Desengajamento crítico (presença baixa, participação fraca)")
    print(f"   - Modelo identifica alunos em risco de abandonar o programa")
    print(f"   - Estratégia: Intervenções de reengajamento (tutoria, suporte psicossocial)")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Testar API: uvicorn app.main:app --reload")
    print("   2. Validar predições com script de teste")
    print("   3. Verificar que IEG BAIXO → ALTO risco de evasão")
    print("="*60)


if __name__ == "__main__":
    main()
