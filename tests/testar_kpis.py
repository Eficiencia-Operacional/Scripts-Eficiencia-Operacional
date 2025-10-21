#!/usr/bin/env python3
"""
Script para testar a atualização dos KPIs do dashboard
"""

import json
import os
from datetime import datetime

# Dados de exemplo para simular execuções
kpis_teste = {
    'total_processados': 2981,
    'taxa_sucesso': 98.5,
    'tempo_medio': 12,
    'ultima_execucao': 'Hoje 14:32',
    'arquivos_processados': 45,
    'arquivos_sucesso': 43,
    'arquivos_erro': 2
}

# Salvar no arquivo JSON
arquivo_kpis = os.path.join('config', 'kpis_historico.json')

# Garantir que o diretório existe
os.makedirs('config', exist_ok=True)

# Salvar dados
with open(arquivo_kpis, 'w', encoding='utf-8') as f:
    json.dump(kpis_teste, f, indent=2, ensure_ascii=False)

print("✅ KPIs de teste salvos!")
print(f"📊 Arquivo: {arquivo_kpis}")
print("\n📈 Dados salvos:")
for chave, valor in kpis_teste.items():
    print(f"  - {chave}: {valor}")

print("\n💡 Agora execute a interface (python interface_visual.py) para ver os KPIs com dados REAIS!")
