"""
Testes para o módulo de feature engineering
"""
import pytest
import pandas as pd
import numpy as np
from src.feature_engineering import (
    add_engineered_features,
    parse_fase_to_numeric
)


def test_parse_fase_to_numeric_alfa():
    """Testa conversão de ALFA para 0"""
    assert parse_fase_to_numeric("ALFA") == 0.0
    assert parse_fase_to_numeric("alfa") == 0.0


def test_parse_fase_to_numeric_with_letter():
    """Testa conversão de fases com letra (1A, 2B, etc)"""
    assert parse_fase_to_numeric("1A") == 1.0
    assert parse_fase_to_numeric("2B") == 2.0
    assert parse_fase_to_numeric("3C") == 3.0
    assert parse_fase_to_numeric("9") == 9.0


def test_parse_fase_to_numeric_integer():
    """Testa conversão quando já é inteiro"""
    assert parse_fase_to_numeric(5) == 5.0
    assert parse_fase_to_numeric(9) == 9.0


def test_parse_fase_to_numeric_nan():
    """Testa conversão com valor NaN"""
    result = parse_fase_to_numeric(np.nan)
    assert pd.isna(result)


def test_parse_fase_to_numeric_invalid():
    """Testa conversão com valor inválido"""
    result = parse_fase_to_numeric("INVALID")
    assert pd.isna(result)


def test_add_engineered_features_tempo_programa():
    """Testa criação de feature Tempo_programa"""
    df = pd.DataFrame({
        "Ano ingresso": [2020, 2021, 2019],
        "Fase": ["1A", "2A", "3A"]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    assert "Tempo_programa" in result.columns
    assert result["Tempo_programa"].iloc[0] == 4  # 2024 - 2020
    assert result["Tempo_programa"].iloc[1] == 3  # 2024 - 2021
    assert result["Tempo_programa"].iloc[2] == 5  # 2024 - 2019


def test_add_engineered_features_idade_ingresso():
    """Testa criação de feature Idade_ingresso"""
    df = pd.DataFrame({
        "Ano ingresso": [2020, 2021],
        "Idade": [12, 13],
        "Fase": ["1A", "2A"]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    assert "Idade_ingresso" in result.columns
    assert result["Idade_ingresso"].iloc[0] == 8  # 12 - 4
    assert result["Idade_ingresso"].iloc[1] == 10  # 13 - 3


def test_add_engineered_features_fase_num():
    """Testa criação de feature Fase_num"""
    df = pd.DataFrame({
        "Fase": ["ALFA", "1A", "2B", "9"],
        "Ano ingresso": [2023, 2022, 2021, 2020]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    assert "Fase_num" in result.columns
    assert result["Fase_num"].iloc[0] == 0.0  # ALFA
    assert result["Fase_num"].iloc[1] == 1.0  # 1A
    assert result["Fase_num"].iloc[2] == 2.0  # 2B
    assert result["Fase_num"].iloc[3] == 9.0  # 9


def test_add_engineered_features_clip_tempo_programa():
    """Testa que Tempo_programa não pode ser negativo"""
    df = pd.DataFrame({
        "Ano ingresso": [2025],  # Futuro
        "Fase": ["1A"]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Deve ser clippado para 0
    assert result["Tempo_programa"].iloc[0] >= 0


def test_add_engineered_features_clip_idade_ingresso():
    """Testa que Idade_ingresso é clippado entre 5 e 20"""
    df = pd.DataFrame({
        "Ano ingresso": [2023, 2020],
        "Idade": [6, 25],
        "Fase": ["1A", "5A"]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Idade_ingresso deve estar entre 5 e 20
    assert all(result["Idade_ingresso"] >= 5)
    assert all(result["Idade_ingresso"] <= 20)


def test_add_engineered_features_numeric_conversion():
    """Testa conversão de colunas numéricas"""
    df = pd.DataFrame({
        "Fase": ["1A"],
        "Ano ingresso": ["2020"],  # String
        "Idade": ["12"],  # String
        "IAA": ["7.5"],  # String
        "INDE 2024": ["8.0"]  # String
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Deve converter para numérico
    assert pd.api.types.is_numeric_dtype(result["Ano ingresso"])
    assert pd.api.types.is_numeric_dtype(result["Idade"])
    assert pd.api.types.is_numeric_dtype(result["IAA"])
    assert pd.api.types.is_numeric_dtype(result["INDE 2024"])


def test_add_engineered_features_preserves_original():
    """Testa que colunas originais são preservadas"""
    df = pd.DataFrame({
        "Fase": ["1A", "2A"],
        "Turma": ["1A", "2A"],
        "Ano ingresso": [2020, 2021],
        "Idade": [12, 13],
        "Gênero": ["M", "F"]
    })
    
    original_cols = set(df.columns)
    result = add_engineered_features(df, current_year=2024)
    
    # Todas as colunas originais devem estar presentes
    assert original_cols.issubset(set(result.columns))


def test_add_engineered_features_with_nan():
    """Testa comportamento com valores NaN"""
    df = pd.DataFrame({
        "Fase": ["1A", np.nan],
        "Ano ingresso": [2020, np.nan],
        "Idade": [12, np.nan]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Deve ter as features engineered
    assert "Tempo_programa" in result.columns
    assert "Fase_num" in result.columns
    
    # Primeiro registro válido
    assert result["Tempo_programa"].iloc[0] == 4
    assert result["Fase_num"].iloc[0] == 1.0
    
    # Segundo registro com NaN
    assert pd.isna(result["Fase_num"].iloc[1])


def test_add_engineered_features_categorical_conversion():
    """Testa conversão de colunas categóricas para string"""
    df = pd.DataFrame({
        "Fase": ["1A", "2A"],
        "Turma": ["1A", "2A"],  # String
        "Gênero": ["M", "F"],
        "Ano ingresso": [2020, 2021]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Turma deve permanecer string
    assert result["Turma"].dtype == object
    assert result["Turma"].iloc[0] == "1A"
    assert result["Turma"].iloc[1] == "2A"


def test_get_feature_target_columns():
    """Testa obtenção de colunas de features e target"""
    from src.feature_engineering import get_feature_target_columns
    
    df = pd.DataFrame({
        "Fase": ["1A"],
        "Ano ingresso": [2020],
        "Idade": [12],
        "IAA": [7.5],
        "INDE 2024": [8.0],
        "at_risk": [0]  # Coluna target
    })
    
    df = add_engineered_features(df, current_year=2024)
    numeric_cols, categorical_cols = get_feature_target_columns(df, target_name="at_risk")
    
    # Colunas devem existir
    assert len(numeric_cols) > 0
    assert "Idade" in numeric_cols
    
    # Target não deve estar nas features
    assert "at_risk" not in numeric_cols and "at_risk" not in categorical_cols
    
    # Features engineeradas devem estar presentes
    assert "Tempo_programa" in numeric_cols
    assert "Fase_num" in numeric_cols


def test_engineered_features_all_columns_present():
    """Testa que todas as colunas engineeradas são criadas"""
    df = pd.DataFrame({
        "Fase": ["1A", "2A"],
        "Ano ingresso": [2020, 2021],
        "Idade": [12, 14]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Verificar que as 3 features engineeradas existem
    assert "Tempo_programa" in result.columns
    assert "Idade_ingresso" in result.columns
    assert "Fase_num" in result.columns


def test_engineered_features_without_fase():
    """Testa quando coluna Fase não existe"""
    df = pd.DataFrame({
        "Ano ingresso": [2020],
        "Idade": [12]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Fase_num não deve ser criada
    assert "Fase_num" not in result.columns
    # Mas outras features devem existir
    assert "Tempo_programa" in result.columns


def test_engineered_features_without_idade():
    """Testa quando coluna Idade não existe"""
    df = pd.DataFrame({
        "Fase": ["1A"],
        "Ano ingresso": [2020]
    })
    
    result = add_engineered_features(df, current_year=2024)
    
    # Idade_ingresso não deve ser criada
    assert "Idade_ingresso" not in result.columns
    # Mas outras features devem existir
    assert "Tempo_programa" in result.columns
    assert "Fase_num" in result.columns


def test_to_clean_object_string():
    """Testa conversão para string preservando NaN"""
    from src.feature_engineering import _to_clean_object_string
    
    series = pd.Series([1, 2, None, "test", 5.5])
    result = _to_clean_object_string(series)
    
    assert result.iloc[0] == "1"
    assert result.iloc[1] == "2"
    assert pd.isna(result.iloc[2])
    assert result.iloc[3] == "test"
    assert result.iloc[4] == "5.5"
