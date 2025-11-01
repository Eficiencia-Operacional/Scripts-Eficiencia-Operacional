#!/usr/bin/env python3
"""
Teste Específico: Enviar VOZ HC.csv para BASE VOZ
Complementa dados existentes sem excluir e remove cabeçalho
"""
import sys
import os

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase

def main():
    print("🎯 TESTE MELHORADO: COMPLEMENTAR DADOS VOZ HC")
    print("=" * 60)
    
    try:
        # ID da planilha oficial Genesys
        id_planilha = "14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc"
        
        print(f"📊 Planilha: {id_planilha}")
        print("📂 Arquivo: VOZ HC.csv")
        print("📝 Destino: ABA 'BASE VOZ'")
        print("🔧 Modo: COMPLEMENTAR (não excluir dados existentes)")
        print("📋 Cabeçalho: REMOVIDO automaticamente")
        print()
        
        # Criar instância com a planilha específica
        sheets = GoogleSheetsBase(id_planilha=id_planilha)
        
        print("🔗 Conectando...")
        client = sheets.client
        
        print("📋 Acessando planilha...")
        planilha = client.open_by_key(id_planilha)
        print(f"✅ Planilha: '{planilha.title}'")
        
        # Verificar se a aba BASE VOZ existe
        abas = [aba.title for aba in planilha.worksheets()]
        if "BASE VOZ" not in abas:
            print("❌ Aba 'BASE VOZ' não encontrada!")
            print(f"📑 Abas disponíveis: {abas}")
            return
        
        print("✅ Aba 'BASE VOZ' encontrada")
        
        # Verificar dados existentes
        aba_voz = planilha.worksheet("BASE VOZ")
        valores_existentes = aba_voz.get_all_values()
        linhas_com_dados = sum(1 for linha in valores_existentes if any(cell.strip() for cell in linha))
        print(f"📊 Dados existentes: {linhas_com_dados} linhas")
        
        # Buscar arquivo VOZ HC
        arquivos_voz = []
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        if os.path.exists(data_dir):
            for arquivo in os.listdir(data_dir):
                if 'VOZ' in arquivo.upper() and 'HC' in arquivo.upper() and arquivo.lower().endswith('.csv'):
                    arquivos_voz.append(arquivo)
        
        if not arquivos_voz:
            print(f"❌ Nenhum arquivo VOZ HC.csv encontrado na pasta {data_dir}")
            print("💡 Arquivos esperados: VOZ HC.csv, VOZ HC (1).csv, etc.")
            return
        
        print(f"📁 Arquivos VOZ HC encontrados: {arquivos_voz}")
        arquivo_escolhido = arquivos_voz[0]  # Usar o primeiro encontrado
        
        # Enviar o arquivo CSV
        print(f"\n📤 Enviando {arquivo_escolhido}...")
        resultado = sheets.enviar_csv_para_planilha(arquivo_escolhido, "BASE VOZ")
        
        if resultado:
            print("🎉 SUCESSO! Dados complementados na BASE VOZ")
            print("✅ Dados existentes preservados")
            print("✅ Cabeçalho removido automaticamente")
            print("✅ Novos dados adicionados após os existentes")
            print("\n🔗 Acesse a planilha para ver os dados atualizados")
        else:
            print("❌ Falha ao enviar arquivo")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n🔧 VERIFICAÇÕES:")
        print("1. Arquivo 'VOZ HC.csv' existe na pasta 'dados'?")
        print("2. Planilha foi compartilhada com: boletim@sublime-shift-472919-f0.iam.gserviceaccount.com?")
        print("3. Service Account tem permissão de 'Editor'?")

if __name__ == "__main__":
    main()