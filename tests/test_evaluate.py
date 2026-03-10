"""
Testes para o módulo de avaliação
"""
import pytest
import numpy as np
from src.evaluate import evaluate_binary


def test_evaluate_binary_perfect_prediction():
    """Testa métricas com predição perfeita"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, 0.2, 0.9, 0.95])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
    assert metrics["roc_auc"] == 1.0


def test_evaluate_binary_random_prediction():
    """Testa métricas com predição aleatória"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.6, 0.4, 0.3, 0.7])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["roc_auc"] <= 1.0


def test_evaluate_binary_all_positive():
    """Testa métricas quando prediz tudo como positivo"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.9, 0.8, 0.95, 0.99])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    # Com threshold 0.5, todos são positivos
    assert metrics["recall"] == 1.0


def test_evaluate_binary_all_negative():
    """Testa métricas quando prediz tudo como negativo"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, 0.2, 0.3, 0.4])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    # Com threshold 0.5, todos são negativos
    assert metrics["recall"] == 0.0


def test_evaluate_binary_confusion_matrix():
    """Testa matriz de confusão"""
    y_true = np.array([0, 0, 1, 1, 0, 1])
    y_proba = np.array([0.2, 0.6, 0.8, 0.4, 0.1, 0.9])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    cm = metrics["confusion_matrix"]
    
    # Deve ser matriz 2x2
    assert len(cm) == 2
    assert len(cm[0]) == 2


def test_evaluate_binary_returns_all_metrics():
    """Testa que todas as métricas esperadas são retornadas"""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([0.1, 0.9, 0.2, 0.8])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    expected_keys = [
        "accuracy", "precision", "recall", "f1",
        "roc_auc", "pr_auc", "confusion_matrix", "threshold"
    ]
    
    for key in expected_keys:
        assert key in metrics


def test_evaluate_binary_custom_threshold():
    """Testa com threshold customizado"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.3, 0.4, 0.6, 0.7])
    
    # Threshold 0.5 (padrão)
    metrics_05 = evaluate_binary(y_true, y_proba, threshold=0.5)
    
    # Threshold 0.55 (mais restritivo)
    metrics_055 = evaluate_binary(y_true, y_proba, threshold=0.55)
    
    assert metrics_05["threshold"] == 0.5
    assert metrics_055["threshold"] == 0.55
    
    # Com threshold mais alto, menos classificações positivas
    # Logo recall deve ser menor ou igual
    assert metrics_055["recall"] <= metrics_05["recall"]


def test_evaluate_binary_imbalanced_data():
    """Testa métricas com dados desbalanceados"""
    y_true = np.array([0, 0, 0, 0, 1])
    y_proba = np.array([0.1, 0.2, 0.3, 0.6, 0.9])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
    assert 0.0 <= metrics["f1"] <= 1.0


def test_evaluate_binary_with_probabilities():
    """Testa que probabilidades são usadas para ROC-AUC"""
    y_true = np.array([0, 0, 1, 1])
    
    # Probabilidades boas
    y_proba_good = np.array([0.1, 0.2, 0.9, 0.95])
    metrics_good = evaluate_binary(y_true, y_proba_good)
    
    # Probabilidades ruins (perto de 0.5)
    y_proba_bad = np.array([0.4, 0.45, 0.55, 0.6])
    metrics_bad = evaluate_binary(y_true, y_proba_bad)
    
    # ROC-AUC deve ser melhor ou igual com probabilidades boas
    assert metrics_good["roc_auc"] >= metrics_bad["roc_auc"]


def test_evaluate_binary_numpy_types():
    """Testa que métricas retornam tipos Python nativos"""
    y_true = np.array([0, 1])
    y_proba = np.array([0.2, 0.8])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    # Deve ser float nativo
    assert isinstance(metrics["accuracy"], float)
    assert isinstance(metrics["precision"], float)
    assert isinstance(metrics["recall"], float)
    assert isinstance(metrics["f1"], float)


def test_evaluate_binary_boundary_probabilities():
    """Testa com probabilidades nos limites (0 e 1)"""
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.0, 0.0, 1.0, 1.0])
    
    metrics = evaluate_binary(y_true, y_proba)
    
    assert metrics["accuracy"] == 1.0
    assert metrics["roc_auc"] == 1.0
