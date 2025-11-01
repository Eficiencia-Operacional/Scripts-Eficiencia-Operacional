#!/usr/bin/env python3
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

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os
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
        # Cores do tema
        self.CORES = {
            'primary': '#2E86AB',       # Azul principal
            'secondary': '#A23B72',     # Rosa secundário
            'accent': '#F18F01',        # Laranja destaque
            'success': '#C73E1D',       # Verde sucesso
            'warning': '#FFE66D',       # Amarelo aviso
            'error': '#FF6B6B',         # Vermelho erro
            'dark': '#2C3E50',          # Azul escuro
            'light': '#ECF0F1',         # Cinza claro
            'white': '#FFFFFF',         # Branco
            'text': '#2C3E50',          # Texto escuro
            'text_light': '#7F8C8D'     # Texto claro
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
        """Cria a janela principal"""
        self.root = tk.Tk()
        self.root.title("🎨 Gerenciador de Planilhas - Leroy Merlin")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.CORES['light'])
        self.root.minsize(1000, 600)
        
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
        """Configura estilos personalizados"""
        # Notebook
        self.style.configure('Custom.TNotebook', 
                           background=self.CORES['light'],
                           tabmargins=[2, 5, 2, 0])
        
        self.style.configure('Custom.TNotebook.Tab',
                           background=self.CORES['white'],
                           foreground=self.CORES['text'],
                           padding=[20, 8],
                           focuscolor='none')
        
        self.style.map('Custom.TNotebook.Tab',
                      background=[('selected', self.CORES['primary']),
                                 ('active', self.CORES['secondary'])],
                      foreground=[('selected', self.CORES['white']),
                                 ('active', self.CORES['white'])])
        
        # Botões
        self.style.configure('Primary.TButton',
                           background=self.CORES['primary'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8),
                           relief='flat',
                           borderwidth=0)
        
        self.style.map('Primary.TButton',
                      background=[('active', self.CORES['secondary']),
                                 ('pressed', self.CORES['dark'])])
        
        self.style.configure('Success.TButton',
                           background=self.CORES['success'],
                           foreground=self.CORES['white'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Warning.TButton',
                           background=self.CORES['warning'],
                           foreground=self.CORES['dark'],
                           font=('Segoe UI', 10, 'bold'),
                           padding=(12, 6))
        
        # Frames
        self.style.configure('Card.TFrame',
                           background=self.CORES['white'],
                           relief='raised',
                           borderwidth=1)
        
    def criar_header(self):
        """Cria o cabeçalho"""
        header_frame = tk.Frame(self.root, bg=self.CORES['primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container do header
        header_content = tk.Frame(header_frame, bg=self.CORES['primary'])
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Título principal
        titulo = tk.Label(
            header_content,
            text="🎨 Gerenciador de Planilhas",
            font=('Segoe UI', 20, 'bold'),
            bg=self.CORES['primary'],
            fg=self.CORES['white']
        )
        titulo.pack(side='left')
        
        # Subtítulo
        subtitulo = tk.Label(
            header_content,
            text="Sistema Centralizado de Configurações • Leroy Merlin RPA",
            font=('Segoe UI', 10),
            bg=self.CORES['primary'],
            fg=self.CORES['light']
        )
        subtitulo.pack(side='left', padx=(10, 0))
        
        # Status no canto direito
        self.status_label = tk.Label(
            header_content,
            text="● Sistema Carregado",
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
        """Cria aba do dashboard"""
        # Frame da aba
        self.aba_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_dashboard, text='📊 Dashboard')
        
        # Configurar grid
        self.aba_dashboard.grid_columnconfigure(0, weight=1)
        self.aba_dashboard.grid_columnconfigure(1, weight=1)
        
        # Card de estatísticas
        self.criar_card_estatisticas()
        
        # Card de planilhas
        self.criar_card_planilhas()
        
        # Card de ações rápidas
        self.criar_card_acoes_rapidas()
        
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
        
    def criar_card_planilhas(self):
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
        
    def criar_card_acoes_rapidas(self):
        """Cria card com ações rápidas"""
        card_frame = ttk.Frame(self.aba_dashboard, style='Card.TFrame')
        card_frame.grid(row=1, column=1, sticky='nsew', padx=(5, 10), pady=10)
        
        # Título
        titulo = tk.Label(card_frame, text="⚡ Ações Rápidas", 
                         font=('Segoe UI', 14, 'bold'),
                         bg=self.CORES['white'], fg=self.CORES['text'])
        titulo.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Container dos botões
        botoes_frame = tk.Frame(card_frame, bg=self.CORES['white'])
        botoes_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Botões de ação
        ttk.Button(botoes_frame, text="🔄 Recarregar Dados", 
                  style='Primary.TButton',
                  command=self.carregar_dados).pack(fill='x', pady=5)
        
        ttk.Button(botoes_frame, text="📊 Abrir Planilha Genesys", 
                  style='Success.TButton',
                  command=lambda: self.abrir_planilha('genesys_boletim')).pack(fill='x', pady=5)
        
        ttk.Button(botoes_frame, text="💼 Abrir Planilha Salesforce", 
                  style='Success.TButton',
                  command=lambda: self.abrir_planilha('salesforce_boletim')).pack(fill='x', pady=5)
        
        ttk.Button(botoes_frame, text="📈 Abrir Planilha Produtividade", 
                  style='Success.TButton',
                  command=lambda: self.abrir_planilha('produtividade_boletim')).pack(fill='x', pady=5)
        
        ttk.Button(botoes_frame, text="💾 Criar Backup Manual", 
                  style='Warning.TButton',
                  command=self.criar_backup_manual).pack(fill='x', pady=5)
        
        ttk.Button(botoes_frame, text="📖 Abrir Documentação", 
                  style='Primary.TButton',
                  command=self.abrir_documentacao).pack(fill='x', pady=5)
        
    def criar_aba_atualizar(self):
        """Cria aba para atualizar planilhas"""
        self.aba_atualizar = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_atualizar, text='🔧 Atualizar')
        
        # Container principal
        main_frame = tk.Frame(self.aba_atualizar, bg=self.CORES['light'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Card de seleção
        card_selecao = ttk.Frame(main_frame, style='Card.TFrame')
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
        self.card_info_atual = ttk.Frame(main_frame, style='Card.TFrame')
        self.card_info_atual.pack(fill='x', pady=(0, 10))
        
        tk.Label(self.card_info_atual, text="📊 Informações Atuais", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', padx=20, pady=(15, 10))
        
        self.info_frame = tk.Frame(self.card_info_atual, bg=self.CORES['white'])
        self.info_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Labels de informação (serão preenchidos dinamicamente)
        self.label_nome_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_id_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_tipo_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        self.label_update_atual = tk.Label(self.info_frame, bg=self.CORES['white'], fg=self.CORES['text'])
        
        # Card de atualização
        self.card_atualizacao = ttk.Frame(main_frame, style='Card.TFrame')
        self.card_atualizacao.pack(fill='x', pady=(0, 10))
        
        tk.Label(self.card_atualizacao, text="🔄 Nova Configuração", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', padx=20, pady=(15, 10))
        
        atualizacao_frame = tk.Frame(self.card_atualizacao, bg=self.CORES['white'])
        atualizacao_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Campo para novo ID
        tk.Label(atualizacao_frame, text="Novo ID da Planilha:", 
                font=('Segoe UI', 10, 'bold'),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w')
        
        self.entry_novo_id = tk.Entry(atualizacao_frame, 
                                     font=('Segoe UI', 10),
                                     width=50)
        self.entry_novo_id.pack(fill='x', pady=(5, 10))
        self.entry_novo_id.bind('<KeyRelease>', self.validar_id_em_tempo_real)
        
        # Label de validação
        self.label_validacao = tk.Label(atualizacao_frame, 
                                       font=('Segoe UI', 9),
                                       bg=self.CORES['white'])
        self.label_validacao.pack(anchor='w')
        
        # Campo para nova descrição (opcional)
        tk.Label(atualizacao_frame, text="Nova Descrição (opcional):", 
                font=('Segoe UI', 10),
                bg=self.CORES['white'], fg=self.CORES['text']).pack(anchor='w', pady=(10, 0))
        
        self.entry_nova_descricao = tk.Entry(atualizacao_frame, 
                                            font=('Segoe UI', 10),
                                            width=50)
        self.entry_nova_descricao.pack(fill='x', pady=(5, 15))
        
        # Botões de ação
        botoes_frame = tk.Frame(atualizacao_frame, bg=self.CORES['white'])
        botoes_frame.pack(fill='x')
        
        self.btn_atualizar = ttk.Button(botoes_frame, text="✅ Atualizar Planilha", 
                                       style='Success.TButton',
                                       command=self.atualizar_planilha,
                                       state='disabled')
        self.btn_atualizar.pack(side='left', padx=(0, 10))
        
        ttk.Button(botoes_frame, text="🔍 Validar ID", 
                  style='Primary.TButton',
                  command=self.validar_id).pack(side='left', padx=(0, 10))
        
        ttk.Button(botoes_frame, text="🧹 Limpar Campos", 
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
            
            self.status_label.config(text="● Dados Atualizados", fg=self.CORES['success'])
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\\n{str(e)}")
            self.status_label.config(text="● Erro ao Carregar", fg=self.CORES['error'])
    
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
            
            # Atualizar labels
            self.stat_0_label.config(text=str(total_planilhas))
            self.stat_1_label.config(text=str(total_updates))
            self.stat_2_label.config(text=str(total_backups))
            self.stat_3_label.config(text="OK" if total_planilhas > 0 else "ERRO")
            
            # Atualizar tree de planilhas
            for item in self.tree_planilhas.get_children():
                self.tree_planilhas.delete(item)
            
            for chave, dados in self.dados_planilhas.items():
                nome = dados.get('nome', chave)
                tipo = dados.get('tipo', 'N/A')
                id_planilha = dados.get('id', 'N/A')
                
                # Verificar status (simplificado)
                status = "✅ OK" if len(id_planilha) > 20 else "❌ Erro"
                
                self.tree_planilhas.insert('', 'end', 
                                         values=(nome, tipo.upper(), status),
                                         tags=(chave,))
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
    
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
            self.label_validacao.config(text="", fg=self.CORES['text'])
            self.btn_atualizar.config(state='disabled')
            return
        
        # Validação básica
        if len(novo_id) != 44:
            self.label_validacao.config(text="❌ ID deve ter exatamente 44 caracteres", 
                                       fg=self.CORES['error'])
            self.btn_atualizar.config(state='disabled')
        elif not novo_id.replace('-', '').replace('_', '').isalnum():
            self.label_validacao.config(text="❌ ID contém caracteres inválidos", 
                                       fg=self.CORES['error'])
            self.btn_atualizar.config(state='disabled')
        else:
            self.label_validacao.config(text="✅ Formato válido", 
                                       fg=self.CORES['success'])
            if self.planilha_selecionada:
                self.btn_atualizar.config(state='normal')
    
    def validar_id(self):
        """Valida ID com mais detalhes"""
        novo_id = self.entry_novo_id.get().strip()
        
        if not novo_id:
            messagebox.showwarning("Aviso", "Digite um ID para validar")
            return
        
        # Validações
        erros = []
        
        if len(novo_id) != 44:
            erros.append(f"• Comprimento incorreto: {len(novo_id)} (deve ser 44)")
        
        if not novo_id.replace('-', '').replace('_', '').isalnum():
            erros.append("• Contém caracteres inválidos (só letras, números, - e _)")
        
        # Verificar se já existe
        for chave, dados in self.dados_planilhas.items():
            if dados.get('id') == novo_id and chave != self.planilha_selecionada:
                erros.append(f"• ID já está em uso pela planilha '{chave}'")
        
        if erros:
            messagebox.showerror("ID Inválido", "Problemas encontrados:\\n\\n" + "\\n".join(erros))
        else:
            messagebox.showinfo("ID Válido", "✅ ID está no formato correto e disponível!")
    
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
            messagebox.showerror("Erro", f"Erro ao abrir planilha:\\n{str(e)}")
    
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
