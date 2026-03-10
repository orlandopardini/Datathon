"""
Testa a integracao do dashboard com a API

Para executar:
    1. Iniciar API: uvicorn app.main:app --reload
    2. Rodar: pytest tests/test_dashboard_integration.py -v
"""
import pytest
import requests
import json

API_URL = "http://localhost:8000"


@pytest.fixture(scope="module")
def api_available():
    """Verifica se API esta disponivel, senao pula os testes"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    pytest.skip("API nao esta rodando. Inicie: uvicorn app.main:app --reload")


def test_dashboard_indicadores_baixos(api_available):
    """Testa predicao via dashboard com indicadores baixos"""
    test_data_low = {
        "Fase": "3A",
        "Turma": "3A",
        "Idade": 12,
        "Gênero": "M",
        "Ano ingresso": 2020,
        "Instituição de ensino": "Escola Pública",
        "INDE 22": 4.5,
        "INDE 23": 4.8,
        "INDE 2024": 5.0,
        "IAA": 4.0,
        "IPS": 4.5,
        "IPP": 4.2,
        "IPV": 4.8,
        "IAN": 4.3,
        "Nº Av": 10
    }

    response = requests.post(
        f"{API_URL}/predict",
        json={"records": [test_data_low]},
        timeout=5
    )

    assert response.status_code == 200
    result = response.json()
    pred = result["predictions"][0]
    
    assert "at_risk_probability" in pred
    assert "at_risk_label" in pred
    assert 0 <= pred["at_risk_probability"] <= 1.0


def test_dashboard_indicadores_altos(api_available):
    """Testa predicao via dashboard com indicadores altos"""
    test_data_high = {
        "Fase": "5A",
        "Turma": "5A",
        "Idade": 14,
        "Gênero": "F",
        "Ano ingresso": 2018,
        "Instituição de ensino": "Escola Pública",
        "INDE 22": 8.5,
        "INDE 23": 8.8,
        "INDE 2024": 9.0,
        "IAA": 8.5,
        "IPS": 8.8,
        "IPP": 9.0,
        "IPV": 8.7,
        "IAN": 8.9,
        "Nº Av": 15
    }

    response = requests.post(
        f"{API_URL}/predict",
        json={"records": [test_data_high]},
        timeout=5
    )

    assert response.status_code == 200
    result = response.json()
    pred = result["predictions"][0]
    
    assert "at_risk_probability" in pred
    assert "at_risk_label" in pred
    assert 0 <= pred["at_risk_probability"] <= 1.0
