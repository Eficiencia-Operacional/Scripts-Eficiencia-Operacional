# 📊 data - Arquivos de Dados CSV

Esta pasta contém todos os arquivos CSV utilizados pelos sistemas RPA para processamento e upload nas planilhas Google Sheets.

---

## 📁 Estrutura de Pastas

```
data/
├── *.csv                    # Arquivos CSV gerais (Pulso Boletim e Power BI)
└── hibernação/              # 🟣 Arquivos CSV de Hibernação (Power BI)
    └── *.csv
```

---

## 📁 Arquivos por Sistema

### **🟢 Pulso Boletim - Arquivos CSV**

#### **Arquivos Genesys**
Dados extraídos do sistema Genesys para análise de atendimento.

##### Bases de Atendimento
- `BASE_GENESYS_VOZ_HC.csv` - Atendimentos de voz (Help Center)
- `BASE_GENESYS_TEXTO_HC.csv` - Atendimentos de texto/chat (Help Center)
- `BASE_GENESYS_GESTAO_HC.csv` - Dados de gestão da entrega

**Colunas Típicas:**
- Data/Hora de início
- Agente/Colaborador
- Fila de atendimento
- Tempo de atendimento
- Status
- Métricas de qualidade

#### **Arquivos Salesforce**
Dados extraídos do Salesforce para análise de casos e tickets.

##### Bases de Casos
- `BASE_SALESFORCE_CRIADO.csv` - Casos criados (abertura)
- `BASE_SALESFORCE_RESOLVIDO.csv` - Casos resolvidos (fechamento)
- `BASE_SALESFORCE_COMENTARIO_BKO.csv` - Comentários de backoffice

**Colunas Típicas:**
- Data de abertura
- Data/Hora de abertura
- Data/Hora de fechamento
- Número do caso
- Número do Pedido LM
- Status
- Proprietário
- Tipo de registro
- Origem
- Motivo

#### **Arquivos de Produtividade**
Dados de produtividade e tempo da equipe.

- `BASE_PRODUTIVIDADE.csv` - Métricas de produtividade

---

### **🟡🟠🟣 Power BI Looker Studio - Arquivos CSV**

#### **🟡 Filas Genesys** (Amarelo)
- `Filas Genesys - Todas as Filas .csv` - Dados de todas as filas Genesys
- **Localização:** `data/`
- **Processadores:** 
  - Primeiro Semestre (Q1/Q2)
  - Segundo Semestre (Q3/Q4)

#### **🟠 Autoserviço** (Laranja)
- Detectado automaticamente pelo renomeador
- **Localização:** `data/`
- **Processadores:**
  - Primeiro Semestre (Q1/Q2)
  - Segundo Semestre (Q3/Q4)

#### **🟣 Hibernação** (Roxo)
- Detectado automaticamente pelo renomeador
- **Localização:** `data/hibernação/` ⚠️ **Pasta específica**
- **Processadores:**
  - Primeiro Semestre (Q1/Q2)
  - Segundo Semestre (Q3/Q4)

**⚠️ IMPORTANTE:** Arquivos de Hibernação devem estar na pasta `data/hibernação/`, não na raiz de `data/`.

---
- `BASE_TEMPO.csv` - Registro de tempo por atividade

**Colunas Típicas:**
- Data
- Colaborador
- Atividade
- Tempo
- Quantidade
- Produtividade

---

### **🟡 Power BI Looker Studio - Arquivos CSV**

#### **Arquivo de Filas Genesys**
Dados unificados de todas as filas do Genesys para dashboards BI.

- `Filas Genesys - Todas as Filas .csv` - Dados completos de todas as filas

**Colunas Típicas:**
- Nome da Fila
- Data/Hora
- Métricas de volume
- Tempo médio de atendimento
- SLA
- Taxa de abandono
- Quantidade de atendimentos

**Variações Reconhecidas pelo Renomeador:**
- `Filas genesys.csv` → Renomeado automaticamente
- `Fila genesys.csv` → Renomeado automaticamente
- `filas genesys.csv` → Renomeado automaticamente

---

## 📋 Formato dos Arquivos CSV

### **Características Padrão**

```csv
# Exemplo de formato esperado
"Coluna1";"Coluna2";"Coluna3"
"Valor1";"Valor2";"Valor3"
"Valor4";"Valor5";"Valor6"
```

**Especificações:**
- ✅ **Separador:** `;` (ponto e vírgula)
- ✅ **Encoding:** UTF-8, UTF-8-SIG, Latin-1 ou CP1252 (detectado automaticamente)
- ✅ **Delimitador de texto:** `"` (aspas duplas)
- ✅ **Cabeçalho:** Primeira linha contém nomes das colunas
- ✅ **Formato de data:** `DD/MM/YYYY` ou `DD/MM/YYYY HH:MM`
- ✅ **Decimal:** `.` (ponto) ou `,` (vírgula) - normalizado automaticamente

### **Encodings Suportados**
O sistema tenta automaticamente (em ordem):
1. `utf-8-sig` (UTF-8 com BOM)
2. `utf-8`
3. `latin-1` (ISO-8859-1)
4. `cp1252` (Windows-1252)
5. `iso-8859-1`

---

## 🔄 Nomenclatura de Arquivos

### **Padrão Recomendado**

**🟢 Pulso Boletim:**
```
BASE_[SISTEMA]_[TIPO].csv
```

**Exemplos Corretos:**
- ✅ `BASE_GENESYS_VOZ_HC.csv`
- ✅ `BASE_SALESFORCE_CRIADO.csv`
- ✅ `BASE_PRODUTIVIDADE.csv`

**🟡 Power BI:**
```
Filas Genesys - Todas as Filas .csv
```

**Exemplo Correto:**
- ✅ `Filas Genesys - Todas as Filas .csv`

**Exemplos Incorretos:**
- ❌ `genesys_voz.csv` (sem prefixo BASE)
- ❌ `Salesforce Criado.csv` (espaços no nome)
- ❌ `base-genesys-voz-hc.csv` (hífens em vez de underscore)

### **Renomeação Automática**
O sistema possui um **renomeador inteligente** que:
- 🔍 Detecta tipo de arquivo pelo conteúdo
- 🔄 Renomeia automaticamente para padrão correto
- ✅ Valida estrutura do CSV
- 📝 Gera log de renomeações

**Executar renomeador:**
```bash
python renomeador_inteligente.py
# ou
python scripts/executar_renomeacao.py
```

---

## 📥 Como Adicionar Novos Arquivos

### **Passo a Passo**

1. **Exportar do sistema fonte**
   - Salesforce → Exportar relatório como CSV
   - Genesys → Exportar dados de atendimento
   - Produtividade → Exportar planilha

2. **Salvar na pasta `data/`**
   ```bash
   # Mover arquivo para pasta correta
   mv ~/Downloads/relatorio.csv ./data/
   ```

3. **Executar renomeador (opcional)**
   ```bash
   python renomeador_inteligente.py
   ```

4. **Executar automação**
   ```bash
   python main.py --salesforce
   # ou
   python interface_visual.py
   ```

---

## 🧹 Limpeza e Manutenção

### **Limpeza Automática de Dados**
O sistema aplica automaticamente:

- ✅ **Remoção de apóstrofos** em datas: `'20/10/2025` → `20/10/2025`
- ✅ **Remoção de .0 desnecessário**: `123.0` → `123`
- ✅ **Normalização de vírgulas**: `,` → `.` em números
- ✅ **Remoção de aspas extras**: `"valor"` → `valor`
- ✅ **Limpeza de caracteres invisíveis**: Unicode zero-width, BOM, etc.

### **Manutenção Manual**

```bash
# Listar arquivos CSV na pasta
ls data/*.csv

# Ver tamanho dos arquivos
ls -lh data/*.csv

# Contar linhas de um arquivo
wc -l data/BASE_SALESFORCE_CRIADO.csv

# Limpar arquivos antigos (mais de 30 dias)
find data/ -name "*.csv" -mtime +30 -delete
```

---

## ⚠️ Boas Práticas

### **✅ Fazer**
- ✅ Manter backup dos arquivos originais
- ✅ Usar nomes descritivos e padronizados
- ✅ Verificar encoding antes de processar
- ✅ Validar dados antes de upload
- ✅ Limpar arquivos processados regularmente

### **❌ Evitar**
- ❌ Modificar arquivos manualmente no Excel (pode alterar encoding)
- ❌ Usar espaços ou caracteres especiais em nomes
- ❌ Misturar separadores (`;` e `,`)
- ❌ Deixar arquivos duplicados na pasta
- ❌ Processar arquivos sem cabeçalho

---

## 🔍 Validação de Dados

### **Checklist Antes de Processar**

```bash
# 1. Verificar formato do arquivo
file data/BASE_SALESFORCE_CRIADO.csv

# 2. Ver primeiras linhas
head -n 5 data/BASE_SALESFORCE_CRIADO.csv

# 3. Verificar separador
cat data/BASE_SALESFORCE_CRIADO.csv | head -1

# 4. Contar colunas
awk -F';' '{print NF; exit}' data/BASE_SALESFORCE_CRIADO.csv

# 5. Verificar encoding
file -i data/BASE_SALESFORCE_CRIADO.csv
```

### **Problemas Comuns**

| Problema | Sintoma | Solução |
|----------|---------|---------|
| **Encoding errado** | Caracteres estranhos (�, Ã§) | Converter para UTF-8 |
| **Separador errado** | Colunas não divididas | Usar `;` em vez de `,` |
| **Sem cabeçalho** | Primeira linha com dados | Adicionar linha de cabeçalho |
| **Datas inválidas** | Formato americano MM/DD/YYYY | Converter para DD/MM/YYYY |
| **Aspas duplicadas** | `""valor""` | Remover aspas extras |

---

## 📊 Estatísticas de Processamento

### **Logs de Execução**
Após processar, o sistema exibe:

```
📊 CSV carregado: 3746 linhas, 21 colunas
🔤 Encoding usado: latin-1
📋 Colunas: ['Data de abertura', 'Data/Hora de abertura'...]
✅ 3746 registros adicionados (sem cabeçalho)
```

### **Arquivos Gerados**
- `config/kpis_historico.json` - Histórico de KPIs
- Logs no console da interface
- Planilhas Google Sheets atualizadas

---

## 🔒 Segurança

### **Dados Sensíveis**
- ⚠️ Arquivos CSV podem conter dados pessoais
- ⚠️ Não commitar CSVs com dados reais no Git
- ⚠️ `.gitignore` já está configurado para ignorar `data/*.csv`
- ⚠️ Fazer backup local dos arquivos

### **Verificação do .gitignore**
```bash
# Verificar se CSVs estão sendo ignorados
git status
# Não deve listar arquivos .csv em data/
```

---

## 📚 Referências

- [RFC 4180 - CSV Format](https://tools.ietf.org/html/rfc4180)
- [Python pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Character Encoding](https://www.w3.org/International/questions/qa-what-is-encoding)

---

**Última atualização:** 21/10/2025  
**Versão:** 2.4.0  
**Mantido por:** Equipe RPA Leroy Merlin
