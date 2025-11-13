# Automação Leroy Merlin - RPA

<div align="center">

<img src="img/leroy.png" alt="Leroy Merlin Logo" width="200">

**Sistema RPA para Processamento Automatizado de Dados**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Internal-red.svg)]()
[![Status](https://img.shields.io/badge/status-production-success.svg)]()
[![Version](https://img.shields.io/badge/version-3.2.0-green.svg)]()
[![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)]()

Sistema automatizado para processamento e envio de dados para Google Sheets  
**(Pulso Boletim e Power BI Looker Studio)**

[Características](#-recursos) •
[Instalação](#-instalação) •
[Uso](#-uso) •
[Power BI](#-power-bi-looker-studio) •
[Documentação](#-documentação) •
[Suporte](#-suporte)

</div>

---

## 📋 Índice

- [Recursos](#-recursos)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Power BI Looker Studio](#-power-bi-looker-studio)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Segurança](#-segurança)
- [Suporte](#-suporte)

---

## ✨ Recursos

### 🟢 Processamento Pulso Boletim (Verde)
- ✅ **Genesys**: VOZ HC, TEXTO HC, Gestão da Entrega
- ✅ **Salesforce**: Criado, Resolvido, Comentários BKO
- ✅ **Produtividade**: Base Produtividade, Base Tempo
- 🎨 **Cor**: Verde Leroy Merlin (#00A859)

### 🟡 Processamento Power BI Looker Studio (Amarelo/Laranja/Roxo)
- ✅ **Filas Genesys - PRIMEIRO SEMESTRE**: Base unificada Q1/Q2 (Amarelo #FFD700)
- ✅ **Filas Genesys - SEGUNDO SEMESTRE**: Base unificada Q3/Q4 (Amarelo #FFD700)
- ✅ **Autoserviço - PRIMEIRO SEMESTRE**: Dados URA + LIA Q1/Q2 (Laranja #FF6B35)
- ✅ **Autoserviço - SEGUNDO SEMESTRE**: Dados URA + LIA Q3/Q4 (Laranja #FF6B35)
- ✅ **Hibernação - PRIMEIRO SEMESTRE**: Base Hibernação Q1/Q2 (Roxo #9C27B0)
- ✅ **Hibernação - SEGUNDO SEMESTRE**: Base Hibernação Q3/Q4 (Roxo #9C27B0)
- 🎨 **Cores**: Amarelo (Filas), Laranja (Autoserviço), Roxo (Hibernação)
- 📊 **Looker Studio**: Alimentação direta de dashboards BI
- 🔒 **Thread-Safe**: Interface não trava durante processamento

### Funcionalidades Avançadas
- 🔄 Detecção automática de encoding (UTF-8, Latin-1, CP1252, etc.)
- 🔢 Limpeza inteligente de números (remove apóstrofos, aspas, .0 desnecessário)
- 🎨 Coloração automática diferenciada por projeto
- 📊 Complementa dados existentes (não sobrescreve)
- 🔁 Renomeação inteligente de arquivos
- 🖥️ **Duas interfaces gráficas**: `interface_pulso_boletim.py` e `interface_powerbi.py`
- 📝 Relatórios detalhados de processamento
- 💾 Histórico de KPIs e métricas

---

## 📦 Requisitos

### Sistema
- Windows 10/11
- Python 3.12 ou superior
- PowerShell 5.1 ou superior
- Conexão com internet

### Python Packages
```
pandas>=2.0.0
gspread>=5.0.0
google-auth>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

## 🔧 Instalação

### 1. Clone o Repositório
```powershell
git clone https://github.com/Eficiencia-Operacional/Scripts-Eficiencia-Operacional.git
cd Scripts-Eficiencia-Operacional
```

### 2. Instale as Dependências
```powershell
pip install -r requirements.txt
```

Ou instale manualmente:
```powershell
pip install pandas gspread google-auth
```

---

## ⚙️ Configuração

### 1. Credenciais do Google (OBRIGATÓRIO)

#### Opção A: Usar Credenciais Existentes
Se você já tem o arquivo `boletim.json`:
1. Coloque-o na raiz do projeto
2. Prossiga para o passo 2

#### Opção B: Criar Novas Credenciais

1. **Acesse o Google Cloud Console**
   - https://console.cloud.google.com

2. **Crie um Projeto** (se não tiver)
   - Clique em "Select a project" → "New Project"
   - Nome: "Automacao Leroy Merlin"

3. **Habilite as APIs**
   - APIs & Services → Enable APIs and Services
   - Busque e habilite:
     - Google Sheets API
     - Google Drive API

4. **Crie Service Account**
   - IAM & Admin → Service Accounts
   - "Create Service Account"
   - Nome: `boletim` (ou outro nome)
   - Role: `Editor`
   - Create Key → JSON
   - Salve como `boletim.json` na raiz do projeto

5. **Configure Permissões nas Planilhas**
   - Copie o email da service account (ex: `boletim-315@projeto.iam.gserviceaccount.com`)
   - Abra cada planilha do Google Sheets
   - Compartilhar → Cole o email
   - Permissão: **Editor**

### 2. Estrutura de Pastas

Certifique-se de que existem as pastas necessárias:
```powershell
mkdir data -Force
mkdir data/hibernação -Force
mkdir json -Force
```

### 3. Verificação

Teste se tudo está configurado:
```powershell
python tests/test_sistema.py
```

Você deve ver:
```
✅ TODOS OS TESTES PASSARAM COM SUCESSO!
```

Para validar especificamente os 6 processadores Power BI:
```powershell
python tests/teste_todos_processadores.py
```

---

## 🎯 Uso

### Opção 1: Interface Gráfica - Pulso Boletim 🟢 (Recomendado)

```powershell
python interface_pulso_boletim.py
```

Ou use os atalhos:
```powershell
.\utils\interface.bat
# ou
.\utils\interface.ps1
```

**Na interface:**
1. Marque as caixas dos sistemas desejados (Genesys, Salesforce, Produtividade)
2. Clique em "EXECUTAR AUTOMAÇÃO"
3. Acompanhe o progresso em tempo real
4. Veja KPIs atualizados (Total Processado, Taxa de Sucesso, Tempo Médio)

### Opção 2: Interface Gráfica - Power BI Looker Studio 🟡🟠🟣

```powershell
python -m interfaces.interface_powerbi
```

Ou use os atalhos:
```powershell
.\utils\powerbi.bat
# ou
.\utils\powerbi.ps1
```

**Na interface:**
1. **Gestão de Arquivos:**
   - 🔄 Renomear arquivos automaticamente
   - 🔍 Verificar arquivos disponíveis
   - 📂 Abrir pasta de dados

2. **Acesso Rápido às Planilhas:**
   - 📊 Filas Genesys (1º e 2º Semestres) - Amarelo
   - 🤖 Autoserviço (1º e 2º Semestres) - Laranja
   - 💤 Hibernação (1º e 2º Semestres) - Roxo

3. **Opções de Processamento:**
   - ☑️ Processar PRIMEIRO SEMESTRE (Filas Genesys)
   - ☑️ Processar SEGUNDO SEMESTRE (Filas Genesys)
   - ☑️ Processar AUTOSERVIÇO - PRIMEIRO SEMESTRE
   - ☑️ Processar AUTOSERVIÇO - SEGUNDO SEMESTRE
   - ☑️ Processar HIBERNAÇÃO - PRIMEIRO SEMESTRE
   - ☑️ Processar HIBERNAÇÃO - SEGUNDO SEMESTRE
   - ☑️ Modo detalhado (logs completos)

4. **Botões de Processamento Individual:**
   - 📊 PROCESSAR FILAS GENESYS 1º SEM
   - 📊 PROCESSAR FILAS GENESYS 2º SEM
   - 🤖 PROCESSAR AUTOSERVIÇO 1º SEM
   - 🤖 PROCESSAR AUTOSERVIÇO 2º SEM
   - 💤 PROCESSAR HIBERNAÇÃO 1º SEM
   - 💤 PROCESSAR HIBERNAÇÃO 2º SEM

5. **Execução Completa:**
   - 🚀 EXECUTAR AUTOMAÇÃO COMPLETA (processa tudo marcado)

6. **Acompanhe em tempo real:**
   - KPIs dinâmicos (Total, Taxa de Sucesso, Tempo Médio)
   - Logs coloridos por tipo de operação
   - Barra de progresso
1. Marque PRIMEIRO e/ou SEGUNDO semestre
2. Clique em "PROCESSAR PRIMEIRO SEMESTRE" ou "PROCESSAR SEGUNDO SEMESTRE"
3. Ou use "Renomear Arquivos" para padronizar nomes
4. Acesso rápido às planilhas pelo botão "Abrir Planilha"

**Arquivo necessário:**
- `data/Filas Genesys - Todas as Filas .csv`

**Na interface Power BI:**
1. Selecione o arquivo CSV das Filas do Genesys
2. Escolha entre Primeiro ou Segundo Semestre
3. Clique em "PROCESSAR"
4. Os dados serão enviados com cor AMARELA

### Opção 2: Linha de Comando

```powershell
# Processar tudo
python main.py

# Processar apenas Genesys
python main.py --genesys

# Processar apenas Salesforce
python main.py --salesforce

# Processar apenas Produtividade
python main.py --produtividade

# Ver ajuda
python main.py --help
```

### Opção 3: Executáveis Batch

```powershell
# Executar tudo
.\executar.bat

# Ou via PowerShell
.\executar.ps1
```

---

## 📁 Estrutura do Projeto

```
Scripts-Eficiencia-Operacional/
│
├── � interfaces/
│   ├── interface_pulso_boletim.py  # Interface gráfica Pulso Boletim (Verde)
│   └── interface_powerbi.py        # Interface gráfica Power BI (Amarelo/Laranja/Roxo)
│
├── 📂 src/
│   ├── core/
│   │   └── google_sheets_base.py   # Classe base com limpeza de números
│   └── processadores/
│       ├── genesys/
│       │   └── processador_genesys.py
│       ├── salesforce/
│       │   ├── criado.py
│       │   ├── resolvido.py
│       │   └── comentario_bko.py
│       ├── produtividade/
│       │   └── produtividade.py
│       └── powerbi/
│           ├── filas/
│           │   ├── filas_primeiro_semestre.py    # ✅ Amarelo
│           │   └── filas_segundo_semestre.py     # ✅ Amarelo
│           ├── autoservico/
│           │   ├── autoservico_primeiro_semestre.py  # ✅ Laranja
│           │   └── autoservico_segundo_semestre.py   # ✅ Laranja
│           └── hibernação/
│               ├── hibernacao_primeiro_semestre.py   # ✅ Roxo
│               └── hibernacao_segundo_semestre.py    # ✅ Roxo
│
├── 📂 json/
│   ├── planilhas_config.json       # Configuração centralizada de planilhas
│   ├── kpis_historico.json        # Histórico de KPIs
│   └── historico_renomeacao.json  # Histórico de renomeações
│
├── � docs/
│   ├── interface_powerbi_completa.md      # Documentação completa (v3.2.0)
│   ├── adicao_botoes_hibernacao.md        # Implementação Hibernação
│   ├── correcao_thread_safety.md          # Correção crítica de threading
│   ├── relatorio_status_automacoes.md     # Status de todos processadores
│   └── gerenciador_planilhas.md           # Uso do gerenciador
│
├── � tests/
│   ├── teste_todos_processadores.py       # ✅ Validação completa (6/6)
│   ├── teste_botao_processar_tudo.py      # ✅ Teste integração
│   ├── teste_botoes_hibernacao.py         # ✅ Teste Hibernação
│   └── teste_checkboxes_hibernacao.py     # ✅ Teste visual
│
├── 📂 data/                        # Arquivos CSV (gitignored)
│   └── hibernação/                 # CSVs específicos de Hibernação
│
├── 📂 utils/
│   ├── interface.bat/.ps1          # Atalhos Pulso Boletim
│   └── powerbi.bat/.ps1            # Atalhos Power BI
│
├── 📄 main.py                      # Script principal Pulso Boletim
├── 🔄 renomeador_inteligente.py    # Renomeação automática de CSVs
├── 📋 requirements.txt             # Dependências Python
├── 🔒 boletim.json.example         # Exemplo de credenciais
├── 🚫 .gitignore                   # Proteção de credenciais
└── 📖 README.md                    # Este arquivo
```
│       ├── genesys/
│       │   └── processador_genesys.py
│       ├── salesforce/
│       │   ├── criado.py
│       │   ├── resolvido.py
│       │   └── comentario_bko.py
│       ├── produtividade/
│       │   └── produtividade.py
│       └── powerbi/
│           └── genesys/
│               ├── filas_primeiro_semestre.py
│               └── filas_segundo_semestre.py
│
├── 📂 data/                        # Coloque seus CSVs aqui
│   └── *.csv
│
├── 📂 config/
│   └── boletim.json               # Credenciais (não versionado)
│
├── 📂 tests/                      # Scripts de teste
│   ├── teste_powerbi.py           # Teste Power BI
│   └── *.py
│
├── 📂 utils/                      # Scripts auxiliares
│   ├── powerbi.bat                # Atalho Power BI
│   └── powerbi.ps1                # Atalho Power BI PS
│
├── 📂 docs/                       # Documentação adicional
│
├── 📄 .gitignore                  # Arquivos ignorados pelo Git
├── 📄 .gitattributes              # Configuração de line endings
├── 📄 boletim.json.example        # Template de credenciais
├── 📄 requirements.txt            # Dependências Python
├── 📄 CORRECAO_APOSTROFOS.md      # Doc da correção de aspas
├── 📄 SEGURANCA_GIT.md            # Guia de segurança
└── 📄 README.md                   # Este arquivo
```

---

## 🎯 Power BI Looker Studio

### 📊 Automação Completa para Dashboards BI

A automação Power BI alimenta diretamente os dashboards do Looker Studio com dados de **Filas Genesys**, **Autoserviço** e **Hibernação**.

#### Características Especiais
- 🎨 **Cores Distintivas**: Amarelo (Filas), Laranja (Autoserviço), Roxo (Hibernação)
- 📊 **6 Planilhas**: 2 por categoria x 2 semestres
- 🔄 **Complementação Inteligente**: Adiciona dados sem sobrescrever existentes
- 📈 **Dashboard KPIs**: Total processado, Taxa de sucesso, Tempo médio, Última execução
- 💾 **Histórico**: Salva métricas em `json/kpis_historico.json`
- 🔒 **Thread-Safe**: Interface não trava durante processamento

#### Planilhas de Destino

**🟡 FILAS GENESYS:**

**PRIMEIRO SEMESTRE (Q1/Q2):**
- 🔗 [BASE FILAS GENESYS - PRIMEIRO SEMESTRE](https://docs.google.com/spreadsheets/d/1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc)
- Aba: `BASE`
- Processador: `ProcessadorFilasPrimeiroSemestre`
- Cor: Amarelo (#FFD700)

**SEGUNDO SEMESTRE (Q3/Q4):**
- 🔗 [BASE FILAS GENESYS - SEGUNDO SEMESTRE](https://docs.google.com/spreadsheets/d/1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8)
- Aba: `BASE`
- Processador: `ProcessadorFilasSegundoSemestre`
- Cor: Amarelo (#FFD700)

**🟠 AUTOSERVIÇO:**

**PRIMEIRO SEMESTRE (Q1/Q2):**
- 🔗 [AUTOSERVIÇO - PRIMEIRO SEMESTRE](https://docs.google.com/spreadsheets/d/1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw)
- Aba: `URA + LIA`
- Processador: `ProcessadorAutoservicoPrimeiroSemestre`
- Cor: Laranja (#FF6B35)

**SEGUNDO SEMESTRE (Q3/Q4):**
- 🔗 [AUTOSERVIÇO - SEGUNDO SEMESTRE](https://docs.google.com/spreadsheets/d/1Py1W4sSnIbsgMCrr0h0PSTL0DpN-eLj0NoYGbcHLmUI)
- Aba: `URA + LIA`
- Processador: `ProcessadorAutoservicoSegundoSemestre`
- Cor: Laranja (#FF6B35)

**🟣 HIBERNAÇÃO:**

**PRIMEIRO SEMESTRE (Q1/Q2):**
- 🔗 [HIBERNAÇÃO - PRIMEIRO SEMESTRE](https://docs.google.com/spreadsheets/d/1v2kpi1tIChOQezQgA8jjRTGeK2iS9vfcrWoSdhLoZKM)
- Aba: `BASE`
- Processador: `ProcessadorHibernacaoPrimeiroSemestre`
- Cor: Roxo (#9C27B0)
- Pasta: `data/hibernação/`

**SEGUNDO SEMESTRE (Q3/Q4):**
- 🔗 [HIBERNAÇÃO - SEGUNDO SEMESTRE](https://docs.google.com/spreadsheets/d/1G3Tf67VXk14n1IUIeaINQAjI7PFNhIpRqtVvlEkeBPY)
- Aba: `BASE`
- Processador: `ProcessadorHibernacaoSegundoSemestre`
- Cor: Roxo (#9C27B0)
- Pasta: `data/hibernação/`

#### Como Usar

**Método 1 - Interface Gráfica (Recomendado):**
```powershell
python -m interfaces.interface_powerbi
```

**Na interface você pode:**
- ✅ Processar cada semestre/categoria individualmente ou em lote
- ✅ Renomear arquivos automaticamente
- ✅ Abrir planilhas diretamente no navegador (botões de acesso rápido)
- ✅ Visualizar KPIs em tempo real
- ✅ Acompanhar logs detalhados com cores
- ✅ Marcar múltiplas opções e processar tudo de uma vez

**Método 2 - Executáveis Batch:**
```powershell
.\utils\powerbi.bat
# ou
.\utils\powerbi.ps1
```

#### Arquivos de Entrada

**Filas Genesys:**
- **Nome Padrão**: `Filas Genesys - Todas as Filas .csv`
- **Localização**: pasta `data/`

**Autoserviço:**
- **Nome Padrão**: Detectado automaticamente pelo renomeador
- **Localização**: pasta `data/`

**Hibernação:**
- **Nome Padrão**: Detectado automaticamente pelo renomeador
- **Localização**: pasta `data/hibernação/`

**Formato Comum:**
- Separador: Ponto e vírgula (;) detectado automaticamente
- Encoding: UTF-8 (detectado automaticamente)

**Renomeação Automática:**
O renomeador inteligente detecta e padroniza automaticamente:
- `Filas genesys.csv` → `Filas Genesys - Todas as Filas .csv`
- `Fila genesys.csv` → `Filas Genesys - Todas as Filas .csv`
- `filas genesys.csv` → `Filas Genesys - Todas as Filas .csv`

#### Estrutura dos Processadores

**Arquitetura Modular por Categoria:**

```
src/processadores/powerbi/
├── genesys/filas/                    # 🟡 Filas Genesys
│   ├── filas_primeiro_semestre.py
│   └── filas_segundo_semestre.py
├── autoservico/                       # 🟠 Autoserviço
│   ├── autoservico_primeiro_semestre.py
│   └── autoservico_segundo_semestre.py
└── hibernação/                        # 🟣 Hibernação
    ├── hibernacao_primeiro_semestre.py
    └── hibernacao_segundo_semestre.py
```

**Características Comuns dos 6 Processadores:**
- ✅ Herdam de `GoogleSheetsBase` para reutilização de código
- ✅ Limpeza automática de dados (inf, -inf, nan)
- ✅ Formatação com cores diferenciadas (Amarelo/Laranja/Roxo)
- ✅ Complementação inteligente (append_rows, não sobrescreve)
- ✅ Thread-safe (não bloqueiam interface durante processamento)
- ✅ Validação de dados antes de enviar

#### Diferenças Power BI vs Pulso Boletim

| Aspecto | Pulso Boletim 🟢 | Power BI 🟡🟠🟣 |
|---------|------------------|-----------------|
| **Cor de destaque** | Verde (#00A859) | Amarelo/Laranja/Roxo |
| **Planilhas** | Boletim Genesys/SF/Prod | 6 planilhas (3 categorias x 2 semestres) |
| **Sistemas** | 3 (Genesys, SF, Prod) | 3 (Filas, Autoserviço, Hibernação) |
| **Finalidade** | Relatórios internos | Dashboards Looker Studio |
| **Frequência** | Diária | Sob demanda |
| **Interface** | interface_pulso_boletim.py | interface_powerbi.py |
| **KPIs** | kpis_historico.json | kpis_historico.json |
| **Processamento** | Individual | Individual + Batch |

---

## 📚 Documentação

### Documentos Principais
- 📘 [`docs/interface_powerbi_completa.md`](docs/interface_powerbi_completa.md) - **Documentação completa v3.2.0** (6 processadores, cores, thread-safety)
- 📗 [`docs/adicao_botoes_hibernacao.md`](docs/adicao_botoes_hibernacao.md) - Implementação UI Hibernação
- 📙 [`docs/correcao_thread_safety.md`](docs/correcao_thread_safety.md) - Correção crítica de threading
- 📕 [`docs/relatorio_status_automacoes.md`](docs/relatorio_status_automacoes.md) - Status geral das automações

### Documentos Técnicos
- [`CORRECAO_APOSTROFOS.md`](CORRECAO_APOSTROFOS.md) - Detalhes da correção de números
- [`SEGURANCA_GIT.md`](SEGURANCA_GIT.md) - Guia de segurança e boas práticas
- [`Renomear.md`](Renomear.md) - Sistema de renomeação inteligente
- [`Implementações.md`](Implementações.md) - Histórico de implementações

### Planilhas Google Sheets

**🟢 Pulso Boletim:**
- 🔗 [BASE BOLETIM VOZ - Genesys](https://docs.google.com/spreadsheets/d/1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE/edit)
- Abas: BASE VOZ, BASE TEXTO, BASE GE COLABORADOR

**Salesforce:**
- 🔗 [BASE BOLETIM - Salesforce](https://docs.google.com/spreadsheets/d/1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk/edit)
- Abas: CRIADO, RESOLVIDO, COMENTARIO BKO

**Produtividade:**
- 🔗 [BASE PRODUTIVIDADE](https://docs.google.com/spreadsheets/d/1nzSa4cnPOPau1-BF221Vc6VEvUiFe6D1suebCcQmAT4/edit)
- Abas: BASE PROD, BASE TEMPO

---

## 🔒 Segurança

### ⚠️ IMPORTANTE: Arquivos Sensíveis

**NUNCA commite os seguintes arquivos:**
- ❌ `boletim.json` - Contém credenciais
- ❌ `*.csv` em `data/` - Podem conter dados sensíveis
- ❌ Qualquer arquivo com "credentials" no nome

### Verificação de Segurança
```powershell
# Verificar que arquivos sensíveis estão ignorados
git check-ignore boletim.json
# Deve retornar: boletim.json

# Ver arquivos ignorados
git status --ignored
```

### Se Credenciais Foram Expostas
Consulte [`SEGURANCA_GIT.md`](SEGURANCA_GIT.md) para:
- Remover credenciais do histórico
- Rotacionar service accounts
- Procedimentos de segurança

---

## 🐛 Solução de Problemas

### Erro: "Arquivo de credenciais não encontrado"
```
Solução:
1. Certifique-se que boletim.json existe na raiz do projeto ou em config/
2. Copie boletim.json.example para boletim.json e configure
3. Verifique permissões do arquivo
```

### Erro: "No module named 'gspread'"
```powershell
pip install -r requirements.txt
# ou especificamente
pip install gspread google-auth pandas
```

### Erro: "Permission denied" nas planilhas
```
Solução:
1. Abra a planilha no Google Sheets
2. Compartilhar → Adicionar email da service account (do boletim.json)
3. Dar permissão de "Editor"
4. Verifique com: python scripts/verificar_acesso_planilhas.py
```

### Interface Travando Durante Processamento
```
Solução:
✅ CORRIGIDO na v3.2.0 - Thread-safety implementado
- Todas as interfaces agora usam .after() para atualizações UI
- "Processar Tudo" funciona sem travar
- Se ainda encontrar problemas, veja docs/correcao_thread_safety.md
```

### Números Aparecem com Apóstrofos
```
Solução:
1. Verifique versão mais recente (v3.2.0+)
2. Execute: python tests/test_sistema.py
3. Função de limpeza deve estar operacional
4. Consulte CORRECAO_APOSTROFOS.md para detalhes
```

### Erro ao Processar Hibernação
```
Solução:
1. Certifique-se que a pasta data/hibernação/ existe
2. Arquivos devem estar nessa pasta específica
3. Use renomeador para padronizar nomes
4. Verifique planilhas_config.json tem IDs corretos
```

---

## 🔄 Fluxo de Trabalho

**Pulso Boletim 🟢:**
```
1. Colocar CSVs na pasta data/
   ↓
2. Executar interface_pulso_boletim.py
   ↓
3. Marcar sistemas desejados (Genesys/Salesforce/Produtividade)
   ↓
4. Sistema detecta e renomeia arquivos automaticamente
   ↓
5. Processa cada CSV:
   - Detecta encoding
   - Limpa formatação de números
   - Remove apóstrofos/aspas
   - Complementa dados na planilha
   ↓
6. Aplica coloração verde
   ↓
7. Gera relatório de sucesso/falhas
```

**Power BI 🟡🟠🟣:**
```
1. Colocar CSVs nas pastas:
   - Filas: data/
   - Autoserviço: data/
   - Hibernação: data/hibernação/
   ↓
2. Executar interface_powerbi.py
   ↓
3. Marcar processadores desejados (Filas/Autoserviço/Hibernação)
   - Escolher semestres (1º ou 2º)
   - Ou marcar tudo e usar "PROCESSAR TUDO"
   ↓
4. Sistema detecta e renomeia arquivos automaticamente
   ↓
5. Processa cada CSV:
   - Detecta encoding
   - Limpa formatação de números
   - Valida dados
   - Complementa dados na planilha (append, não sobrescreve)
   ↓
6. Aplica coloração diferenciada:
   - Filas: Amarelo (#FFD700)
   - Autoserviço: Laranja (#FF6B35)
   - Hibernação: Roxo (#9C27B0)
   ↓
7. Gera KPIs e histórico (json/kpis_historico.json)
```

---

## 📊 Recursos da Limpeza de Números

A função `limpar_numero_formato()` automaticamente:

- ✅ Remove apóstrofos e aspas de números: `'37` → `37`
- ✅ Remove `.0` de inteiros: `37.0` → `37`
- ✅ Normaliza decimais: `1,234.56` → `1.23456`
- ✅ Preserva zeros à esquerda: `0037` → `"0037"`
- ✅ Preserva códigos: `H3014` → `"H3014"`
- ✅ Retorna tipos numéricos (int/float) para números reais

**Resultado:** Números aparecem como números no Google Sheets, não como texto!

---

## 🧪 Testes

### Suite Completa de Testes

```powershell
# Teste geral do sistema
python tests/test_sistema.py

# Teste específico dos 6 processadores Power BI
python tests/teste_todos_processadores.py

# Teste de interfaces
python tests/testar_interfaces.py

# Teste de conversão de números
python tests/testar_conversao_numeros.py
```

**Cobertura:**
- ✅ Imports de todos os módulos
- ✅ Instantiação dos processadores
- ✅ Métodos obrigatórios (processar_e_enviar, formatar_dados)
- ✅ Segurança (ausência de .clear())
- ✅ Thread-safety das interfaces
- ✅ Conversão de números
- ✅ KPIs e histórico

---

## 🤝 Contribuindo

### Reportar Bugs
Abra uma issue com:
- Descrição do problema
- Passos para reproduzir
- Mensagens de erro
- Ambiente (Windows version, Python version)

### Sugerir Melhorias
Abra uma issue com:
- Descrição da funcionalidade
- Casos de uso
- Benefícios esperados

---

## 📝 Changelog

### v3.2.0 (Atual - Dezembro 2024)
**🎨 NOVOS RECURSOS:**
- ✅ **Hibernação Completa**: 2 novos processadores (1º e 2º semestres)
- ✅ **Thread-Safety**: Interfaces não travam durante "Processar Tudo"
- ✅ **UI Aprimorada**: Botões de Hibernação (roxo), links rápidos, seções organizadas
- ✅ **6 Processadores Power BI**: Filas, Autoserviço, Hibernação (2 semestres cada)
- ✅ **Código de Cores**: Amarelo (Filas), Laranja (Autoserviço), Roxo (Hibernação)

**🔧 CORREÇÕES CRÍTICAS:**
- 🐛 Corrigido travamento da interface em processamento batch
- 🐛 Thread-safety: `.update()` substituído por `.after(0, callback)`
- 🐛 Arquivo `hibernacao_segundo_semestre.py` recriado (estava corrompido)

**📚 DOCUMENTAÇÃO:**
- 📘 Criado `docs/interface_powerbi_completa.md` (doc completa v3.2.0)
- 📗 Criado `docs/adicao_botoes_hibernacao.md`
- 📙 Criado `docs/correcao_thread_safety.md`
- 📕 README.md atualizado com 6 processadores

**🧪 TESTES:**
- ✅ `tests/teste_todos_processadores.py` (24/24 testes passando)
- ✅ `tests/teste_botoes_hibernacao.py`
- ✅ `tests/teste_checkboxes_hibernacao.py`
- ✅ 100% dos processadores validados

### v3.1.0 (Outubro 2024)
- ✅ Correção completa de apóstrofos/aspas em números
- ✅ Função `limpar_numero_formato()` implementada
- ✅ Sistema de imports corrigido
- ✅ Integração com Produtividade
- ✅ Interface gráfica melhorada
- ✅ Documentação completa

---

## 👥 Equipe

- **Organização:** Leroy Merlin - Eficiência Operacional
- **Repositório:** Scripts-Eficiencia-Operacional

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação completa em `docs/interface_powerbi_completa.md`
2. Verifique documentos específicos em `docs/`
3. Execute testes de validação em `tests/`
4. Revise exemplos de configuração (boletim.json.example)

---

## � Licença

Este projeto é de uso interno da Leroy Merlin.  
Todos os direitos reservados © 2024

---

<div align="center">

**Desenvolvido com 💚 para Leroy Merlin**

![Verde Leroy Merlin](https://img.shields.io/badge/Pulso_Boletim-%2300A859-00A859?style=for-the-badge)
![Amarelo Power BI](https://img.shields.io/badge/Filas_Genesys-%23FFD700-FFD700?style=for-the-badge)
![Laranja Autoserviço](https://img.shields.io/badge/Autoserviço-%23FF6B35-FF6B35?style=for-the-badge)
![Roxo Hibernação](https://img.shields.io/badge/Hibernação-%239C27B0-9C27B0?style=for-the-badge)

*Sistema RPA • 2 Interfaces • 9 Processadores • Thread-Safe v3.2.0*

</div>

---

## 🎯 Próximos Passos

**Para Pulso Boletim 🟢:**
1. ✅ Coloque CSVs em `data/`
2. ✅ Execute `python -m interfaces.interface_pulso_boletim`
3. ✅ Marque sistemas desejados e clique "EXECUTAR"
4. ✅ Verifique planilhas no Google Sheets

**Para Power BI 🟡🟠🟣:**
1. ✅ Organize arquivos:
   - Filas/Autoserviço → `data/`
   - Hibernação → `data/hibernação/`
2. ✅ Execute `python -m interfaces.interface_powerbi`
3. ✅ Marque processadores e semestres
4. ✅ Use "PROCESSAR TUDO" ou individual
5. ✅ Confira dashboards no Looker Studio

---

**Última atualização:** Dezembro 2024  
**Status:** ✅ Sistema Operacional • ✅ Thread-Safe • ✅ 6 Processadores Power BI
