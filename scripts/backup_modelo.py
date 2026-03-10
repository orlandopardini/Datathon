"""
Backup do Modelo Atual
Cria backup completo antes de retreino
"""
import sys
sys.path.insert(0, '.')

import shutil
from pathlib import Path
from datetime import datetime
import json

print("="*80)
print("BACKUP DO MODELO")
print("="*80)

# Diretorios
MODEL_DIR = Path("app/model")
BACKUP_DIR = Path("backups")

def criar_backup():
    """Cria backup timestamped do modelo atual"""
    
    # Criar diretorio de backups se nao existir
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Timestamp para backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"model_{timestamp}"
    
    print(f"\nCriando backup em: {backup_path}")
    
    # Copiar toda pasta app/model
    if MODEL_DIR.exists():
        shutil.copytree(MODEL_DIR, backup_path)
        print(f"  [OK] Backup criado com sucesso")
        
        # Listar arquivos copiados
        arquivos = list(backup_path.glob("*"))
        print(f"  [INFO] {len(arquivos)} arquivos copiados:")
        for arq in arquivos:
            size_kb = arq.stat().st_size / 1024
            print(f"    - {arq.name} ({size_kb:.1f} KB)")
        
        # Salvar metadata do backup
        metadata = {
            "timestamp": timestamp,
            "source": str(MODEL_DIR.absolute()),
            "backup_path": str(backup_path.absolute()),
            "files_count": len(arquivos),
            "created_at": datetime.now().isoformat()
        }
        
        # Carregar versao do modelo para metadata
        config_path = backup_path / "model_config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                model_config = json.load(f)
            metadata["model_version"] = model_config.get("version", "unknown")
            metadata["model_type"] = model_config.get("model_type", "unknown")
        
        # Salvar metadata
        metadata_path = backup_path / "backup_metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n  [INFO] Metadata salva em: {metadata_path.name}")
        print(f"  [INFO] Versao do modelo: {metadata.get('model_version', 'unknown')}")
        
        return backup_path
    else:
        print(f"  [ERRO] Diretorio {MODEL_DIR} nao encontrado!")
        return None


def listar_backups():
    """Lista todos os backups disponiveis"""
    print("\n" + "="*80)
    print("BACKUPS DISPONIVEIS")
    print("="*80)
    
    if not BACKUP_DIR.exists():
        print("\n  [INFO] Nenhum backup encontrado")
        return []
    
    backups = sorted(BACKUP_DIR.glob("model_*"), reverse=True)
    
    if not backups:
        print("\n  [INFO] Nenhum backup encontrado")
        return []
    
    print(f"\nTotal de backups: {len(backups)}\n")
    
    for backup in backups[:10]:  # Mostrar apenas os 10 mais recentes
        # Ler metadata se existir
        metadata_path = backup / "backup_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            created = metadata.get("created_at", "unknown")
            version = metadata.get("model_version", "unknown")
            model_type = metadata.get("model_type", "unknown")
            
            print(f"  {backup.name}")
            print(f"    Criado: {created}")
            print(f"    Versao: {version} ({model_type})")
        else:
            # Se nao tem metadata, mostrar info basica
            created = datetime.fromtimestamp(backup.stat().st_ctime).isoformat()
            print(f"  {backup.name}")
            print(f"    Criado: {created}")
        print()
    
    if len(backups) > 10:
        print(f"  ... e mais {len(backups) - 10} backups antigos")
    
    return backups


def limpar_backups_antigos(manter_ultimos: int = 5):
    """Remove backups antigos, mantendo apenas os N mais recentes"""
    print("\n" + "="*80)
    print(f"LIMPEZA DE BACKUPS (manter {manter_ultimos} mais recentes)")
    print("="*80)
    
    if not BACKUP_DIR.exists():
        print("\n  [INFO] Nenhum backup para limpar")
        return
    
    backups = sorted(BACKUP_DIR.glob("model_*"), reverse=True)
    
    if len(backups) <= manter_ultimos:
        print(f"\n  [INFO] Apenas {len(backups)} backups encontrados (abaixo do limite)")
        return
    
    # Remover backups antigos
    backups_remover = backups[manter_ultimos:]
    
    print(f"\nRemovendo {len(backups_remover)} backups antigos:\n")
    
    for backup in backups_remover:
        try:
            shutil.rmtree(backup)
            print(f"  [OK] Removido: {backup.name}")
        except Exception as e:
            print(f"  [ERRO] Falha ao remover {backup.name}: {e}")
    
    print(f"\n  [INFO] Backups restantes: {manter_ultimos}")


# Executar
if __name__ == "__main__":
    # Criar backup
    backup_path = criar_backup()
    
    if backup_path:
        print("\n" + "="*80)
        print("BACKUP CONCLUIDO COM SUCESSO")
        print("="*80)
        print(f"\nCaminho do backup: {backup_path.absolute()}")
        
        # Listar todos os backups
        listar_backups()
        
        # Limpar backups antigos (manter 5)
        limpar_backups_antigos(manter_ultimos=5)
        
        print("\n" + "="*80)
        print("Para restaurar este backup, execute:")
        print(f"  python scripts/restaurar_backup.py {backup_path.name}")
        print("="*80)
        
        sys.exit(0)
    else:
        print("\n[ERRO] Falha ao criar backup!")
        sys.exit(1)
