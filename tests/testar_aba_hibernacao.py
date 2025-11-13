#!/usr/bin/env python3
"""
🧪 Teste para verificar abas nas planilhas de Hibernação
"""

import sys
import os

# Adicionar diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

from scripts.gerenciador_planilhas import GerenciadorPlanilhas
import gspread
from google.oauth2.service_account import Credentials

def testar_abas():
    """Testa se as abas existem nas planilhas de Hibernação"""
    
    print("="*60)
    print("🧪 TESTE: Verificar Abas Hibernação")
    print("="*60)
    
    # Configurar credenciais
    arquivo_credenciais = os.path.join(root_dir, 'config', 'boletim.json')
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(arquivo_credenciais, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Obter IDs
    gerenciador = GerenciadorPlanilhas()
    
    planilhas = {
        "HIBERNAÇÃO 1º SEM": gerenciador.obter_id('hibernacao_primeiro_semestre'),
        "HIBERNAÇÃO 2º SEM": gerenciador.obter_id('hibernacao_segundo_semestre')
    }
    
    print(f"\n📋 Planilhas a verificar:")
    for nome, planilha_id in planilhas.items():
        print(f"   • {nome}: {planilha_id}")
    
    # Verificar cada planilha
    for nome, planilha_id in planilhas.items():
        print(f"\n" + "="*60)
        print(f"📊 Verificando: {nome}")
        print("="*60)
        
        try:
            # Abrir planilha
            planilha = client.open_by_key(planilha_id)
            print(f"✅ Planilha aberta: {planilha.title}")
            
            # Listar todas as abas
            abas = planilha.worksheets()
            print(f"\n📑 Abas encontradas ({len(abas)}):")
            
            for i, aba in enumerate(abas, 1):
                print(f"   {i}. '{aba.title}'")
            
            # Verificar se existe a aba "BASE"
            aba_esperada = "BASE"
            aba_existe = any(aba.title == aba_esperada for aba in abas)
            
            if aba_existe:
                print(f"\n✅ Aba '{aba_esperada}' ENCONTRADA!")
                
                # Tentar abrir a aba
                try:
                    aba = planilha.worksheet(aba_esperada)
                    print(f"✅ Aba acessível")
                    print(f"   Dimensões: {aba.row_count} linhas x {aba.col_count} colunas")
                except Exception as e:
                    print(f"❌ Erro ao acessar aba: {e}")
            else:
                print(f"\n❌ Aba '{aba_esperada}' NÃO ENCONTRADA!")
                print(f"💡 Possíveis soluções:")
                print(f"   1. Criar aba com nome exato: '{aba_esperada}'")
                print(f"   2. Ou usar uma das abas existentes")
                
        except Exception as e:
            print(f"❌ Erro ao acessar planilha: {e}")
    
    print("\n" + "="*60)
    print("✅ Teste concluído!")
    print("="*60)

if __name__ == '__main__':
    testar_abas()
