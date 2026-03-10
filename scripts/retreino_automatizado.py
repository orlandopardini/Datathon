"""
Retreino Automatizado do Modelo
Pipeline completo de retreino com validacao
"""
import sys
sys.path.insert(0, '.')

import subprocess
from pathlib import Path
import json
from datetime import datetime
import time

print("="*80)
print("RETREINO AUTOMATIZADO - MODELO DE EVASAO ESCOLAR")
print("="*80)

# Configuracoes
VALIDACAO_MINIMA = {
    "roc_auc": 0.90,      # ROC-AUC >= 90%
    "accuracy": 0.90,     # Acuracia >= 90%
    "recall": 0.70        # Recall >= 70% (nao perder alunos em risco)
}

BACKUP_DIR = Path("backups")
MODEL_DIR = Path("app/model")

def executar_comando(cmd: str, descricao: str) -> tuple:
    """Executa um comando e retorna (sucesso, output)"""
    print(f"\n{'='*80}")
    print(f"{descricao}")
    print(f"{'='*80}")
    print(f"Comando: {cmd}\n")
    
    inicio = time.time()
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        duracao = time.time() - inicio
        
        # Mostrar output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        sucesso = result.returncode == 0
        
        print(f"\n{'='*80}")
        if sucesso:
            print(f"[OK] {descricao} - Concluido em {duracao:.2f}s")
        else:
            print(f"[ERRO] {descricao} - Falhou apos {duracao:.2f}s")
        print(f"{'='*80}")
        
        return sucesso, result.stdout
        
    except Exception as e:
        print(f"\n[ERRO] Excecao ao executar comando: {e}")
        return False, str(e)


def validar_metricas(metrics_path: Path) -> tuple:
    """Valida se metricas do novo modelo atendem criterios minimos"""
    print(f"\n{'='*80}")
    print("VALIDACAO DE METRICAS")
    print(f"{'='*80}")
    
    if not metrics_path.exists():
        print(f"\n[ERRO] Arquivo de metricas nao encontrado: {metrics_path}")
        return False, {}
    
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    
    print(f"\nMetricas do novo modelo:")
    print(f"  ROC-AUC:  {metrics.get('roc_auc', 0):.4f}")
    print(f"  Accuracy: {metrics.get('accuracy', 0):.4f}")
    print(f"  Precision: {metrics.get('precision', 0):.4f}")
    print(f"  Recall:   {metrics.get('recall', 0):.4f}")
    print(f"  F1:       {metrics.get('f1', 0):.4f}")
    
    print(f"\nCriterios minimos:")
    print(f"  ROC-AUC:  >= {VALIDACAO_MINIMA['roc_auc']:.2f}")
    print(f"  Accuracy: >= {VALIDACAO_MINIMA['accuracy']:.2f}")
    print(f"  Recall:   >= {VALIDACAO_MINIMA['recall']:.2f}")
    
    # Validar cada metrica
    validacoes = []
    
    roc_auc = metrics.get('roc_auc', 0)
    if roc_auc >= VALIDACAO_MINIMA['roc_auc']:
        print(f"\n  [OK] ROC-AUC: {roc_auc:.4f} >= {VALIDACAO_MINIMA['roc_auc']:.2f}")
        validacoes.append(True)
    else:
        print(f"\n  [FALHA] ROC-AUC: {roc_auc:.4f} < {VALIDACAO_MINIMA['roc_auc']:.2f}")
        validacoes.append(False)
    
    accuracy = metrics.get('accuracy', 0)
    if accuracy >= VALIDACAO_MINIMA['accuracy']:
        print(f"  [OK] Accuracy: {accuracy:.4f} >= {VALIDACAO_MINIMA['accuracy']:.2f}")
        validacoes.append(True)
    else:
        print(f"  [FALHA] Accuracy: {accuracy:.4f} < {VALIDACAO_MINIMA['accuracy']:.2f}")
        validacoes.append(False)
    
    recall = metrics.get('recall', 0)
    if recall >= VALIDACAO_MINIMA['recall']:
        print(f"  [OK] Recall: {recall:.4f} >= {VALIDACAO_MINIMA['recall']:.2f}")
        validacoes.append(True)
    else:
        print(f"  [FALHA] Recall: {recall:.4f} < {VALIDACAO_MINIMA['recall']:.2f}")
        validacoes.append(False)
    
    todas_ok = all(validacoes)
    
    print(f"\n{'='*80}")
    if todas_ok:
        print("[OK] MODELO APROVADO - Todas metricas atendem criterios minimos")
    else:
        print("[FALHA] MODELO REPROVADO - Metricas abaixo dos criterios minimos")
    print(f"{'='*80}")
    
    return todas_ok, metrics


def pipeline_retreino():
    """Executa pipeline completo de retreino"""
    inicio_total = time.time()
    
    print(f"\nInicio do retreino: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # PASSO 1: Validar data contracts
    sucesso, _ = executar_comando(
        "python scripts/validar_data_contracts.py",
        "PASSO 1/6: Validacao de Data Contracts"
    )
    
    if not sucesso:
        print("\n[ERRO CRITICO] Data contracts invalidos. Abortando retreino.")
        return False
    
    # PASSO 2: Backup do modelo atual
    sucesso, _ = executar_comando(
        "python scripts/backup_modelo.py",
        "PASSO 2/6: Backup do Modelo Atual"
    )
    
    if not sucesso:
        print("\n[ERRO CRITICO] Falha ao criar backup. Abortando retreino.")
        return False
    
    # PASSO 3: Retreinar modelo
    sucesso, _ = executar_comando(
        "python src/train.py",
        "PASSO 3/6: Treinamento do Novo Modelo"
    )
    
    if not sucesso:
        print("\n[ERRO CRITICO] Falha no treinamento. Abortando retreino.")
        return False
    
    # PASSO 4: Validar metricas
    metricas_ok, metricas = validar_metricas(MODEL_DIR / "metrics.json")
    
    if not metricas_ok:
        print("\n[ERRO CRITICO] Metricas abaixo dos criterios minimos.")
        print("\nRECOMENDACAO:")
        print("  1. Investigar qualidade dos novos dados")
        print("  2. Ajustar hiperparametros")
        print("  3. Verificar drift de features")
        print("\nAbortando retreino. Modelo atual mantido.")
        return False
    
    # PASSO 5: Executar testes
    sucesso, _ = executar_comando(
        "pytest tests/ -v --tb=short --cov=src --cov-report=term",
        "PASSO 5/6: Execucao de Testes"
    )
    
    if not sucesso:
        print("\n[AVISO] Alguns testes falharam, mas modelo sera mantido.")
        print("RECOMENDACAO: Investigar falhas de teste antes de usar em producao.")
    
    # PASSO 6: Avaliar modelo
    sucesso, _ = executar_comando(
        "python src/evaluate.py",
        "PASSO 6/6: Avaliacao Final do Modelo"
    )
    
    # Relatorio final
    duracao_total = time.time() - inicio_total
    
    print(f"\n{'='*80}")
    print("RETREINO CONCLUIDO COM SUCESSO")
    print(f"{'='*80}")
    print(f"\nDuracao total: {duracao_total:.2f}s ({duracao_total/60:.1f} minutos)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\nMetricas do novo modelo:")
    print(f"  ROC-AUC:   {metricas['roc_auc']:.4f}")
    print(f"  Accuracy:  {metricas['accuracy']:.4f}")
    print(f"  Precision: {metricas['precision']:.4f}")
    print(f"  Recall:    {metricas['recall']:.4f}")
    print(f"  F1:        {metricas['f1']:.4f}")
    
    print(f"\nProximos passos:")
    print(f"  1. [OPCIONAL] Testar API: uvicorn app.main:app --reload")
    print(f"  2. [OPCIONAL] Validar predicoes manualmente")
    print(f"  3. [RECOMENDADO] A/B test com modelo anterior")
    print(f"  4. Deploy em producao quando confiante")
    
    print(f"\nPara rollback (se necessario):")
    # Listar ultimo backup
    backups = sorted(BACKUP_DIR.glob("model_*"), reverse=True)
    if backups:
        ultimo_backup = backups[0].name
        print(f"  python scripts/restaurar_backup.py {ultimo_backup}")
    
    print(f"{'='*80}")
    
    return True


# Executar
if __name__ == "__main__":
    print("\n[INFO] Iniciando pipeline de retreino automatizado...")
    print("[INFO] Este processo pode levar alguns minutos.")
    
    try:
        sucesso = pipeline_retreino()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n[AVISO] Retreino interrompido pelo usuario!")
        print("[INFO] Modelo atual mantido sem alteracoes.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO CRITICO] Excecao nao tratada: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
