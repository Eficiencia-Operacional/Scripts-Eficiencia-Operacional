# 🎨 INTERFACE VISUAL LEROY MERLIN - SCRIPT POWERSHELL
# Execute: .\interface.ps1

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Green
Write-Host " 🎨 INTERFACE VISUAL LEROY MERLIN - CARREGANDO..." -ForegroundColor Green  
Write-Host "=================================================================" -ForegroundColor Green
Write-Host ""

# Verificar se Python está disponível
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado! Instale Python 3.8+ primeiro" -ForegroundColor Red
    Read-Host "Pressione Enter para sair..."
    exit 1
}

# Mudar para o diretório do script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "🔧 Verificando dependências..." -ForegroundColor Yellow
Write-Host ""

# Executar interface visual
Write-Host "🎨 Iniciando interface visual..." -ForegroundColor Green

try {
    python interface_visual.py
    Write-Host ""
    Write-Host "✅ Interface encerrada!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao executar interface. Tentando instalar tkinter..." -ForegroundColor Yellow
    pip install tk
    python interface_visual.py
}

Read-Host "Pressione Enter para sair..."