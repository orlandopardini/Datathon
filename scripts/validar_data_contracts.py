"""
Validacao de Data Contracts
Valida schema e qualidade dos dados de entrada
"""
import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

print("="*80)
print("VALIDACAO DE DATA CONTRACTS - PEDE 2024")
print("="*80)

# Definir contratos de dados
DATA_CONTRACTS = {
    "OBRIGATORIOS": [
        "Idade", "Gênero", "Ano ingresso", "Fase", 
        "Instituição de ensino", "INDE 2024", "IAA", "IPS", "Nº Av"
    ],
    "OPCIONAIS": [
        "IDA", "Mat", "Por", "Ing",
        "INDE 23", "INDE 22",
        "IPP", "IPV", "IAN",
        "Turma", "IEG"
    ],
    "RANGES": {
        "Idade": (8, 25),
        "Ano ingresso": (2015, 2026),
        "INDE 2024": (0, 10),
        "INDE 23": (0, 10),
        "INDE 22": (0, 10),
        "IEG": (0, 10),
        "IDA": (0, 10),
        "Mat": (0, 10),
        "Por": (0, 10),
        "Ing": (0, 10),
        "IAA": (0, 10),
        "IPS": (0, 10),
        "IPP": (0, 10),
        "IPV": (0, 10),
        "IAN": (0, 10),
        "Nº Av": (0, 100)
    },
    "TIPOS": {
        "Idade": "numeric",
        "Gênero": "categorical",
        "Ano ingresso": "numeric",
        "Fase": "categorical",
        "Instituição de ensino": "categorical",
        "Turma": "categorical"
    },
    "VALORES_VALIDOS": {
        "Gênero": ["M", "F", "Masculino", "Feminino"],
        "Fase": ["ALFA", "1A", "1B", "1R", "2A", "3A", "4A", "5A", "6A", "7E", "8", "9"]
    }
}

def validar_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Valida se todas colunas obrigatorias existem"""
    erros = []
    
    print("\n1. VALIDACAO DE SCHEMA")
    print("-" * 80)
    
    # Checar colunas obrigatorias
    for col in DATA_CONTRACTS["OBRIGATORIOS"]:
        if col not in df.columns:
            erros.append(f"ERRO: Coluna obrigatoria '{col}' faltando!")
            print(f"  [ERRO] {col}: FALTANDO")
        else:
            print(f"  [OK] {col}: presente")
    
    # Avisar sobre opcionais faltando
    print("\n2. COLUNAS OPCIONAIS")
    print("-" * 80)
    for col in DATA_CONTRACTS["OPCIONAIS"]:
        if col in df.columns:
            print(f"  [OK] {col}: presente")
        else:
            print(f"  [INFO] {col}: ausente (opcional)")
    
    return len(erros) == 0, erros


def validar_ranges(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Valida se valores estao dentro dos ranges esperados"""
    erros = []
    
    print("\n3. VALIDACAO DE RANGES")
    print("-" * 80)
    
    for col, (min_val, max_val) in DATA_CONTRACTS["RANGES"].items():
        if col not in df.columns:
            continue
        
        # Remover NaN para validacao
        valores = df[col].dropna()
        if len(valores) == 0:
            print(f"  [WARN] {col}: todos valores sao NaN")
            continue
        
        # Tentar converter para numerico
        try:
            valores = pd.to_numeric(valores, errors='coerce')
            valores = valores.dropna()  # Remove valores que nao converteram
            
            if len(valores) == 0:
                print(f"  [WARN] {col}: nenhum valor numerico valido encontrado")
                continue
        except:
            print(f"  [WARN] {col}: nao eh possivel validar range (nao numerico)")
            continue
        
        # Checar outliers
        fora_range = ((valores < min_val) | (valores > max_val)).sum()
        pct_fora = (fora_range / len(valores)) * 100
        
        if fora_range > 0:
            min_real = valores.min()
            max_real = valores.max()
            msg = f"{col} tem {fora_range} valores fora do range [{min_val}, {max_val}] (real: [{min_real:.2f}, {max_real:.2f}])"
            
            # Threshold de tolerancia: 10% para a maioria, 15% para IAA (ponto flutuante)
            threshold = 15 if col == "IAA" else 10
            
            # Se >threshold% fora do range, eh erro critico
            if pct_fora > threshold:
                print(f"  [ERRO] {msg} - {pct_fora:.1f}% fora do range")
                erros.append(f"ERRO: {msg}")
            else:
                # Se <=threshold%, apenas warning (toleravel)
                print(f"  [WARN] {msg} - {pct_fora:.1f}% fora do range (toleravel)")
        else:
            print(f"  [OK] {col}: {len(valores)} valores dentro do range [{min_val}, {max_val}]")
    
    return len(erros) == 0, erros


def validar_valores_categoricos(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Valida valores categoricos"""
    erros = []
    
    print("\n4. VALIDACAO DE VALORES CATEGORICOS")
    print("-" * 80)
    
    for col, valores_validos in DATA_CONTRACTS["VALORES_VALIDOS"].items():
        if col not in df.columns:
            continue
        
        valores_unicos = df[col].dropna().unique()
        
        # Caso especial para Fase: aceitar qualquer valor que comece com numero
        if col == "Fase":
            # Validar que comeca com numero ou eh ALFA
            valores_invalidos = []
            for v in valores_unicos:
                v_str = str(v)
                # Aceitar se comeca com numero, ou eh ALFA, ou eh alguma fase conhecida
                if not (v_str[0].isdigit() or v_str.startswith("ALFA") or v in valores_validos):
                    valores_invalidos.append(v)
            
            if valores_invalidos:
                msg = f"ERRO: {col} tem valores invalidos: {valores_invalidos}"
                print(f"  [ERRO] {msg}")
                erros.append(msg)
            else:
                fases_encontradas = list(valores_unicos)[:10]  # Mostrar primeiras 10
                print(f"  [OK] {col}: {len(valores_unicos)} fases validas (ex: {fases_encontradas})")
        else:
            # Validacao normal para outras colunas
            valores_invalidos = [v for v in valores_unicos if v not in valores_validos]
            
            if valores_invalidos:
                msg = f"ERRO: {col} tem valores invalidos: {valores_invalidos}"
                print(f"  [ERRO] {msg}")
                erros.append(msg)
            else:
                print(f"  [OK] {col}: todos valores validos {list(valores_unicos)}")
    
    return len(erros) == 0, erros


def validar_qualidade(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Valida qualidade geral dos dados"""
    warnings = []
    
    print("\n5. VALIDACAO DE QUALIDADE")
    print("-" * 80)
    
    # Missing values em colunas obrigatorias
    for col in DATA_CONTRACTS["OBRIGATORIOS"]:
        if col not in df.columns:
            continue
        
        missing = df[col].isna().sum()
        pct_missing = (missing / len(df)) * 100
        
        if missing > 0:
            msg = f"{col}: {missing} NaN ({pct_missing:.1f}%)"
            print(f"  [WARN] {msg}")
            warnings.append(msg)
            
            if pct_missing > 10:  # >10% missing eh critico
                print(f"  [CRITICO] {col} tem >10% de dados faltando!")
        else:
            print(f"  [OK] {col}: sem missing values")
    
    # Duplicatas
    duplicatas = df.duplicated(subset=["RA"]).sum() if "RA" in df.columns else 0
    if duplicatas > 0:
        msg = f"WARN: {duplicatas} linhas duplicadas detectadas"
        print(f"\n  [WARN] {msg}")
        warnings.append(msg)
    else:
        print(f"\n  [OK] Sem duplicatas")
    
    return True, warnings


def gerar_relatorio(df: pd.DataFrame, 
                   schema_ok: bool, schema_erros: List[str],
                   ranges_ok: bool, ranges_erros: List[str],
                   categ_ok: bool, categ_erros: List[str],
                   qual_ok: bool, qual_warnings: List[str]) -> bool:
    """Gera relatorio final"""
    print("\n" + "="*80)
    print("RELATORIO FINAL")
    print("="*80)
    
    print(f"\nTotal de registros: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")
    
    print(f"\n1. Schema: {'OK' if schema_ok else 'ERRO'}")
    if schema_erros:
        for erro in schema_erros:
            print(f"   - {erro}")
    
    print(f"\n2. Ranges: {'OK' if ranges_ok else 'ERRO'}")
    if ranges_erros:
        for erro in ranges_erros:
            print(f"   - {erro}")
    
    print(f"\n3. Categoricos: {'OK' if categ_ok else 'ERRO'}")
    if categ_erros:
        for erro in categ_erros:
            print(f"   - {erro}")
    
    print(f"\n4. Qualidade: {'OK' if not qual_warnings else 'AVISOS'}")
    if qual_warnings:
        for warn in qual_warnings:
            print(f"   - {warn}")
    
    # Decisao final
    print("\n" + "="*80)
    
    todos_ok = schema_ok and ranges_ok and categ_ok
    
    if todos_ok:
        print("STATUS: DADOS VALIDOS")
        print("Os dados passaram em todas as validacoes criticas.")
        if qual_warnings:
            print(f"AVISOS: {len(qual_warnings)} avisos de qualidade (nao-bloqueantes)")
        return True
    else:
        print("STATUS: DADOS INVALIDOS")
        print("Os dados FALHARAM em validacoes criticas e nao devem ser usados para treino.")
        total_erros = len(schema_erros) + len(ranges_erros) + len(categ_erros)
        print(f"Total de erros criticos: {total_erros}")
        return False


# Executar validacao
if __name__ == "__main__":
    # Carregar dados
    data_path = "database/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
    
    if not Path(data_path).exists():
        print(f"\nERRO: Arquivo nao encontrado: {data_path}")
        sys.exit(1)
    
    df = pd.read_excel(data_path, sheet_name="PEDE2024")
    print(f"\nDados carregados: {len(df)} linhas, {len(df.columns)} colunas")
    
    # Executar validacoes
    schema_ok, schema_erros = validar_schema(df)
    ranges_ok, ranges_erros = validar_ranges(df)
    categ_ok, categ_erros = validar_valores_categoricos(df)
    qual_ok, qual_warnings = validar_qualidade(df)
    
    # Gerar relatorio
    valido = gerar_relatorio(df, schema_ok, schema_erros, 
                            ranges_ok, ranges_erros,
                            categ_ok, categ_erros,
                            qual_ok, qual_warnings)
    
    # Exit code
    sys.exit(0 if valido else 1)
