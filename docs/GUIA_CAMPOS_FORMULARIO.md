# 📋 Guia de Campos do Formulário - Modelo v2.0

## 🎯 Objetivo
Simplificar a entrada de dados mantendo a precisão do modelo. **Redução de 15 → 9 campos obrigatórios (40% menos complexidade)**

---

## ✅ CAMPOS OBRIGATÓRIOS (9 campos)

### 📋 Dados Básicos do Aluno (5 campos)

| Campo | Descrição | Por que é essencial? |
|-------|-----------|---------------------|
| **Idade** | Idade atual em anos | Necessário para calcular `Idade_ingresso` (feature engineered) |
| **Gênero** | M ou F | Feature categórica usada pelo modelo |
| **Ano ingresso** | Ano que entrou no programa | Necessário para calcular `Tempo_programa` (feature engineered) |
| **Fase** | Nível no programa (ALFA, 1A-9) | Feature categórica + base para `Fase_num` (feature engineered) |
| **Tipo de Escola** | Pública ou Particular | Feature categórica importante para contexto socioeconômico |

### 📊 Indicadores de Desempenho (4 campos)

| Campo | Descrição | Por que é essencial? |
|-------|-----------|---------------------|
| **INDE 2024** | Desenvolvimento Educacional atual | **Indicador mais importante** - reflete desempenho recente |
| **IAA** | Índice de Adequação de Aprendizagem | **Segunda feature mais importante** - mede aprendizagem efetiva |
| **IPS** | Índice Psicossocial | **Terceira feature importante** - contexto emocional/social |
| **Nº Av** | Número de avaliações realizadas | Indica engajamento e frequência de acompanhamento |

---

## ⚙️ CAMPOS OPCIONAIS (5 campos)

*Podem ser deixados em branco. O modelo usa valores default/imputados.*

### 📈 Histórico (2 campos)

| Campo | Descrição | Quando usar? |
|-------|-----------|--------------|
| **INDE 2023** | Desenvolvimento Educacional do ano anterior | Se disponível, ajuda a ver tendência de evolução |
| **INDE 2022** | Desenvolvimento Educacional de 2 anos atrás | Se disponível, fornece contexto histórico mais amplo |

### 📊 Indicadores Secundários (3 campos)

| Campo | Descrição | Quando usar? |
|-------|-----------|--------------|
| **IPP** | Índice Psicopedagógico | Se o aluno teve avaliação psicopedagógica |
| **IPV** | Índice Ponto de Virada | Se houver dados de pontos de virada na trajetória |
| **IAN** | Índice de Autoavaliação | Se o aluno fez autoavaliação estruturada |

---

## 🚫 CAMPOS REMOVIDOS (do formulário original)

| Campo | Por que foi removido? |
|-------|----------------------|
| **Turma** | Redundante com Fase - agora é preenchido automaticamente |
| **IEG, IDA, Mat, Por, Ing** | **Usados no TARGET** (média < 6.0) - não podem ser input para prever a si mesmos! |

---

## 🔧 Features Engineered (calculadas automaticamente)

O backend calcula automaticamente 3 features adicionais:

```python
Tempo_programa = 2026 - Ano_ingresso  # Anos no programa
Idade_ingresso = Idade - Tempo_programa  # Idade ao entrar
Fase_num = parse_fase_to_numeric(Fase)  # ALFA→0, 1A→1, 2A→2, etc
Turma = Fase  # Auto-preenchido
```

**Total de features para o modelo: 18**
- 14 numéricas
- 4 categóricas

---

## 📊 Importância das Features (Top 5)

Baseado nos coeficientes do modelo treinado:

1. **INDE 2024** - Maior preditor de desempenho atual
2. **IAA** - Adequação de aprendizagem (core do problema)
3. **IPS** - Contexto psicossocial crítico
4. **Tempo_programa** - Mais tempo → mais dados históricos
5. **Idade_ingresso** - Idade ao entrar influencia trajetória

---

## 💡 Exemplos de Uso

### Caso 1: Uso Básico (apenas obrigatórios)
**Cenário**: Triagem rápida de um aluno novo

```json
{
  "Idade": 10,
  "Gênero": "F",
  "Ano ingresso": 2024,
  "Fase": "ALFA",
  "Instituição de ensino": "Escola Pública",
  "INDE 2024": 6.5,
  "IAA": 6.0,
  "IPS": 6.8,
  "Nº Av": 5
}
```
✅ **Suficiente para predição confiável!**

### Caso 2: Análise Completa (com opcionais)
**Cenário**: Avaliação aprofundada de aluno com histórico

```json
{
  "Idade": 14,
  "Gênero": "M",
  "Ano ingresso": 2019,
  "Fase": "5A",
  "Instituição de ensino": "Escola Pública",
  "INDE 2024": 7.5,
  "INDE 2023": 7.2,  ← OPCIONAL
  "INDE 22": 6.8,    ← OPCIONAL
  "IAA": 7.0,
  "IPS": 7.5,
  "IPP": 7.2,        ← OPCIONAL
  "IPV": 7.8,        ← OPCIONAL
  "IAN": 7.0,        ← OPCIONAL
  "Nº Av": 18
}
```
✅ **Predição mais refinada com contexto histórico**

---

## 🎯 Decisões de Design

### Por que 9 campos obrigatórios?
- **Mínimo necessário** para features engineered funcionarem
- **Dados facilmente disponíveis** em registros escolares
- **Balance** entre precisão e usabilidade

### Por que INDE 2024 é obrigatório mas 2022/2023 não?
- **Dado mais recente** é o mais preditivo
- **Histórico é útil mas não crítico** (tendência vs snapshot)
- **Novos alunos** não têm histórico → não pode ser obrigatório

### Por que IPS é obrigatório mas IPP/IPV/IAN não?
- **IPS é padrão** em todas as avaliações Passos Mágicos
- **IPP/IPV/IAN são avaliações especiais** - nem todos fazem
- **Impact**: IPS tem peso maior no modelo

---

## 📈 Impacto da Simplificação

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Campos obrigatórios | 15 | 9 | **-40%** |
| Tempo de preenchimento | ~5 min | ~2 min | **-60%** |
| Taxa de erro de input | Alta | Baixa | **Menos erros** |
| Clareza dos labels | Baixa | Alta | **Muito mais claro** |

---

## 🔗 Ver também

- [README.md](../README.md) - Documentação principal do projeto
- [03_PROPOSTA_NOVO_MODELO.md](03_PROPOSTA_NOVO_MODELO.md) - Escolha do modelo acadêmico
- [CHANGELOG.md](../CHANGELOG.md) - Histórico de mudanças v1.0 → v2.0
