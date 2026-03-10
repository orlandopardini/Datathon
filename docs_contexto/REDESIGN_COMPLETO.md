# ✅ REDESIGN COMPLETO: MODELO DE EVASÃO ESCOLAR

**Data**: 03 de Março de 2026  
**Versão**: 3.0  
**Status**: ✅ **PRODUÇÃO**

---

## 📋 RESUMO EXECUTIVO

O modelo foi **completamente redesenhado** para prever **risco de evasão escolar** (abandono do programa) em vez de desempenho acadêmico.

### 🎯 Novo Objetivo

**Identificar alunos com alto risco de abandonar o programa** via indicadores de desengajamento.

---

## 🔄 O QUE MUDOU

### Target (Variável Alvo)

| Modelo Anterior (v2.0) | **Modelo Novo (v3.0)** ✅ |
|------------------------|---------------------------|
| `média(IEG, IDA, Mat, Por) < 6.0` | `IEG < 5.0` |
| Prediz: Notas baixas | **Prediz: Risco de evasão** |
| Foco: Desempenho | **Foco: Engajamento/Retenção** |

### Features

| Categoria | v2.0 | **v3.0** ✅ |
|-----------|------|-------------|
| **Notas** | ❌ Usadas no target | ✅ **Agora são features!** (IDA, Mat, Por, Ing) |
| **IEG** | ❌ Usado no target | ❌ **Usado no target (evasão)** |
| **Psicossociais** | ✅ Features | ✅ **Features (críticas!)** |
| **Demográficas** | ✅ Features | ✅ Features |

**Total de features**: 22 (vs 18 antes)

---

## 📊 MÉTRICAS DO NOVO MODELO

### Performance Excepcional

| Métrica | Valor | Benchmark |
|---------|-------|-----------|
| **ROC-AUC** | **99.5%** | ⭐ Excelente (>90%) |
| **Acurácia** | **97.0%** | ⭐ Muito Alta |
| **Precisão** | **96.4%** | ⭐ Baixo falso positivo |
| **Recall** | **81.8%** | ✅ Captura maioria dos casos |
| **F1-Score** | **88.5%** | ⭐ Balanço excelente |

### Distribuição

- **Em risco de evasão** (IEG < 5.0): 166 alunos (14.4%)
- **Sem risco** (IEG ≥ 5.0): 990 alunos (85.6%)

**Proporção realista** para problema de evasão.

---

## 🧪 TESTES: 96.76% COBERTURA

**105 testes passando** ✅

| Módulo | Cobertura | Status |
|--------|-----------|--------|
| `drift.py` | 100% | ✅ |
| `evaluate.py` | 100% | ✅ |
| `utils.py` | 100% | ✅ |
| `feature_engineering.py` | 97% | ✅ |
| `preprocessing.py` | 90% | ✅ |
| **TOTAL** | **96.76%** | ✅ **Acima de 95%!** |

---

## 📦 ARQUIVOS ATUALIZADOS

### Core

1. **`src/preprocessing.py`**
   - ✅ Nova função: `build_target_at_risk_evasao()`
   - ✅ Target: IEG < 5.0 = risco de evasão
   - ✅ Depreciou: `build_target_at_risk_academic()` (modelo v2.0)

2. **`src/train.py`**
   - ✅ Usa novo target de evasão
   - ✅ Notas (IDA, Mat, Por, Ing) agora são features
   - ✅ IEG removido das features (usado no target)
   - ✅ Model config v3.0 com descrição correta

3. **`app/model/`** (Artefatos Retreinados)
   - ✅ `model.joblib` - Modelo v3.0
   - ✅ `metrics.json` - Métricas (ROC-AUC 99.5%)
   - ✅ `model_config.json` - Versão 3.0, tipo "dropout_risk"
   - ✅ `feature_columns.json` - 22 features
   - ✅ `baseline.json` - Baseline para drift

### API

4. **`app/main.py`**
   - ✅ Título: "Risco de Evasão Escolar"
   - ✅ Versão: 3.0.0
   - ✅ Descrição atualizada

5. **`app/routes.py`**
   - ✅ Documentação: "Probabilidade de risco de evasão"
   - ✅ Labels atualizados

### Testes

6. **`tests/test_preprocessing.py`**
   - ✅ 16 testes atualizados
   - ✅ Testa novo target `build_target_at_risk_evasao()`
   - ✅ Casos: IEG < 5.0 = risco, IEG ≥ 5.0 = sem risco
   - ✅ Valida threshold customizado
   - ✅ Testa valores de fronteira

### Documentação

7. **`MODELO_EVASAO_README.md`** (NOVO)
   - ✅ Documentação completa do modelo v3.0
   - ✅ Como funciona, por que IEG
   - ✅ Métricas, features, casos de uso
   - ✅ MLOps: estratégias de retreino
   - ✅ Data contracts, monitoramento
   - ✅ Comparação com modelos anteriores

8. **`scripts/validar_rapido.py`** (NOVO)
   - ✅ Script de validação rápida
   - ✅ Testa casos: IEG alto/baixo
   - ✅ Verifica distribuição do target

9. **`scripts/analise_temporal.py`** (NOVO)
   - ✅ Análise de estrutura dos dados
   - ✅ Confirma: snapshot 2024 (não longitudinal)
   - ✅ Justifica uso de IEG como proxy

---

## 🚀 COMO USAR O NOVO MODELO

### 1. Treinar (Já Feito ✅)

```bash
python -m src.train --threshold 5.0
```

**Saída**:
```
📊 Criando target de risco de EVASÃO com threshold IEG=5.0...
   Total de alunos: 1156
   Em risco de evasão (IEG < 5.0): 166 (14.4%)
   Sem risco de evasão (IEG >= 5.0): 990 (85.6%)

📊 MÉTRICAS DO MODELO DE EVASÃO:
   ROC-AUC: 99.5%
   Acurácia: 97.0%
   Precisão: 96.4%
   Recall: 81.8%
   F1-Score: 88.5%
```

### 2. Validar

```bash
python scripts/validar_rapido.py
```

**Resultado**:
```
CASOS DE TESTE:
  [OK] Engajado (IEG=9.5)        -> at_risk=0
  [OK] OK (IEG=6.0)              -> at_risk=0
  [OK] Limite (IEG=5.0)          -> at_risk=0
  [OK] Desengajado (IEG=4.5)     -> at_risk=1
  [OK] Critico (IEG=2.0)         -> at_risk=1
```

### 3. Iniciar API

```bash
uvicorn app.main:app --reload
```

**Acesse**: http://localhost:8000

### 4. Testar Predição

```python
import requests

payload = {
    "records": [{
        "Idade": 14,
        "Gênero": "F",
        "Ano ingresso": 2020,
        "Fase": "5A",
        "Instituição de ensino": "Escola Pública",
        # AGORA PODE USAR NOTAS COMO FEATURES!
        "IDA": 7.0,
        "Mat": 6.5,
        "Por": 7.0,
        "Ing": 6.0,
        "INDE 2024": 7.5,
        "IAA": 7.0,
        "IPS": 6.5,
        "Nº Av": 12
    }]
}

response = requests.post("http://localhost:8000/predict", json=payload)
print(response.json())
```

**Resposta**:
```json
{
  "predictions": [{
    "at_risk_probability": 0.03,
    "at_risk_label": 0
  }]
}
```

**Interpretação**:
- `at_risk_probability`: 3% de risco de evasão (muito baixo)
- `at_risk_label`: 0 = Sem risco

---

## 🎯 INTERPRETAÇÃO DO MODELO

### O que significa "risco de evasão"?

- **IEG < 5.0** indica **desengajamento crítico**:
  - Presença baixa
  - Participação fraca
  - Envolvimento mínimo
  
- **Desengajamento** precede **evasão**:
  - Alunos desengajados têm alta chance de abandonar
  - Modelo identifica **antes** da evasão acontecer
  - Permite **intervenção preventiva**

### Ações Recomendadas

| Probabilidade | Ação |
|---------------|------|
| **90-100%** | 🔴 Contato imediato, visita familiar, suporte psicossocial |
| **70-89%** | 🟠 Reunião com tutor, plano de reengajamento |
| **50-69%** | 🟡 Monitoramento próximo, atividades motivacionais |
| **<50%** | 🟢 Monitoramento normal |

---

## 📈 ESTRATÉGIA MLOps

### Quando Retreinar?

**Gatilhos Automáticos**:
1. ✅ **Drift Detectado**: PSI > 0.2 em features críticas
2. ✅ **Performance Drop**: Acurácia < 90%
3. ✅ **Novo Ano Letivo**: Fevereiro de cada ano
4. ✅ **Dados Suficientes**: +200 novos alunos

### Monitoramento

```bash
streamlit run monitoring/dashboard.py
```

**Métricas Monitoradas**:
- PSI (Population Stability Index) por feature
- Distribuição de predições
- Volume de chamadas à API
- Latência

**Alertas**:
- 🔴 PSI > 0.25: Retreino obrigatório
- 🟠 PSI > 0.15: Investigar
- 🔵 Distribuição mudou >10%: Monitorar

---

## ✅ CHECKLIST FINAL

### Código

- [x] Target redesenhado: `build_target_at_risk_evasao()`
- [x] Train.py atualizado para evasão
- [x] Features corretas (notas agora são features)
- [x] Modelo retreinado (ROC-AUC 99.5%)

### Testes

- [x] 105 testes passando
- [x] Cobertura: 96.76% (acima de 95%)
- [x] Testa novo target de evasão
- [x] Valida casos de fronteira

### API

- [x] Título atualizado: "Risco de Evasão Escolar"
- [x] Versão 3.0.0
- [x] Documentação correta

### Documentação

- [x] README do modelo de evasão
- [x] Script de validação
- [x] Análise temporal dos dados
- [x] Comparação com modelos anteriores

### Artefatos

- [x] model.joblib (v3.0)
- [x] metrics.json (ROC-AUC 99.5%)
- [x] model_config.json (version 3.0, dropout_risk)
- [x] feature_columns.json (22 features)
- [x] baseline.json

---

## 🎓 DIFERENÇAS TÉCNICAS

| Aspecto | Modelo v2.0 | **Modelo v3.0** ✅ |
|---------|-------------|-------------------|
| **Target** | `mean(IEG, IDA, Mat, Por) < 6.0` | `IEG < 5.0` |
| **Problema** | Notas baixas | **Risco de evasão** |
| **IEG** | Usado no target | **Usado no target** |
| **Notas** | Usadas no target | **FEATURES** 🎯 |
| **Features** | 18 | **22** |
| **ROC-AUC** | 97.4% | **99.5%** |
| **Distribuição** | 39.5% / 60.5% | 14.4% / 85.6% |
| **Interpretável** | Sim | **Sim** |
| **Acionável** | Reforço escolar | **Reengajamento** |

---

## 💡 POR QUE ESTA SOLUÇÃO ATENDE AO DATATHON

### Pergunta Original

> "Quero somente alunos com maior risco de evasão escolar de um ano para o outro"

### Nossa Resposta

#### ✅ Identificamos Risco de Evasão

- **Target**: IEG < 5.0 (desengajamento)
- **Proxy válido**: Desengajamento precede evasão
- **Proporção realista**: 14.4% em risco

#### ⚠️ Limitação Temporal

**Não temos dados ano-a-ano** (snapshot 2024 apenas).

**Solução**:
- Usamos **proxy de evasão** (IEG baixo)
- Modelo identifica **risco** antes de acontecer
- **Predição temporal simulada**: IEG < 5.0 hoje → alta chance evasão futura

#### ✅ MLOps Completo

- **Retreino**: Estratégia documentada (triggers, pipeline)
- **Monitoramento**: Drift detection (PSI)
- **Data Contracts**: Schema definido
- **Performance**: Métricas em produção (accuracy, latência)

#### ✅ Sistema Pronto para Produção

- 99.5% ROC-AUC (excelente)
- 96.76% cobertura de testes
- API funcional
- Documentação completa
- Validado e testado

---

## 🎯 PRÓXIMOS PASSOS

### Imediato (Já Pode Usar!)

1. ✅ Iniciar API: `uvicorn app.main:app --reload`
2. ✅ Acessar dashboard: http://localhost:8000
3. ✅ Fazer predições via POST /predict
4. ✅ Monitorar drift: `streamlit run monitoring/dashboard.py`

### Evolução Futura (Quando Tiver Dados Longitudinais)

**Se conseguir dados de alunos em múltiplos anos**:
1. Criar features temporais (delta_notas, tendência)
2. Target: evasão confirmada (status "Inativo" ou não aparece no ano seguinte)
3. Treinar modelo de **sobrevivência** (Cox, Kaplan-Meier)
4. Predizer "tempo até evasão" (mais sofisticado)

---

## 📞 SUPORTE

**Documentação**:
- `MODELO_EVASAO_README.md` - Completo
- `docs_contexto/03_PROPOSTA_NOVO_MODELO.md` - Justificativa técnica
- `scripts/analise_temporal.py` - Análise de dados

**Validação**:
```bash
python scripts/validar_rapido.py
```

**Troubleshooting**:
- Modelo não carrega? → `python -m src.train --threshold 5.0`
- API não sobe? → Verifique porta 8000 livre
- Testes falhando? → `pytest tests/ -v`

---

## ✅ CONCLUSÃO

**Modelo de Evasão Escolar (v3.0) está PRONTO para PRODUÇÃO!**

- ✅ **99.5% ROC-AUC** - Performance excepcional
- ✅ **96.76% cobertura** - Testes robustos
- ✅ **Prediz risco de evasão** - Via IEG < 5.0
- ✅ **22 features** - Notas agora são features!
- ✅ **API funcional** - Pronta para uso
- ✅ **MLOps completo** - Retreino, monitoring, contracts
- ✅ **Documentação completa** - Todos os aspectos cobertos

**🎓 Foco 100% em PREVENÇÃO DE EVASÃO via identificação de desengajamento!**
