#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO - Gerenciador de Planilhas
Script para demonstrar todas as funcionalidades do gerenciador

Uso:
    python scripts/demo_gerenciador.py
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from scripts.gerenciador_planilhas import GerenciadorPlanilhas

def print_header(titulo):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🎯 {titulo}")
    print("="*60)

def print_subheader(titulo):
    """Imprime subcabeçalho formatado"""
    print(f"\n📋 {titulo}")
    print("-"*40)

def demonstrar_listagem():
    """Demonstra listagem de planilhas"""
    print_header("DEMONSTRAÇÃO: Listagem de Planilhas")
    
    gp = GerenciadorPlanilhas()
    
    print_subheader("Todas as Planilhas Configuradas")
    planilhas = gp.listar_planilhas()
    
    for chave, nome in planilhas.items():
        id_planilha = gp.obter_id(chave)
        abas = gp.obter_abas(chave)
        info = gp.obter_info_planilha(chave)
        
        print(f"🔑 {chave}")
        print(f"   📛 {nome}")
        print(f"   🆔 {id_planilha[:30]}...")
        print(f"   📂 Tipo: {info.get('tipo', 'N/A').upper()}")
        print(f"   📑 Abas: {len(abas)} configuradas")
        print(f"   📅 Última atualização: {info.get('ultima_atualizacao', 'N/A')}")
        print()

def demonstrar_informacoes():
    """Demonstra obtenção de informações"""
    print_header("DEMONSTRAÇÃO: Obtenção de Informações")
    
    gp = GerenciadorPlanilhas()
    
    # Exemplo com Genesys
    print_subheader("Informações Detalhadas - Genesys")
    
    id_genesys = gp.obter_id('genesys_boletim')
    abas_genesys = gp.obter_abas('genesys_boletim')
    info_genesys = gp.obter_info_planilha('genesys_boletim')
    
    print(f"📊 ID da Planilha: {id_genesys}")
    print(f"📋 Nome: {info_genesys.get('nome', 'N/A')}")
    print(f"📝 Descrição: {info_genesys.get('descricao', 'N/A')}")
    print(f"📂 Tipo: {info_genesys.get('tipo', 'N/A')}")
    print(f"📅 Última Atualização: {info_genesys.get('ultima_atualizacao', 'N/A')}")
    
    print(f"\n📑 Abas Configuradas ({len(abas_genesys)}):")
    for chave_aba, nome_aba in abas_genesys.items():
        print(f"   • {chave_aba}: '{nome_aba}'")
    
    # URL gerada
    url = gp.gerar_url('genesys_boletim')
    print(f"\n🔗 URL: {url}")

def demonstrar_validacao():
    """Demonstra validação de IDs"""
    print_header("DEMONSTRAÇÃO: Validação de IDs")
    
    ids_teste = [
        ("1ABC123def456GHI789jkl012MNO345pqr678STU", "✅ ID Válido"),
        ("1ABC123", "❌ Muito curto"),
        ("1ABC123def456GHI789jkl012MNO345pqr678STU123", "❌ Muito longo"),
        ("1ABC123def456GHI789jkl012MNO345pqr678ST@", "❌ Caractere inválido"),
        ("", "❌ Vazio")
    ]
    
    print_subheader("Testes de Validação")
    
    for id_teste, esperado in ids_teste:
        print(f"\n🔍 Testando: '{id_teste[:20]}{'...' if len(id_teste) > 20 else ''}'")
        
        # Validação manual
        valido = True
        erros = []
        
        if not id_teste:
            valido = False
            erros.append("ID vazio")
        elif len(id_teste) != 44:
            valido = False
            erros.append(f"Tamanho incorreto: {len(id_teste)} (deve ser 44)")
        elif not id_teste.replace('-', '').replace('_', '').isalnum():
            valido = False
            erros.append("Contém caracteres inválidos")
        
        resultado = "✅ VÁLIDO" if valido else f"❌ INVÁLIDO: {', '.join(erros)}"
        print(f"   Resultado: {resultado}")
        print(f"   Esperado: {esperado}")

def demonstrar_urls():
    """Demonstra geração de URLs"""
    print_header("DEMONSTRAÇÃO: Geração de URLs")
    
    gp = GerenciadorPlanilhas()
    
    print_subheader("URLs das Planilhas")
    
    planilhas = ['genesys_boletim', 'salesforce_boletim', 'produtividade_boletim']
    
    for planilha in planilhas:
        id_planilha = gp.obter_id(planilha)
        if id_planilha:
            url = gp.gerar_url(planilha)
            nome = gp.obter_info_planilha(planilha).get('nome', planilha)
            
            print(f"\n📊 {nome}")
            print(f"   🆔 ID: {id_planilha}")
            print(f"   🔗 URL: {url}")
        else:
            print(f"\n❌ Planilha '{planilha}' não encontrada")

def demonstrar_historico():
    """Demonstra histórico de mudanças"""
    print_header("DEMONSTRAÇÃO: Histórico de Mudanças")
    
    gp = GerenciadorPlanilhas()
    
    historico = gp.config.get('historico_mudancas', [])
    
    if not historico:
        print("📝 Nenhuma mudança registrada ainda")
        return
    
    print_subheader(f"Últimas {min(5, len(historico))} Mudanças")
    
    for i, entrada in enumerate(historico[:5]):
        data = entrada.get('data', 'N/A')
        titulo = entrada.get('titulo', 'N/A')
        mudancas = entrada.get('mudancas', [])
        autor = entrada.get('autor', 'N/A')
        
        print(f"\n{i+1}. 📅 {data}")
        print(f"   👤 Autor: {autor}")
        print(f"   📝 {titulo}")
        
        if mudancas:
            print("   🔄 Mudanças:")
            for mudanca in mudancas[:3]:  # Mostrar só as primeiras 3
                print(f"      • {mudanca}")
            if len(mudancas) > 3:
                print(f"      ... e mais {len(mudancas) - 3} mudanças")

def demonstrar_backups():
    """Demonstra listagem de backups"""
    print_header("DEMONSTRAÇÃO: Sistema de Backups")
    
    gp = GerenciadorPlanilhas()
    
    # Diretório de backups
    backup_dir = os.path.join(os.path.dirname(gp.caminho_config), 'backups')
    
    print_subheader("Informações de Backup")
    print(f"📁 Diretório de backups: {backup_dir}")
    print(f"📄 Arquivo principal: {gp.caminho_config}")
    
    if not os.path.exists(backup_dir):
        print("⚠️  Diretório de backups não existe ainda")
        return
    
    # Listar backups
    backups = []
    for arquivo in os.listdir(backup_dir):
        if arquivo.endswith('.json'):
            caminho = os.path.join(backup_dir, arquivo)
            stat = os.stat(caminho)
            
            backups.append({
                'arquivo': arquivo,
                'tamanho': stat.st_size,
                'modificado': datetime.fromtimestamp(stat.st_mtime)
            })
    
    if not backups:
        print("📝 Nenhum backup encontrado")
        return
    
    # Ordenar por data (mais recente primeiro)
    backups.sort(key=lambda x: x['modificado'], reverse=True)
    
    print_subheader(f"Backups Disponíveis ({len(backups)})")
    
    for backup in backups[:5]:  # Mostrar só os 5 mais recentes
        arquivo = backup['arquivo']
        tamanho_kb = backup['tamanho'] / 1024
        data = backup['modificado'].strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"💾 {arquivo}")
        print(f"   📅 Data: {data}")
        print(f"   📊 Tamanho: {tamanho_kb:.1f} KB")
        print()

def demonstrar_status_sistema():
    """Demonstra status geral do sistema"""
    print_header("DEMONSTRAÇÃO: Status do Sistema")
    
    try:
        gp = GerenciadorPlanilhas()
        
        # Estatísticas básicas
        total_planilhas = len(gp.config.get('planilhas', {}))
        historico = gp.config.get('historico_mudancas', [])
        total_mudancas = len(historico)
        
        # Backup info
        backup_dir = os.path.join(os.path.dirname(gp.caminho_config), 'backups')
        total_backups = 0
        if os.path.exists(backup_dir):
            total_backups = len([f for f in os.listdir(backup_dir) if f.endswith('.json')])
        
        print_subheader("Estatísticas Gerais")
        print(f"📊 Total de planilhas configuradas: {total_planilhas}")
        print(f"📜 Total de mudanças registradas: {total_mudancas}")
        print(f"💾 Total de backups disponíveis: {total_backups}")
        print(f"📁 Arquivo de configuração: {os.path.basename(gp.caminho_config)}")
        
        # Verificar integridade
        print_subheader("Verificação de Integridade")
        
        problemas = []
        
        for chave, dados in gp.config.get('planilhas', {}).items():
            id_planilha = dados.get('id', '')
            
            if not id_planilha:
                problemas.append(f"Planilha '{chave}' sem ID")
            elif len(id_planilha) != 44:
                problemas.append(f"Planilha '{chave}' com ID inválido (tamanho: {len(id_planilha)})")
            elif not id_planilha.replace('-', '').replace('_', '').isalnum():
                problemas.append(f"Planilha '{chave}' com caracteres inválidos no ID")
        
        if problemas:
            print("⚠️  Problemas encontrados:")
            for problema in problemas:
                print(f"   • {problema}")
        else:
            print("✅ Sistema íntegro - nenhum problema encontrado")
        
        # Status por tipo
        print_subheader("Status por Tipo")
        
        tipos = {}
        for chave, dados in gp.config.get('planilhas', {}).items():
            tipo = dados.get('tipo', 'indefinido')
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(chave)
        
        for tipo, planilhas in tipos.items():
            print(f"📂 {tipo.upper()}: {len(planilhas)} planilhas")
            for planilha in planilhas:
                nome = gp.config['planilhas'][planilha].get('nome', planilha)
                status = "✅" if gp.obter_id(planilha) else "❌"
                print(f"   {status} {nome}")
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")

def menu_principal():
    """Menu principal da demonstração"""
    print_header("DEMONSTRAÇÃO INTERATIVA - Gerenciador de Planilhas")
    
    opcoes = [
        ("1", "📋 Listar todas as planilhas", demonstrar_listagem),
        ("2", "📊 Informações detalhadas", demonstrar_informacoes),
        ("3", "🔍 Validação de IDs", demonstrar_validacao),
        ("4", "🔗 Geração de URLs", demonstrar_urls),
        ("5", "📜 Histórico de mudanças", demonstrar_historico),
        ("6", "💾 Sistema de backups", demonstrar_backups),
        ("7", "🔧 Status do sistema", demonstrar_status_sistema),
        ("8", "🎨 Abrir interface visual", lambda: os.system("python interfaces/interface_gerenciador_planilhas.py")),
        ("0", "🚪 Sair", None)
    ]
    
    while True:
        print("\n" + "-"*50)
        print("🎯 MENU DE DEMONSTRAÇÃO")
        print("-"*50)
        
        for opcao, descricao, _ in opcoes:
            print(f"{opcao}. {descricao}")
        
        escolha = input("\n👆 Escolha uma opção: ").strip()
        
        if escolha == "0":
            print("\n👋 Demonstração encerrada!")
            break
        
        # Encontrar e executar opção
        opcao_encontrada = False
        for opcao, descricao, funcao in opcoes:
            if escolha == opcao and funcao:
                funcao()
                opcao_encontrada = True
                break
        
        if not opcao_encontrada:
            print("❌ Opção inválida! Tente novamente.")
        
        input("\n⏸️  Pressione Enter para continuar...")

def main():
    """Função principal"""
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")

if __name__ == "__main__":
    main()
