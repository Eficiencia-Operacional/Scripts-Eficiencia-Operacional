#!/usr/bin/env python3
"""
Teste Específico: Salesforce - Processar dados para planilha Salesforce
URL: https://docs.google.com/spreadsheets/d/1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0 (Planilha oficial)
"""
import sys
import os

# Adicionar o diretório core ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase

def detectar_tipo_salesforce(nome_arquivo):
    """Detecta o tipo do arquivo Salesforce baseado no nome"""
    nome_lower = nome_arquivo.lower()
    
    if 'criado' in nome_lower or 'created' in nome_lower:
        return 'BASE ATUALIZADA CORRETA - CRIADO', 'SALESFORCE CRIADO'
    elif 'resolvido' in nome_lower or 'resolved' in nome_lower:
        return 'BASE ATUALIZADA CORRETA - RESOLVIDA', 'SALESFORCE RESOLVIDO'
    elif 'comentario' in nome_lower or 'comment' in nome_lower or 'bko' in nome_lower:
        return 'COMENTARIO BKO', 'SALESFORCE COMENTÁRIOS'
    elif 'seller' in nome_lower or 'vendedor' in nome_lower:
        return 'DADOS SELLER', 'SALESFORCE SELLER'
    elif 'boletim' in nome_lower and 'criado' in nome_lower:
        return 'BASE ATUALIZADA CORRETA - CRIADO', 'BOLETIM CRIADO'
    else:
        return None, None

def main():
    print("🔄 TESTE SALESFORCE - Processamento de Dados")
    print("=" * 60)
    
    try:
        # ID da planilha Salesforce oficial
        id_planilha_salesforce = "1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0"
        
        print(f"📊 Planilha Salesforce: {id_planilha_salesforce}")
        print("🔧 Modo: COMPLEMENTAR (preserva dados existentes)")
        print("📋 Cabeçalho: REMOVIDO automaticamente")
        print()
        
        # Criar instância com a planilha Salesforce
        sheets = GoogleSheetsBase(id_planilha=id_planilha_salesforce)
        
        print("🔗 Conectando...")
        client = sheets.client
        
        print("📋 Acessando planilha...")
        planilha = client.open_by_key(id_planilha_salesforce)
        print(f"✅ Planilha: '{planilha.title}'")
        
        # Listar abas disponíveis
        abas_disponiveis = [aba.title for aba in planilha.worksheets()]
        print(f"📑 Abas disponíveis:")
        for i, aba in enumerate(abas_disponiveis, 1):
            print(f"   {i}. {aba}")
        print()
        
        # Buscar arquivos CSV na pasta data
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        arquivos_csv = []
        
        if os.path.exists(data_dir):
            for arquivo in os.listdir(data_dir):
                if arquivo.lower().endswith('.csv'):
                    arquivos_csv.append(arquivo)
        
        print(f"📁 Arquivos CSV encontrados na pasta data: {len(arquivos_csv)}")
        for arquivo in arquivos_csv:
            aba_destino, tipo_detectado = detectar_tipo_salesforce(arquivo)
            if aba_destino:
                print(f"   📄 {arquivo} → {aba_destino}")
            else:
                print(f"   📄 {arquivo} → [Tipo não identificado para Salesforce]")
        print()
        
        # Processar apenas arquivos relevantes para Salesforce
        arquivos_salesforce = []
        for arquivo in arquivos_csv:
            aba_destino, tipo_detectado = detectar_tipo_salesforce(arquivo)
            if aba_destino and aba_destino in abas_disponiveis:
                arquivos_salesforce.append((arquivo, aba_destino, tipo_detectado))
        
        if not arquivos_salesforce:
            print("⚠️  Nenhum arquivo Salesforce encontrado ou abas correspondentes não existem")
            print("\n💡 Para testar, adicione arquivos CSV com nomes como:")
            print("   - BASE - BOLETIM - CRIADO-2025-09-23.csv")
            print("   - dados_resolvidos.csv")
            print("   - comentarios_bko.csv")
            print("   - dados_seller.csv")
            return
        
        print(f"🎯 Arquivos Salesforce identificados: {len(arquivos_salesforce)}")
        
        # Processar cada arquivo Salesforce
        sucessos = 0
        falhas = 0
        
        for arquivo, aba_destino, tipo_detectado in arquivos_salesforce:
            print(f"\n📤 Processando: {arquivo}")
            print(f"🎯 Tipo detectado: {tipo_detectado}")
            print(f"📝 Destino: {aba_destino}")
            
            # Verificar dados existentes na aba
            aba = planilha.worksheet(aba_destino)
            valores_existentes = aba.get_all_values()
            linhas_com_dados = sum(1 for linha in valores_existentes if any(cell.strip() for cell in linha))
            print(f"📊 Dados existentes: {linhas_com_dados} linhas")
            
            # Enviar arquivo
            resultado = sheets.enviar_csv_para_planilha(arquivo, aba_destino)
            
            if resultado:
                print(f"✅ {arquivo} → {aba_destino} - SUCESSO!")
                sucessos += 1
            else:
                print(f"❌ {arquivo} → {aba_destino} - FALHA!")
                falhas += 1
            
            print("-" * 50)
        
        # Relatório final
        print(f"\n🎉 PROCESSAMENTO SALESFORCE CONCLUÍDO!")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Falhas: {falhas}")
        print(f"📊 Total processado: {sucessos + falhas}")
        
        if sucessos > 0:
            print(f"\n🔗 Acesse a planilha Salesforce para ver os dados atualizados:")
            print(f"   https://docs.google.com/spreadsheets/d/{id_planilha_salesforce}")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n🔧 VERIFICAÇÕES:")
        print("1. Planilha Salesforce foi compartilhada com: boletim@sublime-shift-472919-f0.iam.gserviceaccount.com?")
        print("2. Service Account tem permissão de 'Editor'?")
        print("3. Arquivos CSV com dados Salesforce estão na pasta 'data'?")
        print("4. Nomes das abas estão corretos na planilha?")

if __name__ == "__main__":
    main()