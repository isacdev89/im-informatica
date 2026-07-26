@echo off
setlocal enabledelayedexpansion
title I e M Informatica - Publicar no GitHub
cd /d "%~dp0"

echo ============================================================
echo   I e M INFORMATICA - Enviar o codigo para o GitHub
echo ============================================================
echo.
echo Este script envia esta pasta para um repositorio no GitHub.
echo Depois disso, voce usa esse repositorio para publicar o site
echo de graca no GitHub Pages (site estatico) e/ou no Render
echo (versao completa com banco de dados).
echo.
echo ANTES DE CONTINUAR, voce precisa ter:
echo   1) Uma conta no GitHub (gratis): https://github.com/join
echo   2) O Git instalado neste computador: https://git-scm.com/downloads
echo   3) Um repositorio VAZIO ja criado no GitHub (botao "New repository")
echo.
pause

where git >nul 2>nul
if errorlevel 1 (
    echo.
    echo [ERRO] O Git nao foi encontrado neste computador.
    echo Baixe e instale em: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

set /p REPO_URL="Cole aqui o link do seu repositorio no GitHub (ex: https://github.com/seuusuario/im-informatica.git) e pressione ENTER: "

if "%REPO_URL%"=="" (
    echo.
    echo Nenhum link foi informado. Cancelando.
    pause
    exit /b 1
)

if not exist ".git\" (
    echo.
    echo [1/5] Iniciando repositorio Git local...
    git init
    git branch -M main
) else (
    echo.
    echo [1/5] Repositorio Git ja existe, pulando esta etapa.
)

echo [2/5] Selecionando os arquivos...
git add .

echo [3/5] Criando o registro (commit)...
git commit -m "Site I e M Informatica" >nul 2>nul

echo [4/5] Configurando o endereco do GitHub...
git remote remove origin >nul 2>nul
git remote add origin "%REPO_URL%"

echo [5/5] Enviando os arquivos para o GitHub...
echo (uma janela do navegador/GitHub pode abrir pedindo seu login)
git push -u origin main

echo.
echo ============================================================
echo   Pronto! Confira seu repositorio em:
echo   %REPO_URL%
echo.
echo   Proximo passo: siga o arquivo COMO_PUBLICAR_GRATIS.md
echo   para deixar o site no ar de graca.
echo ============================================================
echo.
pause
