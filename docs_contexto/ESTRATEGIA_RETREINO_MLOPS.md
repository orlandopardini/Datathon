# 🔄 Estratégia de Retreino e MLOps

**Versão**: 3.0  
**Data**: 03 de Março de 2026  
**Status**: ✅ Produção

---

## 📋 Visão Geral

Documento define **quando**, **como** e **por que** retreinar o modelo de predição de risco de evasão escolar.

---

## ⏰ QUANDO RETREINAR

### 1. Gatilhos Automáticos (Alta Prioridade)

#### 🔴 Drift Crítico Detectado
- **Condição**: PSI > 0.25 em qualquer feature crítica
- **Features críticas**: IPS, IAA, IPP, IDA, Mat, Por
- **Ação**: Retreino imediato (24-48h)
- **Justificativa**: Dados mudaram significativamente, modelo pode estar desatualizado

```python
# Exemplo de alerta
if psi_IPS > 0.25:
    TRIGGER: "DRIFT_CRITICO_IPS"
    ACAO: iniciar_retreino_imediato()
```

#### 🟠 Performance Drop
- **Condição**: Acurácia em produção < 90% (modelo atual: 97%)
- **Medida**: Comparar predições vs outcomes reais (quando disponível)
- **Ação**: Investigar causa + retreino em 1 semana
- **Justificativa**: Modelo perdendo capacidade preditiva

#### 🟡 Distribuição Shift
- **Condição**: % de alunos em risco mudou >15%
- **Baseline**: 14.4% em risco (IEG < 5.0)
- **Exemplo**: Se passar para >29% ou <7%, investigar
- **Ação**: Análise exploratória + retreino se confirmado

---

### 2. Gatilhos Calendário (Planejados)

#### 📅 Início do Ano Letivo
- **Frequência**: **Anual** (Fevereiro de cada ano)
- **Motivo**: Nova turma de alunos, possível mudança de perfil
- **Processo**: 
  1. Coletar dados do ano anterior (2025, 2026, etc)
  2. Retreinar com dados históricos + novos
  3. Validar em holdout set
  4. Deploy se métricas OK (ROC-AUC > 95%)

#### 📊 Review Trimestral
- **Frequência**: **Trimestral** (Março, Junho, Setembro, Dezembro)
- **Motivo**: Monitoramento proativo de performance
- **Processo**:
  1. Gerar relatório de drift (PSI all features)
  2. Comparar distribuição de predições
  3. Se PSI > 0.15 em múltiplas features → retreinar
  4. Se estável → manter modelo atual

---

### 3. Gatilhos de Volume

#### 📈 Novos Dados Acumulados
- **Condição**: +200 novos alunos desde último treino
- **Motivo**: Amostra suficiente para melhorar modelo
- **Ação**: Retreino opcional (se drift moderado)

---

## 🔧 COMO RETREINAR

### Pipeline Automatizado

```bash
# 1. Backup do modelo atual
procedures/backup_modelo.bat

# 2. Retreinar com novos dados
python scripts/retreino_automatizado.py --data-path database/PEDE_2026.xlsx

# 3. Validar novo modelo
python scripts/validar_modelo_evasao.py

# 4. A/B Test (opcional)
python scripts/ab_test_modelos.py --modelo-a app/model/model.joblib --modelo-b app/model/model_new.joblib

# 5. Deploy se métricas OK
python scripts/deploy_modelo.py --modelo model_new.joblib
```

### Critérios de Validação

**Novo modelo é aceito SE:**
1. ✅ ROC-AUC ≥ modelo atual (99.5%)
2. ✅ Acurácia ≥ 95%
3. ✅ Recall ≥ 75% (captura maioria dos casos em risco)
4. ✅ PSI < 0.25 em todas as features
5. ✅ Distribuição de predições similar (±10%)

**Se falhar qualquer critério**:
- 🔍 Investigar causa (dados ruins? features faltando?)
- 🛠️ Corrigir e retreinar
- ❌ Não deploy (manter modelo atual)

---

## 📊 MÉTRICAS DE PRODUÇÃO

### 1. Métricas de Negócio

#### Taxa de Intervenção
```python
taxa_intervencao = alunos_com_intervencao / alunos_preditos_em_risco
# Target: > 80% (maioria dos alertas deve gerar ação)
```

#### Taxa de Sucesso
```python
taxa_sucesso = alunos_reengajados / alunos_com_intervencao
# Target: > 50% (metade das intervenções funciona)
```

#### Falsos Positivos (Tolerância)
```python
fp_rate = falsos_positivos / total_predito_em_risco
# Tolerável: < 30% (1 em 3 pode ser FP aceitável)
# Crítico: Perder alunos em risco (FN) é PIOR que FP
```

### 2. Métricas Técnicas

#### Latência de Predição
- **Target**: < 200ms por aluno
- **Medida**: Tempo de resposta do endpoint `/predict`
- **Alerta**: Se latência > 500ms, investigar

#### Throughput
- **Target**: 100 predições/minuto
- **Medida**: Requests por segundo (RPS)
- **Alerta**: Se RPS cai abaixo de esperado

#### Disponibilidade
- **Target**: 99.5% uptime
- **Medida**: Health checks a cada 60s
- **Alerta**: Se 3 checks consecutivos falham

---

## 📝 DATA CONTRACTS

### Schema de Entrada (Obrigatório)

```python
from pydantic import BaseModel, Field, validator

class AlunoInput(BaseModel):
    # Obrigatórios
    Idade: int = Field(..., ge=8, le=25, description="Idade entre 8-25 anos")
    Genero: str = Field(..., regex="^(M|F|Masculino|Feminino)$")
    Ano_ingresso: int = Field(..., ge=2015, le=2026)
    Fase: str = Field(..., description="Ex: 1A, 3A, 5A, 7E, 9")
    Instituicao_ensino: str
    INDE_2024: float = Field(..., ge=0, le=10)
    IAA: float = Field(..., ge=0, le=10)
    IPS: float = Field(..., ge=0, le=10)
    Num_Av: int = Field(..., ge=0)
    
    # Opcionais
    IDA: Optional[float] = Field(None, ge=0, le=10)
    Mat: Optional[float] = Field(None, ge=0, le=10)
    Por: Optional[float] = Field(None, ge=0, le=10)
    Ing: Optional[float] = Field(None, ge=0, le=10)
    INDE_23: Optional[float] = Field(None, ge=0, le=10)
    INDE_22: Optional[float] = Field(None, ge=0, le=10)
    IPP: Optional[float] = Field(None, ge=0, le=10)
    IPV: Optional[float] = Field(None, ge=0, le=10)
    IAN: Optional[float] = Field(None, ge=0, le=10)
    
    @validator('Fase')
    def validate_fase(cls, v):
        valid_fases = ['ALFA', '1A', '1B', '1R', '2A', '3A', '4A', '5A', '6A', '7E', '8', '9']
        if v not in valid_fases:
            raise ValueError(f'Fase deve ser uma de: {valid_fases}')
        return v
```

### Validações de Qualidade

```python
# Great Expectations Suite
expectations = {
    "expect_column_values_to_be_between": {
        "Idade": {"min_value": 8, "max_value": 25},
        "INDE_2024": {"min_value": 0, "max_value": 10},
        "IAA": {"min_value": 0, "max_value": 10},
        "IPS": {"min_value": 0, "max_value": 10}
    },
    "expect_column_values_to_not_be_null": [
        "Idade", "Genero", "Ano_ingresso", "Fase", "INDE_2024", "IAA", "IPS"
    ],
    "expect_column_values_to_be_of_type": {
        "Idade": "int",
        "INDE_2024": "float",
        "Fase": "str"
    }
}
```

---

## 🔄 PROCESSO DE RETREINO COMPLETO

### Fase 1: Preparação (1-2 dias)

1. ✅ **Backup do modelo atual**
   ```bash
   cp app/model/model.joblib app/model/backups/model_v3.0_$(date +%Y%m%d).joblib
   ```

2. ✅ **Coletar novos dados**
   - Baixar nova base PEDE (ex: PEDE_2026.xlsx)
   - Validar schema (data contracts)
   - Verificar qualidade (missing values, outliers)

3. ✅ **Análise Exploratória**
   ```bash
   python scripts/analise_completa_database.py
   ```
   - Distribuição de IEG mudou?
   - Novas fases apareceram?
   - Features com valores anormais?

### Fase 2: Retreino (1 dia)

4. ✅ **Retreinar modelo**
   ```bash
   python -m src.train --threshold 5.0 --data-path database/PEDE_2026.xlsx --outdir app/model_new
   ```

5. ✅ **Validar métricas**
   ```bash
   python scripts/validar_modelo_evasao.py
   ```
   - ROC-AUC ≥ 99.5%?
   - Acurácia ≥ 95%?
   - Recall ≥ 75%?

### Fase 3: Testes (1-2 dias)

6. ✅ **A/B Test** (opcional mas recomendado)
   ```bash
   python scripts/ab_test_modelos.py
   ```
   - Comparar modelo novo vs antigo em holdout
   - Verificar se predições melhoram

7. ✅ **Teste em produção (canary)**
   - Deploy 10% do tráfego para novo modelo
   - Monitorar por 24h
   - Se estável, aumentar para 50%, depois 100%

### Fase 4: Deploy (1 dia)

8. ✅ **Deploy final**
   ```bash
   mv app/model_new/model.joblib app/model/model.joblib
   mv app/model_new/metrics.json app/model/metrics.json
   mv app/model_new/feature_columns.json app/model/feature_columns.json
   mv app/model_new/baseline.json app/model/baseline.json
   mv app/model_new/model_config.json app/model/model_config.json
   ```

9. ✅ **Validação pós-deploy**
   - Testar endpoint /predict
   - Verificar latência
   - Monitorar logs por 48h

10. ✅ **Documentação**
    - Atualizar CHANGELOG.md
    - Registrar versão (v3.1, v3.2, etc)
    - Documentar mudanças

---

## 📈 MONITORAMENTO CONTÍNUO

### Dashboard de Produção

```bash
streamlit run monitoring/dashboard.py
```

**Métricas Exibidas**:
1. 📊 PSI por feature (drift detection)
2. 📉 Distribuição de predições (% em risco)
3. ⏱️ Latência média
4. 📈 Volume de chamadas/dia
5. ⚠️ Alertas ativos

### Alertas Automáticos

```python
# Configurar alertas (ex: email, Slack, PagerDuty)
alertas = {
    "drift_critico": {
        "condicao": "psi > 0.25",
        "acao": "email_equipe + iniciar_retreino",
        "prioridade": "ALTA"
    },
    "performance_drop": {
        "condicao": "accuracy < 0.90",
        "acao": "notificar_equipe",
        "prioridade": "ALTA"
    },
    "latencia_alta": {
        "condicao": "latencia_p95 > 500ms",
        "acao": "investigar_infra",
        "prioridade": "MEDIA"
    }
}
```

---

## 🎯 EXEMPLO: Retreino Anual (Fevereiro 2027)

### Timeline

**Semana 1 (01-07 Fev)**:
- Coletar dados PEDE 2026 completos
- Validar schema e qualidade
- Análise exploratória

**Semana 2 (08-14 Fev)**:
- Retreinar modelo com dados 2026
- Validar métricas (ROC-AUC, Acurácia)
- A/B test vs modelo atual

**Semana 3 (15-21 Fev)**:
- Canary deploy (10% tráfego)
- Monitorar performance 24h
- Se OK, aumentar para 50%

**Semana 4 (22-28 Fev)**:
- Deploy full (100% tráfego)
- Monitorar por 7 dias
- Documentar lições aprendidas

---

## 📋 CHECKLIST PRÉ-DEPLOY

Antes de deployar modelo novo:

- [ ] ✅ ROC-AUC ≥ modelo atual
- [ ] ✅ Acurácia ≥ 95%
- [ ] ✅ Recall ≥ 75%
- [ ] ✅ PSI < 0.25 em todas features
- [ ] ✅ Distribuição de predições similar (±10%)
- [ ] ✅ Validado em holdout set
- [ ] ✅ A/B test completo
- [ ] ✅ Backup do modelo atual feito
- [ ] ✅ Documentação atualizada
- [ ] ✅ Testes de integração passando
- [ ] ✅ Plano de rollback definido

---

## 🔙 PLANO DE ROLLBACK

Se modelo novo causar problemas:

```bash
# 1. Restaurar backup imediatamente
cp app/model/backups/model_v3.0_20260302.joblib app/model/model.joblib

# 2. Reiniciar API
sudo systemctl restart datathon-api

# 3. Validar que voltou ao normal
curl http://localhost:8000/health

# 4. Investigar causa
python scripts/debug_modelo_problema.py
```

**Tempo de rollback**: < 5 minutos

---

## 📞 RESPONSABILIDADES

### Equipe de Dados
- Monitorar drift diariamente
- Executar retreino quando gatilhos dispararem
- Validar qualidade dos dados novos
- Documentar mudanças

### Equipe de Engenharia
- Manter API rodando (99.5% uptime)
- Implementar melhorias de performance
- Configurar alertas automáticos
- Gerenciar infraestrutura

### Coordenação Pedagógica
- Fornecer feedback sobre predições
- Reportar casos de falsos positivos/negativos
- Validar se intervenções estão funcionando
- Prover dados de outcome (aluno reengajou?)

---

## 📊 MÉTRICAS DE SUCESSO DO MLOPS

**Sistema MLOps é bem-sucedido quando**:

1. ✅ **Modelo sempre atualizado**: Retreino ocorre nos gatilhos definidos
2. ✅ **Alta disponibilidade**: API com >99% uptime
3. ✅ **Performance estável**: ROC-AUC mantém >95%
4. ✅ **Drift controlado**: PSI monitorado, alertas funcionando
5. ✅ **Deploy rápido**: Novo modelo em produção em <1 semana
6. ✅ **Rollback confiável**: Volta ao modelo anterior em <5 min
7. ✅ **Visibilidade total**: Dashboard mostra todas métricas

---

**🎯 Estratégia MLOps completa e pronta para produção!**
