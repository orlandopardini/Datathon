"""
Script de Validação Manual do Novo Modelo Acadêmico
Testa se predições fazem sentido: notas baixas → alto risco, notas altas → baixo risco
"""
import joblib
import pandas as pd
import numpy as np

print("="*80)
print("VALIDAÇÃO DO MODELO ACADÊMICO")
print("="*80)

# Carregar modelo
model = joblib.load('app/model/model.joblib')

# Cenários de teste
cenarios = [
    {
        "nome": "Aluno EXCELENTE (todas notas 9-10)",
        "dados": {
            'Idade': 12, 'Gênero': 'Feminino', 'Ano ingresso': 2020,
            'Instituição de ensino': 'Pública', 'Fase': '3A', 'Turma': '3A',
            'INDE 22': 8.0, 'INDE 23': 8.5, 'INDE 2024': 9.0,
            'IAA': 9.0, 'IPS': 8.5, 'IPP': 8.5, 'IPV': 8.0, 'IAN': 9.0,
            'Nº Av': 2, 'Fase_num': 3.0, 'Tempo_programa': 4, 'Idade_ingresso': 8
        },
        "esperado": "BAIXO risco (5-20%)"
    },
    {
        "nome": "Aluno BOM (notas 7-8)",
        "dados": {
            'Idade': 13, 'Gênero': 'Masculino', 'Ano ingresso': 2021,
            'Instituição de ensino': 'Pública', 'Fase': '2B', 'Turma': '2B',
            'INDE 22': 7.0, 'INDE 23': 7.2, 'INDE 2024': 7.5,
            'IAA': 7.5, 'IPS': 7.0, 'IPP': 7.0, 'IPV': 7.0, 'IAN': 7.5,
            'Nº Av': 2, 'Fase_num': 2.0, 'Tempo_programa': 3, 'Idade_ingresso': 10
        },
        "esperado": "BAIXO-MÉDIO risco (20-40%)"
    },
    {
        "nome": "Aluno MEDIANO (notas 6-6.5)",
        "dados": {
            'Idade': 14, 'Gênero': 'Feminino', 'Ano ingresso': 2022,
            'Instituição de ensino': 'Pública', 'Fase': '3C', 'Turma': '3C',
            'INDE 22': 6.5, 'INDE 23': 6.3, 'INDE 2024': 6.2,
            'IAA': 6.5, 'IPS': 6.0, 'IPP': 6.0, 'IPV': 6.0, 'IAN': 6.5,
            'Nº Av': 2, 'Fase_num': 3.0, 'Tempo_programa': 2, 'Idade_ingresso': 12
        },
        "esperado": "MÉDIO risco (40-60%)"
    },
    {
        "nome": "Aluno FRACO (notas 4-5)",
        "dados": {
            'Idade': 11, 'Gênero': 'Masculino', 'Ano ingresso': 2023,
            'Instituição de ensino': 'Pública', 'Fase': '1B', 'Turma': '1B',
            'INDE 22': np.nan, 'INDE 23': 5.0, 'INDE 2024': 4.8,
            'IAA': 5.0, 'IPS': 5.0, 'IPP': 5.0, 'IPV': 5.0, 'IAN': 5.0,
            'Nº Av': 2, 'Fase_num': 1.0, 'Tempo_programa': 1, 'Idade_ingresso': 10
        },
        "esperado": "ALTO risco (60-85%)"
    },
    {
        "nome": "Aluno CRÍTICO (todas notas 1-3)",
        "dados": {
            'Idade': 10, 'Gênero': 'Feminino', 'Ano ingresso': 2023,
            'Instituição de ensino': 'Pública', 'Fase': '1A', 'Turma': '1A',
            'INDE 22': np.nan, 'INDE 23': np.nan, 'INDE 2024': 3.5,
            'IAA': 3.0, 'IPS': 3.0, 'IPP': 3.0, 'IPV': 3.0, 'IAN': 3.0,
            'Nº Av': 3, 'Fase_num': 1.0, 'Tempo_programa': 1, 'Idade_ingresso': 9
        },
        "esperado": "MUITO ALTO risco (85-99%)"
    },
    {
        "nome": "Aluno AVANÇADO mas com notas BAIXAS",
        "dados": {
            'Idade': 16, 'Gênero': 'Masculino', 'Ano ingresso': 2019,
            'Instituição de ensino': 'Pública', 'Fase': '5A', 'Turma': '5A',
            'INDE 22': 5.5, 'INDE 23': 5.3, 'INDE 2024': 5.0,
            'IAA': 5.0, 'IPS': 5.0, 'IPP': 5.0, 'IPV': 5.0, 'IAN': 5.0,
            'Nº Av': 4, 'Fase_num': 5.0, 'Tempo_programa': 5, 'Idade_ingresso': 11
        },
        "esperado": "ALTO risco (70-90%) - Fase avançada com desempenho ruim"
    },
    {
        "nome": "Aluno INICIAL com notas ALTAS",
        "dados": {
            'Idade': 8, 'Gênero': 'Feminino', 'Ano ingresso': 2023,
            'Instituição de ensino': 'Privada', 'Fase': 'ALFA', 'Turma': 'ALFA',
            'INDE 22': np.nan, 'INDE 23': np.nan, 'INDE 2024': 8.5,
            'IAA': 8.5, 'IPS': 8.0, 'IPP': 8.0, 'IPV': 8.0, 'IAN': 8.5,
            'Nº Av': 2, 'Fase_num': 0.0, 'Tempo_programa': 1, 'Idade_ingresso': 7
        },
        "esperado": "BAIXO risco (5-20%) - Início do programa com bom desempenho"
    }
]

# Testar cada cenário
resultados = []
for i, cenario in enumerate(cenarios, 1):
    print(f"\n{'='*80}")
    print(f"TESTE {i}: {cenario['nome']}")
    print(f"{'='*80}")
    
    # Criar DataFrame
    df_test = pd.DataFrame([cenario['dados']])
    
    # Fazer predição
    try:
        proba = model.predict_proba(df_test)[0]
        pred = model.predict(df_test)[0]
        
        prob_sem_risco = proba[0] * 100
        prob_em_risco = proba[1] * 100
        
        print(f"Dados de entrada:")
        print(f"  - Fase: {cenario['dados']['Fase']}, Idade: {cenario['dados']['Idade']}, Tempo programa: {cenario['dados']['Tempo_programa']} anos")
        print(f"  - INDEs: 2022={cenario['dados']['INDE 22']}, 2023={cenario['dados']['INDE 23']}, 2024={cenario['dados']['INDE 2024']}")
        print(f"  - Indicadores: IAA={cenario['dados']['IAA']}, IPS={cenario['dados']['IPS']}, IPP={cenario['dados']['IPP']}")
        
        print(f"\n📊 PREDIÇÃO:")
        print(f"  Probabilidade SEM RISCO: {prob_sem_risco:.1f}%")
        print(f"  Probabilidade EM RISCO:  {prob_em_risco:.1f}%")
        print(f"  Classificação: {'⚠️ EM RISCO' if pred == 1 else '✅ SEM RISCO'}")
        
        print(f"\n✅ ESPERADO: {cenario['esperado']}")
        
        # Avaliar se está correto
        if "MUITO ALTO" in cenario['esperado'] or "CRÍTICO" in cenario['nome']:
            correto = prob_em_risco >= 85
        elif "ALTO" in cenario['esperado'] and "BAIXO" not in cenario['esperado']:
            correto = prob_em_risco >= 60
        elif "MÉDIO" in cenario['esperado']:
            correto = 40 <= prob_em_risco <= 60
        elif "BAIXO" in cenario['esperado']:
            correto = prob_em_risco <= 40
        else:
            correto = True
        
        status = "✅ CORRETO" if correto else "❌ INCORRETO"
        print(f"\n{status}")
        
        resultados.append({
            'cenario': cenario['nome'],
            'prob_risco': prob_em_risco,
            'esperado': cenario['esperado'],
            'correto': correto
        })
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        resultados.append({
            'cenario': cenario['nome'],
            'prob_risco': None,
            'esperado': cenario['esperado'],
            'correto': False
        })

# Resumo final
print("\n\n" + "="*80)
print("RESUMO DA VALIDAÇÃO")
print("="*80)

corretos = sum(1 for r in resultados if r['correto'])
total = len(resultados)

print(f"\n✅ Cenários CORRETOS: {corretos}/{total} ({corretos/total*100:.1f}%)")
print(f"❌ Cenários INCORRETOS: {total - corretos}/{total}\n")

print("Detalhes:")
print("-" * 80)
for r in resultados:
    if r['prob_risco'] is not None:
        status = "✅" if r['correto'] else "❌"
        print(f"{status} {r['cenario'][:40]:40s} | Risco: {r['prob_risco']:5.1f}% | Esperado: {r['esperado']}")
    else:
        print(f"❌ {r['cenario'][:40]:40s} | ERRO na predição")

print("\n" + "="*80)
if corretos == total:
    print("🎉 VALIDAÇÃO 100% SUCESSO! Modelo está funcionando perfeitamente!")
elif corretos >= total * 0.8:
    print("✅ VALIDAÇÃO APROVADA! Modelo está funcionando bem (≥80% correto).")
else:
    print("⚠️ ATENÇÃO! Modelo precisa de ajustes.")
print("="*80)
