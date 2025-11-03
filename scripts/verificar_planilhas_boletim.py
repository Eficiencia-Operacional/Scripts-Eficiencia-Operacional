#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar planilhas do Pulso Boletim no gerenciador"""

from scripts.gerenciador_planilhas import GerenciadorPlanilhas

gp = GerenciadorPlanilhas()

print("\n" + "="*70)
print("PLANILHAS DO PULSO BOLETIM NO GERENCIADOR")
print("="*70 + "\n")

planilhas_boletim = ['genesys_boletim', 'salesforce_boletim', 'produtividade_boletim']

for chave in planilhas_boletim:
    info = gp.obter_info_planilha(chave)
    if info:
        print(f"✅ {info['nome']}")
        print(f"   ID: {info['id']}")
        print(f"   Abas: {', '.join(info['abas'].keys())}")
        print(f"   URL: {info['url']}")
        print()
    else:
        print(f"❌ {chave}: Não encontrada")
        print()

print("="*70)
print(f"\nTotal de planilhas configuradas: {len(gp.listar_planilhas())}")
print("="*70)
