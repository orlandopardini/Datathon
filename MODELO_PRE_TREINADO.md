# ⚠️ IMPORTANTE: Modelo Pré-Treinado

## ✅ Modelo Já Incluído no Repositório

Este projeto **já vem com o modelo treinado e validado**. Você **NÃO precisa** treinar novamente para usar a API.

### 📦 Arquivos do Modelo (já incluídos)

Localização: `app/model/`

- ✅ `model.joblib` - Modelo treinado (8.4 KB)
- ✅ `metrics.json` - Métricas de validação (ROC-AUC: 99.5%)
- ✅ `model_config.json` - Configurações do modelo v3.0
- ✅ `feature_columns.json` - Features esperadas
- ✅ `baseline.json` - Baseline para drift detection (238 KB)

### 🚀 Como Usar

**Para uso normal da API:**
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Acesse:**
- Dashboard: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- API ReDoc: http://localhost:8000/redoc

### 🔄 Quando Retreinar?

Você só precisa retreinar o modelo em casos específicos:

1. **Novos dados disponíveis** (ex: PEDE 2025)
2. **Drift detectado** (PSI > 0.25 no dashboard de monitoramento)
3. **Performance caiu** (acurácia < 90%)
4. **Mudanças nas features** (novos indicadores)

### 📚 Script de Retreino (Apenas para Desenvolvimento)

Se você tiver novos dados e quiser retreinar:

```bash
# 1. Validar dados
python scripts/validar_data_contracts.py

# 2. Backup do modelo atual
python scripts/backup_modelo.py

# 3. Retreino automatizado
python scripts/retreino_automatizado.py
```

Ver documentação completa: [docs_contexto/ESTRATEGIA_RETREINO_MLOPS.md](docs_contexto/ESTRATEGIA_RETREINO_MLOPS.md)

---

## 🎯 Para Deploy em Produção

O modelo **já está pronto** para deploy no Render:

1. Código já inclui modelo treinado ✅
2. `render.yaml` configurado ✅
3. Dependências em `requirements.txt` ✅

**Próximos passos:**
1. Push para GitHub (já feito ✅)
2. Deploy no Render (ver [DEPLOY_QUICKSTART.md](DEPLOY_QUICKSTART.md))

---

## ❓ FAQ

**Q: Preciso do arquivo Excel para rodar a API?**  
A: **Não**. O modelo já foi treinado com os dados PEDE 2024. O Excel só é necessário se você quiser retreinar.

**Q: Como fazer predições?**  
A: Acesse http://localhost:8000/docs e use o endpoint `/predict`

**Q: O modelo é bom?**  
A: Sim! ROC-AUC de 99.5%, Accuracy 97.0%, validado com dados reais.

**Q: Posso usar em produção?**  
A: Sim! Modelo testado, validado e pronto para produção.

---

**Última atualização**: 2026-03-09  
**Versão do modelo**: 3.0  
**Status**: Pronto para uso ✅
