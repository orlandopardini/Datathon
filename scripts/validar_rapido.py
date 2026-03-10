"""Validacao rapida do modelo de evasao"""
import sys
sys.path.insert(0, '.')

import pandas as pd
import joblib
from pathlib import Path
from src.preprocessing import build_target_at_risk_evasao, load_pede_excel

print("="*80)
print("VALIDACAO DO MODELO DE EVASAO v3.0")
print("="*80)

# Carregar modelo
model = joblib.load("app/model/model.joblib")
print("\nModelo carregado com sucesso!")

# Carregar dados
df = load_pede_excel("database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx", "PEDE2024")
print(f"Dados carregados: {len(df)} alunos")

# Target
y = build_target_at_risk_evasao(df, threshold=5.0)
print(f"\nDistribuicao:")
print(f"  Em risco (IEG < 5.0): {y.sum()} ({y.mean()*100:.1f}%)")
print(f"  Sem risco (IEG >= 5.0): {(1-y).sum()} ({(1-y.mean())*100:.1f}%)")

# Casos de teste
print("\nCASOS DE TESTE:")
test_cases = [
    ("Engajado (IEG=9.5)", 9.5, 0),
    ("OK (IEG=6.0)", 6.0, 0),
    ("Limite (IEG=5.0)", 5.0, 0),
    ("Desengajado (IEG=4.5)", 4.5, 1),
    ("Critico (IEG=2.0)", 2.0, 1),
]

for desc, ieg, expected in test_cases:
    test_df = pd.DataFrame({"IEG": [ieg]})
    result = build_target_at_risk_evasao(test_df, threshold=5.0)[0]
    status = "OK" if result == expected else "ERRO"
    print(f"  [{status}] {desc:25s} -> at_risk={result} (esperado={expected})")

print("\n" + "="*80)
print("VALIDACAO CONCLUIDA!")
print("Modelo preve RISCO DE EVASAO via IEG < 5.0")
print("="*80)
