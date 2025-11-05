"""
Script para atualizar interface_powerbi.py com suporte a Autoserviço
"""

import re
import os

def atualizar_interface():
    # Encontra o caminho do arquivo de forma relativa (compatível com qualquer sistema)
    script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    arquivo = os.path.join(project_root, 'interfaces', 'interface_powerbi.py')
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Atualizar sistemas_nomes para incluir Autoserviço
    padrao_sistemas = r"sistemas_nomes = \{\s+'primeiro': \"[^\"]+PRIMEIRO SEMESTRE\",\s+'segundo': \"[^\"]+SEGUNDO SEMESTRE\"\s+\}"
    substituicao_sistemas = """sistemas_nomes = {
            'primeiro': "📊 PRIMEIRO SEMESTRE",
            'segundo': "📊 SEGUNDO SEMESTRE",
            'autoservico_primeiro': "🤖 AUTOSERVIÇO 1º SEMESTRE",
            'autoservico_segundo': "🤖 AUTOSERVIÇO 2º SEMESTRE"
        }"""
    
    conteudo = re.sub(padrao_sistemas, substituicao_sistemas, conteudo)
    
    # Salvar arquivo
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ Arquivo atualizado com sucesso!")

if __name__ == '__main__':
    atualizar_interface()
