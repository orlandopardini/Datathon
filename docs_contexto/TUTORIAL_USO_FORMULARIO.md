## 🎯 Como Usar o Formulário Simplificado

### Acesse o Dashboard
1. Inicie a API: `procedures\run.bat`
2. Abra no navegador: **http://localhost:8000**
3. Role até a seção **"🔮 Realizar Predição"**

---

### Exemplo Visual do Formulário

```
┌─────────────────────────────────────────────────────────────┐
│  🔮 Realizar Predição                                       │
├─────────────────────────────────────────────────────────────┤
│  📚 Modelo v2.0: Preencha os dados do aluno para prever o   │
│  risco de desempenho acadêmico baixo (média < 6.0).         │
│  Apenas os campos essenciais são solicitados.               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📋 Dados Básicos                                           │
├─────────────────────────────────────────────────────────────┤
│  Idade (anos completos)*         [____12____]               │
│  Gênero*                         [Masculino ▼]              │
│  Ano de Ingresso*                [____2020___]              │
│  (quando entrou no programa)                                │
│  Fase Atual*                     [3A ▼]                     │
│  (nível no programa)                                        │
│  Tipo de Escola*                 [Pública ▼]                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📊 Indicadores de Desempenho (escala 0-10)                 │
├─────────────────────────────────────────────────────────────┤
│  INDE 2024*                      [____5.0____]              │
│  (Desenvolvimento Educacional atual)                        │
│  IAA*                            [____4.5____]              │
│  (Adequação de Aprendizagem)                                │
│  IPS*                            [____5.2____]              │
│  (Psicossocial)                                             │
│  Nº de Avaliações*               [____10____]               │
│  (realizadas no ano)                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Campos Opcionais (clique para expandir) ▶               │
└─────────────────────────────────────────────────────────────┘

         [🎯 Calcular Risco Acadêmico]

```

---

### 📊 Resultado da Predição

Após clicar em **"Calcular Risco Acadêmico"**, você verá:

```
┌─────────────────────────────────────────────────────────────┐
│  Resultado da Predição                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│         ⚠️ Em Risco                                         │
│                                                              │
│  Probabilidade de Risco: 100.0%                             │
│  ████████████████████████████████████████ 100%              │
│                                                              │
│  Este estudante apresenta alto risco de desempenho          │
│  acadêmico baixo (média de notas < 6.0). Recomenda-se       │
│  acompanhamento pedagógico intensivo e suporte              │
│  psicopedagógico.                                           │
└─────────────────────────────────────────────────────────────┘
```

---

### ⚙️ Campos Opcionais Expandidos

Ao clicar em **"⚙️ Campos Opcionais"**:

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Campos Opcionais (clique para expandir) ▼               │
├─────────────────────────────────────────────────────────────┤
│  INDE 2023                       [___________]              │
│  (histórico)                     Deixe vazio se não souber  │
│                                                              │
│  INDE 2022                       [___________]              │
│  (histórico)                     Deixe vazio se não souber  │
│                                                              │
│  IPP                             [___________]              │
│  (Psicopedagógico)              Deixe vazio se não souber  │
│                                                              │
│  IPV                             [___________]              │
│  (Ponto de Virada)              Deixe vazio se não souber  │
│                                                              │
│  IAN                             [___________]              │
│  (Autoavaliação)                Deixe vazio se não souber  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎓 Casos de Uso

### Caso 1: Triagem Rápida
**Situação**: Novo aluno ingressou, sem histórico completo

**O que preencher**: Apenas os 9 campos obrigatórios
- Idade, gênero, ano ingresso, fase, tipo de escola
- INDE 2024, IAA, IPS, nº avaliações

**Tempo**: ~2 minutos  
**Resultado**: Predição confiável para primeira avaliação

---

### Caso 2: Avaliação Aprofundada
**Situação**: Aluno com 3+ anos no programa, histórico completo disponível

**O que preencher**: 9 campos obrigatórios + opcionais
- Adicionar INDE 2023, INDE 2022
- Adicionar IPP, IPV, IAN se disponível

**Tempo**: ~3-4 minutos  
**Resultado**: Predição mais refinada com contexto histórico

---

### Caso 3: Monitoramento Contínuo
**Situação**: Reavaliação semestral de todos os alunos

**O que preencher**: Apenas atualizar INDE 2024, IAA, IPS, Nº Av
- Dados básicos ficam os mesmos
- Histórico opcional se houve mudanças

**Tempo**: ~1 minuto (dados pré-existentes)  
**Resultado**: Acompanhamento da evolução do risco

---

## 🔍 Detalhes Técnicos (Backend)

### O que acontece quando você submete o formulário:

1. **Validação**: Frontend valida tipos e ranges
2. **Envio**: POST para `/predict` endpoint
3. **Feature Engineering Automático**:
   ```python
   Tempo_programa = 2026 - Ano_ingresso  # Ex: 2026 - 2020 = 6 anos
   Idade_ingresso = Idade - Tempo_programa  # Ex: 12 - 6 = 6 anos
   Fase_num = parse_fase_to_numeric(Fase)  # Ex: "3A" → 3.0
   Turma = Fase  # Auto-preenchido
   ```
4. **Imputação**: Campos opcionais vazios recebem valores default
5. **Predição**: Modelo processa 18 features
6. **Retorno**: Probabilidade (0-100%) e label (em risco / sem risco)

---

## ❓ FAQ

**P: O que acontece se eu deixar campos opcionais em branco?**  
R: O modelo usa valores imputados automaticamente (média ou moda dos dados de treino).

**P: Por que INDE 2024 é obrigatório mas 2022/2023 não?**  
R: O desempenho atual é o melhor preditor. Histórico ajuda mas não é essencial.

**P: Preciso calcular Tempo_programa manualmente?**  
R: Não! O backend calcula automaticamente baseado em Ano ingresso.

**P: Por que não posso inputar IEG, IDA, Mat, Por?**  
R: Essas notas são o TARGET do modelo (média < 6.0 = risco). Usar como input seria "vazamento de dados".

**P: O modelo funciona para alunos novos sem histórico?**  
R: Sim! Os 9 campos obrigatórios são suficientes para predição confiável.

---

## 📊 Comparação: Antes vs Depois

| Aspecto | v1.0 (Antes) | v2.0 (Depois) | Melhoria |
|---------|--------------|---------------|----------|
| Campos obrigatórios | 15 | 9 | **-40%** |
| Tempo de preenchimento | ~5 min | ~2 min | **-60%** |
| Clareza dos labels | ❌ Siglas sem contexto | ✅ Labels + tooltips | **Muito melhor** |
| Campos bem explicados | ❌ Não | ✅ Sim | **100%** |
| Suporte a dados parciais | ❌ Não | ✅ Sim (opcionais) | **Flexível** |
| Target correto | ❌ Defasagem | ✅ Desempenho | **Corrigido** |
| Predições intuitivas | ❌ Invertidas | ✅ Corretas | **Corrigido** |

---

## 🚀 Próximos Passos Sugeridos

1. **Testar com dados reais**: Use alunos conhecidos para validar predições
2. **Feedback dos educadores**: Coletar input sobre clareza dos campos
3. **Ajustar threshold**: Se 6.0 não for ideal, retreinar com novo valor
4. **Exportar resultados**: Adicionar botão para exportar predições em lote (CSV)
5. **Integração**: Conectar com sistema de gestão escolar existente

---

## 📞 Suporte

Dúvidas sobre os campos ou resultados? Consulte:
- [GUIA_CAMPOS_FORMULARIO.md](GUIA_CAMPOS_FORMULARIO.md) - Explicação detalhada
- [03_PROPOSTA_NOVO_MODELO.md](03_PROPOSTA_NOVO_MODELO.md) - Por que este modelo?
- [README.md](../README.md) - Documentação técnica completa
