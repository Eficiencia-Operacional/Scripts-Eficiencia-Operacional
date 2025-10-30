#!/usr/bin/env python3
"""
📋 LISTAR PLANILHAS
Lista todas as planilhas acessíveis pela service account
"""

import gspread
from google.oauth2.service_account import Credentials

print("="*60)
print("📋 LISTANDO PLANILHAS ACESSÍVEIS")
print("="*60)

try:
    # Carregar credenciais
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file('config/boletim.json', scopes=scopes)
    client = gspread.authorize(creds)
    
    print("\n🔍 Buscando planilhas...")
    planilhas = client.openall()
    
    print(f"\n✅ Total: {len(planilhas)} planilhas acessíveis\n")
    
    for i, p in enumerate(planilhas, 1):
        print(f"{i}. 📊 {p.title}")
        print(f"   ID: {p.id}")
        print(f"   Link: https://docs.google.com/spreadsheets/d/{p.id}")
        print()
    
    # Verificar se as planilhas do Power BI estão na lista
    print("\n" + "="*60)
    print("🔍 VERIFICANDO PLANILHAS DO POWER BI")
    print("="*60)
    
    ids_esperados = {
        'Primeiro Semestre': '1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc',
        'Segundo Semestre': '1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8'
    }
    
    ids_encontrados = [p.id for p in planilhas]
    
    for nome, id_esperado in ids_esperados.items():
        print(f"\n📊 {nome}:")
        print(f"   ID esperado: {id_esperado}")
        
        if id_esperado in ids_encontrados:
            print(f"   ✅ ENCONTRADA!")
            planilha = next(p for p in planilhas if p.id == id_esperado)
            print(f"   📄 Título real: {planilha.title}")
        else:
            print(f"   ❌ NÃO ENCONTRADA - ID pode estar errado!")
            
            # Procurar por nome similar
            for p in planilhas:
                if 'fila' in p.title.lower() or 'semestre' in p.title.lower():
                    print(f"   💡 Encontrei similar: {p.title}")
                    print(f"      ID: {p.id}")

except Exception as e:
    print(f"\n❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
