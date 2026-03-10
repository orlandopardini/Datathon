@echo off
REM Script de Deploy no Render (Windows)
REM Prepara o projeto para deployment no Render

echo ========================================================================
echo PREPARANDO PROJETO PARA DEPLOY NO RENDER
echo ========================================================================
echo.

REM 1. Verificar se Git esta inicializado
if not exist ".git" (
    echo [INFO] Inicializando repositorio Git...
    git init
    git branch -M main
) else (
    echo [OK] Repositorio Git ja inicializado
)

REM 2. Verificar se modelo existe
if not exist "app\model\model.joblib" (
    echo.
    echo [ATENCAO] Modelo nao encontrado!
    echo Execute primeiro: python src\train.py
    echo.
    set /p confirm="Deseja continuar mesmo assim? (s/N): "
    if /i not "%confirm%"=="s" (
        echo [ERRO] Deploy cancelado
        exit /b 1
    )
) else (
    echo [OK] Modelo encontrado: app\model\model.joblib
)

REM 3. Verificar arquivos essenciais
echo.
echo [INFO] Verificando arquivos essenciais...

if exist "requirements.txt" (echo    [OK] requirements.txt) else (echo    [ERRO] requirements.txt - FALTANDO!)
if exist "render.yaml" (echo    [OK] render.yaml) else (echo    [ERRO] render.yaml - FALTANDO!)
if exist "app\main.py" (echo    [OK] app\main.py) else (echo    [ERRO] app\main.py - FALTANDO!)
if exist "app\routes.py" (echo    [OK] app\routes.py) else (echo    [ERRO] app\routes.py - FALTANDO!)

REM 4. Commit
echo.
echo [INFO] Preparando commit...
git add .
git status

echo.
set /p do_commit="Fazer commit das alteracoes? (S/n): "
if /i not "%do_commit%"=="n" (
    set /p commit_msg="Mensagem do commit: "
    if "%commit_msg%"=="" set commit_msg=Deploy: API v3.0 - Risco de Evasao
    
    git commit -m "%commit_msg%"
    echo    [OK] Commit realizado
)

REM 5. Instrucoes finais
echo.
echo ========================================================================
echo PREPARACAO CONCLUIDA!
echo ========================================================================
echo.
echo Proximos passos:
echo.
echo 1. Criar repositorio no GitHub:
echo    https://github.com/new
echo.
echo 2. Adicionar remote (substitua SEU_USUARIO):
echo    git remote add origin https://github.com/SEU_USUARIO/passos-magicos-evasao-api.git
echo.
echo 3. Push para GitHub:
echo    git push -u origin main
echo.
echo 4. Deploy no Render:
echo    - Acesse: https://dashboard.render.com
echo    - New -^> Web Service
echo    - Connect GitHub repository
echo    - Render lera automaticamente render.yaml
echo.
echo Documentacao completa:
echo    docs_contexto\DEPLOY_RENDER.md
echo.
echo URL da API apos deploy:
echo    https://passos-magicos-evasao-api.onrender.com
echo.
echo ========================================================================

pause
