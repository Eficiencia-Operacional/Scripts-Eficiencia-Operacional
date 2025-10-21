# 📋 Automação de Boletins - Leroy Merlin

Sistema inteligente para processamento automático de relatórios do Genesys e Salesforce.

## 🏗️ Estrutura Organizada

```
automacao_boletins/
├── 📁 main.py                     # 🚀 ENTRADA ÚNICA - Execute este arquivo
├── 📁 dados/                      # 📂 Coloque seus arquivos CSV aqui
├── 📁 config/                     # ⚙️ Configurações e credenciais
│   ├── boletim.json              # 🔑 Credenciais Google Sheets
│   └── README.md                 # 📋 Info das planilhas
├── 📁 core/                       # 🧠 Motor principal
│   ├── __init__.py
│   └── google_sheets_base.py     # 🔧 Classe base inteligente
├── 📁 processadores/              # ⚙️ Processadores especializados
│   ├── __init__.py
│   ├── 📁 genesys/               # 📊 Processadores Genesys
│   │   ├── __init__.py
│   │   └── processador_genesys.py
│   └── 📁 salesforce/            # 💼 Processadores Salesforce
│       ├── __init__.py
│       ├── criado.py
│       ├── resolvido.py
│       ├── comentario_bko.py
│       └── processador_salesforce.py
└── 📁 docs/                       # 📚 Documentação
    └── README.md                 # 📖 Este arquivo
```

## 🚀 Como Usar

### Uso Básico (Recomendado)
```bash
# Coloque seus CSVs na pasta 'dados/'
# Execute o arquivo principal
python main.py
```

### Uso Avançado
```bash
# Processar apenas Genesys
python main.py --genesys

# Processar apenas Salesforce  
python main.py --salesforce

# Especificar pasta de dados diferente
python main.py --dados ./meus_csvs

# Modo verboso
python main.py --verbose

# Ajuda
python main.py --help
```

## 📁 Arquivos Suportados

### 🔵 Genesys (Detecção Automática)
- `Gestão da entrega N1 HC.csv`
- `Gestão da entrega N1 HC (1).csv` ✨ **Detecta duplicados**
- `Texto HC.csv`
- `Texto HC (1).csv` ✨ **Detecta duplicados**
- `Voz HC.csv`
- `Voz HC (1).csv` ✨ **Detecta duplicados**

### 🟠 Salesforce (Detecção Automática)
- `BASE-BOLETIM-CRIADO-2025-09-2.csv`
- `BASE-BOLETIM-CRIADO (1).csv` ✨ **Detecta duplicados**
- `BASE-BOLETIM-RESOLVIDO-2025-09-2.csv`
- `BASE-BOLETIM-RESOLVIDO (1).csv` ✨ **Detecta duplicados**
- `Cópia de BASE-BOLETIM-COMENTARI.csv`
- `BASE-BOLETIM-COMENTARI (1).csv` ✨ **Detecta duplicados**

## ✨ Funcionalidades Inteligentes

### 🔍 Detecção Automática de Arquivos
- **Busca flexível:** Encontra arquivos mesmo com variações no nome
- **Duplicados:** Detecta e usa automaticamente arquivos com `(1)`, `(2)`, etc.
- **Mais recente:** Sempre usa o arquivo modificado mais recentemente
- **Tolerante:** Funciona com diferentes formatos de nome

### 🎯 Sistema Organizado
- **Responsabilidade única:** Cada arquivo tem uma função específica
- **Imports limpos:** Estrutura de pacotes Python adequada
- **Manutenção fácil:** Código organizado por domínio (Genesys/Salesforce)
- **Extensível:** Fácil adicionar novos processadores

### 📊 Relatórios Claros
- **Feedback em tempo real:** Mostra qual arquivo está sendo processado
- **Relatório final:** Resume sucessos e falhas
- **Status detalhado:** Identifica exatamente quais bases foram processadas

## ⚙️ Configuração Inicial

### 1. Credenciais Google Sheets
Coloque o arquivo `boletim.json` em:
- `config/boletim.json` (recomendado)
- Ou na raiz do projeto

### 2. Dependências
```bash
pip install pandas gspread google-auth openpyxl
```

### 3. Estrutura de Pastas
```bash
# Criar pasta de dados (se não existir)
mkdir dados

# Colocar seus CSVs na pasta dados/
```

## 🔧 Arquitetura Técnica

### Core (`core/`)
- **`google_sheets_base.py`**: Classe base com funcionalidades comuns
  - Autenticação Google Sheets
  - Detecção inteligente de arquivos
  - Upload para planilhas
  - Tratamento de erros

### Processadores (`processadores/`)
- **Genesys**: Especializado em arquivos do sistema Genesys
- **Salesforce**: Especializado em relatórios do Salesforce
- **Modular**: Cada processador é independente

### Entrada Principal (`main.py`)
- **CLI amigável**: Argumentos de linha de comando
- **Orquestração**: Coordena todos os processadores
- **Relatórios**: Feedback completo do processamento

## 🚨 Solução de Problemas

### Arquivo não encontrado
```
❌ Arquivo não encontrado para padrão: arquivo.csv
```
**Solução:** Verifique se o arquivo está na pasta `dados/`

### Erro de credenciais
```
❌ Arquivo de credenciais 'boletim.json' não encontrado
```
**Solução:** Coloque `boletim.json` na pasta `config/`

### Erro de importação
```
❌ Erro ao importar processador
```
**Solução:** Execute a partir da pasta `automacao_boletins/`

## 🎯 Vantagens da Nova Estrutura

✅ **Organização clara:** Cada pasta tem responsabilidade específica
✅ **Manutenção fácil:** Código modular e bem estruturado  
✅ **Escalável:** Fácil adicionar novos processadores
✅ **Robusto:** Tratamento de erros em todos os níveis
✅ **Inteligente:** Detecção automática de arquivos duplicados
✅ **Profissional:** Estrutura padrão da indústria
✅ **Documentado:** Documentação completa e clara

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Execute `python main.py --help`
3. Confira os logs de erro no terminal