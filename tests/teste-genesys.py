#!/usr/bin/env python3
"""
Teste Específico: Genesys - Processar dados para planilha Genesys
ID: 14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc (Planilha oficial)
"""
import sys
import os

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase

def detectar_tipo_genesys(nome_arquivo):
    """Detecta o tipo do arquivo Genesys baseado no nome"""
    nome_lower = nome_arquivo.lower()
    
    if 'voz' in nome_lower and 'hc' in nome_lower:
        return 'BASE VOZ', 'GENESYS VOZ HC'
    elif 'texto' in nome_lower and 'hc' in nome_lower:
        return 'BASE TEXTO', 'GENESYS TEXTO HC'
    elif 'gestão' in nome_lower or 'gestao' in nome_lower:
        if 'n1' in nome_lower or 'entrega' in nome_lower:
            return 'BASE GE COLABORADOR', 'GENESYS GESTÃO N1'
        else:
            return 'BASE GE COLABORADOR', 'GENESYS GESTÃO'  # Corrigido: era "BASE GE FILA"
    elif 'fila' in nome_lower:
        return 'BASE VOZ FILA', 'GENESYS FILA'
    else:
        return None, None

def main():
    print("🎤 TESTE GENESYS - Processamento de Dados")
    print("=" * 60)
    
    try:
        # ID da planilha Genesys oficial
        id_planilha_genesys = "14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc"
        
        print(f"📊 Planilha Genesys: {id_planilha_genesys}")
        print("🔧 Modo: COMPLEMENTAR (preserva dados existentes)")
        print("📋 Cabeçalho: REMOVIDO automaticamente")
        print()
        
        # Criar instância com o ID da planilha Genesys
        sheets = GoogleSheetsBase(id_planilha=id_planilha_genesys)
        
        print("🔗 Conectando...")
        client = sheets.client
        
        print("📋 Acessando planilha...")
        planilha = client.open_by_key(id_planilha_genesys)
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
            aba_destino, tipo_detectado = detectar_tipo_genesys(arquivo)
            if aba_destino:
                print(f"   📄 {arquivo} → {aba_destino}")
            else:
                print(f"   📄 {arquivo} → [Tipo não identificado para Genesys]")
        print()
        
        # Processar apenas arquivos relevantes para Genesys
        arquivos_genesys = []
        for arquivo in arquivos_csv:
            aba_destino, tipo_detectado = detectar_tipo_genesys(arquivo)
            if aba_destino and aba_destino in abas_disponiveis:
                arquivos_genesys.append((arquivo, aba_destino, tipo_detectado))
        
        if not arquivos_genesys:
            print("⚠️  Nenhum arquivo Genesys encontrado ou abas correspondentes não existem")
            print("\n💡 Para testar, certifique-se de ter arquivos CSV como:")
            print("   - Voz HC.csv")
            print("   - Texto HC.csv")
            print("   - Gestão da entrega N1 HC.csv")
            return
        
        print(f"🎯 Arquivos Genesys identificados: {len(arquivos_genesys)}")
        
        # Processar cada arquivo Genesys
        sucessos = 0
        falhas = 0
        
        for arquivo, aba_destino, tipo_detectado in arquivos_genesys:
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
        print(f"\n🎉 PROCESSAMENTO GENESYS CONCLUÍDO!")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Falhas: {falhas}")
        print(f"📊 Total processado: {sucessos + falhas}")
        
        if sucessos > 0:
            print(f"\n🔗 Acesse a planilha Genesys para ver os dados atualizados:")
            print(f"   https://docs.google.com/spreadsheets/d/{id_planilha_genesys}")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n🔧 VERIFICAÇÕES:")
        print("1. Planilha Genesys foi compartilhada com: boletim@sublime-shift-472919-f0.iam.gserviceaccount.com?")
        print("2. Service Account tem permissão de 'Editor'?")
        print("3. Arquivos CSV com dados Genesys estão na pasta 'data'?")
        print("4. Nomes das abas estão corretos na planilha?")

if __name__ == "__main__":
    main()