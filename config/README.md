# ⚙️ config - Configurações do Sistema

Esta pasta contém apenas os arquivos de configuração necessários para o funcionamento do sistema RPA Leroy Merlin.

**📊 Arquivos de histórico foram movidos para `/json/`**

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

## � Gerenciador de Planilhas

### **gerenciador_planilhas.py** 🐍
Sistema centralizado para gerenciar IDs e configurações das planilhas.

**Localização:** Agora em `scripts/gerenciador_planilhas.py`  
**Dados:** Os IDs das planilhas são gerenciados através do arquivo `json/planilhas_config.json`

**Recursos:**
- ✅ Configuração centralizada em JSON
- ✅ Fácil atualização de IDs
- ✅ Histórico de mudanças
- ✅ Validação de configurações
- ✅ Interface de linha de comando

**Uso:**
```bash
# Ver status atual
python scripts/gerenciador_planilhas.py --status

# Listar planilhas
python scripts/gerenciador_planilhas.py --listar

# Atualizar ID de uma planilha
python scripts/gerenciador_planilhas.py --atualizar genesys_boletim --id novo_id_aqui
```

---

## 🔐 Segurança

### **Arquivos Protegidos pelo .gitignore**
```gitignore
# Credenciais sensíveis
boletim.json
*.json

# Dados sensíveis
data/*.csv

# Históricos (agora em /json/)
json/historico_renomeacao.json
json/kpis_historico.json
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

**Última atualização:** 01/11/2025  
**Versão:** 2.5.0 - Reorganização JSON  
**Mantido por:** Equipe RPA Leroy Merlin