#!/usr/bin/env python3
"""
🎨 INTERFACE VISUAL - AUTOMAÇÃO LEROY MERLIN
Interface gráfica moderna para execução das automações

Cores Leroy Merlin:j
- Verde Principal: #00A859
- Verde Escuro: #008A47
- Laranja: #FF6B35
- Cinza Escuro: #333333
- Branco: #FFFFFF
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import sys  
import os
import json
from datetime import datetime
import subprocess 
from tkinter import messagebox as mb
from tkinter import ttk

# Adicionar o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

# Importar renomeador
from renomeador_inteligente import RenomeadorInteligente

# Simple tooltip helper (lightweight and safe)
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        try:
            widget.bind("<Enter>", self.show)
            widget.bind("<Leave>", self.hide)
        except Exception:
            pass

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        try:
            x = event.x_root + 20 if event else self.widget.winfo_rootx() + 20
            y = event.y_root + 10 if event else self.widget.winfo_rooty() + 10
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, justify='left',
                             background="#FFFFE0", relief='solid', borderwidth=1,
                             font=('Segoe UI', 9))
            label.pack(ipadx=4, ipady=2)
        except Exception:
            self.tipwindow = None

    def hide(self, event=None):
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None

class AutomacaoLeroyMerlinGUI:
    """Interface visual para automação Leroy Merlin"""
    
    def __init__(self): 
        # Cores da Leroy Merlin - PROFISSIONAL (Verde + Preto + Branco)
        self.CORES = {
            'verde_leroy': '#00A859',       # Verde oficial Leroy Merlin
            'verde_escuro': '#00864A',      # Verde escuro
            'verde_hover': '#00C46A',       # Verde hover
            'preto': '#000000',             # Preto puro
            'preto_suave': '#1A1A1A',       # Preto suave para fundos
            'cinza_escuro': '#2A2A2A',      # Cinza escuro
            'cinza_medio': '#404040',       # Cinza médio
            'branco': '#FFFFFF',            # Branco puro
            'branco_suave': '#F5F5F5',      # Branco suave
            'texto_claro': '#E8E8E8',       # Texto claro
            'laranja': '#FF6B35',           # Laranja destaque
            'azul_info': '#2196F3',         # Azul info
            'amarelo_aviso': '#FFC107',     # Amarelo aviso
            'vermelho': '#F44336'           # Vermelho erro
        }
        
        # KPIs para dashboard - DADOS DINÂMICOS 
        self.kpis_data = {
            'total_processados': 0,
            'taxa_sucesso': 0.0,
            'tempo_medio': 0,
            'ultima_execucao': 'Nunca',
            'arquivos_processados': 0,
            'arquivos_sucesso': 0,
            'arquivos_erro': 0
        }
        
        # Variáveis para labels KPI (para atualização dinâmica)
        self.kpi_labels = {}
        
        # Arquivo para persistência dos KPIs - agora na pasta json/
        self.arquivo_kpis = os.path.join('json', 'kpis_historico.json')
        
        self.janela_principal = None
        self.texto_log = None
        self.botao_executar = None
        self.botao_renomear = None
        self.progresso = None
        self.status_label = None
        self.executando = False
        self.renomeador = RenomeadorInteligente()
        
        # Carregar KPIs salvos
        self.carregar_kpis()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Janela principal - TEMA PROFISSIONAL (Preto + Verde + Branco)
        self.janela_principal = tk.Tk()
        self.janela_principal.title("Dashboard RPA - Leroy Merlin v2.4")
        self.janela_principal.geometry("1400x800")  # Maior para dashboards
        self.janela_principal.configure(bg=self.CORES['preto_suave'])
        self.janela_principal.minsize(1200, 700)
        
        # Ícone da janela (se disponível)
        try:
            self.janela_principal.iconbitmap(default="favicon.ico")
        except:
            pass
        
        # Estilo personalizado
        self.configurar_estilos()
        
        # Criar canvas principal com scroll
        self.criar_canvas_principal()
        
        # Header PROFISSIONAL com logo
        self.criar_header_profissional()
        
        # KPIs Dashboard (NOVO!)
        self.criar_kpis_dashboard()
        
        # Atualizar KPIs com dados carregados
        self.janela_principal.after(100, self.atualizar_kpis)
        
        # Área de controles (prioridade)
        self.criar_controles()
        
        # Área de logs (compacta)
        self.criar_area_logs()
        
        # Footer com informações
        self.criar_footer()
        
        # Configurar scroll da janela
        self.configurar_scroll()
        
        # Centralizar janela
        self.centralizar_janela()
    
    def configurar_estilos(self):
        """Configura estilos personalizados com visual melhorado"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botão principal verde com hover melhorado (MAIOR)
        style.configure(
            'Verde.TButton',
            background=self.CORES['verde_leroy'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 12, 'bold'),
            padding=(25, 18),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Verde.TButton',
                  background=[('active', self.CORES['verde_escuro']),
                             ('pressed', self.CORES['verde_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão renomear verde claro com melhor visual (MAIOR)
        style.configure(
            'VerdeClaro.TButton',
            background=self.CORES['verde_leroy'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 11, 'bold'),
            padding=(18, 14),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('VerdeClaro.TButton',
                  background=[('active', self.CORES['verde_hover']),
                             ('pressed', self.CORES['verde_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão laranja com visual melhorado (MAIOR)
        style.configure(
            'Laranja.TButton',
            background=self.CORES['laranja'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 11, 'bold'),
            padding=(20, 14),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Laranja.TButton',
                  background=[('active', '#E55A2B'),
                             ('pressed', '#CC5020'),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão info azul melhorado (MAIOR)
        style.configure(
            'Info.TButton',
            background=self.CORES['azul_info'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 10, 'bold'),
            padding=(16, 12),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Info.TButton',
                  background=[('active', '#1976D2'),
                             ('pressed', '#1565C0'),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão perigo vermelho melhorado
        style.configure(
            'Perigo.TButton',
            background='#DC3545',
            foreground=self.CORES['branco'],
            font=('Segoe UI', 9, 'bold'),
            padding=(10, 8),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Perigo.TButton',
                  background=[('active', '#C82333'),
                             ('pressed', '#BD2130'),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Barra de progresso verde personalizada
        style.configure(
            'Verde.Horizontal.TProgressbar',
            troughcolor=self.CORES['cinza_medio'],
            background=self.CORES['verde_leroy'],
            lightcolor=self.CORES['verde_hover'],
            darkcolor=self.CORES['verde_escuro'],
            relief='flat',
            borderwidth=2,
            focuscolor='none'
        )
    
    def criar_canvas_principal(self):
        """Cria canvas principal com scroll para interface responsiva"""
        # Canvas principal - FUNDO PRETO PROFISSIONAL
        self.canvas = tk.Canvas(
            self.janela_principal,
            bg=self.CORES['preto_suave'],
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.janela_principal, 
            orient="vertical", 
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame que conterá todo o conteúdo - FUNDO PRETO
        self.frame_conteudo = tk.Frame(self.canvas, bg=self.CORES['preto_suave'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_conteudo, anchor="nw")
        
        # Posicionar canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind para atualizar scroll region
        self.frame_conteudo.bind("<Configure>", self.atualizar_scroll)
        self.canvas.bind("<Configure>", self.redimensionar_canvas)
        
        # Habilitar scroll com mouse wheel
        self.canvas.bind("<MouseWheel>", self.scroll_mouse)
        
        # Agora usar frame_conteudo como container principal
        self.container_principal = self.frame_conteudo
    
    def criar_header_profissional(self):
        """Cria header PROFISSIONAL com logo Leroy Merlin"""
        # Header VERDE LEROY MERLIN
        header_frame = tk.Frame(self.container_principal, bg=self.CORES['verde_leroy'], height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container interno
        header_content = tk.Frame(header_frame, bg=self.CORES['verde_leroy'])
        header_content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # LOGO LEROY MERLIN (se existir)
        try:
            from PIL import Image, ImageTk
            logo_path = os.path.join(current_dir, 'leroy.png')
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(header_content, image=logo_photo, bg=self.CORES['verde_leroy'])
                logo_label.image = logo_photo  # Manter referência
                logo_label.pack(side='left', padx=(0, 20))
        except:
            # Fallback: emoji foguete
            logo_label = tk.Label(
                header_content,
                text="🚀",
                font=('Segoe UI Emoji', 40, 'bold'),
                bg=self.CORES['verde_leroy'],
                fg=self.CORES['branco']
            )
            logo_label.pack(side='left', padx=(0, 20))
        
        # Textos
        texto_frame = tk.Frame(header_content, bg=self.CORES['verde_leroy'])
        texto_frame.pack(side='left', fill='both', expand=True)
        
        # Título
        titulo = tk.Label(
            texto_frame,
            text="DASHBOARD RPA",
            font=('Segoe UI', 26, 'bold'),
            bg=self.CORES['verde_leroy'],
            fg=self.CORES['branco']
        )
        titulo.pack(anchor='w')
        
        # Subtítulo - LIMPO E PROFISSIONAL
        subtitulo = tk.Label(
            texto_frame,
            text="Sistema RPA • Processamento Automatizado • Leroy Merlin",
            font=('Segoe UI', 12),
            bg=self.CORES['verde_leroy'],
            fg=self.CORES['branco']
        )
        subtitulo.pack(anchor='w', pady=(6, 0))
        
        # Status lado direito
        status_frame = tk.Frame(header_content, bg=self.CORES['verde_leroy'])
        status_frame.pack(side='right')
        
        # Online indicator
        status_dot = tk.Label(
            status_frame,
            text="● ONLINE",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['verde_leroy'],
            fg=self.CORES['branco']
        )
        status_dot.pack(anchor='e')
        
        # Data/hora
        from datetime import datetime
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        data_label = tk.Label(
            status_frame,
            text=f"📅 {agora}",
            font=('Segoe UI', 9),
            bg=self.CORES['verde_leroy'],
            fg=self.CORES['branco_suave']
        )
        data_label.pack(anchor='e', pady=(4, 0))
        
        # Linha decorativa preta
        linha = tk.Frame(self.container_principal, bg=self.CORES['preto'], height=3)
        linha.pack(fill='x')
    
    def criar_kpis_dashboard(self):
        """Cria KPIs dashboard estilo Power BI - DADOS DINÂMICOS"""
        # Container KPIs
        kpis_frame = tk.Frame(self.container_principal, bg=self.CORES['preto_suave'])
        kpis_frame.pack(fill='x', padx=30, pady=20)
        
        # Grid de 4 KPIs DINÂMICOS
        kpis_config = [
            {
                'key': 'total_processados',
                'titulo': 'Total Processado',
                'valor_inicial': '0',
                'subtitulo': 'registros',
                'emoji': '📊',
                'cor': self.CORES['verde_leroy']
            },
            {
                'key': 'taxa_sucesso',
                'titulo': 'Taxa de Sucesso',
                'valor_inicial': '0%',
                'subtitulo': 'aproveitamento',
                'emoji': '✅',
                'cor': self.CORES['verde_leroy']
            },
            {
                'key': 'tempo_medio',
                'titulo': 'Tempo Médio',
                'valor_inicial': '0s',
                'subtitulo': 'por arquivo',
                'emoji': '⚡',
                'cor': self.CORES['azul_info']
            },
            {
                'key': 'ultima_execucao',
                'titulo': 'Última Execução',
                'valor_inicial': 'Nunca',
                'subtitulo': 'aguardando',
                'emoji': '🕐',
                'cor': self.CORES['laranja']
            }
        ]
        
        for i, kpi in enumerate(kpis_config):
            # Card KPI com sombra
            kpi_shadow = tk.Frame(kpis_frame, bg='#000000')
            kpi_shadow.grid(row=0, column=i, padx=10, pady=0, sticky='ew')
            
            kpi_card = tk.Frame(kpi_shadow, bg=self.CORES['cinza_escuro'], relief='flat', bd=0)
            kpi_card.pack(fill='both', expand=True, padx=2, pady=2)
            
            # Container interno
            kpi_inner = tk.Frame(kpi_card, bg=self.CORES['cinza_escuro'])
            kpi_inner.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Emoji/Ícone grande
            emoji_label = tk.Label(
                kpi_inner,
                text=kpi['emoji'],
                font=('Segoe UI Emoji', 32),
                bg=self.CORES['cinza_escuro'],
                fg=kpi['cor']
            )
            emoji_label.pack()
            
            # Título
            titulo_label = tk.Label(
                kpi_inner,
                text=kpi['titulo'],
                font=('Segoe UI', 10),
                bg=self.CORES['cinza_escuro'],
                fg=self.CORES['texto_claro']
            )
            titulo_label.pack(pady=(8, 2))
            
            # Valor GRANDE (DINÂMICO - salvar referência)
            valor_label = tk.Label(
                kpi_inner,
                text=kpi['valor_inicial'],
                font=('Segoe UI', 28, 'bold'),
                bg=self.CORES['cinza_escuro'],
                fg=self.CORES['branco']
            )
            valor_label.pack()
            
            # Salvar referência para atualização posterior
            self.kpi_labels[kpi['key']] = valor_label
            
            # Subtítulo (DINÂMICO - salvar referência também)
            sub_label = tk.Label(
                kpi_inner,
                text=kpi['subtitulo'],
                font=('Segoe UI', 9),
                bg=self.CORES['cinza_escuro'],
                fg=self.CORES['texto_claro']
            )
            sub_label.pack(pady=(2, 0))
            
            # Salvar referência do subtítulo também
            self.kpi_labels[f"{kpi['key']}_sub"] = sub_label
        
        # Configurar grid weights para distribuição uniforme
        for i in range(4):
            kpis_frame.grid_columnconfigure(i, weight=1, uniform='kpi')
    
    def atualizar_kpis(self):
        """Atualiza os KPIs com dados reais"""
        try:
            # Calcular taxa de sucesso
            if self.kpis_data['arquivos_processados'] > 0:
                taxa = (self.kpis_data['arquivos_sucesso'] / self.kpis_data['arquivos_processados']) * 100
                self.kpis_data['taxa_sucesso'] = taxa
            else:
                taxa = 0
            
            # Atualizar labels
            if 'total_processados' in self.kpi_labels:
                self.kpi_labels['total_processados'].configure(
                    text=f"{self.kpis_data['total_processados']:,}".replace(',', '.')
                )
            
            if 'taxa_sucesso' in self.kpi_labels:
                self.kpi_labels['taxa_sucesso'].configure(
                    text=f"{taxa:.1f}%"
                )
            
            if 'tempo_medio' in self.kpi_labels:
                tempo = self.kpis_data['tempo_medio']
                if tempo > 60:
                    texto_tempo = f"{tempo//60}m{tempo%60}s"
                else:
                    texto_tempo = f"{tempo}s"
                self.kpi_labels['tempo_medio'].configure(text=texto_tempo)
            
            if 'ultima_execucao' in self.kpi_labels:
                self.kpi_labels['ultima_execucao'].configure(
                    text=self.kpis_data['ultima_execucao']
                )
            
            # Atualizar interface
            self.janela_principal.update()
            
        except Exception as e:
            print(f"Erro ao atualizar KPIs: {e}")
    
    def carregar_kpis(self):
        """Carrega KPIs salvos do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_kpis):
                with open(self.arquivo_kpis, 'r', encoding='utf-8') as f:
                    dados_salvos = json.load(f)
                    self.kpis_data.update(dados_salvos)
                print(f"✅ KPIs carregados: {self.kpis_data}")
            else:
                print("⚠️ Arquivo de KPIs não encontrado, usando valores padrão")
        except Exception as e:
            print(f"❌ Erro ao carregar KPIs: {e}")
    
    def salvar_kpis(self):
        """Salva KPIs no arquivo JSON"""
        try:
            # Garantir que o diretório config existe
            os.makedirs('config', exist_ok=True)
            
            with open(self.arquivo_kpis, 'w', encoding='utf-8') as f:
                json.dump(self.kpis_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ KPIs salvos: {self.kpis_data}")
        except Exception as e:
            print(f"❌ Erro ao salvar KPIs: {e}")
    
    def registrar_execucao(self, sucesso=True, registros_processados=0, tempo_segundos=0):
        """Registra uma execução e atualiza os KPIs"""
        try:
            from datetime import datetime
            
            # Atualizar contadores
            self.kpis_data['arquivos_processados'] += 1
            
            if sucesso:
                self.kpis_data['arquivos_sucesso'] += 1
            else:
                self.kpis_data['arquivos_erro'] += 1
            
            # Atualizar total de registros
            self.kpis_data['total_processados'] += registros_processados
            
            # Atualizar tempo médio (média ponderada simples)
            if tempo_segundos > 0:
                tempo_atual = self.kpis_data['tempo_medio']
                total_exec = self.kpis_data['arquivos_processados']
                
                # Média incremental: novo_tempo = (tempo_atual * (n-1) + tempo_novo) / n
                if total_exec > 1:
                    novo_tempo = ((tempo_atual * (total_exec - 1)) + tempo_segundos) / total_exec
                else:
                    novo_tempo = tempo_segundos
                
                self.kpis_data['tempo_medio'] = int(novo_tempo)
            
            # Atualizar última execução
            agora = datetime.now()
            self.kpis_data['ultima_execucao'] = agora.strftime("Hoje %H:%M")
            
            # Salvar dados
            self.salvar_kpis()
            
            # Atualizar interface
            self.atualizar_kpis()
            
            print(f"✅ Execução registrada: Sucesso={sucesso}, Registros={registros_processados}, Tempo={tempo_segundos}s")
            
        except Exception as e:
            print(f"❌ Erro ao registrar execução: {e}")
    
    def extrair_total_registros(self, output):
        """Extrai o total de registros processados do output"""
        try:
            if not output:
                return 50  # Valor padrão estimado
            
            # Buscar padrões comuns no output
            import re
            
            # Padrões: "processados: 123", "Total: 123", "123 registros"
            padroes = [
                r'processados?:\s*(\d+)',
                r'Total.*?:\s*(\d+)',
                r'(\d+)\s+registros?',
                r'linhas?\s+processadas?:\s*(\d+)'
            ]
            
            for padrao in padroes:
                match = re.search(padrao, output, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            
            # Se não encontrar, retornar valor padrão
            return 50
            
        except:
            return 50
    
    def extrair_tempo_execucao(self, output):
        """Extrai o tempo de execução do output"""
        try:
            if not output:
                return 15  # Valor padrão estimado (15 segundos)
            
            import re
            
            # Padrões: "Tempo: 45s", "Duração: 1m30s", "45.5 segundos"
            padroes = [
                r'tempo.*?:\s*(\d+)s',
                r'duração.*?:\s*(\d+)s',
                r'(\d+)\s+segundos?',
                r'tempo.*?:\s*(\d+)m\s*(\d+)s'  # Minutos e segundos
            ]
            
            for padrao in padroes:
                match = re.search(padrao, output, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:  # Formato minutos + segundos
                        minutos = int(match.group(1))
                        segundos = int(match.group(2))
                        return (minutos * 60) + segundos
                    else:
                        return int(match.group(1))
            
            # Se não encontrar, retornar valor padrão
            return 15
            
        except:
            return 15
    
    def criar_controles(self):
        """Cria área de controles - PROFISSIONAL (Verde + Preto + Branco)"""
        controles_frame = tk.Frame(self.container_principal, bg=self.CORES['preto_suave'])
        controles_frame.pack(fill='x', padx=30, pady=15)
        
        # Frame superior com duas colunas
        superior_frame = tk.Frame(controles_frame, bg=self.CORES['preto_suave'])
        superior_frame.pack(fill='x', pady=(0, 12))
        
        # ==== COLUNA ESQUERDA ====
        opcoes_shadow = tk.Frame(superior_frame, bg=self.CORES['preto'])
        opcoes_shadow.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        opcoes_frame = tk.LabelFrame(
            opcoes_shadow,
            text="  📋 Opções de Execução  ",
            font=('Segoe UI', 12, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            relief='flat',
            bd=0,
            padx=20,
            pady=15,
            labelanchor='n'
        )
        opcoes_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Variáveis para checkboxes
        self.var_genesys = tk.BooleanVar(value=True)
        self.var_salesforce = tk.BooleanVar(value=True)
        self.var_produtividade = tk.BooleanVar(value=True)
        self.var_verbose = tk.BooleanVar(value=False)
        
        # Checkboxes - PROFISSIONAL
        checkbox_frame = tk.Frame(opcoes_frame, bg=self.CORES['cinza_escuro'])
        checkbox_frame.pack(fill='x', padx=8, pady=10)
        
        # Checkbox Genesys
        cb_genesys = tk.Checkbutton(
            checkbox_frame,
            text="📊 Processar Genesys (VOZ, TEXTO, GESTÃO)",
            variable=self.var_genesys,
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            activebackground=self.CORES['verde_leroy'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['verde_leroy'],
            relief='flat',
            highlightthickness=0,
            bd=0,
            cursor='hand2'
        )
        cb_genesys.pack(anchor='w', pady=5)
        
        # Checkbox Salesforce
        cb_salesforce = tk.Checkbutton(
            checkbox_frame,
            text="💼 Processar Salesforce (CRIADO, RESOLVIDO, COMENTÁRIOS)",
            variable=self.var_salesforce,
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            activebackground=self.CORES['verde_leroy'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['verde_leroy'],
            relief='flat',
            highlightthickness=0,
            bd=0,
            cursor='hand2'
        )
        cb_salesforce.pack(anchor='w', pady=5)
        
        # Checkbox Produtividade
        cb_produtividade = tk.Checkbutton(
            checkbox_frame,
            text="📈 Processar Produtividade (VISÃO PRODUTIVA, TEMPO)",
            variable=self.var_produtividade,
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            activebackground=self.CORES['verde_leroy'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['verde_leroy'],
            relief='flat',
            highlightthickness=0,
            bd=0,
            cursor='hand2'
        )
        cb_produtividade.pack(anchor='w', pady=5)
        
        # Separador
        sep1 = tk.Frame(checkbox_frame, bg=self.CORES['cinza_medio'], height=1)
        sep1.pack(fill='x', pady=8)
        
        # Checkbox Verbose
        cb_verbose = tk.Checkbutton(
            checkbox_frame,
            text="🔍 Modo detalhado (logs completos)",
            variable=self.var_verbose,
            font=('Segoe UI', 9),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['texto_claro'],
            activebackground=self.CORES['azul_info'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['azul_info'],
            relief='flat',
            highlightthickness=0,
            bd=0,
            cursor='hand2'
        )
        cb_verbose.pack(anchor='w', pady=5)
        
        # ==== COLUNA DIREITA ====
        gestao_shadow = tk.Frame(superior_frame, bg=self.CORES['preto'])
        gestao_shadow.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        gestao_frame = tk.LabelFrame(
            gestao_shadow,
            text="  📁 Gestão de Arquivos  ",
            font=('Segoe UI', 12, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            relief='flat',
            bd=0,
            padx=18,
            pady=15,
            labelanchor='n'
        )
        gestao_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Configurar grid
        superior_frame.grid_columnconfigure(0, weight=1, uniform='col')
        superior_frame.grid_columnconfigure(1, weight=1, uniform='col')
        
        # Botões de gestão - PROFISSIONAL
        gestao_botoes_frame = tk.Frame(gestao_frame, bg=self.CORES['cinza_escuro'])
        gestao_botoes_frame.pack(fill='x', padx=10, pady=12)
        
        # Botão renomear arquivos (DESTAQUE)
        self.botao_renomear = ttk.Button(
            gestao_botoes_frame,
            text="🔁 Renomear Arquivos",
            style='VerdeClaro.TButton',
            command=self.renomear_arquivos,
            cursor='hand2'
        )
        self.botao_renomear.pack(fill='x', pady=(0, 6))
        
        # Botão verificar arquivos
        botao_verificar = ttk.Button(
            gestao_botoes_frame,
            text="📁 Verificar Arquivos",
            style='Info.TButton',
            command=self.verificar_arquivos,
            cursor='hand2'
        )
        botao_verificar.pack(fill='x', pady=4)
        
        # Botão abrir pasta dados
        botao_pasta = ttk.Button(
            gestao_botoes_frame,
            text="📂 Abrir Pasta Dados",
            style='Info.TButton',
            command=self.abrir_pasta_dados,
            cursor='hand2'
        )
        botao_pasta.pack(fill='x', pady=(4, 6))
        
        # Separador - PROFISSIONAL
        separador = tk.Frame(gestao_botoes_frame, height=1, bg=self.CORES['cinza_medio'])
        separador.pack(fill='x', pady=10)
        
        # Label planilhas
        label_planilhas = tk.Label(
            gestao_botoes_frame,
            text="🔗 Acesso Rápido às Planilhas",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco']
        )
        label_planilhas.pack(pady=(8, 10))
        
        # Botão planilha Genesys
        botao_planilha_genesys = ttk.Button(
            gestao_botoes_frame,
            text="📊 Planilha Genesys",
            style='VerdeClaro.TButton',
            command=lambda: self.abrir_planilha('genesys'),
            cursor='hand2'
        )
        botao_planilha_genesys.pack(fill='x', pady=(0, 4))
        
        # Botão planilha Salesforce
        botao_planilha_salesforce = ttk.Button(
            gestao_botoes_frame,
            text="💼 Planilha Salesforce",
            style='Info.TButton',
            command=lambda: self.abrir_planilha('salesforce'),
            cursor='hand2'
        )
        botao_planilha_salesforce.pack(fill='x', pady=(4, 4))
        
        # Botão planilha Produtividade (NOVO)
        botao_planilha_produtividade = ttk.Button(
            gestao_botoes_frame,
            text="📈 Planilha Produtividade",
            style='VerdeClaro.TButton',
            command=lambda: self.abrir_planilha('produtividade'),
            cursor='hand2'
        )
        botao_planilha_produtividade.pack(fill='x', pady=(4, 0))
        # Tooltips for quick access buttons
        try:
            ToolTip(botao_planilha_genesys, "Abrir a planilha oficial do Genesys no navegador")
            ToolTip(botao_planilha_salesforce, "Abrir a planilha oficial do Salesforce no navegador")
            ToolTip(botao_planilha_produtividade, "Abrir a planilha oficial de Produtividade")
            ToolTip(self.botao_renomear, "Executa renomeação inteligente dos arquivos na pasta data/")
        except Exception:
            pass
        
        # Frame para botões principais (COM SOMBRA) - PROFISSIONAL
        botoes_shadow = tk.Frame(controles_frame, bg=self.CORES['preto'])
        botoes_shadow.pack(fill='x', pady=(20, 0))
        
        botoes_frame = tk.Frame(botoes_shadow, bg=self.CORES['cinza_escuro'])
        botoes_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Padding interno
        botoes_inner = tk.Frame(botoes_frame, bg=self.CORES['cinza_escuro'])
        botoes_inner.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título da seção
        titulo_botoes = tk.Label(
            botoes_inner,
            text="⚡ Execução de Processos",
            font=('Segoe UI', 12, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco']
        )
        titulo_botoes.pack(pady=(0, 15))
        
        # Frame para botões individuais (primeira linha) - MAIOR espaçamento
        botoes_individuais_frame = tk.Frame(botoes_inner, bg=self.CORES['cinza_escuro'])
        botoes_individuais_frame.pack(fill='x', pady=(0, 15))
        
        # Botão Genesys individual (DESTAQUE VERDE)
        self.botao_genesys = ttk.Button(
            botoes_individuais_frame,
            text="📊 PROCESSAR GENESYS",
            style='Verde.TButton',
            command=lambda: self.executar_individual('genesys'),
            cursor='hand2'
        )
        self.botao_genesys.pack(side='left', expand=True, fill='both', padx=(0, 8))
        
        # Botão Salesforce individual (DESTAQUE VERDE)
        self.botao_salesforce = ttk.Button(
            botoes_individuais_frame,
            text="💼 PROCESSAR SALESFORCE", 
            style='Verde.TButton',
            command=lambda: self.executar_individual('salesforce'),
            cursor='hand2'
        )
        self.botao_salesforce.pack(side='left', expand=True, fill='both', padx=(8, 8))
        
        # Botão Produtividade individual (DESTAQUE VERDE)
        self.botao_produtividade = ttk.Button(
            botoes_individuais_frame,
            text="📈 PROCESSAR PRODUTIVIDADE", 
            style='Verde.TButton',
            command=lambda: self.executar_individual('produtividade'),
            cursor='hand2'
        )
        self.botao_produtividade.pack(side='left', expand=True, fill='both', padx=(8, 0))
        
        # Separador visual
        sep_botoes = tk.Frame(botoes_inner, bg=self.CORES['cinza_medio'], height=1)
        sep_botoes.pack(fill='x', pady=15)
        
        # Botão principal EXECUTAR (centralizado e MUITO MAIOR) - segunda linha - PROFISSIONAL
        botoes_principais_frame = tk.Frame(botoes_inner, bg=self.CORES['cinza_escuro'])
        botoes_principais_frame.pack(expand=True, pady=(0, 0))
        
        self.botao_executar = ttk.Button(
            botoes_principais_frame,
            text="🚀 EXECUTAR AUTOMAÇÃO COMPLETA",
            style='Verde.TButton',
            command=self.executar_automacao,
            cursor='hand2'
        )
        self.botao_executar.pack(side='left', padx=15, ipadx=35, ipady=10)
        
        # Botão limpar logs (MELHORADO)
        botao_limpar = ttk.Button(
            botoes_principais_frame,
            text="🧹 Limpar Logs",
            style='Laranja.TButton',
            command=self.limpar_logs,
            cursor='hand2'
        )
        botao_limpar.pack(side='left', padx=15)
        
        # Status e barra de progresso melhorados (COM CARD) - PROFISSIONAL
        status_shadow = tk.Frame(controles_frame, bg=self.CORES['preto'])
        status_shadow.pack(fill='x', pady=(15, 0))
        
        status_frame = tk.LabelFrame(
            status_shadow,
            text="  📊 Status do Sistema  ",
            font=('Segoe UI', 11, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['branco'],
            relief='flat',
            bd=0,
            padx=20,
            pady=12,
            labelanchor='n'
        )
        status_frame.pack(fill='x', padx=2, pady=2)
        
        # Label de status melhorado (MAIOR) - PROFISSIONAL
        self.status_label = tk.Label(
            status_frame,
            text="💚 Sistema pronto para execução",
            font=('Segoe UI', 12, 'bold'),
            bg=self.CORES['cinza_escuro'],
            fg=self.CORES['verde_leroy']
        )
        self.status_label.pack(anchor='w', pady=(10, 12))
        
        # Barra de progresso com estilo melhorado (MAIS GROSSA)
        self.progresso = ttk.Progressbar(
            status_frame,
            style='Verde.Horizontal.TProgressbar',
            mode='indeterminate',
            length=500 
        )
        self.progresso.pack(fill='x', pady=(0, 10), ipady=6)
    
    def criar_area_logs(self):
        """Cria área de logs compacta e MODERNA"""
        # Sombra do card
        logs_shadow = tk.Frame(self.container_principal, bg='#D0D0D0')
        logs_shadow.pack(fill='x', padx=20, pady=(8, 15))
        
        logs_frame = tk.LabelFrame(
            logs_shadow,
            text="  📄 Logs de Execução  ",
            font=('Segoe UI', 11, 'bold'),
            bg='#1E1E1E',
            fg='#00D9FF',
            relief='flat',
            bd=0,
            padx=8,
            pady=8,
            labelanchor='n'
        )
        logs_frame.pack(fill='x', padx=2, pady=2)
        logs_frame.pack_propagate(False)
        logs_frame.configure(height=140)  # Altura aumentada
        
        # Frame interno para melhor organização
        logs_content = tk.Frame(logs_frame, bg='#1E1E1E')
        logs_content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Área de texto compacta (ESTILO TERMINAL MODERNO)
        self.texto_log = scrolledtext.ScrolledText(
            logs_content,
            font=('Cascadia Code', 9),
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='#00FF00',
            selectbackground='#264F78',
            selectforeground='white',
            wrap='word',
            height=6,
            width=100,
            relief='flat',
            bd=0,
            padx=8,
            pady=6,
            state='normal'
        )
        self.texto_log.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Inserir texto de teste imediatamente
        self.texto_log.insert('end', "🔧 Sistema iniciando...\n")
        self.texto_log.see('end')
        
        # Configurar tags para cores melhoradas e VIBRANTES
        self.texto_log.tag_configure('sucesso', foreground='#4EC9B0', font=('Cascadia Code', 9, 'bold'))
        self.texto_log.tag_configure('erro', foreground='#F48771', font=('Cascadia Code', 9, 'bold'))
        self.texto_log.tag_configure('info', foreground='#9CDCFE', font=('Cascadia Code', 9))
        self.texto_log.tag_configure('aviso', foreground='#DCDCAA', font=('Cascadia Code', 9, 'bold'))
        self.texto_log.tag_configure('destaque', foreground='#C586C0', font=('Cascadia Code', 9, 'bold'))
        
        # Forçar atualização antes de adicionar mensagens
        self.janela_principal.update_idletasks()
        
        # Exibir mensagens iniciais imediatamente
        self.exibir_mensagens_iniciais()
    
    def exibir_mensagens_iniciais(self):
        """Exibe mensagens iniciais no log"""
        self.log_mensagem("🎯 Interface Visual Leroy Merlin v2.3 iniciada com sucesso!", 'destaque')
        self.log_mensagem("📋 Configure as opções acima e execute a automação", 'info')
        self.log_mensagem("🔗 NOVO: Use os links rápidos para acessar as planilhas diretamente", 'aviso')
        self.log_mensagem("📈 NOVIDADE: Automação de Produtividade adicionada!", 'sucesso')
        self.log_mensagem("✨ Execução individual + Encoding robusto + Coloração completa + Correção .0", 'aviso')
        self.log_mensagem("🎨 Agora todas as linhas da planilha são pintadas com verde Leroy Merlin!", 'sucesso')
        self.log_mensagem("-" * 70, 'info')
    
    def criar_footer(self):
        """Cria rodapé MODERNO com gradiente"""
        # Linha decorativa superior
        linha_top = tk.Frame(self.container_principal, bg=self.CORES['laranja'], height=3)
        linha_top.pack(fill='x', pady=(8, 0))
        
        footer_frame = tk.Frame(self.container_principal, bg=self.CORES['verde_escuro'], height=50)
        footer_frame.pack(fill='x', pady=0)
        footer_frame.pack_propagate(False)
        
        # Informações do sistema - layout mais limpo
        info_frame = tk.Frame(footer_frame, bg=self.CORES['verde_escuro'])
        info_frame.pack(expand=True, fill='both')
        
        # Data/hora (MAIOR)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_label = tk.Label(
            info_frame,
            text=f"⏰ {agora}",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['verde_escuro'],
            fg=self.CORES['branco']
        )
        data_label.pack(side='left', padx=25, pady=15)
        
        # Versão (centralizada) - MAIOR
        versao_label = tk.Label(
            info_frame,
            text="✨ Automação Boletins Leroy Merlin v2.4 • RPA System",
            font=('Segoe UI', 11, 'bold'),
            bg=self.CORES['verde_escuro'],
            fg=self.CORES['branco']
        )
        versao_label.pack(expand=True, pady=15)
        
        # Status (direita) - MAIOR
        status_label = tk.Label(
            info_frame,
            text="✅ Pronto para uso",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['verde_escuro'],
            fg='#A5D6A7'
        )
        status_label.pack(side='right', padx=25, pady=15)
    
    def configurar_scroll(self):
        """Configura os eventos de scroll da interface"""
        # Atualizar scroll region após criar todos os elementos
        self.janela_principal.after(100, self.atualizar_scroll)
    
    def atualizar_scroll(self, event=None):
        """Atualiza a região de scroll baseada no conteúdo"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def redimensionar_canvas(self, event):
        """Redimensiona o canvas quando a janela muda de tamanho"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def scroll_mouse(self, event):
        """Habilita scroll com mouse wheel"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.janela_principal.update_idletasks()
        largura = self.janela_principal.winfo_width()
        altura = self.janela_principal.winfo_height()
        x = (self.janela_principal.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_principal.winfo_screenheight() // 2) - (altura // 2)
        self.janela_principal.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def log_mensagem(self, mensagem, tag=None):
        """Adiciona mensagem ao log com timestamp e cores"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            mensagem_completa = f"[{timestamp}] {mensagem}\n"
            
            # Debug: imprimir no console também
            print(f"LOG: {mensagem_completa.strip()}")
            
            # Garantir que o widget existe
            if hasattr(self, 'texto_log') and self.texto_log:
                # Sempre manter habilitado para inserção
                self.texto_log.configure(state='normal')
                self.texto_log.insert('end', mensagem_completa, tag)
                self.texto_log.see('end')  # Auto-scroll para o final
                # Não desabilitar mais - deixar sempre editável
                self.janela_principal.update()  # Atualização imediata
            else:
                print("Widget texto_log não encontrado!")
        except Exception as e:
            print(f"Erro ao adicionar log: {e}")  # Fallback para console
    
    def verificar_arquivos(self):
        """Verifica arquivos CSV disponíveis"""
        self.log_mensagem("🔍 Verificando arquivos disponíveis...", 'info')
        
        data_dir = os.path.join(current_dir, 'data')
        
        if not os.path.exists(data_dir):
            self.log_mensagem("❌ Pasta 'data' não encontrada!", 'erro')
            messagebox.showerror("Erro", "Pasta 'data' não encontrada!\nCrie a pasta e adicione os arquivos CSV.")
            return
        
        arquivos_csv = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
        
        if not arquivos_csv:
            self.log_mensagem("⚠️ Nenhum arquivo CSV encontrado na pasta data/", 'aviso')
            messagebox.showwarning("Aviso", "Nenhum arquivo CSV encontrado na pasta data/")
        else:
            self.log_mensagem(f"📁 Encontrados {len(arquivos_csv)} arquivos CSV:", 'sucesso')
            for arquivo in sorted(arquivos_csv):
                tamanho = os.path.getsize(os.path.join(data_dir, arquivo))
                tamanho_mb = tamanho / (1024 * 1024)
                self.log_mensagem(f"   📄 {arquivo} ({tamanho_mb:.2f} MB)", 'info')
    
    def abrir_pasta_dados(self):
        """Abre a pasta de dados no explorer"""
        data_dir = os.path.join(current_dir, 'data')
        
        if not os.path.exists(data_dir):
            # Criar pasta se não existir
            os.makedirs(data_dir)
            self.log_mensagem("📁 Pasta 'data' criada", 'info')
        
        try:
            # Abrir pasta no Windows Explorer
            os.startfile(data_dir)
            self.log_mensagem("📂 Pasta de dados aberta", 'sucesso')
        except Exception as e:
            self.log_mensagem(f"❌ Erro ao abrir pasta: {e}", 'erro')
    
    def abrir_url(self, url):
        """Abre URL no navegador padrão"""
        import webbrowser
        try:
            webbrowser.open(url)
            self.log_mensagem(f"🌐 Abrindo planilha no navegador...", 'info')
        except Exception as e:
            self.log_mensagem(f"❌ Erro ao abrir link: {e}", 'erro')
    
    def abrir_planilha(self, tipo):
        """Abre planilha oficial no navegador"""
        urls = {
            'genesys': 'https://docs.google.com/spreadsheets/d/1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE/edit?gid=282816795#gid=282816795',      # Planilha oficial Genesys
            'salesforce': 'https://docs.google.com/spreadsheets/d/1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk/edit?gid=1897032278#gid=1897032278',  # Planilha oficial Salesforce
            'produtividade': 'https://docs.google.com/spreadsheets/d/1nzSa4cnPOPau1-BF221Vc6VEvUiFe6D1suebCcQmAT4'   # Planilha oficial Produtividade
        }
        
        if tipo in urls:
            self.abrir_url(urls[tipo])
            self.log_mensagem(f"🔗 Planilha {tipo.title()} aberta no navegador", 'sucesso')
        else:
            self.log_mensagem(f"❌ Tipo de planilha desconhecido: {tipo}", 'erro')
    
    def limpar_logs(self):
        """Limpa a área de logs"""
        self.texto_log.configure(state='normal')
        self.texto_log.delete(1.0, 'end')
        self.texto_log.configure(state='disabled')
        self.log_mensagem("🧹 Logs limpos", 'info')
        self.log_mensagem("💚 Sistema pronto para nova operação", 'sucesso')
    
    def renomear_arquivos(self):
        """Executa renomeação inteligente de arquivos"""
        if self.executando:
            mb.showwarning("Aviso", "Operação já está em execução!")
            return
        
        # Primeiro mostrar preview
        self.log_mensagem("🔍 Analisando arquivos para renomeação...", 'info')
        
        try:
            preview = self.renomeador.preview_renomeacoes()
            
            if not preview['renomeacoes']:
                self.log_mensagem("✅ Todos os arquivos já estão com nomes padronizados!", 'sucesso')
                mb.showinfo("Informação", "Todos os arquivos já estão com nomes padronizados!")
                return
            
            # Mostrar preview das renomeações
            preview_texto = f"📝 PREVIEW DE RENOMEAÇÕES:\n\n"
            for item in preview['renomeacoes']:
                preview_texto += f"📄 {item['nome_original']}\n"
                preview_texto += f"   ➡️  {item['nome_novo']}\n"
                preview_texto += f"   🎯 {item['tipo_detectado']} ({item['tamanho_mb']} MB)\n\n"
            
            self.log_mensagem("📋 Preview das renomeações:", 'destaque')
            for item in preview['renomeacoes']:
                self.log_mensagem(f"   📄 {item['nome_original']}", 'info')
                self.log_mensagem(f"      ➡️  {item['nome_novo']}", 'aviso')
                self.log_mensagem(f"      🎯 {item['tipo_detectado']} ({item['tamanho_mb']} MB)", 'sucesso')
            
            # Perguntar confirmação
            resposta = mb.askyesno(
                "Confirmar Renomeação", 
                f"Encontrados {len(preview['renomeacoes'])} arquivos para renomear.\n\n"
                f"Deseja executar as renomeações?\n\n"
                f"(Os nomes originais serão salvos no histórico)"
            )
            
            if resposta:
                self.log_mensagem("🚀 Executando renomeações...", 'destaque')
                
                # Executar renomeações
                resultado = self.renomeador.executar_renomeacoes()
                
                if resultado['sucesso']:
                    self.log_mensagem(f"✅ Renomeação concluída com sucesso!", 'sucesso')
                    self.log_mensagem(f"📊 {resultado['sucessos']} arquivos renomeados", 'info')
                    
                    if resultado['falhas'] > 0:
                        self.log_mensagem(f"⚠️ {resultado['falhas']} arquivos com problemas", 'aviso')
                    
                    # Mostrar resultados detalhados
                    for item in resultado['renomeacoes']:
                        if item['status'] == 'sucesso':
                            self.log_mensagem(f"   ✅ {item['nome_novo']}", 'sucesso')
                        else:
                            self.log_mensagem(f"   ❌ {item['nome_original']} - {item.get('erro', 'Erro desconhecido')}", 'erro')
                    
                    mb.showinfo("Sucesso", f"Renomeação concluída!\n\n✅ {resultado['sucessos']} sucessos\n❌ {resultado['falhas']} falhas")
                else:
                    self.log_mensagem("❌ Falha na renomeação", 'erro')
                    mb.showerror("Erro", "Falha ao renomear arquivos!")
            else:
                self.log_mensagem("🚫 Renomeação cancelada pelo usuário", 'aviso')
                
        except Exception as e:
            self.log_mensagem(f"❌ Erro na renomeação: {str(e)}", 'erro')
            mb.showerror("Erro", f"Erro na renomeação:\n{str(e)}")
    
    def executar_individual(self, sistema):
        """Executa apenas um sistema específico (genesys, salesforce ou produtividade)"""
        if self.executando:
            messagebox.showwarning("Aviso", "Automação já está em execução!")
            return
        
        # Confirmar execução
        sistemas_nomes = {
            'genesys': "📊 Genesys",
            'salesforce': "💼 Salesforce", 
            'produtividade': "📈 Produtividade"
        }
        sistema_nome = sistemas_nomes.get(sistema, sistema)
        
        resposta = messagebox.askyesno(
            f"Confirmar Execução - {sistema_nome}",
            f"Executar automação apenas para {sistema_nome}?\n\n"
            f"Isso processará somente os dados relacionados ao {sistema.upper()}."
        )
        
        if not resposta:
            return
        
        # Temporariamente definir checkboxes para executar apenas o sistema escolhido
        checkbox_original_genesys = self.var_genesys.get()
        checkbox_original_salesforce = self.var_salesforce.get()
        checkbox_original_produtividade = self.var_produtividade.get()
        
        # Configurar para executar apenas o sistema selecionado
        self.var_genesys.set(sistema == 'genesys')
        self.var_salesforce.set(sistema == 'salesforce')
        self.var_produtividade.set(sistema == 'produtividade')
        
        try:
            # Iniciar execução em thread separada
            thread = threading.Thread(
                target=self._executar_automacao_individual_thread, 
                args=(sistema, checkbox_original_genesys, checkbox_original_salesforce, checkbox_original_produtividade),
                daemon=True
            )
            thread.start()
        except Exception as e:
            # Restaurar checkboxes originais em caso de erro
            self.var_genesys.set(checkbox_original_genesys)
            self.var_salesforce.set(checkbox_original_salesforce)
            self.var_produtividade.set(checkbox_original_produtividade)
            messagebox.showerror("Erro", f"Erro ao iniciar execução: {str(e)}")
    
    def _executar_automacao_individual_thread(self, sistema, original_genesys, original_salesforce, original_produtividade):
        """Thread específica para execução individual"""
        try:
            # Usar o mesmo método de execução, mas com parâmetros específicos
            self._executar_automacao_thread()
        finally:
            # Sempre restaurar checkboxes originais no final
            self.var_genesys.set(original_genesys)
            self.var_salesforce.set(original_salesforce)
            self.var_produtividade.set(original_produtividade)
    
    def executar_automacao(self):
        """Executa a automação em thread separada"""
        if self.executando:
            messagebox.showwarning("Aviso", "Automação já está em execução!")
            return
        
        # Verificar se pelo menos uma opção está selecionada
        if not self.var_genesys.get() and not self.var_salesforce.get() and not self.var_produtividade.get():
            messagebox.showerror("Erro", "Selecione pelo menos uma opção (Genesys, Salesforce ou Produtividade)!")
            return
        
        # Iniciar execução em thread separada
        thread = threading.Thread(target=self._executar_automacao_thread, daemon=True)
        thread.start()
    
    def _executar_automacao_thread(self):
        """Thread para execução da automação com encoding robusto"""
        try:
            self.executando = True
            
            # Atualizar interface
            self.botao_executar.configure(text="⏳ EXECUTANDO...", state='disabled')
            self.botao_genesys.configure(state='disabled')
            self.botao_salesforce.configure(state='disabled')
            self.botao_produtividade.configure(state='disabled')
            self.botao_renomear.configure(state='disabled')
            self.status_label.configure(text="🔄 Executando automação...", fg=self.CORES['laranja'])
            self.progresso.start()
            
            self.log_mensagem("🚀 Iniciando automação...", 'sucesso')
            
            # Construir comando
            comando = ["python", "main.py"]
            
            # Adicionar opções baseadas nos checkboxes (lógica melhorada para três sistemas)
            sistemas_selecionados = []
            if self.var_genesys.get():
                sistemas_selecionados.append("genesys")
            if self.var_salesforce.get():
                sistemas_selecionados.append("salesforce")
            if self.var_produtividade.get():
                sistemas_selecionados.append("produtividade")
            
            # Se apenas um sistema está selecionado, usar parâmetro específico
            if len(sistemas_selecionados) == 1:
                comando.append(f"--{sistemas_selecionados[0]}")
                self.log_mensagem(f"🎯 Modo: Apenas {sistemas_selecionados[0].title()}", 'info')
            else:
                # Se múltiplos ou todos, não adicionar parâmetro específico (processará todos selecionados)
                sistemas_texto = " + ".join([s.title() for s in sistemas_selecionados])
                self.log_mensagem(f"🎯 Modo: {sistemas_texto}", 'info')
            
            if self.var_verbose.get():
                comando.append("--verbose")
                self.log_mensagem("🔍 Modo detalhado ativado", 'info')
            
            # Configurar variáveis de ambiente para encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'
            
            self.log_mensagem(f"📋 Comando: {' '.join(comando)}", 'info')
            
            # Executar comando com encoding robusto
            processo = subprocess.Popen(
                comando,
                cwd=current_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # Capturar stderr separadamente
                text=True,
                encoding='utf-8',
                errors='replace',  # Substituir caracteres inválidos
                universal_newlines=True,
                env=env,
                bufsize=0  # Sem buffer para saída em tempo real
            )
            
            # Ler saída em tempo real (stdout e stderr)
            import select
            import time
            
            # Para Windows, ler linha por linha
            linha_count = 0
            while processo.poll() is None:
                # Ler stdout
                if processo.stdout.readable():
                    linha = processo.stdout.readline()
                    if linha:
                        linha = linha.strip()
                        if linha:
                            linha_count += 1
                            # Detectar tipo de mensagem baseado em emojis/símbolos
                            if '✅' in linha or 'sucesso' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'sucesso')
                            elif '❌' in linha or 'erro' in linha.lower() or 'falha' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'erro')
                            elif '⚠️' in linha or 'aviso' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'aviso')
                            elif '🔍' in linha or '📊' in linha or '💼' in linha:
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'info')
                            elif linha.startswith('=') or linha.startswith('-'):
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'destaque')
                            else:
                                self.log_mensagem(f"[{linha_count:03d}] {linha}")
                
                time.sleep(0.01)  # Pequena pausa para não sobrecarregar CPU
            
            # Ler qualquer saída restante
            stdout_restante, stderr_output = processo.communicate()
            
            if stdout_restante:
                for linha in stdout_restante.split('\n'):
                    linha = linha.strip()
                    if linha:
                        linha_count += 1
                        self.log_mensagem(f"[{linha_count:03d}] {linha}")
            
            # Capturar stderr se houver
            if stderr_output:
                self.log_mensagem("🔍 Saída de erro (stderr):", 'aviso')
                for linha in stderr_output.split('\n'):
                    linha = linha.strip()
                    if linha:
                        linha_count += 1
                        self.log_mensagem(f"[ERR{linha_count:03d}] {linha}", 'erro')
            
            # Verificar código de retorno
            if processo.returncode == 0:
                self.log_mensagem("🎉 Automação concluída com sucesso!", 'sucesso')
                self.status_label.configure(text="✅ Automação concluída com sucesso!", fg=self.CORES['verde_leroy'])
                
                # Registrar execução bem-sucedida com dados estimados
                # (aqui você pode melhorar pegando dados reais do log/output)
                registros = self.extrair_total_registros(stdout_restante)
                tempo = self.extrair_tempo_execucao(stdout_restante)
                self.registrar_execucao(sucesso=True, registros_processados=registros, tempo_segundos=tempo)
                
                messagebox.showinfo("Sucesso", "Automação concluída com sucesso! ✅")
            else:
                self.log_mensagem(f"❌ Automação falhou (código {processo.returncode})", 'erro')
                self.status_label.configure(text="❌ Automação falhou", fg=self.CORES['laranja'])
                
                # Registrar execução com falha
                self.registrar_execucao(sucesso=False, registros_processados=0, tempo_segundos=0)
                
                # Construir mensagem de erro mais detalhada
                erro_msg = f"Automação falhou (código {processo.returncode})"
                if stderr_output:
                    erro_msg += f"\n\nDetalhes do erro:\n{stderr_output[:500]}"  # Limitar tamanho
                
                messagebox.showerror("Erro", erro_msg)
                
        except Exception as e:
            error_msg = str(e)
            self.log_mensagem(f"❌ Erro na execução: {error_msg}", 'erro')
            self.status_label.configure(text="❌ Erro na execução", fg=self.CORES['laranja'])
            
            # Tentar capturar mais detalhes do erro
            import traceback
            traceback_info = traceback.format_exc()
            self.log_mensagem(f"🔍 Traceback completo:", 'info')
            for linha in traceback_info.split('\n'):
                if linha.strip():
                    self.log_mensagem(f"    {linha}", 'erro')
            
            messagebox.showerror("Erro", f"Erro na execução:\n{error_msg}\n\nVerifique o log para mais detalhes.")
            
        finally:
            # Restaurar interface
            self.executando = False
            self.botao_executar.configure(text="🚀 EXECUTAR AUTOMAÇÃO COMPLETA", state='normal')
            self.botao_genesys.configure(state='normal')
            self.botao_salesforce.configure(state='normal')
            self.botao_produtividade.configure(state='normal')
            self.botao_renomear.configure(state='normal')
            self.progresso.stop()
            if not self.status_label.cget('text').startswith(('❌', '✅')):
                self.status_label.configure(text="💚 Pronto para nova execução", fg=self.CORES['verde_escuro'])
    
    def executar(self):
        """Inicia a interface"""
        try:
            self.janela_principal.mainloop()
        except KeyboardInterrupt:
            print("Interface encerrada pelo usuário")
        except Exception as e:
            print(f"Erro na interface: {e}")

def main():
    """Função principal"""
    try:
        app = AutomacaoLeroyMerlinGUI()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar interface: {e}")

if __name__ == "__main__":
    main()