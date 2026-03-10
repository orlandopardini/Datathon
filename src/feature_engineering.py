from __future__ import annotations

import re
import pandas as pd
import numpy as np


def parse_fase_to_numeric(val) -> float:
    """
    Converte códigos de fase (ex.: '2A', 'ALFA', 9) para um número aproximado.
    Regras:
      - 'ALFA' -> 0
      - '1A'...'1Z' -> 1
      - '2A' -> 2, etc.
      - inteiro 9 (observado no dataset) é mantido como 9
    """
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return float(val)
    s = str(val).strip().upper()
    if s == "ALFA":
        return 0.0
    m = re.match(r"^(\d+)", s)
    if m:
        return float(m.group(1))
    return np.nan


_NUMERIC_LIKE = [
    "INDE 2024", "INDE 23", "INDE 22",
    "IAA", "IEG", "IPS", "IPP", "IDA", "Mat", "Por", "Ing",
    "IPV", "IAN",
    "Cg", "Cf", "Ct",
    "Nº Av", "Idade", "Ano ingresso",
    "Rec Av1", "Rec Av2", "Rec Psicologia",
    "Indicado", "Atingiu PV",
    "Destaque IEG", "Destaque IDA", "Destaque IPV",
]


def _to_clean_object_string(col: pd.Series) -> pd.Series:
    """Converte valores não-nulos para string, preservando NaN."""
    return col.apply(lambda x: np.nan if pd.isna(x) else str(x)).astype("object")


def add_engineered_features(df: pd.DataFrame, current_year: int = 2024) -> pd.DataFrame:
    """
    Adiciona features engenheiradas ao dataset.
    
    Features criadas:
    - Fase_num: Conversão de Fase para numérico (ALFA=0, 1A=1, 2B=2, etc)
    - Tempo_programa: Anos desde o ingresso no programa
    - Idade_ingresso: Idade quando entrou no programa
    """
    out = df.copy()

    # Coerce colunas numéricas que às vezes vêm como object
    for c in _NUMERIC_LIKE:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    # fase numérica (feature adicional)
    if "Fase" in out.columns:
        out["Fase_num"] = out["Fase"].apply(parse_fase_to_numeric)
    
    # Tempo no programa (anos desde ingresso)
    if "Ano ingresso" in out.columns:
        out["Tempo_programa"] = current_year - pd.to_numeric(out["Ano ingresso"], errors="coerce")
        # Garantir valores não negativos
        out["Tempo_programa"] = out["Tempo_programa"].clip(lower=0)
    
    # Idade quando ingressou no programa
    if "Idade" in out.columns and "Tempo_programa" in out.columns:
        out["Idade_ingresso"] = out["Idade"] - out["Tempo_programa"]
        # Garantir valores razoáveis (mínimo 5 anos, máximo 20 anos)
        out["Idade_ingresso"] = out["Idade_ingresso"].clip(lower=5, upper=20)

    # Garantir categoricals sem tipos mistos (int/str) e sem None,
    # pois isso quebra o SimpleImputer(strategy="most_frequent").
    for c in out.columns:
        if not pd.api.types.is_numeric_dtype(out[c]):
            out[c] = _to_clean_object_string(out[c])

    return out


def get_feature_target_columns(df: pd.DataFrame, target_name: str = "at_risk") -> tuple[list[str], list[str]]:
    """
    Retorna listas de colunas numéricas e categóricas (com base em dtype).
    """
    X = df.copy()
    if target_name in X.columns:
        X = X.drop(columns=[target_name])

    numeric_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
    categorical_cols = [c for c in X.columns if c not in numeric_cols]
    return numeric_cols, categorical_cols
