@echo off
title I e M Informatica - Testar site (versao estatica)
cd /d "%~dp0"

echo ============================================================
echo   I e M INFORMATICA - Testando o site localmente
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado no seu computador.
    echo Baixe em: https://www.python.org/downloads/
    echo IMPORTANTE: na instalacao, marque "Add Python to PATH".
    pause
    exit /b 1
)

echo Abrindo o navegador em http://localhost:8000 ...
start "" cmd /c "timeout /t 3 >nul & start http://localhost:8000"

echo.
echo O site esta rodando em: http://localhost:8000
echo Para PARAR, feche esta janela ou pressione CTRL+C.
echo.
python -m http.server 8000

pause
