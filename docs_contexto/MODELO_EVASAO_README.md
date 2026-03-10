# 🎓 Modelo de Predição de Risco de Evasão Escolar

**Versão**: 3.0  
**Data**: 03 de Março de 2026  
**Status**: ✅ Produção

---

## 📋 Visão Geral

Sistema de Machine Learning para **identificação precoce de estudantes em risco de evasão escolar** (abandono do programa) da ONG Passos Mágicos.

### 🎯 Objetivo

Predizer quais alunos têm **alto risco de abandonar o programa** com base em indicadores de engajamento, permitindo intervenções preventivas de reengajamento.

---

## 🔍 Como Funciona

### Target (Variável Alvo)

```python
at_risk_evasao = 1 if IEG < 5.0 else 0
```

**IEG (Indicador de Engajamento)**:
- Mede: Presença, participação e envolvimento nas atividades
- Escala: 0 (sem engajamento) a 10 (engajamento máximo)
- **Threshold**: 5.0
  - IEG < 5.0 → Alto risco de evasão (14.4% dos alunos)
  - IEG ≥ 5.0 → Sem risco (85.6% dos alunos)

### Por que IEG?

1. **Indicador de desengajamento**: Baixa presença/participação precede evasão
2. **Proxy realista**: Na ausência de dados longitudinais de evasão confirmada
3. **Acionável**: Permite intervenções de reengajamento imediatas
4. **Proporção adequada**: 14.4% em risco é realista para problema de evasão

---

## 📊 Métricas do Modelo

**Modelo**: Logistic Regression (baseline robusto e interpretável)  
**Dataset**: PEDE 2024 (1156 alunos, snapshot)  
**Split**: 80% treino / 20% teste (estratificado)

| Métrica | Valor | Interpretação |
|---------|-------|---------------|
| **ROC-AUC** | **99.5%** | Excelente separação entre classes |
| **Acurácia** | **97.0%** | Alta taxa de acerto geral |
| **Precisão** | **96.4%** | Baixo índice de falsos positivos |
| **Recall** | **81.8%** | Captura maioria dos casos em risco |
| **F1-Score** | **88.5%** | Balanço entre precisão e recall |

### Distribuição do Target

- **Em risco de evasão** (IEG < 5.0): 166 alunos (14.4%)
- **Sem risco** (IEG ≥ 5.0): 990 alunos (85.6%)

---

## 🔧 Features Utilizadas

### Prioridade para Evasão

O modelo usa **22 features**, priorizando:

**📊 Notas Acadêmicas** (agora são features!):
- IDA (Desempenho Acadêmico)
- Mat (Matemática)
- Por (Português)
- Ing (Inglês)

**🧠 Indicadores Psicossociais** (CRÍTICOS para evasão):
- IAA (Autoavaliação)
- IPS (Psicossocial)
- IPP (Psicopedagógico)
- IPV (Ponto de virada)
- IAN (Autoavaliação numérica)

**📅 Histórico de Performance**:
- INDE 2022, 2023, 2024

**👤 Demográficas**:
- Idade, Gênero, Ano ingresso
- Instituição de ensino, Fase, Turma

**🔢 Engenheiradas**:
- Fase_num, Tempo_programa, Idade_ingresso

**⚠️ IMPORTANTE**: IEG **NÃO** é feature (é usado para construir o target)

---

## 🚀 Como Usar

### 1. Treinar Modelo

```bash
python -m src.train --threshold 5.0
```

**Saída**:
- `app/model/model.joblib` - Modelo treinado
- `app/model/metrics.json` - Métricas de avaliação
- `app/model/feature_columns.json` - Features esperadas
- `app/model/model_config.json` - Configuração (versão 3.0)
- `app/model/baseline.json` - Baseline para drift

### 2. Iniciar API

```bash
uvicorn app.main:app --reload
```

**Endpoints**:
- `GET /` - Dashboard web interativo
- `GET /health` - Status da API
- `POST /predict` - Fazer predições
- `GET /metrics` - Ver métricas do modelo
- `GET /drift` - Monitorar drift

### 3. Fazer Predição

```python
import requests

payload = {
    "records": [
        {
            "Idade": 12,
            "Gênero": "M",
            "Ano ingresso": 2020,
            "Fase": "3A",
            "Instituição de ensino": "Escola Pública",
            "IDA": 6.5,  # Agora é feature!
            "Mat": 7.0,
            "Por": 6.0,
            "Ing": 7.5,
            "INDE 2024": 7.0,
            "IAA": 6.5,
            "IPS": 7.0,
            "Nº Av": 10
        }
    ]
}

response = requests.post("http://localhost:8000/predict", json=payload)
print(response.json())
```

**Resposta**:
```json
{
  "predictions": [
    {
      "at_risk_probability": 0.05,
      "at_risk_label": 0
    }
  ]
}
```

**Interpretação**:
- `at_risk_probability`: Probabilidade de evasão (0-1)
- `at_risk_label`: 
  - 1 = **Alto risco de evasão** → Intervenção urgente
  - 0 = **Sem risco** → Monitorar normalmente

---

## 🔬 Validação do Modelo

### Casos de Teste

| IEG | Predição Esperada | Interpretação |
|-----|-------------------|---------------|
| 9.0 | 0 (sem risco) | Engajado, participativo |
| 5.5 | 0 (sem risco) | Engajamento adequado |
| 4.5 | 1 (em risco) | Desengajamento preocupante |
| 2.0 | 1 (em risco) | **Crítico** - Intervenção imediata |

### Script de Validação

```bash
python scripts/validar_modelo_evasao.py
```

---

## 📈 Estratégias de Intervenção

### Quando `at_risk_label = 1` (Risco de Evasão)

**Nível de Urgência** (baseado em `at_risk_probability`):

| Probabilidade | Urgência | Ações Recomendadas |
|---------------|----------|-------------------|
| 90-100% | 🔴 Crítica | Contato imediato, visita familiar, suporte psicossocial |
| 70-89% | 🟠 Alta | Reunião com tutor, plano de reengajamento personalizado |
| 50-69% | 🟡 Média | Monitoramento próximo, atividades motivacionais |

**Tipos de Intervenção**:
1. **Tutoria individualizada**: Apoio acadêmico extra
2. **Suporte psicossocial**: Sessões com psicólogos/assistentes sociais
3. **Engajamento familiar**: Envolver pais/responsáveis
4. **Atividades motivacionais**: Eventos, oficinas, gamificação
5. **Flexibilização**: Adaptar horários, formatos de atividade

---

## 🔄 MLOps: Retraining & Monitoring

### Quando Retreinar?

**Gatilhos Automáticos**:
1. **Drift Detectado**: PSI > 0.2 em features críticas (IPS, IAA, IPP)
2. **Performance Drop**: Acurácia cai abaixo de 90%
3. **Novo Ano Letivo**: Início de cada ciclo (Fevereiro)
4. **Dados Suficientes**: +200 novos alunos desde último treino

### Pipeline de Retreino

```bash
# 1. Backup do modelo atual
cp app/model/model.joblib app/model/model_backup_$(date +%Y%m%d).joblib

# 2. Retreinar com novos dados
python -m src.train --threshold 5.0 --data-path database/PEDE_2026.xlsx

# 3. Validar novo modelo
python scripts/validar_modelo_evasao.py

# 4. A/B Test (opcional)
# Comparar performance modelo novo vs antigo em dados holdout

# 5. Deploy
# Se métricas OK, modelo novo já está em app/model/
```

### Monitoramento Contínuo

**Dashboard Streamlit**:
```bash
streamlit run monitoring/dashboard.py
```

**Métricas Monitoradas**:
- PSI (Population Stability Index) por feature
- Distribuição de predições (% em risco)
- Volume de chamadas à API
- Latência de predições

**Alertas**:
- 🔴 PSI > 0.25: Drift severo - Retreino obrigatório
- 🟠 PSI > 0.15: Drift moderado - Investigar
- 🔵 Distribuição mudou >10%: Monitorar

---

## 📋 Data Contracts

### Schema de Entrada (Obrigatório)

```json
{
  "Idade": "int (8-25)",
  "Gênero": "enum ['M', 'F']",
  "Ano ingresso": "int (2015-2026)",
  "Fase": "str (ex: '3A', '7E', '9')",
  "Instituição de ensino": "str",
  "IDA": "float (0-10) opcional",
  "Mat": "float (0-10) opcional",
  "Por": "float (0-10) opcional",
  "Ing": "float (0-10) opcional",
  "INDE 2024": "float (0-10) opcional",
  "IAA": "float (0-10) opcional",
  "IPS": "float (0-10) opcional",
  "IPP": "float (0-10) opcional",
  "IPV": "float (0-10) opcional",
  "IAN": "float (0-10) opcional",
  "Nº Av": "int (>=0) opcional"
}
```

**Campos Mínimos** (9 obrigatórios): Idade, Gênero, Ano ingresso, Fase, Instituição, INDE 2024, IAA, IPS, Nº Av

---

## 🧪 Testes

**Cobertura**: 97.48% (105 testes passando)

```bash
# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html
```

**Suítes de Teste**:
- `test_preprocessing.py` - Target de evasão
- `test_feature_engineering.py` - Features derivadas
- `test_train.py` - Pipeline de treino
- `test_evaluate.py` - Métricas
- `test_drift.py` - Detecção de drift
- `test_utils.py` - Utilitários

---

## 🎓 Diferenças dos Modelos Anteriores

| Aspecto | Modelo v1.0 (Defasagem) | Modelo v2.0 (Acadêmico) | **Modelo v3.0 (Evasão)** ✅ |
|---------|-------------------------|-------------------------|----------------------------|
| **Target** | Defasagem > 0 | Média notas < 6.0 | **IEG < 5.0** |
| **Objetivo** | Atraso de fase | Notas baixas | **Risco de abandonar** |
| **Features** | Demog + Psico | Demog + Psico | **Demog + Notas + Psico** |
| **IEG** | Feature | Usado no target | **Usado no target** |
| **Notas** | Features | Usadas no target | **Features** |
| **Foco** | Permanência | Desempenho | **Retenção/Engajamento** |
| **ROC-AUC** | ~85% | 97.4% | **99.5%** |

---

## 📞 Suporte

**Documentação Adicional**:
- `docs_contexto/03_PROPOSTA_NOVO_MODELO.md` - Justificativa técnica
- `docs_contexto/RESUMO_EXECUTIVO.md` - Visão gerencial
- `docs_contexto/STATUS_TESTES.md` - Cobertura de testes

**Troubleshooting**:
- Modelo não carrega? → Rode `python -m src.train`
- API não sobe? → Verifique porta 8000 livre
- Predições estranhas? → Valide schema de entrada
- Drift alto? → Retreine o modelo

---

**🎯 Modelo focado em PREVENÇÃO de evasão via identificação precoce de desengajamento!**
