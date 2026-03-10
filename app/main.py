from __future__ import annotations

import warnings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# Suprimir warnings do sklearn durante predições
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

app = FastAPI(
    title="API de Predição - Risco de Evasão Escolar | Passos Mágicos",
    version="3.0.0",
    description="""
    ## 🎯 API de Predição de Risco de Evasão Escolar
    
    **Modelo**: v3.0 - Dropout Risk Prediction (ROC-AUC: 99.5%)
    
    ### 📊 O que este modelo faz?
    
    Prediz o risco de **evasão escolar** de estudantes com base em indicadores de engajamento:
    - **Alto Risco**: IEG < 5.0 (engajamento baixo)
    - **Baixo Risco**: IEG ≥ 5.0 (engajamento adequado)
    
    ### 🚀 Como usar:
    
    1. Use o endpoint `/predict` para fazer predições
    2. Envie os dados do estudante (idade, fase, indicadores, etc)
    3. Receba a predição com probabilidade e nível de risco
    
    ### 📚 Documentação Completa:
    
    - **Swagger UI**: [/docs](/docs) (esta página)
    - **ReDoc**: [/redoc](/redoc)
    - **Dashboard**: [/dashboard](/dashboard)
    
    ### 💻 Modelo Pré-Treinado:
    
    ✅ O modelo já vem **treinado e validado** com os dados PEDE 2024
    - Não é necessário treinar novamente
    - Métricas validadas: ROC-AUC 99.5%, Accuracy 97.0%
    - Pronto para uso em produção
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Passos Mágicos",
        "url": "https://github.com/orlandopardini/Datathon",
    },
    license_info={
        "name": "MIT",
    }
)

# CORS - Allow all origins (ajustar para produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios: ["https://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root route - Redirect to docs or serve dashboard
@app.get("/", include_in_schema=False)
async def read_root():
    """Redireciona para documentação Swagger ou serve dashboard"""
    return FileResponse("app/static/index.html")

@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    """Serve o dashboard interativo"""
    return FileResponse("app/static/index.html")

app.include_router(router)
