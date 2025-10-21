# Automação Leroy Merlin - RPA

<div align="center">

<img src="img/leroy.png" alt="Leroy Merlin Logo" width="200">

**Sistema RPA Profissional para Processamento Automatizado de Dados**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Internal-red.svg)]()
[![Status](https://img.shields.io/badge/status-production-success.svg)]()
[![Version](https://img.shields.io/badge/version-2.4.0-green.svg)]()
[![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)]()

Sistema automatizado para processamento e envio de dados para Google Sheets  
**(Genesys, Salesforce e Produtividade)**

[Características](#-recursos) •
[Instalação](#-instalação) •
[Uso](#-uso) •
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
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Segurança](#-segurança)
- [Suporte](#-suporte)

---

## ✨ Recursos

### Processamento Automatizado
- ✅ **Genesys**: VOZ HC, TEXTO HC, Gestão da Entrega
- ✅ **Salesforce**: Criado, Resolvido, Comentários BKO
- ✅ **Produtividade**: Base Produtividade, Base Tempo

### Funcionalidades
- 🔄 Detecção automática de encoding (UTF-8, Latin-1, CP1252, etc.)
- 🔢 Limpeza inteligente de números (remove apóstrofos, aspas, .0 desnecessário)
- 🎨 Coloração automática (verde Leroy Merlin)
- 📊 Complementa dados existentes (não sobrescreve)
- 🔁 Renomeação inteligente de arquivos
- 🖥️ Interface gráfica e linha de comando
- 📝 Relatórios detalhados de processamento

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
```

---

## 🔧 Instalação

### 1. Clone o Repositório
```powershell
git clone https://github.com/Ryanditko/rpa-leroy-merlin.git
cd rpa-leroy-merlin
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

Certifique-se de que existe a pasta `data/`:
```powershell
mkdir data -Force
```

### 3. Verificação

Teste se tudo está configurado:
```powershell
python teste_sistema_completo.py
```

Você deve ver:
```
✅ TODOS OS TESTES PASSARAM COM SUCESSO!
```

---

## 🎯 Uso

### Opção 1: Interface Gráfica (Recomendado)

```powershell
python interface_visual.py
```

Ou use os atalhos:
```powershell
.\interface.bat
# ou
.\interface.ps1
```

**Na interface:**
1. Marque as caixas dos sistemas desejados
2. Clique em "EXECUTAR AUTOMAÇÃO"
3. Acompanhe o progresso em tempo real

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
rpa-leroy-merlin/
│
├── 📄 main.py                      # Script principal
├── 🖥️ interface_visual.py          # Interface gráfica
├── 🔄 renomeador_inteligente.py    # Renomeação automática de CSVs
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
│       └── produtividade/
│           └── produtividade.py
│
├── 📂 data/                        # Coloque seus CSVs aqui
│   └── *.csv
│
├── 📂 config/
│   └── boletim.json               # Credenciais (não versionado)
│
├── 📂 tests/                      # Scripts de teste
│   └── *.py
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

## 📚 Documentação

### Documentos Disponíveis
- [`CORRECAO_APOSTROFOS.md`](CORRECAO_APOSTROFOS.md) - Detalhes da correção de números
- [`SEGURANCA_GIT.md`](SEGURANCA_GIT.md) - Guia de segurança e boas práticas
- [`Renomear.md`](Renomear.md) - Sistema de renomeação inteligente
- [`Implementações.md`](Implementações.md) - Histórico de implementações

### Planilhas Google Sheets

**Genesys:**
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
1. Certifique-se que boletim.json existe na raiz do projeto
2. Ou na pasta config/
3. Verifique permissões do arquivo
```

### Erro: "No module named 'gspread'"
```powershell
pip install gspread google-auth pandas
```

### Erro: "Permission denied" nas planilhas
```
Solução:
1. Abra a planilha no Google Sheets
2. Compartilhar → Adicionar email da service account
3. Dar permissão de "Editor"
```

### Números ainda aparecem com apóstrofos
```
Solução:
1. Verifique que está usando a versão mais recente
2. Execute: python teste_sistema_completo.py
3. A função de limpeza deve estar operacional
4. Consulte CORRECAO_APOSTROFOS.md
```

---

## 🔄 Fluxo de Trabalho

```
1. Colocar CSVs na pasta data/
   ↓
2. Executar automação (GUI ou CLI)
   ↓
3. Sistema detecta e renomeia arquivos
   ↓
4. Processa cada CSV:
   - Detecta encoding
   - Limpa formatação de números
   - Remove apóstrofos/aspas
   - Complementa dados na planilha
   ↓
5. Aplica coloração verde
   ↓
6. Gera relatório de sucesso/falhas
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

### Versão Atual (Outubro 2025)
- ✅ Correção completa de apóstrofos/aspas em números
- ✅ Função `limpar_numero_formato()` implementada
- ✅ Sistema de imports corrigido
- ✅ Integração com Produtividade
- ✅ Interface gráfica melhorada
- ✅ Documentação completa

---

## 👥 Equipe

- **Desenvolvedor Principal:** Ryanditko
- **Organização:** Leroy Merlin
- **Repositório:** https://github.com/Ryanditko/automacao-LM

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `docs/`
2. Verifique issues existentes no GitHub
3. Abra uma nova issue se necessário

---

## 📜 Licença
---

## 📄 Licença

Este projeto é de uso interno da Leroy Merlin.  
Todos os direitos reservados © 2025

---

<div align="center">

**Desenvolvido com 💚 para Leroy Merlin**

![Verde Leroy Merlin](https://img.shields.io/badge/Verde_Leroy_Merlin-%2300A859-00A859?style=for-the-badge)

*Sistema RPA • Processamento Automatizado • Interface Profissional v2.4*

</div>

---

## 🎯 Próximos Passos

Após configuração:
1. ✅ Coloque seus CSVs em `data/`
2. ✅ Execute `python interface_visual.py`
3. ✅ Verifique as planilhas no Google Sheets
4. ✅ Confirme que os números estão sem apóstrofos
5. ✅ Aproveite a automação! 🚀

---

**Última atualização:** 21/10/2025 
**Status:** ✅ Sistema Operacional
