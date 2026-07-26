@echo off
setlocal enabledelayedexpansion
title I e M Informatica - Instalar e Rodar
cd /d "%~dp0"

echo ============================================================
echo   I e M INFORMATICA - Instalador automatico (Windows)
echo ============================================================
echo.

REM ---------- 1) verificar se o Python esta instalado ----------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado no seu computador.
    echo.
    echo Baixe e instale o Python em: https://www.python.org/downloads/
    echo IMPORTANTE: na instalacao, marque a opcao "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

REM ---------- 2) criar o ambiente virtual (venv), se nao existir ----------
if not exist "venv\" (
    echo [1/4] Criando ambiente virtual...
    python -m venv venv
) else (
    echo [1/4] Ambiente virtual ja existe, pulando esta etapa.
)

REM ---------- 3) instalar as dependencias ----------
echo [2/4] Instalando dependencias (isso pode levar alguns minutos)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar as dependencias. Verifique sua internet e tente novamente.
    pause
    exit /b 1
)

REM ---------- 4) abrir o navegador automaticamente ----------
echo [3/4] Abrindo o navegador em http://localhost:5000 ...
start "" cmd /c "timeout /t 4 >nul & start http://localhost:5000"

REM ---------- 5) iniciar o servidor ----------
echo [4/4] Iniciando o site...
echo.
echo ============================================================
echo   O site esta rodando em: http://localhost:5000
echo   Painel administrativo:  http://localhost:5000/admin/login
echo   Usuario: admin   Senha: im@admin123
echo.
echo   Para PARAR o site, feche esta janela ou pressione CTRL+C.
echo ============================================================
echo.
python app.py

pause
