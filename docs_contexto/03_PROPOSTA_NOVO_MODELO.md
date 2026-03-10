# 🎯 Proposta de Reformulação do Modelo Preditivo

**Data**: 23 Fevereiro 2026  
**Status**: 📋 AGUARDANDO DECISÃO

---

## 🚨 Problema Identificado

O modelo atual **não prevê risco acadêmico**, mas sim **permanência no programa (defasagem cronológica)**.

### Comportamento Atual (PROBLEMÁTICO)
```
Entrada: Aluno Fase 1A, notas (1, 1, 1, 1, 1)
Saída: 4.2% de risco ❌ (esperado: ALTO risco)

Entrada: Aluno Fase 7E, notas (9, 9, 9, 9, 9)
Saída: 76% de risco ❌ (esperado: BAIXO risco)
```

**Causa Raiz**: Target baseado em "Defasagem" que mede tempo no programa, não desempenho.

---

## 🎯 3 Opções de Modelos Preditivos

Apresento 3 abordagens distintas. **Você precisa escolher qual faz mais sentido para a Passos Mágicos.**

---

## Opção A: Modelo de Risco de Desempenho Acadêmico Baixo 📉

**RECOMENDADO** ✅

### Objetivo
Identificar alunos com alto risco de **notas baixas** que precisam de intervenção pedagógica urgente.

### Definição do Target

```python
def build_target_at_risk_academic(df: pd.DataFrame) -> pd.Series:
    """
    Target: Aluno tem risco acadêmico se a média das suas notas for < 6.0
    
    Critério: Média(IEG, IDA, Mat, Por) < 6.0
    """
    notas_cols = ['IEG', 'IDA', 'Mat', 'Por']
    
    # Calcular média (ignorando nulls)
    media_notas = df[notas_cols].mean(axis=1)
    
    # Definir threshold de risco
    THRESHOLD_RISCO = 6.0
    
    return (media_notas < THRESHOLD_RISCO).astype(int)
```

### Comportamento Esperado

| Cenário | IEG | IDA | Mat | Por | Média | at_risk | ✅/❌ |
|---------|-----|-----|-----|-----|-------|---------|-------|
| Aluno excelente | 9.0 | 9.0 | 9.0 | 9.0 | 9.0 | **0** | ✅ Sem risco |
| Aluno médio | 7.0 | 6.5 | 6.0 | 6.5 | 6.5 | **0** | ✅ Sem risco |
| Aluno em risco | 5.0 | 5.5 | 4.0 | 5.0 | 4.875 | **1** | ✅ EM RISCO |
| Aluno crítico | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | **1** | ✅ EM RISCO |

### Features a Utilizar

**✅ INCLUIR** (18 features):
```python
features = [
    # Demográficas (5)
    "Idade",
    "Gênero",
    "Ano ingresso",
    "Instituição de ensino",
    "Fase",  # Indica complexidade do conteúdo
    
    # Indicadores históricos (3)
    "INDE 22",  # Performance passada
    "INDE 23",
    "INDE 2024",
    
    # Indicadores psicossociais (4)
    "IAA",   # Autoavaliação
    "IPS",   # Psicossocial
    "IPP",   # Psicopedagógico
    "IPV",   # Ponto de virada
    
    # Engajamento e suporte (3)
    "IAN",   # Autoavaliação numérica
    "Nº Av", # Número de avaliações (proxy de atenção recebida)
    "Turma", # Contexto da turma
    
    # Features engenheiradas (3)
    "Fase_num",  # Fase convertida para numérico
    "Tempo_programa",  # Anos desde ingresso
    "Idade_ingresso"   # Idade quando entrou
]
```

**❌ NÃO INCLUIR**:
- `IEG, IDA, Mat, Por, Ing` - Serão usadas para **construir o target**
- `Defasagem, Fase Ideal` - Data leakage
- `RA, Nome Anonimizado` - Identificadores
- `Ativo/ Inativo` - Pode vazar informação de evasão

### Distribuição Esperada do Novo Target

Baseado na análise dos dados (médias: IEG=7.37, IDA=6.35, Mat=6.23, Por=6.18):

```python
# Simulação com os dados reais
média_geral = (7.37 + 6.35 + 6.23 + 6.18) / 4 = 6.53

# Estimativa de distribuição (assumindo desvio padrão ~1.5):
# Alunos com média < 6.0: ~35-45%
# Alunos com média >= 6.0: ~55-65%
```

**Balanceamento**: ✅ Melhor que o atual (50/50 é ideal, 40/60 é aceitável)

### Vantagens ✅
1. **Intuitivo**: Notas baixas → Alto risco (faz sentido!)
2. **Acionável**: Educadores sabem o que fazer (reforço nas matérias fracas)
3. **Correlações corretas**: Todas as features deveriam ter sinal esperado
4. **Interpretável**: "Este aluno tem 85% de chance de ter média < 6.0"

### Desvantagens ⚠️
1. **Target construído**: Não é uma variável observada naturalmente
2. **Threshold arbitrário**: Por que 6.0? Poderia ser 5.5 ou 6.5
3. **Não prevê evasão**: Apenas performance acadêmica

### Métricas de Sucesso Esperadas
- **ROC-AUC**: 75-85% (realista para problema de desempenho)
- **Precisão**: 70-80%
- **Recall**: 65-75%
- **F1-Score**: 65-75%

---

## Opção B: Modelo de Risco de Evasão/Desengajamento 🚪

### Objetivo
Identificar alunos com alto risco de **abandonar o programa** ou se desengajar.

### Definição do Target

```python
def build_target_at_risk_evasao(df: pd.DataFrame) -> pd.Series:
    """
    Target: Aluno tem risco de evasão se:
    1. IEG (Indicador de Engajamento) < 5.0  OU
    2. Já está marcado como Inativo
    """
    # Critério 1: Baixo engajamento
    baixo_engajamento = df['IEG'] < 5.0
    
    # Critério 2: Status inativo (se existir na base)
    if 'Ativo/ Inativo' in df.columns:
        inativo = df['Ativo/ Inativo'].str.contains('Inativo', case=False, na=False)
    else:
        inativo = False
    
    return (baixo_engajamento | inativo).astype(int)
```

### Comportamento Esperado

| Cenário | IEG | IDA | Mat | Status | at_risk | Interpretação |
|---------|-----|-----|-----|--------|---------|---------------|
| Alto engajamento | 9.0 | 6.0 | 5.0 | Ativo | **0** | Engajado, sem risco |
| Médio engajamento | 6.5 | 7.0 | 7.0 | Ativo | **0** | Participativo |
| Baixo engajamento | 3.0 | 5.0 | 4.0 | Ativo | **1** | ⚠️ Risco de evasão |
| Já evadiu | 2.0 | - | - | Inativo | **1** | ⚠️ Evasão confirmada |

### Features a Utilizar

**✅ INCLUIR** (20+ features):
```python
features = [
    # TODAS as notas (importantes para prever desengajamento)
    "IDA", "Mat", "Por", "Ing",  # Notas (IEG já está no target)
    
    # Demográficas
    "Idade", "Gênero", "Ano ingresso", "Instituição de ensino",
    
    # Contexto acadêmico
    "Fase", "Turma",
    
    # Indicadores históricos
    "INDE 22", "INDE 23", "INDE 2024",
    
    # Indicadores psicossociais (CRÍTICOS para evasão)
    "IAA", "IPS", "IPP", "IPV", "IAN",
    
    # Suporte recebido
    "Nº Av",  # Alunos com mais avaliações podem ter mais suporte
    
    # Features engenheiradas
    "Fase_num", "Tempo_programa", "Idade_ingresso",
    "Tendencia_notas"  # Notas melhorando ou piorando?
]
```

### Distribuição Esperada do Novo Target

Baseado em IEG < 5.0:

```python
# Análise: IEG tem média 7.37, desvio padrão ~2.0
# Alunos com IEG < 5.0: ~15-20% (estimativa)
```

**Balanceamento**: ⚠️ Desbalanceado (15/85), mas realista para problema de evasão.

### Vantagens ✅
1. **Problema real**: Evasão é crítica para ONGs
2. **Foco em engajamento**: IEG é um bom proxy
3. **Usável**: Permite identificar alunos antes que evadam
4. **Acionável**: Intervenções de reengajamento

### Desvantagens ⚠️
1. **Dados limitados**: Maioria está "Ativo", dificulta treino
2. **Threshold arbitrário**: Por que IEG < 5.0?
3. **Não captura outros motivos**: Pode ter IEG alto mas evadir por questões familiares

### Métricas de Sucesso Esperadas
- **ROC-AUC**: 70-80%
- **Precisão**: 60-70% (aceitável para evasão)
- **Recall**: 70-80% (crítico capturar maioria dos casos)
- **F1-Score**: 65-75%

---

## Opção C: Modelo de Predição de Notas Futuras 🔮

### Objetivo
**Prever a nota futura** do aluno (próximo período/ano), permitindo intervenção antecipada.

### Definição do Target

```python
def build_target_proxima_nota(df: pd.DataFrame) -> pd.Series:
    """
    Target: Média das notas do PRÓXIMO período
    
    REQUER: Dados longitudinais (aluno em múltiplos períodos)
    """
    # Agrupar por aluno
    df_sorted = df.sort_values(['RA', 'Ano ingresso'])
    
    # Pegar nota do próximo ano
    df['proxima_media'] = df.groupby('RA')['media_notas'].shift(-1)
    
    return df['proxima_media']
```

### Tipo de Problema
- **Regressão** (prediz valor numérico 0-10)
- Ou **Classificação Multi-classe** (prediz faixa: 0-4, 4-6, 6-8, 8-10)

### Features a Utilizar

**✅ INCLUIR**:
```python
features = [
    # Notas atuais (todas)
    "IEG", "IDA", "Mat", "Por", "Ing",
    
    # Indicadores atuais
    "INDE 2024", "IAA", "IPS", "IPP", "IPV", "IAN",
    
    # Histórico (CRÍTICO para predizer futuro)
    "INDE 22", "INDE 23",  # Tendência de melhora/piora
    "Pedra 22", "Pedra 23",  # Gamificação
    
    # Demografia e contexto
    "Idade", "Gênero", "Fase", "Instituição de ensino",
    
    # Features temporais
    "Tempo_programa",
    "Taxa_melhora",  # (INDE_2024 - INDE_2022) / 2
    "Consistencia_notas"  # Desvio padrão das notas atuais
]
```

### Vantagens ✅
1. **Altamente acionável**: "Este aluno vai ter nota 4 em Mat ano que vem!"
2. **Métrica clara**: MAE (Mean Absolute Error) = erro médio em pontos
3. **Interpretável**: Educadores entendem "nota prevista"
4. **Permite intervenção antecipada**: 1 ano antes do problema

### Desvantagens ⚠️
1. **REQUER dados longitudinais**: Dataset atual parece ser snapshot (1 foto no tempo)
2. **Complexidade maior**: Precisa rastrear alunos ao longo do tempo
3. **Dados históricos limitados**: Muitos alunos novos sem histórico

### Viabilidade com Dataset Atual
⚠️ **NÃO RECOMENDADO NO MOMENTO**

Razões:
- Dataset parece ser cross-sectional (snapshot de 2024)
- Não há coluna de "período" ou "semestre"
- INDEs históricos têm muitos nulls (40-59%)

**Poderia ser implementado se**:
- Passos Mágicos fornecer dados de múltiplos anos
- Formato: mesmo aluno aparece várias vezes (uma por ano)

### Métricas de Sucesso Esperadas
- **MAE**: ± 0.8-1.2 pontos (erro médio aceitável)
- **R²**: 0.60-0.75 (correlação entre predito e real)

---

## 📊 Comparação das Opções

| Critério | Opção A: Desempenho | Opção B: Evasão | Opção C: Predição |
|----------|---------------------|-----------------|-------------------|
| **Intuitividade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Acionabilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Viabilidade Dados** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ (requer longitudinal) |
| **Balanceamento** | ⭐⭐⭐⭐ (40/60) | ⭐⭐⭐ (15/85) | ⭐⭐⭐⭐⭐ (contínuo) |
| **Complexidade** | ⭐⭐ (baixa) | ⭐⭐⭐ (média) | ⭐⭐⭐⭐ (alta) |
| **Tempo Implementação** | 2-3 dias | 3-4 dias | 5-7 dias + dados |
| **Valor para ONG** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🏆 Recomendação Final

### **OPÇÃO A: Modelo de Risco de Desempenho Acadêmico Baixo** ✅

#### Por que Opção A?

1. **Resolve o problema atual**
   - Correlações ficam corretas (notas baixas → alto risco)
   - Predições fazem sentido intuitivo
   - Dashboard mostra informações úteis

2. **Viável com dados atuais**
   - Não requer dados longitudinais
   - Todas as features estão disponíveis
   - Balanceamento razoável (~40/60)

3. **Altamente acionável**
   - Educadores sabem exatamente o que fazer
   - "Aluno X tem 85% de chance de ter média < 6.0"
   - Permite intervenção em matérias específicas

4. **Implementação rápida**
   - ~2-3 dias de trabalho
   - Aproveita infraestrutura existente
   - Testes podem ser adaptados facilmente

#### Alternativa: Opção B (se objetivo for evasão)

Se a Passos Mágicos prioriza **retenção de alunos** acima de tudo, então Opção B (Evasão) seria melhor.

#### NÃO Recomendo: Opção C

Requer dados que não temos. Pode ser considerada no futuro se:
- Passos Mágicos coletar dados longitudinais
- Formato: mesmo aluno em múltiplos anos
- Investir em pipeline de dados temporal

---

## 🛠 Plano de Implementação (Opção A)

### Fase 1: Preparação (Dia 1)
- [ ] **Decisão confirmada**: Cliente aprova Opção A
- [ ] **Análise de threshold**: Validar se 6.0 é o melhor corte
- [ ] **Análise de balanceamento**: Verificar distribuição real do novo target

### Fase 2: Implementação do Novo Target (Dia 1-2)
- [ ] **Modificar** `src/preprocessing.py`:
  ```python
  def build_target_at_risk_academic(df, threshold=6.0):
      notas_cols = ['IEG', 'IDA', 'Mat', 'Por']
      media = df[notas_cols].mean(axis=1)
      return (media < threshold).astype(int)
  ```
- [ ] **Validar distribuição**: Confirmar ~40/60 ou similar
- [ ] **Teste unitário**: Atualizar `tests/test_preprocessing.py`

### Fase 3: Feature Engineering (Dia 2)
- [ ] **Adicionar features** em `src/feature_engineering.py`:
  ```python
  df['Tempo_programa'] = 2024 - df['Ano ingresso']
  df['Idade_ingresso'] = df['Idade'] - df['Tempo_programa']
  ```
- [ ] **Remover features de notas** da lista de features de treino
- [ ] **Adicionar indicadores históricos** (INDE 22, 23)

### Fase 4: Re-treino do Modelo (Dia 2)
- [ ] **Atualizar** `src/train.py`:
  - Usar novo target
  - Nova lista de features (sem IEG, IDA, Mat, Por)
  - Adicionar INDE, IAA, IPS, IPP
- [ ] **Treinar modelo**: `python -m src.train`
- [ ] **Validar métricas**: ROC-AUC esperado ~75-85%

### Fase 5: Validação Manual (Dia 2-3)
- [ ] **Criar script de teste** `validate_predictions.py`:
  ```python
  # Teste 1: Notas baixas → ALTO risco
  test_low = {..., 'IEG': 1.0, 'IDA': 1.0, 'Mat': 1.0, 'Por': 1.0}
  # Esperado: 80-95% de risco
  
  # Teste 2: Notas altas → BAIXO risco
  test_high = {..., 'IEG': 9.0, 'IDA': 9.0, 'Mat': 9.0, 'Por': 9.0}
  # Esperado: 5-15% de risco
  ```
- [ ] **Executar 10 cenários** de teste
- [ ] **Validar** que todos fazem sentido

### Fase 6: Atualização de Testes (Dia 3)
- [ ] **Atualizar todos testes** em `tests/`:
  - Novos valores esperados para target
  - Novas features
  - Novos cenários de validação
- [ ] **Garantir 81%+ cobertura**

### Fase 7: Atualização de Documentação (Dia 3)
- [ ] **README.md**: Explicar novo modelo ("risco de desempenho baixo")
- [ ] **Dashboard**: Remover nota sobre "defasagem"
- [ ] **API docs**: Atualizar exemplos

### Fase 8: Deploy e Validação Final (Dia 3)
- [ ] **Testar API**: Múltiplos cenários via `/predict`
- [ ] **Testar Dashboard**: Verificar visualizações
- [ ] **Monitoramento**: Verificar logs e drift
- [ ] **Documentar resultados**: Métricas finais

---

## 🎯 Critérios de Sucesso

### Métricas Técnicas
- [ ] **ROC-AUC ≥ 75%** (mínimo aceitável)
- [ ] **Precisão ≥ 70%** (baixo índice de falsos positivos)
- [ ] **Recall ≥ 65%** (capturar maioria dos alunos em risco)
- [ ] **F1-Score ≥ 65%** (balanço geral)

### Validações Qualitativas
- [ ] ✅ Notas BAIXAS (1-3) → Risco ALTO (70-95%)
- [ ] ✅ Notas MÉDIAS (5-7) → Risco MÉDIO (30-70%)
- [ ] ✅ Notas ALTAS (8-10) → Risco BAIXO (5-30%)
- [ ] ✅ Todas correlações com sinal esperado (negativo)

### Aceitação do Cliente
- [ ] Cliente concorda que predições "fazem sentido"
- [ ] Dashboard mostra informações úteis e acionáveis
- [ ] Documentação clara sobre o que o modelo prevê

---

## ❓ Decisão Necessária

**Preciso que você confirme:**

### Qual opção você escolhe?
- [ ] **Opção A**: Risco de Desempenho Acadêmico Baixo (RECOMENDADO)
- [ ] **Opção B**: Risco de Evasão/Desengajamento
- [ ] **Opção C**: Predição de Notas Futuras (requer dados longitudinais)
- [ ] **Outra**: Descrever o que você realmente precisa

### Perguntas para você responder:
1. **Qual o objetivo prioritário da Passos Mágicos com este modelo?**
   - Identificar alunos com desempenho ruim para reforço escolar?
   - Prevenir evasão do programa?
   - Outro?

2. **Qual threshold de "risco" faz sentido?**
   - Média < 6.0? (recomendo)
   - Média < 5.5?
   - Outro critério?

3. **Passos Mágicos tem dados históricos de alunos?**
   - Mesmo aluno em múltiplos anos/períodos?
   - Se sim, posso implementar Opção C

4. **Qual a tolerância para falsos positivos?**
   - Prefere capturar TODOS em risco (recall alto, pode ter falsos positivos)?
   - Ou só alertar quando tiver CERTEZA (precisão alta, pode perder alguns)?

---

## 📞 Próximos Passos

1. **VOCÊ**: Responder as perguntas acima
2. **EU**: Implementar a opção escolhida (2-3 dias)
3. **NÓS**: Validar juntos que faz sentido
4. **DEPLOY**: Novo modelo em produção

---

**Aguardando sua decisão para prosseguir! 🚀**
