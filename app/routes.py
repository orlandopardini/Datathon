from __future__ import annotations

import json
import os
import subprocess
import warnings
from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.utils import read_json, ensure_dir
from src.drift import compute_drift
from src.feature_engineering import add_engineered_features

# Suprimir warnings de features ausentes (comportamento esperado)
warnings.filterwarnings('ignore', message='.*Skipping features without any observed values.*')
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


router = APIRouter()


def _path(env_name: str, default: str) -> Path:
    return Path(os.environ.get(env_name, default))


def get_paths() -> Dict[str, Path]:
    """
    Lê os caminhos a partir de variáveis de ambiente (útil para testes/CI),
    com defaults para execução local.
    """
    return {
        "MODEL_PATH": _path("MODEL_PATH", "app/model/model.joblib"),
        "FEATURES_PATH": _path("FEATURES_PATH", "app/model/feature_columns.json"),
        "BASELINE_PATH": _path("BASELINE_PATH", "app/model/baseline.json"),
        "METRICS_PATH": _path("METRICS_PATH", "app/model/metrics.json"),
        "LOG_PATH": _path("LOG_PATH", "app/logs/predictions.jsonl"),
    }


class PredictRequest(BaseModel):
    records: List[Dict[str, Any]] = Field(..., description="Lista de registros (dict por estudante).")


class PredictItem(BaseModel):
    at_risk_probability: float = Field(..., description="Probabilidade de risco de evasão (0-1)")
    at_risk_label: int = Field(..., description="Classe predita: 1 = em risco de evasão, 0 = sem risco")


class PredictResponse(BaseModel):
    predictions: List[PredictItem]


def _load_model(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}. Rode o treino antes.")
    return joblib.load(model_path)


def _load_feature_columns(features_path: Path) -> Dict[str, List[str]]:
    if not features_path.exists():
        raise FileNotFoundError(f"Arquivo de features não encontrado em {features_path}. Rode o treino antes.")
    return read_json(features_path)


def _align_features(df: pd.DataFrame, feature_spec: Dict[str, List[str]]) -> pd.DataFrame:
    """
    Garante que o DataFrame tenha exatamente as colunas esperadas.
    - Colunas faltantes são criadas como NaN.
    - Colunas extras são descartadas.
    - Colunas numéricas são coerced para float.
    - Colunas categóricas são coerced para object (strings), preservando NaN.
    """
    numeric = feature_spec.get("numeric", [])
    categorical = feature_spec.get("categorical", [])
    expected = numeric + categorical

    out = df.copy()

    for c in expected:
        if c not in out.columns:
            out[c] = np.nan

    out = out[expected]

    for c in numeric:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    for c in categorical:
        if c in out.columns:
            out[c] = out[c].apply(lambda x: np.nan if pd.isna(x) else str(x)).astype("object")

    return out


def _append_log(log_path: Path, payload: Dict[str, Any]) -> None:
    ensure_dir(log_path.parent)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/metrics")
def metrics():
    paths = get_paths()
    if paths["METRICS_PATH"].exists():
        return read_json(paths["METRICS_PATH"])
    return {"warning": "metrics.json não encontrado. Rode o treino."}


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    paths = get_paths()
    try:
        model = _load_model(paths["MODEL_PATH"])
        feature_spec = _load_feature_columns(paths["FEATURES_PATH"])
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = pd.DataFrame(req.records)
    
    # Adicionar features engineered (Tempo_programa, Idade_ingresso)
    df = add_engineered_features(df)
    
    X = _align_features(df, feature_spec)

    try:
        proba = model.predict_proba(X)[:, 1]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao prever: {e}")

    preds = [{"at_risk_probability": float(p), "at_risk_label": int(p >= 0.5)} for p in proba.tolist()]

    _append_log(
        paths["LOG_PATH"],
        {
            "ts": pd.Timestamp.utcnow().isoformat(),
            "n_records": int(len(req.records)),
            "predictions": preds,
            "features": req.records[:10],
        },
    )

    return {"predictions": preds}


@router.get("/drift")
def drift(max_rows: int = 2000):
    paths = get_paths()

    if not paths["BASELINE_PATH"].exists():
        raise HTTPException(status_code=400, detail="baseline.json não encontrado. Rode o treino.")
    if not paths["LOG_PATH"].exists():
        return {"warning": "Sem logs ainda (faça chamadas ao /predict).", "n_current": 0}

    baseline = read_json(paths["BASELINE_PATH"])

    rows = []
    with paths["LOG_PATH"].open("r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                feats = obj.get("features", [])
                for r in feats:
                    rows.append(r)
            except Exception:
                continue
            if len(rows) >= max_rows:
                break

    if not rows:
        return {"warning": "Logs não têm features suficientes.", "n_current": 0}

    cur = pd.DataFrame(rows)
    report = compute_drift(baseline, cur)
    return report.to_dict()


@router.get("/procedures/info")
def procedures_info():
    """Retorna informações sobre os procedimentos disponíveis"""
    return {
        "procedures": [
            {
                "id": "setup",
                "name": "Setup Inicial",
                "description": "Configura o ambiente pela primeira vez. Cria o ambiente virtual Python, instala todas as dependências necessárias (FastAPI, scikit-learn, pandas, etc.) e prepara o projeto para execução.",
                "file": "procedures/setup.bat",
                "icon": "⚙️",
                "steps": [
                    "Verifica instalação do Python",
                    "Remove ambiente virtual antigo (se existir)",
                    "Cria novo ambiente virtual (.venv)",
                    "Ativa o ambiente virtual",
                    "Instala todas as dependências"
                ]
            },
            {
                "id": "train",
                "name": "Treinar Modelo",
                "description": "Executa o pipeline completo de treinamento do modelo de ML. Carrega os dados do Excel, realiza feature engineering, treina o modelo de classificação e gera todos os artefatos necessários (model.joblib, metrics.json, baseline.json, feature_columns.json).",
                "file": "procedures/train.bat",
                "icon": "🤖",
                "steps": [
                    "Ativa ambiente virtual",
                    "Verifica arquivo de dados Excel",
                    "Carrega e preprocessa os dados",
                    "Realiza feature engineering",
                    "Treina modelo de classificação",
                    "Avalia métricas de performance",
                    "Salva artefatos em app/model/"
                ]
            },
            {
                "id": "test",
                "name": "Executar Testes",
                "description": "Executa a suíte completa de testes unitários com cobertura de código. Valida o preprocessing, feature engineering, API endpoints, drift detection e garante cobertura mínima de 80% do código.",
                "file": "procedures/test.bat",
                "icon": "✅",
                "steps": [
                    "Ativa ambiente virtual",
                    "Define PYTHONPATH",
                    "Executa pytest com cobertura",
                    "Testa preprocessing e features",
                    "Testa API endpoints",
                    "Testa drift detection",
                    "Gera relatório de cobertura"
                ]
            },
            {
                "id": "run",
                "name": "Iniciar Dashboard",
                "description": "Inicia apenas a API FastAPI com o dashboard web. Serve o dashboard interativo na porta 8000 com todas as visualizações, formulário de predição e métricas do modelo.",
                "file": "procedures/run.bat",
                "icon": "🚀",
                "steps": [
                    "Ativa ambiente virtual",
                    "Verifica se modelo existe",
                    "Inicia servidor FastAPI",
                    "Serve dashboard em localhost:8000",
                    "Disponibiliza API docs em /docs"
                ]
            },
            {
                "id": "monitor",
                "name": "Dashboard com Monitoramento",
                "description": "Inicia tanto a API FastAPI quanto o dashboard Streamlit de monitoramento de drift. Permite visualizar métricas em tempo real, PSI (Population Stability Index) e alertas de data drift em duas interfaces simultâneas.",
                "file": "procedures/run-with-monitoring.bat",
                "icon": "📊",
                "steps": [
                    "Ativa ambiente virtual",
                    "Verifica modelo treinado",
                    "Inicia FastAPI em background (porta 8000)",
                    "Aguarda API inicializar",
                    "Inicia Streamlit (porta 8501)",
                    "Monitora drift em tempo real"
                ]
            }
        ]
    }
