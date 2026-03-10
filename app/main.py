from __future__ import annotations

import warnings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router

# Suprimir warnings do sklearn durante predições
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

app = FastAPI(
    title="Passos Mágicos — Risco de Evasão Escolar",
    version="3.0.0",
    description="Prediz risco de EVASÃO ESCOLAR via engajamento baixo (IEG < 5.0)"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root route to serve the dashboard
@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

app.include_router(router)
