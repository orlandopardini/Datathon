"""
Script rápido para testar a API de predição após correção do modelo.
IMPORTANTE: Execute ANTES de iniciar a API para verificar se o modelo está correto.
"""
import joblib
import pandas as pd
import sys

print("=" * 60)
print("🔍 VERIFICANDO MODELO CORRIGIDO")
print("=" * 60)
print()

try:
    # 1. Verificar se modelo existe
    print("1️⃣ Carregando modelo...")
    model = joblib.load("app/model/model.joblib")
    print("   ✅ Modelo carregado com sucesso!")
    
    # 2. Verificar parâmetros do LogisticRegression
    print()
    print("2️⃣ Verificando parâmetros do modelo...")
    clf = model.named_steps['clf']
    params = clf.get_params()
    
    print(f"   Tipo: {type(clf).__name__}")
    print(f"   Max Iter: {params.get('max_iter')}")
    print(f"   Solver: {params.get('solver')}")
    print(f"   Random State: {params.get('random_state')}")
    
    # Verificar se multi_class NÃO está nos parâmetros (sklearn 1.8.0+)
    if 'multi_class' in params:
        print("   ❌ PROBLEMA: Modelo ainda tem parâmetro multi_class (modelo antigo)")
        sys.exit(1)
    else:
        print("   ✅ Modelo correto (sem parâmetro multi_class)")
    
    # 3. Testar predição diretamente
    print()
    print("3️⃣ Testando predição com dados de exemplo...")
    
    from src.feature_engineering import add_engineered_features
    from src.utils import read_json
    
    sample_data = {
        "Idade": 12,
        "Gênero": "M",
        "Ano ingresso": 2020,
        "Fase": "1A",
        "Turma": "1A",
        "Instituição de ensino": "Escola Pública",
        "INDE 2024": 7.5,
        "IAA": 6.8,
        "IPS": 7.0,
        "Nº Av": 12,
        # Campos opcionais com NaN
        "IDA": None,
        "Mat": None,
        "Por": None,
        "Ing": None,
        "INDE 22": None,
        "INDE 23": None,
        "IPP": None,
        "IPV": None,
        "IAN": None
    }
    
    df = pd.DataFrame([sample_data])
    df = add_engineered_features(df)
    
    # Fazer predição
    proba = model.predict_proba(df)[:, 1][0]
    label = int(proba >= 0.5)
    
    print("   ✅ Predição realizada com sucesso!")
    print()
    print("=" * 60)
    print("📊 RESULTADO DO TESTE")
    print("=" * 60)
    print()
    print(f"   Probabilidade de Risco: {proba * 100:.1f}%")
    print(f"   Classificação: {'⚠️ EM RISCO' if label == 1 else '✅ SEM RISCO'}")
    print()
    print("=" * 60)
    print()
    print("✅ MODELO ESTÁ FUNCIONANDO CORRETAMENTE!")
    print()
    print("📋 PRÓXIMO PASSO:")
    print("   Execute: restart-api.bat")
    print("   Ou: uvicorn app.main:app --reload")
    print()
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)

