#!/usr/bin/env python3
"""
🎯 PROCESSADOR AUTOSERVIÇO - PRIMEIRO SEMESTRE
Processador para alimentar Power BI no Looker Studio

Características:
- Processa dados do arquivo "Autoserviço Power BI.csv"
- Envia para planilha do primeiro semestre
- Pinta células de AMARELO (#FFD700)
- Complementa dados existentes sem sobrescrever

Planilha: AUTOSERVIÇO - PRIMEIRO SEMESTRE
Link: https://docs.google.com/spreadsheets/d/1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw
Aba: URA + LIA
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import sys
from datetime import datetime
import re

# Adicionar diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
sys.path.insert(0, root_dir)

from src.core.google_sheets_base import GoogleSheetsBase


class ProcessadorAutoservicoPrimeiroSemestre(GoogleSheetsBase):
    """
    Processador de Autoserviço para Power BI - Primeiro Semestre
    
    Envia dados do CSV para a planilha do Looker Studio
    Cor de destaque: AMARELO (#FFD700)
    """
    
    def __init__(self, caminho_credenciais=None):
        """
        Inicializa o processador
        
        Args:
            caminho_credenciais: Caminho para arquivo de credenciais Google
        """
        # Tentar usar gerenciador de configurações
        try:
            sys.path.insert(0, os.path.join(root_dir, 'config'))
            from scripts.gerenciador_planilhas import GerenciadorPlanilhas
            
            gp = GerenciadorPlanilhas()
            planilha_id = gp.obter_id('autoservico_primeiro_semestre')
            
            if not planilha_id:
                raise ValueError("ID da planilha não encontrado no gerenciador")
            
            print("✅ Configuração carregada via gerenciador centralizado")
            print(f"✅ ID obtido via configuração centralizada: {planilha_id}")
            
        except Exception as e:
            print(f"⚠️ Erro ao usar gerenciador: {e}")
            print("⚠️ Usando ID hardcoded...")
            planilha_id = "1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw"
        
        # Inicializar classe base
        if caminho_credenciais is None:
            caminho_credenciais = os.path.join(root_dir, 'config', 'boletim.json')
        
        super().__init__(
            caminho_credenciais=caminho_credenciais,
            id_planilha=planilha_id
        )
        
        # Configurações específicas
        self.PLANILHA_ID = planilha_id
        self.ABA_NOME = "URA + LIA"
        
        # Validar compatibilidade
        self._validar_service_account()
        
        print(f"\n{'='*60}")
        print(f"✅ ProcessadorAutoservicoPrimeiroSemestre inicializado")
        print(f"📊 Planilha ID: {self.PLANILHA_ID}")
        print(f"📄 Aba: {self.ABA_NOME}")
        print(f"🎨 Cor de destaque: AMARELO")
    
    def processar_e_enviar(self, caminho_csv):
        """
        Processa o CSV e envia para o Google Sheets
        
        Args:
            caminho_csv: Caminho para o arquivo CSV do Autoserviço
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            print(f"\n{'='*60}")
            print(f"🚀 INICIANDO PROCESSAMENTO - AUTOSERVIÇO PRIMEIRO SEMESTRE")
            print(f"{'='*60}")
            print(f"📁 Arquivo: {os.path.basename(caminho_csv)}")
            print(f"📊 Destino: AUTOSERVIÇO - PRIMEIRO SEMESTRE")
            print(f"📄 Aba: {self.ABA_NOME}")
            
            # Validar arquivo
            if not os.path.exists(caminho_csv):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")
            
            # Ler CSV
            print("\n📖 Lendo arquivo CSV...")
            df = self._ler_csv(caminho_csv)
            print(f"   ✅ {len(df)} linhas carregadas")
            print(f"   ✅ {len(df.columns)} colunas encontradas")
            
            # Limpar e preparar dados
            print("\n🧹 Limpando e preparando dados...")
            df = self._limpar_dados(df)
            print(f"   ✅ Dados limpos e preparados")
            
            # Conectar ao Google Sheets
            print("\n🔗 Conectando ao Google Sheets...")
            planilha = self.client.open_by_key(self.PLANILHA_ID)
            aba = planilha.worksheet(self.ABA_NOME)
            print(f"   ✅ Conectado à aba '{self.ABA_NOME}'")
            
            # Obter dados existentes
            print("\n📊 Verificando dados existentes...")
            dados_existentes = aba.get_all_values()
            
            if not dados_existentes:
                print("   ⚠️  Planilha vazia - criando cabeçalho")
                # Criar cabeçalho
                cabecalho = df.columns.tolist()
                aba.append_row(cabecalho)
                linha_inicial = 2
            else:
                print(f"   ✅ {len(dados_existentes)} linhas existentes")
                linha_inicial = len(dados_existentes) + 1
            
            # Enviar dados
            print(f"\n📤 Enviando dados para a planilha...")
            print(f"   📍 Linha inicial: {linha_inicial}")
            
            # Converter DataFrame para lista de listas
            dados = df.values.tolist()
            
            # SEMPRE formatar CABEÇALHO (linha 1) PRIMEIRO - ANTES de enviar dados
            print("\n🎨 Aplicando formatação AMARELA no CABEÇALHO...")
            self._aplicar_formatacao_cabecalho(aba, 1, len(df.columns))
            print("   ✅ Cabeçalho formatado (amarelo ESCURO #FFA800 + texto branco + NEGRITO)")
            
            # Enviar dados em lote
            if dados:
                # Processar dados para garantir compatibilidade com Google Sheets
                dados_processados = []
                for linha in dados:
                    linha_processada = []
                    for valor in linha:
                        # Converter valores para tipos apropriados
                        if valor is None or valor == '' or str(valor).lower() == 'nan':
                            linha_processada.append('')
                        else:
                            valor_str = str(valor).strip()
                            # Tentar converter para número se possível
                            try:
                                # Se contém apenas dígitos, ponto ou vírgula, pode ser número
                                if valor_str.replace('.', '').replace(',', '').replace('-', '').replace('+', '').isdigit():
                                    # Tentar converter para float
                                    valor_num = float(valor_str.replace(',', '.'))
                                    # Se for inteiro, converter para int
                                    if valor_num.is_integer():
                                        linha_processada.append(int(valor_num))
                                    else:
                                        linha_processada.append(valor_num)
                                else:
                                    # Manter como string
                                    linha_processada.append(valor_str)
                            except:
                                # Se falhar, manter como string
                                linha_processada.append(valor_str)
                    dados_processados.append(linha_processada)
                
                # Usar USER_ENTERED para que o Sheets interprete números como números
                aba.append_rows(dados_processados, value_input_option='USER_ENTERED')
                print(f"   ✅ {len(dados_processados)} linhas enviadas")
                
                # Formatar PRIMEIRA LINHA de dados com amarelo FORTE
                print("\n🎨 Aplicando formatação AMARELA nos DADOS...")
                if len(dados_processados) > 0:
                    print(f"   🎨 Primeira linha de dados: amarelo FORTE (#FFA800)")
                    self._aplicar_formatacao_linha_forte(aba, linha_inicial, len(df.columns))
                
                # Formatar DEMAIS LINHAS com amarelo CLARO
                if len(dados_processados) > 1:
                    print(f"   🎨 Demais linhas: amarelo claro (#FFF299)")
                    self._aplicar_formatacao_amarela(aba, linha_inicial + 1, len(dados_processados) - 1, len(df.columns))
                
                print("   ✅ Dados formatados com destaque na primeira linha")
            
            resultado = {
                'sucesso': True,
                'arquivo': os.path.basename(caminho_csv),
                'linhas_processadas': len(dados),
                'planilha': 'AUTOSERVIÇO - PRIMEIRO SEMESTRE',
                'aba': self.ABA_NOME,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"\n{'='*60}")
            print(f"✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print(f"{'='*60}")
            print(f"📊 {len(dados)} linhas processadas")
            print(f"🎨 Cor aplicada: AMARELO")
            print(f"🔗 Link: https://docs.google.com/spreadsheets/d/{self.PLANILHA_ID}")
            
            return resultado
            
        except Exception as e:
            print(f"\n❌ ERRO no processamento: {str(e)}")
            return {
                'sucesso': False,
                'erro': str(e),
                'arquivo': os.path.basename(caminho_csv) if caminho_csv else 'N/A'
            }
    
    def _ler_csv(self, caminho_csv):
        """
        Lê o arquivo CSV mantendo TODOS os dados como texto (sem conversão)
        
        Args:
            caminho_csv: Caminho do arquivo
            
        Returns:
            pd.DataFrame: Dados carregados
        """
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                # Tentar com ponto e vírgula primeiro (padrão Genesys)
                # dtype=str força TUDO como string - sem conversão numérica
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=';', dtype=str, keep_default_na=False)
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ';'")
                    print(f"   ✅ {len(df)} linhas carregadas")
                    print(f"   ✅ {len(df.columns)} colunas encontradas")
                    return df
            except:
                pass
            
            try:
                # Tentar com vírgula
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=',', dtype=str, keep_default_na=False)
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ','")
                    print(f"   ✅ {len(df)} linhas carregadas")
                    print(f"   ✅ {len(df.columns)} colunas encontradas")
                    return df
            except:
                pass
        
        # Última tentativa: deixar pandas detectar automaticamente
        try:
            df = pd.read_csv(caminho_csv, dtype=str, keep_default_na=False)
            print(f"   ✅ Arquivo lido com detecção automática")
            print(f"   ✅ {len(df)} linhas carregadas")
            print(f"   ✅ {len(df.columns)} colunas encontradas")
            return df
        except Exception as e:
            raise Exception(f"Erro ao ler CSV: {str(e)}")
    
    def _limpar_dados(self, df):
        """
        Limpa dados mantendo formato original
        
        Args:
            df: DataFrame para limpar
            
        Returns:
            pd.DataFrame: Dados limpos
        """
        # Converter tudo para string e remover 'nan'
        for col in df.columns:
            df[col] = df[col].apply(lambda x: '' if str(x).lower() == 'nan' else str(x))
        
        return df
    
    def _aplicar_formatacao_cabecalho(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA ESCURA (#FFA800) no cabeçalho
        
        Args:
            aba: Worksheet do gspread
            linha: Número da linha do cabeçalho (geralmente 1)
            num_colunas: Número de colunas
        """
        # Range do cabeçalho
        range_cabecalho = f"A{linha}:{chr(65 + num_colunas - 1)}{linha}"
        
        formato_cabecalho = {
            "backgroundColor": {
                "red": 1.0,      # #FFA800 = RGB(255, 168, 0)
                "green": 0.66,
                "blue": 0.0
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "bold": True,
                "fontSize": 11
            },
            "horizontalAlignment": "CENTER"
        }
        
        aba.format(range_cabecalho, formato_cabecalho)
    
    def _aplicar_formatacao_linha_forte(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA FORTE (#FFA800) em uma linha
        
        Args:
            aba: Worksheet do gspread
            linha: Número da linha
            num_colunas: Número de colunas
        """
        range_linha = f"A{linha}:{chr(65 + num_colunas - 1)}{linha}"
        
        formato_forte = {
            "backgroundColor": {
                "red": 1.0,      # #FFA800
                "green": 0.66,
                "blue": 0.0
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 0.0,
                    "green": 0.0,
                    "blue": 0.0
                },
                "bold": True
            }
        }
        
        aba.format(range_linha, formato_forte)
    
    def _aplicar_formatacao_amarela(self, aba, linha_inicial, num_linhas, num_colunas):
        """
        Aplica formatação AMARELA CLARA (#FFF299) em múltiplas linhas
        
        Args:
            aba: Worksheet do gspread
            linha_inicial: Primeira linha
            num_linhas: Quantidade de linhas
            num_colunas: Número de colunas
        """
        linha_final = linha_inicial + num_linhas - 1
        range_linhas = f"A{linha_inicial}:{chr(65 + num_colunas - 1)}{linha_final}"
        
        formato_claro = {
            "backgroundColor": {
                "red": 1.0,      # #FFF299
                "green": 0.95,
                "blue": 0.6
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 0.0,
                    "green": 0.0,
                    "blue": 0.0
                }
            }
        }
        
        aba.format(range_linhas, formato_claro)
    
    def _validar_service_account(self):
        """
        Valida se a service account tem acesso à planilha
        """
        try:
            # Tentar obter o email da service account de diferentes formas
            email = None
            
            # Tentar via auth (versões antigas do gspread)
            if hasattr(self.client, 'auth') and hasattr(self.client.auth, 'service_account_email'):
                email = self.client.auth.service_account_email
            # Tentar via credentials (versões novas)
            elif hasattr(self, '_client') and hasattr(self._client, 'auth'):
                if hasattr(self._client.auth, 'service_account_email'):
                    email = self._client.auth.service_account_email
                elif hasattr(self._client.auth, '_service_account_email'):
                    email = self._client.auth._service_account_email
            
            # Se conseguiu obter o email, mostrar mensagem
            if email:
                print(f"\n{'='*60}")
                print(f"⚠️  ATENÇÃO - COMPARTILHAMENTO NECESSÁRIO")
                print(f"{'='*60}")
                print(f"📧 Compartilhe a planilha com:")
                print(f"   {email}")
                print(f"   Permissão: Editor")
                print(f"{'='*60}\n")
        except Exception as e:
            # Se falhar, apenas continuar sem mostrar o aviso
            pass
