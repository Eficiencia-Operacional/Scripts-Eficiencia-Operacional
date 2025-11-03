#!/usr/bin/env python3
"""
🔧 GERENCIADOR DE CONFIGURAÇÕES DE PLANILHAS
Sistema centralizado para gerenciar IDs e configurações das planilhas

Recursos:
- Configuração centralizada em JSON
- Fácil atualização de IDs
- Histórico de mudanças
- Validação de configurações
- Interface de linha de comando para atualizações

Uso:
    from scripts.gerenciador_planilhas import GerenciadorPlanilhas
    
    # Obter ID de uma planilha
    gp = GerenciadorPlanilhas()
    id_genesys = gp.obter_id('genesys_boletim')
    
    # Atualizar ID via código
    gp.atualizar_planilha('genesys_boletim', novo_id='novo_id_aqui')
    
    # Via linha de comando
    python scripts/gerenciador_planilhas.py --atualizar genesys_boletim --id novo_id
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List

class GerenciadorPlanilhas:
    """Gerenciador centralizado de configurações de planilhas"""
    
    def __init__(self, caminho_config: str = None):
        """
        Inicializa o gerenciador
        
        Args:
            caminho_config: Caminho para o arquivo de configuração
        """
        if caminho_config is None:
            # Detectar automaticamente o caminho - arquivo agora está na pasta json/
            # Como estamos em scripts/, precisamos subir um nível para chegar na raiz
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.caminho_config = os.path.join(project_root, 'json', 'planilhas_config.json')
        else:
            self.caminho_config = caminho_config
            
        self.config = self._carregar_config()
        
    def _carregar_config(self) -> Dict[str, Any]:
        """Carrega a configuração do arquivo JSON"""
        try:
            if not os.path.exists(self.caminho_config):
                raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.caminho_config}")
            
            with open(self.caminho_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            print(f"✅ Configuração carregada: {len(config.get('planilhas', {}))} planilhas")
            return config
            
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            return {"planilhas": {}, "historico_mudancas": []}
    
    def _salvar_config(self) -> bool:
        """Salva a configuração no arquivo JSON"""
        try:
            with open(self.caminho_config, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuração salva em: {self.caminho_config}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def obter_id(self, chave_planilha: str) -> Optional[str]:
        """
        Obtém o ID de uma planilha
        
        Args:
            chave_planilha: Chave da planilha (ex: 'genesys_boletim')
            
        Returns:
            str: ID da planilha ou None se não encontrada
        """
        planilha = self.config.get('planilhas', {}).get(chave_planilha)
        if planilha:
            return planilha.get('id')
        
        print(f"⚠️  Planilha '{chave_planilha}' não encontrada")
        return None
    
    def obter_abas(self, chave_planilha: str) -> Dict[str, str]:
        """
        Obtém as abas de uma planilha
        
        Args:
            chave_planilha: Chave da planilha
            
        Returns:
            dict: Mapeamento de abas
        """
        planilha = self.config.get('planilhas', {}).get(chave_planilha)
        if planilha:
            return planilha.get('abas', {})
        
        print(f"⚠️  Abas da planilha '{chave_planilha}' não encontradas")
        return {}
    
    def obter_info_planilha(self, chave_planilha: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações completas de uma planilha
        
        Args:
            chave_planilha: Chave da planilha
            
        Returns:
            dict: Informações da planilha
        """
        return self.config.get('planilhas', {}).get(chave_planilha)
    
    def listar_planilhas(self) -> Dict[str, str]:
        """
        Lista todas as planilhas disponíveis
        
        Returns:
            dict: Mapeamento chave -> nome
        """
        planilhas = {}
        for chave, info in self.config.get('planilhas', {}).items():
            planilhas[chave] = info.get('nome', chave)
        
        return planilhas
    
    def atualizar_planilha(self, chave_planilha: str, novo_id: str, 
                          nova_descricao: str = None, novas_abas: Dict[str, str] = None,
                          registrar_historico: bool = True) -> bool:
        """
        Atualiza uma planilha
        
        Args:
            chave_planilha: Chave da planilha
            novo_id: Novo ID da planilha
            nova_descricao: Nova descrição (opcional)
            novas_abas: Novas abas (opcional)
            registrar_historico: Se deve registrar no histórico
            
        Returns:
            bool: Sucesso da operação
        """
        if chave_planilha not in self.config.get('planilhas', {}):
            print(f"❌ Planilha '{chave_planilha}' não encontrada")
            return False
        
        # Obter dados atuais
        planilha_atual = self.config['planilhas'][chave_planilha]
        id_antigo = planilha_atual.get('id', 'N/A')
        
        # Atualizar
        mudancas = []
        if novo_id != id_antigo:
            planilha_atual['id'] = novo_id
            mudancas.append(f"ID: {id_antigo[:8]}... → {novo_id[:8]}...")
        
        if nova_descricao:
            desc_antiga = planilha_atual.get('descricao', 'N/A')
            planilha_atual['descricao'] = nova_descricao
            mudancas.append(f"Descrição: {desc_antiga} → {nova_descricao}")
        
        if novas_abas:
            planilha_atual['abas'].update(novas_abas)
            mudancas.append(f"Abas atualizadas: {list(novas_abas.keys())}")
        
        planilha_atual['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d')
        
        # Registrar no histórico
        if registrar_historico and mudancas:
            self._registrar_historico(f"Atualização da planilha '{chave_planilha}'", mudancas)
        
        # Salvar
        if self._salvar_config():
            print(f"✅ Planilha '{chave_planilha}' atualizada com sucesso!")
            for mudanca in mudancas:
                print(f"   📝 {mudanca}")
            return True
        
        return False
    
    def criar_planilha(self, chave_planilha: str, nome: str, id_planilha: str,
                      descricao: str, tipo: str, abas: Dict[str, str]) -> bool:
        """
        Cria uma nova configuração de planilha
        
        Args:
            chave_planilha: Chave única da planilha
            nome: Nome display da planilha
            id_planilha: ID do Google Sheets
            descricao: Descrição da planilha
            tipo: Tipo (boletim, power_bi)
            abas: Mapeamento de abas
            
        Returns:
            bool: Sucesso da operação
        """
        if chave_planilha in self.config.get('planilhas', {}):
            print(f"❌ Planilha '{chave_planilha}' já existe!")
            return False
        
        nova_planilha = {
            "nome": nome,
            "id": id_planilha,
            "descricao": descricao,
            "tipo": tipo,
            "ultima_atualizacao": datetime.now().strftime('%Y-%m-%d'),
            "abas": abas
        }
        
        if 'planilhas' not in self.config:
            self.config['planilhas'] = {}
        
        self.config['planilhas'][chave_planilha] = nova_planilha
        
        # Registrar no histórico
        self._registrar_historico(f"Criação da planilha '{chave_planilha}'", [
            f"Nome: {nome}",
            f"ID: {id_planilha[:8]}...",
            f"Tipo: {tipo}",
            f"Abas: {list(abas.keys())}"
        ])
        
        if self._salvar_config():
            print(f"✅ Nova planilha '{chave_planilha}' criada com sucesso!")
            return True
        
        return False
    
    def remover_planilha(self, chave_planilha: str) -> bool:
        """
        Remove uma planilha da configuração
        
        Args:
            chave_planilha: Chave da planilha
            
        Returns:
            bool: Sucesso da operação
        """
        if chave_planilha not in self.config.get('planilhas', {}):
            print(f"❌ Planilha '{chave_planilha}' não encontrada")
            return False
        
        planilha_info = self.config['planilhas'][chave_planilha]
        nome = planilha_info.get('nome', chave_planilha)
        
        del self.config['planilhas'][chave_planilha]
        
        # Registrar no histórico
        self._registrar_historico(f"Remoção da planilha '{chave_planilha}'", [
            f"Nome: {nome}",
            f"Motivo: Remoção manual"
        ])
        
        if self._salvar_config():
            print(f"✅ Planilha '{chave_planilha}' removida com sucesso!")
            return True
        
        return False
    
    def gerar_url(self, chave_planilha: str, aba: str = None) -> Optional[str]:
        """
        Gera URL completa para uma planilha
        
        Args:
            chave_planilha: Chave da planilha
            aba: Nome da aba específica (opcional)
            
        Returns:
            str: URL da planilha
        """
        id_planilha = self.obter_id(chave_planilha)
        if not id_planilha:
            return None
        
        template = self.config.get('templates', {}).get('url_completa', 
                   'https://docs.google.com/spreadsheets/d/{id}/edit#gid=0')
        
        return template.format(id=id_planilha)
    
    def _registrar_historico(self, titulo: str, mudancas: List[str]):
        """Registra mudança no histórico"""
        if 'historico_mudancas' not in self.config:
            self.config['historico_mudancas'] = []
        
        entrada = {
            "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "titulo": titulo,
            "mudancas": mudancas,
            "autor": "Sistema"
        }
        
        self.config['historico_mudancas'].insert(0, entrada)  # Mais recente primeiro
        
        # Manter apenas os últimos 50 registros
        self.config['historico_mudancas'] = self.config['historico_mudancas'][:50]
    
    def imprimir_status(self):
        """Imprime status atual das configurações"""
        print("\n" + "="*80)
        print("📊 STATUS DAS CONFIGURAÇÕES DE PLANILHAS")
        print("="*80)
        
        planilhas = self.config.get('planilhas', {})
        print(f"📈 Total de planilhas: {len(planilhas)}")
        
        # Agrupar por tipo
        tipos = {}
        for chave, info in planilhas.items():
            tipo = info.get('tipo', 'indefinido')
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(chave)
        
        for tipo, lista in tipos.items():
            print(f"\n🔸 Tipo: {tipo.upper()}")
            for chave in lista:
                info = planilhas[chave]
                nome = info.get('nome', chave)
                id_planilha = info.get('id', 'N/A')
                ultima_atualizacao = info.get('ultima_atualizacao', 'N/A')
                
                print(f"   📋 {nome}")
                print(f"      🔑 Chave: {chave}")
                print(f"      🆔 ID: {id_planilha[:20]}...")
                print(f"      📅 Última atualização: {ultima_atualizacao}")
                print(f"      📑 Abas: {len(info.get('abas', {}))}")
        
        # Histórico recente
        historico = self.config.get('historico_mudancas', [])
        if historico:
            print(f"\n📜 ÚLTIMAS 5 MUDANÇAS:")
            for entrada in historico[:5]:
                data = entrada.get('data', 'N/A')
                titulo = entrada.get('titulo', 'N/A')
                print(f"   📅 {data}: {titulo}")
        
        print("="*80)


def main():
    """Interface de linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🔧 Gerenciador de Configurações de Planilhas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python gerenciador_planilhas.py --status                    # Mostra status atual
  python gerenciador_planilhas.py --listar                    # Lista todas as planilhas
  python gerenciador_planilhas.py --atualizar genesys_boletim --id novo_id_aqui
  python gerenciador_planilhas.py --criar nova_planilha --nome "Nova Planilha" --id id_planilha --tipo boletim
        """
    )
    
    parser.add_argument('--status', action='store_true', help='Mostra status das configurações')
    parser.add_argument('--listar', action='store_true', help='Lista todas as planilhas')
    parser.add_argument('--atualizar', type=str, help='Chave da planilha para atualizar')
    parser.add_argument('--criar', type=str, help='Chave da nova planilha para criar')
    parser.add_argument('--remover', type=str, help='Chave da planilha para remover')
    parser.add_argument('--id', type=str, help='Novo ID da planilha')
    parser.add_argument('--nome', type=str, help='Nome da planilha')
    parser.add_argument('--descricao', type=str, help='Descrição da planilha')
    parser.add_argument('--tipo', type=str, choices=['boletim', 'power_bi'], help='Tipo da planilha')
    parser.add_argument('--url', type=str, help='Gerar URL para planilha')
    
    args = parser.parse_args()
    
    # Inicializar gerenciador
    gp = GerenciadorPlanilhas()
    
    if args.status:
        gp.imprimir_status()
    
    elif args.listar:
        print("\n📋 PLANILHAS DISPONÍVEIS:")
        print("-" * 50)
        planilhas = gp.listar_planilhas()
        for chave, nome in planilhas.items():
            id_planilha = gp.obter_id(chave)
            print(f"🔑 {chave}")
            print(f"   📛 {nome}")
            print(f"   🆔 {id_planilha[:30]}...")
            print()
    
    elif args.atualizar and args.id:
        sucesso = gp.atualizar_planilha(
            args.atualizar, 
            args.id, 
            args.descricao
        )
        if sucesso:
            print(f"✅ Planilha '{args.atualizar}' atualizada!")
        else:
            print(f"❌ Falha ao atualizar planilha '{args.atualizar}'")
    
    elif args.criar and args.nome and args.id and args.tipo:
        sucesso = gp.criar_planilha(
            args.criar,
            args.nome,
            args.id,
            args.descricao or f"Planilha {args.nome}",
            args.tipo,
            {"base": "BASE"}  # Aba padrão
        )
        if sucesso:
            print(f"✅ Nova planilha '{args.criar}' criada!")
        else:
            print(f"❌ Falha ao criar planilha '{args.criar}'")
    
    elif args.remover:
        sucesso = gp.remover_planilha(args.remover)
        if sucesso:
            print(f"✅ Planilha '{args.remover}' removida!")
        else:
            print(f"❌ Falha ao remover planilha '{args.remover}'")
    
    elif args.url:
        url = gp.gerar_url(args.url)
        if url:
            print(f"🔗 URL da planilha '{args.url}':")
            print(f"   {url}")
        else:
            print(f"❌ Planilha '{args.url}' não encontrada")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
