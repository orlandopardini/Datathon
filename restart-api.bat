@echo off
echo ============================================================
echo    REINICIANDO API COM MODELO CORRIGIDO
echo ============================================================
echo.

echo 1. Parando processos uvicorn antigos...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 >nul

echo 2. Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo 3. Iniciando API com modelo atualizado...
echo.
echo    API estara disponivel em: http://localhost:8000
echo    Documentacao Swagger: http://localhost:8000/docs
echo.
echo    Pressione CTRL+C para parar a API
echo.
echo ============================================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
