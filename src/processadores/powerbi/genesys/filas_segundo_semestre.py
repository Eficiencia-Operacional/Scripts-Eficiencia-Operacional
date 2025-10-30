#!/usr/bin/env python3
"""
🎯 PROCESSADOR FILAS GENESYS - SEGUNDO SEMESTRE
Processador para alimentar Power BI no Looker Studio

Características:
- Processa dados do arquivo "Filas Genesys - Todas as Filas.csv"
- Envia para planilha do segundo semestre
- Pinta células de AMARELO (#FFD700) ao invés de verde
- Complementa dados existentes sem sobrescrever

Planilha: BASE FILA UNIFICADA - SEGUNDO SEMESTRE
Link: https://docs.google.com/spreadsheets/d/1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8
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


class ProcessadorFilasSegundoSemestre(GoogleSheetsBase):
    """
    Processador de Filas Genesys para Power BI - Segundo Semestre
    
    Envia dados do CSV para a planilha do Looker Studio
    Cor de destaque: AMARELO (#FFD700)
    """
    
    def __init__(self, caminho_credenciais=None):
        """
        Inicializa o processador
        
        Args:
            caminho_credenciais: Caminho para arquivo de credenciais Google
        """
        # ID da planilha do segundo semestre
        planilha_id = '1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8'
        
        # Inicializar classe base com ID correto
        super().__init__(caminho_credenciais, planilha_id)
        
        self.PLANILHA_ID = planilha_id
        self.ABA_NOME = 'BASE'
        
        print("\n" + "="*60)
        print("⚠️  ATENÇÃO - COMPARTILHAMENTO NECESSÁRIO")
        print("="*60)
        print("📧 Compartilhe a planilha com:")
        print("   boletim-315@sublime-shift-472919-f0.iam.gserviceaccount.com")
        print("   Permissão: Editor")
        print("="*60)
        
        # Cores AMARELAS para Power BI
        # Cabeçalho: Amarelo FORTE (equivalente ao verde #00A859 do boletim)
        self.COR_AMARELA_FORTE = {
            'red': 1.0,
            'green': 0.66,
            'blue': 0.0
        }
        
        # Dados: Amarelo claro
        self.COR_AMARELA_CLARA = {
            'red': 1.0,
            'green': 0.95,
            'blue': 0.6
        }
        
        print("✅ ProcessadorFilasSegundoSemestre inicializado")
        print(f"📊 Planilha ID: {self.PLANILHA_ID}")
        print(f"📄 Aba: {self.ABA_NOME}")
        print(f"🎨 Cor de destaque: AMARELO")
    
    def processar_e_enviar(self, caminho_csv):
        """
        Processa o CSV e envia para o Google Sheets
        
        Args:
            caminho_csv: Caminho para o arquivo CSV das filas
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            print(f"\n{'='*60}")
            print(f"🚀 INICIANDO PROCESSAMENTO - FILAS SEGUNDO SEMESTRE")
            print(f"{'='*60}")
            print(f"📁 Arquivo: {os.path.basename(caminho_csv)}")
            print(f"📊 Destino: BASE FILA UNIFICADA - SEGUNDO SEMESTRE")
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
                aba.append_rows(dados, value_input_option='USER_ENTERED')
                print(f"   ✅ {len(dados)} linhas enviadas")
                
                # Formatar PRIMEIRA LINHA de dados com amarelo FORTE
                print("\n🎨 Aplicando formatação AMARELA nos DADOS...")
                if len(dados) > 0:
                    print(f"   🎨 Primeira linha de dados: amarelo FORTE (#FFA800)")
                    self._aplicar_formatacao_linha_forte(aba, linha_inicial, len(df.columns))
                
                # Formatar DEMAIS LINHAS com amarelo CLARO
                if len(dados) > 1:
                    print(f"   🎨 Demais linhas: amarelo claro (#FFF299)")
                    self._aplicar_formatacao_amarela(aba, linha_inicial + 1, len(dados) - 1, len(df.columns))
                
                print("   ✅ Dados formatados com destaque na primeira linha")
            
            resultado = {
                'sucesso': True,
                'arquivo': os.path.basename(caminho_csv),
                'linhas_processadas': len(dados),
                'planilha': 'BASE FILA UNIFICADA - SEGUNDO SEMESTRE',
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
        Lê o arquivo CSV com tratamento de encoding
        
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
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=';')
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ';'")
                    return df
            except:
                pass
            
            try:
                # Tentar com vírgula
                df = pd.read_csv(caminho_csv, encoding=encoding, sep=',')
                if len(df.columns) > 1:
                    print(f"   ✅ Arquivo lido com encoding: {encoding}, separador: ','")
                    return df
            except:
                pass
        
        # Última tentativa: deixar pandas detectar automaticamente
        try:
            df = pd.read_csv(caminho_csv)
            print(f"   ✅ Arquivo lido com detecção automática")
            return df
        except Exception as e:
            raise Exception(f"Erro ao ler CSV: {str(e)}")
    
    def _limpar_dados(self, df):
        """
        Limpa e prepara os dados
        
        Args:
            df: DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame limpo
        """
        import numpy as np
        
        # Remover espaços dos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Tratar valores nulos
        df = df.fillna('')
        
        # Limpar números (remover apóstrofos, aspas)
        for col in df.columns:
            if df[col].dtype == 'object':
                # Remover aspas simples no início
                df[col] = df[col].astype(str).str.replace("^'", "", regex=True)
                df[col] = df[col].astype(str).str.replace('^"', "", regex=True)
                
                # Limpar espaços extras
                df[col] = df[col].str.strip()
        
        # Converter tipos de dados quando apropriado
        for col in df.columns:
            # Tentar converter colunas numéricas
            if 'oferta' in col.lower() or 'resposta' in col.lower() or 'abandono' in col.lower():
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Substituir inf e -inf por vazio
                    df[col] = df[col].replace([np.inf, -np.inf], '')
                    # Substituir NaN por vazio
                    df[col] = df[col].fillna('')
                except:
                    pass
        
        # Substituir qualquer inf/-inf/nan remanescente
        df = df.replace([np.inf, -np.inf, np.nan], '')
        
        return df
    
    def _aplicar_formatacao_cabecalho(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA FORTE no cabeçalho (primeira linha)
        Mesmo padrão do boletim: cor forte + negrito + texto branco
        
        Args:
            aba: Worksheet do gspread
            linha: Linha do cabeçalho (normalmente 1)
            num_colunas: Número de colunas
        """
        try:
            # Formato AMARELO FORTE para cabeçalho (igual ao verde #00A859 do boletim)
            formato_cabecalho = {
                'backgroundColor': self.COR_AMARELA_FORTE,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial',
                    'bold': True,  # Negrito no cabeçalho
                    'foregroundColor': {  # Texto branco para contraste
                        'red': 1.0,
                        'green': 1.0,
                        'blue': 1.0
                    }
                }
            }
            
            # Aplicar formato
            range_notacao = f'A{linha}:{self._col_to_letter(num_colunas)}{linha}'
            aba.format(range_notacao, formato_cabecalho)
            
        except Exception as e:
            print(f"   ⚠️  Aviso ao aplicar formatação no cabeçalho: {str(e)}")
    
    def _aplicar_formatacao_linha_forte(self, aba, linha, num_colunas):
        """
        Aplica formatação AMARELA FORTE na primeira linha de dados (destaque)
        
        Args:
            aba: Worksheet do gspread
            linha: Linha para formatar
            num_colunas: Número de colunas
        """
        try:
            # Formato AMARELO FORTE para primeira linha de dados
            formato_forte = {
                'backgroundColor': self.COR_AMARELA_FORTE,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial',
                    'bold': True  # Negrito para destaque
                }
            }
            
            # Aplicar formato
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
            # Definir range
            linha_final = linha_inicial + num_linhas - 1
            
            # Formato AMARELO CLARO para dados
            formato_amarelo = {
                'backgroundColor': self.COR_AMARELA_CLARA,
                'horizontalAlignment': 'LEFT',
                'verticalAlignment': 'MIDDLE',
                'textFormat': {
                    'fontSize': 10,
                    'fontFamily': 'Arial'
                }
            }
            
            # Aplicar formato
            range_notacao = f'A{linha_inicial}:{self._col_to_letter(num_colunas)}{linha_final}'
            aba.format(range_notacao, formato_amarelo)
            
        except Exception as e:
            print(f"   ⚠️  Aviso ao aplicar formatação: {str(e)}")
    
    def _col_to_letter(self, col_num):
        """
        Converte número de coluna para letra (1=A, 2=B, etc)
        
        Args:
            col_num: Número da coluna
            
        Returns:
            str: Letra da coluna
        """
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + ord('A')) + result
            col_num //= 26
        return result


def main():
    """Função principal para testes"""
    print("🧪 Testando ProcessadorFilasSegundoSemestre...")
    
    # Caminho do CSV
    caminho_csv = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', '..',
        'data',
        'Filas Genesys - Todas as Filas .csv'
    )
    
    # Caminho das credenciais
    caminho_credenciais = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', '..',
        'config',
        'boletim.json'
    )
    
    # Criar processador
    processador = ProcessadorFilasSegundoSemestre(caminho_credenciais)
    
    # Processar
    resultado = processador.processar_e_enviar(caminho_csv)
    
    print("\n" + "="*60)
    print("📊 RESULTADO:")
    print("="*60)
    for key, value in resultado.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    main()
