import sys
import os

# Adicionar o diretório src ao path para imports funcionarem tanto no main.py quanto em testes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.google_sheets_base import GoogleSheetsBase

class Produtividade(GoogleSheetsBase):
    """Processador especializado para arquivos de produtividade"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            # ID da planilha oficial de Produtividade ATUALIZADO
            super().__init__(id_planilha="1XftLATi3eAQXYAk0Em1SY5tMisOBra8kkViFBEjEem0")
        self.NOME_ABAS = {
            "produtividade": "BASE PROD", 
            "tempo": "BASE TEMPO"
        }

        # Padrões de arquivos - nomes renomeados dos CSVs
        self.PADROES_ARQUIVOS = {
            "produtividade": "BASE_PRODUTIVIDADE.csv",  # Nome renomeado
            "tempo": "BASE_TEMPO.csv"                    # Nome renomeado
        }
    
    def processar_produtividade(self, caminho_csv=None):
        """Processa base de produtividade (Base - Visão Produtiva)"""
        if caminho_csv is None:
            caminho_csv = self.PADROES_ARQUIVOS['produtividade']
        
        resultado = self.enviar_csv_para_planilha(
            caminho_csv,
            self.NOME_ABAS["produtividade"]
        )
        
        return resultado.get('sucesso', False)
    
    def processar_tempo(self, caminho_csv=None):
        """Processa base de tempo (Base tempo - Visão Produtiva)"""
        if caminho_csv is None:
            caminho_csv = self.PADROES_ARQUIVOS['tempo']
        
        resultado = self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["tempo"]
        )
        
        return resultado.get('sucesso', False)
    
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