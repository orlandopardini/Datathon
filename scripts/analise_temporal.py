"""Análise de dados temporais para modelo de evasão."""
import pandas as pd

# Carregar dados
df = pd.read_excel('database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx', sheet_name='PEDE2024')

print("=" * 80)
print("ANÁLISE DE ESTRUTURA TEMPORAL DOS DADOS")
print("=" * 80)

print("\n📊 Dimensões:")
print(f"   Total de registros: {len(df)}")
print(f"   Alunos únicos (RA): {df['RA'].nunique()}")
print(f"   Registros por aluno: {len(df) / df['RA'].nunique():.2f}")

print("\n📅 Indicadores Temporais (INDE):")
for col in ['INDE 2024', 'INDE 23', 'INDE 22']:
    total = df[col].notna().sum()
    pct = (total / len(df)) * 100
    print(f"   {col:15s}: {total:4d} valores ({pct:5.1f}%)")

print("\n🎓 Status Ativo/Inativo:")
if 'Ativo/ Inativo' in df.columns:
    status_counts = df['Ativo/ Inativo'].value_counts()
    for status, count in status_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {status:15s}: {count:4d} alunos ({pct:5.1f}%)")
else:
    print("   ⚠️  Coluna 'Ativo/ Inativo' não encontrada")

print("\n📋 Indicadores de Engajamento (IEG):")
if 'IEG' in df.columns:
    ieg_stats = df['IEG'].describe()
    print(f"   Média: {ieg_stats['mean']:.2f}")
    print(f"   Min: {ieg_stats['min']:.2f}")
    print(f"   Max: {ieg_stats['max']:.2f}")
    
    # Alunos com baixo engajamento (proxy para risco de evasão)
    baixo_engajamento = (df['IEG'] < 5.0).sum()
    pct = (baixo_engajamento / len(df)) * 100
    print(f"\n   🚨 Alunos com IEG < 5.0: {baixo_engajamento} ({pct:.1f}%)")
    print(f"      → Potencial target para risco de evasão")

print("\n🔍 Conclusão sobre Estrutura Temporal:")
if len(df) == df['RA'].nunique():
    print("   ⚠️  SNAPSHOT: 1 registro por aluno (dados de 2024 apenas)")
    print("   📌 Modelo temporal ano-a-ano: NÃO VIÁVEL")
    print("   ✅ Modelo de risco de evasão via proxy: VIÁVEL")
    print("\n   💡 Estratégia recomendada:")
    print("      Target: evasão = 1 se IEG < 5.0 OU status 'Inativo'")
    print("      Interpretação: Risco de desengajamento/abandono")
else:
    print("   ✅ LONGITUDINAL: Múltiplos registros por aluno")
    print("   ✅ Modelo temporal ano-a-ano: VIÁVEL")

print("\n" + "=" * 80)
