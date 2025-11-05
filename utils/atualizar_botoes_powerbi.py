"""
Script para atualizar textos dos botões Power BI
"""

import re
import os

# Encontra o caminho do arquivo de forma relativa (compatível com qualquer sistema)
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
arquivo = os.path.join(project_root, 'interfaces', 'interface_powerbi.py')

with open(arquivo, 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Atualizar botão individual PRIMEIRO SEMESTRE
conteudo = re.sub(
    r'text="[^"]*PROCESSAR PRIMEIRO SEMESTRE"',
    'text="📊 PROCESSAR POWER BI 1º SEM"',
    conteudo
)

# Atualizar botão individual SEGUNDO SEMESTRE
conteudo = re.sub(
    r'text="[^"]*PROCESSAR SEGUNDO SEMESTRE"',
    'text="📊 PROCESSAR POWER BI 2º SEM"',
    conteudo
)

with open(arquivo, 'w', encoding='utf-8') as f:
    f.write(conteudo)

print("✅ Botões de processamento individual atualizados!")
