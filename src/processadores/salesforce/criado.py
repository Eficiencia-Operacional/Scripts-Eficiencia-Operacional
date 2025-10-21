"""
Processador para base CRIADO do Salesforce
"""
import sys
import os

# Adicionar o diretório src ao path para imports funcionarem tanto no main.py quanto em testes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.google_sheets_base import GoogleSheetsBase

class ProcessadorCriado(GoogleSheetsBase):
    """Processador para base CRIADO"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            # ID da planilha oficial do Salesforce ATUALIZADO
            super().__init__(id_planilha="1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk")
        self.NOME_ABA = "BASE ATUALIZADA CORRETA - CRIADO"
        self.PADRAO_ARQUIVO = "BASE-BOLETIM-CRIADO"
        
        # Sem fórmulas configuradas para esta aba (conforme solicitado)
        self.FORMULAS_CONFIG = []
    
    def processar(self, caminho_csv=None):
        """Processa base CRIADO"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADRAO_ARQUIVO}.csv"
        
        resultado = self.enviar_csv_para_planilha(caminho_csv, self.NOME_ABA)
        
        # Aplicar fórmulas APENAS nas linhas recém-adicionadas (as novas linhas verdes)
        if resultado.get('sucesso') and resultado.get('num_linhas', 0) > 0:
            if self.FORMULAS_CONFIG:
                print(f"🔧 Aplicando fórmulas nas {resultado['num_linhas']} linhas novas da aba {self.NOME_ABA}...")
                self.aplicar_formulas_linhas_novas(
                    self.NOME_ABA,
                    self.FORMULAS_CONFIG,
                    resultado['linha_inicial'],
                    resultado['linha_final']
                )
        
        return resultado.get('sucesso', False)