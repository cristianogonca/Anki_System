@echo off
echo ====================================
echo  Instalando Gerador de Baralhos Anki
echo ====================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Por favor instale o Python primeiro.
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo ====================================
echo  Instalacao concluida com sucesso!
echo ====================================
echo.
echo Para executar a aplicacao, use:
echo    run.bat
echo.
pause
