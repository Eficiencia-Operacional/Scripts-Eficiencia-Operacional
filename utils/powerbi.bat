@echo off
REM =====================================================
REM INTERFACE POWER BI LOOKER STUDIO
REM Automação de dados para Power BI
REM =====================================================

echo.
echo ================================================
echo    POWER BI LOOKER STUDIO - LEROY MERLIN
echo ================================================
echo.

REM Executar interface
python interface_powerbi.py

REM Manter janela aberta em caso de erro
if errorlevel 1 (
    echo.
    echo ERRO ao executar a interface!
    echo.
    pause
)
