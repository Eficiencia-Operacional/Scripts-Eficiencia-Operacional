#!/usr/bin/env python3
"""
AUTOMAÇÃO DE BOLETINS - LEROY MERLIN
Sistema inteligente para processamento automático de relatórios

ENTRADA ÚNICA PARA TODA A AUTOMAÇÃO

Uso:
    python main.py                    # Processa tudo automaticamente
    python main.py --genesys          # Apenas bases Genesys
    python main.py --salesforce       # Apenas bases Salesforce
    python main.py --help             # Mostra ajuda
"""

import sys
import os
import argparse
from typing import Dict, Any

# Configurar paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Adicionar paths necessários
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'processadores', 'genesys'))
sys.path.append(os.path.join(current_dir, 'processadores', 'salesforce'))
sys.path.append(os.path.join(current_dir, 'processadores', 'produtividade'))

def main():
    """Função principal da automação"""
    
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description='Automação de Boletins Leroy Merlin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py                    # Processa tudo
  python main.py --genesys          # Só Genesys
  python main.py --salesforce       # Só Salesforce
  python main.py --produtividade    # Só Produtividade
  python main.py --dados ./meus_csvs # Especifica pasta de dados
        """
    )
    
    parser.add_argument('--genesys', action='store_true', 
                       help='Processar apenas bases Genesys')
    parser.add_argument('--salesforce', action='store_true',
                       help='Processar apenas bases Salesforce')
    parser.add_argument('--produtividade', action='store_true',
                       help='Processar apenas bases de Produtividade')
    parser.add_argument('--dados', type=str, default='dados',
                       help='Pasta onde estão os arquivos CSV (default: dados)')
    parser.add_argument('--planilha', type=str, 
                       help='ID específico da planilha Google Sheets')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo verboso')
    
    args = parser.parse_args()
    
    # Banner inicial
    print("🚀 AUTOMAÇÃO DE BOLETINS - LEROY MERLIN")
    print("=" * 60)
    print("📁 Sistema de detecção inteligente de arquivos ativado")
    print(f"📂 Pasta de dados: {args.dados}")
    print()
    
    # Verificar se pasta de dados existe
    if not os.path.exists(args.dados):
        print(f"⚠️  Pasta '{args.dados}' não encontrada. Criando...")
        os.makedirs(args.dados, exist_ok=True)
    
    # Mudar para pasta de dados para facilitar busca
    os.chdir(args.dados)
    
    resultados = {}
    
    # Processar Genesys
    if not args.salesforce and not args.produtividade:  # Se não especificou só salesforce ou produtividade
        resultados.update(processar_genesys(args.verbose, args.planilha))
    
    # Processar Salesforce
    if not args.genesys and not args.produtividade:  # Se não especificou só genesys ou produtividade
        resultados.update(processar_salesforce(args.verbose, args.planilha))
    
    # Processar Produtividade
    if not args.genesys and not args.salesforce:  # Se não especificou só genesys ou salesforce
        resultados.update(processar_produtividade(args.verbose, args.planilha))
    
    # Relatório final
    gerar_relatorio_final(resultados)

def processar_genesys(verbose=False, id_planilha=None) -> Dict[str, bool]:
    """Processa todas as bases Genesys"""
    try:
        from processadores.genesys.processador_genesys import ProcessadorGenesys
        
        print("🔄 INICIANDO PROCESSAMENTO GENESYS")
        print("-" * 40)
        
        if id_planilha:
            print(f"📊 Usando planilha específica: {id_planilha}")
        
        processador = ProcessadorGenesys(id_planilha=id_planilha)
        resultados = processador.processar_todos()
        
        if verbose:
            print(f"📊 Genesys processado: {sum(resultados.values())}/{len(resultados)} bases")
        
        return {f"Genesys - {k}": v for k, v in resultados.items()}
        
    except ImportError as e:
        print(f"❌ Erro ao importar processador Genesys: {e}")
        return {"Genesys": False}
    except Exception as e:
        print(f"❌ Erro no processamento Genesys: {e}")
        return {"Genesys": False}

def processar_salesforce(verbose=False, id_planilha=None) -> Dict[str, bool]:
    """Processa todas as bases Salesforce"""
    try:
        from processadores.salesforce.processador_salesforce import ProcessadorSalesforce
        
        print("\n🔄 INICIANDO PROCESSAMENTO SALESFORCE")
        print("-" * 40)
        
        if id_planilha:
            print(f"📊 Usando planilha específica: {id_planilha}")
        
        processador = ProcessadorSalesforce(id_planilha=id_planilha)
        resultados = processador.processar_todos()
        
        if verbose:
            print(f"📊 Salesforce processado: {sum(resultados.values())}/{len(resultados)} bases")
        
        return {f"Salesforce - {k}": v for k, v in resultados.items()}
        
    except ImportError as e:
        print(f"❌ Erro ao importar processador Salesforce: {e}")
        return {"Salesforce": False}
    except Exception as e:
        print(f"❌ Erro no processamento Salesforce: {e}")
        return {"Salesforce": False}

def processar_produtividade(verbose=False, id_planilha=None) -> Dict[str, bool]:
    """Processa todas as bases de Produtividade"""
    try:
        from processadores.produtividade.produtividade import Produtividade
        
        print("\n🔄 INICIANDO PROCESSAMENTO PRODUTIVIDADE")
        print("-" * 40)
        
        if id_planilha:
            print(f"📊 Usando planilha específica: {id_planilha}")
        
        processador = Produtividade(id_planilha=id_planilha)
        resultados = processador.processar_todos()
        
        if verbose:
            print(f"📊 Produtividade processada: {sum(resultados.values())}/{len(resultados)} bases")
        
        return {f"Produtividade - {k}": v for k, v in resultados.items()}
        
    except ImportError as e:
        print(f"❌ Erro ao importar processador Produtividade: {e}")
        return {"Produtividade": False}
    except Exception as e:
        print(f"❌ Erro no processamento Produtividade: {e}")
        return {"Produtividade": False}

def gerar_relatorio_final(resultados: Dict[str, bool]):
    """Gera relatório final da automação"""
    print("\n" + "=" * 60)
    print("📈 RELATÓRIO FINAL DA AUTOMAÇÃO")
    print("=" * 60)
    
    if not resultados:
        print("❌ Nenhum resultado para reportar")
        return
    
    sucesso = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    
    # Listagem detalhada
    for base, resultado in resultados.items():
        status = "✅ SUCESSO" if resultado else "❌ FALHA/NÃO ENCONTRADO"
        print(f"{status} - {base}")
    
    # Resumo
    print("\n📊 RESUMO:")
    print(f"   Total de bases: {total}")
    print(f"   Processadas com sucesso: {sucesso}")
    print(f"   Taxa de sucesso: {(sucesso/total*100):.1f}%" if total > 0 else "   Taxa: 0%")
    
    # Status final
    if sucesso == total:
        print("\n🎉 AUTOMAÇÃO 100% CONCLUÍDA!")
    elif sucesso > 0:
        print("\n⚠️  AUTOMAÇÃO PARCIALMENTE CONCLUÍDA")
    else:
        print("\n❌ NENHUMA BASE FOI PROCESSADA")
        print("💡 Verifique se os arquivos CSV estão na pasta 'dados'")

def mostrar_ajuda():
    """Mostra informações de ajuda"""
    print("""
🔍 ARQUIVOS SUPORTADOS:

GENESYS:
• Gestão da entrega N1 HC.csv (ou com (1), (2), etc.)
• Texto HC.csv
• Voz HC.csv

SALESFORCE:  
• BASE-BOLETIM-CRIADO-*.csv
• BASE-BOLETIM-RESOLVIDO-*.csv
• BASE-BOLETIM-COMENTARI*.csv (ou Cópia de...)

PRODUTIVIDADE:
• Base - Visão Produtiva.csv
• Base tempo - Visão Produtiva.csv

📂 ESTRUTURA RECOMENDADA:
automacao_boletins/
├── dados/              # Coloque seus CSVs aqui
├── config/             # boletim.json (credenciais)
└── main.py            # Execute este arquivo

💡 DICAS:
- O sistema detecta automaticamente arquivos duplicados
- Não precisa renomear arquivos com (1), (2) no nome
- Coloque todos os CSVs na pasta 'dados'
- Execute 'python main.py' para processar tudo
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Execute 'python main.py --help' para mais informações")
    
    input("\nPressione Enter para sair...")