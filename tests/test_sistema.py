#!/usr/bin/env python3
"""
🔧 TESTE COMPLETO DO SISTEMA
Script para verificar se tudo está funcionando
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, '.')

def test_gerenciador():
    """Teste do gerenciador de planilhas"""
    try:
        from scripts.gerenciador_planilhas import GerenciadorPlanilhas
        gp = GerenciadorPlanilhas()
        planilhas = gp.listar_planilhas()
        print(f"✅ Gerenciador: {len(planilhas)} planilhas carregadas")
        return True
    except Exception as e:
        print(f"❌ Gerenciador: {e}")
        return False

def test_interfaces():
    """Teste das interfaces"""
    resultados = []
    
    interfaces = [
        ("Power BI", "interfaces.interface_powerbi"),
        ("Pulso Boletim", "interfaces.interface_pulso_boletim"),
        ("Gerenciador", "interfaces.interface_gerenciador"),
        ("Gerenciador Planilhas", "interfaces.interface_gerenciador_planilhas")
    ]
    
    for nome, modulo in interfaces:
        try:
            __import__(modulo)
            print(f"✅ Interface {nome}: OK")
            resultados.append(True)
        except Exception as e:
            print(f"❌ Interface {nome}: {e}")
            resultados.append(False)
    
    return all(resultados)

def test_processadores():
    """Teste dos processadores"""
    resultados = []
    
    processadores = [
        ("Genesys", "src.processadores.genesys.processador_genesys"),
        ("Salesforce", "src.processadores.salesforce.processador_salesforce"),
        ("Produtividade", "src.processadores.produtividade.produtividade"),
        ("Power BI Primeiro", "src.processadores.powerbi.genesys.filas_primeiro_semestre"),
        ("Power BI Segundo", "src.processadores.powerbi.genesys.filas_segundo_semestre")
    ]
    
    for nome, modulo in processadores:
        try:
            __import__(modulo)
            print(f"✅ Processador {nome}: OK")
            resultados.append(True)
        except Exception as e:
            print(f"❌ Processador {nome}: {e}")
            resultados.append(False)
    
    return all(resultados)

def test_renomeador():
    """Teste do renomeador"""
    try:
        from renomeador_inteligente import RenomeadorInteligente
        renomeador = RenomeadorInteligente()
        print("✅ Renomeador: OK")
        return True
    except Exception as e:
        print(f"❌ Renomeador: {e}")
        return False

def main():
    """Teste principal"""
    print("🔧 TESTE COMPLETO DO SISTEMA")
    print("="*50)
    
    testes = [
        ("Gerenciador de Planilhas", test_gerenciador),
        ("Interfaces", test_interfaces),
        ("Processadores", test_processadores),
        ("Renomeador", test_renomeador)
    ]
    
    sucessos = 0
    total = len(testes)
    
    for nome, funcao in testes:
        print(f"\n📋 Testando {nome}...")
        if funcao():
            sucessos += 1
    
    print("\n" + "="*50)
    print(f"📊 RESULTADO FINAL: {sucessos}/{total} testes passou")
    
    if sucessos == total:
        print("🎉 SISTEMA 100% FUNCIONAL!")
        return True
    else:
        print("⚠️ Alguns componentes precisam de atenção")
        return False

if __name__ == "__main__":
    main()
