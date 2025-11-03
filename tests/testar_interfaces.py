#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de teste para validar todas as interfaces"""

import sys
import os

# Não modificar stdout/stderr para evitar conflitos
print("="*70)
print("TESTE DE VALIDACAO DAS INTERFACES")
print("="*70)
print()

# Teste 1: Arquivos de configuração
print("1. Testando arquivos de configuracao...")
arquivos = [
    ('config/boletim.json', 'Credenciais Google'),
    ('json/planilhas_config.json', 'Config Planilhas'),
    ('data/Filas Genesys - Todas as Filas .csv', 'CSV Filas Genesys')
]

for arquivo, desc in arquivos:
    if os.path.exists(arquivo):
        print(f"   OK {desc}: {arquivo}")
    else:
        print(f"   ERRO {desc}: {arquivo} (nao encontrado)")

print()

# Teste 2: Configuração de planilhas
print("2. Testando configuracao de planilhas...")
try:
    from scripts.gerenciador_planilhas import GerenciadorPlanilhas
    gp = GerenciadorPlanilhas()
    
    planilhas_teste = [
        'power_bi_primeiro_semestre',
        'power_bi_segundo_semestre'
    ]
    
    for chave in planilhas_teste:
        id_planilha = gp.obter_id(chave)
        if id_planilha:
            print(f"   OK {chave}: {id_planilha[:20]}...")
        else:
            print(f"   ERRO {chave}: ID nao encontrado")
            
except Exception as e:
    print(f"   ERRO ao carregar configuracoes: {e}")

print()

# Teste 3: Acesso às planilhas
print("3. Testando acesso as planilhas (Google Sheets)...")
try:
    from google.oauth2.service_account import Credentials
    import gspread
    
    creds = Credentials.from_service_account_file(
        'config/boletim.json',
        scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    
    client = gspread.authorize(creds)
    
    from scripts.gerenciador_planilhas import GerenciadorPlanilhas
    gp = GerenciadorPlanilhas()
    
    planilhas = {
        'Primeiro Semestre': gp.obter_id('power_bi_primeiro_semestre'),
        'Segundo Semestre': gp.obter_id('power_bi_segundo_semestre')
    }
    
    for nome, planilha_id in planilhas.items():
        if not planilha_id:
            print(f"   AVISO {nome}: ID nao configurado")
            continue
            
        try:
            sheet = client.open_by_key(planilha_id)
            print(f"   OK {nome}: Acesso OK ({sheet.title})")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"   ERRO {nome}: Sem permissao ou nao existe")
        except Exception as e:
            print(f"   ERRO {nome}: {type(e).__name__}")
            
except Exception as e:
    print(f"   ERRO ao testar acesso: {e}")

print()
print("="*70)
print("TESTE CONCLUIDO")
print("="*70)

