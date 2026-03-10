# 📚 Documentação de Contexto - Análise e Reformulação do Modelo

Esta pasta contém toda a documentação técnica do projeto, desde a análise inicial até a implementação MLOps.

---

## 📄 Índice de Documentos

### 🔍 Análise Inicial (Contexto Histórico)

#### 1. [`01_CONTEXTO_ATUAL.md`](01_CONTEXTO_ATUAL.md)
**Descrição**: Análise completa do estado atual do projeto  
**Conteúdo**:
- Estrutura do projeto e arquivos
- Tecnologias e versões utilizadas
- Estado atual do modelo e métricas
- Problema conceitual identificado
- Tentativas anteriores de correção
- Infraestrutura e testes

**Quando ler**: Primeiro documento - entender o que tínhamos originalmente

---

#### 2. [`02_ANALISE_DATABASE.md`](02_ANALISE_DATABASE.md)
**Descrição**: Análise detalhada da database PEDE 2024  
**Conteúdo**:
- Catalogação completa das 50 colunas
- Estatísticas descritivas de todas as variáveis
- Correlações entre features e target
- Análise por Fase e outros segmentos
- Identificação de dados faltantes
- Problemas identificados para modelagem

**Quando ler**: Segundo documento - entender os dados disponíveis

---

#### 3. [`03_PROPOSTA_NOVO_MODELO.md`](03_PROPOSTA_NOVO_MODELO.md)
**Descrição**: Proposta de reformulação com 3 opções de modelos  
**Conteúdo**:
- **Opção A**: Modelo de Risco de Desempenho Acadêmico (RECOMENDADO)
- **Opção B**: Modelo de Risco de Evasão/Desengajamento
- **Opção C**: Modelo de Predição de Notas Futuras
- Comparação detalhada das opções
- Plano de implementação completo
- Critérios de sucesso

**Quando ler**: Terceiro documento - entender as opções de redesign

---

### 🚀 Modelo Implementado (v3.0 - Risco de Evasão)

#### 4. [`MODELO_EVASAO_README.md`](MODELO_EVASAO_README.md) ⭐
**Descrição**: Documentação completa do modelo v3.0 de predição de risco de evasão  
**Conteúdo**:
- **Target**: IEG < 5.0 = risco de evasão (14.4% dos alunos)
- **Features**: 22 features (IDA, Mat, Por, Ing como preditores)
- **Métricas**: ROC-AUC 99.5%, Accuracy 97.0%, Recall 81.8%
- **Motivação**: Engajamento prediz evasão escolar
- **Uso**: Como fazer predições via API
- **Limitações**: Dados snapshot 2024 (sem histórico longitudinal)

**Quando ler**: Para entender o modelo atual em produção

---

#### 5. [`REDESIGN_COMPLETO.md`](REDESIGN_COMPLETO.md)
**Descrição**: Resumo técnico de todas as mudanças do redesign v2.0 → v3.0  
**Conteúdo**:
- Análise temporal dos dados (descoberta: dados snapshot)
- Mudança de target: desempenho acadêmico → risco de evasão
- Alterações de código (src/, tests/, app/)
- Resultados de treinamento e testes
- Documentação criada
- Próximos passos

**Quando ler**: Para entender o histórico de mudanças

---

### 🛠️ MLOps e Operação

#### 6. [`ESTRATEGIA_RETREINO_MLOPS.md`](ESTRATEGIA_RETREINO_MLOPS.md) ⭐
**Descrição**: Estratégia completa de retreino e operação MLOps (400+ linhas)  
**Conteúdo**:
- **Quando retreinar**: 4 triggers (Drift PSI>0.25, Performance drop, Calendar, Volume)
- **Como retreinar**: Pipeline de 10 passos com validações
- **Validação**: Critérios mínimos (ROC-AUC ≥ 99.5%, Accuracy ≥ 95%, Recall ≥ 75%)
- **Métricas de produção**: Taxa de intervenção, taxa de sucesso, FP tolerance
- **Data contracts**: Esquema Pydantic com validadores
- **Monitoramento**: Dashboard com alertas automáticos
- **Rollback**: Plano de recuperação <5 minutos

**Quando ler**: Para operacionalizar o modelo em produção

---

#### 7. [`MLOPS_IMPLEMENTATION.md`](MLOPS_IMPLEMENTATION.md) ⭐
**Descrição**: Checklist completo de implementação MLOps (4/4 concluído)  
**Conteúdo**:
1. ✅ **Estratégia de Retreino** - Documentada em ESTRATEGIA_RETREINO_MLOPS.md
2. ✅ **Data Contracts** - Implementado em scripts/validar_data_contracts.py
3. ✅ **Métricas de Produção** - Dashboard Streamlit em monitoring/producao_dashboard.py
4. ✅ **Pipeline Automatizado** - Scripts de backup/restore/retreino automatizados

**Arquivos criados**:
- scripts/validar_data_contracts.py
- scripts/backup_modelo.py
- scripts/restaurar_backup.py
- scripts/retreino_automatizado.py
- monitoring/producao_dashboard.py
- procedures/retreino.bat, dashboard-producao.bat

**Como usar**: Guia completo de comandos para retreino, monitoramento e rollback

**Quando ler**: Para entender a infraestrutura MLOps completa

---

### 📋 Guias de Uso

#### 8. [`GUIA_CAMPOS_FORMULARIO.md`](GUIA_CAMPOS_FORMULARIO.md)
**Descrição**: Guia explicativo de todos os campos do formulário  
**Uso**: Referência para preenchimento do formulário web

---

#### 9. [`TUTORIAL_USO_FORMULARIO.md`](TUTORIAL_USO_FORMULARIO.md)
**Descrição**: Tutorial passo-a-passo para usar o sistema  
**Uso**: Onboarding de novos usuários

---

### 📊 Status e Organização

#### 10. [`ORGANIZACAO_PROJETO.md`](ORGANIZACAO_PROJETO.md)
**Descrição**: Estrutura de pastas e arquivos do projeto  
**Uso**: Entender onde cada coisa está

---

#### 11. [`STATUS_TESTES.md`](STATUS_TESTES.md)
**Descrição**: Status dos testes unitários e integração  
**Uso**: Verificar cobertura e qualidade do código

---

#### 12. [`RESUMO_EXECUTIVO.md`](RESUMO_EXECUTIVO.md)
**Descrição**: Resumo executivo para stakeholders não-técnicos  
**Uso**: Apresentação para gestores e parceiros

---

### 📜 Arquivos Auxiliares

- [`passo_a_passo.txt`](passo_a_passo.txt) - Notas de desenvolvimento
- [`regras.txt`](regras.txt) - Regras de negócio

---

## 🗺️ Fluxo de Leitura Recomendado

### Para Desenvolvedores (Novo no Projeto)
1. ✅ `01_CONTEXTO_ATUAL.md` - Entender o histórico
2. ✅ `02_ANALISE_DATABASE.md` - Entender os dados
3. ✅ `MODELO_EVASAO_README.md` - Entender o modelo atual
4. ✅ `MLOPS_IMPLEMENTATION.md` - Entender a infraestrutura

### Para MLOps / DevOps
1. ✅ `MODELO_EVASAO_README.md` - O que o modelo faz
2. ✅ `ESTRATEGIA_RETREINO_MLOPS.md` - Como retreinar
3. ✅ `MLOPS_IMPLEMENTATION.md` - Pipeline completo
4. ✅ [`../scripts/README.md`](../scripts/README.md) - Scripts disponíveis

### Para Gestores / Stakeholders
1. ✅ `RESUMO_EXECUTIVO.md` - Visão geral
2. ✅ `MODELO_EVASAO_README.md` - Detalhes do modelo
3. ✅ `TUTORIAL_USO_FORMULARIO.md` - Como usar

### Para Data Scientists (Melhorias)
1. ✅ `02_ANALISE_DATABASE.md` - Exploração de dados
2. ✅ `03_PROPOSTA_NOVO_MODELO.md` - Opções de modelagem
3. ✅ `REDESIGN_COMPLETO.md` - Mudanças implementadas
4. ✅ `MODELO_EVASAO_README.md` - Modelo atual

---

## 📦 Arquivos Relacionados (Fora desta Pasta)

- **README principal**: [`../README.md`](../README.md) - Visão geral do projeto
- **Scripts**: [`../scripts/README.md`](../scripts/README.md) - Documentação de scripts
- **Testes**: [`../tests/README.md`](../tests/README.md) - Documentação de testes
- **Código-fonte**: `../src/` - Módulos de ML
- **API**: `../app/` - Endpoints REST
- **Monitoramento**: `../monitoring/` - Dashboards

---

## 🎯 Documentos Mais Importantes

Para entender o sistema rapidamente, leia estes 3 documentos na ordem:

1. **[`MODELO_EVASAO_README.md`](MODELO_EVASAO_README.md)** - O que é o modelo e como funciona
2. **[`MLOPS_IMPLEMENTATION.md`](MLOPS_IMPLEMENTATION.md)** - Como operar o modelo em produção
3. **[`ESTRATEGIA_RETREINO_MLOPS.md`](ESTRATEGIA_RETREINO_MLOPS.md)** - Como retreinar quando necessário

---

**Última atualização**: 2026-03-08  
**Versão do modelo**: 3.0 (Dropout Risk - IEG < 5.0)  
**Status**: Produção Ready com MLOps completo ✅

### 4. [`RESUMO_EXECUTIVO.md`](RESUMO_EXECUTIVO.md) 🎯
**Descrição**: Resumo de 1 página para tomada de decisão rápida  
**Conteúdo**:
- Problema em poucas palavras
- Recomendação clara
- Próximos passos

**Quando ler**: Se tiver pouco tempo - leia ESTE primeiro

---

## 🎯 Para Decisão Rápida

### Se você tem POUCO TEMPO (5 min):
1. Leia: [`RESUMO_EXECUTIVO.md`](RESUMO_EXECUTIVO.md)
2. Decida: Qual opção (A, B ou C)?
3. Responda: As 4 perguntas no final de `03_PROPOSTA_NOVO_MODELO.md`

### Se você tem TEMPO (30-60 min):
1. Leia: `01_CONTEXTO_ATUAL.md` (entender o problema)
2. Leia: `02_ANALISE_DATABASE.md` (entender os dados)
3. Leia: `03_PROPOSTA_NOVO_MODELO.md` (escolher solução)
4. Decida e responda as perguntas

---

## 🔴 Problema Identificado (Resumo)

O modelo atual prevê **"DEFASAGEM"** (tempo no programa) em vez de **"RISCO ACADÊMICO"** (desempenho ruim).

**Evidência**:
- Aluno com notas 1,1,1,1,1 → 4% de risco (❌ deveria ser ALTO)
- Aluno com notas 9,9,9,9,9 → 76% de risco (❌ deveria ser BAIXO)

**Causa**: Target baseado em "Defasagem" que mede se o aluno está atrasado em relação à fase ideal para sua idade, NÃO se tem notas ruins.

---

## ✅ Solução Recomendada

**OPÇÃO A: Modelo de Risco de Desempenho Acadêmico Baixo**

**Novo Target**:
```python
at_risk = 1 se média(IEG, IDA, Mat, Por) < 6.0
at_risk = 0 caso contrário
```

**Resultado Esperado**:
- Notas baixas → Alto risco ✅
- Notas altas → Baixo risco ✅
- Correlações corretas ✅
- Predições fazem sentido ✅

**Tempo de Implementação**: 2-3 dias

---

## 📊 Arquivos de Análise Criados

Durante esta análise, foram criados scripts Python para exploração:

- [`analise_completa_database.py`](../analise_completa_database.py) - Script de análise rodado para gerar os dados dos markdowns

---

## 📞 Contato / Próximos Passos

**Aguardando decisão do cliente sobre**:
1. Qual opção escolher (A, B ou C)?
2. Confirmar threshold de risco (média < 6.0?)
3. Prioridade: desempenho acadêmico ou evasão?
4. Aprovação para implementar

**Após decisão**: Implementação em 2-3 dias conforme plano detalhado em `03_PROPOSTA_NOVO_MODELO.md`

---

**Data de Criação**: 23 Fevereiro 2026  
**Autor**: Análise completa do projeto Datathon Passos Mágicos
