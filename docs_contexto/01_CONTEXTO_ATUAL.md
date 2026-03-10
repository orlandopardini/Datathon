# 📋 Contexto Atual do Projeto - Datathon Passos Mágicos

**Data de Análise**: 23 Fevereiro 2026  
**Status**: ⚠️ MODELO FUNCIONAL MAS COM PROBLEMA CONCEITUAL

---

## 1. Estrutura do Projeto

### Arquivos Principais

```
datathon/
├── app/
│   ├── main.py              # API FastAPI
│   ├── routes.py            # Endpoint /predict
│   ├── static/              # Dashboard web
│   └── model/               # Artefatos do modelo
│       ├── model.joblib     # Pipeline treinada
│       ├── feature_columns.json
│       ├── metrics.json
│       └── baseline.json
├── src/
│   ├── preprocessing.py     # Carregamento e limpeza de dados
│   ├── feature_engineering.py  # Engenharia de features
│   ├── train.py            # Treinamento do modelo
│   ├── evaluate.py         # Métricas de avaliação
│   ├── drift.py            # Detecção de drift
│   └── utils.py            # Utilitários
├── tests/                   # 81% cobertura de testes
├── procedures/              # Scripts .bat de execução
├── database/               # BASE DE DADOS PEDE 2024.xlsx
└── requirements.txt        # Dependências Python
```

---

## 2. Tecnologias e Versões

| Componente | Tecnologia | Versão |
|-----------|-----------|---------|
| Linguagem | Python | 3.14.0 |
| ML Framework | scikit-learn | 1.8.0 |
| API | FastAPI | 0.128.0 |
| Data Processing | pandas | 2.3.3 |
| Servidor | Uvicorn | 0.40.0 |
| Testes | pytest | 8.3.0 |
| Cobertura | pytest-cov | 6.0.0 |

---

## 3. Estado Atual do Modelo

### Definição do Target (PROBLEMA IDENTIFICADO)

**Código Atual** (`src/preprocessing.py`):
```python
def build_target_at_risk(df: pd.DataFrame, defasagem_col: str = "Defasagem") -> pd.Series:
    """
    Define alvo binário: 1 se Defasagem > 0 (em atraso/risco), 0 caso contrário.
    """
    return (pd.to_numeric(df[defasagem_col], errors="coerce") > 0).astype(int)
```

**O que isso significa:**
- `at_risk = 1` quando `Defasagem > 0`
- "Defasagem" = diferença entre a Fase ATUAL e a Fase IDEAL para a idade do aluno
- **NÃO mede desempenho acadêmico, mas sim tempo no programa**

### Features Utilizadas (11 features)

**Código Atual** (`src/train.py`):
```python
features_disponiveis = [
    # Numéricas (7)
    "Idade", "Ano ingresso", "IEG", "IDA", "Mat", "Por", "Ing",
    # Categóricas (4)
    "Fase", "Turma", "Gênero", "Instituição de ensino"
]
```

### Métricas do Modelo Atual

Conforme `app/model/metrics.json`:
- **ROC-AUC**: 96.0%
- **Acurácia**: 93.5%
- **Precisão**: 77.3%
- **Recall**: 63.0%
- **F1-Score**: 69.4%

**Interpretação**: Métricas excelentes, mas o modelo está prevendo a **variável errada**.

---

## 4. Problema Conceitual Identificado

### 🔴 O Que Está Acontecendo

O modelo atual prevê **"Defasagem"** (atraso em relação à série ideal), NÃO **"Risco Acadêmico"** (desempenho ruim nas notas).

### Evidências do Problema

#### Correlações Contra-Intuitivas

| Nota | Correlação com at_risk | Interpretação |
|------|----------------------|---------------|
| IEG | **-0.154** | ✅ Negativa (correto) |
| IDA | **+0.084** | ❌ Positiva (invertido) |
| Mat | **+0.030** | ❌ Positiva (invertido) |
| Por | **+0.060** | ❌ Positiva (invertido) |
| Ing | **+0.175** | ❌ Positiva (invertido) |

**Significado**: Alunos com notas ALTAS em IDA, Mat, Por, Ing têm MAIOR "defasagem" (mais tempo no programa).

#### Análise por Fase

| Fase | Total Alunos | Em Risco | Taxa de Risco | Notas Médias |
|------|--------------|----------|---------------|--------------|
| **Fase 9** | 38 | **38** | **100%** | IEG=0.00, Mat=NaN, Por=NaN |
| **Fase 7E** | 25 | **19** | **76%** | IEG=6.91, Mat=4.81, Por=5.18 |
| Fase 1A-1R | ~200 | 0 | **0%** | IEG=8.5, Mat=7.8, Por=6.8 |
| Fase 2A-2U | ~180 | 6 | **3%** | IEG=7.9, Mat=5.9, Por=6.7 |
| Fase 3A-3U | ~210 | 40 | **19%** | IEG=7.5, Mat=5.5, Por=5.0 |

**Padrão Descoberto**:
- Fases **avançadas** (7E, 9) têm **ALTA** defasagem (76-100%)
- Fases **iniciais** (1A-1R, ALFA) têm **ZERO** defasagem
- Alunos em fases avançadas ficaram mais tempo no programa = mais "defasados"

---

## 5. Comportamento Atual da API

### Exemplo 1: Notas Baixas (1, 1, 1, 1, 1)
```json
{
  "Fase": "1A",
  "Idade": 11,
  "IEG": 1.0, "IDA": 1.0, "Mat": 1.0, "Por": 1.0, "Ing": 1.0,
  "Gênero": "Masculino",
  "Ano ingresso": 2021,
  "Instituição de ensino": "Escola Pública"
}
```
**Resultado**: 4.2% de risco (BAIXO)  
**Por quê?**: Fase 1A (inicial) + jovem = pouco tempo no programa = baixa defasagem

### Exemplo 2: Notas Altas (9, 9, 9, 9, 9)
```json
{
  "Fase": "7E",
  "Idade": 16,
  "IEG": 9.0, "IDA": 9.0, "Mat": 9.0, "Por": 9.0, "Ing": 9.0,
  "Gênero": "Feminino",
  "Ano ingresso": 2018,
  "Instituição de ensino": "Escola Particular"
}
```
**Resultado**: 76% de risco (ALTO)  
**Por quê?**: Fase 7E (avançada) + mais velha = muito tempo no programa = alta defasagem

---

## 6. O Que o Modelo REALMENTE Prevê

### Definição Técnica
O modelo prevê a probabilidade de um aluno estar **atrasado em relação à progressão ideal** no programa (permanência/defasagem).

### O Que NÃO Prevê
O modelo **NÃO** prevê:
- Risco de desempenho acadêmico ruim
- Risco de reprovação
- Risco de evasão do programa
- Necessidade de intervenção pedagógica

---

## 7. Tentativas de Correção (Histórico)

### Tentativa 1: Inverter Target de `< 0` para `> 0`
- **Status**: ✅ Concluído
- **Resultado**: Tecnicamente correto, mas não resolveu o problema conceitual

### Tentativa 2: Reduzir Features de 48 para 11
- **Status**: ✅ Concluído
- **Resultado**: Features agora correspondem ao formulário web, mas problema persiste

### Tentativa 3: Inverter Probabilidades (`proba = 1 - proba`)
- **Status**: ❌ Revertido
- **Resultado**: Piorou o modelo, tornando-o incorreto para ambas interpretações

### Tentativa 4: Adicionar Nota Explicativa no Dashboard
- **Status**: ✅ Concluído
- **Resultado**: Explica o problema, mas não o resolve

---

## 8. Testes e Cobertura

### Status dos Testes
- **Total de testes**: 11
- **Testes passando**: 11 (100%)
- **Cobertura de código**: 81%

### Principais Arquivos Testados
- `tests/test_preprocessing.py` - Testes de carregamento e target
- `tests/test_feature_engineering.py` - Testes de engenharia de features
- `tests/test_train.py` - Testes do pipeline de treino
- `tests/test_evaluate.py` - Testes de métricas
- `tests/test_drift.py` - Testes de detecção de drift

**Observação**: Todos os testes estão passando porque testam a implementação ATUAL (defasagem), não a implementação DESEJADA (risco acadêmico).

---

## 9. Infraestrutura e Deploy

### Scripts de Execução (procedures/)
- `setup.bat` - Cria venv e instala dependências
- `train.bat` - Treina o modelo
- `test.bat` - Executa testes com cobertura
- `run.bat` - Sobe API + abre browser em localhost:8000
- `run-with-monitoring.bat` - API (8000) + Dashboard Drift (8501)

### Docker
- `Dockerfile` configurado
- Build: `docker build -t passos-mlops:latest .`
- Run: `docker run -d -p 8000:8000 passos-mlops:latest`

### Monitoramento
- Dashboard Streamlit em `monitoring/dashboard.py`
- Logs de predições em `app/logs/predictions.jsonl`
- Detecção de drift com PSI (Population Stability Index)

---

## 10. Documentação Existente

### Arquivos de Documentação
- `README.md` - Documentação principal (1392 linhas)
- `passo_a_passo.txt` - Guia de execução passo a passo
- `regras.txt` - Requisitos do Datathon
- `GUIA_DEMONSTRACAO_DETALHADO.md` - Guia de demonstração

### Estado da Documentação
⚠️ **Toda documentação atual descreve o modelo de "defasagem", não de "risco acadêmico"**

---

## 11. Dependências (requirements.txt)

```txt
fastapi>=0.128.0
uvicorn[standard]>=0.40.0
pydantic>=2.0
pandas>=2.3.0
numpy>=2.4.0
scikit-learn>=1.8.0
joblib>=1.4.0
python-multipart
pyyaml
rich
python-dotenv
streamlit>=1.52.0
matplotlib>=3.9.0
openpyxl>=3.1.0
pytest>=8.3.0
pytest-cov>=6.0.0
httpx
```

**Status**: ✅ Todas instaladas e funcionando

---

## 12. Database

### Localização
`database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`

### Estrutura
- **Total de registros**: 1.156 alunos
- **Total de colunas**: 50
- **Aba utilizada**: "PEDE2024"

### Colunas Principais
| Coluna | Tipo | Nulls | Descrição |
|--------|------|-------|-----------|
| RA | object | 0 | Registro do Aluno |
| Nome Anonimizado | object | 0 | Nome anonimizado |
| Fase | object | 0 | Fase atual (1A, 2B, 7E, 9, etc) |
| Turma | object | 0 | Turma |
| Idade | int64 | 0 | Idade do aluno |
| Gênero | object | 0 | Masculino/Feminino |
| Ano ingresso | int64 | 0 | Ano de entrada no programa |
| Instituição de ensino | object | 1 | Tipo de escola |
| IEG | float64 | 0 | Indicador de Engajamento |
| IDA | float64 | 101 | Indicador de Autodesenvolvimento |
| Mat | float64 | 105 | Nota de Matemática |
| Por | float64 | 106 | Nota de Português |
| Ing | float64 | 682 | Nota de Inglês (muitos nulls) |
| Defasagem | int64 | 0 | **VARIÁVEL ALVO ATUAL** |
| Fase Ideal | object | 0 | Fase esperada para a idade |

### Distribuição do Target Atual

```
Defasagem = -3:     3 alunos (adiantados 3 níveis)
Defasagem = -2:    90 alunos (adiantados 2 níveis)
Defasagem = -1:   441 alunos (adiantados 1 nível)
Defasagem =  0:   485 alunos (no nível ideal) ← 42%
Defasagem = +1:   119 alunos (atrasados 1 nível)
Defasagem = +2:    16 alunos (atrasados 2 níveis)
Defasagem = +3:     2 alunos (atrasados 3 níveis)

at_risk = 1 (Defasagem > 0): 137 alunos (11.9%)
at_risk = 0 (Defasagem <= 0): 1.019 alunos (88.1%)
```

---

## 13. Conclusão do Estado Atual

### ✅ O Que Está Funcionando
1. Infraestrutura completa de MLOps
2. API REST funcional com FastAPI
3. Dashboard web interativo
4. Pipeline de treino automatizada
5. Testes com 81% de cobertura
6. Monitoramento de drift
7. Containerização Docker
8. Documentação extensa
9. Métricas excelentes (96% ROC-AUC)

### ❌ O Que Está Errado
1. **Modelo prevê a variável errada** (defasagem ≠ risco acadêmico)
2. **Correlações contra-intuitivas** (notas altas → alto risco)
3. **Predições nonsensicais** para o usuário final
4. **Documentação descreve problema errado**
5. **Testes validam comportamento incorreto**

### 🎯 O Que Precisa Ser Feito
**REDEFINIR O PROBLEMA DO ZERO**:
1. Decidir o que realmente queremos prever
2. Criar novo target baseado no objetivo real
3. Re-treinar modelo com novo target
4. Atualizar todos os testes
5. Re-escrever documentação
6. Validar que predições fazem sentido

---

## 14. Próximos Passos Recomendados

Ver documentos:
- `02_ANALISE_DATABASE.md` - Análise detalhada dos dados
- `03_PROPOSTA_NOVO_MODELO.md` - Proposta de reformulação
