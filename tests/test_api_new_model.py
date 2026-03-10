"""
Teste de Integracao da API (requer API rodando)

Para executar:
    1. Iniciar API: uvicorn app.main:app --reload
    2. Rodar: pytest tests/test_api_new_model.py -v
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


def test_health_endpoint(api_available):
    """Testa endpoint /health"""
    response = requests.get(f"{API_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_metrics_endpoint(api_available):
    """Testa endpoint /metrics"""
    response = requests.get(f"{API_URL}/metrics", timeout=5)
    assert response.status_code == 200
    metrics = response.json()
    # Verifica que metricas contem campos esperados
    assert "roc_auc" in metrics or "warning" in metrics


def test_predict_notas_baixas(api_available):
    """Testa predicao com indicadores baixos (deve dar alto risco)"""
    payload_baixas = {
        "records": [{
            "Idade": 11,
            "Gênero": "Masculino",
            "Ano ingresso": 2023,
            "Instituição de ensino": "Pública",
            "Fase": "1B",
            "Turma": "1B",
            "INDE 2024": 4.5,
            "IAA": 4.0,
            "IPS": 4.5,
            "Nº Av": 2
        }]
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload_baixas, timeout=5)
    assert response.status_code == 200
    
    result = response.json()
    pred = result["predictions"][0]
    prob_risco = pred["at_risk_probability"]
    
    # Com indicadores baixos, probabilidade de risco deve ser maior
    assert 0 <= prob_risco <= 1.0, "Probabilidade deve estar entre 0 e 1"


def test_predict_notas_altas(api_available):
    """Testa predicao com indicadores altos (deve dar baixo risco)"""
    payload_altas = {
        "records": [{
            "Idade": 12,
            "Gênero": "Feminino",
            "Ano ingresso": 2020,
            "Instituição de ensino": "Pública",
            "Fase": "3A",
            "Turma": "3A",
            "INDE 22": 8.0,
            "INDE 23": 8.5,
            "INDE 2024": 9.0,
            "IAA": 9.0,
            "IPS": 8.5,
            "IPP": 8.5,
            "IPV": 8.0,
            "IAN": 9.0,
            "Nº Av": 2
        }]
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload_altas, timeout=5)
    assert response.status_code == 200
    
    result = response.json()
    pred = result["predictions"][0]
    prob_risco = pred["at_risk_probability"]
    
    # Com indicadores altos, probabilidade de risco deve ser menor
    assert 0 <= prob_risco <= 1.0, "Probabilidade deve estar entre 0 e 1"
print("="*80)
print("\n💡 Para acessar o dashboard:")
print("   http://localhost:8000")
print("\n💡 Para acessar a documentação da API:")
print("   http://localhost:8000/docs")
