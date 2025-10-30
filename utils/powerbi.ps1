# =====================================================
# INTERFACE POWER BI LOOKER STUDIO
# Automação de dados para Power BI
# =====================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "   POWER BI LOOKER STUDIO - LEROY MERLIN" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""

# Executar interface
python interface_powerbi.py

# Verificar erro
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERRO ao executar a interface!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
}
