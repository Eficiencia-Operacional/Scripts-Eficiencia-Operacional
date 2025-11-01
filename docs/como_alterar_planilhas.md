# 🔧 Guia Prático - Como Alterar IDs das Planilhas

## 🎯 Sistemas Suportados

### ✅ PULSO BOLETIM (100% Funcional)
- 📊 **Genesys** → `interface_pulso_boletim.py`
- 💼 **Salesforce** → `interface_pulso_boletim.py`
- 📈 **Produtividade** → `interface_pulso_boletim.py`

### ⚠️ POWER BI (Configuração Manual)
- 🟡 **Filas 1º Semestre** → `interface_powerbi.py`
- 🟡 **Filas 2º Semestre** → `interface_powerbi.py`

---

## 🚀 Método 1: Interface Visual (RECOMENDADO)

### Para Pulso Boletim
```bash
python scripts/interface_gerenciador.py
```

**Passos:**
1. Abra a **Aba Planilhas**
2. Localize a planilha que quer alterar
3. Cole o novo ID no campo **"Novo ID"**
4. Clique **✅** para validar
5. Clique **💾 Salvar Alterações**

### Para Power BI
Ainda precisa editar manualmente os arquivos:
- `src/processadores/powerbi/genesys/filas_primeiro_semestre.py`
- `src/processadores/powerbi/genesys/filas_segundo_semestre.py`

---

## ⚡ Método 2: Linha de Comando (RÁPIDO)

```bash
# Atualizar Genesys
python scripts/gerenciador_planilhas.py --atualizar genesys_boletim --id "SEU_NOVO_ID_GENESYS"

# Atualizar Salesforce
python scripts/gerenciador_planilhas.py --atualizar salesforce_boletim --id "SEU_NOVO_ID_SALESFORCE"

# Atualizar Produtividade
python scripts/gerenciador_planilhas.py --atualizar produtividade_boletim --id "SEU_NOVO_ID_PRODUTIVIDADE"

# Ver todas as planilhas
python scripts/gerenciador_planilhas.py --listar
```

---

## 📝 Método 3: Edição Manual (DIRETO)

### Arquivo: `config/planilhas_config.json`

```json
{
  "planilhas": {
    "genesys_boletim": {
      "id": "COLE_SEU_NOVO_ID_GENESYS_AQUI"
    },
    "salesforce_boletim": {
      "id": "COLE_SEU_NOVO_ID_SALESFORCE_AQUI"
    },
    "produtividade_boletim": {
      "id": "COLE_SEU_NOVO_ID_PRODUTIVIDADE_AQUI"
    }
  }
}
```

---

## 🟡 Power BI - Configuração Manual (Temporário)

### Arquivo: `src/processadores/powerbi/genesys/filas_primeiro_semestre.py`
```python
# Linha ~54-58 (aproximadamente)
planilha_id = 'COLE_SEU_ID_1_SEMESTRE_AQUI'
```

### Arquivo: `src/processadores/powerbi/genesys/filas_segundo_semestre.py`
```python
# Linha similar
planilha_id = 'COLE_SEU_ID_2_SEMESTRE_AQUI'
```

---

## 🧪 Como Validar Alterações

### 1. Testar Sistema Completo
```bash
python scripts/teste_sistema.py
```

### 2. Testar Pulso Boletim
```bash
python interface_pulso_boletim.py
# Ou
python main.py --genesys
```

### 3. Testar Power BI
```bash
python interface_powerbi.py
```

---

## 📋 Checklist de Atualização Mensal

### ✅ Para Pulso Boletim (Automatizado)
- [ ] Abrir `python scripts/interface_gerenciador.py`
- [ ] Atualizar IDs na interface
- [ ] Validar IDs (botão ✅)
- [ ] Salvar alterações
- [ ] Testar execução

### ⚙️ Para Power BI (Manual)
- [ ] Editar `filas_primeiro_semestre.py`
- [ ] Editar `filas_segundo_semestre.py`
- [ ] Testar interface Power BI

---

## 🚨 Em Caso de Problema

### Backup Automático
O sistema sempre faz backup antes de alterar. Para restaurar:
```bash
python scripts/atualizar_planilhas.py --listar-backups
python scripts/atualizar_planilhas.py --restaurar nome_do_backup.json
```

### Compatibilidade Retroativa
Se algo der errado, os scripts continuam funcionando com IDs hardcoded antigos.

---

## 🎯 Resumo Rápido

| **Sistema** | **Método** | **Status** |
|-------------|------------|------------|
| **Genesys** | Interface Visual | ✅ Automático |
| **Salesforce** | Interface Visual | ✅ Automático |
| **Produtividade** | Interface Visual | ✅ Automático |
| **Power BI 1º Sem** | Edição Manual | ⚠️ Manual |
| **Power BI 2º Sem** | Edição Manual | ⚠️ Manual |

**Objetivo**: Migrar Power BI para o sistema centralizado também (próxima versão).

---

## 💡 Dica Pro

Use sempre o **Método 1 (Interface Visual)** para Pulso Boletim.
É mais seguro, faz backup automático e valida os IDs automaticamente!
