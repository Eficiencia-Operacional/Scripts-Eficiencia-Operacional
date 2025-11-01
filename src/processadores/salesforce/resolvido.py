"""
Processador para base RESOLVIDO do Salesforce
"""
import sys
import os

# Adicionar o diretório src ao path para imports funcionarem tanto no main.py quanto em testes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.google_sheets_base import GoogleSheetsBase

class ProcessadorResolvido(GoogleSheetsBase):
    """Processador para base RESOLVIDO"""
    
    def __init__(self, id_planilha=None):
        # Usar ID específico se fornecido, senão usar padrão
        if id_planilha:
            super().__init__(id_planilha=id_planilha)
        else:
            # ID da planilha oficial do Salesforce ATUALIZADO
            super().__init__(id_planilha="1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk")
        self.NOME_ABA = "BASE ATUALIZADA CORRETA - RESOLVIDA"
        self.PADRAO_ARQUIVO = "BASE-BOLETIM-RESOLVIDO"
        
        # Configuração de fórmulas para BASE ATUALIZADA CORRETA - RESOLVIDA
        self.FORMULAS_CONFIG = [
            {'coluna': 'U', 'formula': '=B{row}'},  # ANALISE_ABERTURA
            {'coluna': 'V', 'formula': '=C{row}'},  # ANALISE_FECHAMENTO
            {'coluna': 'W', 'formula': '=SE(V{row}=""; ""; V{row}-U{row})'},  # TMR
            {'coluna': 'X', 'formula': '=SEERRO(ÍNDICE($Z$2:$Z$3;CORRESP(VERDADEIRO;W{row}<=$AA$2:$AA$3;0));"")'},  # Prazo
            {'coluna': 'Y', 'formula': '=SE(C{row}=""; ""; VALOR(C{row}))'},  # DATA FECHAMENTO
            {'coluna': 'AB', 'formula': '=TEXTO(Y{row};"dd/mm/yyyy")'}  # DATA FECHAMENTO teste
        ]
    
    def processar(self, caminho_csv=None):
        """Processa base RESOLVIDO"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADRAO_ARQUIVO}.csv"
        
        resultado = self.enviar_csv_para_planilha(caminho_csv, self.NOME_ABA)
        
        # Aplicar fórmulas APENAS nas linhas recém-adicionadas (as novas linhas verdes)
        if resultado.get('sucesso') and resultado.get('num_linhas', 0) > 0:
            print(f"🔧 Aplicando fórmulas nas {resultado['num_linhas']} linhas novas da aba {self.NOME_ABA}...")
            self.aplicar_formulas_linhas_novas(
                self.NOME_ABA,
                self.FORMULAS_CONFIG,
                resultado['linha_inicial'],
                resultado['linha_final']
            )
        
        return resultado.get('sucesso', False)