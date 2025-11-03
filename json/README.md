# 📊 json - Arquivos de Histórico e Dados

Esta pasta contém todos os arquivos JSON relacionados a histórico e dados do sistema RPA Leroy Merlin.

---

## 📁 Arquivos de Histórico

### **kpis_historico.json** 📊
Arquivo de histórico de KPIs das interfaces gráficas.

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

**Campos:**
- `total_processados` - Total de execuções do sistema
- `taxa_sucesso` - Porcentagem de sucesso (0-100%)
- `tempo_medio` - Tempo médio de execução em segundos
- `ultima_execucao` - Timestamp da última execução
- `arquivos_processados` - Total de arquivos processados
- `arquivos_sucesso` - Arquivos processados com sucesso
- `arquivos_erro` - Arquivos com erro

---

### **historico_renomeacao.json** 📝
Arquivo de histórico do renomeador inteligente de arquivos CSV.

**Gerado automaticamente pelo RenomeadorInteligente.**

```json
[
  {
    "timestamp": "2025-11-01T10:30:00",
    "renomeacoes": [
      {
        "nome_original": "arquivo_antigo.csv",
        "nome_novo": "BASE_SALESFORCE_CRIADO.csv",
        "tipo_detectado": "Salesforce - Casos Criados",
        "tamanho_mb": 2.5,
        "status": "sucesso"
      }
    ],
    "total_arquivos": 1
  }
]
```

**Campos:**
- `timestamp` - Data e hora da renomeação
- `renomeacoes` - Lista de renomeações realizadas
- `total_arquivos` - Total de arquivos processados na operação

---

### **planilhas_config.json** 📋
Configuração centralizada de IDs e metadados das planilhas Google Sheets.

**Gerenciado pelo GerenciadorPlanilhas.**

```json
{
  "planilhas": {
    "genesys_boletim": {
      "nome": "📊 GENESYS BOLETIM",
      "id": "1e48VAZd2v5ZEQ4OK7yDu6KhrRi7mft5eVkh3qwZcdZE",
      "descricao": "Planilha principal do Genesys para boletim diário",
      "tipo": "boletim",
      "ultima_atualizacao": "2025-11-01",
      "abas": {
        "gestao": "BASE GE COLABORADOR",
        "texto": "BASE TEXTO HC",
        "voz": "BASE VOZ HC"
      }
    }
  },
  "historico_mudancas": [
    {
      "data": "2025-11-01 09:17:44",
      "titulo": "Atualização da planilha 'genesys_boletim'",
      "mudancas": ["ID: 1e48VAZd... → novo_id..."],
      "autor": "Sistema"
    }
  ]
}
```

---

## 🔧 Gerenciamento

### **Como Atualizar IDs das Planilhas**

```bash
# Ver status atual
python scripts/gerenciador_planilhas.py --status

# Atualizar ID de uma planilha
python scripts/gerenciador_planilhas.py --atualizar genesys_boletim --id novo_id_aqui

# Listar todas as planilhas
python scripts/gerenciador_planilhas.py --listar
```

### **Como Visualizar Históricos**

```python
import json

# KPIs
with open('json/kpis_historico.json', 'r') as f:
    kpis = json.load(f)
    print(f"Taxa de sucesso: {kpis['taxa_sucesso']}%")

# Renomeações
with open('json/historico_renomeacao.json', 'r') as f:
    historico = json.load(f)
    print(f"Última renomeação: {historico[0]['timestamp']}")
```

---

## 🔐 Segurança

### **Arquivos Protegidos pelo .gitignore**
```gitignore
# Históricos com dados sensíveis
json/historico_renomeacao.json
json/kpis_historico.json
```

### **Backup Automático**
- ✅ Histórico de renomeações mantém últimos 10 registros
- ✅ Histórico de mudanças nas planilhas mantém últimos 50 registros
- ✅ KPIs são atualizados a cada execução das interfaces

---

**Última atualização:** 01/11/2025  
**Versão:** 1.0.0 - Criação da pasta JSON  
**Mantido por:** Equipe RPA Leroy Merlin
