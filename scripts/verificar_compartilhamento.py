#!/usr/bin/env python3
"""
🔍 VERIFICADOR DE COMPARTILHAMENTO
Verifica se as planilhas estão compartilhadas corretamente
"""

import sys
sys.path.insert(0, 'src')

from src.core.google_sheets_base import GoogleSheetsBase

print("="*60)
print("🔍 VERIFICANDO COMPARTILHAMENTO DAS PLANILHAS")
print("="*60)

planilhas = {
    'Primeiro Semestre': '1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc',
    'Segundo Semestre': '1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8'
}

base = GoogleSheetsBase('config/boletim.json')

for nome, planilha_id in planilhas.items():
    print(f"\n📊 Testando: {nome}")
    print(f"   ID: {planilha_id}")
    
    try:
        planilha = base.client.open_by_key(planilha_id)
        print(f"   ✅ Acesso OK!")
        print(f"   📄 Título: {planilha.title}")
        
        # Listar abas
        abas = [ws.title for ws in planilha.worksheets()]
        print(f"   📑 Abas: {', '.join(abas)}")
        
        # Verificar se tem aba BASE
        if 'BASE' in abas:
            print(f"   ✅ Aba 'BASE' encontrada")
        else:
            print(f"   ⚠️  Aba 'BASE' não encontrada - precisa criar")
            
    except Exception as e:
        erro = str(e)
        if '404' in erro:
            print(f"   ❌ PLANILHA NÃO COMPARTILHADA!")
            print(f"   📧 Compartilhe com: boletim-315@sublime-shift-472919-f0.iam.gserviceaccount.com")
            print(f"   🔗 Link: https://docs.google.com/spreadsheets/d/{planilha_id}")
        else:
            print(f"   ❌ Erro: {erro}")

print("\n" + "="*60)
print("📋 INSTRUÇÕES PARA COMPARTILHAR")
print("="*60)
print("\n1. Abra cada planilha no navegador")
print("2. Clique em 'Compartilhar' (canto superior direito)")
print("3. Adicione este email:")
print("   📧 boletim-315@sublime-shift-472919-f0.iam.gserviceaccount.com")
print("4. Selecione 'Editor' nas permissões")
print("5. Desmarque 'Notificar pessoas' (opcional)")
print("6. Clique em 'Compartilhar' ou 'Enviar'")
print("\n🔗 Links das planilhas:")
for nome, planilha_id in planilhas.items():
    print(f"   • {nome}:")
    print(f"     https://docs.google.com/spreadsheets/d/{planilha_id}")
print("="*60)
