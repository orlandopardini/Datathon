# 📋 RESUMO EXECUTIVO - Reformulação do Modelo Preditivo

**Data**: 23 Fevereiro 2026  
**Status**: ⚠️ AGUARDANDO DECISÃO

---

## 🔴 O PROBLEMA

Seu modelo atual **NÃO está fazendo o que você pensa**.

### O que você espera:
```
📝 Aluno com notas BAIXAS (1, 1, 1, 1, 1) → ALTO risco ❌
📝 Aluno com notas ALTAS (9, 9, 9, 9, 9) → BAIXO risco ❌
```

### O que está acontecendo:
```
📝 Aluno com notas BAIXAS → 4% de risco (BAIXO) ❌
📝 Aluno com notas ALTAS → 76% de risco (ALTO) ❌
```

**🔍 Por quê?**  
O modelo prevê **"DEFASAGEM"** (tempo no programa / atraso de fase) e não **"RISCO ACADÊMICO"** (desempenho ruim).

- "Defasagem" = Aluno está em uma fase abaixo da ideal para sua idade
- Alunos em fases avançadas (mais velhos) têm ALTA defasagem (ficaram mais tempo)
- Alunos em fases iniciais (mais jovos) têm BAIXA defasagem (acabaram de entrar)
- **Notas NÃO importam** para medir tempo no programa

---

## ✅ A SOLUÇÃO

### OPÇÃO A: Modelo de Risco de Desempenho Acadêmico (RECOMENDADA)

**Novo Target**:
```python
at_risk = 1 se MÉDIA(IEG, IDA, Mat, Por) < 6.0
at_risk = 0 caso contrário
```

**O que muda**:
- ✅ Notas BAIXAS → ALTO risco (faz sentido!)
- ✅ Notas ALTAS → BAIXO risco (faz sentido!)
- ✅ Educadores sabem o que fazer (reforço escolar)
- ✅ Dashboard mostra informações úteis

**Tempo**: 2-3 dias de implementação

---

## 🎯 OUTRAS OPÇÕES

### OPÇÃO B: Modelo de Risco de Evasão
- **Target**: IEG (Engajamento) < 5.0 = risco de abandonar programa
- **Quando usar**: Se prioridade é RETENÇÃO de alunos
- **Tempo**: 3-4 dias

### OPÇÃO C: Predição de Notas Futuras
- **Target**: Prever nota do próximo ano
- **Quando usar**: Se tiver dados de alunos em múltiplos anos
- **Tempo**: 5-7 dias + requer dados longitudinais
- ⚠️ **NÃO VIÁVEL AGORA** (dados atuais são snapshot de 2024)

---

## 📊 COMPARAÇÃO RÁPIDA

| Critério | Opção A | Opção B | Opção C |
|----------|---------|---------|---------|
| Resolve problema atual | ✅ SIM | ✅ SIM | ⚠️ Parcial |
| Viável com dados atuais | ✅ SIM | ✅ SIM | ❌ NÃO |
| Fácil de explicar | ✅ SIM | ✅ SIM | ✅ SIM |
| Acionável para educadores | ✅ SIM | ✅ SIM | ✅ SIM |
| Tempo de implementação | 2-3 dias | 3-4 dias | 5-7 dias |

---

## 🚀 PRÓXIMOS PASSOS

### 1️⃣ VOCÊ DECIDE (5 minutos)
Responda estas 4 perguntas:

**a) Qual problema você quer resolver?**
- [ ] Alunos com desempenho acadêmico ruim (notas baixas) → OPÇÃO A
- [ ] Alunos em risco de abandonar o programa (evasão) → OPÇÃO B
- [ ] Outro: __________

**b) Qual threshold de "risco" faz sentido?**
- [ ] Média das notas < 6.0 (recomendo)
- [ ] Média das notas < 5.5 (mais restritivo)
- [ ] Outro: __________

**c) Prioridade para o modelo:**
- [ ] Capturar TODOS os alunos em risco (pode gerar alguns falsos alarmes)
- [ ] Só alertar quando tiver CERTEZA (pode perder alguns casos)
- [ ] Balanço entre os dois (recomendo)

**d) Você tem dados históricos?**
- [ ] SIM - Mesmo aluno aparece em múltiplos anos/períodos
- [ ] NÃO - Só tenho snapshot de 2024
- [ ] Não sei

---

### 2️⃣ EU IMPLEMENTO (2-3 dias)
- Redefino o target conforme sua escolha
- Re-treino o modelo com nova definição
- Atualizo todos os testes (manter 81%+ cobertura)
- Re-escrevo documentação

---

### 3️⃣ NÓS VALIDAMOS (1 dia)
- Testamos juntos vários cenários
- Confirmamos que predições fazem sentido
- Ajustamos se necessário

---

### 4️⃣ DEPLOY (1 dia)
- Modelo novo em produção
- API funcionando
- Dashboard atualizado

---

## 💰 INVESTIMENTO

**Tempo Total**: 4-5 dias úteis  
**Resultado**: Modelo que REALMENTE prevê o que você precisa

---

## 📞 DECISÃO NECESSÁRIA AGORA

**Complete isto e envie de volta:**

```
DECISÃO:
[ ] Opção A: Risco de Desempenho Acadêmico (RECOMENDADO)
[ ] Opção B: Risco de Evasão
[ ] Opção C: Predição de Notas (requer dados longitudinais)

RESPOSTAS:
a) Problema prioritário: _________________________
b) Threshold de risco: _________________________
c) Prioridade: _________________________
d) Dados históricos: [ ] Sim [ ] Não

APROVAÇÃO PARA PROSSEGUIR:
[ ] SIM, pode começar implementação
[ ] NÃO, preciso discutir mais
[ ] Tenho dúvidas: _________________________
```

---

## 📄 Documentação Completa

Para análise detalhada, consulte:
- [`01_CONTEXTO_ATUAL.md`](01_CONTEXTO_ATUAL.md) - Estado atual do projeto
- [`02_ANALISE_DATABASE.md`](02_ANALISE_DATABASE.md) - Análise completa dos dados
- [`03_PROPOSTA_NOVO_MODELO.md`](03_PROPOSTA_NOVO_MODELO.md) - Proposta detalhada

---

**Aguardando sua decisão para prosseguir! 🎯**
