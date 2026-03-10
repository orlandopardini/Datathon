# 🚀 Quick Deploy Guide

Guia rápido para fazer deploy no Render em 5 minutos.

---

## ✅ Modelo Já Incluído

**Importante**: O modelo já vem **treinado e validado** no repositório.  
Você **não precisa treinar** - apenas fazer deploy!

📦 Localização: `app/model/model.joblib` (já no GitHub)

---

## ⚡ Deploy Rápido (5 minutos)

### 1. Código Já Está no GitHub

✅ **Repositório**: https://github.com/orlandopardini/Datathon  
✅ **Modelo incluído**: app/model/model.joblib  
✅ **Configuração**: render.yaml

**Não precisa fazer nada localmente!**

1. Acesse: https://dashboard.render.com
2. Clique em **"New"** → **"Web Service"**
3. Conecte sua conta GitHub (se ainda não conectou)
4. Selecione o repositório: **orlandopardini/Datathon**
5. Render detectará automaticamente `render.yaml`
6. Clique em **"Create Web Service"**
7. Aguarde ~3-5 minutos

### 3. Testar API

Após deploy concluído:

```bash
# Health check
curl https://passos-magicos-evasao-api.onrender.com/health

# Documentação Swagger (abrir no navegador)
https://passos-magicos-evasao-api.onrender.com/docs
```

### 4. Fazer Predição

Acesse a documentação Swagger: `/docs`

Ou use curl:

---

## 🎉 Pronto!

Sua API está no ar em:
**https://passos-magicos-evasao-api.onrender.com**

---

## 📚 Documentação Completa

Para informações detalhadas, troubleshooting e configurações avançadas:

👉 [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

## 🆘 Problemas Comuns

### "Application failed to respond"
- Verifique se porta está correta no `render.yaml`
- Confira logs no Render Dashboard

### "Model not found"
- Verifique se `app/model/model.joblib` está no repo
- Confirme que `.gitignore` não está bloqueando o modelo

### "Out of memory"
- Modelo muito grande para plano free (512MB)
- Solução: Upgrade para Starter ($7/mês) ou otimizar modelo

---

## 🔄 Atualizar Modelo

```bash
# 1. Retreinar
python scripts/retreino_automatizado.py

# 2. Commit e push
git add app/model/
git commit -m "Update model v3.1"
git push

# Deploy automático em ~3 minutos
```

---

**Tempo total**: ~5 minutos  
**Custo**: $0 (plano free)  
**Status**: Produção ready ✅
