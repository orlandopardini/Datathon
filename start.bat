@echo off
title Passos Magicos - MLOps Platform
color 0A
cls

:MENU
echo.
echo ========================================
echo    PASSOS MAGICOS - MLOps Platform
echo ========================================
echo.
echo   Selecione uma opcao:
echo.
echo   [1] Setup Inicial (primeira vez)
echo   [2] Treinar Modelo
echo   [3] Executar Testes
echo   [4] Iniciar Dashboard
echo   [5] Iniciar com Monitoramento
echo   [0] Sair
echo.
echo ========================================
echo.

set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" goto SETUP
if "%opcao%"=="2" goto TRAIN
if "%opcao%"=="3" goto TEST
if "%opcao%"=="4" goto RUN
if "%opcao%"=="5" goto MONITOR
if "%opcao%"=="0" goto EXIT

echo.
echo Opcao invalida! Tente novamente.
timeout /t 2 >nul
cls
goto MENU

:SETUP
cls
echo.
echo ========================================
echo   EXECUTANDO: Setup Inicial
echo ========================================
echo.
call procedures\setup.bat
pause
cls
goto MENU

:TRAIN
cls
echo.
echo ========================================
echo   EXECUTANDO: Treinamento do Modelo
echo ========================================
echo.
call procedures\train.bat
pause
cls
goto MENU

:TEST
cls
echo.
echo ========================================
echo   EXECUTANDO: Testes
echo ========================================
echo.
call procedures\test.bat
pause
cls
goto MENU

:RUN
cls
echo.
echo ========================================
echo   EXECUTANDO: Dashboard Principal
echo ========================================
echo.
call procedures\run.bat
pause
cls
goto MENU

:MONITOR
cls
echo.
echo ========================================
echo   EXECUTANDO: Dashboard com Monitoramento
echo ========================================
echo.
call procedures\run-with-monitoring.bat
pause
cls
goto MENU

:EXIT
cls
echo.
echo Encerrando...
echo.
timeout /t 1 >nul
exit
