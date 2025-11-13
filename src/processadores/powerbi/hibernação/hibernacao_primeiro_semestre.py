#!/usr/bin/env python3
"""
🎯 PROCESSADOR HIBERNAÇÃO - PRIMEIRO SEMESTRE
Processador para alimentar Power BI no Looker Studio

Características:
- Processa dados do arquivo "Hibernação Power BI.csv" (ou "data (número).csv")
- Pasta: data/hibernação/
- Envia para planilha do primeiro semestre
- Pinta células de AMARELO (#FFD700)
- Complementa dados existentes sem sobrescrever

Planilha: BASE HIBERNAÇÃO POWER BI- PRIMEIRO SEMESTRE
Link: https://docs.google.com/spreadsheets/d/1v2kpi1tIChOQezQgA8jjRTGeK2iS9vfcrWoSdhLoZKM/edit
Aba: BASE
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


class ProcessadorHibernacaoPrimeiroSemestre(GoogleSheetsBase):
    """
    Processador de Hibernação para Power BI - Primeiro Semestre
    
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
            planilha_id = gp.obter_id('hibernacao_primeiro_semestre')
            
            if planilha_id:
                print("✅ Usando ID da planilha do gerenciador de configurações")
            else:
                # Fallback para ID hardcoded
                planilha_id = '1v2kpi1tIChOQezQgA8jjRTGeK2iS9vfcrWoSdhLoZKM'
                print("⚠️  ID não encontrado no gerenciador, usando ID padrão")
                
        except ImportError:
            # Fallback para configuração tradicional
            planilha_id = '1v2kpi1tIChOQezQgA8jjRTGeK2iS9vfcrWoSdhLoZKM'
            print("⚠️  Gerenciador não disponível, usando configuração hardcoded")
        
        # Inicializar classe base com ID correto
        super().__init__(caminho_credenciais, planilha_id)
        
        self.PLANILHA_ID = planilha_id
        self.ABA_NOME = 'BASE'
        
        print("\n" + "="*60)
        print("⚠️  ATENÇÃO - COMPARTILHAMENTO NECESSÁRIO")
        print("="*60)
        print("📧 Compartilhe a planilha com:")
        print("   boletim@sublime-shift-472919-f0.iam.gserviceaccount.com")
        print("   Permissão: Editor")
        print("="*60)
    
    def _ler_csv(self, caminho_csv):
        """
        Lê arquivo CSV do Power BI
        
        Args:
            caminho_csv: Caminho do arquivo CSV
            
        Returns:
            DataFrame com os dados
        """
        print(f"📖 Lendo CSV: {caminho_csv}")
        
        # Ler CSV preservando tipos como string para evitar conversões indesejadas
        df = pd.read_csv(caminho_csv, dtype=str)
        
        print(f"✅ CSV lido: {len(df)} linhas, {len(df.columns)} colunas")
        return df
    
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
                # Tentar com ponto e vírgula primeiro
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=';', dtype=str, keep_default_na=False)
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ';'")
                    return df
            except:
                pass
            
            try:
                # Tentar com vírgula
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=',', dtype=str, keep_default_na=False)
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ','")
                    return df
            except:
                pass
        
        # Última tentativa: deixar pandas detectar automaticamente
        try:
            df = pd.read_csv(caminho_csv, dtype=str, keep_default_na=False)
            print(f"   ✅ Arquivo lido com detecção automática")
            return df
        except Exception as e:
            raise Exception(f"Erro ao ler CSV: {str(e)}")
    
    def _limpar_dados(self, df):
        """
        Limpa e prepara os dados MANTENDO formato original
        
        Args:
            df: DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame limpo
        """
        # Remover espaços dos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Substituir NaN por string vazia
        df = df.fillna('')
        
        # Converter tudo para string para manter formato EXATO do CSV
        for col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].replace('nan', '')
            df[col] = df[col].str.strip()
        
        return df
    
    def _aplicar_formatacao_cabecalho(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA FORTE no cabeçalho
        
        Args:
            aba: Worksheet do gspread
            linha: Linha do cabeçalho (normalmente 1)
            num_colunas: Número de colunas
        """
        try:
            formato_cabecalho = {
                'backgroundColor': self.COR_AMARELA_FORTE,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial',
                    'bold': True,
                    'foregroundColor': {
                        'red': 1.0,
                        'green': 1.0,
                        'blue': 1.0
                    }
                }
            }
            
            range_notacao = f'A{linha}:{self._col_to_letter(num_colunas)}{linha}'
            aba.format(range_notacao, formato_cabecalho)
            
        except Exception as e:
            print(f"   ⚠️  Aviso ao aplicar formatação no cabeçalho: {str(e)}")
    
    def _aplicar_formatacao_linha_forte(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA FORTE na primeira linha de dados
        
        Args:
            aba: Worksheet do gspread
            linha: Linha para formatar
            num_colunas: Número de colunas
        """
        try:
            formato_forte = {
                'backgroundColor': self.COR_AMARELA_FORTE,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial',
                    'bold': True
                }
            }
            
            range_notacao = f'A{linha}:{self._col_to_letter(num_colunas)}{linha}'
            aba.format(range_notacao, formato_forte)
            
        except Exception as e:
            print(f"   ⚠️  Aviso ao aplicar formatação forte: {str(e)}")
    
    def _aplicar_formatacao_amarela(self, aba, linha_inicial, num_linhas, num_colunas):
        """
        Aplica formatação AMARELA CLARA nas células de dados
        
        Args:
            aba: Worksheet do gspread
            linha_inicial: Primeira linha para formatar
            num_linhas: Número de linhas
            num_colunas: Número de colunas
        """
        try:
            linha_final = linha_inicial + num_linhas - 1
            
            formato_amarelo = {
                'backgroundColor': self.COR_AMARELA_CLARA,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial'
                }
            }
            
            range_notacao = f'A{linha_inicial}:{self._col_to_letter(num_colunas)}{linha_final}'
            aba.format(range_notacao, formato_amarelo)
            
        except Exception as e:
            print(f"   ⚠️  Aviso ao aplicar formatação: {str(e)}")
    
    def _col_to_letter(self, col_num):
        """
        Converte número de coluna para letra (1=A, 2=B, etc)
        """
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + ord('A')) + result
            col_num //= 26
        return result
    
    def processar_e_enviar(self, caminho_csv):
        """
        Processa o CSV e envia para o Google Sheets
        
        Args:
            caminho_csv: Caminho para o arquivo CSV de hibernação
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            print(f"\n{'='*60}")
            print(f"🚀 INICIANDO PROCESSAMENTO - HIBERNAÇÃO PRIMEIRO SEMESTRE")
            print(f"{'='*60}")
            print(f"📁 Arquivo: {os.path.basename(caminho_csv)}")
            print(f"📊 Destino: BASE HIBERNAÇÃO POWER BI - PRIMEIRO SEMESTRE")
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
                if len(dados) > 1:
                    print(f"   🎨 Demais linhas: amarelo claro (#FFE066)")
                    self._aplicar_formatacao_amarela(aba, linha_inicial + 1, len(dados) - 1, len(df.columns))
                
                print("   ✅ Dados formatados com destaque na primeira linha")
            
            resultado = {
                'sucesso': True,
                'arquivo': os.path.basename(caminho_csv),
                'linhas_processadas': len(dados),
                'planilha': 'BASE HIBERNAÇÃO POWER BI - PRIMEIRO SEMESTRE',
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


if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando Processador Hibernação - Primeiro Semestre")
    
    arquivo_cred = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'config', 'boletim.json')
    
    try:
        processador = ProcessadorHibernacaoPrimeiroSemestre(arquivo_cred)
        print("✅ Processador inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
