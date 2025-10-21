#!/usr/bin/env python3
"""
Processamento Completo: Enviar todos os CSVs para suas respectivas abas
Detecta automaticamente o tipo de arquivo e envia para a aba correta
"""
import sys
import os

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase

def detectar_tipo_arquivo(nome_arquivo):
    """Detecta o tipo do arquivo baseado no nome"""
    nome_lower = nome_arquivo.lower()
    
    if 'voz' in nome_lower and 'hc' in nome_lower:
        return 'BASE VOZ', 'VOZ HC'
    elif 'texto' in nome_lower and 'hc' in nome_lower:
        return 'BASE TEXTO', 'TEXTO HC'
    elif 'gestão' in nome_lower or 'gestao' in nome_lower:
        if 'n1' in nome_lower:
            return 'BASE GE COLABORADOR', 'GESTÃO N1'  # Corrigido para BASE GE COLABORADOR
        else:
            return 'BASE GE COLABORADOR', 'GESTÃO'
    elif 'fila' in nome_lower:
        return 'BASE GE FILA', 'FILA'
    elif 'colaborador' in nome_lower or 'colab' in nome_lower:
        return 'BASE GE COLABORADOR', 'COLABORADOR'
    else:
        return None, None

def main():
    print("🚀 PROCESSAMENTO COMPLETO - TODOS OS ARQUIVOS CSV")
    print("=" * 70)
    
    try:
        # ID da planilha oficial Genesys
        id_planilha = "14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc"
        
        print(f"📊 Planilha: {id_planilha}")
        print("🔧 Modo: COMPLEMENTAR (preserva dados existentes)")
        print("📋 Cabeçalho: REMOVIDO automaticamente")
        print()
        
        # Criar instância
        sheets = GoogleSheetsBase(id_planilha=id_planilha)
        
        print("🔗 Conectando...")
        client = sheets.client
        
        print("📋 Acessando planilha...")
        planilha = client.open_by_key(id_planilha)
        print(f"✅ Planilha: '{planilha.title}'")
        
        # Listar abas disponíveis
        abas_disponiveis = [aba.title for aba in planilha.worksheets()]
        print(f"📑 Abas disponíveis: {abas_disponiveis}")
        print()
        
        # Buscar arquivos CSV na pasta data
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        arquivos_csv = []
        
        if os.path.exists(data_dir):
            for arquivo in os.listdir(data_dir):
                if arquivo.lower().endswith('.csv'):
                    arquivos_csv.append(arquivo)
        
        if not arquivos_csv:
            print(f"❌ Nenhum arquivo CSV encontrado na pasta {data_dir}")
            return
        
        print(f"📁 Arquivos CSV encontrados: {len(arquivos_csv)}")
        for arquivo in arquivos_csv:
            print(f"   📄 {arquivo}")
        print()
        
        # Processar cada arquivo
        sucessos = 0
        falhas = 0
        
        for arquivo in arquivos_csv:
            print(f"📤 Processando: {arquivo}")
            
            # Detectar tipo e aba de destino
            aba_destino, tipo_detectado = detectar_tipo_arquivo(arquivo)
            
            if not aba_destino:
                print(f"⚠️  Tipo não identificado para: {arquivo} - Pulando...")
                falhas += 1
                continue
            
            if aba_destino not in abas_disponiveis:
                print(f"❌ Aba '{aba_destino}' não existe na planilha - Pulando...")
                falhas += 1
                continue
            
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
        print("\n🎉 PROCESSAMENTO CONCLUÍDO!")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Falhas: {falhas}")
        print(f"📊 Total processado: {sucessos + falhas}")
        
        if sucessos > 0:
            print("\n🔗 Acesse a planilha para ver os dados atualizados")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n🔧 VERIFICAÇÕES:")
        print("1. Arquivos CSV existem na pasta 'data'?")
        print("2. Planilha foi compartilhada com o Service Account?")
        print("3. Service Account tem permissão de 'Editor'?")

if __name__ == "__main__":
    main()