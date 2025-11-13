# 🛠️ utils - Utilitários e Scripts Auxiliares

Esta pasta contém scripts utilitários e executores auxiliares para facilitar o uso do sistema RPA Leroy Merlin v3.2.0.

---

## 📁 Estrutura de Arquivos

### **Scripts Executores (.bat e .ps1)**
Arquivos batch e PowerShell para Windows que facilitam a execução do sistema.

**São apenas "atalhos convenientes"!** ✨

---

## 🎯 Como Usar e Quando Usar Arquivos BAT ou PS1

### **O que são?**
Estes arquivos são como **atalhos automatizados** que:

✅ Verificam se Python está instalado  
✅ Instalam todas as dependências automaticamente  
✅ Executam o script principal após as verificações  
✅ Facilitam o uso para pessoas não-técnicas  

---

### **Arquivos Disponíveis**

#### **🟢 Pulso Boletim**

##### **executar.bat**
Executor principal para automação via linha de comando.

**Como usar:**
```bash
# Duplo clique no arquivo
# ou
executar.bat

# Com argumentos
executar.bat --salesforce
executar.bat --genesys
executar.bat --produtividade
```

---

##### **interface.bat**
Executor para abrir a interface gráfica do Pulso Boletim (verde).

**Como usar:**
```bash
# Duplo clique no arquivo
# ou
interface.bat
```

**Executa:**
```bash
python -m interfaces.interface_pulso_boletim
```

---

##### **executar.ps1**
Versão PowerShell do executor (mais moderna).

**Como usar:**
```powershell
# No PowerShell
.\executar.ps1
.\executar.ps1 --salesforce
```

---

##### **interface.ps1**
Versão PowerShell para interface gráfica do Pulso Boletim.

**Como usar:**
```powershell
.\interface.ps1
```

---

#### **🟡🟠🟣 Power BI Looker Studio**

##### **powerbi.bat**
Executor para abrir a interface gráfica do Power BI (com 6 processadores: Filas/Autoserviço/Hibernação).

**Como usar:**
```bash
# Duplo clique no arquivo
# ou
powerbi.bat
```

**Executa:**
```bash
python -m interfaces.interface_powerbi
```

**Funcionalidades:**
- 🟡 Processar Filas Genesys (1º e 2º semestres)
- 🟠 Processar Autoserviço (1º e 2º semestres)
- 🟣 Processar Hibernação (1º e 2º semestres)
- ✅ Processar Tudo (marca múltiplos + batch processing)

##### **powerbi.ps1**
Versão PowerShell para interface gráfica do Power BI.

**Como usar:**
```powershell
.\powerbi.ps1
```

**Executa:**
```powershell
python interface_powerbi.py
```

---

## 🚀 Casos de Uso

### **Caso 1: Usuário Não-Técnico - Pulso Boletim**
👤 **Perfil:** Analista que não conhece Python

**Solução:** Duplo clique em `interface.bat`
- ✅ Abre interface gráfica verde automaticamente
- ✅ Não precisa abrir terminal
- ✅ Interface amigável com botões
- 🟢 Processa Genesys, Salesforce e Produtividade

---

### **Caso 2: Usuário Não-Técnico - Power BI**
👤 **Perfil:** Analista que trabalha com dashboards BI

**Solução:** Duplo clique em `powerbi.bat`
- ✅ Abre interface gráfica amarela automaticamente
- ✅ Não precisa abrir terminal
- ✅ Interface focada em Filas Genesys
- 🟡 Alimenta dashboards Looker Studio

---

### **Caso 3: Usuário Avançado - Pulso Boletim**
👤 **Perfil:** Desenvolvedor/Analista técnico

**Solução:** Executar via PowerShell
```powershell
.\executar.ps1 --salesforce
```

---

### **Caso 4: Usuário Avançado - Power BI**
👤 **Perfil:** Desenvolvedor/Analista técnico

**Solução:** Executar via Python
```powershell
python interface_powerbi.py
```

---

### **Caso 3: Automação Agendada**
👤 **Perfil:** Execução diária automática

**Solução:** Agendador de Tarefas do Windows
```
1. Abrir "Agendador de Tarefas"
2. Criar Tarefa Básica
3. Nome: "Automação Leroy Merlin Diária"
4. Gatilho: Diariamente às 08:00
5. Ação: Iniciar programa
   - Programa: C:\...\utils\executar.bat
   - Argumentos: --all
6. Concluir
```

---

## 🔄 Alternativas aos Executores

### **Não quer usar .bat/.ps1?**

**Opção 1: Direto no Python**
```bash
python main.py --salesforce
python interface_visual.py
```

**Opção 2: Instalar como pacote**
```bash
pip install -e .
lm-automacao --salesforce
lm-interface
```

---

## 🐛 Troubleshooting

### **Erro: Python não encontrado**
```bash
# Solução: Instalar Python
# Baixar em python.org
# Marcar "Add Python to PATH" durante instalação
```

### **Erro: Módulo não encontrado**
```bash
# Solução: Reinstalar dependências
pip install -r requirements.txt
```

### **Erro: Permissão negada (PowerShell)**
```powershell
# Solução: Habilitar execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 💡 Resumo

**Arquivos .bat e .ps1 são:**
- ✅ Atalhos convenientes para executar o sistema
- ✅ Fazem verificações automáticas (Python, dependências)
- ✅ Facilitam uso para não-desenvolvedores
- ✅ **NÃO são obrigatórios** - pode executar direto com Python

**Use se:**
- Quer facilidade de duplo clique
- Trabalha com usuários não-técnicos
- Precisa agendar execuções automáticas

**Não use se:**
- Prefere linha de comando direta
- Já tem ambiente configurado
- Usa IDE como VS Code

---

**Última atualização:** 21/10/2025  
**Versão:** 2.4.0  
**Mantido por:** Equipe RPA Leroy Merlin 