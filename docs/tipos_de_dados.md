# 📊 Tipos de Dados e Interfaces Corretas

## 🎯 Visão Geral

Este documento explica quais tipos de dados devem ser processados por cada interface do sistema.

## 🟢 Interface Pulso Boletim (`interface_pulso_boletim.py`)

### 📊 Genesys - Boletim
- **VOZ HC** → `BASE_GENESYS_VOZ_HC.csv`
- **TEXTO HC** → `BASE_GENESYS_TEXTO_HC.csv`
- **GESTÃO N1** → `BASE_GENESYS_GESTAO_N1_HC.csv`

### 💼 Salesforce - Boletim
- **CRIADO** → Arquivos com "criado" no nome
- **RESOLVIDO** → Arquivos com "resolvido" no nome
- **COMENTÁRIOS** → Arquivos com "comentario" ou "bko" no nome

### 📈 Produtividade - Boletim
- **PRODUTIVIDADE** → Arquivos com "produtiv" no nome
- **TEMPO** → Arquivos com "tempo" no nome

---

## 🟡 Interface Power BI (`interface_powerbi.py`)

### 📊 Filas Genesys - Power BI/Looker Studio
- **FILAS GENESYS** → `Filas Genesys - Todas as Filas .csv`
  - Destino: Planilhas separadas para 1º e 2º semestre
  - Cor de destaque: **AMARELO** (ao invés de verde)
  - Usado para alimentar dashboards Power BI

---

## ❌ Problema Identificado

### 🚨 Erro Comum
Usuários tentam processar o arquivo **"Filas Genesys - Todas as Filas.csv"** na interface do **Pulso Boletim**.

### ✅ Solução
Este arquivo deve ser processado na interface **Power BI**:
```bash
python interface_powerbi.py
```

### 🔍 Diferenças Técnicas

| Característica | Pulso Boletim | Power BI |
|----------------|---------------|----------|
| **Dados** | VOZ HC, TEXTO HC, GESTÃO | FILAS |
| **Cor** | Verde Leroy Merlin | Amarelo |
| **Destino** | Planilha Boletim | Planilhas Semestre |
| **Estrutura** | Dados operacionais | Métricas de filas |

---

## 🛠️ Correções Implementadas

### 1. Detecção Melhorada
- Arquivos de filas são detectados e redirecionados
- Avisos claros sobre interface correta

### 2. Mensagens de Erro
- Sistema agora avisa quando arquivo está na interface errada
- Orientação clara sobre qual interface usar

### 3. Validação Preventiva
- Interface do boletim ignora arquivos de filas
- Mensagens explicativas durante execução

---

## 📋 Como Usar Corretamente

### Para Dados do Boletim
```bash
# Interface visual
python interface_pulso_boletim.py

# Linha de comando
python main.py --genesys     # Só Genesys
python main.py --salesforce  # Só Salesforce
python main.py               # Todos os sistemas
```

### Para Dados de Filas (Power BI)
```bash
# Interface visual Power BI
python interface_powerbi.py
```

---

## 🎯 Resumo

- **Filas Genesys** = Interface Power BI (amarelo)
- **VOZ/TEXTO/GESTÃO** = Interface Pulso Boletim (verde)
- **Salesforce/Produtividade** = Interface Pulso Boletim (verde)

✨ **Resultado**: Cada tipo de dado vai para a planilha e interface corretas!
