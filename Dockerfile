FROM python:3.11-slim

# CACHE BREAKER - Força rebuild completo - Timestamp: 2026-03-10-01:20
ENV MODEL_VERSION=v3.1-fixed-multiclass-2026-03-10-01:20
ENV REBUILD_TRIGGER=20260310012000

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# COPIAR MODELO PRIMEIRO (importante para debugging)
COPY app/model/ ./app/model/

# Verificar modelo ANTES de copiar resto do código
RUN python -c "import joblib; \
    model = joblib.load('app/model/model.joblib'); \
    clf = model.named_steps['clf']; \
    print('✅ Modelo carregado com sucesso!'); \
    print('Solver:', clf.solver); \
    print('Has multi_class attr:', hasattr(clf, 'multi_class')); \
    assert not hasattr(clf, 'multi_class'), 'ERRO: Modelo ainda tem multi_class!'"

# Copiar resto do código
COPY app/ ./app/
COPY src/ ./src/

# Expor porta (Render usa variável $PORT)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
