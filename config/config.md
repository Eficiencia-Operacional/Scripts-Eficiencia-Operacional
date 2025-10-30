# ⚙️ config - Configurações do Sistema

Esta pasta contém todos os arquivos de configuração necessários para o funcionamento do sistema RPA Leroy Merlin.

---

## 📁 Arquivos de Configuração

### **boletim.json** 🔐
Arquivo de credenciais do Google Service Account para acesso às planilhas Google Sheets.

**⚠️ ARQUIVO SENSÍVEL - NÃO COMMITAR NO GIT**

```json
{
  "type": "service_account",
  "project_id": "sublime-shift-472919-f0",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "boletim-315@sublime-shift-472919-f0.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

**Como Obter:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou use existente
3. Ative Google Sheets API
4. Crie Service Account
5. Gere chave JSON
6. Baixe como `boletim.json`
7. Salve nesta pasta **E** na raiz do projeto

**Permissões Necessárias:**
- ✅ Google Sheets API habilitada
- ✅ Email da service account com acesso Editor nas planilhas
- ✅ Arquivo com permissões de leitura apenas

---

### **kpis_historico.json** 📊
Arquivo de histórico de KPIs da interface gráfica do **Pulso Boletim** (verde).

**Gerado automaticamente pelo sistema.**

```json
{
  "total_processados": 9,
  "taxa_sucesso": 100.0,
  "tempo_medio": 15,
  "ultima_execucao": "Hoje 10:07",
  "arquivos_processados": 7,
  "arquivos_sucesso": 7,
  "arquivos_erro": 0
}
```

---

### **kpis_powerbi_historico.json** 📊
Arquivo de histórico de KPIs da interface gráfica do **Power BI** (amarelo).

**Gerado automaticamente pelo sistema.**

```json
{
  "total_processados": 5,
  "taxa_sucesso": 100.0,
  "tempo_medio": 12,
  "ultima_execucao": "Hoje 14:30",
  "arquivos_processados": 2,
  "arquivos_sucesso": 2,
  "arquivos_erro": 0
}
```

**Campos:**
- `total_processados` - Total de execuções do sistema
- `taxa_sucesso` - Porcentagem de sucesso (0-100%)
- `tempo_medio` - Tempo médio de execução em segundos
- `ultima_execucao` - Timestamp da última execução
- `arquivos_processados` - Total de arquivos processados
- `arquivos_sucesso` - Arquivos processados com sucesso
- `arquivos_erro` - Arquivos com erro

---

## 🔧 Configurações do Sistema

### **IDs das Planilhas Google Sheets**

#### **🟢 Pulso Boletim**

##### **Salesforce**
```python
ID_PLANILHA_SALESFORCE = "1luDIE2OSjunty4-l_pHkRKsP3AMCMOes80A4Xc607Qk"
```

**Abas:**
- `BASE ATUALIZADA CORRETA - CRIADO`
- `BASE ATUALIZADA CORRETA - RESOLVIDA`
- `BASE ATUALIZADA CORRETA - COMENTARIO BKO`

##### **Genesys**
```python
ID_PLANILHA_GENESYS = "1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE"
```

**Abas:**
- `BASE GE COLABORADOR` (Gestão da Entrega)
- `BASE TEXTO HC` (Texto Help Center)
- `BASE VOZ HC` (Voz Help Center)

---

#### **🟡 Power BI Looker Studio**

##### **Primeiro Semestre (Q1/Q2)**
```python
ID_PLANILHA_PRIMEIRO_SEMESTRE = "1VtNTqp907enX0M3gB05dmPckDRl7nnfgVEl3mNF8ILc"
```

**Aba:**
- `BASE` (Base Fila Unificada - Primeiro Semestre)

##### **Segundo Semestre (Q3/Q4)**
```python
ID_PLANILHA_SEGUNDO_SEMESTRE = "1r5eZWGVuBP4h68KfrA73lSvfEf37P-AuUCNHF40ttv8"
```

**Aba:**
- `BASE` (Base Fila Unificada - Segundo Semestre)

---

## 🔐 Segurança

### **Arquivos Protegidos pelo .gitignore**
```gitignore
# Credenciais sensíveis
boletim.json
*.json

# Dados sensíveis
data/*.csv
```

### **Verificação de Segurança**
```bash
# Verificar se credenciais estão protegidas
git status
# boletim.json NÃO deve aparecer
```

---

## 🛠️ Configuração Inicial

### **Setup Passo a Passo**

#### 1. **Obter Credenciais Google**
```bash
# 1. Acessar Google Cloud Console
# 2. Criar Service Account
# 3. Baixar boletim.json
# 4. Copiar para config/ E raiz
cp ~/Downloads/boletim.json config/
cp ~/Downloads/boletim.json ./
```

#### 2. **Configurar Permissões nas Planilhas**
```
1. Abrir planilha Google Sheets
2. Clicar em "Compartilhar"
3. Adicionar email da Service Account
4. Definir como "Editor"
5. Clicar em "Compartilhar"
```

#### 3. **Testar Conexão**
```bash
python tests/teste_credenciais.py
# Deve exibir: ✅ Credenciais válidas
```

---

**Última atualização:** 21/10/2025  
**Versão:** 2.4.0  
**Mantido por:** Equipe RPA Leroy Merlin