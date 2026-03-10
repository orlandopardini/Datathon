#!/usr/bin/env python3
"""
Verifica se o modelo carregado está correto e não tem o atributo multi_class problemático.
Este script é executado durante o build do Docker para garantir que o modelo é válido.
"""
import sys
import joblib
from pathlib import Path

def verify_model():
    model_path = Path("app/model/model.joblib")
    
    if not model_path.exists():
        print(f"❌ ERRO: Modelo não encontrado em {model_path}")
        sys.exit(1)
    
    print(f"📦 Carregando modelo de {model_path}...")
    print(f"   Tamanho do arquivo: {model_path.stat().st_size} bytes")
    
    try:
        model = joblib.load(model_path)
        print("✅ Modelo carregado com sucesso")
    except Exception as e:
        print(f"❌ ERRO ao carregar modelo: {e}")
        sys.exit(1)
    
    # Verificar estrutura do modelo
    if not hasattr(model, 'named_steps'):
        print("❌ ERRO: Modelo não é um pipeline sklearn")
        sys.exit(1)
    
    print(f"📋 Pipeline steps: {list(model.named_steps.keys())}")
    
    # Verificar classificador
    if 'clf' not in model.named_steps:
        print("❌ ERRO: Pipeline não contém step 'clf'")
        sys.exit(1)
    
    clf = model.named_steps['clf']
    print(f"🤖 Classificador: {type(clf).__name__}")
    
    # VERIFICAÇÃO CRÍTICA: multi_class attribute
    if hasattr(clf, 'multi_class'):
        print("❌ ERRO CRÍTICO: Modelo tem atributo 'multi_class'!")
        print("   Este modelo é incompatível com sklearn 1.8.0+")
        print("   O modelo precisa ser retreinado.")
        sys.exit(1)
    
    print("✅ Modelo NÃO tem atributo multi_class (OK para sklearn 1.8.0+)")
    
    # Verificar parâmetros esperados
    params = clf.get_params()
    print(f"⚙️  Parâmetros do modelo:")
    print(f"   - solver: {params.get('solver', 'N/A')}")
    print(f"   - max_iter: {params.get('max_iter', 'N/A')}")
    print(f"   - random_state: {params.get('random_state', 'N/A')}")
    
    if params.get('solver') != 'lbfgs':
        print("⚠️  AVISO: Solver não é 'lbfgs'")
    
    print("\n✅ VERIFICAÇÃO COMPLETA: Modelo válido e compatível!")
    return 0

if __name__ == "__main__":
    sys.exit(verify_model())
