FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação e modelo (FORÇA REBUILD - 2026-03-10)
COPY app/ ./app/
COPY src/ ./src/

# Verificar que o modelo foi copiado corretamente
RUN python -c "import joblib; model = joblib.load('app/model/model.joblib'); print('Modelo carregado com sucesso!')"

# Expor porta (Render usa variável $PORT)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
