# 📝 Renomeador Inteligente - Leroy Merlin

Sistema de renomeação automática de arquivos CSV com padronização inteligente baseada em padrões de detecção.

## 🎯 Funcionalidade

O **Renomeador Inteligente** resolve o problema de arquivos CSV que vêm com nomes variáveis (timestamps, datas, etc.) padronizando-os automaticamente para nomes consistentes que o sistema de automação consegue detectar.

## 🔍 Padrões de Detecção

### Salesforce
- `*criado*-2025-09-23-07-00-06.csv` → `BASE_SALESFORCE_CRIADO.csv`
- `*resolvido*-2025-09-23-07-00-06.csv` → `BASE_SALESFORCE_RESOLVIDO.csv` 
- `*comentario*bko*-2025-09-23-07-00-02.csv` → `BASE_SALESFORCE_COMENTARIO_BKO.csv`
- `cópia de *comentario*bko*.csv` → `BASE_SALESFORCE_COMENTARIO_BKO.csv`

### Genesys
- `*voz*hc*.csv` → `BASE_GENESYS_VOZ_HC.csv`
- `*texto*hc*.csv` → `BASE_GENESYS_TEXTO_HC.csv`
- `*gestão*entrega*n1*hc*.csv` → `BASE_GENESYS_GESTAO_N1_HC.csv`
- `*gestão*hc*.csv` → `BASE_GENESYS_GESTAO_HC.csv`

## ⚡ Como Usar

### 🎨 Interface Visual (Recomendado)
1. Abra `interface_visual.py`
2. Clique no botão **"📝 Renomear Arquivos"**
3. Veja o preview das renomeações
4. Confirme para executar

### 🖥️ Linha de Comando
```bash
# Ver preview das renomeações
python renomeador_inteligente.py --preview

# Executar renomeações
python renomeador_inteligente.py --executar

# Especificar pasta diferente
python renomeador_inteligente.py --pasta minha_pasta --preview
```

### 📊 Exemplo de Saída
```
🔍 Testando Renomeador Inteligente...
🔍 Encontrados 6 arquivos CSV

📝 Renomeações planejadas:
  📄 BASE - BOLETIM - CRIADO-2025-09-23-07-00-06.csv
     ➡️  BASE_SALESFORCE_CRIADO.csv
     🎯 Salesforce - Casos Criados (1.19 MB)

  📄 BASE - BOLETIM - RESOLVIDO-2025-09-23-07-00-06.csv
     ➡️  BASE_SALESFORCE_RESOLVIDO.csv
     🎯 Salesforce - Casos Resolvidos (1.08 MB)
```

## 🔧 Recursos Avançados

### 📚 Histórico de Renomeações
- Mantém histórico das últimas 10 renomeações
- Salvo em `data/historico_renomeacao.json`
- Permite restaurar nomes originais

### 🔒 Segurança
- **Modo Preview**: Simula renomeações sem executar
- **Backups**: Histórico permite reverter mudanças
- **Validação**: Verifica conflitos de nomes
- **Timestamp**: Adiciona timestamp em caso de conflito

### 🧠 Detecção Inteligente
- **Regex Patterns**: Múltiplos padrões por tipo
- **Case Insensitive**: Funciona com maiúsculas/minúsculas
- **Fallback**: Padrões genéricos se específicos falharem
- **Tamanho**: Mostra tamanho dos arquivos

## 🎨 Integração com Interface Visual

O renomeador está **totalmente integrado** na interface visual:

1. **Botão Dedicado**: "📝 Renomear Arquivos" na seção "Gestão de Arquivos"
2. **Preview Visual**: Mostra renomeações antes de executar
3. **Confirmação**: Pergunta antes de executar mudanças
4. **Logs Coloridos**: Feedback visual completo
5. **Bloqueio**: Não permite executar durante automação

## ❗ Casos Especiais

### Arquivos Duplicados
- Se `arquivo.csv` e `arquivo (1).csv` existem
- Renomeia para o mesmo padrão
- Sistema detecta e resolve automaticamente

### Conflitos de Nome
- Se arquivo de destino já existe
- Adiciona timestamp: `ARQUIVO_20250923_140530.csv`
- Preserva dados originais

### Histórico
```json
{
  "timestamp": "2025-09-23T14:05:30",
  "renomeacoes": [
    {
      "nome_original": "BASE - BOLETIM - CRIADO-2025-09-23.csv",
      "nome_novo": "BASE_SALESFORCE_CRIADO.csv",
      "tipo_detectado": "Salesforce - Casos Criados",
      "tamanho_mb": 1.19,
      "status": "sucesso"
    }
  ],
  "total_arquivos": 1
}
```

## 🚀 Fluxo Recomendado

1. **Baixar arquivos** da plataforma (nomes originais)
2. **Abrir interface visual** (`python interface_visual.py`)
3. **Clicar "📝 Renomear Arquivos"** (padronizar nomes)
4. **Clicar "🚀 Executar Automação"** (processar para planilhas)

## 🔍 Troubleshooting

### ❌ "Padrão não reconhecido"
- Arquivo não corresponde a nenhum padrão conhecido
- Verificar nome do arquivo
- Adicionar padrão personalizado se necessário

### ⚠️ "Conflito detectado"  
- Arquivo de destino já existe
- Sistema criará nome com timestamp
- Dados preservados em ambos arquivos

### 📁 "Nenhum arquivo encontrado"
- Verificar pasta `data/`
- Confirmar extensão `.csv`
- Verificar permissões de acesso

---

**🎯 O Renomeador Inteligente garante que seus arquivos sempre tenham nomes consistentes, eliminando problemas de detecção automática na automação!**

**💡 Use sempre através da Interface Visual para melhor experiência!**