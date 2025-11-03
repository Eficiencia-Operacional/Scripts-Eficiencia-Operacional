#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN
Executa processamento completo das planilhas Genesys e Salesforce

Este script executa automaticamente:
1. Processamento de dados Genesys (VOZ, TEXTO, GESTÃO)
2. Processamento de dados Salesforce (CRIADO, RESOLVIDO, COMENTÁRIOS)
3. Relatório consolidado dos resultados

Uso:
    python main.py                # Executa tudo automaticamente
    python main.py --genesys      # Só Genesys
    python main.py --salesforce   # Só Salesforce
    python main.py --help         # Mostra ajuda
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

import argparse
from datetime import datetime

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), 'core')
sys.path.append(core_dir)

from src.core.google_sheets_base import GoogleSheetsBase
from scripts.gerenciador_planilhas import GerenciadorPlanilhas

# Inicializar gerenciador de configurações
gp = GerenciadorPlanilhas()

# Configurações das planilhas - AGORA DINÂMICAS
def obter_config_planilhas():
    """Obtém configurações atualizadas das planilhas"""
    return {
        "genesys": {
            "id": gp.obter_id("genesys_boletim"),
            "nome": "📊 GENESYS",
            "deteccao": {
                "voz_hc": (gp.obter_abas("genesys_boletim").get("voz_hc", "BASE VOZ"), "GENESYS VOZ HC"),
                "texto_hc": (gp.obter_abas("genesys_boletim").get("texto_hc", "BASE TEXTO"), "GENESYS TEXTO HC"), 
                "gestao_n1": (gp.obter_abas("genesys_boletim").get("gestao_n1", "BASE GE COLABORADOR"), "GENESYS GESTÃO N1"),
                "gestao": (gp.obter_abas("genesys_boletim").get("gestao_entrega", "BASE GE COLABORADOR"), "GENESYS GESTÃO"),
                "fila": (gp.obter_abas("genesys_boletim").get("fila", "BASE VOZ FILA"), "GENESYS FILA")
            }
        },
        "salesforce": {
            "id": gp.obter_id("salesforce_boletim"),
            "nome": "💼 SALESFORCE", 
            "deteccao": {
                "criado": (gp.obter_abas("salesforce_boletim").get("criado", "BASE ATUALIZADA CORRETA - CRIADO"), "SALESFORCE CRIADO"),
                "resolvido": (gp.obter_abas("salesforce_boletim").get("resolvido", "BASE ATUALIZADA CORRETA - RESOLVIDA"), "SALESFORCE RESOLVIDO"),
                "comentario_bko": (gp.obter_abas("salesforce_boletim").get("comentario_bko", "COMENTARIO BKO"), "SALESFORCE COMENTÁRIOS"),
                "seller": (gp.obter_abas("salesforce_boletim").get("seller", "DADOS SELLER"), "SALESFORCE SELLER")
            }
        },
        "produtividade": {
            "id": gp.obter_id("produtividade_boletim"),
            "nome": "📈 PRODUTIVIDADE",
            "deteccao": {
                "produtividade": (gp.obter_abas("produtividade_boletim").get("produtividade", "BASE PROD"), "PRODUTIVIDADE VISÃO"),
                "tempo": (gp.obter_abas("produtividade_boletim").get("tempo", "BASE TEMPO"), "PRODUTIVIDADE TEMPO")
            }
        }
    }

# Obter configurações dinâmicas
PLANILHAS_CONFIG = obter_config_planilhas()

def detectar_tipo_arquivo(nome_arquivo, sistema):
    """Detecta o tipo do arquivo baseado no sistema (genesys, salesforce ou produtividade)"""
    nome_lower = nome_arquivo.lower()
    
    if sistema == "genesys":
        if 'voz' in nome_lower and 'hc' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["voz_hc"]
        elif 'texto' in nome_lower and 'hc' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["texto_hc"]
        elif 'gestão' in nome_lower or 'gestao' in nome_lower:
            if 'n1' in nome_lower or 'entrega' in nome_lower:
                return PLANILHAS_CONFIG["genesys"]["deteccao"]["gestao_n1"]
            else:
                return PLANILHAS_CONFIG["genesys"]["deteccao"]["gestao"]
        elif 'fila' in nome_lower and 'todas' in nome_lower:
            # Arquivo de filas deve ir para Power BI, não para o boletim
            print(f"⚠️  ATENÇÃO: Arquivo '{nome_arquivo}' é de FILAS GENESYS")
            print("🎯 Este arquivo deve ser processado pela interface Power BI, não pelo Pulso Boletim")
            print("💡 Use a interface Power BI para processar dados de filas")
            return None, None  # Não processar na interface do boletim
        elif 'fila' in nome_lower:
            return PLANILHAS_CONFIG["genesys"]["deteccao"]["fila"]
    
    elif sistema == "salesforce":
        if 'criado' in nome_lower or 'created' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["criado"]
        elif 'resolvido' in nome_lower or 'resolved' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["resolvido"]
        elif 'comentario' in nome_lower or 'comment' in nome_lower or 'bko' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["comentario_bko"]
        elif 'seller' in nome_lower or 'vendedor' in nome_lower:
            return PLANILHAS_CONFIG["salesforce"]["deteccao"]["seller"]
    
    elif sistema == "produtividade":
        if 'tempo' in nome_lower:
            return PLANILHAS_CONFIG["produtividade"]["deteccao"]["tempo"]
        elif 'produtiv' in nome_lower or 'visao' in nome_lower or 'visão' in nome_lower:
            return PLANILHAS_CONFIG["produtividade"]["deteccao"]["produtividade"]
    
    return None, None

def buscar_arquivos_csv():
    """Busca todos os arquivos CSV na pasta data"""
    data_dir = os.path.join(current_dir, 'data')
    arquivos_csv = []
    
    if os.path.exists(data_dir):
        for arquivo in os.listdir(data_dir):
            if arquivo.lower().endswith('.csv'):
                arquivos_csv.append(arquivo)
    
    return arquivos_csv, data_dir

def processar_sistema(sistema_nome, executar_sistema=True):
    """Processa um sistema específico (genesys, salesforce ou produtividade)"""
    if not executar_sistema:
        return {"sucessos": 0, "falhas": 0, "processados": 0}
    
    print(f"\n{'='*70}")
    print(f"🎯 PROCESSANDO SISTEMA: {PLANILHAS_CONFIG[sistema_nome]['nome']}")
    print(f"{'='*70}")
    
    # Configurar para a planilha específica
    id_planilha = PLANILHAS_CONFIG[sistema_nome]["id"]
    sheets = GoogleSheetsBase(id_planilha=id_planilha)
    
    print(f"📊 ID da Planilha: {id_planilha}")
    print(f"🔗 Conectando...")
    
    try:
        client = sheets.client
        planilha = client.open_by_key(id_planilha)
        print(f"✅ Planilha: '{planilha.title}'")
        
        # Listar abas disponíveis
        abas_disponiveis = [aba.title for aba in planilha.worksheets()]
        print(f"📑 Abas disponíveis: {len(abas_disponiveis)} abas")
        
        # Buscar arquivos
        arquivos_csv, data_dir = buscar_arquivos_csv()
        
        # Verificar se há arquivos de filas que não devem ser processados aqui
        arquivos_filas = [arq for arq in arquivos_csv if 'fila' in arq.lower() and 'todas' in arq.lower()]
        if arquivos_filas:
            print(f"⚠️  AVISO: Encontrados {len(arquivos_filas)} arquivo(s) de FILAS GENESYS:")
            for arq in arquivos_filas:
                print(f"   📄 {arq}")
            print("🎯 Estes arquivos devem ser processados pela interface POWER BI, não pelo Pulso Boletim")
            print("💡 Execute: python interface_powerbi.py")
            print("-" * 70)
        
        # Filtrar arquivos para este sistema
        arquivos_sistema = []
        for arquivo in arquivos_csv:
            aba_destino, tipo_detectado = detectar_tipo_arquivo(arquivo, sistema_nome)
            if aba_destino and aba_destino in abas_disponiveis:
                arquivos_sistema.append((arquivo, aba_destino, tipo_detectado))
            elif 'fila' in arquivo.lower() and 'todas' in arquivo.lower():
                # Arquivo de filas - mostrar aviso específico
                print(f"⚠️  IGNORADO: {arquivo} (arquivo de filas - use interface Power BI)")
        
        print(f"📁 Arquivos {sistema_nome.upper()} válidos: {len(arquivos_sistema)}")
        
        if not arquivos_sistema:
            if arquivos_filas:
                print(f"💡 Use a interface Power BI para processar os arquivos de filas encontrados")
            else:
                print(f"⚠️  Nenhum arquivo {sistema_nome.upper()} encontrado")
            return {"sucessos": 0, "falhas": 0, "processados": 0}
        
        # Processar cada arquivo
        sucessos = 0
        falhas = 0
        
        for arquivo, aba_destino, tipo_detectado in arquivos_sistema:
            print(f"\n📤 Processando: {arquivo}")
            print(f"🎯 Tipo: {tipo_detectado}")
            print(f"📝 Destino: {aba_destino}")
            
            # Verificar dados existentes
            aba = planilha.worksheet(aba_destino)
            valores_existentes = aba.get_all_values()
            linhas_com_dados = sum(1 for linha in valores_existentes if any(cell.strip() for cell in linha))
            print(f"📊 Dados existentes: {linhas_com_dados:,} linhas")
            
            # Processar arquivo
            resultado = sheets.enviar_csv_para_planilha(arquivo, aba_destino)
            
            if resultado:
                print(f"✅ SUCESSO: {arquivo} → {aba_destino}")
                sucessos += 1
            else:
                print(f"❌ FALHA: {arquivo} → {aba_destino}")
                falhas += 1
            
            print("-" * 50)
        
        return {"sucessos": sucessos, "falhas": falhas, "processados": sucessos + falhas}
        
    except Exception as e:
        print(f"❌ ERRO no sistema {sistema_nome.upper()}: {e}")
        return {"sucessos": 0, "falhas": 1, "processados": 1}

def main():
    """Função principal"""
    
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description='🚀 Automação Principal Leroy Merlin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py                    # Executa Genesys + Salesforce + Produtividade
  python main.py --genesys          # Só Genesys
  python main.py --salesforce       # Só Salesforce
  python main.py --produtividade    # Só Produtividade
  python main.py --dados ./csvs     # Especifica pasta de dados
        """
    )
    
    parser.add_argument('--genesys', action='store_true', 
                       help='Processar apenas sistema Genesys')
    parser.add_argument('--salesforce', action='store_true',
                       help='Processar apenas sistema Salesforce')
    parser.add_argument('--produtividade', action='store_true',
                       help='Processar apenas sistema Produtividade')
    parser.add_argument('--dados', type=str, 
                       help='Pasta onde estão os arquivos CSV')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo detalhado')
    
    args = parser.parse_args()
    
    # Header principal
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("🚀 AUTOMAÇÃO PRINCIPAL LEROY MERLIN")
    print("=" * 80)
    print(f"⏰ Iniciado em: {timestamp}")
    print("🔧 Modo: COMPLEMENTAR (preserva dados existentes)")
    print("🎨 Primeira linha: VERDE LEROY MERLIN")
    print("📋 Cabeçalho: REMOVIDO automaticamente")
    
    # Determinar quais sistemas executar
    executar_genesys = True
    executar_salesforce = True
    executar_produtividade = True
    
    # Lógica para sistemas específicos
    sistemas_selecionados = []
    if args.genesys:
        sistemas_selecionados.append("genesys")
    if args.salesforce:
        sistemas_selecionados.append("salesforce")
    if args.produtividade:
        sistemas_selecionados.append("produtividade")
    
    # Se algum sistema foi especificamente selecionado, executar apenas eles
    if sistemas_selecionados:
        executar_genesys = "genesys" in sistemas_selecionados
        executar_salesforce = "salesforce" in sistemas_selecionados
        executar_produtividade = "produtividade" in sistemas_selecionados
        sistemas_texto = " + ".join([s.upper() for s in sistemas_selecionados])
        print(f"🎯 Executando apenas: {sistemas_texto}")
    else:
        print("🎯 Executando: GENESYS + SALESFORCE + PRODUTIVIDADE")
    
    # Verificar arquivos disponíveis
    arquivos_csv, data_dir = buscar_arquivos_csv()
    print(f"📁 Pasta de dados: {data_dir}")
    print(f"📄 Arquivos CSV encontrados: {len(arquivos_csv)}")
    
    if not arquivos_csv:
        print(f"❌ Nenhum arquivo CSV encontrado em: {data_dir}")
        print("💡 Adicione arquivos CSV na pasta data/ e execute novamente")
        return
    
    # Executar processamentos
    inicio_processamento = datetime.now()
    
    resultado_genesys = processar_sistema("genesys", executar_genesys)
    resultado_salesforce = processar_sistema("salesforce", executar_salesforce)
    resultado_produtividade = processar_sistema("produtividade", executar_produtividade)
    
    fim_processamento = datetime.now()
    duracao = fim_processamento - inicio_processamento
    
    # Relatório final consolidado
    print(f"\n{'='*80}")
    print("🎉 RELATÓRIO FINAL CONSOLIDADO")
    print(f"{'='*80}")
    print(f"⏱️  Tempo total: {duracao}")
    print(f"📊 Processamento iniciado: {inicio_processamento.strftime('%H:%M:%S')}")
    print(f"🏁 Processamento concluído: {fim_processamento.strftime('%H:%M:%S')}")
    print()
    
    # Estatísticas por sistema
    total_sucessos = resultado_genesys["sucessos"] + resultado_salesforce["sucessos"] + resultado_produtividade["sucessos"]
    total_falhas = resultado_genesys["falhas"] + resultado_salesforce["falhas"] + resultado_produtividade["falhas"]
    total_processados = resultado_genesys["processados"] + resultado_salesforce["processados"] + resultado_produtividade["processados"]
    
    if executar_genesys:
        print(f"📊 GENESYS:")
        print(f"   ✅ Sucessos: {resultado_genesys['sucessos']}")
        print(f"   ❌ Falhas: {resultado_genesys['falhas']}")
        print(f"   📊 Total: {resultado_genesys['processados']}")
    
    if executar_salesforce:
        print(f"💼 SALESFORCE:")
        print(f"   ✅ Sucessos: {resultado_salesforce['sucessos']}")
        print(f"   ❌ Falhas: {resultado_salesforce['falhas']}")
        print(f"   📊 Total: {resultado_salesforce['processados']}")
    
    if executar_produtividade:
        print(f"📈 PRODUTIVIDADE:")
        print(f"   ✅ Sucessos: {resultado_produtividade['sucessos']}")
        print(f"   ❌ Falhas: {resultado_produtividade['falhas']}")
        print(f"   📊 Total: {resultado_produtividade['processados']}")
    
    print(f"\n🎯 TOTAIS GERAIS:")
    print(f"   ✅ Total de sucessos: {total_sucessos}")
    print(f"   ❌ Total de falhas: {total_falhas}")
    print(f"   📊 Total processado: {total_processados}")
    
    # Taxa de sucesso
    if total_processados > 0:
        taxa_sucesso = (total_sucessos / total_processados) * 100
        print(f"   📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
    
    # Links para as planilhas
    if total_sucessos > 0:
        print(f"\n🔗 ACESSE AS PLANILHAS ATUALIZADAS:")
        if executar_genesys and resultado_genesys["sucessos"] > 0:
            print(f"   📊 Genesys: https://docs.google.com/spreadsheets/d/{PLANILHAS_CONFIG['genesys']['id']}")
        if executar_salesforce and resultado_salesforce["sucessos"] > 0:
            print(f"   💼 Salesforce: https://docs.google.com/spreadsheets/d/{PLANILHAS_CONFIG['salesforce']['id']}")
    
    print(f"\n✨ Automação concluída! Primeira linha de cada inserção está pintada de VERDE LEROY MERLIN 🟢")
    print("=" * 80)

if __name__ == "__main__":
    main()