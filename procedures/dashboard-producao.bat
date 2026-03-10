@echo off
echo ================================================================================
echo DASHBOARD DE PRODUCAO - METRICAS DE NEGOCIO
echo ================================================================================
echo.

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Iniciar dashboard
echo [INFO] Iniciando dashboard de producao...
echo.
echo Acesse: http://localhost:8502
echo.

streamlit run monitoring\producao_dashboard.py --server.port 8502

pause
