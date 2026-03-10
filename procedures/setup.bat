@echo off
echo ========================================
echo   Passos Magicos - Setup Inicial
echo ========================================
echo.

REM Verifica se Python está instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.11+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version

REM Remove ambiente virtual antigo se existir
if exist ".venv" (
    echo.
    echo [2/5] Removendo ambiente virtual antigo...
    rmdir /s /q .venv
)

REM Cria novo ambiente virtual
echo [3/5] Criando ambiente virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)

REM Ativa o ambiente virtual
echo [4/5] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instala dependências
echo [5/5] Instalando dependencias (isso pode demorar)...
echo.
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic pandas numpy scikit-learn joblib python-multipart pyyaml rich python-dotenv streamlit matplotlib openpyxl pytest pytest-cov httpx

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Setup concluido com sucesso!
    echo.
    echo   Proximos passos:
    echo   1. Execute: train.bat
    echo   2. Execute: run.bat
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   ERRO na instalacao das dependencias!
    echo ========================================
    echo.
)

pause
