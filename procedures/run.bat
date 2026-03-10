@echo off
echo ========================================
echo   Passos Magicos - ML Dashboard
echo   Iniciando aplicacao localmente...
echo ========================================
echo.

REM Ativa o ambiente virtual
echo [1/3] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual
    echo Execute primeiro: python -m venv .venv
    pause
    exit /b 1
)

REM Verifica se o modelo existe
echo [2/3] Verificando modelo treinado...
if not exist "app\model\model.joblib" (
    echo.
    echo AVISO: Modelo nao encontrado!
    echo Execute o treinamento primeiro:
    echo   python -m src.train --data-path "caminho\do\arquivo.xlsx" --sheet "PEDE2024"
    echo.
    pause
    exit /b 1
)

REM Inicia a API
echo [3/3] Iniciando API na porta 8000...
echo.
echo ========================================
echo   Dashboard: http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo ========================================
echo.
echo Abrindo navegador...
echo Pressione Ctrl+C para parar o servidor
echo.

REM Aguarda 3 segundos e abre o navegador
start /b timeout /t 3 /nobreak > nul && start http://localhost:8000

uvicorn app.main:app --host 0.0.0.0 --port 8000
