# Scripts de Análise e MLOps

Esta pasta contém scripts auxiliares para análise, debug, validação e operações MLOps.

## 📂 Conteúdo

### 🔍 Análise e Debug

#### `analise_completa_database.py`
Script de análise exploratória da base de dados PEDE 2024.
- Estatísticas descritivas
- Distribuições das variáveis
- Correlações entre features
- Análise de missings

**Uso:**
```bash
python scripts/analise_completa_database.py
```

#### `analise_temporal.py`
Análise da estrutura temporal dos dados PEDE.
- Verifica se há dados longitudinais (múltiplos anos por aluno)
- Detecta evolução temporal de métricas
- Valida estrutura snapshot vs time-series

**Uso:**
```bash
python scripts/analise_temporal.py
```

#### `debug_feature_engineering.py`
Script para debug e validação do módulo de feature engineering.
- Testa criação de features engineeradas (Tempo_programa, Idade_ingresso, Fase_num)
- Valida conversões de tipo
- Verifica edge cases

**Uso:**
```bash
python scripts/debug_feature_engineering.py
```

---

### ✅ Validação de Modelo

#### `validar_modelo_evasao.py`
Validação completa do modelo de evasão v3.0.
- Valida target (IEG < 5.0 = risco de evasão)
- Testa distribuição de classes
- Verifica features usadas (22 features)
- Valida métricas do modelo

**Uso:**
```bash
python scripts/validar_modelo_evasao.py
```

#### `validar_rapido.py`
Validação rápida em 30 segundos.
- Data contracts
- Distribuição da target
- Features disponíveis
- Métricas do modelo

**Uso:**
```bash
python scripts/validar_rapido.py
```

---

### 🔒 Data Contracts

#### `validar_data_contracts.py`
Valida schema e qualidade dos dados de entrada.

**Validações:**
1. **Schema**: Verifica colunas obrigatórias e opcionais
2. **Ranges**: Valida valores dentro dos limites esperados (ex: INDE 0-10)
3. **Categóricos**: Valida valores válidos para Gênero, Fase, etc
4. **Qualidade**: Detecta missings, duplicatas, outliers

**Uso:**
```bash
python scripts/validar_data_contracts.py
```

**Exit codes:**
- `0`: Dados válidos (passou em todas validações críticas)
- `1`: Dados inválidos (falhou em validações críticas)

**Exemplo de output:**
```
1. VALIDACAO DE SCHEMA
  [OK] Idade: presente
  [OK] Gênero: presente
  
2. VALIDACAO DE RANGES
  [OK] INDE 2024: 1156 valores dentro do range [0, 10]
  [WARN] Idade: 5 valores fora do range [8, 25]
  
3. VALIDACAO DE VALORES CATEGORICOS
  [OK] Gênero: todos valores validos ['M', 'F']
  
4. VALIDACAO DE QUALIDADE
  [OK] INDE 2024: sem missing values
  [WARN] IDA: 234 NaN (20.2%)

STATUS: DADOS VALIDOS
```

---

### 🔄 Pipeline de Retreino

#### `backup_modelo.py`
Cria backup timestamped do modelo atual antes de retreino.

**Funcionalidades:**
- Backup completo de `app/model/` (model.joblib, metrics.json, etc)
- Timestamp automático: `backups/model_YYYYMMDD_HHMMSS/`
- Salva metadata (versão, data, arquivos)
- Lista backups disponíveis
- Limpa backups antigos (mantém 5 mais recentes)

**Uso:**
```bash
python scripts/backup_modelo.py
```

**Estrutura do backup:**
```
backups/
  model_20250122_153045/
    model.joblib
    metrics.json
    model_config.json
    feature_columns.json
    baseline.json
    backup_metadata.json  # metadata do backup
```

---

#### `restaurar_backup.py`
Restaura um backup específico do modelo.

**Funcionalidades:**
- Lista backups disponíveis com metadata
- Restaura modelo de backup específico
- Faz backup do modelo atual antes de sobrescrever
- Validações de segurança

**Uso:**
```bash
# Listar backups disponíveis
python scripts/restaurar_backup.py

# Restaurar backup específico
python scripts/restaurar_backup.py model_20250122_153045
```

**ATENÇÃO:**
- Sempre faz backup do modelo atual antes de restaurar
- Reinicie a API após restaurar: `uvicorn app.main:app --reload`

---

#### `retreino_automatizado.py`
Pipeline completo de retreino automatizado com validações.

**Pipeline (6 passos):**

1. **Validação de Data Contracts**: Valida qualidade dos novos dados
2. **Backup**: Cria backup do modelo atual
3. **Treinamento**: Treina novo modelo com `src/train.py`
4. **Validação de Métricas**: Verifica se métricas atendem critérios mínimos
5. **Testes**: Executa suite de testes (`pytest`)
6. **Avaliação**: Avalia modelo final com `src/evaluate.py`

**Critérios de Aprovação:**
- ROC-AUC ≥ 0.90
- Accuracy ≥ 0.90
- Recall ≥ 0.70 (prioriza não perder alunos em risco)

**Uso:**
```bash
# Python
python scripts/retreino_automatizado.py

# Windows (batch)
procedures\retreino.bat
```

**Exit codes:**
- `0`: Retreino bem-sucedido, modelo aprovado
- `1`: Retreino falhou (dados inválidos, métricas ruins, etc)

**Em caso de falha:**
- Modelo anterior é mantido sem alterações
- Logs indicam causa da falha
- Recomendações de correção são exibidas

**Exemplo de output:**
```
PASSO 1/6: Validacao de Data Contracts
[OK] Dados validos

PASSO 2/6: Backup do Modelo Atual
[OK] Backup criado: backups/model_20250122_143010/

PASSO 3/6: Treinamento do Novo Modelo
[OK] Modelo treinado com sucesso

PASSO 4/6: Validacao de Metricas
  [OK] ROC-AUC: 0.9950 >= 0.90
  [OK] Accuracy: 0.9700 >= 0.90
  [OK] Recall: 0.8180 >= 0.70
[OK] MODELO APROVADO

PASSO 5/6: Execucao de Testes
[OK] 105 passed, 8 skipped

PASSO 6/6: Avaliacao Final do Modelo
[OK] Avaliacao concluida

RETREINO CONCLUIDO COM SUCESSO
Duracao total: 45.2s

Proximos passos:
  1. Testar API
  2. Validar predicoes manualmente
  3. Deploy em producao
```

---

## 🎯 Propósito

### Scripts de Desenvolvimento
- Análises ad-hoc, debugging, exploração de dados
- Validação manual de comportamento
- Prototipagem rápida

### Scripts MLOps
- **Data Contracts**: Garantir qualidade dos dados de entrada
- **Backup/Restore**: Segurança e rollback rápido (<5 min)
- **Retreino Automatizado**: Pipeline reproduzível e validado

### Quando usar cada ferramenta

| Tarefa | Ferramenta |
|--------|-----------|
| Explorar dados novos | `analise_completa_database.py` |
| Validar modelo v3.0 | `validar_modelo_evasao.py` |
| Check rápido (30s) | `validar_rapido.py` |
| Validar novos dados | `validar_data_contracts.py` |
| Antes de retreino | `backup_modelo.py` |
| Retreino completo | `retreino_automatizado.py` |
| Rollback de modelo | `restaurar_backup.py` |

---

## 📊 Diferença entre pastas

- **scripts/**: Ferramentas de análise e MLOps (CLI)
- **tests/**: Testes unitários automatizados (pytest, CI/CD)
- **notebooks/**: Análise interativa (Jupyter)
- **monitoring/**: Dashboards visuais (Streamlit)
- **procedures/**: Atalhos batch para Windows (.bat)

---

## 🚀 Quick Start

### Validação Rápida do Sistema
```bash
# 1. Validar dados
python scripts/validar_data_contracts.py

# 2. Validar modelo
python scripts/validar_modelo_evasao.py

# 3. Check rápido
python scripts/validar_rapido.py
```

### Retreino Completo
```bash
# Windows
procedures\retreino.bat

# Linux/Mac
python scripts/retreino_automatizado.py
```

### Rollback de Emergência
```bash
# Listar backups
python scripts/restaurar_backup.py

# Restaurar backup
python scripts/restaurar_backup.py model_20250122_153045

# Reiniciar API
uvicorn app.main:app --reload
```

---

## 📚 Documentação Adicional

- **Estratégia de Retreino**: [ESTRATEGIA_RETREINO_MLOPS.md](../docs/ESTRATEGIA_RETREINO_MLOPS.md)

