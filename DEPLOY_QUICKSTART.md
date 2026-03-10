# 🚀 Quick Deploy Guide

Guia rápido para fazer deploy no Render em 5 minutos.

---

## ⚡ Deploy Rápido (5 minutos)

### 1. Preparar Projeto

```bash
# Windows
prepare-deploy.bat

# Linux/Mac
bash prepare-deploy.sh
```

### 2. Criar Repositório GitHub

1. Acesse: https://github.com/new
2. Nome: `passos-magicos-evasao-api`
3. Deixe vazio (não adicione README, .gitignore, etc)

### 3. Push para GitHub

```bash
git remote add origin https://github.com/SEU_USUARIO/passos-magicos-evasao-api.git
git push -u origin main
```

### 4. Deploy no Render

1. Acesse: https://dashboard.render.com
2. Clique em **"New"** → **"Web Service"**
3. Conecte sua conta GitHub (se ainda não conectou)
4. Selecione o repositório `passos-magicos-evasao-api`
5. Render detectará automaticamente `render.yaml`
6. Clique em **"Create Web Service"**
7. Aguarde ~3-5 minutos

### 5. Testar API

Após deploy concluído:

```bash
# Health check
curl https://passos-magicos-evasao-api.onrender.com/health

# Documentação (abrir no navegador)
https://passos-magicos-evasao-api.onrender.com/docs
```

---

## 🎉 Pronto!

Sua API está no ar em:
**https://passos-magicos-evasao-api.onrender.com**

---

## 📚 Documentação Completa

Para informações detalhadas, troubleshooting e configurações avançadas:

👉 [DEPLOY_RENDER.md](docs_contexto/DEPLOY_RENDER.md)

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
