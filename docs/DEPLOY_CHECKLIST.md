# ✅ Checklist de Deploy - Render

Use este checklist para garantir que tudo está pronto para deploy.

---

## 📋 Antes do Deploy

### Arquivos Essenciais

- [ ] `requirements.txt` - Dependências atualizadas
- [ ] `render.yaml` - Configuração do Render
- [ ] `app/main.py` - FastAPI app
- [ ] `app/routes.py` - Endpoints
- [ ] `app/model/model.joblib` - Modelo treinado
- [ ] `app/model/metrics.json` - Métricas do modelo
- [ ] `app/model/feature_columns.json` - Features esperadas
- [ ] `app/model/baseline.json` - Baseline para drift
- [ ] `src/` - Módulos de ML (train, preprocessing, etc)
- [ ] `.gitignore` - Configurado corretamente (modelo NÃO ignorado)
- [ ] `.env.example` - Template de variáveis de ambiente

### Código

- [ ] Porta configurada via variável `PORT` do Render
- [ ] CORS configurado (se necessário para frontend)
- [ ] Health check endpoint implementado (`/health`)
- [ ] Logs configurados (level INFO)
- [ ] Tratamento de erros nos endpoints
- [ ] Validação de input (Pydantic models)

### Modelo

- [ ] Modelo treinado e validado (ROC-AUC > 90%)
- [ ] Tamanho do modelo < 100MB (ou Git LFS configurado)
- [ ] Métricas documentadas
- [ ] Features documentadas

### Testes

- [ ] Testes unitários passando (`pytest tests/`)
- [ ] Coverage > 90% (idealmente)
- [ ] Testes de integração funcionando
- [ ] API testada localmente (`uvicorn app.main:app`)

---

## 🔧 Configuração do Render

### render.yaml

- [ ] `type: web` definido
- [ ] `runtime: python-3.11` especificado
- [ ] `buildCommand` correto
- [ ] `startCommand` usando `$PORT`
- [ ] `healthCheckPath: /health` configurado
- [ ] `plan: free` ou plano desejado
- [ ] `region` definido (oregon = mais próximo Brasil)
- [ ] Variáveis de ambiente configuradas

### Variáveis de Ambiente

- [ ] `ENVIRONMENT=production`
- [ ] `MODEL_VERSION=3.0`
- [ ] `LOG_LEVEL=INFO`
- [ ] Outras variáveis específicas do projeto

---

## 📦 Git e GitHub

### Repositório Local

- [ ] Git inicializado (`git init`)
- [ ] `.gitignore` configurado
- [ ] Commits organizados
- [ ] Branch `main` criada

### Repositório GitHub

- [ ] Repositório criado no GitHub
- [ ] Nome sugerido: `passos-magicos-evasao-api`
- [ ] Remote adicionado (`git remote add origin ...`)
- [ ] Código enviado (`git push -u origin main`)

### Arquivos no Repo

- [ ] Código-fonte completo
- [ ] `app/model/model.joblib` incluído (essencial!)
- [ ] Documentação incluída
- [ ] Scripts de utilidade incluídos

---

## 🚀 Deploy no Render

### Configuração

- [ ] Conta criada no Render (https://render.com)
- [ ] GitHub conectado ao Render
- [ ] Novo Web Service criado
- [ ] Repositório selecionado
- [ ] `render.yaml` detectado automaticamente

### Build

- [ ] Build iniciado (acompanhar logs)
- [ ] Dependências instaladas sem erros
- [ ] Tempo de build < 15 minutos
- [ ] Build concluído com sucesso

### Deploy

- [ ] Deploy iniciado
- [ ] Health check passando
- [ ] Aplicação rodando
- [ ] URL pública gerada

---

## ✅ Pós-Deploy

### Validação

- [ ] Health check: `curl https://SEU-APP.onrender.com/health`
- [ ] Docs acessíveis: `https://SEU-APP.onrender.com/docs`
- [ ] Endpoint raiz funcionando: `https://SEU-APP.onrender.com/`
- [ ] Predição funcionando: `POST /predict`

### Testes de Produção

```bash
# Health check
curl https://SEU-APP.onrender.com/health

# Predição de teste
curl -X POST https://SEU-APP.onrender.com/predict \
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

### Monitoramento

- [ ] Logs funcionando (Render Dashboard → Logs)
- [ ] Métricas de CPU/RAM visíveis
- [ ] Alertas configurados (se necessário)
- [ ] Uptime monitorado

### Documentação

- [ ] README atualizado com URL da API
- [ ] Documentação de endpoints atualizada
- [ ] Exemplos de uso atualizados
- [ ] Changelog atualizado

---

## 📊 Performance e Otimização

### Plano Free (512MB RAM)

- [ ] Cold start testado (~30s primeira req)
- [ ] Tempo de resposta OK (<2s)
- [ ] Memória suficiente para modelo

### Se Necessário Otimizar

- [ ] Lazy loading do modelo
- [ ] Compressão de resposta (gzip)
- [ ] Cache de predições comuns
- [ ] Upgrade para plano pago ($7/mês = 1GB RAM)

---

## 🔒 Segurança

- [ ] HTTPS habilitado (automático no Render)
- [ ] CORS configurado corretamente
- [ ] Secrets não estão no código
- [ ] Variáveis sensíveis em Environment Variables
- [ ] Rate limiting considerado (opcional)
- [ ] Autenticação considerada (se necessário)

---

## 📚 Documentação Adicional

- [ ] README principal atualizado
- [ ] DEPLOY_RENDER.md lido
- [ ] Troubleshooting conhecido
- [ ] Contatos de suporte documentados

---

## 🆘 Troubleshooting

Se algo der errado:

1. **Verificar logs**: Render Dashboard → Logs
2. **Testar localmente**: `uvicorn app.main:app`
3. **Verificar dependências**: `pip list`
4. **Verificar modelo**: `ls -lh app/model/`
5. **Consultar**: [docs_contexto/DEPLOY_RENDER.md](docs_contexto/DEPLOY_RENDER.md)

---

## 🎉 Deploy Concluído!

Quando todos os itens estiverem ✅:

**Sua API está PRONTA em produção!** 🚀

**URL**: `https://passos-magicos-evasao-api.onrender.com`  
**Docs**: `https://passos-magicos-evasao-api.onrender.com/docs`  
**Status**: Produção ✅

---

**Próximos passos**:
- Integrar com frontend
- Configurar monitoramento avançado
- Implementar analytics
- Adicionar autenticação

---

**Última atualização**: 2026-03-09  
**Versão**: 1.0
