#!/usr/bin/env python3
"""Script para verificar acesso às planilhas Power BI"""

from google.oauth2.service_account import Credentials
import gspread

print("🔐 Verificando acesso às planilhas Power BI...")

# Credenciais
creds = Credentials.from_service_account_file(
    'config/boletim.json',
    scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)

client = gspread.authorize(creds)
print("✅ Conectado ao Google Sheets\n")

# IDs das planilhas
planilhas = {
    'Primeiro Semestre': '1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc',
    'Segundo Semestre': '1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8'
}

print("🔍 Testando acesso às planilhas:")
print("="*70)

for nome, planilha_id in planilhas.items():
    try:
        sheet = client.open_by_key(planilha_id)
        print(f"✅ {nome}")
        print(f"   ID: {planilha_id}")
        print(f"   Nome: {sheet.title}")
        print(f"   URL: https://docs.google.com/spreadsheets/d/{planilha_id}")
        print()
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ {nome}")
        print(f"   ID: {planilha_id}")
        print(f"   Erro: Planilha não encontrada ou sem permissão")
        print(f"   ⚠️  AÇÃO NECESSÁRIA: Compartilhe com boletim@sublime-shift-472919-f0.iam.gserviceaccount.com")
        print(f"   URL: https://docs.google.com/spreadsheets/d/{planilha_id}")
        print()
    except Exception as e:
        print(f"❌ {nome}")
        print(f"   ID: {planilha_id}")
        print(f"   Erro: {type(e).__name__}: {e}")
        print()

print("="*70)
print("📧 Service Account Email:")
print("   boletim@sublime-shift-472919-f0.iam.gserviceaccount.com")
print("\n💡 Como compartilhar:")
print("   1. Abra a planilha no Google Sheets")
print("   2. Clique em 'Compartilhar'")
print("   3. Adicione o email da service account")
print("   4. Defina permissão como 'Editor'")
print("   5. Clique em 'Enviar'")
