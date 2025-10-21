import sys
import os

# Adicionar o diretório src ao path para imports funcionarem tanto no main.py quanto em testes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.google_sheets_base import GoogleSheetsBase

class Produtividade(GoogleSheetsBase):
    """Processador especializado para arquivos de produtividade da Genesys"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão do Genesys
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            # ID da planilha oficial do Genesys
            super().__init__(id_planilha="1nzSa4cnPOPau1-BF221Vc6VEvUiFe6D1suebCcQmAT4")
        self.NOME_ABAS = {
            "produtividade": "BASE PROD", 
            "tempo": "BASE TEMPO"
        }

        # Padrões de arquivos baseados nos nomes padronizados pelo renomeador
        self.PADROES_ARQUIVOS = {
            "produtividade": "BASE_PRODUTIVIDADE", 
            "tempo": "BASE_TEMPO"
        }
    
    def processar_produtividade(self, caminho_csv=None):
        """Processa base de produtividade (Base - Visão Produtiva)"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['produtividade']}.csv"
        
        return self.enviar_csv_para_planilha(
            caminho_csv,
            self.NOME_ABAS["produtividade"]
        )
    
    def processar_tempo(self, caminho_csv=None):
        """Processa base de tempo (Base tempo - Visão Produtiva)"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['tempo']}.csv"
        
        return self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["tempo"]
        )
    
    # função para processar todos os csvs 
    def processar_todos(self):
        """Processa todos os arquivos de Produtividade disponíveis"""
        resultados = {}
        
        print("🔄 Processando bases de Produtividade...")
        
        processadores = {
            "Base Produtividade": self.processar_produtividade,
            "Base Tempo": self.processar_tempo
        }

        # função para iterar os processadores 
        for nome, funcao in processadores.items():
            try:
                resultado = funcao()
                resultados[nome] = resultado
                if resultado:
                    print(f"✅ {nome} processado")
                else:
                    print(f"⚠️  {nome} não encontrado")
            except Exception as e:
                print(f"❌ Erro ao processar {nome}: {str(e)}")
                resultados[nome] = False
        
        return resultados