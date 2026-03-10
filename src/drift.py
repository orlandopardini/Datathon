from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List

import numpy as np
import pandas as pd


def _safe_float(x: float) -> float | None:
    try:
        if x is None:
            return None
        x = float(x)
        if np.isnan(x) or np.isinf(x):
            return None
        return x
    except Exception:
        return None


def _psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10, eps: float = 1e-6) -> float:
    """
    Population Stability Index (PSI) para variáveis numéricas.
    PSI ~ 0 => estável; >0.2 alerta, >0.3 severo (heurísticas comuns).
    """
    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]
    if expected.size < 50 or actual.size < 50:
        return float("nan")

    quantiles = np.linspace(0, 1, buckets + 1)
    cuts = np.unique(np.quantile(expected, quantiles))
    if cuts.size <= 2:
        return float("nan")

    exp_counts, _ = np.histogram(expected, bins=cuts)
    act_counts, _ = np.histogram(actual, bins=cuts)
    exp_perc = exp_counts / max(exp_counts.sum(), 1)
    act_perc = act_counts / max(act_counts.sum(), 1)

    exp_perc = np.clip(exp_perc, eps, 1)
    act_perc = np.clip(act_perc, eps, 1)

    return float(np.sum((act_perc - exp_perc) * np.log(act_perc / exp_perc)))


def _js_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-9) -> float:
    p = p.astype(float)
    q = q.astype(float)
    p = p / max(p.sum(), 1)
    q = q / max(q.sum(), 1)
    p = np.clip(p, eps, 1)
    q = np.clip(q, eps, 1)
    m = 0.5 * (p + q)
    return float(0.5 * (np.sum(p * np.log(p / m)) + np.sum(q * np.log(q / m))))


@dataclass
class DriftReport:
    numeric_psi: Dict[str, float]
    categorical_js: Dict[str, float]
    n_baseline: int
    n_current: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_baseline": int(self.n_baseline),
            "n_current": int(self.n_current),
            "numeric_psi": {k: _safe_float(v) for k, v in self.numeric_psi.items()},
            "categorical_js": {k: _safe_float(v) for k, v in self.categorical_js.items()},
        }


def build_baseline(df: pd.DataFrame, numeric_cols: List[str], categorical_cols: List[str]) -> Dict[str, Any]:
    baseline = {
        "n_rows": int(df.shape[0]),
        "numeric": {},
        "categorical": {},
    }
    for c in numeric_cols:
        arr = pd.to_numeric(df[c], errors="coerce").to_numpy(dtype=float)
        baseline["numeric"][c] = {
            "mean": _safe_float(np.nanmean(arr)) if np.isfinite(arr).any() else None,
            "std": _safe_float(np.nanstd(arr)) if np.isfinite(arr).any() else None,
            "values": arr[np.isfinite(arr)].tolist()[:5000],  # amostra p/ PSI
        }
    for c in categorical_cols:
        vc = df[c].astype("object").where(pd.notna(df[c]), "<NA>").value_counts()
        baseline["categorical"][c] = {
            "counts": vc.to_dict(),
        }
    return baseline


def compute_drift(baseline: Dict[str, Any], current: pd.DataFrame) -> DriftReport:
    n_base = int(baseline.get("n_rows", 0))
    n_cur = int(current.shape[0])

    numeric_psi = {}
    for c, meta in baseline.get("numeric", {}).items():
        expected = np.array(meta.get("values", []), dtype=float)
        cur_series = current.get(c, pd.Series(dtype=float))
        actual = pd.to_numeric(cur_series, errors="coerce").to_numpy(dtype=float)
        numeric_psi[c] = _psi(expected, actual)

    categorical_js = {}
    for c, meta in baseline.get("categorical", {}).items():
        base_counts = meta.get("counts", {})
        base_keys = set(base_counts.keys())
        cur_series = current.get(c, pd.Series(dtype="object"))
        cur_vc = cur_series.astype("object").where(pd.notna(cur_series), "<NA>").value_counts().to_dict()

        keys = sorted(base_keys | set(cur_vc.keys()))
        p = np.array([base_counts.get(k, 0.0) for k in keys], dtype=float)
        q = np.array([cur_vc.get(k, 0.0) for k in keys], dtype=float)
        categorical_js[c] = _js_divergence(p, q)

    return DriftReport(numeric_psi=numeric_psi, categorical_js=categorical_js, n_baseline=n_base, n_current=n_cur)
