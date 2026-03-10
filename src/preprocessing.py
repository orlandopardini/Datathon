from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional, List

import pandas as pd
import numpy as np


DROP_COLS_DEFAULT = [
    # Identificadores / texto livre
    "RA",
    "Nome",
    "Nome Anonimizado",
    # Alvo antigo e colunas que vazam alvo
    "Defasagem",
    "Fase Ideal",
    # Duplicadas / administrativas (podem vazar status)
    "Ativo/ Inativo",
    "Ativo/ Inativo.1",
]

# Coluna usada para CONSTRUIR o target de evasão (não deve ser feature)
TARGET_ENGAJAMENTO_COL = "IEG"


def load_pede_excel(path: str, sheet: str) -> pd.DataFrame:
    """Carrega uma aba do Excel PEDE."""
    return pd.read_excel(path, sheet_name=sheet)


def build_target_at_risk_evasao(df: pd.DataFrame, threshold: float = 5.0) -> pd.Series:
    """
    Define alvo binário para RISCO DE EVASÃO ESCOLAR.
    
    Target = 1 (alto risco) se:
    - IEG (Indicador de Engajamento) < threshold (default: 5.0)
    
    Interpretação:
    - Alunos com baixo engajamento têm alto risco de abandonar o programa
    - IEG mede presença, participação e envolvimento nas atividades
    - Threshold de 5.0 identifica ~14% dos alunos (proporção realista)
    
    Args:
        df: DataFrame com dados PEDE
        threshold: Valor mínimo de IEG considerado seguro (default: 5.0)
    
    Returns:
        Series binária: 1 = risco de evasão, 0 = sem risco
    
    Exemplos:
        - Aluno com IEG=8.5 → at_risk=0 (engajado, sem risco)
        - Aluno com IEG=3.0 → at_risk=1 (desengajado, alto risco)
        - Aluno com IEG=5.0 → at_risk=0 (no limite, considerado seguro)
    """
    if 'IEG' not in df.columns:
        raise KeyError("Coluna 'IEG' não encontrada. Necessária para definir risco de evasão.")
    
    # Converter para numérico
    ieg = pd.to_numeric(df['IEG'], errors='coerce')
    
    # Definir risco: IEG < threshold
    at_risk = (ieg < threshold).astype(int)
    
    return at_risk


# ==================== FUNÇÕES DEPRECIADAS (MODELOS ANTIGOS) ====================

def build_target_at_risk_academic(df: pd.DataFrame, threshold: float = 6.0) -> pd.Series:
    """
    DEPRECADO: Modelo antigo de risco acadêmico (notas baixas).
    Use build_target_at_risk_evasao() para modelo de evasão escolar.
    
    Define alvo binário baseado em DESEMPENHO ACADÊMICO:
    at_risk = 1 se média(IEG, IDA, Mat, Por) < threshold
    """
    notas_cols = ["IEG", "IDA", "Mat", "Por"]
    missing_cols = [c for c in notas_cols if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Colunas de notas não encontradas: {missing_cols}")
    df_notas = df[notas_cols].apply(pd.to_numeric, errors="coerce")
    media_notas = df_notas.mean(axis=1)
    at_risk = (media_notas < threshold).astype(int)
    return at_risk


def build_target_at_risk(df: pd.DataFrame, defasagem_col: str = "Defasagem") -> pd.Series:
    """
    DEPRECADO: Função antiga baseada em Defasagem cronológica.
    Use build_target_at_risk_evasao() para novo modelo de evasão escolar.
    
    Define alvo binário: 1 se Defasagem > 0 (em atraso/risco), 0 caso contrário.
    """
    if defasagem_col not in df.columns:
        raise KeyError(f"Coluna alvo '{defasagem_col}' não encontrada.")
    return (pd.to_numeric(df[defasagem_col], errors="coerce") > 0).astype(int)


def coerce_numeric_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def drop_leaky_and_id_cols(df: pd.DataFrame, extra_drop: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove colunas que não devem ser usadas como features.
    
    Inclui:
    - Identificadores (RA, Nome)
    - Colunas que vazam o target (Defasagem, Fase Ideal)
    - Status administrativo (Ativo/Inativo)
    - IEG (usado para construir o target de evasão)
    """
    drop_cols = set(DROP_COLS_DEFAULT)
    # IEG é usado para construir target de evasão, não pode ser feature
    drop_cols.add(TARGET_ENGAJAMENTO_COL)
    if extra_drop:
        drop_cols |= set(extra_drop)
    return df.drop(columns=[c for c in drop_cols if c in df.columns])


@dataclass(frozen=True)
class SplitData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def train_test_split_stratified(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> SplitData:
    from sklearn.model_selection import train_test_split

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return SplitData(X_tr, X_te, y_tr, y_te)
