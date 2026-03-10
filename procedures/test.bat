@echo off
echo ========================================
echo   Passos Magicos - Executar Testes
echo ========================================
echo.

REM Ativa o ambiente virtual
echo [1/2] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual
    pause
    exit /b 1
)

REM Executa os testes
echo [2/2] Executando testes com cobertura...
echo.

REM Configuracoes de cobertura em .coveragerc (threshold: 10%%)
REM Cobertura atual: preprocessing.py = 68%% (modulo core testado)
REM TODO: Adicionar testes para feature_engineering, train, evaluate, drift
set PYTHONPATH=%CD%
pytest tests/ -v --cov=src --cov-report=term-missing

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Todos os testes passaram! ^_^
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   Alguns testes falharam!
    echo ========================================
    echo.
)

pause
