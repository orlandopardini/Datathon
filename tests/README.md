# Testes do Projeto

Esta pasta contém todos os testes do projeto, organizados por tipo.

## 📋 Estrutura

### Testes Unitários (Unit Tests)
Testam componentes individuais isoladamente:

- **`test_drift.py`** (29 testes)
  - Detecção de drift (PSI, JS divergence)
  - Build baseline, compute drift
  
- **`test_evaluate.py`** (11 testes)
  - Métricas: ROC-AUC, Precision, Recall, F1, PR-AUC
  - Avaliação de modelos binários
  
- **`test_feature_engineering.py`** (19 testes)
  - Parse de Fase, criação de features engineeradas
  - Tempo_programa, Idade_ingresso, Fase_num
  
- **`test_preprocessing.py`** (15 testes)
  - Target acadêmico, remoção de colunas
  - Train/test split estratificado
  
- **`test_train.py`** (19 testes)
  - Pipeline scikit-learn, Logistic Regression
  - Handle missing values e unknown categories
  
- **`test_utils.py`** (11 testes)
  - JSON read/write, criação de diretórios
  - Encoding UTF-8

### Testes de Integração (Integration Tests)
Testam componentes trabalhando juntos:

- **`test_api_new_model.py`**
  - Testa API FastAPI com modelo v2.0
  - Endpoints /predict, /health, /model-info
  - Validação de payloads e respostas
  
- **`test_simplified_form.py`**
  - Testa formulário simplificado (9 campos obrigatórios)
  - Validação de campos opcionais
  - Integração frontend-backend
  
- **`test_dashboard_integration.py`**
  - Testa dashboard de monitoramento
  - Validação de métricas e gráficos
  
- **`validate_new_model.py`**
  - Validação end-to-end do modelo v2.0
  - Testa pipeline completo: dados → predição → métricas

## 🚀 Executando os Testes

### Todos os testes unitários
```bash
pytest tests/ -v
```

### Com relatório de cobertura
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Testes específicos
```bash
pytest tests/test_drift.py -v
pytest tests/test_api_new_model.py -v
```

### Testes de integração
```bash
python tests/test_api_new_model.py
python tests/validate_new_model.py
```

## 📊 Cobertura Atual

**Total: 97.48%** (excede meta de 80%)

| Módulo                  | Cobertura | Testes |
|-------------------------|-----------|--------|
| drift.py                | 100.00%   | 29     |
| evaluate.py             | 100.00%   | 11     |
| utils.py                | 100.00%   | 15     |
| feature_engineering.py  | 97.01%    | 19     |
| preprocessing.py        | 92.45%    | 15     |

## 🔧 Configuração

Configurações de teste em:
- **`pytest.ini`**: Configuração do pytest
- **`.coveragerc`**: Configuração de cobertura
  - Omite `src/train.py` (script principal, testado via E2E)
  - Threshold: 80%

## 📝 Convenções

- Nomes de arquivo: `test_*.py`
- Nomes de função: `test_*`
- Use fixtures para setup/teardown
- Mock externos (DB, API calls)
- Docstrings explicando o que está sendo testado

## 🐛 Debug

Para debug de testes específicos:
```bash
pytest tests/test_drift.py::test_psi_identical_distributions -v -s
```

Para ver printouts durante testes:
```bash
pytest tests/ -v -s
```
