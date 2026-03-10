"""
Debug: Verifica se add_engineered_features está funcionando corretamente
"""
import pandas as pd
from src.feature_engineering import add_engineered_features

# Dados de teste (mesmo do test_dashboard_integration.py)
test_data = {
    "Fase": "3A",
    "Turma": "3A",
    "Idade": 12,
    "Gênero": "M",
    "Ano ingresso": 2020,
    "Instituição de ensino": "Escola Pública",
    "INDE 22": 4.5,
    "INDE 23": 4.8,
    "INDE 2024": 5.0,
    "IAA": 4.0,
    "IPS": 4.5,
    "IPP": 4.2,
    "IPV": 4.8,
    "IAN": 4.3,
    "Nº Av": 10
}

print("=" * 80)
print("DEBUG: add_engineered_features")
print("=" * 80)
print()

# Criar DataFrame
df_input = pd.DataFrame([test_data])
print("INPUT:")
print(df_input.to_string())
print()

# Aplicar add_engineered_features
df_output = add_engineered_features(df_input, current_year=2024)
print("OUTPUT (depois de add_engineered_features):")
print(df_output.to_string())
print()

# Verificar features críticas
print("FEATURES CRIADAS:")
print(f"  Fase_num: {df_output['Fase_num'].iloc[0] if 'Fase_num' in df_output.columns else 'FALTANDO!'}")
print(f"  Tempo_programa: {df_output['Tempo_programa'].iloc[0] if 'Tempo_programa' in df_output.columns else 'FALTANDO!'}")
print(f"  Idade_ingresso: {df_output['Idade_ingresso'].iloc[0] if 'Idade_ingresso' in df_output.columns else 'FALTANDO!'}")
print()

# Agora vamos fazer uma predição com esse DataFrame
print("=" * 80)
print("TESTANDO PREDIÇÃO COM FEATURES ENGINEERED")
print("=" * 80)
print()

import joblib
import json

# Carregar modelo e features
model = joblib.load('app/model/model.joblib')
with open('app/model/feature_columns.json', 'r', encoding='utf-8') as f:
    feature_spec = json.load(f)

print(f"Features esperadas pelo modelo:")
print(f"  Numéricas ({len(feature_spec['numeric'])}): {feature_spec['numeric']}")
print(f"  Categóricas ({len(feature_spec['categorical'])}): {feature_spec['categorical']}")
print()

# Garantir que temos todas as features
expected_cols = feature_spec['numeric'] + feature_spec['categorical']
for col in expected_cols:
    if col not in df_output.columns:
        print(f"⚠️ FALTANDO: {col}")
        df_output[col] = None

# Ordenar colunas
df_aligned = df_output[expected_cols]

print("DataFrame alinhado com modelo:")
print(df_aligned.to_string())
print()

# Fazer predição
try:
    proba = model.predict_proba(df_aligned)
    prob_risco = proba[0, 1] * 100
    print(f"✅ Predição bem-sucedida!")
    print(f"   Probabilidade de RISCO: {prob_risco:.1f}%")
except Exception as e:
    print(f"❌ Erro na predição: {e}")
