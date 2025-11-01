# 🟡 Power BI Looker Studio - Documentação Completa

> Automação dedicada para alimentação de dashboards Looker Studio com dados de Filas Genesys.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Diferenças vs Pulso Boletim](#-diferenças-vs-pulso-boletim)
- [Como Usar](#-como-usar)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Planilhas de Destino](#-planilhas-de-destino)
- [Formatação e Cores](#-formatação-e-cores)
- [Processamento](#-processamento)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

O **Power BI Looker Studio** é um sistema de automação independente que:

- ✅ Processa arquivos CSV de **Filas Genesys**
- ✅ Envia dados para **duas planilhas** (Primeiro e Segundo Semestre)
- ✅ Usa **cor amarela** (#FFD700) para diferenciação visual
- ✅ Alimenta **dashboards Looker Studio** para análise BI
- ✅ Interface gráfica dedicada com KPIs em tempo real
- ✅ Renomeação automática de arquivos

---

## 🔄 Diferenças vs Pulso Boletim

| Característica | Pulso Boletim 🟢 | Power BI 🟡 |
|----------------|------------------|-------------|
| **Cor Principal** | Verde (#00A859) | Amarelo (#FFD700) |
| **Cor Cabeçalho** | Verde escuro | Amarelo escuro (#FFA800) |
| **Interface** | `interface_visual.py` | `interface_powerbi.py` |
| **Sistemas** | 3 (Genesys VOZ/TEXTO/GESTÃO, Salesforce, Produtividade) | 1 (Filas Genesys) |
| **Planilhas** | 2 (Genesys, Salesforce) | 2 (Primeiro Semestre, Segundo Semestre) |
| **Arquivo de Entrada** | Múltiplos CSVs padronizados | `Filas Genesys - Todas as Filas .csv` |
| **Finalidade** | Relatórios internos de operação | Dashboards Looker Studio para BI |
| **Frequência** | Diária | Sob demanda |
| **KPIs** | `config/kpis_historico.json` | `config/kpis_powerbi_historico.json` |

**Resumo:** São sistemas **completamente independentes** que compartilham apenas a infraestrutura base (Google Sheets API, renomeador inteligente).

---

## 🚀 Como Usar

### **Método 1: Interface Gráfica (Recomendado)**

#### Windows (Batch):
```bash
# Navegue até a pasta utils/ e execute:
.\utils\powerbi.bat

# Ou duplo clique no arquivo powerbi.bat
```

#### PowerShell:
```powershell
.\utils\powerbi.ps1
```

#### Python Direto:
```powershell
python interface_powerbi.py
```

### **Método 2: Linha de Comando**

#### Processar Primeiro Semestre:
```powershell
python -c "import sys; sys.path.insert(0, 'src'); from src.processadores.powerbi.genesys.filas_primeiro_semestre import ProcessadorFilasPrimeiroSemestre; p = ProcessadorFilasPrimeiroSemestre('config/boletim.json'); p.processar_e_enviar('data/Filas Genesys - Todas as Filas .csv')"
```

#### Processar Segundo Semestre:
```powershell
python -c "import sys; sys.path.insert(0, 'src'); from src.processadores.powerbi.genesys.filas_segundo_semestre import ProcessadorFilasSegundoSemestre; p = ProcessadorFilasSegundoSemestre('config/boletim.json'); p.processar_e_enviar('data/Filas Genesys - Todas as Filas .csv')"
```

---

## 📁 Estrutura de Arquivos

### **Código Fonte**
```
src/processadores/powerbi/
├── __init__.py
└── genesys/
    ├── __init__.py
    ├── filas_primeiro_semestre.py    # Processador Q1/Q2
    └── filas_segundo_semestre.py     # Processador Q3/Q4
```

### **Interface**
```
interface_powerbi.py    # Interface gráfica amarela
```

### **Utilitários**
```
utils/
├── powerbi.bat         # Executor Windows (CMD)
└── powerbi.ps1         # Executor PowerShell
```

### **Configuração**
```
config/
├── boletim.json                # Credenciais Google Service Account
└── kpis_powerbi_historico.json # Histórico de KPIs (auto-gerado)
```

### **Dados**
```
data/
└── Filas Genesys - Todas as Filas .csv    # Arquivo de entrada
```

---

## 📊 Planilhas de Destino

### **🔵 PRIMEIRO SEMESTRE (Q1/Q2)**

**Link:**
[BASE FILA UNIFICADA - PRIMEIRO SEMESTRE](https://docs.google.com/spreadsheets/d/1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc)

**ID:**
```
1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc
```

**Aba:**
- `BASE` (Base Fila Unificada)

**Processador:**
- `ProcessadorFilasPrimeiroSemestre`

**Período:**
- Janeiro a Junho (Q1 e Q2)

---

### **🔵 SEGUNDO SEMESTRE (Q3/Q4)**

**Link:**
[BASE FILA UNIFICADA - SEGUNDO SEMESTRE](https://docs.google.com/spreadsheets/d/1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8)

**ID:**
```
1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8
```

**Aba:**
- `BASE` (Base Fila Unificada)

**Processador:**
- `ProcessadorFilasSegundoSemestre`

**Período:**
- Julho a Dezembro (Q3 e Q4)

---

## 🎨 Formatação e Cores

### **Paleta de Cores**

| Elemento | Cor | Código Hex | RGB |
|----------|-----|------------|-----|
| **Dados** | Amarelo claro | `#FFF299` | rgb(255, 242, 153) |
| **Cabeçalho** | Amarelo escuro | `#FFA800` | rgb(255, 168, 0) |
| **Texto Cabeçalho** | Branco | `#FFFFFF` | rgb(255, 255, 255) |

### **Formatação Aplicada**

#### **Linha 1 (Cabeçalho):**
- ✅ Background: Amarelo escuro (#FFA800)
- ✅ Texto: Branco (#FFFFFF)
- ✅ Fonte: Negrito
- ✅ Alinhamento: Centralizado

#### **Dados (Linha 2+):**
- ✅ Background: Amarelo claro (#FFF299)
- ✅ Texto: Preto (padrão)
- ✅ Fonte: Normal

### **Ordem de Aplicação**
1. Cabeçalho é formatado **ANTES** de adicionar dados
2. Dados são adicionados via `append_rows()`
3. Formatação amarela claro é aplicada nas linhas de dados

---

## ⚙️ Processamento

### **Pipeline de Dados**

```
1. Leitura do CSV
   ├─ Detecta encoding automaticamente (UTF-8, UTF-8-SIG, Latin-1)
   ├─ Detecta separador (;, ,)
   └─ Carrega com pandas

2. Limpeza
   ├─ Remove valores infinitos (inf, -inf)
   ├─ Remove NaN
   └─ Substitui por string vazia

3. Formatação Cabeçalho
   ├─ Aplica amarelo escuro (#FFA800)
   ├─ Texto branco
   └─ Negrito

4. Envio para Planilha
   ├─ Complementa dados existentes
   ├─ Aplica formatação amarela claro (#FFF299)
   └─ Atualiza timestamp

5. Atualização KPIs
   ├─ Total processado
   ├─ Taxa de sucesso
   ├─ Tempo médio
   └─ Última execução
```

### **Complementação de Dados**

O sistema **NÃO sobrescreve** dados existentes:

- ✅ Detecta última linha com dados
- ✅ Adiciona novos dados logo após
- ✅ Mantém histórico completo
- ✅ Não duplica informações

---

## 📝 Arquivo de Entrada

### **Nome Padrão**
```
Filas Genesys - Todas as Filas .csv
```

### **Localização**
```
data/Filas Genesys - Todas as Filas .csv
```

### **Formato**
- **Separador:** `;` (ponto e vírgula) ou `,` (vírgula)
- **Encoding:** UTF-8, UTF-8-SIG, Latin-1 (detectado automaticamente)
- **Cabeçalho:** Primeira linha
- **Dados:** Segunda linha em diante

### **Renomeação Automática**

O renomeador inteligente detecta e corrige automaticamente:

| Arquivo Original | Arquivo Renomeado |
|------------------|-------------------|
| `Filas genesys.csv` | `Filas Genesys - Todas as Filas .csv` |
| `Fila genesys.csv` | `Filas Genesys - Todas as Filas .csv` |
| `filas genesys.csv` | `Filas Genesys - Todas as Filas .csv` |
| `FILAS GENESYS.csv` | `Filas Genesys - Todas as Filas .csv` |

**Como usar:**
1. Coloque o arquivo na pasta `data/`
2. Clique no botão "Renomear Arquivos" na interface
3. Sistema detecta e renomeia automaticamente

---

## 🔧 Troubleshooting

### **Erro: Arquivo não encontrado**

**Sintoma:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/Filas Genesys - Todas as Filas .csv'
```

**Solução:**
1. Verifique se o arquivo está na pasta `data/`
2. Use o botão "Renomear Arquivos" na interface
3. Confirme que o nome está correto (com espaços e acentos)

---

### **Erro: Credenciais inválidas**

**Sintoma:**
```
gspread.exceptions.APIError: [401] Invalid Credentials
```

**Solução:**
1. Verifique se `config/boletim.json` existe
2. Confirme que a service account tem acesso às planilhas
3. Teste com outro processador para isolar o problema

---

### **Erro: Cabeçalho não formatado**

**Sintoma:**
Cabeçalho não aparece com fundo amarelo escuro

**Solução:**
1. Verifique se há dados na linha 1 da planilha
2. Limpe a planilha e processe novamente
3. O cabeçalho é sempre formatado ANTES dos dados

---

### **Erro: Dados não aparecem**

**Sintoma:**
Processamento finaliza sem erros, mas dados não aparecem

**Solução:**
1. Verifique se a aba `BASE` existe
2. Confirme que o CSV tem dados (mais de 1 linha)
3. Verifique logs no console para erros de parsing

---

### **Performance lenta**

**Sintoma:**
Processamento demora mais de 30 segundos

**Solução:**
1. Verifique tamanho do CSV (arquivos >10MB podem demorar)
2. Conexão com internet estável é necessária
3. Google Sheets API tem rate limits (100 requisições/100 segundos)

---

### **Formatação perdida após manual edit**

**Sintoma:**
Editou a planilha manualmente e formatação sumiu

**Solução:**
1. Reprocesse o arquivo
2. Sistema sempre reaplica formatação correta
3. Evite editar linhas 1-2 manualmente

---

## 📞 Suporte

**Dúvidas ou problemas?**

1. Consulte o [README.md](../README.md) principal
2. Verifique a [documentação completa](../docs/documentação.md)
3. Entre em contato com a equipe de RPA Leroy Merlin

---

## 📜 Licença

© 2024 Leroy Merlin - Sistema RPA Interno

---

**Última atualização:** Janeiro 2024  
**Versão:** 3.1.0  
**Autor:** Equipe RPA Leroy Merlin
