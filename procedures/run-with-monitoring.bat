@echo off
echo ========================================
echo   Passos Magicos - ML Dashboard
echo   Com Monitoramento de Drift
echo ========================================
echo.

REM Ativa o ambiente virtual
echo [1/4] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual
    pause
    exit /b 1
)

REM Verifica se o modelo existe
echo [2/4] Verificando modelo treinado...
if not exist "app\model\model.joblib" (
    echo AVISO: Modelo nao encontrado!
    echo Execute o treinamento primeiro.
    pause
    exit /b 1
)

REM Inicia a API em background
echo [3/4] Iniciando API na porta 8000...
start "FastAPI Server" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM Aguarda a API iniciar
timeout /t 5 /nobreak > nul

REM Inicia o Dashboard Streamlit
echo [4/4] Iniciando Dashboard Drift na porta 8501...
echo.
echo ========================================
echo   Dashboard ML:   http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Dashboard Drift: http://localhost:8501
echo ========================================
echo.
echo Abrindo navegadores...
echo Feche esta janela para parar todos os servicos
echo.

REM Aguarda 3 segundos e abre os navegadores
start /b timeout /t 3 /nobreak > nul && start http://localhost:8000
start /b timeout /t 5 /nobreak > nul && start http://localhost:8501

streamlit run monitoring\dashboard.py
