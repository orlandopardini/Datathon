FROM python:3.11-slim

# CACHE BREAKER ULTRA - Força rebuild completo - Timestamp: 2026-03-10-01:30
ENV MODEL_VERSION=v3.2-verified-no-multiclass-2026-03-10-01:30
ENV REBUILD_TRIGGER=20260310013000
ENV FORCE_NEW_MODEL=true

WORKDIR /app

# LIMPAR QUALQUER CACHE DE MODELO ANTIGO
RUN rm -rf /app/model /app/app/model /tmp/*.joblib /tmp/joblib_* 2>/dev/null || true

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# COPIAR SCRIPT DE VERIFICAÇÃO PRIMEIRO
COPY verify_model.py ./

# COPIAR MODELO
COPY app/model/ ./app/model/

# VERIFICAÇÃO RIGOROSA DO MODELO (FALHA SE multi_class EXISTIR)
RUN python verify_model.py

# Copiar resto do código
COPY app/ ./app/
COPY src/ ./src/

# Expor porta (Render usa variável $PORT)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
