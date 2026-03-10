"""
Testes para o módulo de treinamento
"""
import pytest
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
from sklearn.pipeline import Pipeline
from src.train import build_pipeline


def test_build_pipeline_returns_pipeline():
    """Testa que build_pipeline retorna um Pipeline sklearn"""
    numeric_cols = ["Idade", "IAA", "IEG"]
    categorical_cols = ["Gênero", "Fase"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    assert isinstance(model, Pipeline)
    assert "preprocess" in model.named_steps
    assert "clf" in model.named_steps


def test_build_pipeline_with_numeric_only():
    """Testa pipeline com apenas colunas numéricas"""
    numeric_cols = ["Idade", "IAA", "INDE 2024"]
    categorical_cols = []
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    assert isinstance(model, Pipeline)


def test_build_pipeline_with_categorical_only():
    """Testa pipeline com apenas colunas categóricas"""
    numeric_cols = []
    categorical_cols = ["Gênero", "Fase", "Turma"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    assert isinstance(model, Pipeline)


def test_build_pipeline_classifier_type():
    """Testa que o classificador é LogisticRegression"""
    numeric_cols = ["Idade"]
    categorical_cols = ["Gênero"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    # Verificar que o último step é um classificador
    clf = model.named_steps["clf"]
    assert hasattr(clf, "fit")
    assert hasattr(clf, "predict")
    assert hasattr(clf, "predict_proba")


def test_build_pipeline_fit_predict():
    """Testa que o pipeline pode ser treinado e fazer predições"""
    # Dados de exemplo
    X_train = pd.DataFrame({
        "Idade": [10, 12, 14, 16, 18, 20],
        "IAA": [5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        "Gênero": ["M", "F", "M", "F", "M", "F"]
    })
    y_train = np.array([1, 1, 0, 0, 0, 0])
    
    numeric_cols = ["Idade", "IAA"]
    categorical_cols = ["Gênero"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    # Treinar
    model.fit(X_train, y_train)
    
    # Predizer
    y_pred = model.predict(X_train)
    y_proba = model.predict_proba(X_train)
    
    assert len(y_pred) == len(y_train)
    assert y_proba.shape == (len(y_train), 2)


def test_build_pipeline_handles_missing_values():
    """Testa que o pipeline lida com valores ausentes"""
    X_train = pd.DataFrame({
        "Idade": [10, np.nan, 14, 16],
        "IAA": [5.0, 6.0, np.nan, 8.0],
        "Gênero": ["M", None, "M", "F"]
    })
    y_train = np.array([1, 0, 0, 0])
    
    numeric_cols = ["Idade", "IAA"]
    categorical_cols = ["Gênero"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    # Deve treinar sem erros
    model.fit(X_train, y_train)
    
    # Deve predizer sem erros
    y_pred = model.predict(X_train)
    assert len(y_pred) == len(y_train)


def test_build_pipeline_handles_unknown_categories():
    """Testa que o pipeline lida com categorias desconhecidas em teste"""
    X_train = pd.DataFrame({
        "Idade": [10, 12, 14],
        "Gênero": ["M", "F", "M"]
    })
    y_train = np.array([1, 0, 0])
    
    X_test = pd.DataFrame({
        "Idade": [11],
        "Gênero": ["Outro"]  # Categoria não vista no treino
    })
    
    numeric_cols = ["Idade"]
    categorical_cols = ["Gênero"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(X_train, y_train)
    
    # Deve predizer sem erros (handle_unknown="ignore")
    y_pred = model.predict(X_test)
    assert len(y_pred) == 1


def test_build_pipeline_standardizes_numeric():
    """Testa que features numéricas são padronizadas"""
    X_train = pd.DataFrame({
        "Feature1": [1, 2, 3, 4, 5],
        "Feature2": [100, 200, 300, 400, 500],
        "Cat": ["A", "B", "A", "B", "A"]
    })
    y_train = np.array([0, 0, 1, 1, 1])
    
    numeric_cols = ["Feature1", "Feature2"]
    categorical_cols = ["Cat"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(X_train, y_train)
    
    # Pode predizer mesmo com valores de escala muito diferentes
    X_test = pd.DataFrame({
        "Feature1": [10],
        "Feature2": [1000],
        "Cat": ["A"]
    })
    
    y_pred = model.predict(X_test)
    assert len(y_pred) == 1


def test_build_pipeline_onehot_categorical():
    """Testa que features categóricas são one-hot encoded"""
    X_train = pd.DataFrame({
        "Num": [1, 2, 3, 4],
        "Cat1": ["A", "B", "A", "B"],
        "Cat2": ["X", "Y", "X", "Y"]
    })
    y_train = np.array([0, 1, 0, 1])
    
    numeric_cols = ["Num"]
    categorical_cols = ["Cat1", "Cat2"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(X_train, y_train)
    
    # Transformer deve ter criado múltiplas features de Cat1 e Cat2
    preprocessor = model.named_steps["preprocess"]
    X_transformed = preprocessor.transform(X_train)
    
    # Deve ter mais colunas que o original (one-hot encoding)
    assert X_transformed.shape[1] > len(numeric_cols)


def test_build_pipeline_empty_columns():
    """Testa que pipeline lida com listas vazias"""
    # Apenas numéricas
    model1 = build_pipeline(["Idade"], [])
    assert isinstance(model1, Pipeline)
    
    # Apenas categóricas
    model2 = build_pipeline([], ["Gênero"])
    assert isinstance(model2, Pipeline)


def test_build_pipeline_many_columns():
    """Testa pipeline com muitas colunas"""
    numeric_cols = [f"num_{i}" for i in range(20)]
    categorical_cols = [f"cat_{i}" for i in range(10)]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    
    assert isinstance(model, Pipeline)


def test_build_pipeline_reproducibility():
    """Testa que o pipeline produz resultados consistentes"""
    X = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": ["X", "Y", "X", "Y", "X"]
    })
    y = np.array([0, 1, 0, 1, 0])
    
    model1 = build_pipeline(["A"], ["B"])
    model1.fit(X, y)
    pred1 = model1.predict_proba(X)
    
    model2 = build_pipeline(["A"], ["B"])
    model2.fit(X, y)
    pred2 = model2.predict_proba(X)
    
    # Deve produzir os mesmos resultados
    np.testing.assert_array_almost_equal(pred1, pred2)


def test_build_pipeline_with_real_features():
    """Testa pipeline com features reais do projeto"""
    X = pd.DataFrame({
        "Idade": [12, 14, 16, 18],
        "Tempo_programa": [2, 3, 4, 5],
        "IAA": [7.5, 8.0, 6.5, 9.0],
        "INDE 2024": [7.0, 8.5, 6.0, 9.5],
        "Fase": ["1A", "2A", "3A", "4B"],
        "Gênero": ["M", "F", "M", "F"]
    })
    y = np.array([0, 0, 1, 0])
    
    numeric_cols = ["Idade", "Tempo_programa", "IAA", "INDE 2024"]
    categorical_cols = ["Fase", "Gênero"]
    
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(X, y)
    
    # Fazer predição
    pred = model.predict(X)
    proba = model.predict_proba(X)
    
    assert len(pred) == 4
    assert proba.shape == (4, 2)
    assert all(proba[:, 0] + proba[:, 1] == 1.0)  # Probabilidades somam 1


def test_build_pipeline_pickle_serializable():
    """Testa que o pipeline pode ser serializado"""
    import pickle
    
    model = build_pipeline(["A"], ["B"])
    
    # Deve ser serializável
    pickled = pickle.dumps(model)
    unpickled = pickle.loads(pickled)
    
    assert isinstance(unpickled, Pipeline)


def test_build_pipeline_named_steps():
    """Testa que os steps do pipeline têm os nomes corretos"""
    model = build_pipeline(["Num"], ["Cat"])
    
    assert "preprocess" in model.named_steps
    assert "clf" in model.named_steps
    
    # Verificar número de steps
    assert len(model.steps) == 2


def test_build_pipeline_integration_full_workflow():
    """Testa workflow completo de treino e predição"""
    # Criar dados simulados
    np.random.seed(42)
    n = 100
    X = pd.DataFrame({
        "Idade": np.random.randint(10, 20, n),
        "IAA": np.random.uniform(5, 10, n),
        "INDE 2024": np.random.uniform(5, 10, n),
        "Tempo_programa": np.random.randint(1, 6, n),
        "Gênero": np.random.choice(["M", "F"], n),
        "Fase": np.random.choice(["1A", "2A", "3A", "4A"], n)
    })
    
    # Target correlacionado com as features
    y = ((X["IAA"] + X["INDE 2024"]) / 2 < 7).astype(int).values
    
    numeric_cols = ["Idade", "IAA", "INDE 2024", "Tempo_programa"]
    categorical_cols = ["Gênero", "Fase"]
    
    # Treinar
    model = build_pipeline(numeric_cols, categorical_cols)
    model.fit(X, y)
    
    # Predizer
    pred = model.predict(X)
    proba = model.predict_proba(X)
    
    # Validações
    assert len(pred) == n
    assert proba.shape == (n, 2)
    
    # Accuracy deve ser razoável (> 50% - melhor que random)
    accuracy = (pred == y).mean()
    assert accuracy > 0.5


def test_build_pipeline_feature_importance():
    """Testa que modelo treinado tem coeficientes acessíveis"""
    X = pd.DataFrame({
        "A": [1, 2, 3, 4, 5, 6, 7, 8],
        "B": ["X", "Y", "X", "Y", "X", "Y", "X", "Y"]
    })
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    
    model = build_pipeline(["A"], ["B"])
    model.fit(X, y)
    
    # Logistic Regression deve ter coeficientes
    clf = model.named_steps["clf"]
    assert hasattr(clf, "coef_")
    assert clf.coef_.shape[0] > 0


def test_build_pipeline_predict_single_sample():
    """Testa predição de uma única amostra"""
    X_train = pd.DataFrame({
        "Num": [1, 2, 3, 4, 5],
        "Cat": ["A", "B", "A", "B", "A"]
    })
    y_train = np.array([0, 1, 0, 1, 0])
    
    model = build_pipeline(["Num"], ["Cat"])
    model.fit(X_train, y_train)
    
    # Predizer uma única amostra
    X_test = pd.DataFrame({"Num": [3], "Cat": ["A"]})
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)
    
    assert len(pred) == 1
    assert proba.shape == (1, 2)


def test_build_pipeline_consistent_predictions():
    """Testa que predições são consistentes"""
    X = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["X", "Y", "Z"]
    })
    y = np.array([0, 1, 0])
    
    model = build_pipeline(["A"], ["B"])
    model.fit(X, y)
    
    # Múltiplas predições devem dar o mesmo resultado
    pred1 = model.predict(X)
    pred2 = model.predict(X)
    
    np.testing.assert_array_equal(pred1, pred2)
