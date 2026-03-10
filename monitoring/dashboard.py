from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.utils import read_json
from src.drift import compute_drift

BASELINE_PATH = Path("app/model/baseline.json")
LOG_PATH = Path("app/logs/predictions.jsonl")

st.set_page_config(page_title="Drift Dashboard — Passos Mágicos", layout="wide")

st.title("📉 Drift Dashboard — Passos Mágicos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Baseline")
    if not BASELINE_PATH.exists():
        st.error("baseline.json não encontrado. Rode o treino primeiro.")
        st.stop()
    baseline = read_json(BASELINE_PATH)
    st.write(f"Registros baseline: {baseline.get('n_rows', 0)}")

with col2:
    st.markdown("### Logs de produção")
    if not LOG_PATH.exists():
        st.warning("Sem logs ainda. Faça chamadas ao endpoint /predict.")
        st.stop()

# carrega logs
rows = []
with LOG_PATH.open("r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            feats = obj.get("features", [])
            for r in feats:
                rows.append(r)
        except Exception:
            continue

if not rows:
    st.warning("Nenhuma feature encontrada nos logs.")
    st.stop()

current = pd.DataFrame(rows)
st.write(f"Registros atuais (amostrados): {current.shape[0]}")

report = compute_drift(baseline, current)

st.markdown("## PSI (numéricas)")
psi_df = pd.DataFrame(
    [{"feature": k, "psi": v} for k, v in report.numeric_psi.items()]
).sort_values("psi", ascending=False)
st.dataframe(psi_df, use_container_width=True)

st.markdown("## JS divergence (categóricas)")
js_df = pd.DataFrame(
    [{"feature": k, "js_divergence": v} for k, v in report.categorical_js.items()]
).sort_values("js_divergence", ascending=False)
st.dataframe(js_df, use_container_width=True)

st.info("Heurística comum: PSI > 0.2 (alerta), PSI > 0.3 (severo).")
