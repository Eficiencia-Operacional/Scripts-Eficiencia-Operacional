# 🤖 Resumo da Implementação - Autoserviço Power BI

## ✅ Implementação Concluída

A automação para **Autoserviço Power BI** foi completamente integrada ao sistema seguindo o mesmo padrão das **Filas Genesys**.

---

## 📁 Arquivos Criados

### 1. **Processadores Autoserviço**
- ✅ `src/processadores/powerbi/autoservico/autoservico_primeiro_semestre.py` (465 linhas)
  - Processa dados para o **1º Semestre** (Jan-Jun)
  - Spreadsheet ID: `1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw`
  - Aba: "URA + LIA"

- ✅ `src/processadores/powerbi/autoservico/autoservico_segundo_semestre.py` (465 linhas)
  - Processa dados para o **2º Semestre** (Jul-Dez)
  - Spreadsheet ID: `1Py1W4sSnIbsgMCrr0h0PSTL0DpN-eLj0NoYGbcHLmUI`
  - Aba: "URA + LIA"

- ✅ `src/processadores/powerbi/autoservico/__init__.py`
  - Exporta ambos os processadores

### 2. **Scripts de Teste**
- ✅ `tests/teste_autoservico.py` - Valida todas as importações

---

## 📝 Arquivos Modificados

### 1. **Configuração**
- ✅ `json/planilhas_config.json`
  - Adicionadas 2 novas entradas:
    - `autoservico_primeiro_semestre`
    - `autoservico_segundo_semestre`

### 2. **Renomeador Inteligente**
- ✅ `renomeador_inteligente.py`
  - Adicionados 5 padrões regex para reconhecer arquivos:
    - `Autoserviço Power BI-*.csv`
    - `autoservico power bi*.csv`
    - Variações com/sem acento, com/sem espaços

### 3. **Interface Power BI**
- ✅ `interfaces/interface_powerbi.py`
  
  **Imports:**
  - Adicionados `ProcessadorAutoservicoPrimeiroSemestre` e `ProcessadorAutoservicoSegundoSemestre`
  
  **Checkboxes (linhas ~740):**
  - `self.var_autoservico_primeiro = tk.BooleanVar(value=True)`
  - `self.var_autoservico_segundo = tk.BooleanVar(value=True)`
  - 2 checkboxes laranja com texto "🤖 Processar AUTOSERVIÇO..."
  
  **Botões de Acesso Rápido às Planilhas (linhas ~940):**
  - "🤖 Planilha AUTOSERVIÇO 1º SEM"
  - "🤖 Planilha AUTOSERVIÇO 2º SEM"
  - Estilo: `Laranja.TButton`
  
  **Botões de Processamento Individual (linhas ~1020):**
  - "🤖 PROCESSAR AUTOSERVIÇO 1º SEM"
  - "🤖 PROCESSAR AUTOSERVIÇO 2º SEM"
  - Estilo: `Laranja.TButton`
  
  **Método `abrir_planilha()` (linhas ~1360):**
  - Adicionados casos para `'autoservico_primeiro'` e `'autoservico_segundo'`
  - URLs de fallback incluídas
  
  **Método `executar_individual()` (linhas ~1450):**
  - Atualizado para suportar 4 tipos: `primeiro`, `segundo`, `autoservico_primeiro`, `autoservico_segundo`
  - Checkboxes temporários incluem Autoserviço
  
  **Método `_executar_automacao_thread()` (linhas ~1550):**
  - Adicionadas variáveis `processar_auto_primeiro` e `processar_auto_segundo`
  - Validação atualizada: "pelo menos um semestre/tipo selecionado"
  - **Novo bloco de processamento para Autoserviço 1º Semestre (linhas ~1650)**
  - **Novo bloco de processamento para Autoserviço 2º Semestre (linhas ~1690)**
  - Procura arquivo: `data/Autoserviço Power BI.csv`
  - Usa os processadores corretos
  - Logs detalhados com emojis 🤖
  
  **Controle de Botões:**
  - Desabilita `botao_auto_primeiro` e `botao_auto_segundo` durante execução
  - Reabilita ao finalizar

### 4. **Módulo PowerBI**
- ✅ `src/processadores/powerbi/__init__.py`
  - Adicionados imports dos processadores Autoserviço
  - Atualizado `__all__` para incluir os 4 processadores

---

## 🎨 Padrão de Cores

- **Genesys (Filas):** Verde (`Verde.TButton`) com emoji 📊
- **Autoserviço:** Laranja (`Laranja.TButton`) com emoji 🤖

---

## 🔄 Fluxo de Funcionamento

### **Automação Completa:**
1. Usuário marca checkboxes de Autoserviço
2. Clica em "🚀 EXECUTAR AUTOMAÇÃO COMPLETA"
3. Sistema procura arquivo `Autoserviço Power BI.csv` em `data/`
4. Para cada semestre marcado:
   - Conecta à planilha correspondente
   - Lê e limpa dados do CSV
   - Aplica pré-processamento inteligente (converte números)
   - Envia para aba "URA + LIA"
   - Aplica formatação amarela (#FFA800 cabeçalho, #FFF299 dados)
5. Log detalhado de cada etapa
6. Resumo final com total de linhas processadas

### **Processamento Individual:**
1. Usuário clica em botão específico (ex: "🤖 PROCESSAR AUTOSERVIÇO 1º SEM")
2. Confirma a execução no dialog
3. Sistema executa apenas aquele semestre
4. Restaura checkboxes originais ao finalizar

### **Acesso Rápido:**
1. Usuário clica no botão da planilha (ex: "🤖 Planilha AUTOSERVIÇO 1º SEM")
2. Sistema obtém ID via `GerenciadorPlanilhas`
3. Abre no navegador padrão

---

## 📊 Processamento de Dados

### **Leitura CSV:**
```python
pd.read_csv(caminho, sep=';', dtype=str, keep_default_na=False)
```
- Separador: ponto e vírgula
- Todas as colunas como texto (preserva formato original)
- Não converte células vazias em NaN

### **Pré-processamento Inteligente:**
```python
# Para cada valor:
if valor.replace('.','').replace(',','').isdigit():
    # Converter para int ou float
else:
    # Manter como string
```

### **Upload:**
- Modo: `value_input_option='USER_ENTERED'`
- Google Sheets interpreta números automaticamente
- Sem apóstrofos indesejados

### **Formatação:**
- **Cabeçalho:** #FFA800 (amarelo forte) + negrito
- **Dados:** #FFF299 (amarelo claro)
- Bordas: preto sólido
- Alinhamento: centralizado

---

## 🔗 IDs das Planilhas

| Tipo | Semestre | ID | URL |
|------|----------|----|----|
| Autoserviço | 1º | `1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw` | [Abrir](https://docs.google.com/spreadsheets/d/1kGExLBYIWf3bjSl3MWBea6PohOLFaAZoF16ojT0ktlw/edit) |
| Autoserviço | 2º | `1Py1W4sSnIbsgMCrr0h0PSTL0DpN-eLj0NoYGbcHLmUI` | [Abrir](https://docs.google.com/spreadsheets/d/1Py1W4sSnIbsgMCrr0h0PSTL0DpN-eLj0NoYGbcHLmUI/edit) |

**⚠️ IMPORTANTE:** Compartilhe ambas as planilhas com a conta de serviço:
```
boletim@sublime-shift-472919-f0.iam.gserviceaccount.com
```
Permissão: **Editor**

---

## ✅ Checklist Final

- [x] Processadores criados e testados
- [x] Configuração JSON atualizada
- [x] Renomeador reconhece arquivos Autoserviço
- [x] Interface com checkboxes laranja
- [x] Botões de acesso rápido às planilhas
- [x] Botões de processamento individual
- [x] Integração no workflow principal
- [x] Controle de estado dos botões
- [x] Logs detalhados com emojis
- [x] Testes de importação passando
- [ ] **PENDENTE:** Compartilhar planilhas com conta de serviço ⚠️
- [ ] **PENDENTE:** Testar com CSV real

---

## 🚀 Próximos Passos

1. **Compartilhar Planilhas:**
   - Abra cada planilha no navegador
   - Clique em "Compartilhar"
   - Adicione: `boletim@sublime-shift-472919-f0.iam.gserviceaccount.com`
   - Permissão: **Editor**

2. **Testar CSV Real:**
   - Coloque o arquivo `Autoserviço Power BI.csv` na pasta `data/`
   - Execute a interface: `python utils/interface.ps1` ou `python interfaces/interface_powerbi.py`
   - Marque os checkboxes de Autoserviço
   - Execute e verifique os resultados

3. **Validar Resultados:**
   - Verifique se os dados aparecem corretamente na aba "URA + LIA"
   - Confirme que os números não têm apóstrofos
   - Verifique a formatação amarela

---

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs na interface (área de texto grande)
2. Execute `tests/teste_autoservico.py` para validar importações
3. Confirme que o arquivo CSV está na pasta `data/`
4. Verifique as permissões da conta de serviço nas planilhas

---

**Desenvolvido com sucesso! 🎉**
