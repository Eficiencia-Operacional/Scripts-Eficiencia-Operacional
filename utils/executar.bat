@echo off
REM 🚀 AUTOMAÇÃO LEROY MERLIN - SCRIPT DE EXECUÇÃO RÁPIDA
REM Execute este arquivo para rodar a automação completa

echo.
echo =================================================================
echo  🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN - EXECUÇÃO RÁPIDA
echo =================================================================
echo.

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.8+ primeiro
    pause
    exit /b 1
)

REM Mudar para o diretório do script
cd /d "%~dp0"
echo 📁 Diretório atual: %CD%
echo.

REM Verificar se requirements.txt existe
if not exist "config\requirements.txt" (
    echo ❌ Arquivo config\requirements.txt não encontrado!
    pause
    exit /b 1
)

echo 🔧 Instalando dependências...
pip install -r config\requirements.txt

echo.
echo 🚀 Iniciando automação...
echo.

REM Executar o script principal
python main.py

echo.
echo ✅ Automação concluída!
pause

