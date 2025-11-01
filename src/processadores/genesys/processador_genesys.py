"""
Processador para bases do Genesys
Handles: Gestão da entrega, Texto HC, Voz HC
"""
import sys
import os

# Adicionar o diretório src ao path para imports funcionarem tanto no main.py quanto em testes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Adicionar diretório config ao path
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
config_dir = os.path.join(root_dir, 'config')
sys.path.insert(0, config_dir)

from core.google_sheets_base import GoogleSheetsBase

try:
    from scripts.gerenciador_planilhas import GerenciadorPlanilhas
except ImportError:
    # Fallback se não conseguir importar
    print("⚠️  Gerenciador de planilhas não encontrado, usando configuração padrão")
    GerenciadorPlanilhas = None

class ProcessadorGenesys(GoogleSheetsBase):
    """Processador especializado para arquivos do Genesys"""
    
    def __init__(self, id_planilha=None):
        # Usar gerenciador de configurações se disponível
        if GerenciadorPlanilhas:
            self.gp = GerenciadorPlanilhas()
            
            # Usar ID específico se fornecido, senão usar do gerenciador
            if id_planilha:
                planilha_id = id_planilha
            else:
                planilha_id = self.gp.obter_id("genesys_boletim")
                if not planilha_id:
                    # Fallback para ID hardcoded
                    planilha_id = "1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE"
                    print("⚠️  Usando ID padrão hardcoded para Genesys")
            
            # Obter configurações dinâmicas das abas
            abas_config = self.gp.obter_abas("genesys_boletim")
            
            self.NOME_ABAS = {
                "gestao_entrega": abas_config.get("gestao_entrega", "BASE GE COLABORADOR"),
                "texto": abas_config.get("texto_hc", "BASE TEXTO"), 
                "voz": abas_config.get("voz_hc", "BASE VOZ")
            }
            
            print(f"✅ ProcessadorGenesys configurado com gerenciador:")
            print(f"   📊 ID Planilha: {planilha_id}")
            print(f"   📑 Abas: {self.NOME_ABAS}")
        else:
            # Configuração tradicional hardcoded
            if id_planilha:
                planilha_id = id_planilha
            else:
                planilha_id = "1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE"
            
            self.NOME_ABAS = {
                "gestao_entrega": "BASE GE COLABORADOR",
                "texto": "BASE TEXTO", 
                "voz": "BASE VOZ"
            }
            
            print(f"✅ ProcessadorGenesys configurado (modo tradicional):")
            print(f"   📊 ID Planilha: {planilha_id}")
        
        super().__init__(id_planilha=planilha_id)
        
        # Padrões de arquivos Genesys
        self.PADROES_ARQUIVOS = {
            "gestao_entrega": "Gestão da entrega N1 HC",
            "texto": "Texto HC", 
            "voz": "VOZ HC"  # Corrigido para VOZ HC
        }
        
        # Configuração de fórmulas para cada aba
        # Fórmula TEXT na coluna P para formatar data (coluna C) como DD/M
        self.FORMULAS_CONFIG = {
            "voz": [
                {'coluna': 'P', 'formula': '=TEXT(C{row};"DD/M")'}
            ],
            "texto": [
                {'coluna': 'P', 'formula': '=TEXT(C{row};"DD/M")'}
            ],
            "gestao_entrega": [
                {'coluna': 'P', 'formula': '=TEXT(C{row};"DD/M")'}
            ]
        }
    
    def processar_gestao_entrega(self, caminho_csv=None):
        """Processa base Gestão da Entrega"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['gestao_entrega']}.csv"
        
        resultado = self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["gestao_entrega"]
        )
        
        # Aplicar fórmulas APENAS nas linhas recém-adicionadas (as novas linhas verdes)
        if resultado.get('sucesso') and resultado.get('num_linhas', 0) > 0:
            if self.FORMULAS_CONFIG.get("gestao_entrega"):
                print(f"🔧 Aplicando fórmulas nas {resultado['num_linhas']} linhas novas da aba {self.NOME_ABAS['gestao_entrega']}...")
                self.aplicar_formulas_linhas_novas(
                    self.NOME_ABAS["gestao_entrega"], 
                    self.FORMULAS_CONFIG["gestao_entrega"],
                    resultado['linha_inicial'],
                    resultado['linha_final']
                )
        
        return resultado.get('sucesso', False)
    
    def processar_texto_hc(self, caminho_csv=None):
        """Processa base Texto HC"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['texto']}.csv"
        
        resultado = self.enviar_csv_para_planilha(
            caminho_csv, 
            self.NOME_ABAS["texto"]
        )
        
        # Aplicar fórmulas APENAS nas linhas recém-adicionadas (as novas linhas verdes)
        if resultado.get('sucesso') and resultado.get('num_linhas', 0) > 0:
            if self.FORMULAS_CONFIG.get("texto"):
                print(f"🔧 Aplicando fórmulas nas {resultado['num_linhas']} linhas novas da aba {self.NOME_ABAS['texto']}...")
                self.aplicar_formulas_linhas_novas(
                    self.NOME_ABAS["texto"], 
                    self.FORMULAS_CONFIG["texto"],
                    resultado['linha_inicial'],
                    resultado['linha_final']
                )
        
        return resultado.get('sucesso', False)
    
    def processar_voz_hc(self, caminho_csv=None):
        """Processa base Voz HC"""
        if caminho_csv is None:
            caminho_csv = f"{self.PADROES_ARQUIVOS['voz']}.csv"
        
        resultado = self.enviar_csv_para_planilha(
            caminho_csv,
            self.NOME_ABAS["voz"]
        )
        
        # Aplicar fórmulas APENAS nas linhas recém-adicionadas (as novas linhas verdes)
        if resultado.get('sucesso') and resultado.get('num_linhas', 0) > 0:
            if self.FORMULAS_CONFIG.get("voz"):
                print(f"🔧 Aplicando fórmulas nas {resultado['num_linhas']} linhas novas da aba {self.NOME_ABAS['voz']}...")
                self.aplicar_formulas_linhas_novas(
                    self.NOME_ABAS["voz"], 
                    self.FORMULAS_CONFIG["voz"],
                    resultado['linha_inicial'],
                    resultado['linha_final']
                )
        
        return resultado.get('sucesso', False)
    
    def processar_todos(self):
        """Processa todos os arquivos Genesys disponíveis"""
        resultados = {}
        
        print("🔄 Processando bases Genesys...")
        
        processadores = {
            "Gestão da Entrega": self.processar_gestao_entrega,
            "Texto HC": self.processar_texto_hc,
            "Voz HC": self.processar_voz_hc
        }
        
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