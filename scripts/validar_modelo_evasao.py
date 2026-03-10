"""
Script de Validacao do Modelo de Evasao Escolar (v3.0)
"""
import pandas as pd
import joblib
from pathlib import Path

from src.preprocessing import build_target_at_risk_evasao, drop_leaky_and_id_cols, load_pede_excel
from src.feature_engineering import add_engineered_features

print("=" * 80)
print("VALIDACAO DO MODELO DE EVASAO ESCOLAR (v3.0)")
print("=" * 80)

# Carregar modelo
model_path = Path("app/model/model.joblib")
if not model_path.exists():
    print("\nModelo nao encontrado! Execute: python -m src.train --threshold 5.0")
    exit(1)

model = joblib.load(model_path)
print(f"\nModelo carregado: {model_path}")

# Carregar dados
df = load_pede_excel("database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx", "PEDE2024")
print(f"Dados carregados: {len(df)} alunos")

# Criar target
y = build_target_at_risk_evasao(df, threshold=5.0)
print(f"\nDistribuicao do Target:")
print(f"   Em risco de evasao (IEG < 5.0): {y.sum()} alunos ({y.mean()*100:.1f}%)")
print(f"   Sem risco (IEG >= 5.0): {(1-y).sum()} alunos ({(1-y.mean())*100:.1f}%)")

# Preparar features
X = df.copy()
X = drop_leaky_and_id_cols(X)
X = add_engineered_features(X)

# Validar predições spot-check
print("\n" + "=" * 80)
print("CASOS DE TESTE (VALIDAÇÃO QUALITATIVA)")
print("=" * 80)

# Caso 1: IEG muito alto (engajado)
test_cases = [
    {"desc": "Aluno ENGAJADO (IEG=9.5)", "IEG": 9.5, "expected": 0},
    {"desc": "Aluno ENGAJAMENTO OK (IEG=6.0)", "IEG": 6.0, "expected": 0},
    {"desc": "Aluno ENGAJAMENTO LIMITE (IEG=5.0)", "IEG": 5.0, "expected": 0},
    {"desc": "Aluno DESENGAJADO (IEG=4.5)", "IEG": 4.5, "expected": 1},
    {"desc": "Aluno CRÍTICO (IEG=2.0)", "IEG": 2.0, "expected": 1},
]

print("\nValidando consistência do target:")
for case in test_cases:
    test_df = pd.DataFrame({"IEG": [case["IEG"]]})
    target = build_target_at_risk_evasao(test_df, threshold=5.0)
    status = "✅" if target[0] == case["expected"] else "❌"
    print(f"   {status} {case['desc']:40s} → at_risk={target[0]} (esperado={case['expected']})")

# Validar predições do modelo em alguns alunos reais
print("\n" + "=" * 80)
print("PREDIÇÕES EM ALUNOS REAIS (SAMPLE)")
print("=" * 80)

# Pegar 5 alunos em risco e 5 sem risco
em_risco_idx = df[df['IEG'] < 5.0].index[:5]
sem_risco_idx = df[df['IEG'] >= 5.0].index[:5]

from src.utils import read_json
feature_spec = read_json("app/model/feature_columns.json")
expected_features = feature_spec["numeric"] + feature_spec["categorical"]

print("\n🔴 ALUNOS EM RISCO (IEG < 5.0):")
for idx in em_risco_idx:
    ieg_val = df.loc[idx, 'IEG']
    X_sample = X.loc[[idx], expected_features]
    proba = model.predict_proba(X_sample)[0, 1]
    pred = int(proba >= 0.5)
    print(f"   Aluno {idx:4d}: IEG={ieg_val:4.1f} | P(evasão)={proba:.1%} | Pred={pred}")

print("\n🟢 ALUNOS SEM RISCO (IEG >= 5.0):")
for idx in sem_risco_idx:
    ieg_val = df.loc[idx, 'IEG']
    X_sample = X.loc[[idx], expected_features]
    proba = model.predict_proba(X_sample)[0, 1]
    pred = int(proba >= 0.5)
    print(f"   Aluno {idx:4d}: IEG={ieg_val:4.1f} | P(evasão)={proba:.1%} | Pred={pred}")

# Estatísticas globais
print("\n" + "=" * 80)
print("ESTATÍSTICAS DE PREDIÇÃO (TODO O DATASET)")
print("=" * 80)

X_all = X[expected_features]
proba_all = model.predict_proba(X_all)[:, 1]
pred_all = (proba_all >= 0.5).astype(int)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

print(f"\n📊 Métricas Globais:")
print(f"   Acurácia:  {accuracy_score(y, pred_all):.1%}")
print(f"   Precisão:  {precision_score(y, pred_all, zero_division=0):.1%}")
print(f"   Recall:    {recall_score(y, pred_all, zero_division=0):.1%}")
print(f"   F1-Score:  {f1_score(y, pred_all, zero_division=0):.1%}")
print(f"   ROC-AUC:   {roc_auc_score(y, proba_all):.1%}")

print("\n📋 Distribuição de Predições:")
print(f"   Predito EM RISCO:  {pred_all.sum()} alunos ({pred_all.mean()*100:.1f}%)")
print(f"   Predito SEM RISCO: {(1-pred_all).sum()} alunos ({(1-pred_all.mean())*100:.1f}%)")

print("\n" + "=" * 80)
print("✅ VALIDAÇÃO CONCLUÍDA")
print("=" * 80)
print("\n💡 Interpretação:")
print("   - Modelo prevê RISCO DE EVASÃO via IEG < 5.0")
print("   - IEG baixo = desengajamento = risco de abandonar programa")
print("   - Alunos em risco devem receber intervenções de reengajamento")
print("   - ROC-AUC perto de 100% indica excelente separação")
print("\n🎯 Próximos passos:")
print("   1. Iniciar API: uvicorn app.main:app --reload")
print("   2. Testar endpoint /predict com casos reais")
print("   3. Monitorar drift: streamlit run monitoring/dashboard.py")
print("=" * 80)
