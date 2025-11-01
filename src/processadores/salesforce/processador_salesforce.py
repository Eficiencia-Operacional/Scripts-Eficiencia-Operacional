"""
Orquestrador principal para Salesforce
Gerencia todos os processadores do Salesforce
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from criado import ProcessadorCriado
from resolvido import ProcessadorResolvido
from comentario_bko import ProcessadorComentarioBKO

class ProcessadorSalesforce:
    """Orquestrador para todas as bases do Salesforce"""
    
    def __init__(self, id_planilha=None):
        self.processadores = {
            "Criado": ProcessadorCriado(id_planilha=id_planilha),
            "Resolvido": ProcessadorResolvido(id_planilha=id_planilha),
            "Comentário BKO": ProcessadorComentarioBKO(id_planilha=id_planilha)
        }
    
    def processar_todos(self):
        """Processa todas as bases Salesforce disponíveis"""
        resultados = {}
        
        print("🔄 Processando bases Salesforce...")
        
        for nome, processador in self.processadores.items():
            try:
                resultado = processador.processar()
                resultados[nome] = resultado
                if resultado:
                    print(f"✅ {nome} processado")
                else:
                    print(f"⚠️  {nome} não encontrado")
            except Exception as e:
                print(f"❌ Erro ao processar {nome}: {str(e)}")
                resultados[nome] = False
        
        return resultados
    
    def processar_individual(self, tipo_base, caminho_csv=None):
        """Processa uma base específica"""
        if tipo_base not in self.processadores:
            print(f"❌ Tipo '{tipo_base}' não encontrado")
            return False
        
        try:
            return self.processadores[tipo_base].processar(caminho_csv)
        except Exception as e:
            print(f"❌ Erro ao processar {tipo_base}: {str(e)}")
            return False