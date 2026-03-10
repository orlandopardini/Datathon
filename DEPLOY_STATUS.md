# 🚀 Deploy Realizado com Sucesso!

Código enviado para: **https://github.com/orlandopardini/Datathon**

---

## ✅ Status Atual

- ✅ **153 arquivos** enviados (5.95 MB)
- ✅ **Modelo treinado** incluído em `app/model/`
- ✅ **Configuração Render** pronta em `render.yaml`
- ✅ **Documentação completa** disponível

---

## 🎯 Próximo Passo: Deploy no Render

### 1️⃣ Acesse o Render Dashboard
👉 https://dashboard.render.com

### 2️⃣ Crie um Novo Web Service
- Clique em **"New +"** → **"Web Service"**

### 3️⃣ Conecte o GitHub
- Se ainda não conectou, autorize o Render a acessar seus repositórios

### 4️⃣ Selecione o Repositório
```
orlandopardini/Datathon
```

### 5️⃣ Configuração Automática
O Render detectará automaticamente o `render.yaml` com as seguintes configurações:

| Campo | Valor |
|-------|-------|
| **Name** | `passos-magicos-evasao-api` |
| **Runtime** | `Python 3.11` |
| **Region** | `Oregon` (mais próximo do Brasil) |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` (512MB RAM) |

### 6️⃣ Criar Web Service
- Revise as configurações
- Clique em **"Create Web Service"**

### 7️⃣ Aguardar Deploy
- ⏱️ Tempo estimado: **3-5 minutos**
- 📊 Acompanhe os logs em tempo real no dashboard
- ✅ Quando concluir, verá: "Build & Deploy successful"

---

## 🌐 URL da Sua API (Após Deploy)

### API Principal
```
https://passos-magicos-evasao-api.onrender.com
```

### Documentação Interativa (Swagger)
```
https://passos-magicos-evasao-api.onrender.com/docs
```

### Health Check
```
https://passos-magicos-evasao-api.onrender.com/health
```

---

## 🧪 Testar a API Após Deploy

### Teste 1: Health Check
```bash
curl https://passos-magicos-evasao-api.onrender.com/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "model_version": "3.0",
  "timestamp": "2026-03-09T..."
}
```

### Teste 2: Fazer uma Predição
```bash
curl -X POST https://passos-magicos-evasao-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Idade": 15,
    "Genero": "M",
    "Ano_ingresso": 2020,
    "Fase": "2A",
    "Instituicao_ensino": "Publica",
    "INDE_2024": 7.5,
    "IAA": 8.0,
    "IPS": 7.0,
    "Nro_Av": 4
  }'
```

**Resposta esperada:**
```json
{
  "prediction": 0,
  "probability": 0.15,
  "risk_level": "Baixo Risco",
  "message": "Aluno com BAIXO risco de evasão",
  "model_version": "3.0"
}
```

---

## 📚 Documentação

- **Guia Rápido**: [DEPLOY_QUICKSTART.md](DEPLOY_QUICKSTART.md)
- **Guia Completo**: [docs_contexto/DEPLOY_RENDER.md](docs_contexto/DEPLOY_RENDER.md)
- **Checklist**: [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)
- **README Principal**: [README.md](README.md)

---

## 🆘 Problemas Comuns

### "Application failed to respond"
- **Causa**: Porta incorreta ou app não ouvindo em `0.0.0.0`
- **Solução**: Verificar que `startCommand` usa `$PORT` (variável do Render)

### "Module not found"
- **Causa**: Dependência faltando em `requirements.txt`
- **Solução**: Atualizar `requirements.txt` e fazer novo commit/push

### "Model file not found"
- **Causa**: Modelo não está no repositório Git
- **Solução**: Já está incluído! Se não funcionar, verificar `.gitignore`

### "Out of memory"
- **Causa**: Modelo muito grande para 512MB RAM (plano free)
- **Solução**: Upgrade para plano Starter ($7/mês = 1GB RAM)

### Deploy demora muito
- **Primeira vez**: Pode levar até 5 minutos (instalando dependências)
- **Deploys seguintes**: ~2-3 minutos (cache de dependências)

---

## 🔄 Atualizar o Modelo (Futuro)

Quando retreinar o modelo:

```bash
# 1. Retreinar
python scripts/retreino_automatizado.py

# 2. Commitar modelo atualizado
git add app/model/
git commit -m "Update model v3.1 - ROC-AUC 99.7%"
git push origin main

# 3. Render fará deploy automático em ~3 minutos
```

---

## 💡 Dicas

### Cold Start no Plano Free
- ⚠️ No plano free, a API "dorme" após 15 minutos de inatividade
- 🐌 Primeira requisição após dormir pode levar ~30 segundos
- 💰 Plano Starter ($7/mês) mantém API sempre ativa

### Monitoramento
- 📊 Acesse **Metrics** no dashboard para ver CPU/RAM
- 📝 Acesse **Logs** para ver requisições e erros
- 🔔 Configure **Notifications** para alertas

### Custom Domain (Opcional)
- Adicione domínio próprio: `api.passos-magicos.org.br`
- SSL/HTTPS automático via Let's Encrypt

---

## 🎉 Sucesso!

Seu projeto está **pronto para produção**! 🚀

**Repositório**: https://github.com/orlandopardini/Datathon  
**Modelo**: v3.0 - Risco de Evasão (ROC-AUC 99.5%)  
**Status**: Aguardando deploy no Render ⏳

---

**Última atualização**: 2026-03-09  
**Próxima ação**: Deploy no Render (3-5 minutos)
