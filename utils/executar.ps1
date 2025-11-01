# 🚀 AUTOMAÇÃO LEROY MERLIN - SCRIPT POWERSHELL
# Execute: .\executar.ps1

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Yellow
Write-Host " 🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN - EXECUÇÃO RÁPIDA" -ForegroundColor Yellow  
Write-Host "=================================================================" -ForegroundColor Yellow
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
Write-Host "📁 Diretório atual: $PWD" -ForegroundColor Cyan
Write-Host ""

# Verificar se requirements.txt existe
if (-not (Test-Path "config\requirements.txt")) {
    Write-Host "❌ Arquivo config\requirements.txt não encontrado!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair..."
    exit 1
}

Write-Host "🔧 Instalando dependências..." -ForegroundColor Yellow
pip install -r config\requirements.txt

Write-Host ""
Write-Host "🚀 Iniciando automação..." -ForegroundColor Green
Write-Host ""

# Executar o script principal
python main.py

Write-Host ""
Write-Host "✅ Automação concluída!" -ForegroundColor Green
Read-Host "Pressione Enter para sair..."