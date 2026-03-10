import pandas as pd
import numpy as np
import pytest

from src.preprocessing import (
    build_target_at_risk_evasao,  # NOVO target de evasão
    build_target_at_risk_academic,  # ANTIGO target acadêmico (deprecado)
    build_target_at_risk,  # ANTIGO target defasagem (deprecado)
    drop_leaky_and_id_cols,
    TARGET_ENGAJAMENTO_COL
)


def test_build_target_at_risk_evasao_basic():
    """
    Testa a construção do target de EVASÃO ESCOLAR.
    
    Lógica: at_risk = 1 quando IEG < threshold
            at_risk = 0 quando IEG >= threshold
    
    Threshold padrão: 5.0
    
    Exemplos:
    - IEG=8.5 → NÃO em risco (0)
    - IEG=5.0 → NÃO em risco (0) [igual ao threshold]
    - IEG=3.0 → EM risco de evasão (1)
    """
    df = pd.DataFrame({
        "IEG": [10.0, 8.5, 5.0, 4.5, 3.0, 0.0]
    })
    y = build_target_at_risk_evasao(df, threshold=5.0)
    # Apenas índices 3, 4, 5 (IEG < 5.0) estão em risco
    assert y.tolist() == [0, 0, 0, 1, 1, 1]


def test_build_target_at_risk_evasao_com_nulls():
    """
    Testa comportamento com NaN (deve tratar como ausente).
    """
    df = pd.DataFrame({
        "IEG": [8.0, None, 3.0, 6.0]  # None deve retornar 0 (considerado sem risco por padrão)
    })
    y = build_target_at_risk_evasao(df, threshold=5.0)
    # None é coerced para NaN, que < 5.0 retorna False
    # Então temos: [0, 0, 1, 0]
    expected = [0, 0, 1, 0]
    assert y.tolist() == expected


def test_build_target_at_risk_evasao_custom_threshold():
    """
    Testa com threshold customizado.
    """
    df = pd.DataFrame({
        "IEG": [7.0, 6.0, 4.0]
    })
    
    # Threshold 5.0: apenas último em risco
    y1 = build_target_at_risk_evasao(df, threshold=5.0)
    assert y1.tolist() == [0, 0, 1]
    
    # Threshold 6.5: dois últimos em risco
    y2 = build_target_at_risk_evasao(df, threshold=6.5)
    assert y2.tolist() == [0, 1, 1]
    
    # Threshold 3.0: nenhum em risco
    y3 = build_target_at_risk_evasao(df, threshold=3.0)
    assert y3.tolist() == [0, 0, 0]


def test_build_target_at_risk_evasao_missing_column():
    """
    Testa se levanta erro quando falta coluna IEG.
    """
    df = pd.DataFrame({"IDA": [8.0], "Mat": [8.0]})  # Falta IEG
    
    with pytest.raises(KeyError, match="IEG"):
        build_target_at_risk_evasao(df)


def test_target_engajamento_col_constant():
    """
    Valida que a constante TARGET_ENGAJAMENTO_COL está corretamente definida.
    """
    assert TARGET_ENGAJAMENTO_COL == "IEG"


def test_build_target_at_risk_evasao_boundary_values():
    """
    Testa valores de fronteira (exatamente no threshold).
    """
    df = pd.DataFrame({
        "IEG": [5.0, 5.00001, 4.99999]
    })
    y = build_target_at_risk_evasao(df, threshold=5.0)
    # 5.0 e 5.00001 não são < 5.0, então = 0
    # 4.99999 é < 5.0, então = 1
    assert y.tolist() == [0, 0, 1]


# ========== TESTES ANTIGOS (DEPRECADOS) ==========
# Mantidos para compatibilidade com código legado

def test_build_target_at_risk_academic_basic_deprecated():
    """
    DEPRECADO: Testa target acadêmico antigo.
    Use build_target_at_risk_evasao() para novo modelo de evasão.
    """
    df = pd.DataFrame({
        "IEG": [9.0, 5.0],
        "IDA": [9.0, 5.0],
        "Mat": [9.0, 5.0],
        "Por": [9.0, 5.0]
    })
    y = build_target_at_risk_academic(df, threshold=6.0)
    assert y.tolist() == [0, 1]


def test_build_target_at_risk_basic_deprecated():
    """
    DEPRECADO: Testa a construção do target at_risk ANTIGO (baseado em Defasagem).
    Use build_target_at_risk_evasao() para novo modelo.
    """
    df = pd.DataFrame({"Defasagem": [-1, 0, 2, -3]})
    y = build_target_at_risk(df)
    assert y.tolist() == [0, 0, 1, 0]  # Apenas índice 2 (Defasagem=2) está em risco


def test_drop_leaky_cols():
    df = pd.DataFrame({"RA":[1], "Defasagem":[-1], "Fase Ideal":["X"], "X":[10]})
    out = drop_leaky_and_id_cols(df)
    assert "RA" not in out.columns
    assert "Defasagem" not in out.columns
    assert "Fase Ideal" not in out.columns
    assert "X" in out.columns


# ========== TESTES ADICIONAIS ==========

def test_coerce_numeric_columns():
    """Testa conversão de colunas para numérico"""
    from src.preprocessing import coerce_numeric_columns
    
    df = pd.DataFrame({
        "A": ["1", "2", "3"],
        "B": ["4.5", "5.5", "6.5"],
        "C": ["x", "y", "z"]
    })
    
    result = coerce_numeric_columns(df, ["A", "B"])
    
    assert pd.api.types.is_numeric_dtype(result["A"])
    assert pd.api.types.is_numeric_dtype(result["B"])
    assert result["C"].dtype == object


def test_coerce_numeric_columns_with_invalid():
    """Testa conversão com valores inválidos"""
    from src.preprocessing import coerce_numeric_columns
    
    df = pd.DataFrame({
        "Num": ["1", "2", "invalid", "4"]
    })
    
    result = coerce_numeric_columns(df, ["Num"])
    
    assert pd.isna(result["Num"].iloc[2])


def test_drop_leaky_with_extra():
    """Testa remoção com colunas extras"""
    df = pd.DataFrame({
        "RA": [1],
        "Custom": ["test"],
        "Keep": ["data"]
    })
    
    result = drop_leaky_and_id_cols(df, extra_drop=["Custom"])
    
    assert "RA" not in result.columns
    assert "Custom" not in result.columns
    assert "Keep" in result.columns


def test_train_test_split_stratified():
    """Testa divisão estratificada"""
    from src.preprocessing import train_test_split_stratified
    
    X = pd.DataFrame({
        "A": range(100),
        "B": range(100, 200)
    })
    y = pd.Series([0] * 50 + [1] * 50)
    
    split = train_test_split_stratified(X, y, test_size=0.2, random_state=42)
    
    assert len(split.X_train) == 80
    assert len(split.X_test) == 20
    
    # Verificar estratificação
    train_ratio = split.y_train.mean()
    test_ratio = split.y_test.mean()
    assert abs(train_ratio - 0.5) < 0.1
    assert abs(test_ratio - 0.5) < 0.1


def test_load_pede_excel():
    """Testa carregamento do Excel (se arquivo existir)"""
    from src.preprocessing import load_pede_excel
    from pathlib import Path
    
    # Testar que a função existe e pode ser chamada
    assert callable(load_pede_excel)
    
    # Não vamos testar com arquivo real pois pode não existir no CI


def test_build_target_edge_case_all_nan():
    """Testa target quando todas as notas são NaN"""
    df = pd.DataFrame({
        "IEG": [np.nan, np.nan],
        "IDA": [np.nan, np.nan],
        "Mat": [np.nan, np.nan],
        "Por": [np.nan, np.nan]
    })
    
    y = build_target_at_risk_academic(df, threshold=6.0)
    
    # Com todas as notas NaN, média é NaN, resultado não é < threshold
    # In Pandas, NaN < 6.0 is False
    assert all(y == 0)


def test_build_target_at_risk_custom_column():
    """Testa função antiga com coluna customizada"""
    df = pd.DataFrame({
        "CustomDefasagem": [0, 1, 2]
    })
    
    y = build_target_at_risk(df, defasagem_col="CustomDefasagem")
    
    assert y.iloc[0] == 0
    assert y.iloc[1] == 1
    assert y.iloc[2] == 1
