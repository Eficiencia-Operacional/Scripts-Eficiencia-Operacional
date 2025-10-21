#!/usr/bin/env python3
"""
TESTE - PROCESSADOR DE PRODUTIVIDADE
Teste isolado para verificar o funcionamento do processador de produtividade
"""

import sys
import os

# Adicionar paths necessários
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')

sys.path.append(src_dir)
sys.path.append(os.path.join(src_dir, 'processadores', 'produtividade'))

def testar_produtividade():
    """Testa o processador de produtividade"""
    try:
        print("🧪 TESTE - PROCESSADOR DE PRODUTIVIDADE")
        print("=" * 50)
        
        # Importar processador
        from processadores.produtividade.produtividade import Produtividade
        
        print("✅ Importação bem sucedida")
        
        # Criar instância
        processador = Produtividade()
        print("✅ Instância criada")
        print(f"📊 ID da planilha: {processador.ID_PLANILHA}")
        print(f"📋 Abas configuradas: {list(processador.NOME_ABAS.keys())}")
        print(f"📁 Padrões de arquivos: {list(processador.PADROES_ARQUIVOS.keys())}")
        
        # Verificar arquivos disponíveis
        data_dir = os.path.join(project_root, 'data')
        if os.path.exists(data_dir):
            arquivos_csv = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
            print(f"\n📂 Arquivos CSV encontrados na pasta data:")
            for arquivo in arquivos_csv:
                print(f"   📄 {arquivo}")
            
            # Verificar se há arquivos de produtividade
            arquivos_produtividade = []
            for arquivo in arquivos_csv:
                arquivo_lower = arquivo.lower()
                if 'produtiv' in arquivo_lower or 'visao' in arquivo_lower or 'tempo' in arquivo_lower:
                    arquivos_produtividade.append(arquivo)
            
            if arquivos_produtividade:
                print(f"\n🎯 Arquivos de produtividade identificados:")
                for arquivo in arquivos_produtividade:
                    print(f"   📈 {arquivo}")
            else:
                print("\n⚠️ Nenhum arquivo de produtividade identificado")
        else:
            print(f"\n⚠️ Pasta 'data' não encontrada: {data_dir}")
        
        print("\n🔧 Testando métodos do processador...")
        
        # Testar localização de arquivos
        try:
            arquivo_prod = processador.encontrar_arquivo_mais_recente(
                processador.PADROES_ARQUIVOS['produtividade'] + ".csv"
            )
            if arquivo_prod:
                print(f"✅ Arquivo produtividade encontrado: {os.path.basename(arquivo_prod)}")
            else:
                print("⚠️ Arquivo de produtividade não encontrado")
        except Exception as e:
            print(f"⚠️ Erro ao buscar arquivo produtividade: {e}")
        
        try:
            arquivo_tempo = processador.encontrar_arquivo_mais_recente(
                processador.PADROES_ARQUIVOS['tempo'] + ".csv"
            )
            if arquivo_tempo:
                print(f"✅ Arquivo tempo encontrado: {os.path.basename(arquivo_tempo)}")
            else:
                print("⚠️ Arquivo de tempo não encontrado")
        except Exception as e:
            print(f"⚠️ Erro ao buscar arquivo tempo: {e}")
        
        print("\n🧪 TESTE CONCLUÍDO COM SUCESSO!")
        print("💡 Para testar o processamento completo, execute:")
        print("   python main.py --produtividade")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se todos os arquivos estão no lugar correto")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_produtividade()
    input("\nPressione Enter para sair...")