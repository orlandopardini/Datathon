# 📊 Análise Completa da Database PEDE 2024

**Data da Análise**: 23 Fevereiro 2026  
**Fonte**: `BASE DE DADOS PEDE 2024 - DATATHON.xlsx` (Aba: PEDE2024)  
**Total de Registros**: 1.156 alunos

---

## 1. Visão Geral da Database

### Dimensões
- **Linhas (Alunos)**: 1.156
- **Colunas (Features)**: 50
- **Classes Balanceadas**: ❌ Desbalanceado (11.9% em risco, 88.1% não em risco)

### Qualidade dos Dados

| Aspecto | Status | Observação |
|---------|--------|------------|
| Duplicatas | ✅ Não identificadas | RA é único por aluno |
| Valores Faltantes | ⚠️ Presentes | Várias colunas com nulls |
| Tipos de Dados | ⚠️ Mistos | Algumas numéricas vêm como object |
| Outliers | ✅ Aparentemente normais | Notas entre 0-10 |

---

## 2. Catalogação Completa de Colunas

### 2.1 Identificadores (NÃO usar como features)
| # | Coluna | Tipo | Nulls | Descrição |
|---|--------|------|-------|-----------|
| 1 | RA | object | 0 | Registro do Aluno (identificador único) |
| 6 | Nome Anonimizado | object | 0 | Nome do aluno (anonimizado) |

### 2.2 Variável Alvo e Relacionadas
| # | Coluna | Tipo | Nulls | Descrição |
|---|--------|------|-------|-----------|
| 44 | **Defasagem** | int64 | 0 | **Diferença entre Fase atual e Fase ideal** |
| 43 | Fase Ideal | object | 0 | Fase esperada para a idade do aluno |
| 2 | Fase | object | 0 | Fase atual do aluno (1A, 2B, 7E, 9, etc) |

**⚠️ ATENÇÃO**: "Defasagem" NÃO é indicador de desempenho ruim, mas sim de tempo no programa.

### 2.3 Demografia e Informações Básicas
| # | Coluna | Tipo | Nulls | Descrição |
|---|--------|------|-------|-----------|
| 7 | Data de Nasc | datetime | 0 | Data de nascimento |
| 8 | **Idade** | int64 | 0 | Idade atual |
| 9 | **Gênero** | object | 0 | Masculino ou Feminino |
| 10 | **Ano ingresso** | int64 | 0 | Ano de entrada no programa |
| 11 | **Instituição de ensino** | object | 1 | Tipo de escola (Pública, Privada, etc) |
| 48 | Escola | object | 1 | Nome da escola (duplicata?) |

### 2.4 Notas e Indicadores de Desempenho
| # | Coluna | Tipo | Nulls (%) | Descrição |
|---|--------|------|-----------|-----------|
| 31 | **IEG** | float64 | 0 (0.0%) | Indicador de Engajamento |
| 35 | **IDA** | float64 | 101 (8.7%) | Indicador de Autodesenvolvimento |
| 36 | **Mat** | float64 | 105 (9.1%) | Nota de Matemática |
| 37 | **Por** | float64 | 106 (9.2%) | Nota de Português |
| 38 | **Ing** | float64 | 682 (59.0%) | Nota de Inglês ⚠️ muitos nulls |

**Observação**: Inglês tem 59% de nulls - considerar remover ou tratar especialmente.

### 2.5 Indicadores Compostos (INDE)
| # | Coluna | Tipo | Nulls (%) | Descrição |
|---|--------|------|-----------|-----------|
| 3 | INDE 2024 | object | 64 (5.5%) | Índice de Desenvolvimento Educacional 2024 |
| 17 | INDE 23 | float64 | 466 (40.3%) | Índice de Desenvolvimento Educacional 2023 |
| 16 | INDE 22 | float64 | 684 (59.2%) | Índice de Desenvolvimento Educacional 2022 |

### 2.6 Outros Indicadores
| # | Coluna | Tipo | Nulls (%) | Descrição |
|---|--------|------|-----------|-----------|
| 30 | IAA | float64 | 102 (8.8%) | Indicador de Autoavaliação |
| 32 | IPS | float64 | 102 (8.8%) | Indicador Psicossocial |
| 33 | IPP | float64 | 102 (8.8%) | Indicador Psicopedagógico |
| 41 | IPV | float64 | 102 (8.8%) | Indicador de Ponto de Virada |
| 42 | IAN | float64 | 0 (0.0%) | Indicador de Autoavaliação Numérica |

### 2.7 Pedras (Gamificação)
| # | Coluna | Tipo | Nulls (%) | Descrição |
|---|--------|------|-----------|-----------|
| 4 | Pedra 2024 | object | 64 (5.5%) | Classificação/conquista 2024 |
| 15 | Pedra 23 | object | 466 (40.3%) | Classificação 2023 |
| 14 | Pedra 22 | object | 684 (59.2%) | Classificação 2022 |
| 13 | Pedra 21 | object | 892 (77.2%) | Classificação 2021 |
| 12 | Pedra 20 | object | 965 (83.5%) | Classificação 2020 |

### 2.8 Turma e Organização
| # | Coluna | Tipo | Nulls | Descrição |
|---|--------|------|-------|-----------|
| 5 | **Turma** | object | 0 | Código da turma |
| 49 | Ativo/ Inativo | object | 0 | Status do aluno |
| 50 | Ativo/ Inativo.1 | object | 0 | Duplicata? |

### 2.9 Avaliadores (Psicologia/Pedagógico)
| # | Coluna | Tipo | Nulls (%) | Descrição |
|---|--------|------|-----------|-----------|
| 21 | Nº Av | int64 | 0 (0.0%) | Número de avaliações |
| 22 | Avaliador1 | object | 127 (11.0%) | Nome do avaliador 1 |
| 24 | Avaliador2 | object | 127 (11.0%) | Nome do avaliador 2 |
| 26 | Avaliador3 | object | 363 (31.4%) | Nome do avaliador 3 |
| 27 | Avaliador4 | object | 749 (64.8%) | Nome do avaliador 4 |
| 28 | Avaliador5 | object | 1008 (87.2%) | Nome do avaliador 5 |
| 29 | Avaliador6 | object | 1150 (99.5%) | Nome do avaliador 6 |

### 2.10 Colunas Vazias (100% Nulls) - IGNORAR
| # | Coluna | Nulls | Ação |
|---|--------|-------|------|
| 18 | Cg | 100% | ❌ Remover |
| 19 | Cf | 100% | ❌ Remover |
| 20 | Ct | 100% | ❌ Remover |
| 23 | Rec Av1 | 100% | ❌ Remover |
| 25 | Rec Av2 | 100% | ❌ Remover |
| 34 | Rec Psicologia | 100% | ❌ Remover |
| 39 | Indicado | 100% | ❌ Remover |
| 40 | Atingiu PV | 100% | ❌ Remover |
| 45 | Destaque IEG | 100% | ❌ Remover |
| 46 | Destaque IDA | 100% | ❌ Remover |
| 47 | Destaque IPV | 100% | ❌ Remover |

---

## 3. Análise Estatística das Notas

### 3.1 Estatísticas Descritivas

| Nota | Mínimo | Média | Máximo | Desvio Padrão | Nulls |
|------|--------|-------|--------|---------------|-------|
| **IEG** | 0.00 | **7.37** | 10.00 | ~2.0 | 0 |
| **IDA** | 0.00 | **6.35** | 10.00 | ~2.2 | 101 |
| **Mat** | 0.00 | **6.23** | 10.00 | ~2.3 | 105 |
| **Por** | 0.00 | **6.18** | 10.00 | ~2.4 | 106 |
| **Ing** | 0.00 | **6.60** | 10.00 | ~2.1 | 682 |

**Interpretação**:
- IEG tem a **maior média** (7.37) e **sem nulls** ✅
- Mat, Por, Ing têm médias similares (~6.2-6.6)
- Inglês tem **59% de dados faltantes** ⚠️

### 3.2 Correlações das Notas com Target Atual (at_risk baseado em Defasagem)

| Nota | Correlação | Média EM RISCO | Média NÃO EM RISCO | Esperado | Real |
|------|------------|----------------|---------------------|----------|------|
| **IEG** | **-0.154** | 6.18 | 7.54 | ✅ Negativa | ✅ Negativa |
| **IDA** | **+0.084** | 6.91 | 6.29 | ✅ Negativa | ❌ Positiva |
| **Mat** | **+0.030** | 6.49 | 6.20 | ✅ Negativa | ❌ Positiva |
| **Por** | **+0.060** | 6.62 | 6.13 | ✅ Negativa | ❌ Positiva |
| **Ing** | **+0.175** | 7.61 | 6.35 | ✅ Negativa | ❌ Positiva |

**🔴 PROBLEMA CRÍTICO**: 4 de 5 notas têm correlação POSITIVA com "risco" (defasagem).

**Significado**:
- Alunos com **notas ALTAS** têm **MAIOR defasagem**
- Alunos com **notas BAIXAS** têm **MENOR defasagem**
- Isso ocorre porque alunos em fases avançadas (com mais tempo para aprender) têm notas melhores MAS também têm maior defasagem cronológica

---

## 4. Análise por Fase

### 4.1 Top 10 Fases com Maior Taxa de "Risco" (Defasagem)

| Fase | Total | Em Risco | Taxa | IEG Média | Mat Média | Por Média | Interpretação |
|------|-------|----------|------|-----------|-----------|-----------|---------------|
| **9** | 38 | 38 | **100%** | 0.00 | NaN | NaN | Fase FINAL - todos defasados |
| **7E** | 25 | 19 | **76%** | 6.91 | 4.81 | 5.18 | Fase avançada |
| **5C** | 13 | 6 | **46%** | 9.13 | 8.46 | 6.15 | Notas ALTAS mas alta defasagem |
| **5N** | 14 | 6 | **43%** | 9.19 | 7.57 | 6.82 | Notas ALTAS mas alta defasagem |
| **4A** | 15 | 6 | **40%** | 8.34 | 6.47 | 6.87 | Notas boas com defasagem |
| **3K** | 16 | 6 | **38%** | 8.32 | 6.34 | 5.78 | Notas boas com defasagem |
| **3B** | 16 | 5 | **31%** | 7.50 | 5.16 | 5.13 | - |
| **4M** | 18 | 5 | **28%** | 7.86 | 5.89 | 6.25 | - |
| **4F** | 16 | 4 | **25%** | 7.60 | 3.81 | 6.19 | - |
| **3U** | 16 | 4 | **25%** | 7.06 | 5.66 | 5.25 | - |

### 4.2 Fases com ZERO Risco (Defasagem = 0)

| Fase | Total | IEG Média | Mat Média | Por Média | Observação |
|------|-------|-----------|-----------|-----------|------------|
| **ALFA** | 196 | 8.50 | 7.85 | 6.79 | Fase inicial - maioria aqui |
| **Todas 1A-1R** | ~200 | 8.00-9.35 | 5.46-8.47 | 5.03-7.50 | Fases iniciais |
| **6A, 6L** | 25 | 8.35-9.27 | 6.29-7.92 | 5.35-6.88 | Fases intermediárias |
| **Todas 8A-8F** | ~64 | 0.00 | NaN/7.00 | NaN/7.00 | Fases finais sem defasagem |

**Padrão Descoberto**:
1. **Fases iniciais (ALFA, 1*, 2*)**: 0-9% defasagem
2. **Fases intermediárias (3*, 4*, 5*)**: 7-46% defasagem
3. **Fases avançadas (7E, 9)**: 76-100% defasagem

**Conclusão**: Defasagem está fortemente correlacionada com **tempo no programa**, NÃO com **desempenho acadêmico**.

---

## 5. Análise de Outras Variáveis

### 5.1 Distribuição de Gênero

| Gênero | Total | Percentual |
|--------|-------|------------|
| Feminino | 623 | 53.9% |
| Masculino | 533 | 46.1% |

**Balanceamento**: ✅ Equilibrado

### 5.2 Tipo de Instituição de Ensino

| Instituição | Total | Percentual |
|-------------|-------|------------|
| Escola Pública | 913 | 79.0% |
| Privada - Programa de Apadrinhamento | 95 | 8.2% |
| Privada | 76 | 6.6% |
| Privada com Bolsa 100% | 41 | 3.5% |
| Bolsista Universitário Formado | 13 | 1.1% |
| Outros | 18 | 1.6% |

**Observação**: 79% dos alunos vêm de escolas públicas.

### 5.3 Distribuição de Idade

| Faixa Etária | Total Aproximado | Fases Típicas |
|--------------|------------------|---------------|
| 7-10 anos | ~300 | ALFA, 1*, 2* |
| 11-14 anos | ~500 | 3*, 4*, 5* |
| 15-18 anos | ~300 | 6*, 7*, 8*, 9 |
| 19+ anos | ~56 | 9 (mayormente) |

### 5.4 Ano de Ingresso

| Ano | Total Aproximado | Observação |
|-----|------------------|------------|
| 2024 | ~100 | Novos alunos |
| 2023 | ~150 | 1 ano no programa |
| 2022 | ~180 | 2 anos |
| 2021 | ~200 | 3 anos |
| 2020 e anterior | ~526 | 4+ anos (maior defasagem) |

**Correlação**: Alunos com mais tempo no programa tendem a ter maior defasagem.

---

## 6. Análise de Indicadores Compostos

### 6.1 Correlações dos INDE com Target Atual

| Indicador | Correlação | Interpretação |
|-----------|------------|---------------|
| INDE 2024 | **+0.203** | ❌ Positiva (invertido) |
| INDE 23 | **+0.223** | ❌ Positiva (invertido) |
| INDE 22 | **+0.350** | ❌ Positiva (invertido) |
| IAA | **+0.046** | ❌ Positiva (invertido) |
| IPS | **+0.013** | ❌ Positiva (invertido) |
| IPP | **+0.130** | ❌ Positiva (invertido) |
| IPV | **+0.184** | ❌ Positiva (invertido) |
| IAN | **+0.339** | ❌ Positiva (invertido) |

**🔴 TODOS os indicadores têm correlação POSITIVA com defasagem!**

**Significado**: Alunos com melhores indicadores de desenvolvimento tendem a estar há mais tempo no programa (maior defasagem cronológica).

---

## 7. Problemas Identificados para Modelagem de Risco Acadêmico

### 7.1 Problema #1: Target Incorreto
- **Current**: `at_risk = Defasagem > 0` (mede tempo no programa)
- **Needed**: Target que meça desempenho ou risco de evasão

### 7.2 Problema #2: Correlações Invertidas
- 80% das features de desempenho têm correlação **OPOSTA** ao esperado
- Modelo aprende padrões de "permanência", não de "risco acadêmico"

### 7.3 Problema #3: Dados Faltantes
- Inglês: 59% nulls
- INDE históricos: 40-59% nulls
- Múltiplas colunas 100% vazias

### 7.4 Problema #4: Features com Data Leakage
- "Fase Ideal" é derivada de Defasagem (vazamento de informação)
- "Defasagem" é calculada a partir de Fase e Idade

---

## 8. Recomendações para Novo Modelo

### 8.1 Opção A: Modelo de Risco de Desempenho Acadêmico Ruim

**Objetivo**: Identificar alunos com risco de notas baixas

**Target Proposto**:
```python
# Definir threshold de risco: média das notas < 6.0
media_notas = (IEG + IDA + Mat + Por) / 4
at_risk_academic = (media_notas < 6.0).astype(int)
```

**Features**:
- **Demográficas**: Idade, Gênero, Ano ingresso, Instituição
- **Features derivadas**: Fase_num, Tempo_no_programa
- **Indicadores históricos**: INDE 22, INDE 23 (se disponíveis)
- **Outras**: Nº Av, IAA, IPS, IPP

**❌ NÃO incluir**: IEG, IDA, Mat, Por, Ing (seriam usadas para criar o target)

### 8.2 Opção B: Modelo de Risco de Evasão/Desengajamento

**Objetivo**: Identificar alunos com risco de abandonar o programa

**Target Proposto**:
```python
# Usar status "Ativo/ Inativo" + baixo engajamento
at_risk_evasao = (
    (IEG < 5.0) |  # Baixo engajamento
    (status == "Inativo")
).astype(int)
```

**Features**:
- Todas as notas (IEG, IDA, Mat, Por, Ing)
- Demografia
- Histórico de INDEs
- Fase, Turma, Ano ingresso

### 8.3 Opção C: Modelo de Predição de Notas

**Objetivo**: Prever a próxima nota do aluno

**Target**: Nota do próximo período (requer dados longitudinais)

**Abordagem**: Regressão em vez de classificação

---

## 9. Features Recomendadas por Tipo de Modelo

### Para Modelo de Risco Acadêmico (Opção A)

| Feature | Tipo | Importância | Justificativa |
|---------|------|-------------|---------------|
| Idade | Numérica | 🔴 Alta | Correlação com maturidade |
| Fase_num | Numérica | 🔴 Alta | Nível de complexidade do conteúdo |
| Gênero | Categórica | 🟡 Média | Padrões de desempenho podem variar |
| Instituição | Categórica | 🔴 Alta | Qualidade da escola base |
| Ano ingresso | Numérica | 🟡 Média | Tempo de adaptação |
| INDE 22/23 | Numérica | 🔴 Alta | Performance histórica |
| IAA | Numérica | 🟡 Média | Autoavaliação |
| IPS | Numérica | 🔴 Alta | Fatores psicossociais |
| IPP | Numérica | 🔴 Alta | Fatores psicopedagógicos |
| Nº Av | Numérica | 🟡 Média | Quantidade de suporte |

### Para Modelo de Permanência/Defasagem (Atual)

| Feature | Tipo | Importância | Justificativa |
|---------|------|-------------|---------------|
| Fase_num | Numérica | 🔴 Alta | Correlação direta (0.7+) |
| Idade | Numérica | 🔴 Alta | Define Fase Ideal |
| Ano ingresso | Numérica | 🔴 Alta | Tempo no programa |
| IEG | Numérica | 🟢 Baixa | Correlação fraca |
| IDA, Mat, Por, Ing | Numérica | 🟢 Baixa | Correlação invertida |

---

## 10. Plano de Ação Sugerido

### Passo 1: Decidir o Problema Real
- [ ] O que você REALMENTE quer prever?
  - Risco de desempenho ruim? (Notas baixas)
  - Risco de evasão do programa?
  - Permanência no programa? (modelo atual)

### Passo 2: Criar Novo Target
- [ ] Definir critério claro de "em risco"
- [ ] Validar que o target faz sentido de negócio
- [ ] Verificar balanceamento das classes

### Passo 3: Selecionar Features Adequadas
- [ ] Remover features com data leakage
- [ ] Tratar dados faltantes (Inglês)
- [ ] Engenharia de features (tempo no programa, tendências, etc)

### Passo 4: Re-treinar Modelo
- [ ] Usar novo target
- [ ] Validar correlações fazem sentido
- [ ] Testar predições manualmente

### Passo 5: Atualizar Infraestrutura
- [ ] Atualizar testes
- [ ] Re-escrever documentação
- [ ] Ajustar dashboard

---

## 11. Conclusão da Análise

### O Que Aprendemos

1. **Defasagem ≠ Risco Acadêmico**
   - Defasagem mede tempo no programa, não performance
   - 100% dos alunos da Fase 9 têm defasagem (são os mais velhos)
   - 0% dos alunos ALFA/Fase 1 têm defasagem (são os mais novos)

2. **Correlações Mostram o Problema**
   - Notas ALTAS → Maior defasagem (correlação positiva)
   - Isso ocorre porque alunos mais velhos tiveram mais tempo para aprender
   - Modelo atual está CORRETO para prever permanência, ERRADO para prever risco acadêmico

3. **Database É Rica Mas Mal Utilizada**
   - 50 colunas disponíveis
   - Apenas 11 sendo usadas
   - Muitos indicadores históricos (INDE, Pedras) ignorados
   - 11 colunas completamente vazias (100% nulls)

### Próximo Documento

Ver `03_PROPOSTA_NOVO_MODELO.md` para proposta detalhada de reformulação com 3 opções de modelos preditivos.
