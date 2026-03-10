"""
Testa o formulario simplificado com campos essenciais e opcionais

Para executar:
    1. Iniciar API: uvicorn app.main:app --reload
    2. Rodar: pytest tests/test_simplified_form.py -v
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


def test_formulario_campos_minimos(api_available):
    """Testa com apenas campos obrigatorios (9 campos)"""
    test_minimal = {
        "Idade": 12,
        "Gênero": "M",
        "Ano ingresso": 2020,
        "Fase": "3A",
        "Instituição de ensino": "Escola Pública",
        "INDE 2024": 5.0,
        "IAA": 4.5,
        "IPS": 5.2,
        "Nº Av": 10
    }

    response = requests.post(
        f"{API_URL}/predict",
        json={"records": [test_minimal]},
        timeout=5
    )

    assert response.status_code == 200
    result = response.json()
    pred = result["predictions"][0]
    
    assert "at_risk_probability" in pred
    assert "at_risk_label" in pred
    assert 0 <= pred["at_risk_probability"] <= 1.0


def test_formulario_campos_completos(api_available):
    """Testa com campos obrigatorios + opcionais"""
    test_with_optionals = {
        "Idade": 14,
        "Gênero": "F",
        "Ano ingresso": 2018,
        "Fase": "5A",
        "Instituição de ensino": "Escola Pública",
        "INDE 2024": 8.5,
        "INDE 23": 8.0,  # OPCIONAL
        "INDE 22": 7.5,  # OPCIONAL
        "IAA": 8.2,
        "IPS": 8.5,
        "IPP": 8.0,      # OPCIONAL
        "IPV": 8.3,      # OPCIONAL
        "IAN": 8.1,      # OPCIONAL
        "Nº Av": 15
    }

    response = requests.post(
        f"{API_URL}/predict",
        json={"records": [test_with_optionals]},
        timeout=5
    )

    assert response.status_code == 200
    result = response.json()
    pred = result["predictions"][0]
    
    assert "at_risk_probability" in pred
    assert "at_risk_label" in pred
    assert 0 <= pred["at_risk_probability"] <= 1.0
print("💡 Redução de complexidade: 15 → 9 campos obrigatórios (40% menos!)")
print("💡 Dashboard: http://localhost:8000")
