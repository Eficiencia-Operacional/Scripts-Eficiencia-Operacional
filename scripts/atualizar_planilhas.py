#!/usr/bin/env python3
"""
🔧 UTILITÁRIO DE ATUALIZAÇÃO MENSAL
Script para facilitar a atualização mensal das planilhas

Este script permite:
- Atualizar todas as planilhas de uma vez
- Fazer backup das configurações antigas
- Validar novos IDs antes da atualização
- Registrar histórico de mudanças

Uso:
    python scripts/atualizar_planilhas.py --mes dezembro --ano 2025
    python scripts/atualizar_planilhas.py --individual genesys_boletim --id novo_id
    python scripts/atualizar_planilhas.py --backup
    python scripts/atualizar_planilhas.py --restaurar backup_2025_11.json
"""

import os
import sys
import json
import argparse
from datetime import datetime
import shutil

# Adicionar diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

from scripts.gerenciador_planilhas import GerenciadorPlanilhas

class AtualizadorPlanilhas:
    """Utilitário para atualização mensal das planilhas"""
    
    def __init__(self):
        self.gp = GerenciadorPlanilhas()
        self.backup_dir = os.path.join(root_dir, 'config', 'backups')
        
        # Criar diretório de backup se não existir
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def fazer_backup(self) -> str:
        """
        Faz backup das configurações atuais
        
        Returns:
            str: Caminho do arquivo de backup
        """
        timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
        nome_backup = f"planilhas_backup_{timestamp}.json"
        caminho_backup = os.path.join(self.backup_dir, nome_backup)
        
        try:
            # Copiar arquivo de configuração atual
            shutil.copy2(self.gp.caminho_config, caminho_backup)
            
            print(f"✅ Backup criado: {nome_backup}")
            print(f"📁 Local: {caminho_backup}")
            
            return caminho_backup
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None
    
    def restaurar_backup(self, caminho_backup: str) -> bool:
        """
        Restaura um backup específico
        
        Args:
            caminho_backup: Caminho do arquivo de backup
            
        Returns:
            bool: Sucesso da operação
        """
        if not os.path.exists(caminho_backup):
            print(f"❌ Arquivo de backup não encontrado: {caminho_backup}")
            return False
        
        try:
            # Fazer backup atual antes de restaurar
            backup_atual = self.fazer_backup()
            if backup_atual:
                print(f"📋 Backup atual salvo como: {os.path.basename(backup_atual)}")
            
            # Restaurar backup
            shutil.copy2(caminho_backup, self.gp.caminho_config)
            
            # Recarregar configurações
            self.gp = GerenciadorPlanilhas()
            
            print(f"✅ Backup restaurado: {os.path.basename(caminho_backup)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def validar_id_planilha(self, id_planilha: str) -> bool:
        """
        Valida se um ID de planilha é válido
        
        Args:
            id_planilha: ID da planilha para validar
            
        Returns:
            bool: Se o ID é válido
        """
        try:
            # Tentar conectar à planilha
            from src.core.google_sheets_base import GoogleSheetsBase
            
            sheets = GoogleSheetsBase(id_planilha=id_planilha)
            client = sheets.client
            planilha = client.open_by_key(id_planilha)
            
            print(f"✅ ID válido - Planilha: '{planilha.title}'")
            print(f"📑 Abas: {len(planilha.worksheets())} encontradas")
            
            return True
            
        except Exception as e:
            print(f"❌ ID inválido: {e}")
            return False
    
    def atualizar_planilha_individual(self, chave: str, novo_id: str, 
                                    validar: bool = True) -> bool:
        """
        Atualiza uma planilha individual
        
        Args:
            chave: Chave da planilha
            novo_id: Novo ID
            validar: Se deve validar o ID antes da atualização
            
        Returns:
            bool: Sucesso da operação
        """
        print(f"\n🔄 Atualizando planilha: {chave}")
        print(f"🆔 Novo ID: {novo_id}")
        
        # Validar ID se solicitado
        if validar:
            print("🔍 Validando novo ID...")
            if not self.validar_id_planilha(novo_id):
                print("❌ Atualização cancelada - ID inválido")
                return False
        
        # Fazer backup antes da atualização
        backup = self.fazer_backup()
        if not backup:
            print("⚠️  Continuando sem backup...")
        
        # Atualizar
        sucesso = self.gp.atualizar_planilha(chave, novo_id)
        
        if sucesso:
            print(f"✅ Planilha {chave} atualizada com sucesso!")
        else:
            print(f"❌ Falha ao atualizar planilha {chave}")
            
            # Restaurar backup em caso de falha
            if backup:
                print("🔄 Restaurando backup...")
                self.restaurar_backup(backup)
        
        return sucesso
    
    def atualizar_lote(self, atualizacoes: dict, validar: bool = True) -> dict:
        """
        Atualiza múltiplas planilhas em lote
        
        Args:
            atualizacoes: Dict {chave: novo_id}
            validar: Se deve validar IDs
            
        Returns:
            dict: Resultado das atualizações
        """
        print(f"\n🚀 ATUALIZAÇÃO EM LOTE")
        print(f"📊 {len(atualizacoes)} planilhas para atualizar")
        print("="*60)
        
        # Fazer backup completo
        backup = self.fazer_backup()
        if not backup:
            print("❌ Falha ao criar backup - cancelando atualização em lote")
            return {"sucessos": 0, "falhas": len(atualizacoes)}
        
        resultados = {"sucessos": 0, "falhas": 0, "detalhes": {}}
        
        # Validar todos os IDs primeiro (se solicitado)
        if validar:
            print("🔍 Validando todos os IDs...")
            for chave, novo_id in atualizacoes.items():
                print(f"   Validando {chave}...")
                if not self.validar_id_planilha(novo_id):
                    print(f"❌ ID inválido para {chave}: {novo_id}")
                    resultados["falhas"] += 1
                    resultados["detalhes"][chave] = "ID inválido"
                    continue
        
        # Executar atualizações
        for chave, novo_id in atualizacoes.items():
            if chave in resultados["detalhes"]:
                continue  # Pular se já falhou na validação
            
            print(f"\n📝 Atualizando {chave}...")
            sucesso = self.gp.atualizar_planilha(chave, novo_id, registrar_historico=False)
            
            if sucesso:
                resultados["sucessos"] += 1
                resultados["detalhes"][chave] = "Sucesso"
            else:
                resultados["falhas"] += 1
                resultados["detalhes"][chave] = "Falha na atualização"
        
        # Registrar atualização em lote no histórico
        if resultados["sucessos"] > 0:
            mudancas = [f"Atualização em lote: {resultados['sucessos']} sucessos, {resultados['falhas']} falhas"]
            for chave, status in resultados["detalhes"].items():
                mudancas.append(f"  {chave}: {status}")
            
            self.gp._registrar_historico("Atualização em lote", mudancas)
            self.gp._salvar_config()
        
        print(f"\n📊 RESULTADO DA ATUALIZAÇÃO EM LOTE:")
        print(f"✅ Sucessos: {resultados['sucessos']}")
        print(f"❌ Falhas: {resultados['falhas']}")
        
        return resultados
    
    def listar_backups(self):
        """Lista todos os backups disponíveis"""
        if not os.path.exists(self.backup_dir):
            print("📁 Nenhum backup encontrado")
            return
        
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
        backups.sort(reverse=True)  # Mais recente primeiro
        
        print(f"\n📋 BACKUPS DISPONÍVEIS ({len(backups)}):")
        print("-" * 60)
        
        for backup in backups:
            caminho = os.path.join(self.backup_dir, backup)
            stat = os.stat(caminho)
            tamanho = stat.st_size
            data_mod = datetime.fromtimestamp(stat.st_mtime)
            
            print(f"📄 {backup}")
            print(f"   📅 {data_mod.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"   📊 {tamanho:,} bytes")
            print()
    
    def preparar_atualizacao_mensal(self, mes: str, ano: int) -> dict:
        """
        Prepara template para atualização mensal
        
        Args:
            mes: Nome do mês
            ano: Ano
            
        Returns:
            dict: Template de atualização
        """
        template = {
            "mes": mes,
            "ano": ano,
            "data_planejada": f"{ano}-{datetime.strptime(mes, '%B').month:02d}-01",
            "planilhas": {}
        }
        
        # Obter planilhas atuais
        planilhas_atuais = self.gp.listar_planilhas()
        
        for chave, nome in planilhas_atuais.items():
            id_atual = self.gp.obter_id(chave)
            template["planilhas"][chave] = {
                "nome": nome,
                "id_atual": id_atual,
                "novo_id": "INSERIR_NOVO_ID_AQUI",
                "status": "pendente"
            }
        
        # Salvar template
        nome_template = f"template_atualizacao_{mes.lower()}_{ano}.json"
        caminho_template = os.path.join(self.backup_dir, nome_template)
        
        with open(caminho_template, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Template criado: {nome_template}")
        print(f"📁 Local: {caminho_template}")
        print("\n📝 Edite o arquivo e substitua 'INSERIR_NOVO_ID_AQUI' pelos IDs corretos")
        print("💡 Depois execute: python atualizar_planilhas.py --executar-template caminho_do_template")
        
        return template
    
    def executar_template(self, caminho_template: str) -> bool:
        """
        Executa um template de atualização
        
        Args:
            caminho_template: Caminho do arquivo template
            
        Returns:
            bool: Sucesso da operação
        """
        if not os.path.exists(caminho_template):
            print(f"❌ Template não encontrado: {caminho_template}")
            return False
        
        try:
            with open(caminho_template, 'r', encoding='utf-8') as f:
                template = json.load(f)
            
            atualizacoes = {}
            
            for chave, info in template.get("planilhas", {}).items():
                novo_id = info.get("novo_id", "")
                if novo_id and novo_id != "INSERIR_NOVO_ID_AQUI":
                    atualizacoes[chave] = novo_id
            
            if not atualizacoes:
                print("❌ Nenhuma atualização válida encontrada no template")
                return False
            
            print(f"🚀 Executando template: {os.path.basename(caminho_template)}")
            print(f"📅 Mês/Ano: {template.get('mes', 'N/A')}/{template.get('ano', 'N/A')}")
            
            resultado = self.atualizar_lote(atualizacoes)
            
            return resultado["falhas"] == 0
            
        except Exception as e:
            print(f"❌ Erro ao executar template: {e}")
            return False


def main():
    """Interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description='🔧 Utilitário de Atualização Mensal de Planilhas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Preparar atualização mensal
  python atualizar_planilhas.py --preparar --mes dezembro --ano 2025
  
  # Atualizar planilha individual
  python atualizar_planilhas.py --individual genesys_boletim --id novo_id_aqui
  
  # Fazer backup
  python atualizar_planilhas.py --backup
  
  # Listar backups
  python atualizar_planilhas.py --listar-backups
  
  # Restaurar backup
  python atualizar_planilhas.py --restaurar backup_2025_11_01_120000.json
  
  # Executar template preenchido
  python atualizar_planilhas.py --executar-template template_dezembro_2025.json
        """
    )
    
    parser.add_argument('--preparar', action='store_true', help='Preparar template de atualização mensal')
    parser.add_argument('--mes', type=str, help='Mês para atualização (ex: dezembro)')
    parser.add_argument('--ano', type=int, help='Ano para atualização')
    parser.add_argument('--individual', type=str, help='Atualizar planilha individual (chave)')
    parser.add_argument('--id', type=str, help='Novo ID da planilha')
    parser.add_argument('--backup', action='store_true', help='Fazer backup das configurações')
    parser.add_argument('--restaurar', type=str, help='Restaurar backup específico')
    parser.add_argument('--listar-backups', action='store_true', help='Listar backups disponíveis')
    parser.add_argument('--executar-template', type=str, help='Executar template de atualização')
    parser.add_argument('--validar', action='store_false', help='Pular validação de IDs')
    
    args = parser.parse_args()
    
    # Inicializar atualizador
    atualizador = AtualizadorPlanilhas()
    
    try:
        if args.preparar and args.mes and args.ano:
            atualizador.preparar_atualizacao_mensal(args.mes, args.ano)
        
        elif args.individual and args.id:
            atualizador.atualizar_planilha_individual(args.individual, args.id, args.validar)
        
        elif args.backup:
            atualizador.fazer_backup()
        
        elif args.restaurar:
            caminho_backup = args.restaurar
            if not os.path.isabs(caminho_backup):
                caminho_backup = os.path.join(atualizador.backup_dir, caminho_backup)
            atualizador.restaurar_backup(caminho_backup)
        
        elif args.listar_backups:
            atualizador.listar_backups()
        
        elif args.executar_template:
            caminho_template = args.executar_template
            if not os.path.isabs(caminho_template):
                caminho_template = os.path.join(atualizador.backup_dir, caminho_template)
            atualizador.executar_template(caminho_template)
        
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
