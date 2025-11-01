@echo off
REM 🎨 INTERFACE VISUAL LEROY MERLIN - EXECUÇÃO RÁPIDA
REM Execute este arquivo para abrir a interface gráfica

echo.
echo =================================================================
echo  🎨 INTERFACE VISUAL LEROY MERLIN - CARREGANDO...
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

REM Instalar tkinter se necessário (geralmente já vem com Python)
echo 🔧 Verificando dependências...

REM Executar interface visual
echo 🎨 Iniciando interface visual...
python interface_visual.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar interface. Tentando instalar tkinter...
    pip install tk
    python interface_visual.py
)

echo.
echo ✅ Interface encerrada!
pause