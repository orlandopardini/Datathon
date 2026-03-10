@echo off
echo ========================================
echo   Passos Magicos - Treinamento do Modelo
echo ========================================
echo.

REM Ativa o ambiente virtual
echo [1/2] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual
    echo Execute primeiro: python -m venv .venv
    pause
    exit /b 1
)

REM Executa o treinamento (caminho padrão: database\BASE DE DADOS PEDE 2024 - DATATHON.xlsx)
echo [2/2] Iniciando treinamento do modelo...
echo.

REM Se quiser usar outro arquivo, adicione: --data-path "caminho\seu_arquivo.xlsx"
python -m src.train

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Treinamento concluido com sucesso!
    echo   Artefatos salvos em: app\model\
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo   ERRO no treinamento!
    echo   Verifique se o arquivo esta em: database\BASE DE DADOS PEDE 2024 - DATATHON.xlsx
    echo ========================================
    echo.
)

pause
