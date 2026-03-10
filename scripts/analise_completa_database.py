"""
Análise Completa da Database PEDE 2024
Objetivo: Entender a estrutura, correlações e padrões dos dados
"""
import pandas as pd
import numpy as np

# Carregar dados
data_path = r'C:\Users\orlando.gardezani\Downloads\datathon\database\BASE DE DADOS PEDE 2024 - DATATHON.xlsx'
df = pd.read_excel(data_path, sheet_name='PEDE2024')

print("="*100)
print("1. ESTRUTURA GERAL DOS DADOS")
print("="*100)
print(f"Total de registros: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")
print(f"\nPrimeiras 5 colunas: {list(df.columns[:5])}")
print(f"\nÚltimas 5 colunas: {list(df.columns[-5:])}")

print("\n" + "="*100)
print("2. COLUNAS DISPONÍVEIS")
print("="*100)
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    n_nulls = df[col].isna().sum()
    pct_nulls = n_nulls / len(df) * 100
    print(f"{i:2d}. {col:30s} | Tipo: {str(dtype):10s} | Nulls: {n_nulls:4d} ({pct_nulls:5.1f}%)")

print("\n" + "="*100)
print("3. ANÁLISE DA VARIÁVEL ALVO: DEFASAGEM")
print("="*100)
if 'Defasagem' in df.columns:
    print("\nDistribuição da Defasagem:")
    print(df['Defasagem'].describe())
    print(f"\nValores únicos: {sorted(df['Defasagem'].dropna().unique())}")
    print(f"\nContagem por valor:")
    print(df['Defasagem'].value_counts().sort_index())
    
    # Criar target binário
    df['at_risk'] = (df['Defasagem'] > 0).astype(int)
    print(f"\n✅ Target binário criado: at_risk = 1 quando Defasagem > 0")
    print(f"   - Em risco (Defasagem > 0): {df['at_risk'].sum()} alunos ({df['at_risk'].mean():.1%})")
    print(f"   - Não em risco (Defasagem <= 0): {(1-df['at_risk']).sum()} alunos ({(1-df['at_risk']).mean():.1%})")

print("\n" + "="*100)
print("4. VARIÁVEIS NUMÉRICAS: NOTAS E INDICADORES")
print("="*100)

# Identificar colunas de notas e indicadores
notas_cols = ['IEG', 'IDA', 'Mat', 'Por', 'Ing']
indicadores = ['INDE 2024', 'INDE 23', 'INDE 22', 'IAA', 'IPS', 'IPP', 'IPV', 'IAN']

print("\nNOTAS PRINCIPAIS:")
for col in notas_cols:
    if col in df.columns:
        stats = df[col].describe()
        print(f"\n{col}:")
        print(f"  Min: {stats['min']:.2f} | Média: {stats['mean']:.2f} | Max: {stats['max']:.2f} | Nulls: {df[col].isna().sum()}")

print("\n\nINDICADORES:")
for col in indicadores:
    if col in df.columns:
        # Converter para numérico antes de calcular estatísticas
        df[col] = pd.to_numeric(df[col], errors='coerce')
        stats = df[col].describe()
        if 'mean' in stats.index:
            print(f"\n{col}:")
            print(f"  Min: {stats['min']:.2f} | Média: {stats['mean']:.2f} | Max: {stats['max']:.2f} | Nulls: {df[col].isna().sum()}")

print("\n" + "="*100)
print("5. CORRELAÇÕES COM O TARGET (at_risk)")
print("="*100)

if 'at_risk' in df.columns:
    print("\nCorrelações das NOTAS com at_risk:")
    print("-" * 60)
    for col in notas_cols:
        if col in df.columns:
            # Limpar dados para correlação
            valid_data = df[[col, 'at_risk']].dropna()
            if len(valid_data) > 0:
                corr = valid_data[col].corr(valid_data['at_risk'])
                
                # Médias por grupo
                media_risco = df[df['at_risk'] == 1][col].mean()
                media_sem_risco = df[df['at_risk'] == 0][col].mean()
                
                interpretacao = "✅ Negativa (esperado: notas altas → baixo risco)" if corr < 0 else "❌ Positiva (invertido: notas altas → alto risco)"
                print(f"{col:10s} | Corr: {corr:+.3f} | {interpretacao}")
                print(f"            Média EM RISCO: {media_risco:.2f} | Média SEM RISCO: {media_sem_risco:.2f}")
    
    print("\n\nCorrelações dos INDICADORES com at_risk:")
    print("-" * 60)
    for col in indicadores:
        if col in df.columns:
            valid_data = df[[col, 'at_risk']].dropna()
            if len(valid_data) > 0:
                corr = valid_data[col].corr(valid_data['at_risk'])
                interpretacao = "✅ Negativa" if corr < 0 else "❌ Positiva"
                print(f"{col:15s} | Corr: {corr:+.3f} | {interpretacao}")

print("\n" + "="*100)
print("6. ANÁLISE POR FASE")
print("="*100)

if 'Fase' in df.columns and 'at_risk' in df.columns:
    fase_analysis = df.groupby('Fase').agg({
        'at_risk': ['count', 'sum', 'mean'],
        'IEG': 'mean',
        'Mat': 'mean',
        'Por': 'mean'
    }).round(2)
    fase_analysis.columns = ['Total', 'Em_Risco', 'Taxa_Risco', 'IEG_Média', 'Mat_Média', 'Por_Média']
    fase_analysis['Taxa_Risco'] = (fase_analysis['Taxa_Risco'] * 100).round(1)
    print(fase_analysis.to_string())

print("\n" + "="*100)
print("7. VARIÁVEIS CATEGÓRICAS IMPORTANTES")
print("="*100)

categoricas_importantes = ['Fase', 'Turma', 'Gênero', 'Instituição de ensino', 'Ativo/ Inativo']
for col in categoricas_importantes:
    if col in df.columns:
        print(f"\n{col}:")
        print(f"  Valores únicos: {df[col].nunique()}")
        print(f"  Top 5 valores:")
        print(df[col].value_counts().head().to_string())

print("\n" + "="*100)
print("8. CONCLUSÕES E RECOMENDAÇÕES")
print("="*100)

print("\n📊 ACHADOS PRINCIPAIS:")
print("1. A variável 'Defasagem' está sendo usada como target (> 0 = em risco)")
print("2. Verificar se as correlações fazem sentido para o negócio")
print("3. Identificar quais features realmente importam para predição de RISCO ACADÊMICO")

print("\n❓ QUESTÕES CRÍTICAS:")
print("1. O que 'Defasagem' realmente significa?")
print("   - É defasagem de fase/série em relação à idade?")
print("   - Ou é risco de evasão/baixo desempenho?")
print("2. Se alunos com NOTAS ALTAS têm ALTA defasagem, o target está correto?")
print("3. O modelo deveria prever:")
print("   a) Risco de estar atrasado em relação à série ideal (permanência)?")
print("   b) Risco de desempenho acadêmico ruim (notas baixas)?")
print("   c) Risco de evasão/abandono do programa?")

print("\n💡 PRÓXIMOS PASSOS SUGERIDOS:")
print("1. Redefinir o target baseado no objetivo real do negócio")
print("2. Se o objetivo é prever desempenho ruim:")
print("   - Criar target baseado em notas, não em Defasagem")
print("   - Exemplo: at_risk = média(IEG, IDA, Mat, Por, Ing) < 6.0")
print("3. Se o objetivo é prever permanência/defasagem:")
print("   - Manter target atual, mas remover notas das features")
print("   - Usar apenas: Fase, Idade, Ano ingresso, dados demográficos")
