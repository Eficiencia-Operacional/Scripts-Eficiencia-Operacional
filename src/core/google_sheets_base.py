"""
Classe base para operações com Google Sheets
Inclui detecção inteligente de arquivos duplicados e localizador automático de credenciais
"""
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import glob
import re
import json
import shutil
from typing import Optional, List

class GoogleSheetsBase:
    """Classe base para operações com Google Sheets com detecção inteligente de arquivos"""
    
    def __init__(self, caminho_credenciais: str = "boletim.json", id_planilha: str = ""):
        """
        Inicializa a classe GoogleSheetsBase
        
        Args:
            caminho_credenciais: Caminho para o arquivo de credenciais JSON
            id_planilha: ID da planilha (será definido pelo sistema principal)
        """
        self.CAMINHO_CREDENCIAIS = caminho_credenciais
        self.ID_PLANILHA = id_planilha
        self._client = None
    
    def localizar_credenciais(self, nome_arquivo: str = "boletim.json") -> Optional[str]:
        """
        Localiza automaticamente o arquivo de credenciais em múltiplas localizações
        """
        print(f"🔍 Procurando por {nome_arquivo}...")
        
        # Locais para buscar (em ordem de prioridade)
        locais_busca = [
            # Pasta config do projeto (nova estrutura)
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config"),
            
            # Local atual e subpastas
            ".",
            "./config",
            "./configs", 
            "./credentials",
            
            # Pasta do usuário
            os.path.expanduser("~"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            
            # Pasta de trabalho atual
            os.getcwd(),
            os.path.join(os.getcwd(), "config"),
            
            # Diretório do script
            os.path.dirname(os.path.abspath(__file__)),
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ]
        
        # Buscar nos locais específicos primeiro
        for local in locais_busca:
            if os.path.exists(local):
                caminho_completo = os.path.join(local, nome_arquivo)
                if os.path.isfile(caminho_completo):
                    print(f"✅ Arquivo encontrado em: {caminho_completo}")
                    if self.validar_credenciais(caminho_completo):
                        return caminho_completo
        
        # Busca recursiva mais ampla
        print("🔍 Fazendo busca recursiva...")
        for local in [os.path.expanduser("~"), os.getcwd()]:
            if os.path.exists(local):
                for root, dirs, files in os.walk(local):
                    # Evitar pastas que normalmente não contêm credenciais
                    dirs[:] = [d for d in dirs if not d.startswith('.') and 
                            d not in ['node_modules', '__pycache__', 'venv', 'env']]
                    
                    if nome_arquivo in files:
                        caminho_encontrado = os.path.join(root, nome_arquivo)
                        print(f"✅ Arquivo encontrado em: {caminho_encontrado}")
                        if self.validar_credenciais(caminho_encontrado):
                            return caminho_encontrado
        
        print(f"❌ Arquivo {nome_arquivo} não encontrado em nenhum local")
        return None
    
    def validar_credenciais(self, caminho_arquivo: str) -> bool:
        """
        Valida se o arquivo de credenciais é válido
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar campos obrigatórios
            campos_obrigatorios = ['type', 'project_id', 'private_key', 'client_email']
            for campo in campos_obrigatorios:
                if campo not in data:
                    print(f"❌ Campo obrigatório '{campo}' não encontrado")
                    return False
            
            # Verificar se é Service Account
            if data.get('type') != 'service_account':
                print("❌ Tipo de credencial inválido (deve ser 'service_account')")
                return False
            
            print(f"✅ Credenciais válidas - Service Account: {data.get('client_email')}")
            return True
            
        except json.JSONDecodeError:
            print(f"❌ Arquivo JSON inválido: {caminho_arquivo}")
            return False
        except Exception as e:
            print(f"❌ Erro ao validar credenciais: {e}")
            return False
    
    def configurar_credenciais(self) -> str:
        """
        Configura automaticamente as credenciais encontrando e copiando o arquivo se necessário
        """
        # Primeiro, tentar localizar o arquivo
        caminho_encontrado = self.localizar_credenciais(self.CAMINHO_CREDENCIAIS)
        
        if not caminho_encontrado:
            raise FileNotFoundError(f"Arquivo de credenciais '{self.CAMINHO_CREDENCIAIS}' não encontrado!")
        
        # Se o arquivo não está no diretório atual, copiar para cá
        caminho_local = os.path.join(".", self.CAMINHO_CREDENCIAIS)
        
        if os.path.abspath(caminho_encontrado) != os.path.abspath(caminho_local):
            try:
                print(f"📋 Copiando credenciais para o diretório local...")
                shutil.copy2(caminho_encontrado, caminho_local)
                print(f"✅ Credenciais copiadas para: {caminho_local}")
                return caminho_local
            except Exception as e:
                print(f"⚠️ Não foi possível copiar o arquivo: {e}")
                print(f"🔧 Usando arquivo original: {caminho_encontrado}")
                return caminho_encontrado
        
        print(f"✅ Usando credenciais locais: {caminho_local}")
        return caminho_encontrado
    
    @property
    def client(self):
        """Lazy loading do cliente Google Sheets com conexão universal robusta"""
        if self._client is None:
            scopes = ["https://www.googleapis.com/auth/spreadsheets", 
                    "https://www.googleapis.com/auth/drive"]
            
            # Configurar credenciais automaticamente
            credenciais_path = self.configurar_credenciais()
            
            # Conexão robusta com múltiplas tentativas
            self._client = self._conectar_robusto(credenciais_path, scopes)
            
        return self._client
    
    def _conectar_robusto(self, credenciais_path: str, scopes: list, max_tentativas: int = 3):
        """Conecta de forma robusta, funcionando em qualquer computador"""
        import time
        
        for tentativa in range(1, max_tentativas + 1):
            try:
                print(f"🔄 Conectando ao Google Sheets (tentativa {tentativa}/{max_tentativas})...")
                print(f"🔍 Usando arquivo de credenciais: {credenciais_path}")
                print(f"🔍 Arquivo existe: {os.path.exists(credenciais_path)}")
                print(f"🔍 Arquivo é legível: {os.access(credenciais_path, os.R_OK)}")
                
                # Verificar se arquivo existe e é legível
                if not os.path.exists(credenciais_path):
                    raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credenciais_path}")
                
                if not os.access(credenciais_path, os.R_OK):
                    raise PermissionError(f"Sem permissão para ler o arquivo: {credenciais_path}")
                
                # Tentar ler o arquivo para verificar se está OK
                try:
                    with open(credenciais_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) < 100:  # Arquivo muito pequeno
                            raise ValueError(f"Arquivo de credenciais parece estar vazio ou corrompido")
                except Exception as read_error:
                    raise PermissionError(f"Erro ao ler arquivo de credenciais: {read_error}")
                
                # Recriar credenciais a cada tentativa
                creds = Credentials.from_service_account_file(credenciais_path, scopes=scopes)
                client = gspread.authorize(creds)
                
                # Teste básico de conectividade
                # Tentar listar uma planilha qualquer para validar conexão
                try:
                    test_sheet = client.open_by_key(self.ID_PLANILHA)
                    print(f"✅ Conexão estabelecida com sucesso!")
                    return client
                except Exception as test_error:
                    # Se for erro de permissão, ainda assim a conexão está OK
                    if 'forbidden' in str(test_error).lower() or 'permission' in str(test_error).lower():
                        print(f"✅ Conexão OK, mas sem permissão na planilha: {self.ID_PLANILHA}")
                        return client
                    else:
                        raise test_error
                
            except Exception as e:
                erro_str = str(e).lower()
                print(f"❌ Tentativa {tentativa} falhou: {e}")
                print(f"🔍 Tipo do erro: {type(e).__name__}")
                print(f"🔍 Erro completo: {repr(e)}")
                
                if tentativa < max_tentativas:
                    if 'invalid_grant' in erro_str or 'jwt' in erro_str:
                        print(f"⏳ Problema de JWT/horário. Aguardando {5 * tentativa}s...")
                        time.sleep(5 * tentativa)  # Delay progressivo
                    else:
                        print(f"⏳ Aguardando {2 * tentativa}s...")
                        time.sleep(2 * tentativa)
                else:
                    # Última tentativa falhou
                    erro_msg = f"Falha na conexão após {max_tentativas} tentativas: {e}"
                    print(f"❌ {erro_msg}")
                    
                    # Sugestões específicas
                    if 'invalid_grant' in erro_str or 'jwt signature' in erro_str:
                        print("💡 Execute: python corretor-universal.py")
                    
                    raise ConnectionError(erro_msg)
        
        # Fallback - não deveria chegar aqui
        raise ConnectionError("Não foi possível estabelecer conexão")
    
    def encontrar_arquivo_mais_recente(self, padrao_nome: str, pasta_busca: Optional[str] = None) -> Optional[str]:
        """
        Encontra o arquivo mais recente que corresponde ao padrão
        Lida com arquivos duplicados como 'arquivo.csv', 'arquivo (1).csv', etc.
        """
        if pasta_busca is None:
            # Buscar nas pastas de dados (nova estrutura)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            possibles_dirs = [
                os.path.join(project_root, "data"),  # Nova estrutura
                "dados",                              # Estrutura antiga
                "data",                              # Diretório local
                "../dados", 
                "../../dados",
                ".",
                ".."
            ]
            pasta_busca = next((d for d in possibles_dirs if os.path.exists(d)), ".")
        
        # Criar padrões de busca flexíveis
        base_nome = padrao_nome.replace('.csv', '').replace('.CSV', '')
        padroes = [
            f"{base_nome}.csv",
            f"{base_nome} (*).csv",
            f"*{base_nome}*.csv",
            f"{base_nome}.CSV",
            f"{base_nome} (*).CSV"
        ]
        
        arquivos_encontrados = []
        
        for padrao in padroes:
            caminho_padrao = os.path.join(pasta_busca, padrao)
            arquivos_encontrados.extend(glob.glob(caminho_padrao))
        
        # Busca adicional por similaridade
        if not arquivos_encontrados and os.path.exists(pasta_busca):
            for arquivo in os.listdir(pasta_busca):
                if arquivo.lower().endswith(('.csv', '.CSV')):
                    # Verificar similaridade no nome
                    arquivo_limpo = arquivo.lower().replace('.csv', '').replace('.CSV', '')
                    base_limpo = base_nome.lower()
                    if base_limpo in arquivo_limpo or arquivo_limpo in base_limpo:
                        arquivos_encontrados.append(os.path.join(pasta_busca, arquivo))
        
        if not arquivos_encontrados:
            return None
        
        # Retorna o arquivo mais recente
        arquivo_mais_recente = max(arquivos_encontrados, key=os.path.getmtime)
        nome_arquivo = os.path.basename(arquivo_mais_recente)
        
        # Feedback sobre o arquivo encontrado
        if re.search(r'\(\d+\)', nome_arquivo):
            print(f"📄 Arquivo duplicado detectado: {nome_arquivo}")
        else:
            print(f"📄 Arquivo encontrado: {nome_arquivo}")
            
        return arquivo_mais_recente
    
    def limpar_data_formato(self, valor):
        """
        Função especializada para limpar formatação de datas
        Remove apóstrofos ('), aspas, vírgulas e outros caracteres que fazem o Sheets interpretar como texto
        """
        if pd.isna(valor) or valor is None:
            return ''
        
        valor_str = str(valor).strip()
        
        # Se está vazio, retornar vazio
        if not valor_str:
            return ''
        
        # Remover caracteres invisíveis comuns
        invisiveis = ['\u200b', '\ufeff', '\u00A0', '\u200e', '\u200f', '\u202f', '\u2019', '\u2018']
        for ch in invisiveis:
            valor_str = valor_str.replace(ch, '')
        
        # LOOP para remover TODOS os apóstrofos, aspas e vírgulas do início
        # Continua removendo até não ter mais nada para remover
        caracteres_remover = ["'", '"', ',', '`', '´', ''', ''', '"', '"', '‹', '›', '«', '»', '‚', '‛']
        
        changed = True
        while changed:
            changed = False
            valor_original = valor_str
            
            # Remove do início
            for ch in caracteres_remover:
                if valor_str.startswith(ch):
                    valor_str = valor_str[1:].strip()
                    changed = True
                    break
            
            # Remove do final
            for ch in caracteres_remover:
                if valor_str.endswith(ch):
                    valor_str = valor_str[:-1].strip()
                    changed = True
                    break
            
            # Se nada mudou, sair do loop
            if valor_str == valor_original:
                break
        
        # Retorna o valor completamente limpo
        return valor_str.strip()
    
    def limpar_numero_formato(self, valor):
        """
        Função utilitária para limpar formatação desnecessária de números
        Remove .0 de números inteiros, aspas desnecessárias e outros problemas comuns
        """
        if pd.isna(valor) or valor is None:
            return ''
        
        valor_str = str(valor).strip()

        # Se está vazio, retornar vazio
        if not valor_str:
            return ''

        # Remover caracteres invisíveis comuns e NBSP
        invisiveis = ['\u200b', '\ufeff', '\u00A0', '\u200e', '\u200f', '\u202f']
        for ch in invisiveis:
            valor_str = valor_str.replace(ch, '')

        # Conjunto de aspas/apóstrofos Unicode e variantes que podem aparecer
        quote_chars = '"' + "'" + '“”‘’‹›«»`´‚‛'  # inclui várias variantes

        # Função para remover aspas/char especiais nas bordas repetidamente
        def strip_edge_quotes(s: str) -> str:
            changed = True
            s = s.strip()
            while changed and s:
                changed = False
                if s[0] in quote_chars:
                    s = s[1:].strip()
                    changed = True
                if s and s[-1] in quote_chars:
                    s = s[:-1].strip()
                    changed = True
            return s

        valor_str = strip_edge_quotes(valor_str)

        # Remover apóstrofo inicial (marcador de texto do Excel) se o restante for numérico
        if valor_str.startswith("'"):
            candidato = valor_str[1:].strip()
            if re.fullmatch(r"[-+]?\d+(?:[\.,]\d+)?", candidato):
                valor_str = candidato

        # Normalizar espaços internos
        valor_str = valor_str.replace('\u00A0', ' ').strip()

        # Preparar versão para tentativa de conversão numérica
        s = valor_str

        # Tratar casos onde ambos '.' e ',' aparecem (assumir '.' milhares e ',' decimal)
        if ',' in s and '.' in s:
            s = s.replace('.', '').replace(',', '.')
        else:
            # Se só tem vírgula, tratar como separador decimal
            s = s.replace(',', '.')

        # Remover espaços remanescentes
        s = s.replace(' ', '')

        # Evitar transformar códigos alfanuméricos com dígitos em números
        if re.search(r'[A-Za-z]', valor_str):
            return valor_str

        # Preservar zeros à esquerda (ex: '037') — não converter para int se começar com '0' e tiver >1 dígito
        if re.match(r'^0\d+$', s):
            return valor_str

        # Tentar converter para número (float ou int)
        try:
            valor_float = float(s)
            # Se for inteiro, retornar int (tipo numérico)
            if valor_float.is_integer():
                return int(round(valor_float))
            # Caso contrário, retornar float
            return float(valor_float)
        except (ValueError, TypeError, OverflowError):
            # Não é numérico — retornar string limpa
            return valor_str

    def enviar_csv_para_planilha(self, caminho_csv_ou_padrao: str, nome_aba: str) -> bool:
        """
        Método genérico para enviar CSV para uma aba específica
        COMPLEMENTA dados existentes (não remove) e remove cabeçalho do CSV
        Detecta automaticamente o separador correto do CSV
        """
        try:
            # Verificar se é um caminho direto ou padrão para buscar
            if os.path.exists(caminho_csv_ou_padrao):
                caminho_csv = caminho_csv_ou_padrao
            else:
                # Tentar encontrar arquivo pelo padrão
                caminho_csv = self.encontrar_arquivo_mais_recente(caminho_csv_ou_padrao)
                if not caminho_csv:
                    print(f"❌ Arquivo não encontrado para padrão: {caminho_csv_ou_padrao}")
                    return False
            
            # Detectar separador automaticamente com suporte robusto a encodings
            import csv
            
            # Lista extendida de encodings para tentar (ordem de prioridade)
            encodings = [
                'utf-8-sig',    # UTF-8 com BOM (comum em Excel)
                'utf-8', 
                'latin-1', 
                'cp1252',       # Windows-1252 (Western European)
                'iso-8859-1',   # ISO Latin-1
                'cp850',        # DOS Latin-1
                'utf-16',       # UTF-16 (pode ter BOM)
                'utf-16le',     # UTF-16 Little Endian
                'utf-16be'      # UTF-16 Big Endian
            ]
            df = None
            encoding_usado = None
            melhor_sep = ','
            max_colunas = 0
            
            for encoding in encodings:
                try:
                    print(f"🔍 Tentando encoding: {encoding}")
                    
                    with open(caminho_csv, 'r', encoding=encoding, errors='replace') as f:
                        # Ler primeira linha para detectar separador
                        primeira_linha = f.readline()
                        
                        # Se a linha está vazia ou muito pequena, tentar próxima
                        if not primeira_linha or len(primeira_linha.strip()) < 3:
                            f.seek(0)  # Voltar ao início
                            primeira_linha = f.read(1000)  # Ler primeiro KB
                        
                        # Testar diferentes separadores
                        separadores = [';', ',', '\t', '|', ':']
                        temp_max_colunas = 0
                        temp_melhor_sep = ','
                        
                        for sep in separadores:
                            # Contar colunas na primeira linha
                            colunas = len(primeira_linha.split(sep))
                            # Verificar se tem pelo menos 2 colunas e se não são todas vazias
                            if colunas >= 2 and colunas > temp_max_colunas:
                                # Verificar se não é um falso positivo (muitos campos vazios)
                                campos_nao_vazios = sum(1 for campo in primeira_linha.split(sep) if campo.strip())
                                if campos_nao_vazios >= 2:  # Pelo menos 2 campos com dados
                                    temp_max_colunas = colunas
                                    temp_melhor_sep = sep
                        
                        max_colunas = temp_max_colunas
                        melhor_sep = temp_melhor_sep
                        
                        print(f"🔍 Separador detectado: '{melhor_sep}' ({max_colunas} colunas)")
                    
                    # Tentar ler o CSV completo com configurações detectadas
                    df = pd.read_csv(
                        caminho_csv, 
                        sep=melhor_sep, 
                        encoding=encoding,
                        on_bad_lines='skip',    # Pular linhas problemáticas
                        engine='python',        # Engine mais tolerante
                        quoting=csv.QUOTE_ALL,  # Tratar todas as aspas corretamente
                        quotechar='"',          # Caractere de aspas padrão
                        skipinitialspace=True,  # Remove espaços extras
                        na_values=['', 'N/A', 'NULL', 'null', 'None', '#N/A', '#NULL!'],  # Valores nulos
                        keep_default_na=True,
                        doublequote=True,       # Tratar aspas duplas escapadas
                        escapechar=None         # Não usar caractere de escape
                    )
                    
                    encoding_usado = encoding
                    print(f"📊 CSV carregado: {len(df)} linhas, {len(df.columns)} colunas")
                    print(f"🔤 Encoding usado: {encoding}")
                    print(f"📋 Colunas: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
                    
                    # Verificar se DataFrame tem dados válidos
                    if len(df) > 0 and len(df.columns) > 0:
                        break  # Sucesso!
                    else:
                        print(f"⚠️ DataFrame vazio com {encoding}, tentando próximo...")
                        df = None
                        continue
                    
                except UnicodeDecodeError as ude:
                    print(f"❌ Erro de encoding {encoding}: {ude}")
                    continue
                except pd.errors.EmptyDataError:
                    print(f"⚠️ Arquivo vazio ou sem dados válidos com {encoding}")
                    continue
                except pd.errors.ParserError as pe:
                    print(f"⚠️ Erro de parsing com {encoding}: {pe}")
                    continue
                except Exception as e:
                    print(f"⚠️ Erro com encoding {encoding}: {e}")
                    continue
            
            if df is None:
                # Último recurso: tentar leitura binária e conversão manual
                print("🔧 Tentando leitura binária como último recurso...")
                try:
                    with open(caminho_csv, 'rb') as f:
                        conteudo_bytes = f.read()
                    
                    # Detectar encoding usando chardet se disponível
                    try:
                        import chardet
                        detectado = chardet.detect(conteudo_bytes)
                        encoding_detectado = detectado['encoding']
                        confianca = detectado['confidence']
                        
                        print(f"🔍 Chardet detectou: {encoding_detectado} (confiança: {confianca:.2f})")
                        
                        if encoding_detectado and confianca > 0.7:
                            conteudo_texto = conteudo_bytes.decode(encoding_detectado, errors='replace')
                            
                            # Salvar temporariamente e tentar ler
                            temp_file = caminho_csv + '.temp'
                            with open(temp_file, 'w', encoding='utf-8') as f:
                                f.write(conteudo_texto)
                            
                            df = pd.read_csv(
                                temp_file,
                                sep=melhor_sep,
                                encoding='utf-8',
                                on_bad_lines='skip',
                                engine='python'
                            )
                            
                            # Remover arquivo temporário
                            os.remove(temp_file)
                            encoding_usado = f"{encoding_detectado} (convertido via chardet)"
                            
                    except ImportError:
                        print("💡 Instale 'chardet' para melhor detecção: pip install chardet")
                except Exception as e:
                    print(f"⚠️ Falha na leitura binária: {e}")
                
                if df is None:
                    raise Exception(
                        "Não foi possível ler o arquivo CSV com nenhum encoding testado. "
                        "Verifique se o arquivo está corrompido ou em formato não suportado. "
                        f"Encodings testados: {', '.join(encodings)}"
                    )
            
            # Abre a planilha e aba
            planilha = self.client.open_by_key(self.ID_PLANILHA)
            print(f"📋 Conectado à planilha: '{planilha.title}'")
            aba = planilha.worksheet(nome_aba)
            print(f"📄 Processando aba: '{nome_aba}'")
            
            # Encontrar a próxima linha vazia (após os dados existentes)
            valores_existentes = aba.get_all_values()
            # Encontrar última linha com dados (não vazia)
            ultima_linha_com_dados = 0
            for i, linha in enumerate(valores_existentes):
                if any(cell.strip() for cell in linha):  # Se tem algum dado na linha
                    ultima_linha_com_dados = i + 1
            
            # Próxima linha disponível
            proxima_linha = ultima_linha_com_dados + 1
            
            # SOLUÇÃO: Adicionar linha em branco para expandir a planilha se necessário
            try:
                # Tentar adicionar uma linha vazia na próxima posição para garantir espaço
                linha_teste = proxima_linha + len(df)
                if linha_teste > len(valores_existentes):
                    print(f"📈 Expandindo planilha para acomodar {len(df)} linhas...")
                    # Adicionar uma linha em branco para forçar expansão
                    aba.append_row([''])
                    print(f"✅ Planilha expandida com sucesso!")
            except Exception as expand_error:
                print(f"⚠️ Aviso ao expandir planilha: {expand_error}")
            
            # Preparar dados SEM CABEÇALHO (só os dados do CSV)
            dados_csv = df.values.tolist()
            
            # Identificar colunas de data baseado nos nomes
            colunas_data = []
            palavras_chave_data = ['data', 'date', 'abertura', 'fechamento', 'criado', 'criação', 
                                    'modificado', 'atualizado', 'hora', 'timestamp', 'criacao']
            
            for idx, col_nome in enumerate(df.columns):
                col_lower = str(col_nome).lower()
                if any(palavra in col_lower for palavra in palavras_chave_data):
                    colunas_data.append(idx)
            
            if colunas_data:
                print(f"📅 Colunas de data identificadas: {[df.columns[i] for i in colunas_data]}")
            
            # Converter valores usando função de limpeza inteligente
            print(f"🔧 Aplicando limpeza automática de formatação (números, datas e aspas)...")
            dados_formatados = []
            for linha in dados_csv:
                linha_formatada = []
                for idx, valor in enumerate(linha):
                    # Se é coluna de data, usar limpeza específica para data
                    if idx in colunas_data:
                        valor_limpo = self.limpar_data_formato(valor)
                    else:
                        # Senão, usar limpeza normal de número
                        valor_limpo = self.limpar_numero_formato(valor)
                    linha_formatada.append(valor_limpo)
                dados_formatados.append(linha_formatada)
            
            print(f"✅ Formatação limpa aplicada a {len(dados_formatados)} linhas ({len(colunas_data)} colunas de data tratadas)")
            
            # Calcular range para inserir dados
            num_colunas = len(df.columns)
            num_linhas = len(dados_formatados)
            
            if num_linhas > 0:
                # Inserir dados a partir da próxima linha
                # IMPORTANTE: usar USER_ENTERED para que Sheets interprete datas corretamente
                range_destino = f"A{proxima_linha}:{chr(65 + num_colunas - 1)}{proxima_linha + num_linhas - 1}"
                aba.update(range_destino, dados_formatados, value_input_option='USER_ENTERED')
                
            # PINTAR TODAS AS LINHAS ADICIONADAS COM VERDE LEROY MERLIN
            try:
                if num_linhas > 0:
                    # Definir range de todas as linhas inseridas
                    range_colorir = f"A{proxima_linha}:{chr(65 + num_colunas - 1)}{proxima_linha + num_linhas - 1}"
                    
                    print(f"🎨 Colorindo linhas {proxima_linha} até {proxima_linha + num_linhas - 1}...")
                    
                    # Criar formatação verde Leroy Merlin com gradiente
                    formato_verde_claro = {
                        "backgroundColor": {
                            "red": 0.8,    # Verde bem claro para contraste
                            "green": 0.95,  
                            "blue": 0.85
                        },
                        "borders": {
                            "top": {"style": "SOLID", "width": 1, "color": {"red": 0.0, "green": 0.66, "blue": 0.35}},
                            "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0.0, "green": 0.66, "blue": 0.35}},
                            "left": {"style": "SOLID", "width": 1, "color": {"red": 0.0, "green": 0.66, "blue": 0.35}},
                            "right": {"style": "SOLID", "width": 1, "color": {"red": 0.0, "green": 0.66, "blue": 0.35}}
                        },
                        "textFormat": {
                            "foregroundColor": {
                                "red": 0.1,
                                "green": 0.3,
                                "blue": 0.1
                            },
                            "fontSize": 10
                        }
                    }
                    
                    # Aplicar formatação para todas as linhas
                    aba.format(range_colorir, formato_verde_claro)
                    
                    # PRIMEIRA LINHA COM DESTAQUE ESPECIAL (verde escuro)
                    primeira_linha_range = f"A{proxima_linha}:{chr(65 + num_colunas - 1)}{proxima_linha}"
                    
                    formato_primeira_linha = {
                        "backgroundColor": {
                            "red": 0.0,
                            "green": 0.66,  # #00A859 Leroy Merlin
                            "blue": 0.35
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
                        "borders": {
                            "top": {"style": "SOLID", "width": 2, "color": {"red": 0.0, "green": 0.53, "blue": 0.28}},
                            "bottom": {"style": "SOLID", "width": 2, "color": {"red": 0.0, "green": 0.53, "blue": 0.28}},
                            "left": {"style": "SOLID", "width": 2, "color": {"red": 0.0, "green": 0.53, "blue": 0.28}},
                            "right": {"style": "SOLID", "width": 2, "color": {"red": 0.0, "green": 0.53, "blue": 0.28}}
                        }
                    }
                    
                    aba.format(primeira_linha_range, formato_primeira_linha)
                    
                    print(f"🎨✅ Coloração aplicada com sucesso!")
                    print(f"   🟢 Primeira linha: Verde escuro Leroy Merlin (destaque)")
                    print(f"   💚 Demais linhas: Verde claro com bordas (total: {num_linhas} linhas)")
                    
                    # Retornar informações das linhas adicionadas para aplicar fórmulas
                    nome_arquivo = os.path.basename(caminho_csv)
                    print(f"✅ {nome_arquivo} → {nome_aba} (linhas {proxima_linha}-{proxima_linha + num_linhas - 1})")
                    print(f"📊 {num_linhas} registros adicionados (sem cabeçalho)")
                    print(f"🔧 Separador usado: '{melhor_sep}'")
                    
                    return {
                        'sucesso': True,
                        'linha_inicial': proxima_linha,
                        'linha_final': proxima_linha + num_linhas - 1,
                        'num_linhas': num_linhas
                    }
                    
            except Exception as format_error:
                print(f"⚠️ Aviso: Não foi possível aplicar formatação colorida: {format_error}")
                print("💡 Os dados foram inseridos com sucesso, apenas sem coloração")
                
                nome_arquivo = os.path.basename(caminho_csv)
                print(f"✅ {nome_arquivo} → {nome_aba} (linhas {proxima_linha}-{proxima_linha + num_linhas - 1})")
                print(f"📊 {num_linhas} registros adicionados (sem cabeçalho)")
                print(f"🔧 Separador usado: '{melhor_sep}'")
                
                # Retornar informações das linhas adicionadas para aplicar fórmulas
                return {
                    'sucesso': True,
                    'linha_inicial': proxima_linha,
                    'linha_final': proxima_linha + num_linhas - 1,
                    'num_linhas': num_linhas
                }
            else:
                print(f"⚠️ Arquivo CSV vazio: {caminho_csv}")
            
            return {'sucesso': True, 'linha_inicial': None, 'linha_final': None, 'num_linhas': 0}
            
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {str(e)}")
            return {'sucesso': False, 'linha_inicial': None, 'linha_final': None, 'num_linhas': 0}
    
    def aplicar_formula_coluna(self, nome_aba, coluna, linha_inicial, formula_template, linha_final=None):
        """
        Aplica uma fórmula em toda uma coluna
        
        Args:
            nome_aba: Nome da aba
            coluna: Letra da coluna (ex: 'P')
            linha_inicial: Primeira linha (geralmente 2 para pular cabeçalho)
            formula_template: Template da fórmula com {row} como placeholder
            linha_final: Última linha (None = detectar automaticamente)
        
        Exemplo:
            self.aplicar_formula_coluna('BASE VOZ', 'P', 2, '=TEXT(C{row};"DD/M")')
        """
        try:
            planilha = self.client.open_by_key(self.ID_PLANILHA)
            aba = planilha.worksheet(nome_aba)
            
            # Detectar automaticamente a última linha com dados se não especificada
            if linha_final is None:
                valores = aba.get_all_values()
                linha_final = len(valores)
            
            # Se não há dados além do cabeçalho, não aplicar fórmulas
            if linha_final < linha_inicial:
                print(f"  ⚠️ Sem dados para aplicar fórmulas na coluna {coluna}")
                return True
            
            # Criar lista de fórmulas
            formulas = []
            for linha in range(linha_inicial, linha_final + 1):
                formula = formula_template.replace('{row}', str(linha))
                formulas.append([formula])
            
            # Aplicar as fórmulas com USER_ENTERED para que sejam interpretadas como fórmulas
            range_cells = f'{coluna}{linha_inicial}:{coluna}{linha_final}'
            aba.update(range_cells, formulas, value_input_option='USER_ENTERED')
            
            print(f"  ✅ Fórmulas aplicadas em {range_cells} ({linha_final - linha_inicial + 1} células)")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao aplicar fórmulas na coluna {coluna}: {str(e)}")
            return False
    
    def aplicar_formulas_multiplas(self, nome_aba, formulas_config, linha_inicial=2):
        """
        Aplica múltiplas fórmulas de uma vez
        
        Args:
            nome_aba: Nome da aba
            formulas_config: Lista de dicts com {'coluna': 'X', 'formula': '=...{row}...'}
            linha_inicial: Linha inicial (padrão: 2 para pular cabeçalho)
        
        Exemplo:
            self.aplicar_formulas_multiplas('BASE VOZ', [
                {'coluna': 'P', 'formula': '=TEXT(C{row};"DD/M")'},
                {'coluna': 'Q', 'formula': '=M{row}-K{row}'}
            ])
        """
        try:
            planilha = self.client.open_by_key(self.ID_PLANILHA)
            aba = planilha.worksheet(nome_aba)
            valores = aba.get_all_values()
            linha_final = len(valores)
            
            if linha_final < linha_inicial:
                print(f"  ⚠️ Sem dados para aplicar fórmulas em {nome_aba}")
                return True
            
            print(f"  🔧 Aplicando {len(formulas_config)} fórmula(s) em {nome_aba}...")
            
            sucesso = True
            for config in formulas_config:
                coluna = config['coluna']
                formula_template = config['formula']
                
                resultado = self.aplicar_formula_coluna(
                    nome_aba, 
                    coluna, 
                    linha_inicial, 
                    formula_template,
                    linha_final
                )
                
                if not resultado:
                    sucesso = False
            
            return sucesso
            
        except Exception as e:
            print(f"  ❌ Erro ao aplicar fórmulas múltiplas: {str(e)}")
            return False
    
    def aplicar_formulas_linhas_novas(self, nome_aba, formulas_config, linha_inicial, linha_final):
        """
        Aplica fórmulas APENAS nas linhas recém-adicionadas (as que ficaram verdes)
        MÉTODO: Copia a fórmula da linha anterior e cola nas linhas novas (simulando Ctrl+C + Ctrl+V)
        
        Args:
            nome_aba: Nome da aba
            formulas_config: Lista de dicts com {'coluna': 'X', 'formula': '=...{row}...'}
            linha_inicial: Primeira linha adicionada
            linha_final: Última linha adicionada
        
        Exemplo:
            # Após enviar CSV que retornou linha_inicial=100, linha_final=150
            self.aplicar_formulas_linhas_novas('BASE VOZ', [
                {'coluna': 'P', 'formula': '=TEXT(C{row};"DD/M")'}
            ], 100, 150)
        """
        try:
            if linha_inicial is None or linha_final is None:
                print(f"  ⚠️ Sem linhas novas para aplicar fórmulas")
                return True
            
            planilha = self.client.open_by_key(self.ID_PLANILHA)
            aba = planilha.worksheet(nome_aba)
            
            print(f"  🔧 Copiando e colando fórmulas nas linhas {linha_inicial}-{linha_final}...")
            print(f"  📋 Método: Copiar fórmula da linha {linha_inicial - 1} e colar nas novas linhas")
            
            sucesso = True
            for config in formulas_config:
                coluna = config['coluna']
                
                # ETAPA 1: Copiar a fórmula da linha ANTERIOR (linha_inicial - 1)
                linha_origem = linha_inicial - 1
                celula_origem = f'{coluna}{linha_origem}'
                
                try:
                    # Pegar o valor/fórmula da célula origem
                    valor_origem = aba.acell(celula_origem, value_render_option='FORMULA').value
                    
                    if valor_origem and valor_origem.startswith('='):
                        print(f"    📋 Copiando de {celula_origem}: {valor_origem[:60]}...")
                        
                        # ETAPA 2: Usar copyPaste do Google Sheets API (simula Ctrl+C + Ctrl+V)
                        # Isso faz o Google Sheets ajustar automaticamente as referências
                        requests = [{
                            "copyPaste": {
                                "source": {
                                    "sheetId": aba.id,
                                    "startRowIndex": linha_origem - 1,  # 0-indexed
                                    "endRowIndex": linha_origem,
                                    "startColumnIndex": self._letra_para_indice(coluna),
                                    "endColumnIndex": self._letra_para_indice(coluna) + 1
                                },
                                "destination": {
                                    "sheetId": aba.id,
                                    "startRowIndex": linha_inicial - 1,  # 0-indexed
                                    "endRowIndex": linha_final,
                                    "startColumnIndex": self._letra_para_indice(coluna),
                                    "endColumnIndex": self._letra_para_indice(coluna) + 1
                                },
                                "pasteType": "PASTE_FORMULA"  # Copiar apenas a fórmula
                            }
                        }]
                        
                        # Executar o copyPaste
                        body = {'requests': requests}
                        planilha.batch_update(body)
                        
                        print(f"    ✅ Fórmula copiada e colada em {coluna}{linha_inicial}:{coluna}{linha_final}")
                        
                    else:
                        # Se não tem fórmula na linha anterior, criar do zero usando template
                        print(f"    ⚠️ Não há fórmula em {celula_origem}, criando do zero...")
                        formula_template = config['formula']
                        formulas = []
                        for linha in range(linha_inicial, linha_final + 1):
                            formula = formula_template.replace('{row}', str(linha))
                            formulas.append([formula])
                        
                        range_cells = f'{coluna}{linha_inicial}:{coluna}{linha_final}'
                        aba.update(range_cells, formulas, value_input_option='USER_ENTERED')
                        print(f"    ✅ Fórmula criada em {coluna}{linha_inicial}:{coluna}{linha_final}")
                        
                except Exception as e:
                    print(f"    ⚠️ Erro ao copiar de {celula_origem}: {e}")
                    # Fallback: criar fórmula do zero
                    formula_template = config['formula']
                    formulas = []
                    for linha in range(linha_inicial, linha_final + 1):
                        formula = formula_template.replace('{row}', str(linha))
                        formulas.append([formula])
                    
                    range_cells = f'{coluna}{linha_inicial}:{coluna}{linha_final}'
                    aba.update(range_cells, formulas, value_input_option='USER_ENTERED')
                    print(f"    ✅ Fórmula criada (fallback) em {coluna}{linha_inicial}:{coluna}{linha_final}")
            
            return sucesso
            
        except Exception as e:
            print(f"  ❌ Erro ao aplicar fórmulas nas linhas novas: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _letra_para_indice(self, letra):
        """Converte letra de coluna (A, B, Z, AA) para índice numérico (0-indexed)"""
        indice = 0
        for char in letra:
            indice = indice * 26 + (ord(char.upper()) - ord('A') + 1)
        return indice - 1
    
    def aplicar_formulas_todas_linhas(self, nome_aba, formulas_config, linha_inicial=2, linha_final=None):
        """
        Aplica fórmulas em TODAS as linhas com dados (não apenas nas novas)
        Isso garante que todas as linhas tenham as fórmulas, permitindo que ao adicionar
        novas linhas manualmente, elas sejam preenchidas automaticamente
        
        Args:
            nome_aba: Nome da aba
            formulas_config: Lista de dicts com {'coluna': 'X', 'formula': '=...{row}...'}
            linha_inicial: Primeira linha para aplicar fórmulas (padrão: 2, após cabeçalho)
            linha_final: Última linha para aplicar fórmulas (None = detectar automaticamente)
        
        Exemplo:
            self.aplicar_formulas_todas_linhas('BASE RESOLVIDA', [
                {'coluna': 'U', 'formula': '=B{row}'},
                {'coluna': 'V', 'formula': '=C{row}'}
            ], linha_inicial=2, linha_final=500)
        """
        try:
            planilha = self.client.open_by_key(self.ID_PLANILHA)
            aba = planilha.worksheet(nome_aba)
            
            # Detectar automaticamente a última linha se não especificada
            if linha_final is None:
                valores = aba.get_all_values()
                linha_final = len(valores)
            
            # Validar que há linhas para processar
            if linha_final < linha_inicial:
                print(f"  ⚠️ Sem dados para aplicar fórmulas (linha_inicial={linha_inicial}, linha_final={linha_final})")
                return True
            
            total_linhas = linha_final - linha_inicial + 1
            print(f"  🔧 Aplicando {len(formulas_config)} fórmula(s) em TODAS as {total_linhas} linhas ({linha_inicial}-{linha_final})...")
            
            sucesso = True
            for config in formulas_config:
                coluna = config['coluna']
                formula_template = config['formula']
                
                # Criar fórmulas para TODAS as linhas
                formulas = []
                for linha in range(linha_inicial, linha_final + 1):
                    formula = formula_template.replace('{row}', str(linha))
                    formulas.append([formula])
                
                # Aplicar fórmulas em lote (mais eficiente)
                range_cells = f'{coluna}{linha_inicial}:{coluna}{linha_final}'
                aba.update(range_cells, formulas, value_input_option='USER_ENTERED')
                
                print(f"    ✅ Coluna {coluna}: {total_linhas} fórmulas aplicadas ({coluna}{linha_inicial}:{coluna}{linha_final})")
            
            print(f"  🎉 Todas as fórmulas aplicadas com sucesso em {total_linhas} linhas!")
            return sucesso
            
        except Exception as e:
            print(f"  ❌ Erro ao aplicar fórmulas em todas as linhas: {str(e)}")
            import traceback
            traceback.print_exc()
            return False