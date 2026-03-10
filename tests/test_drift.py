"""
Testes para o módulo de detecção de drift
"""
import pytest
import numpy as np
import pandas as pd
from src.drift import (
    _safe_float,
    _psi,
    _js_divergence,
    build_baseline,
    compute_drift,
    DriftReport
)


def test_safe_float_valid():
    """Testa conversão de valores válidos"""
    assert _safe_float(3.14) == 3.14
    assert _safe_float(0.0) == 0.0
    assert _safe_float(-5.2) == -5.2


def test_safe_float_none():
    """Testa que None retorna None"""
    assert _safe_float(None) is None


def test_safe_float_nan():
    """Testa que NaN retorna None"""
    assert _safe_float(float('nan')) is None


def test_safe_float_inf():
    """Testa que infinito retorna None"""
    assert _safe_float(float('inf')) is None
    assert _safe_float(float('-inf')) is None


def test_psi_identical_distributions():
    """Testa PSI com distribuições idênticas (deve ser ~0)"""
    expected = np.random.normal(0, 1, 100)
    actual = expected.copy()
    
    psi = _psi(expected, actual)
    
    assert psi < 0.01  # Deve ser muito próximo de 0


def test_psi_different_distributions():
    """Testa PSI com distribuições diferentes"""
    expected = np.random.normal(0, 1, 100)
    actual = np.random.normal(5, 1, 100)  # Média diferente
    
    psi = _psi(expected, actual)
    
    assert psi > 0.1  # Deve indicar mudança


def test_psi_with_nan():
    """Testa PSI ignorando valores NaN"""
    expected = np.array([1, 2, 3, 4, 5, np.nan, 6, 7, 8])
    actual = np.array([1, 2, np.nan, 4, 5, 6, 7, 8, 9])
    
    psi = _psi(expected, actual)
    
    # Deve calcular sem erros, ignorando NaN
    assert isinstance(psi, float)


def test_psi_insufficient_data():
    """Testa PSI com dados insuficientes (< 50)"""
    expected = np.array([1, 2, 3])
    actual = np.array([1, 2, 3])
    
    psi = _psi(expected, actual)
    
    # Deve retornar NaN
    assert np.isnan(psi)


def test_psi_custom_buckets():
    """Testa PSI com número customizado de buckets"""
    expected = np.random.normal(0, 1, 200)
    actual = expected.copy()
    
    psi_5 = _psi(expected, actual, buckets=5)
    psi_20 = _psi(expected, actual, buckets=20)
    
    # Ambos devem ser próximos de 0
    assert psi_5 < 0.05
    assert psi_20 < 0.05


def test_js_divergence_identical():
    """Testa JS divergence com distribuições idênticas"""
    p = np.array([10, 20, 30, 40])
    q = np.array([10, 20, 30, 40])
    
    js = _js_divergence(p, q)
    
    assert js < 0.01  # Deve ser ~0


def test_js_divergence_different():
    """Testa JS divergence com distribuições diferentes"""
    p = np.array([100, 0, 0, 0])
    q = np.array([0, 0, 0, 100])
    
    js = _js_divergence(p, q)
    
    assert js > 0.5  # Deve indicar grande diferença


def test_js_divergence_symmetric():
    """Testa que JS divergence é simétrica"""
    p = np.array([10, 20, 30])
    q = np.array([30, 20, 10])
    
    js_pq = _js_divergence(p, q)
    js_qp = _js_divergence(q, p)
    
    # Deve ser simétrico
    assert abs(js_pq - js_qp) < 0.001


def test_build_baseline_numeric():
    """Testa criação de baseline com colunas numéricas"""
    df = pd.DataFrame({
        "Idade": [10, 12, 14, 16, 18],
        "IAA": [5.0, 6.0, 7.0, 8.0, 9.0]
    })
    
    baseline = build_baseline(df, ["Idade", "IAA"], [])
    
    assert "numeric" in baseline
    assert "Idade" in baseline["numeric"]
    assert "IAA" in baseline["numeric"]
    
    # Verificar estatísticas
    assert baseline["numeric"]["Idade"]["mean"] == 14.0
    assert "std" in baseline["numeric"]["Idade"]
    assert "values" in baseline["numeric"]["Idade"]


def test_build_baseline_categorical():
    """Testa criação de baseline com colunas categóricas"""
    df = pd.DataFrame({
        "Gênero": ["M", "F", "M", "F", "M"],
        "Fase": ["1A", "2A", "1A", "2A", "3A"]
    })
    
    baseline = build_baseline(df, [], ["Gênero", "Fase"])
    
    assert "categorical" in baseline
    assert "Gênero" in baseline["categorical"]
    assert "Fase" in baseline["categorical"]
    
    # Verificar contagens
    assert baseline["categorical"]["Gênero"]["counts"]["M"] == 3
    assert baseline["categorical"]["Gênero"]["counts"]["F"] == 2


def test_build_baseline_mixed():
    """Testa baseline com colunas numéricas e categóricas"""
    df = pd.DataFrame({
        "Idade": [10, 12, 14],
        "Gênero": ["M", "F", "M"]
    })
    
    baseline = build_baseline(df, ["Idade"], ["Gênero"])
    
    assert "numeric" in baseline
    assert "categorical" in baseline
    assert baseline["n_rows"] == 3


def test_build_baseline_with_nan():
    """Testa baseline com valores ausentes"""
    df = pd.DataFrame({
        "Num": [1.0, np.nan, 3.0, 4.0],
        "Cat": ["A", None, "B", "A"]
    })
    
    baseline = build_baseline(df, ["Num"], ["Cat"])
    
    # Deve lidar com NaN
    assert "Num" in baseline["numeric"]
    assert "Cat" in baseline["categorical"]
    
    # Valores ausentes são substituídos por "<NA>"
    assert "<NA>" in baseline["categorical"]["Cat"]["counts"]


def test_build_baseline_large_sample():
    """Testa que baseline limita amostras a 5000"""
    df = pd.DataFrame({
        "Feature": np.random.randn(10000)
    })
    
    baseline = build_baseline(df, ["Feature"], [])
    
    # Deve ter no máximo 5000 valores
    assert len(baseline["numeric"]["Feature"]["values"]) <= 5000


def test_compute_drift_no_drift():
    """Testa detecção de drift quando não há drift"""
    df_base = pd.DataFrame({
        "Num": np.random.normal(0, 1, 200),
        "Cat": ["A"] * 100 + ["B"] * 100
    })
    
    df_current = pd.DataFrame({
        "Num": np.random.normal(0, 1, 200),
        "Cat": ["A"] * 100 + ["B"] * 100
    })
    
    baseline = build_baseline(df_base, ["Num"], ["Cat"])
    report = compute_drift(baseline, df_current)
    
    assert isinstance(report, DriftReport)
    assert report.n_baseline == 200
    assert report.n_current == 200
    
    # PSI e JS devem ser baixos
    assert report.numeric_psi["Num"] < 0.2
    assert report.categorical_js["Cat"] < 0.1


def test_compute_drift_with_drift():
    """Testa detecção de drift quando há drift"""
    df_base = pd.DataFrame({
        "Num": np.random.normal(0, 1, 200),
        "Cat": ["A"] * 180 + ["B"] * 20
    })
    
    df_current = pd.DataFrame({
        "Num": np.random.normal(5, 1, 200),  # Média mudou
        "Cat": ["A"] * 20 + ["B"] * 180  # Distribuição mudou
    })
    
    baseline = build_baseline(df_base, ["Num"], ["Cat"])
    report = compute_drift(baseline, df_current)
    
    # PSI e JS devem ser altos
    assert report.numeric_psi["Num"] > 0.2
    assert report.categorical_js["Cat"] > 0.1


def test_drift_report_to_dict():
    """Testa conversão de DriftReport para dict"""
    report = DriftReport(
        numeric_psi={"A": 0.1, "B": 0.2},
        categorical_js={"X": 0.05},
        n_baseline=100,
        n_current=150
    )
    
    d = report.to_dict()
    
    assert d["n_baseline"] == 100
    assert d["n_current"] == 150
    assert d["numeric_psi"]["A"] == 0.1
    assert d["categorical_js"]["X"] == 0.05


def test_drift_report_to_dict_with_nan():
    """Testa que to_dict converte NaN para None"""
    report = DriftReport(
        numeric_psi={"A": float('nan')},
        categorical_js={"X": float('inf')},
        n_baseline=100,
        n_current=100
    )
    
    d = report.to_dict()
    
    assert d["numeric_psi"]["A"] is None
    assert d["categorical_js"]["X"] is None


def test_compute_drift_missing_columns():
    """Testa drift quando colunas estão ausentes"""
    df_base = pd.DataFrame({
        "Num": [1, 2, 3],
        "Cat": ["A", "B", "A"]
    })
    
    df_current = pd.DataFrame({
        "Num": [1, 2, 3]
        # "Cat" está ausente
    })
    
    baseline = build_baseline(df_base, ["Num"], ["Cat"])
    report = compute_drift(baseline, df_current)
    
    # Deve calcular drift mesmo com coluna ausente
    assert "Num" in report.numeric_psi
    assert "Cat" in report.categorical_js


def test_compute_drift_new_categories():
    """Testa drift quando aparecem novas categorias"""
    df_base = pd.DataFrame({
        "Cat": ["A", "B", "A", "B"]
    })
    
    df_current = pd.DataFrame({
        "Cat": ["A", "B", "C", "D"]  # Novas categorias C e D
    })
    
    baseline = build_baseline(df_base, [], ["Cat"])
    report = compute_drift(baseline, df_current)
    
    # Deve calcular JS sem erros
    assert "Cat" in report.categorical_js
    assert isinstance(report.categorical_js["Cat"], float)


def test_psi_edge_case_uniform():
    """Testa PSI com distribuições uniformes"""
    expected = np.ones(100) * 5.0  # Todos os valores iguais
    actual = np.ones(100) * 5.0
    
    psi = _psi(expected, actual)
    
    # Com valores iguais, pode retornar NaN (cuts <= 2)
    assert np.isnan(psi)


def test_js_divergence_zeros():
    """Testa JS com contagens zero"""
    p = np.array([1, 0, 0, 1])
    q = np.array([0, 1, 1, 0])
    
    js = _js_divergence(p, q)
    
    # Deve calcular sem erros (usando eps)
    assert isinstance(js, float)
    assert not np.isnan(js)
    assert not np.isinf(js)


def test_build_baseline_empty_dataframe():
    """Testa baseline com DataFrame vazio"""
    df = pd.DataFrame({"A": []})
    
    baseline = build_baseline(df, ["A"], [])
    
    assert baseline["n_rows"] == 0
    assert "A" in baseline["numeric"]


def test_safe_float_exception_handling():
    """Testa que _safe_float lida com erros"""
    # Objetos que não podem ser convertidos
    result = _safe_float("not a number")
    assert result is None
    
    result = _safe_float([1, 2, 3])
    assert result is None


def test_psi_with_empty_arrays():
    """Testa PSI com arrays vazios"""
    expected = np.array([])
    actual = np.array([])
    
    psi = _psi(expected, actual)
    
    assert np.isnan(psi)


def test_drift_report_all_nan():
    """Testa DriftReport com todos valores NaN"""
    report = DriftReport(
        numeric_psi={},
        categorical_js={},
        n_baseline=0,
        n_current=0
    )
    
    d = report.to_dict()
    
    assert d["n_baseline"] == 0
    assert d["n_current"] == 0
    assert d["numeric_psi"] == {}
    assert d["categorical_js"] == {}
