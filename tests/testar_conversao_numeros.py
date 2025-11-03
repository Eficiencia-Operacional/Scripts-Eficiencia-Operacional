#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testar conversão de números brasileiros"""

import pandas as pd

def converter_numero_brasileiro(valor):
    """Converte número brasileiro (1.234,56) para formato padrão (1234.56)"""
    if pd.isna(valor) or valor == '' or valor is None:
        return ''
    
    valor_str = str(valor).strip()
    
    # Se já é um número válido, retornar
    try:
        float(valor_str)
        return valor_str
    except:
        pass
    
    # Verificar se é um formato de tempo (HH:MM:SS)
    if ':' in valor_str:
        return valor_str
    
    # Verificar se tem ponto E vírgula (formato brasileiro: 1.234,56)
    if '.' in valor_str and ',' in valor_str:
        # Remover pontos (separador de milhar) e trocar vírgula por ponto
        valor_str = valor_str.replace('.', '').replace(',', '.')
    # Se tem apenas vírgula (formato brasileiro: 123,56)
    elif ',' in valor_str and '.' not in valor_str:
        valor_str = valor_str.replace(',', '.')
    # Se tem apenas ponto
    elif '.' in valor_str:
        # Verificar se é separador de milhar ou decimal
        partes = valor_str.split('.')
        
        # Se todas as partes (exceto a primeira) têm exatamente 3 dígitos, é separador de milhar
        if len(partes) > 1:
            # Verificar padrão de milhar: primeira parte pode ter 1-3 dígitos, resto tem 3
            is_milhar = all(len(p) == 3 for p in partes[1:])
            
            if is_milhar and len(partes[0]) <= 3:
                # É separador de milhar (ex: 96.875 ou 1.234.567)
                valor_str = valor_str.replace('.', '')
            # Caso contrário, assumir que é decimal
    
    # Remover apóstrofos e aspas
    valor_str = valor_str.replace("'", "").replace('"', '')
    
    # Tentar converter
    try:
        # Se for inteiro, retornar sem casas decimais
        num = float(valor_str)
        if num == int(num):
            return str(int(num))
        return str(num)
    except:
        # Se não conseguir converter, retornar original
        return valor

# Exemplos de teste baseados na planilha
testes = [
    ('9.705.136.560.149.140', '9705136560149140'),  # Grande número com pontos
    ('0,85', '0.85'),  # Decimal com vírgula
    ('0,8', '0.8'),  # Decimal com vírgula
    ('0,98', '0.98'),  # Decimal com vírgula
    ('0,9', '0.9'),  # Decimal com vírgula
    ('96.875', '96875'),  # Número com ponto (milhar)
    ('0.85', '0.85'),  # Decimal com ponto (já correto)
    ('00:36:08.422', '00:36:08.422'),  # Tempo
    ('00:00:11.746', '00:00:11.746'),  # Tempo
    ('9.620.991.253.644.310', '9620991253644310'),  # Grande número
    ('0,295561724138', '0.295561724138'),  # Decimal longo
]

print("="*70)
print("TESTE DE CONVERSÃO DE NÚMEROS BRASILEIROS")
print("="*70)
print()

todos_ok = True
for entrada, esperado in testes:
    resultado = converter_numero_brasileiro(entrada)
    status = "✅" if resultado == esperado else "❌"
    
    if resultado != esperado:
        todos_ok = False
        print(f"{status} '{entrada}' -> '{resultado}' (esperado: '{esperado}')")
    else:
        print(f"{status} '{entrada}' -> '{resultado}'")

print()
print("="*70)
if todos_ok:
    print("✅ TODOS OS TESTES PASSARAM!")
else:
    print("❌ ALGUNS TESTES FALHARAM")
print("="*70)
