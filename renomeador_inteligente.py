#!/usr/bin/env python3
"""
📝 RENOMEADOR INTELIGENTE - LEROY MERLIN
Sistema de renomeação automática de arquivos CSV com padrões inteligentes

Este script:
1. Identifica padrões nos nomes dos arquivos
2. Remove timestamps e datas variáveis
3. Padroniza nomes para detecção automática
4. Mantém backups dos nomes originais
"""

import os
import re
import shutil
from datetime import datetime
import json

class RenomeadorInteligente:
    """Classe para renomeação inteligente de arquivos CSV"""
    
    def __init__(self, pasta_dados="data"):
        self.pasta_dados = pasta_dados
        # Histórico agora fica na pasta json/ para melhor organização
        self.historico_file = os.path.join("json", "historico_renomeacao.json")
        self.padroes_renomeacao = self.definir_padroes()
        
    def definir_padroes(self):
        """Define padrões de renomeação para cada tipo de arquivo"""
        return {
            # POWER BI - Padrão para Filas Genesys (vários formatos possíveis)
            r'.*filas.*genesys.*todas.*filas.*\.csv$': 'Filas Genesys - Todas as Filas .csv',
            r'.*filas.*genesys.*\.csv$': 'Filas Genesys - Todas as Filas .csv',
            r'.*genesys.*filas.*\.csv$': 'Filas Genesys - Todas as Filas .csv',
            r'^filas\s*genesys\.csv$': 'Filas Genesys - Todas as Filas .csv',  # "Filas genesys.csv"
            r'^fila\s*genesys\.csv$': 'Filas Genesys - Todas as Filas .csv',   # "Fila genesys.csv"
            
            # POWER BI - Padrão para Autoserviço (vários formatos possíveis)
            r'.*autoservi[cç]o.*power\s*bi.*\.csv$': 'Autoserviço Power BI.csv',
            r'.*autoservi[cç]o.*powerbi.*\.csv$': 'Autoserviço Power BI.csv',
            r'.*auto.*servi[cç]o.*\.csv$': 'Autoserviço Power BI.csv',
            r'^autoservi[cç]o\s*-.*\.csv$': 'Autoserviço Power BI.csv',
            r'^autoservi[cç]o.*\.csv$': 'Autoserviço Power BI.csv',
            
            # SALESFORCE - Padrões
            r'.*criado.*-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.csv$': 'BASE_SALESFORCE_CRIADO.csv',
            r'.*resolvid[oa].*-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.csv$': 'BASE_SALESFORCE_RESOLVIDO.csv',
            r'.*comentario.*bko.*-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.csv$': 'BASE_SALESFORCE_COMENTARIO_BKO.csv',
            r'cópia de.*comentario.*bko.*\.csv$': 'BASE_SALESFORCE_COMENTARIO_BKO.csv',
            r'.*seller.*-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.csv$': 'BASE_SALESFORCE_SELLER.csv',
            
            # GENESYS - Padrões  
            r'.*voz.*hc.*\.csv$': 'BASE_GENESYS_VOZ_HC.csv',
            r'.*texto.*hc.*\.csv$': 'BASE_GENESYS_TEXTO_HC.csv',
            r'.*gestão.*entrega.*n1.*hc.*\.csv$': 'BASE_GENESYS_GESTAO_N1_HC.csv',
            r'.*gestao.*entrega.*n1.*hc.*\.csv$': 'BASE_GENESYS_GESTAO_N1_HC.csv',
            r'.*gestão.*hc.*\.csv$': 'BASE_GENESYS_GESTAO_HC.csv',
            r'.*gestao.*hc.*\.csv$': 'BASE_GENESYS_GESTAO_HC.csv',
            r'.*fila.*hc.*\.csv$': 'BASE_GENESYS_FILA_HC.csv',
            
            # PRODUTIVIDADE - Padrões (mais específicos primeiro)
            r'.*base.*tempo.*visão.*produtiva.*\.csv$': 'BASE_TEMPO.csv',
            r'.*base\s*-\s*visão.*produtiva.*\.csv$': 'BASE_PRODUTIVIDADE.csv',
            r'.*base.*visão.*produtiva.*\.csv$': 'BASE_PRODUTIVIDADE.csv',
            r'.*tempo.*visão.*produtiva.*\.csv$': 'BASE_TEMPO.csv',
            r'.*visão.*produtiva.*\.csv$': 'BASE_PRODUTIVIDADE.csv',
            
            # Padrões genéricos (fallback)
            r'.*criado.*\.csv$': 'BASE_SALESFORCE_CRIADO.csv',
            r'.*resolvid[oa].*\.csv$': 'BASE_SALESFORCE_RESOLVIDO.csv',
            r'.*comentario.*\.csv$': 'BASE_SALESFORCE_COMENTARIO_BKO.csv',
            r'.*voz.*\.csv$': 'BASE_GENESYS_VOZ_HC.csv',
            r'.*texto.*\.csv$': 'BASE_GENESYS_TEXTO_HC.csv',
            r'.*gestão.*\.csv$': 'BASE_GENESYS_GESTAO_HC.csv',
            r'.*gestao.*\.csv$': 'BASE_GENESYS_GESTAO_HC.csv',
        }
    
    def salvar_historico(self, renomeacoes):
        """Salva histórico das renomeações"""
        historico = {
            'timestamp': datetime.now().isoformat(),
            'renomeacoes': renomeacoes,
            'total_arquivos': len(renomeacoes)
        }
        
        # Carregar histórico existente
        historico_completo = []
        if os.path.exists(self.historico_file):
            try:
                with open(self.historico_file, 'r', encoding='utf-8') as f:
                    historico_completo = json.load(f)
            except:
                pass
        
        # Adicionar nova entrada
        historico_completo.append(historico)
        
        # Manter apenas os últimos 10 históricos
        if len(historico_completo) > 10:
            historico_completo = historico_completo[-10:]
        
        # Salvar
        try:
            with open(self.historico_file, 'w', encoding='utf-8') as f:
                json.dump(historico_completo, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Não foi possível salvar histórico: {e}")
    
    def detectar_tipo_arquivo(self, nome_arquivo):
        """Detecta o tipo do arquivo baseado no nome"""
        nome_lower = nome_arquivo.lower()
        
        # Testar cada padrão
        for padrao, novo_nome in self.padroes_renomeacao.items():
            if re.match(padrao, nome_lower):
                return novo_nome
        
        return None
    
    def listar_arquivos_csv(self):
        """Lista todos os arquivos CSV na pasta"""
        if not os.path.exists(self.pasta_dados):
            return []
        
        arquivos = []
        for arquivo in os.listdir(self.pasta_dados):
            if arquivo.lower().endswith('.csv') and not arquivo.startswith('historico'):
                caminho_completo = os.path.join(self.pasta_dados, arquivo)
                if os.path.isfile(caminho_completo):
                    arquivos.append(arquivo)
        
        return sorted(arquivos)
    
    def renomear_arquivos(self, modo_teste=False):
        """Renomeia arquivos CSV baseado nos padrões definidos"""
        arquivos_csv = self.listar_arquivos_csv()
        
        if not arquivos_csv:
            return {
                'sucesso': False,
                'mensagem': 'Nenhum arquivo CSV encontrado na pasta data/',
                'arquivos_processados': 0,
                'renomeacoes': []
            }
        
        renomeacoes = []
        sucessos = 0
        falhas = 0
        
        print(f"🔍 Encontrados {len(arquivos_csv)} arquivos CSV")
        print("-" * 60)
        
        for arquivo in arquivos_csv:
            nome_original = arquivo
            novo_nome = self.detectar_tipo_arquivo(arquivo)
            
            if not novo_nome:
                print(f"⚠️ Padrão não reconhecido: {nome_original}")
                falhas += 1
                continue
            
            # Se já tem o nome correto, pular
            if nome_original == novo_nome:
                print(f"✅ Já padronizado: {nome_original}")
                continue
            
            caminho_original = os.path.join(self.pasta_dados, nome_original)
            caminho_novo = os.path.join(self.pasta_dados, novo_nome)
            
            # Verificar se arquivo de destino já existe
            if os.path.exists(caminho_novo):
                # Se for exatamente igual, apenas remover o arquivo antigo
                if os.path.samefile(caminho_original, caminho_novo):
                    print(f"✅ Mesmo arquivo: {nome_original}")
                    continue
                else:
                    # Arquivo diferente com mesmo nome de destino
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    novo_nome_backup = f"{novo_nome.replace('.csv', '')}_{timestamp}.csv"
                    caminho_novo = os.path.join(self.pasta_dados, novo_nome_backup)
                    print(f"⚠️ Conflito detectado, usando: {novo_nome_backup}")
            
            registro_renomeacao = {
                'nome_original': nome_original,
                'nome_novo': os.path.basename(caminho_novo),
                'tipo_detectado': self.identificar_tipo_por_nome_novo(os.path.basename(caminho_novo)),
                'tamanho_mb': round(os.path.getsize(caminho_original) / (1024*1024), 2)
            }
            
            if modo_teste:
                print(f"🧪 TESTE: {nome_original} → {os.path.basename(caminho_novo)}")
                registro_renomeacao['status'] = 'simulado'
            else:
                try:
                    shutil.move(caminho_original, caminho_novo)
                    print(f"✅ RENOMEADO: {nome_original} → {os.path.basename(caminho_novo)}")
                    registro_renomeacao['status'] = 'sucesso'
                    sucessos += 1
                except Exception as e:
                    print(f"❌ ERRO: {nome_original} - {e}")
                    registro_renomeacao['status'] = 'erro'
                    registro_renomeacao['erro'] = str(e)
                    falhas += 1
            
            renomeacoes.append(registro_renomeacao)
        
        # Salvar histórico se não for modo teste
        if not modo_teste and renomeacoes:
            self.salvar_historico(renomeacoes)
        
        return {
            'sucesso': sucessos > 0 or (modo_teste and len(renomeacoes) > 0),
            'modo_teste': modo_teste,
            'arquivos_processados': len(arquivos_csv),
            'sucessos': sucessos,
            'falhas': falhas,
            'renomeacoes': renomeacoes,
            'mensagem': f'Processados {len(arquivos_csv)} arquivos - {sucessos} sucessos, {falhas} falhas'
        }
    
    def identificar_tipo_por_nome_novo(self, nome_novo):
        """Identifica o tipo baseado no nome novo padronizado"""
        if 'SALESFORCE' in nome_novo:
            if 'CRIADO' in nome_novo:
                return 'Salesforce - Casos Criados'
            elif 'RESOLVIDO' in nome_novo:
                return 'Salesforce - Casos Resolvidos'
            elif 'COMENTARIO' in nome_novo:
                return 'Salesforce - Comentários BKO'
            elif 'SELLER' in nome_novo:
                return 'Salesforce - Dados Seller'
        elif 'GENESYS' in nome_novo:
            if 'VOZ' in nome_novo:
                return 'Genesys - VOZ HC'
            elif 'TEXTO' in nome_novo:
                return 'Genesys - TEXTO HC'
            elif 'GESTAO_N1' in nome_novo:
                return 'Genesys - Gestão N1'
            elif 'GESTAO' in nome_novo:
                return 'Genesys - Gestão'
            elif 'FILA' in nome_novo:
                return 'Genesys - Fila'
        
        return 'Tipo não identificado'
    
    def preview_renomeacoes(self):
        """Mostra preview das renomeações sem executar"""
        return self.renomear_arquivos(modo_teste=True)
    
    def executar_renomeacoes(self):
        """Executa as renomeações reais"""
        return self.renomear_arquivos(modo_teste=False)
    
    def restaurar_backup(self, entrada_historico=0):
        """Restaura arquivos de um backup específico do histórico"""
        if not os.path.exists(self.historico_file):
            return {'sucesso': False, 'mensagem': 'Nenhum histórico encontrado'}
        
        try:
            with open(self.historico_file, 'r', encoding='utf-8') as f:
                historico_completo = json.load(f)
            
            if entrada_historico >= len(historico_completo):
                return {'sucesso': False, 'mensagem': 'Entrada de histórico não encontrada'}
            
            # Pegar entrada específica (0 = mais recente)
            entrada = historico_completo[-(entrada_historico + 1)]
            renomeacoes = entrada['renomeacoes']
            
            restaurados = 0
            for item in renomeacoes:
                if item['status'] == 'sucesso':
                    caminho_atual = os.path.join(self.pasta_dados, item['nome_novo'])
                    caminho_original = os.path.join(self.pasta_dados, item['nome_original'])
                    
                    if os.path.exists(caminho_atual) and not os.path.exists(caminho_original):
                        try:
                            shutil.move(caminho_atual, caminho_original)
                            restaurados += 1
                        except Exception as e:
                            print(f"❌ Erro ao restaurar {item['nome_novo']}: {e}")
            
            return {
                'sucesso': True,
                'restaurados': restaurados,
                'mensagem': f'{restaurados} arquivos restaurados do backup de {entrada["timestamp"]}'
            }
            
        except Exception as e:
            return {'sucesso': False, 'mensagem': f'Erro ao restaurar: {e}'}

def main():
    """Função principal para uso via linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(description='🎯 Renomeador Inteligente Leroy Merlin')
    parser.add_argument('--preview', action='store_true', help='Mostrar preview sem renomear')
    parser.add_argument('--executar', action='store_true', help='Executar renomeações')
    parser.add_argument('--pasta', default='data', help='Pasta dos arquivos CSV')
    
    args = parser.parse_args()
    
    renomeador = RenomeadorInteligente(args.pasta)
    
    print("📝 RENOMEADOR INTELIGENTE LEROY MERLIN")
    print("=" * 50)
    
    if args.preview:
        print("🔍 MODO PREVIEW - Simulação de renomeações:")
        resultado = renomeador.preview_renomeacoes()
    elif args.executar:
        print("🚀 EXECUTANDO RENOMEAÇÕES:")
        resultado = renomeador.executar_renomeacoes()
    else:
        print("💡 Use --preview para simular ou --executar para renomear")
        return
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {resultado['mensagem']}")
    
    if resultado['renomeacoes']:
        print(f"\n📋 Detalhes das renomeações:")
        for item in resultado['renomeacoes']:
            status_emoji = "✅" if item['status'] == 'sucesso' else "🧪" if item['status'] == 'simulado' else "❌"
            print(f"   {status_emoji} {item['nome_original']} → {item['nome_novo']}")
            print(f"      📊 {item['tipo_detectado']} ({item['tamanho_mb']} MB)")

if __name__ == "__main__":
    main()