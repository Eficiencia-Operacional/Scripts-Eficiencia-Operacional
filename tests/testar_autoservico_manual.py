"""
Teste manual do processador de Autoserviço
"""

import sys
import os

# Adicionar diretório raiz ao path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.processadores.powerbi.autoservico.autoservico_primeiro_semestre import ProcessadorAutoservicoPrimeiroSemestre

print("="*60)
print("🧪 TESTE MANUAL - PROCESSADOR AUTOSERVIÇO PRIMEIRO SEMESTRE")
print("="*60)

try:
    # Inicializar processador
    print("\n1️⃣ Inicializando processador...")
    processador = ProcessadorAutoservicoPrimeiroSemestre()
    print("✅ Processador inicializado com sucesso!")
    
    # Definir caminho do CSV
    caminho_csv = os.path.join(project_root, 'data', 'Autoserviço Power BI.csv')
    
    if not os.path.exists(caminho_csv):
        print(f"❌ Arquivo não encontrado: {caminho_csv}")
        sys.exit(1)
    
    print(f"\n2️⃣ Arquivo encontrado: {os.path.basename(caminho_csv)}")
    
    # Processar e enviar
    print("\n3️⃣ Processando e enviando dados...")
    resultado = processador.processar_e_enviar(caminho_csv)
    
    # Exibir resultado
    print("\n" + "="*60)
    print("📊 RESULTADO DO PROCESSAMENTO:")
    print("="*60)
    
    if resultado['sucesso']:
        print(f"✅ Status: SUCESSO")
        print(f"📁 Arquivo: {resultado['arquivo']}")
        print(f"📊 Linhas: {resultado['linhas_processadas']}")
        print(f"📄 Planilha: {resultado['planilha']}")
        print(f"📑 Aba: {resultado['aba']}")
        print(f"🕒 Timestamp: {resultado['timestamp']}")
    else:
        print(f"❌ Status: ERRO")
        print(f"❌ Mensagem: {resultado.get('erro', 'Erro desconhecido')}")
        print(f"📁 Arquivo: {resultado.get('arquivo', 'N/A')}")
    
except Exception as e:
    print(f"\n❌ ERRO FATAL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("🏁 Teste finalizado")
print("="*60)
