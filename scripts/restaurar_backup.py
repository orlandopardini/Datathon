"""
Restaurar Backup do Modelo
Restaura um backup especifico
"""
import sys
sys.path.insert(0, '.')

import shutil
from pathlib import Path
import json

print("="*80)
print("RESTAURAR BACKUP DO MODELO")
print("="*80)

BACKUP_DIR = Path("backups")
MODEL_DIR = Path("app/model")

def listar_backups_disponiveis():
    """Lista backups disponiveis"""
    if not BACKUP_DIR.exists():
        return []
    
    backups = sorted(BACKUP_DIR.glob("model_*"), reverse=True)
    return backups


def restaurar_backup(backup_name: str):
    """Restaura um backup especifico"""
    backup_path = BACKUP_DIR / backup_name
    
    if not backup_path.exists():
        print(f"\n[ERRO] Backup nao encontrado: {backup_path}")
        return False
    
    print(f"\nRestaurando backup: {backup_name}")
    
    # Ler metadata
    metadata_path = backup_path / "backup_metadata.json"
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        print(f"  Versao: {metadata.get('model_version', 'unknown')}")
        print(f"  Criado em: {metadata.get('created_at', 'unknown')}")
        print(f"  Arquivos: {metadata.get('files_count', 0)}")
    
    # Fazer backup do modelo atual antes de sobrescrever
    print(f"\n  [INFO] Fazendo backup do modelo atual...")
    import scripts.backup_modelo as backup_script
    backup_atual = backup_script.criar_backup()
    
    if backup_atual:
        print(f"  [OK] Modelo atual salvo em: {backup_atual.name}")
    
    # Remover modelo atual
    if MODEL_DIR.exists():
        shutil.rmtree(MODEL_DIR)
        print(f"  [OK] Modelo atual removido")
    
    # Copiar backup para local do modelo
    shutil.copytree(backup_path, MODEL_DIR)
    print(f"  [OK] Backup restaurado em: {MODEL_DIR}")
    
    # Verificar arquivos
    arquivos = list(MODEL_DIR.glob("*"))
    print(f"\n  [INFO] {len(arquivos)} arquivos restaurados:")
    for arq in arquivos:
        if arq.name != "backup_metadata.json":
            size_kb = arq.stat().st_size / 1024
            print(f"    - {arq.name} ({size_kb:.1f} KB)")
    
    return True


# Executar
if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("\nUSO: python scripts/restaurar_backup.py <nome_do_backup>")
        print("\nBackups disponiveis:\n")
        
        backups = listar_backups_disponiveis()
        if not backups:
            print("  [INFO] Nenhum backup encontrado")
        else:
            for backup in backups[:10]:
                metadata_path = backup / "backup_metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    version = metadata.get('model_version', 'unknown')
                    created = metadata.get('created_at', 'unknown')
                    print(f"  {backup.name} (v{version}, {created})")
                else:
                    print(f"  {backup.name}")
        
        print(f"\nExemplo: python scripts/restaurar_backup.py model_20250122_153045")
        sys.exit(1)
    
    backup_name = sys.argv[1]
    
    # Restaurar
    if restaurar_backup(backup_name):
        print("\n" + "="*80)
        print("BACKUP RESTAURADO COM SUCESSO")
        print("="*80)
        print("\nReinicie a API para carregar o modelo restaurado:")
        print("  uvicorn app.main:app --reload")
        print("="*80)
        sys.exit(0)
    else:
        print("\n[ERRO] Falha ao restaurar backup")
        sys.exit(1)
