"""
Testes para o módulo de utilitários
"""
import pytest
import json
import tempfile
from pathlib import Path
from src.utils import read_json, write_json, ensure_dir


def test_write_and_read_json():
    """Testa escrita e leitura de JSON"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"
        data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        
        # Escrever
        write_json(file_path, data)
        
        # Ler
        read_data = read_json(file_path)
        
        assert read_data == data


def test_read_json_with_utf8():
    """Testa leitura de JSON com caracteres UTF-8"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_utf8.json"
        data = {
            "nome": "João",
            "descrição": "Aluno com ótimo desempenho",
            "instituição": "Escola Pública"
        }
        
        write_json(file_path, data)
        read_data = read_json(file_path)
        
        assert read_data == data
        assert read_data["nome"] == "João"
        assert "ótimo" in read_data["descrição"]


def test_write_json_creates_directory():
    """Testa que write_json cria diretório se não existir"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "subdir" / "nested" / "test.json"
        data = {"test": "data"}
        
        # Diretório não existe
        assert not file_path.parent.exists()
        
        # Escrever deve criar o diretório
        write_json(file_path, data)
        
        # Agora deve existir
        assert file_path.exists()
        assert read_json(file_path) == data


def test_ensure_dir_creates_directory():
    """Testa que ensure_dir cria diretório"""
    with tempfile.TemporaryDirectory() as tmpdir:
        new_dir = Path(tmpdir) / "new_directory"
        
        assert not new_dir.exists()
        
        ensure_dir(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()


def test_ensure_dir_nested():
    """Testa que ensure_dir cria diretórios aninhados"""
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_dir = Path(tmpdir) / "a" / "b" / "c"
        
        assert not nested_dir.exists()
        
        ensure_dir(nested_dir)
        
        assert nested_dir.exists()
        assert nested_dir.is_dir()


def test_ensure_dir_already_exists():
    """Testa que ensure_dir não quebra se diretório já existe"""
    with tempfile.TemporaryDirectory() as tmpdir:
        existing_dir = Path(tmpdir) / "existing"
        existing_dir.mkdir()
        
        # Não deve lançar exceção
        ensure_dir(existing_dir)
        
        assert existing_dir.exists()


def test_read_json_file_not_found():
    """Testa que read_json lança erro se arquivo não existe"""
    with pytest.raises(FileNotFoundError):
        read_json("non_existent_file.json")


def test_write_json_with_path_string():
    """Testa write_json com string em vez de Path"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = str(Path(tmpdir) / "test.json")
        data = {"test": "string path"}
        
        write_json(file_path, data)
        
        assert Path(file_path).exists()
        assert read_json(file_path) == data


def test_read_json_with_path_string():
    """Testa read_json com string em vez de Path"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"
        data = {"test": "read string"}
        
        file_path.write_text(json.dumps(data), encoding="utf-8")
        
        # Ler usando string
        read_data = read_json(str(file_path))
        
        assert read_data == data


def test_write_json_complex_types():
    """Testa write_json com tipos complexos"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "complex.json"
        data = {
            "string": "text",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "nested": {
                "a": 1,
                "b": [4, 5, 6]
            }
        }
        
        write_json(file_path, data)
        read_data = read_json(file_path)
        
        assert read_data == data
        assert read_data["nested"]["b"] == [4, 5, 6]


def test_ensure_dir_with_file_path():
    """Testa ensure_dir com caminho de arquivo (deve criar diretório pai)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "subdir" / "file.txt"
        
        # Garantir diretório pai
        ensure_dir(file_path.parent)
        
        assert file_path.parent.exists()
        assert file_path.parent.is_dir()
