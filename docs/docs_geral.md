# 📋 Documentação Completa - Sistema RPA Leroy Merlin

> **Sistema Profissional de Automação RPA** com dois subsistemas independentes:
> - 🟢 **Pulso Boletim**: Processamento de Genesys, Salesforce e Produtividade
> - 🟡 **Power BI Looker Studio**: Alimentação de dashboards com dados de Filas Genesys

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-production-success.svg)](https://github.com/Ryanditko/rpa-leroy-merlin)
[![Version](https://img.shields.io/badge/version-3.1.0-green.svg)](https://github.com/Ryanditko/rpa-leroy-merlin)

---

## 📑 Índice

- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Funcionalidades](#-funcionalidades)
- [Como Usar](#-como-usar)
- [Sistemas Suportados](#-sistemas-suportados)
  - [🟢 Pulso Boletim](#-pulso-boletim)
  - [🟡 Power BI Looker Studio](#-power-bi-looker-studio)
- [Arquitetura Técnica](#-arquitetura-técnica)
- [Configuração](#-configuração)
- [Interface Gráfica](#-interface-gráfica)
- [Troubleshooting](#-troubleshooting)
- [Novidades v3.1](#-novidades-v31)

---

## 🏗️ Estrutura do Projeto

```
Automacao-LM/
├── 📁 config/                     # ⚙️ Configurações
│   ├── boletim.json              # 🔑 Credenciais Google Service Account
│   ├── kpis_historico.json       # � Histórico de KPIs (auto-gerado)
│   └── config.md                 # � Documentação de configuração
│
├── 📁 data/                       # 📂 Arquivos CSV para processamento
│   ├── BASE_GENESYS_VOZ_HC.csv
│   ├── BASE_SALESFORCE_CRIADO.csv
│   └── data.md                   # 📖 Documentação de dados
│
├── 📁 docs/                       # 📚 Documentação do projeto
│   ├── documentação.md           # 📋 Esta documentação
│   ├── Implementações.md         # 🔧 Histórico de implementações
│   ├── Renomear.md               # 🔄 Guia de renomeação
│   └── *.md                      # Outras documentações
│
├── 📁 img/                        # �️ Imagens e logos
│
├── 📁 scripts/                    # 🛠️ Scripts auxiliares
│   ├── executar_renomeacao.py    # 🔄 Renomeador de CSVs
│   ├── listar_abas_genesys.py    # 📋 Listar abas Genesys
│   └── processar-todos-csvs.py   # 🚀 Processar múltiplos CSVs
│
├── 📁 src/                        # 💻 Código fonte principal
│   ├── main.py                   # 🎯 Ponto de entrada CLI
│   ├── 📁 core/                  # 🧠 Motor principal
│   │   ├── __init__.py
│   │   └── google_sheets_base.py # 🔧 Classe base Google Sheets
│   └── 📁 processadores/         # ⚙️ Processadores especializados
│       ├── 📁 genesys/           # 📊 Genesys (VOZ, TEXTO, Gestão) - Pulso Boletim
│       ├── 📁 salesforce/        # 💼 Salesforce (CRIADO, RESOLVIDO, BKO) - Pulso Boletim
│       ├── 📁 produtividade/     # 📈 Produtividade e Tempo - Pulso Boletim
│       └── 📁 powerbi/           # 🟡 Power BI Looker Studio
│           └── 📁 genesys/       # 🎯 Filas Genesys (Primeiro e Segundo Semestre)
│
├── 📁 tests/                      # 🧪 Testes automatizados
│   ├── teste_sistema_completo.py
│   ├── teste-genesys.py
│   ├── teste-salesforce.py
│   └── tests.md                  # � Documentação de testes
│
├── 📁 utils/                      # 🛠️ Utilitários
│   ├── executar.bat              # ⚡ Executor Windows (CMD)
│   ├── executar.ps1              # ⚡ Executor PowerShell
│   ├── interface.bat             # 🎨 Abrir interface (CMD)
│   ├── interface.ps1             # 🎨 Abrir interface (PowerShell)
│   └── utils.md                  # 📖 Documentação de utilitários
│
├── .editorconfig                  # 📝 Configuração do editor
├── .gitattributes                 # 🔧 Atributos Git
├── .gitignore                     # 🚫 Arquivos ignorados
├── boletim.json                   # 🔑 Credenciais (cópia da config/)
├── interface_visual.py            # 🎨 Interface Gráfica - Pulso Boletim (Verde)
├── interface_powerbi.py           # 🟡 Interface Gráfica - Power BI (Amarelo)
├── main.py                        # 🚀 Script Principal CLI
├── renomeador_inteligente.py     # 🔄 Renomeador inteligente
├── README.md                      # 📖 Documentação principal
├── requirements.txt               # 📦 Dependências Python
└── setup.py                       # ⚙️ Setup de instalação
```

---

## ✨ Funcionalidades

### 🎯 Funcionalidades Principais

#### **🟢 Pulso Boletim - Processamento Automatizado**
- ✅ **Genesys**: VOZ HC, TEXTO HC, Gestão da Entrega
- ✅ **Salesforce**: Criado, Resolvido, Comentários BKO
- ✅ **Produtividade**: Base Produtividade, Base Tempo
- 🎨 **Cor**: Verde (#00A859)
- 🖥️ **Interface**: `interface_visual.py`

#### **🟡 Power BI Looker Studio - Alimentação de Dashboards**
- ✅ **Filas Genesys**: Primeiro Semestre (Q1/Q2) e Segundo Semestre (Q3/Q4)
- 🎨 **Cor**: Amarelo (#FFD700) com cabeçalho #FFA800
- 🖥️ **Interface**: `interface_powerbi.py`
- 📊 **Destino**: Dashboards Looker Studio para análise BI

#### **Interface Dual**
- 🎨 **Interface Gráfica** (GUI): Dashboard profissional com KPIs dinâmicos
- ⌨️ **Linha de Comando** (CLI): Execução via terminal com argumentos

#### **Detecção Inteligente**
- 🔍 **Auto-detecção de encoding**: UTF-8, Latin-1, CP1252, etc.
- 🔢 **Limpeza automática**: Removes apóstrofos, aspas, .0 desnecessário
- 📅 **Formatação de datas**: Detecta e limpa colunas de data automaticamente
- 🎨 **Coloração verde Leroy Merlin**: Primeira linha destacada, demais em verde claro

#### **Sistema Robusto**
- 🔄 **Modo complementar**: Preserva dados existentes, não sobrescreve
- 📊 **Fórmulas automáticas**: Aplica fórmulas apenas em linhas novas
- 🔁 **Renomeação inteligente**: Padroniza nomes de arquivos CSV
- 📝 **Relatórios detalhados**: Logs completos de cada processamento
- 💾 **KPIs persistentes**: Histórico de execuções salvo em JSON

---

## 🚀 Como Usar

### **Método 1: Interface Gráfica (Recomendado)** 🎨

#### Via Atalho (.bat)
```bash
# Duplo clique em:
utils/interface.bat
# ou
utils/interface.ps1
```

#### Via Python
```bash
python interface_visual.py
```

**Recursos da Interface:**
- 🎨 Dashboard profissional com cores Leroy Merlin
- 📊 4 KPIs dinâmicos (Total Processado, Taxa Sucesso, Tempo Médio, Última Execução)
- 🔘 Botões para execução seletiva (Salesforce, Genesys, Produtividade)
- 📝 Log em tempo real da execução
- 🔗 Links diretos para as planilhas Google Sheets
- 🔄 Renomeação de arquivos integrada

---

### **Método 2: Linha de Comando (Avançado)** ⌨️

#### Via Atalho (.bat)
```bash
# Duplo clique em:
utils/executar.bat
# ou
utils/executar.ps1
```

#### Via Python Direto
```bash
# Processar TODOS os sistemas
python main.py --all

# Processar apenas Salesforce
python main.py --salesforce

# Processar apenas Genesys
python main.py --genesys

# Processar apenas Produtividade
python main.py --produtividade

# Combinar múltiplos sistemas
python main.py --salesforce --genesys

# Modo verboso (mais detalhes)
python main.py --all --verbose

# Ajuda
python main.py --help
```

---

### **Método 3: Renomeação de Arquivos** 🔄

```bash
# Renomear CSVs para padrão correto
python renomeador_inteligente.py

# Via script auxiliar
python scripts/executar_renomeacao.py
```

**Padrão de Nomenclatura:**
- `BASE_GENESYS_VOZ_HC.csv`
- `BASE_GENESYS_TEXTO_HC.csv`
- `BASE_GENESYS_GESTAO_HC.csv`
- `BASE_SALESFORCE_CRIADO.csv`
- `BASE_SALESFORCE_RESOLVIDO.csv`
- `BASE_SALESFORCE_COMENTARIO_BKO.csv`
- `BASE_PRODUTIVIDADE.csv`
- `BASE_TEMPO.csv`

---

## 📊 Sistemas Suportados

### **1. Genesys** 📞

#### **Bases Processadas:**
| Base | Arquivo CSV | Planilha Destino | Aba |
|------|-------------|------------------|-----|
| **VOZ HC** | `BASE_GENESYS_VOZ_HC.csv` | Genesys | `BASE VOZ HC` |
| **TEXTO HC** | `BASE_GENESYS_TEXTO_HC.csv` | Genesys | `BASE TEXTO HC` |
| **Gestão** | `BASE_GENESYS_GESTAO_HC.csv` | Genesys | `BASE GE COLABORADOR` |

#### **ID da Planilha:**
```
1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE
```

#### **Fórmula Aplicada:**
- Coluna P: `=TEXT(C{row};"DD/M")` (formata data)

---

### **2. Salesforce** 💼

#### **Bases Processadas:**
| Base | Arquivo CSV | Planilha Destino | Aba |
|------|-------------|------------------|-----|
| **CRIADO** | `BASE_SALESFORCE_CRIADO.csv` | Salesforce | `BASE ATUALIZADA CORRETA - CRIADO` |
| **RESOLVIDO** | `BASE_SALESFORCE_RESOLVIDO.csv` | Salesforce | `BASE ATUALIZADA CORRETA - RESOLVIDA` |
| **BKO** | `BASE_SALESFORCE_COMENTARIO_BKO.csv` | Salesforce | `BASE ATUALIZADA CORRETA - COMENTARIO BKO` |

#### **ID da Planilha:**
```
1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk
```

#### **Fórmulas Aplicadas (RESOLVIDA):**
- Coluna U: `=B{row}` (ANALISE_ABERTURA)
- Coluna V: `=C{row}` (ANALISE_FECHAMENTO)
- Coluna W: `=SE(V{row}=""; ""; V{row}-U{row})` (TMR)
- Coluna X: `=SEERRO(ÍNDICE($Z$2:$Z$3;CORRESP(VERDADEIRO;W{row}<=$AA$2:$AA$3;0));"")` (Prazo)
- Coluna Y: `=SE(C{row}=""; ""; VALOR(C{row}))` (DATA FECHAMENTO)
- Coluna AB: `=TEXTO(Y{row};"dd/mm/yyyy")` (DATA FECHAMENTO teste)

#### **Fórmulas Aplicadas (COMENTÁRIO BKO):**
- Coluna R: Fórmula de análise de comentários

---

### **3. Produtividade** �

#### **Bases Processadas:**
| Base | Arquivo CSV | Planilha Destino | Aba |
|------|-------------|------------------|-----|
| **PRODUTIVIDADE** | `BASE_PRODUTIVIDADE.csv` | Genesys | `BASE PRODUTIVIDADE` |
| **TEMPO** | `BASE_TEMPO.csv` | Genesys | `BASE TEMPO` |

#### **ID da Planilha:**
```
1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE
```

---

## 🧠 Arquitetura Técnica

### **Camada Core** (`src/core/`)

#### **`google_sheets_base.py`**
Classe base com funcionalidades compartilhadas:

```python
class GoogleSheetsBase:
    def __init__(self, id_planilha, abas_config)
    def autenticar()                          # Autenticação Google Sheets
    def enviar_csv_para_planilha()           # Upload com formatação verde
    def limpar_numero_formato()              # Remove .0, aspas, vírgulas
    def limpar_data_formato()                # Limpeza agressiva de datas
    def aplicar_formulas_linhas_novas()      # Aplica fórmulas em novas linhas
    def _letra_para_indice()                 # Converte letra coluna → índice
```

**Recursos:**
- ✅ Detecção automática de encoding (5 tentativas)
- ✅ Expansão automática de planilha se necessário
- ✅ Coloração verde Leroy Merlin automática
- ✅ Retorno de linha_inicial e linha_final para fórmulas
- ✅ Modo `value_input_option='USER_ENTERED'` (evita apóstrofos em datas)

---

### **Camada Processadores** (`src/processadores/`)

#### **Genesys** (`processadores/genesys/`)
```python
class ProcessadorGenesys(GoogleSheetsBase):
    def processar_voz_hc()           # VOZ HC
    def processar_texto_hc()         # TEXTO HC
    def processar_gestao_entrega()   # Gestão da Entrega
```

#### **Salesforce** (`processadores/salesforce/`)
```python
class ProcessadorSalesforceCriado(GoogleSheetsBase):
    def processar()                  # BASE CRIADO

class ProcessadorSalesforceResolvido(GoogleSheetsBase):
    FORMULAS_CONFIG = {...}          # 6 fórmulas
    def processar()                  # BASE RESOLVIDA + Fórmulas

class ProcessadorSalesforceComentarioBKO(GoogleSheetsBase):
    FORMULAS_CONFIG = {...}          # 1 fórmula
    def processar()                  # BASE COMENTÁRIO BKO
```

#### **Produtividade** (`processadores/produtividade/`)
```python
class ProcessadorProdutividade(GoogleSheetsBase):
    def processar_produtividade()    # BASE PRODUTIVIDADE
    def processar_tempo()            # BASE TEMPO
```

---

### **Camada Interface** 

#### **CLI** (`main.py` / `src/main.py`)
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--salesforce')
    parser.add_argument('--genesys')
    parser.add_argument('--produtividade')
    # ... processa argumentos e executa
```

#### **GUI** (`interface_visual.py`)
```python
class AutomacaoLeroyMerlinGUI:
    def criar_interface()            # Cria janela 1400x800
    def criar_kpis_dashboard()       # 4 KPIs dinâmicos
    def executar_automacao()         # Thread para execução
    def registrar_execucao()         # Atualiza KPIs após execução
    def carregar_kpis()              # Carrega de JSON
    def salvar_kpis()                # Salva em JSON
```

---

## ⚙️ Configuração

### **1. Credenciais Google Sheets** 🔑

#### **Obter Credenciais:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie projeto ou use existente
3. Ative **Google Sheets API**
4. Crie **Service Account**
5. Gere chave JSON
6. Baixe como `boletim.json`

#### **Configurar:**
```bash
# Copiar para config/
cp ~/Downloads/boletim.json config/

# Copiar para raiz (o sistema usa daqui)
cp ~/Downloads/boletim.json ./
```

#### **Compartilhar Planilhas:**
1. Abrir planilha no Google Sheets
2. Clicar em "Compartilhar"
3. Adicionar email da Service Account:
   ```
   boletim-315@sublime-shift-472919-f0.iam.gserviceaccount.com
   ```
4. Definir permissão como **Editor**
5. Desmarcar "Notificar pessoas"

---

### **2. Dependências Python** 📦

```bash
# Instalar via requirements.txt
pip install -r requirements.txt

# Ou manualmente
pip install gspread pandas python-dateutil oauth2client
```

**Dependências Principais:**
- `gspread` - Google Sheets API
- `pandas` - Manipulação de dados
- `python-dateutil` - Parsing de datas
- `oauth2client` - Autenticação Google

---

### **3. Estrutura de Pastas** 📁

```bash
# Criar pasta data/ se não existir
mkdir data

# Colocar CSVs na pasta
mv ~/Downloads/*.csv data/

# Renomear para padrão correto
python renomeador_inteligente.py
```

---

## 🎨 Interface Gráfica

### **Dashboard Profissional**

#### **Cores Leroy Merlin:**
- 🟢 **Verde Principal**: `#00A859`
- 🟢 **Verde Escuro**: `#00864A`
- ⚫ **Preto Suave**: `#1A1A1A`
- ⚫ **Cinza Escuro**: `#2A2A2A`
- ⚪ **Branco**: `#FFFFFF`
- ⚪ **Cinza Claro**: `#F5F5F5`

#### **4 KPIs Dinâmicos:**
1. **Total Processado** - Total de execuções do sistema
2. **Taxa de Sucesso** - Porcentagem de sucessos (%)
3. **Tempo Médio** - Tempo médio de execução (segundos)
4. **Última Execução** - Timestamp da última execução

#### **Recursos:**
- ✅ Atualização automática após cada execução
- ✅ Persistência em `config/kpis_historico.json`
- ✅ Log em tempo real com scroll automático
- ✅ Botões de execução seletiva
- ✅ Links diretos para planilhas
- ✅ Tema escuro profissional

---

## � Troubleshooting

### **Problema 1: Credenciais não encontradas**
```
❌ Arquivo de credenciais 'boletim.json' não encontrado
```

**Soluções:**
```bash
# 1. Verificar se arquivo existe
ls config/boletim.json
ls boletim.json

# 2. Copiar de config/ para raiz
cp config/boletim.json ./

# 3. Baixar novamente do Google Cloud
```

---

### **Problema 2: Arquivo CSV não encontrado**
```
❌ Arquivo não encontrado: BASE_SALESFORCE_CRIADO.csv
```

**Soluções:**
```bash
# 1. Verificar arquivos na pasta data/
ls data/*.csv

# 2. Renomear arquivos para padrão correto
python renomeador_inteligente.py

# 3. Mover CSVs para pasta data/
mv ~/Downloads/*.csv data/
```

---

### **Problema 3: Datas com apóstrofo `'20/10/2025`**
```
Datas aparecem como: '20/10/2025
```

**Solução:**
✅ **JÁ CORRIGIDO NA v2.4!**
- Sistema usa `value_input_option='USER_ENTERED'`
- Método `limpar_data_formato()` remove apóstrofos
- Detecção automática de colunas de data

---

### **Problema 4: Erro de encoding**
```
❌ 'utf-8' codec can't decode byte 0xfa
```

**Solução:**
✅ **Sistema tenta automaticamente:**
1. UTF-8-SIG
2. UTF-8
3. Latin-1
4. CP1252
5. ISO-8859-1

Se falhar, abrir CSV no Excel e salvar como UTF-8.

---

### **Problema 5: Fórmulas não aplicadas**
```
Fórmulas não aparecem nas células
```

**Soluções:**
1. ✅ Verificar se `resultado['linha_inicial']` e `['linha_final']` existem
2. ✅ Confirmar que base tem `FORMULAS_CONFIG`
3. ✅ Ver logs: deve exibir "🧮 Aplicando X fórmulas..."
4. ✅ Testar com `tests/teste_formulas_salesforce.py`

---

### **Problema 6: Erro ao importar módulo**
```
ModuleNotFoundError: No module named 'gspread'
```

**Solução:**
```bash
# Reinstalar dependências
pip install -r requirements.txt

# Ou instalar manualmente
pip install gspread pandas python-dateutil oauth2client
```

---

### **Problema 7: Permissão negada na planilha**
```
❌ Permission denied: You don't have permission to access this resource
```

**Solução:**
1. Abrir planilha no navegador
2. Clicar em "Compartilhar"
3. Adicionar email da Service Account (boletim-315@...)
4. Definir como **Editor**
5. Salvar

---

### **Problema 8: Interface não abre**
```
Duplo clique em interface.bat não faz nada
```

**Soluções:**
```bash
# 1. Verificar Python instalado
python --version

# 2. Executar direto
python interface_visual.py

# 3. Ver erros no terminal
python interface_visual.py 2>&1 | more
```

---

### **Problema 9: KPIs não atualizam**
```
Dashboard mostra sempre os mesmos valores
```

**Soluções:**
```bash
# 1. Verificar arquivo existe
ls config/kpis_historico.json

# 2. Resetar KPIs
rm config/kpis_historico.json

# 3. Executar automação novamente
python main.py --salesforce
```

---

### **Problema 10: Coloração verde não aplica**
```
Linhas não ficam verdes na planilha
```

**Causa:**
- Formatação condicional da planilha pode sobrescrever
- Permissões insuficientes

**Solução:**
- Verificar permissões (deve ser Editor, não Leitor)
- Remover formatação condicional conflitante da planilha

---

## 🚀 Novidades da Versão 3.0 - Sistema de Configuração Centralizada

### 🎯 Problema Resolvido
Antes era necessário **alterar código manualmente** a cada mês para atualizar IDs das planilhas. Agora o sistema é **totalmente centralizado** e **sustentável**.

### ✨ Recursos Adicionados
- ✅ **Gerenciador de planilhas** com interface gráfica moderna
- ✅ **Backup automático** antes de qualquer alteração
- ✅ **Validação automática** de IDs das planilhas
- ✅ **Templates mensais** para atualizações recorrentes
- ✅ **Histórico completo** de todas as mudanças
- ✅ **Atualização em lote** de múltiplas planilhas
- ✅ **Compatibilidade retroativa** mantida

### 🎨 Como Usar o Novo Sistema

#### Interface Visual (Recomendado)
```bash
python scripts/interface_gerenciador.py
```

#### Linha de Comando
```bash
# Ver status atual
python scripts/gerenciador_planilhas.py --status

# Atualizar planilha específica  
python scripts/gerenciador_planilhas.py --atualizar genesys_boletim --id novo_id_aqui

# Preparar atualização mensal
python scripts/atualizar_planilhas.py --preparar --mes dezembro --ano 2025
```

### 📋 Configuração Centralizada
**Arquivo**: `config/planilhas_config.json`

```json
{
  "planilhas": {
    "genesys_boletim": {
      "nome": "📊 GENESYS BOLETIM",
      "id": "1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE",
      "tipo": "boletim",
      "abas": {
        "voz_hc": "BASE VOZ",
        "texto_hc": "BASE TEXTO"
      }
    }
  }
}
```

### 💡 Benefícios
| Antes | Depois |
|-------|--------|
| ❌ 30 minutos para atualizar | ✅ 2 minutos para atualizar |
| ❌ Editar código manualmente | ✅ Interface visual amigável |
| ❌ Risco de quebrar sistema | ✅ Validação automática |
| ❌ Sem backup | ✅ Backup automático |
| ❌ Sem rastreabilidade | ✅ Histórico completo |

**📚 Guia completo**: [`docs/guia_configuracao_centralizada.md`](guia_configuracao_centralizada.md)

---
