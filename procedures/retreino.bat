@echo off
echo ================================================================================
echo RETREINO AUTOMATIZADO - MODELO DE EVASAO ESCOLAR
echo ================================================================================
echo.

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Executar retreino
echo [INFO] Iniciando pipeline de retreino...
echo.
python scripts\retreino_automatizado.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo RETREINO CONCLUIDO COM SUCESSO
    echo ================================================================================
    echo.
    echo Proximos passos:
    echo   1. Testar API: start.bat
    echo   2. Validar predicoes manualmente
    echo   3. Deploy em producao
    echo.
) else (
    echo.
    echo ================================================================================
    echo RETREINO FALHOU
    echo ================================================================================
    echo.
    echo Modelo anterior mantido sem alteracoes.
    echo Verifique os logs acima para detalhes.
    echo.
)

pause
