# 🚀 Deploy no Render - Guia Completo

Este guia explica como fazer deploy da API de Predição de Risco de Evasão no Render.

---

## 📋 Pré-requisitos

1. ✅ Conta no [Render](https://render.com) (gratuita)
2. ✅ Repositório Git (GitHub, GitLab ou Bitbucket)
3. ✅ Modelo treinado em `app/model/`
4. ✅ Python 3.11+

---

## 🎯 Opção 1: Deploy Automático via GitHub (Recomendado)

### Passo 1: Preparar Repositório GitHub

```bash
# 1. Inicializar Git (se ainda não tiver)
git init
git add .
git commit -m "Initial commit - API Risco de Evasão v3.0"

# 2. Criar repositório no GitHub
# Acessar: https://github.com/new
# Nome sugerido: passos-magicos-evasao-api

# 3. Adicionar remote e fazer push
git remote add origin https://github.com/SEU_USUARIO/passos-magicos-evasao-api.git
git branch -M main
git push -u origin main
```

**IMPORTANTE**: Certifique-se de que os arquivos do modelo estão no repositório:
```bash
# Verificar tamanho dos arquivos
ls -lh app/model/

# Se model.joblib for muito grande (>100MB), considere usar Git LFS
git lfs track "*.joblib"
git add .gitattributes
```

### Passo 2: Conectar ao Render

1. **Login no Render**: https://dashboard.render.com
2. **New → Web Service**
3. **Connect Repository**: Conectar sua conta GitHub
4. **Selecionar Repositório**: `passos-magicos-evasao-api`

### Passo 3: Configurar o Serviço

O Render lerá automaticamente o arquivo `render.yaml`. Confirme as configurações:

| Campo | Valor |
|-------|-------|
| **Name** | `passos-magicos-evasao-api` |
| **Region** | `Oregon` (mais próximo do Brasil) |
| **Branch** | `main` |
| **Runtime** | `Python 3.11` |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

### Passo 4: Deploy!

1. Clique em **"Create Web Service"**
2. Aguarde o build (~3-5 minutos)
3. Acompanhe os logs em tempo real

### Passo 5: Testar a API

Após deploy bem-sucedido, sua API estará disponível em:

```
https://passos-magicos-evasao-api.onrender.com
```

**Testar endpoints**:

```bash
# Health check
curl https://passos-magicos-evasao-api.onrender.com/health

# Documentação interativa
# Acessar no navegador:
https://passos-magicos-evasao-api.onrender.com/docs

# Fazer predição
curl -X POST https://passos-magicos-evasao-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Idade": 15,
    "Genero": "M",
    "Ano_ingresso": 2020,
    "Fase": "2A",
    "Instituicao_ensino": "Pública",
    "INDE_2024": 7.5,
    "IAA": 8.0,
    "IPS": 7.0,
    "Nro_Av": 4
  }'
```

---

## 🎯 Opção 2: Deploy Manual (Blueprint)

Se preferir configurar manualmente sem conectar ao Git:

### Passo 1: Criar Serviço Manualmente

1. **Dashboard Render** → **New** → **Web Service**
2. **Selecionar "Build and deploy from a Git repository"**
3. **Public Git Repository**: Colar URL do repo
4. **Configurar manualmente** (ver tabela acima)

### Passo 2: Adicionar Variáveis de Ambiente

Em **Environment**:

```
ENVIRONMENT=production
MODEL_VERSION=3.0
LOG_LEVEL=INFO
PYTHON_VERSION=3.11
```

### Passo 3: Deploy

Clique em **"Create Web Service"** e aguarde.

---

## 📦 O que Acontece no Deploy

### 1. Build Phase
```bash
# Render executa automaticamente:
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Start Phase
```bash
# Inicia servidor na porta definida pelo Render ($PORT)
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. Health Check
```bash
# Render verifica periodicamente:
GET /health
# Espera resposta 200 OK
```

---

## 🔧 Configurações Importantes

### Limites do Plano Free

| Recurso | Limite Free |
|---------|------------|
| **RAM** | 512 MB |
| **CPU** | Compartilhado |
| **Disco** | 1 GB |
| **Bandwidth** | 100 GB/mês |
| **Build Time** | 15 min/build |
| **Dormência** | Após 15 min inatividade |

**NOTA**: No plano free, a API "dorme" após 15 minutos de inatividade. A primeira requisição após dormir pode levar ~30 segundos para responder (cold start).

### Persistência de Dados

O modelo e logs precisam estar no código/repositório, pois o filesystem é **efêmero**:

- ✅ **Persistente**: Arquivos no repositório Git
- ❌ **Não persistente**: Arquivos criados em runtime (logs, backups)

**Solução**: Use o Render Disk (pago) ou armazenamento externo (S3, GCS).

---

## 🐛 Troubleshooting

### Problema 1: "Application failed to respond"

**Causa**: Porta incorreta ou app não está ouvindo em `0.0.0.0`

**Solução**:
```python
# Em app/main.py, garantir que usa variável de ambiente
import os
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
```

### Problema 2: "Module not found"

**Causa**: Dependência faltando em `requirements.txt`

**Solução**: Atualizar `requirements.txt`:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Problema 3: "Model file not found"

**Causa**: Arquivos do modelo não estão no repositório

**Solução**: Verificar `.gitignore` e adicionar modelo:
```bash
# Remover do .gitignore se necessário
git add app/model/model.joblib -f
git commit -m "Add trained model"
git push
```

### Problema 4: "Out of memory"

**Causa**: Modelo muito grande para 512MB RAM

**Soluções**:
1. **Otimizar modelo**: Usar `model = joblib.load('model.joblib', mmap_mode='r')`
2. **Upgrade para plano pago** ($7/mês = 1GB RAM)
3. **Lazy loading**: Carregar modelo só quando necessário

### Problema 5: "Build timeout"

**Causa**: Build levando mais de 15 minutos

**Solução**: Otimizar `requirements.txt` (remover deps desnecessárias)

---

## 🔒 Segurança

### Adicionar CORS

Já configurado em `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Para produção**, restringir origins:
```python
allow_origins=[
    "https://seu-frontend.com",
    "https://passos-magicos.org.br"
]
```

### Rate Limiting (Opcional)

Instalar:
```bash
pip install slowapi
```

Adicionar em `app/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("60/minute")  # 60 requisições por minuto
async def predict(request: Request, item: PredictItem):
    ...
```

---

## 📊 Monitoramento

### Logs no Render

1. **Dashboard** → **Seu serviço** → **Logs**
2. Logs em tempo real da aplicação
3. Filtrar por nível (INFO, ERROR, etc)

### Health Check Endpoint

```python
# Já implementado em app/main.py
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_version": "3.0",
        "timestamp": datetime.now().isoformat()
    }
```

### Métricas no Render

- **CPU Usage**: Dashboard → Metrics
- **Memory Usage**: Dashboard → Metrics
- **Response Time**: Dashboard → Metrics
- **Error Rate**: Logs → Filtrar por ERROR

---

## 🔄 Atualizar Modelo (Retreino)

Quando retreinar o modelo:

```bash
# 1. Retreinar localmente
python scripts/retreino_automatizado.py

# 2. Commitar novo modelo
git add app/model/model.joblib app/model/metrics.json
git commit -m "Update model v3.1 - ROC-AUC 99.6%"

# 3. Push (deploy automático)
git push origin main

# 4. Render fará deploy automático (~3 min)
```

---

## 💰 Custos

### Plano Free (Recomendado para MVP)
- **Custo**: $0/mês
- **Limitações**: 512MB RAM, dormência após 15 min
- **Ideal para**: Testes, demos, baixo volume

### Plano Starter ($7/mês)
- **RAM**: 1GB
- **Sem dormência**: Always-on
- **Ideal para**: Produção, uso frequente

### Plano Pro ($25/mês)
- **RAM**: 2GB
- **Auto-scaling**: Sim
- **Ideal para**: Alto volume, SLA crítico

---

## 🌐 Custom Domain (Opcional)

### Usar domínio próprio

1. **Dashboard** → **Settings** → **Custom Domain**
2. Adicionar: `api.passos-magicos.org.br`
3. Configurar DNS:
   ```
   CNAME api passos-magicos-evasao-api.onrender.com
   ```
4. Aguardar propagação (~1h)
5. SSL automático via Let's Encrypt

---

## 📝 Checklist de Deploy

Antes de fazer deploy, verificar:

- [ ] `requirements.txt` atualizado
- [ ] Modelo treinado em `app/model/`
- [ ] `render.yaml` configurado
- [ ] Variáveis de ambiente definidas
- [ ] `.gitignore` correto (não ignorar modelo)
- [ ] Testes passando localmente (`pytest`)
- [ ] Health check funcionando (`GET /health`)
- [ ] Documentação da API acessível (`/docs`)
- [ ] CORS configurado corretamente
- [ ] README.md atualizado com URL da API

---

## 🆘 Suporte

### Documentação Oficial
- **Render Docs**: https://render.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Uvicorn**: https://www.uvicorn.org

### Comunidade
- **Render Community**: https://community.render.com
- **FastAPI Discord**: https://discord.gg/fastapi

---

## 🎉 Deploy Completo!

Após seguir este guia, você terá:

✅ API funcionando em produção  
✅ URL pública acessível  
✅ Health check configurado  
✅ Deploy automático no push  
✅ Logs centralizados  
✅ SSL/HTTPS automático  

**URL da sua API**: `https://passos-magicos-evasao-api.onrender.com`  
**Documentação**: `https://passos-magicos-evasao-api.onrender.com/docs`

---

**Próximos passos**:
1. Integrar frontend com a API
2. Configurar monitoramento (Sentry, New Relic)
3. Implementar analytics (PostHog, Mixpanel)
4. Adicionar autenticação (JWT, OAuth)

---

**Última atualização**: 2026-03-09  
**Versão**: 1.0  
**Status**: Pronto para produção ✅
