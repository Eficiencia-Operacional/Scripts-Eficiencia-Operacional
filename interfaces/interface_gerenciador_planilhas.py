#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 INTERFACE VISUAL - GERENCIADOR DE PLANILHAS
Interface gráfica moderna para gerenciar configurações das planilhas

Funcionalidades:
- Dashboard com status das planilhas
- Atualização visual de IDs
- Histórico de mudanças
- Backup e restauração
- Validação em tempo real

Uso:
    python scripts/interface_gerenciador_visual.py
"""

import sys
import os
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, io.UnsupportedOperation):
        pass

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from datetime import datetime
import webbrowser
from pathlib import Path

# Adicionar o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

# Importar gerenciador
from scripts.gerenciador_planilhas import GerenciadorPlanilhas

class InterfaceGerenciadorVisual:
    """Interface visual para o gerenciador de planilhas"""
    
    def __init__(self):
        # Cores do tema moderno - Gradiente escuro profissional
        self.CORES = {
            'primary': '#6366F1',       # Indigo vibrante
            'primary_dark': '#4F46E5',  # Indigo escuro
            'secondary': '#EC4899',     # Pink vibrante
            'accent': '#F59E0B',        # Amber destaque
            'success': '#10B981',       # Esmeralda sucesso
            'warning': '#F59E0B',       # Amber aviso
            'error': '#EF4444',         # Vermelho erro
            'dark': '#1F2937',          # Cinza escuro
            'darker': '#111827',        # Quase preto
            'light': '#F9FAFB',         # Cinza bem claro
            'medium': '#6B7280',        # Cinza médio
            'white': '#FFFFFF',         # Branco
            'border': '#E5E7EB',        # Borda sutil
            'hover': '#EEF2FF',         # Hover suave
            'card': '#FFFFFF',          # Card branco
            'shadow': '#00000015',      # Sombra sutil
            'text': '#111827',          # Texto escuro
            'text_light': '#6B7280',    # Texto claro
            'gradient_start': '#6366F1', # Início gradiente
            'gradient_end': '#8B5CF6'    # Fim gradiente (roxo)
        }
        
        # Inicializar gerenciador
        self.gp = GerenciadorPlanilhas()
        
        # Variáveis de estado
        self.planilha_selecionada = None
        self.dados_planilhas = {}
        
        # Criar interface
        self.criar_janela_principal()
        self.criar_notebook()
        self.criar_aba_dashboard()
        self.criar_aba_atualizar()
        self.criar_aba_historico()
        self.criar_aba_backups()
        
        # Carregar dados iniciais
        self.carregar_dados()
        
    def criar_janela_principal(self):
        """Cria a janela principal com design moderno"""
        self.root = tk.Tk()
        self.root.title("🎨 Gerenciador de Planilhas - Leroy Merlin | Eficiência Operacional")
        self.root.geometry("1400x850")
        self.root.configure(bg=self.CORES['light'])
        self.root.minsize(1200, 700)
        
        # Ícone da janela
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configurar_estilos()
        
        # Header
        self.criar_header()
        
    def configurar_estilos(self):
        """Configura estilos modernos e elegantes"""
        # Notebook com transições suaves
        self.style.configure('Custom.TNotebook', 
                           background=self.CORES['light'],
                           borderwidth=0,
                           tabmargins=[0, 0, 0, 0])
        
        self.style.configure('Custom.TNotebook.Tab',
                           background=self.CORES['card'],
                           foreground=self.CORES['text_light'],
                           padding=[24, 12],
                           font=('Segoe UI', 10, 'bold'),
                           borderwidth=0,
                           focuscolor='')
        
        self.style.map('Custom.TNotebook.Tab',
                      background=[('selected', self.CORES['primary']),
                                 ('active', self.CORES['hover'])],
                      foreground=[('selected', self.CORES['white']),
                                 ('active', self.CORES['primary'])])
        
        # Botões com elevação e hover
        self.style.configure('Primary.TButton',
                           background=self.CORES['primary'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 10),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Primary.TButton',
                      background=[('active', self.CORES['primary_dark']),
                                 ('pressed', self.CORES['primary_dark'])],
                      relief=[('pressed', 'flat')])
        
        self.style.configure('Success.TButton',
                           background=self.CORES['success'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(16, 8),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Success.TButton',
                      background=[('active', '#059669')])
        
        self.style.configure('Warning.TButton',
                           background=self.CORES['warning'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(16, 8),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Warning.TButton',
                      background=[('active', '#D97706')])
        
        self.style.configure('Danger.TButton',
                           background=self.CORES['error'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(16, 8),
                           relief='flat',
                           borderwidth=0)
        
        # Cards com sombra
        self.style.configure('Card.TFrame',
                           background=self.CORES['card'],
                           relief='flat',
                           borderwidth=0)
        
    def criar_header(self):
        """Cria o cabeçalho com gradiente"""
        # Frame principal com gradiente simulado
        header_frame = tk.Frame(self.root, bg=self.CORES['primary'], height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container do header
        header_content = tk.Frame(header_frame, bg=self.CORES['primary'])
        header_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Título principal com emoji grande
        titulo = tk.Label(
            header_content,
            text="🎨 Gerenciador de Planilhas",
            font=('Segoe UI', 24, 'bold'),
            bg=self.CORES['primary'],
            fg=self.CORES['white']
        )
        titulo.pack(side='left')
        
        # Subtítulo elegante
        subtitulo = tk.Label(
            header_content,
            text="Sistema Centralizado de Configurações • Eficiência Operacional",
            font=('Segoe UI', 11),
            bg=self.CORES['primary'],
            fg='#E0E7FF'
        )
        subtitulo.pack(side='left', padx=(15, 0), pady=(5, 0))
        
        # Badge de status no canto direito
        status_frame = tk.Frame(header_content, bg=self.CORES['primary'])
        status_frame.pack(side='right')
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Sistema Ativo",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['primary'],
            fg=self.CORES['success']
        )
        self.status_label.pack(side='right')
        
    def criar_notebook(self):
        """Cria o notebook com abas"""
        # Container principal
        main_container = tk.Frame(self.root, bg=self.CORES['light'])
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Notebook
        self.notebook = ttk.Notebook(main_container, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
    def criar_aba_dashboard(self):
        """Cria aba do dashboard com design moderno"""
        # Frame da aba com fundo elegante
        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text='📊 Dashboard')
        
        # Container principal com padding
        main_container = tk.Frame(self.aba_dashboard, bg=self.CORES['light'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Grid responsivo
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=1)
        
        # Cards modernos de estatísticas (3 colunas)
        self.criar_card_estatisticas_moderno(main_container)
        
        # Card de planilhas (largo, 2 colunas)
        self.criar_card_planilhas(main_container)
        
        # Card de ações rápidas (1 coluna)
        self.criar_card_acoes_rapidas(main_container)
        
    def criar_card_estatisticas_moderno(self, parent):
        """Cria cards de estatísticas com design moderno e colorido"""
        # Card 1: Total de Planilhas (Roxo)
        card1 = self.criar_stat_card(parent, "📊", "Total de Planilhas", "0", 
                                     self.CORES['primary'], 0)
        
        # Card 2: Atualizações (Verde)
        card2 = self.criar_stat_card(parent, "🔄", "Últimas Atualizações", "0", 
                                     self.CORES['success'], 1)
        
        # Card 3: Backups (Amber)
        card3 = self.criar_stat_card(parent, "💾", "Backups Disponíveis", "0", 
                                     self.CORES['warning'], 2)
    
    def criar_stat_card(self, parent, emoji, titulo, valor, cor, coluna):
        """Cria um card de estatística individual com sombra e hover"""
        # Frame com sombra simulada
        shadow_frame = tk.Frame(parent, bg='#E5E7EB', bd=0)
        shadow_frame.grid(row=0, column=coluna, sticky='ew', padx=10, pady=(0, 20))
        
        # Card principal
        card = tk.Frame(shadow_frame, bg=self.CORES['card'], bd=0)
        card.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Container interno
        inner = tk.Frame(card, bg=self.CORES['card'])
        inner.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Emoji grande no topo
        emoji_label = tk.Label(inner, text=emoji, font=('Segoe UI', 40),
                              bg=self.CORES['card'], fg=cor)
        emoji_label.pack(pady=(0, 10))
        
        # Valor grande
        valor_label = tk.Label(inner, text=valor, font=('Segoe UI', 32, 'bold'),
                              bg=self.CORES['card'], fg=self.CORES['text'])
        valor_label.pack()
        
        # Título pequeno
        titulo_label = tk.Label(inner, text=titulo, font=('Segoe UI', 11),
                               bg=self.CORES['card'], fg=self.CORES['text_light'])
        titulo_label.pack(pady=(5, 0))
        
        # Salvar referência para atualizar depois
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[titulo] = valor_label
        
        return card
        
    def criar_card_estatisticas(self):
        """Cria card com estatísticas"""
        card_frame = ttk.Frame(self.aba_dashboard, style='Card.TFrame')
        card_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        
        # Título do card
        titulo = tk.Label(card_frame, text="📈 Estatísticas do Sistema", 
                         font=('Segoe UI', 14, 'bold'),
                         bg=self.CORES['white'], fg=self.CORES['text'])
        titulo.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Container das estatísticas
        stats_frame = tk.Frame(card_frame, bg=self.CORES['white'])
        stats_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Estatísticas individuais
        self.criar_stat_box(stats_frame, "Total de Planilhas", "0", "📊", 0)
        self.criar_stat_box(stats_frame, "Últimas Atualizações", "0", "🔄", 1)
        self.criar_stat_box(stats_frame, "Backups Disponíveis", "0", "💾", 2)
        self.criar_stat_box(stats_frame, "Status Sistema", "OK", "✅", 3)
        
    def criar_stat_box(self, parent, titulo, valor, emoji, coluna):
        """Cria uma caixa de estatística"""
        box_frame = tk.Frame(parent, bg=self.CORES['light'], relief='raised', bd=1)
        box_frame.grid(row=0, column=coluna, padx=5, pady=5, sticky='ew')
        parent.grid_columnconfigure(coluna, weight=1)
        
        # Emoji
        emoji_label = tk.Label(box_frame, text=emoji, font=('Segoe UI Emoji', 20),
                              bg=self.CORES['light'], fg=self.CORES['primary'])
        emoji_label.pack(pady=(10, 5))
        
        # Valor
        valor_label = tk.Label(box_frame, text=valor, font=('Segoe UI', 16, 'bold'),
                              bg=self.CORES['light'], fg=self.CORES['text'])
        valor_label.pack()
        
        # Título
        titulo_label = tk.Label(box_frame, text=titulo, font=('Segoe UI', 9),
                               bg=self.CORES['light'], fg=self.CORES['text_light'])
        titulo_label.pack(pady=(0, 10))
        
        # Salvar referência do label de valor para atualização
        setattr(self, f'stat_{coluna}_label', valor_label)
        
    def criar_card_planilhas(self, parent):
        """Cria card moderno com lista de planilhas"""
        # Shadow frame
        shadow_frame = tk.Frame(parent, bg='#E5E7EB', bd=0)
        shadow_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=(0, 20))
        parent.grid_rowconfigure(1, weight=1)
        
        # Card principal
        card_frame = tk.Frame(shadow_frame, bg=self.CORES['card'], bd=0)
        card_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Header do card
        header = tk.Frame(card_frame, bg=self.CORES['card'])
        header.pack(fill='x', padx=25, pady=(20, 15))
        
        # Título do card
        titulo = tk.Label(header, text="📋 Planilhas Configuradas", 
                         font=('Segoe UI', 16, 'bold'),
                         bg=self.CORES['card'], fg=self.CORES['text'])
        titulo.pack(side='left')
        
        # Botão de recarregar
        btn_reload = ttk.Button(header, text="🔄 Recarregar", 
                               style='Primary.TButton',
                               command=self.carregar_dados)
        btn_reload.pack(side='right')
        
        # Container da lista com scroll
        list_container = tk.Frame(card_frame, bg=self.CORES['card'])
        list_container.pack(fill='both', expand=True, padx=25, pady=(0, 20))
        
        # Canvas e scrollbar
        canvas = tk.Canvas(list_container, bg=self.CORES['card'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient='vertical', 
                                  command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.CORES['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.planilhas_frame = scrollable_frame
        
    def criar_item_planilha_moderno(self, parent, chave, info):
        """Cria um item de planilha com design moderno e hover"""
        # Frame do item com hover
        item_frame = tk.Frame(parent, bg=self.CORES['card'], cursor='hand2',
                             relief='solid', bd=1, highlightthickness=0)
        item_frame.pack(fill='x', pady=5)
        
        # Padding interno
        inner = tk.Frame(item_frame, bg=self.CORES['card'])
        inner.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Emoji e nome
        top_frame = tk.Frame(inner, bg=self.CORES['card'])
        top_frame.pack(fill='x')
        
        # Emoji grande
        emoji_map = {
            'genesys': '📞',
            'salesforce': '💼',
            'produtividade': '📈',
            'power_bi': '📊',
            'autoservico': '🤖'
        }
        emoji = emoji_map.get(chave.split('_')[0], '📄')
        
        emoji_label = tk.Label(top_frame, text=emoji, font=('Segoe UI', 24),
                              bg=self.CORES['card'])
        emoji_label.pack(side='left', padx=(0, 15))
        
        # Nome e descrição
        text_frame = tk.Frame(top_frame, bg=self.CORES['card'])
        text_frame.pack(side='left', fill='x', expand=True)
        
        nome_label = tk.Label(text_frame, text=info.get('nome', chave),
                             font=('Segoe UI', 13, 'bold'),
                             bg=self.CORES['card'], fg=self.CORES['text'],
                             anchor='w')
        nome_label.pack(fill='x')
        
        desc_label = tk.Label(text_frame, text=info.get('descricao', ''),
                             font=('Segoe UI', 10),
                             bg=self.CORES['card'], fg=self.CORES['text_light'],
                             anchor='w')
        desc_label.pack(fill='x', pady=(2, 0))
        
        # Botões de ação
        actions_frame = tk.Frame(top_frame, bg=self.CORES['card'])
        actions_frame.pack(side='right')
        
        btn_abrir = ttk.Button(actions_frame, text="🔗 Abrir",
                              style='Success.TButton',
                              command=lambda: self.abrir_planilha(chave))
        btn_abrir.pack(side='left', padx=2)
        
        btn_editar = ttk.Button(actions_frame, text="✏️ Editar",
                               style='Primary.TButton',
                               command=lambda: self.selecionar_planilha(chave))
        btn_editar.pack(side='left', padx=2)
        
        # Efeito hover
        def on_enter(e):
            item_frame.config(bg=self.CORES['hover'], relief='solid')
            inner.config(bg=self.CORES['hover'])
            top_frame.config(bg=self.CORES['hover'])
            emoji_label.config(bg=self.CORES['hover'])
            text_frame.config(bg=self.CORES['hover'])
            nome_label.config(bg=self.CORES['hover'])
            desc_label.config(bg=self.CORES['hover'])
            actions_frame.config(bg=self.CORES['hover'])
        
        def on_leave(e):
            item_frame.config(bg=self.CORES['card'], relief='solid')
            inner.config(bg=self.CORES['card'])
            top_frame.config(bg=self.CORES['card'])
            emoji_label.config(bg=self.CORES['card'])
            text_frame.config(bg=self.CORES['card'])
            nome_label.config(bg=self.CORES['card'])
            desc_label.config(bg=self.CORES['card'])
            actions_frame.config(bg=self.CORES['card'])
        
        item_frame.bind('<Enter>', on_enter)
        item_frame.bind('<Leave>', on_leave)
        inner.bind('<Enter>', on_enter)
        inner.bind('<Leave>', on_leave)
        
    def criar_card_planilhas_OLD(self):
        """Cria card com lista de planilhas"""
        card_frame = ttk.Frame(self.aba_dashboard, style='Card.TFrame')
        card_frame.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=10)
        
        # Título
        titulo = tk.Label(card_frame, text="📋 Planilhas Configuradas", 
                         font=('Segoe UI', 14, 'bold'),
                         bg=self.CORES['white'], fg=self.CORES['text'])
        titulo.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Treeview para listar planilhas
        tree_frame = tk.Frame(card_frame, bg=self.CORES['white'])
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.tree_planilhas = ttk.Treeview(tree_frame, 
                                          columns=('nome', 'tipo', 'status'),
                                          show='headings',
                                          yscrollcommand=scrollbar.set)
        
        # Configurar colunas
        self.tree_planilhas.heading('nome', text='Nome')
        self.tree_planilhas.heading('tipo', text='Tipo')
        self.tree_planilhas.heading('status', text='Status')
        
        self.tree_planilhas.column('nome', width=200)
        self.tree_planilhas.column('tipo', width=100)
        self.tree_planilhas.column('status', width=100)
        
        self.tree_planilhas.pack(fill='both', expand=True)
        scrollbar.config(command=self.tree_planilhas.yview)
        
        # Bind duplo clique
        self.tree_planilhas.bind('<Double-1>', self.on_planilha_duplo_clique)
        
    def criar_card_acoes_rapidas(self, parent):
        """Cria card moderno com ações rápidas"""
        # Shadow frame
        shadow_frame = tk.Frame(parent, bg='#E5E7EB', bd=0)
        shadow_frame.grid(row=1, column=2, sticky='nsew', padx=10, pady=(0, 20))
        
        # Card principal
        card_frame = tk.Frame(shadow_frame, bg=self.CORES['card'], bd=0)
        card_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Header
        header = tk.Frame(card_frame, bg=self.CORES['card'])
        header.pack(fill='x', padx=25, pady=(20, 15))
        
        titulo = tk.Label(header, text="⚡ Ações Rápidas", 
                         font=('Segoe UI', 16, 'bold'),
                         bg=self.CORES['card'], fg=self.CORES['text'])
        titulo.pack(anchor='w')
        
        # Container dos botões
        botoes_frame = tk.Frame(card_frame, bg=self.CORES['card'])
        botoes_frame.pack(fill='both', expand=True, padx=25, pady=(0, 20))
        
        # Botões de ação estilizados
        self.criar_botao_acao(botoes_frame, "🔄", "Recarregar Dados", 
                             self.carregar_dados, self.CORES['primary'])
        
        self.criar_botao_acao(botoes_frame, "📊", "Abrir Power BI 1º Sem", 
                             lambda: self.abrir_planilha('power_bi_primeiro_semestre'), 
                             self.CORES['success'])
        
        self.criar_botao_acao(botoes_frame, "📊", "Abrir Power BI 2º Sem", 
                             lambda: self.abrir_planilha('power_bi_segundo_semestre'), 
                             self.CORES['success'])
        
        self.criar_botao_acao(botoes_frame, "🤖", "Abrir Autoserviço 1º Sem", 
                             lambda: self.abrir_planilha('autoservico_primeiro_semestre'), 
                             self.CORES['warning'])
        
        self.criar_botao_acao(botoes_frame, "🤖", "Abrir Autoserviço 2º Sem", 
                             lambda: self.abrir_planilha('autoservico_segundo_semestre'), 
                             self.CORES['warning'])
        
        self.criar_botao_acao(botoes_frame, "�", "Criar Backup Manual", 
                             self.criar_backup_manual, self.CORES['secondary'])
        
        self.criar_botao_acao(botoes_frame, "📖", "Abrir Documentação", 
                             self.abrir_documentacao, self.CORES['primary'])
    
    def criar_botao_acao(self, parent, emoji, texto, comando, cor):
        """Cria um botão de ação moderno com hover"""
        btn_frame = tk.Frame(parent, bg=self.CORES['card'], cursor='hand2')
        btn_frame.pack(fill='x', pady=6)
        
        # Frame interno com cor
        inner = tk.Frame(btn_frame, bg=cor, bd=0)
        inner.pack(fill='x', padx=2, pady=2)
        
        # Container do conteúdo
        content = tk.Frame(inner, bg=cor)
        content.pack(fill='x', padx=15, pady=12)
        
        # Emoji
        emoji_label = tk.Label(content, text=emoji, font=('Segoe UI', 18),
                              bg=cor, fg='white')
        emoji_label.pack(side='left', padx=(0, 10))
        
        # Texto
        text_label = tk.Label(content, text=texto, font=('Segoe UI', 11, 'bold'),
                             bg=cor, fg='white', anchor='w')
        text_label.pack(side='left', fill='x', expand=True)
        
        # Bind de clique
        def on_click(e):
            comando()
        
        def on_enter(e):
            inner.config(bg=self._darken_color(cor))
            content.config(bg=self._darken_color(cor))
            emoji_label.config(bg=self._darken_color(cor))
            text_label.config(bg=self._darken_color(cor))
        
        def on_leave(e):
            inner.config(bg=cor)
            content.config(bg=cor)
            emoji_label.config(bg=cor)
            text_label.config(bg=cor)
        
        btn_frame.bind('<Button-1>', on_click)
        inner.bind('<Button-1>', on_click)
        content.bind('<Button-1>', on_click)
        emoji_label.bind('<Button-1>', on_click)
        text_label.bind('<Button-1>', on_click)
        
        btn_frame.bind('<Enter>', on_enter)
        btn_frame.bind('<Leave>', on_leave)
    
    def _darken_color(self, hex_color):
        """Escurece uma cor hexadecimal"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def criar_aba_atualizar(self):
        """Cria aba para atualizar planilhas"""
        self.aba_atualizar = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_atualizar, text='🔧 Atualizar')
        
        # Canvas + Scrollbar para permitir scroll
        canvas_container = tk.Frame(self.aba_atualizar, bg=self.CORES['light'])
        canvas_container.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(canvas_container, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        # Canvas
        canvas = tk.Canvas(canvas_container, bg=self.CORES['light'], 
                          yscrollcommand=scrollbar.set, highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Container principal dentro do canvas
        main_frame = tk.Frame(canvas, bg=self.CORES['light'])
        canvas_frame = canvas.create_window((0, 0), window=main_frame, anchor='nw')
        
        # Configurar scroll region
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            # Ajustar largura do frame ao canvas
            canvas.itemconfig(canvas_frame, width=event.width)
        
        main_frame.bind('<Configure>', configure_scroll)
        canvas.bind('<Configure>', configure_scroll)
        
        # Adicionar padding
        main_frame_padded = tk.Frame(main_frame, bg=self.CORES['light'])
        main_frame_padded.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card de seleção
        card_selecao = ttk.Frame(main_frame_padded, style='Card.TFrame')
        card_selecao.pack(fill='x', pady=(0, 10))
        
        tk.Label(card_selecao, text="📋 Selecionar Planilha para Atualizar", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', padx=20, pady=(15, 10))
        
        selecao_frame = tk.Frame(card_selecao, bg=self.CORES['white'])
        selecao_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(selecao_frame, text="Planilha:", 
                font=('Segoe UI', 10),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w')
        
        self.combo_planilhas = ttk.Combobox(selecao_frame, 
                                           font=('Segoe UI', 10),
                                           state='readonly',
                                           width=50)
        self.combo_planilhas.pack(fill='x', pady=(5, 0))
        self.combo_planilhas.bind('<<ComboboxSelected>>', self.on_planilha_selecionada)
        
        # Card de informações atuais
        self.card_info_atual = ttk.Frame(main_frame_padded, style='Card.TFrame')
        self.card_info_atual.pack(fill='x', pady=(0, 10))
        
        tk.Label(self.card_info_atual, text="📊 Informações Atuais", 
                font=('Segoe UI', 13, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', padx=20, pady=(12, 8))
        
        self.info_frame = tk.Frame(self.card_info_atual, bg=self.CORES['white'])
        self.info_frame.pack(fill='x', padx=20, pady=(0, 12))
        
        # Labels de informação (serão preenchidos dinamicamente)
        self.label_nome_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_id_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_tipo_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_update_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        
        # Card de atualização
        self.card_atualizacao = ttk.Frame(main_frame_padded, style='Card.TFrame')
        self.card_atualizacao.pack(fill='x', pady=(0, 10))
        
        tk.Label(self.card_atualizacao, text="🔄 Nova Configuração", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', padx=20, pady=(12, 8))
        
        atualizacao_frame = tk.Frame(self.card_atualizacao, bg=self.CORES['white'])
        atualizacao_frame.pack(fill='x', padx=20, pady=(0, 12))
        
        # Campo para novo ID
        tk.Label(atualizacao_frame, text="Novo ID da Planilha:", 
                font=('Segoe UI', 10, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w')
        
        # Frame com entry e botão de ajuda
        id_input_frame = tk.Frame(atualizacao_frame, bg=self.CORES['white'])
        id_input_frame.pack(fill='x', pady=(5, 10))
        
        self.entry_novo_id = tk.Entry(id_input_frame, 
                                     font=('Segoe UI', 10),
                                     width=50)
        self.entry_novo_id.pack(side='left', fill='x', expand=True)
        self.entry_novo_id.bind('<KeyRelease>', self.validar_id_em_tempo_real)
        
        # Botão de ajuda
        btn_ajuda = tk.Button(id_input_frame, text="❓", 
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.CORES['primary'], fg=self.CORES['white'],
                             cursor='hand2', relief='flat', padx=10,
                             command=self.mostrar_ajuda_id)
        btn_ajuda.pack(side='left', padx=(5, 0))
        
        # Label de validação
        self.label_validacao = tk.Label(atualizacao_frame, 
                                       font=('Segoe UI', 9),
                                       bg=self.CORES['white'])
        self.label_validacao.pack(anchor='w')
        
        # Campo para nova descrição (opcional)
        tk.Label(atualizacao_frame, text="Nova Descrição (opcional):", 
                font=('Segoe UI', 10),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', pady=(8, 0))
        
        self.entry_nova_descricao = tk.Entry(atualizacao_frame, 
                                            font=('Segoe UI', 10),
                                            width=50)
        self.entry_nova_descricao.pack(fill='x', pady=(5, 10))
        
        # Separador visual
        tk.Frame(atualizacao_frame, bg=self.CORES['text_light'], height=1).pack(fill='x', pady=10)
        
        # Botões de ação - COM DESTAQUE
        botoes_frame = tk.Frame(atualizacao_frame, bg=self.CORES['white'])
        botoes_frame.pack(fill='x', pady=(5, 5))
        
        # Botão principal GRANDE
        self.btn_atualizar = tk.Button(botoes_frame, 
                                       text="✅ ATUALIZAR PLANILHA", 
                                       font=('Segoe UI', 12, 'bold'),
                                       bg=self.CORES['success'],
                                       fg=self.CORES['white'],
                                       cursor='hand2',
                                       relief='flat',
                                       padx=30,
                                       pady=12,
                                       command=self.atualizar_planilha,
                                       state='disabled')
        self.btn_atualizar.pack(fill='x', pady=(0, 8))
        
        # Botões secundários
        botoes_sec_frame = tk.Frame(botoes_frame, bg=self.CORES['white'])
        botoes_sec_frame.pack(fill='x')
        
        ttk.Button(botoes_sec_frame, text="🔍 Testar ID", 
                  style='Primary.TButton',
                  command=self.testar_id_online).pack(side='left', padx=(0, 10))
        
        ttk.Button(botoes_sec_frame, text="🧹 Limpar", 
                  style='Warning.TButton',
                  command=self.limpar_campos).pack(side='left')
        
    def criar_aba_historico(self):
        """Cria aba do histórico"""
        self.aba_historico = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_historico, text='📜 Histórico')
        
        # Container principal
        main_frame = tk.Frame(self.aba_historico, bg=self.CORES['light'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card do histórico
        card_frame = ttk.Frame(main_frame, style='Card.TFrame')
        card_frame.pack(fill='both', expand=True)
        
        # Título
        titulo_frame = tk.Frame(card_frame, bg=self.CORES['white'])
        titulo_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(titulo_frame, text="📜 Histórico de Mudanças", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(side='left')
        
        ttk.Button(titulo_frame, text="🔄 Atualizar", 
                  style='Primary.TButton',
                  command=self.carregar_historico).pack(side='right')
        
        # Lista de histórico
        lista_frame = tk.Frame(card_frame, bg=self.CORES['white'])
        lista_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Scrollbar
        scrollbar_hist = ttk.Scrollbar(lista_frame)
        scrollbar_hist.pack(side='right', fill='y')
        
        # Listbox para histórico
        self.listbox_historico = tk.Listbox(lista_frame, 
                                           font=('Segoe UI', 9),
                                           yscrollcommand=scrollbar_hist.set)
        self.listbox_historico.pack(fill='both', expand=True)
        scrollbar_hist.config(command=self.listbox_historico.yview)
        
        # Bind para mostrar detalhes
        self.listbox_historico.bind('<Double-1>', self.mostrar_detalhes_historico)
        
    def criar_aba_backups(self):
        """Cria aba de backups"""
        self.aba_backups = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_backups, text='💾 Backups')
        
        # Container principal
        main_frame = tk.Frame(self.aba_backups, bg=self.CORES['light'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card de ações
        card_acoes = ttk.Frame(main_frame, style='Card.TFrame')
        card_acoes.pack(fill='x', pady=(0, 10))
        
        titulo_acoes = tk.Label(card_acoes, text="⚡ Ações de Backup", 
                               font=('Segoe UI', 14, 'bold'),
                               bg=self.CORES['white'], fg=self.CORES['text'])
        titulo_acoes.pack(anchor='w', padx=20, pady=(15, 10))
        
        acoes_frame = tk.Frame(card_acoes, bg=self.CORES['white'])
        acoes_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        ttk.Button(acoes_frame, text="💾 Criar Backup Agora", 
                  style='Success.TButton',
                  command=self.criar_backup_manual).pack(side='left', padx=(0, 10))
        
        ttk.Button(acoes_frame, text="🔄 Atualizar Lista", 
                  style='Primary.TButton',
                  command=self.carregar_backups).pack(side='left', padx=(0, 10))
        
        ttk.Button(acoes_frame, text="🧹 Limpar Backups Antigos", 
                  style='Warning.TButton',
                  command=self.limpar_backups_antigos).pack(side='left')
        
        # Card de lista de backups
        card_lista = ttk.Frame(main_frame, style='Card.TFrame')
        card_lista.pack(fill='both', expand=True)
        
        titulo_lista = tk.Label(card_lista, text="📂 Backups Disponíveis", 
                               font=('Segoe UI', 14, 'bold'),
                               bg=self.CORES['white'], fg=self.CORES['text'])
        titulo_lista.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Treeview para backups
        tree_backup_frame = tk.Frame(card_lista, bg=self.CORES['white'])
        tree_backup_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        scrollbar_backup = ttk.Scrollbar(tree_backup_frame)
        scrollbar_backup.pack(side='right', fill='y')
        
        self.tree_backups = ttk.Treeview(tree_backup_frame,
                                        columns=('data', 'tamanho', 'status'),
                                        show='headings',
                                        yscrollcommand=scrollbar_backup.set)
        
        self.tree_backups.heading('data', text='Data/Hora')
        self.tree_backups.heading('tamanho', text='Tamanho')
        self.tree_backups.heading('status', text='Status')
        
        self.tree_backups.column('data', width=200)
        self.tree_backups.column('tamanho', width=100)
        self.tree_backups.column('status', width=100)
        
        self.tree_backups.pack(fill='both', expand=True)
        scrollbar_backup.config(command=self.tree_backups.yview)
        
        # Bind para ações
        self.tree_backups.bind('<Double-1>', self.restaurar_backup)
        
    def carregar_dados(self):
        """Carrega dados das planilhas"""
        try:
            # Recarregar gerenciador
            self.gp = GerenciadorPlanilhas()
            
            # Obter dados
            self.dados_planilhas = self.gp.config.get('planilhas', {})
            
            # Atualizar interface
            self.atualizar_dashboard()
            self.atualizar_combo_planilhas()
            self.carregar_historico()
            self.carregar_backups()
            
            self.status_label.config(text="🟢 Sistema Ativo")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{str(e)}")
            self.status_label.config(text="🔴 Erro no Sistema")
    
    def atualizar_dashboard(self):
        """Atualiza o dashboard com dados atuais"""
        try:
            # Estatísticas
            total_planilhas = len(self.dados_planilhas)
            historico = self.gp.config.get('historico_mudancas', [])
            total_updates = len(historico)
            
            # Contar backups
            backup_dir = os.path.join(os.path.dirname(self.gp.caminho_config), 'backups')
            total_backups = 0
            if os.path.exists(backup_dir):
                total_backups = len([f for f in os.listdir(backup_dir) if f.endswith('.json')])
            
            # Atualizar labels dos cards modernos
            if hasattr(self, 'stat_labels'):
                if 'Total de Planilhas' in self.stat_labels:
                    self.stat_labels['Total de Planilhas'].config(text=str(total_planilhas))
                if 'Últimas Atualizações' in self.stat_labels:
                    self.stat_labels['Últimas Atualizações'].config(text=str(total_updates))
                if 'Backups Disponíveis' in self.stat_labels:
                    self.stat_labels['Backups Disponíveis'].config(text=str(total_backups))
            
            # Limpar frame de planilhas
            if hasattr(self, 'planilhas_frame'):
                for widget in self.planilhas_frame.winfo_children():
                    widget.destroy()
                
                # Adicionar cada planilha como card moderno
                for chave, info in self.dados_planilhas.items():
                    self.criar_item_planilha_moderno(self.planilhas_frame, chave, info)
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
            import traceback
            traceback.print_exc()
    
    def atualizar_combo_planilhas(self):
        """Atualiza combo de planilhas"""
        try:
            planilhas = []
            for chave, dados in self.dados_planilhas.items():
                nome = dados.get('nome', chave)
                planilhas.append(f"{chave} - {nome}")
            
            self.combo_planilhas['values'] = planilhas
            
        except Exception as e:
            print(f"Erro ao atualizar combo: {e}")
    
    def on_planilha_selecionada(self, event):
        """Callback quando planilha é selecionada"""
        try:
            selecao = self.combo_planilhas.get()
            if selecao:
                chave = selecao.split(' - ')[0]
                self.planilha_selecionada = chave
                self.mostrar_info_planilha(chave)
                
        except Exception as e:
            print(f"Erro na seleção: {e}")
    
    def mostrar_info_planilha(self, chave):
        """Mostra informações da planilha selecionada"""
        try:
            dados = self.dados_planilhas.get(chave, {})
            
            # Limpar labels anteriores
            for widget in self.info_frame.winfo_children():
                widget.destroy()
            
            # Mostrar informações
            nome = dados.get('nome', 'N/A')
            id_planilha = dados.get('id', 'N/A')
            tipo = dados.get('tipo', 'N/A')
            descricao = dados.get('descricao', 'N/A')
            ultima_atualizacao = dados.get('ultima_atualizacao', 'N/A')
            abas = dados.get('abas', {})
            
            tk.Label(self.info_frame, text=f"📝 Nome: {nome}", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            tk.Label(self.info_frame, text=f"🆔 ID Atual: {id_planilha}", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            tk.Label(self.info_frame, text=f"📂 Tipo: {tipo}", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            tk.Label(self.info_frame, text=f"📄 Descrição: {descricao}", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            tk.Label(self.info_frame, text=f"📅 Última Atualização: {ultima_atualizacao}", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            tk.Label(self.info_frame, text=f"📑 Abas: {len(abas)} configuradas", 
                    font=('Segoe UI', 10), bg=self.CORES['white'], 
                    fg=self.CORES['text']).pack(anchor='w', pady=2)
            
            # Mostrar URL
            url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/edit"
            url_label = tk.Label(self.info_frame, text=f"🔗 URL: {url[:60]}...", 
                                font=('Segoe UI', 9), bg=self.CORES['white'], 
                                fg=self.CORES['primary'], cursor='hand2')
            url_label.pack(anchor='w', pady=2)
            url_label.bind('<Button-1>', lambda e: webbrowser.open(url))
            
        except Exception as e:
            print(f"Erro ao mostrar info: {e}")
    
    def validar_id_em_tempo_real(self, event):
        """Valida ID em tempo real"""
        novo_id = self.entry_novo_id.get().strip()
        
        if not novo_id:
            self.label_validacao.config(text="💡 Digite o ID da planilha do Google Sheets", 
                                       fg=self.CORES['text_light'])
            self.btn_atualizar.config(state='disabled')
            return
        
        # Verificar se planilha foi selecionada
        if not self.planilha_selecionada:
            self.label_validacao.config(text="⚠️ Selecione uma planilha primeiro", 
                                       fg=self.CORES['warning'])
            self.btn_atualizar.config(state='disabled')
            return
        
        # Validação básica de comprimento
        if len(novo_id) < 30:
            self.label_validacao.config(text=f"⏳ ID muito curto: {len(novo_id)} caracteres (mínimo ~40)", 
                                       fg=self.CORES['warning'])
            self.btn_atualizar.config(state='disabled')
        elif len(novo_id) > 50:
            self.label_validacao.config(text=f"⚠️ ID muito longo: {len(novo_id)} caracteres (máximo ~50)", 
                                       fg=self.CORES['warning'])
            self.btn_atualizar.config(state='disabled')
        elif not novo_id.replace('-', '').replace('_', '').isalnum():
            self.label_validacao.config(text="❌ ID contém caracteres inválidos", 
                                       fg=self.CORES['error'])
            self.btn_atualizar.config(state='disabled')
        else:
            # ID válido - habilitar botão
            self.label_validacao.config(text=f"✅ Formato válido ({len(novo_id)} caracteres)", 
                                       fg=self.CORES['success'])
            self.btn_atualizar.config(state='normal')
    
    def testar_id_online(self):
        """Testa se o ID abre uma planilha válida"""
        novo_id = self.entry_novo_id.get().strip()
        
        if not novo_id:
            messagebox.showwarning("Aviso", "Digite um ID para testar")
            return
        
        # Validações básicas primeiro
        erros = []
        avisos = []
        
        if len(novo_id) < 30:
            erros.append(f"• ID muito curto: {len(novo_id)} caracteres")
        elif len(novo_id) > 50:
            avisos.append(f"• ID pode estar muito longo: {len(novo_id)} caracteres")
        
        if not novo_id.replace('-', '').replace('_', '').isalnum():
            erros.append("• Contém caracteres inválidos (só letras, números, - e _)")
        
        # Verificar se já existe em outra planilha
        for chave, dados in self.dados_planilhas.items():
            if dados.get('id') == novo_id and chave != self.planilha_selecionada:
                avisos.append(f"• ID já está em uso pela planilha '{chave}'")
        
        if erros:
            messagebox.showerror("ID Inválido", 
                               "❌ Problemas encontrados:\\n\\n" + "\\n".join(erros))
            return
        
        # Tentar abrir no navegador para testar
        resposta = messagebox.askyesno(
            "Testar ID",
            f"✅ Formato válido!\\n\\n"
            f"Caracteres: {len(novo_id)}\\n"
            + ("\\n⚠️ Avisos:\\n" + "\\n".join(avisos) if avisos else "") +
            "\\n\\nDeseja abrir a planilha no navegador para verificar?"
        )
        
        if resposta:
            url = f"https://docs.google.com/spreadsheets/d/{novo_id}/edit"
            webbrowser.open(url)
    
    def atualizar_planilha(self):
        """Atualiza a planilha selecionada"""
        if not self.planilha_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma planilha primeiro")
            return
        
        novo_id = self.entry_novo_id.get().strip()
        nova_descricao = self.entry_nova_descricao.get().strip()
        
        if not novo_id:
            messagebox.showwarning("Aviso", "Digite o novo ID da planilha")
            return
        
        # Confirmar atualização
        dados_atuais = self.dados_planilhas[self.planilha_selecionada]
        nome = dados_atuais.get('nome', self.planilha_selecionada)
        id_atual = dados_atuais.get('id', 'N/A')
        
        resposta = messagebox.askyesno(
            "Confirmar Atualização",
            f"Atualizar planilha '{nome}'?\\n\\n"
            f"ID Atual: {id_atual[:20]}...\\n"
            f"Novo ID: {novo_id[:20]}...\\n\\n"
            f"Esta ação criará um backup automático."
        )
        
        if not resposta:
            return
        
        try:
            # Atualizar via gerenciador
            sucesso = self.gp.atualizar_planilha(
                self.planilha_selecionada,
                novo_id,
                nova_descricao if nova_descricao else None
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"✅ Planilha '{nome}' atualizada com sucesso!")
                self.carregar_dados()  # Recarregar dados
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "❌ Falha ao atualizar planilha")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na atualização:\\n{str(e)}")
    
    def limpar_campos(self):
        """Limpa os campos de atualização"""
        self.entry_novo_id.delete(0, 'end')
        self.entry_nova_descricao.delete(0, 'end')
        self.label_validacao.config(text="")
        self.btn_atualizar.config(state='disabled')
    
    def carregar_historico(self):
        """Carrega histórico de mudanças"""
        try:
            self.listbox_historico.delete(0, 'end')
            
            historico = self.gp.config.get('historico_mudancas', [])
            
            if not historico:
                self.listbox_historico.insert('end', "📝 Nenhuma mudança registrada ainda")
                return
            
            for entrada in historico:
                data = entrada.get('data', 'N/A')
                titulo = entrada.get('titulo', 'N/A')
                linha = f"{data} - {titulo}"
                self.listbox_historico.insert('end', linha)
                
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
    
    def mostrar_detalhes_historico(self, event):
        """Mostra detalhes de uma entrada do histórico"""
        try:
            selecao = self.listbox_historico.curselection()
            if not selecao:
                return
            
            indice = selecao[0]
            historico = self.gp.config.get('historico_mudancas', [])
            
            if indice < len(historico):
                entrada = historico[indice]
                
                data = entrada.get('data', 'N/A')
                titulo = entrada.get('titulo', 'N/A')
                mudancas = entrada.get('mudancas', [])
                autor = entrada.get('autor', 'N/A')
                
                detalhes = f"📅 Data: {data}\\n"
                detalhes += f"👤 Autor: {autor}\\n"
                detalhes += f"📝 Título: {titulo}\\n\\n"
                detalhes += "🔄 Mudanças:\\n"
                
                for mudanca in mudancas:
                    detalhes += f"• {mudanca}\\n"
                
                messagebox.showinfo("Detalhes da Mudança", detalhes)
                
        except Exception as e:
            print(f"Erro ao mostrar detalhes: {e}")
    
    def carregar_backups(self):
        """Carrega lista de backups"""
        try:
            # Limpar tree
            for item in self.tree_backups.get_children():
                self.tree_backups.delete(item)
            
            # Diretório de backups
            backup_dir = os.path.join(os.path.dirname(self.gp.caminho_config), 'backups')
            
            if not os.path.exists(backup_dir):
                self.tree_backups.insert('', 'end', values=("Nenhum backup encontrado", "-", "-"))
                return
            
            # Listar arquivos de backup
            backups = []
            for arquivo in os.listdir(backup_dir):
                if arquivo.endswith('.json'):
                    caminho = os.path.join(backup_dir, arquivo)
                    stat = os.stat(caminho)
                    
                    # Extrair data do nome do arquivo
                    try:
                        # Formato: planilhas_config_YYYYMMDD_HHMM.json
                        partes = arquivo.replace('.json', '').split('_')
                        if len(partes) >= 4:
                            data_str = partes[2]
                            hora_str = partes[3]
                            data_formatada = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:8]} {hora_str[:2]}:{hora_str[2:4]}"
                        else:
                            data_formatada = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    except:
                        data_formatada = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    
                    tamanho_kb = stat.st_size / 1024
                    tamanho_str = f"{tamanho_kb:.1f} KB"
                    
                    backups.append((data_formatada, tamanho_str, arquivo))
            
            # Ordenar por data (mais recente primeiro)
            backups.sort(reverse=True)
            
            # Adicionar ao tree
            for data, tamanho, arquivo in backups:
                status = "✅ OK"
                self.tree_backups.insert('', 'end', 
                                       values=(data, tamanho, status),
                                       tags=(arquivo,))
                
        except Exception as e:
            print(f"Erro ao carregar backups: {e}")
            self.tree_backups.insert('', 'end', values=("Erro ao carregar", "-", "❌"))
    
    def criar_backup_manual(self):
        """Cria backup manual"""
        try:
            # Criar diretório se não existir
            backup_dir = os.path.join(os.path.dirname(self.gp.caminho_config), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            nome_backup = f"planilhas_config_{timestamp}.json"
            caminho_backup = os.path.join(backup_dir, nome_backup)
            
            # Copiar arquivo atual
            import shutil
            shutil.copy2(self.gp.caminho_config, caminho_backup)
            
            messagebox.showinfo("Backup Criado", f"✅ Backup criado com sucesso:\\n{nome_backup}")
            self.carregar_backups()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup:\\n{str(e)}")
    
    def restaurar_backup(self, event):
        """Restaura um backup selecionado"""
        try:
            selecao = self.tree_backups.selection()
            if not selecao:
                return
            
            item = self.tree_backups.item(selecao[0])
            if not item['tags']:
                return
            
            arquivo_backup = item['tags'][0]
            data = item['values'][0]
            
            resposta = messagebox.askyesno(
                "Restaurar Backup",
                f"Restaurar backup de {data}?\\n\\n"
                f"Arquivo: {arquivo_backup}\\n\\n"
                f"⚠️ ATENÇÃO: Isso substituirá a configuração atual!"
            )
            
            if not resposta:
                return
            
            # Criar backup da configuração atual antes de restaurar
            self.criar_backup_manual()
            
            # Restaurar
            backup_dir = os.path.join(os.path.dirname(self.gp.caminho_config), 'backups')
            caminho_backup = os.path.join(backup_dir, arquivo_backup)
            
            import shutil
            shutil.copy2(caminho_backup, self.gp.caminho_config)
            
            messagebox.showinfo("Backup Restaurado", "✅ Configuração restaurada com sucesso!")
            self.carregar_dados()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup:\\n{str(e)}")
    
    def limpar_backups_antigos(self):
        """Remove backups antigos (mais de 30 dias)"""
        try:
            backup_dir = os.path.join(os.path.dirname(self.gp.caminho_config), 'backups')
            
            if not os.path.exists(backup_dir):
                messagebox.showinfo("Info", "Nenhum diretório de backup encontrado")
                return
            
            import time
            agora = time.time()
            limite = 30 * 24 * 60 * 60  # 30 dias em segundos
            
            removidos = 0
            for arquivo in os.listdir(backup_dir):
                if arquivo.endswith('.json'):
                    caminho = os.path.join(backup_dir, arquivo)
                    idade = agora - os.path.getmtime(caminho)
                    
                    if idade > limite:
                        os.remove(caminho)
                        removidos += 1
            
            messagebox.showinfo("Limpeza Concluída", f"✅ {removidos} backups antigos removidos")
            self.carregar_backups()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na limpeza:\\n{str(e)}")
    
    def on_planilha_duplo_clique(self, event):
        """Callback para duplo clique na lista de planilhas"""
        try:
            selecao = self.tree_planilhas.selection()
            if selecao:
                item = self.tree_planilhas.item(selecao[0])
                chave = item['tags'][0] if item['tags'] else None
                
                if chave:
                    self.abrir_planilha(chave)
                    
        except Exception as e:
            print(f"Erro no duplo clique: {e}")
    
    def abrir_planilha(self, chave):
        """Abre planilha no navegador"""
        try:
            id_planilha = self.gp.obter_id(chave)
            if id_planilha:
                url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/edit"
                webbrowser.open(url)
            else:
                messagebox.showerror("Erro", f"ID da planilha '{chave}' não encontrado")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir planilha:\n{str(e)}")
    
    def selecionar_planilha(self, chave):
        """Seleciona uma planilha para edição"""
        try:
            self.planilha_selecionada = chave
            # Mudar para aba de atualizar
            self.notebook.select(1)  # Índice da aba Atualizar
            # Popular os campos com dados da planilha
            info = self.dados_planilhas.get(chave, {})
            if hasattr(self, 'combo_planilha'):
                # Selecionar no combo
                for i, (k, v) in enumerate(self.dados_planilhas.items()):
                    if k == chave:
                        self.combo_planilha.current(i)
                        break
            messagebox.showinfo("Sucesso", f"Planilha '{info.get('nome', chave)}' selecionada para edição!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar planilha:\n{str(e)}")
    
    def abrir_documentacao(self):
        """Abre documentação"""
        try:
            doc_path = os.path.join(project_root, 'docs', 'gerenciador_planilhas.md')
            if os.path.exists(doc_path):
                os.startfile(doc_path)
            else:
                messagebox.showwarning("Aviso", "Arquivo de documentação não encontrado")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir documentação:\\n{str(e)}")
    
    def mostrar_ajuda_id(self):
        """Mostra ajuda sobre como encontrar o ID da planilha"""
        mensagem = """📋 Como encontrar o ID da Planilha Google Sheets:

1️⃣ Abra a planilha no Google Sheets

2️⃣ Olhe para a URL no navegador:
   https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit

3️⃣ Copie apenas a parte entre /d/ e /edit

📌 Exemplo:
URL: https://docs.google.com/spreadsheets/d/1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc/edit
ID:  1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc

✅ O ID tem entre 40-45 caracteres
✅ Contém letras, números, - e _
"""
        messagebox.showinfo("Como encontrar o ID", mensagem)
    
    def executar(self):
        """Executa a interface"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Interface encerrada pelo usuário")
        except Exception as e:
            print(f"Erro na interface: {e}")


def main():
    """Função principal"""
    try:
        app = InterfaceGerenciadorVisual()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar interface: {e}")


if __name__ == "__main__":
    main()
