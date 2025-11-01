# 🧪 tests - Testes Automatizados

Esta pasta contém todos os scripts de teste para validação do sistema RPA Leroy Merlin.

---

## 📋 Estrutura de Testes

### **Testes de Integração**
Scripts que testam o sistema completo com dados reais.

- `teste_sistema_completo.py` - Testa todo o fluxo de automação
- `teste-genesys.py` - Testa processamento Genesys (VOZ, TEXTO, Gestão)
- `teste-salesforce.py` - Testa processamento Salesforce (Criado, Resolvido, BKO)
- `teste-produtividade.py` - Testa processamento de Produtividade
- `teste-voz.py` - Testa especificamente base VOZ HC

### **Testes de Componentes**
Scripts que testam funcionalidades específicas isoladamente.

#### Credenciais e Conexão
- `teste_credenciais.py` - Valida credenciais do Google Sheets
- `teste_upload_genesys.py` - Testa upload para planilha Genesys

#### Renomeação de Arquivos
- `teste_renomeador.py` - Testa renomeador inteligente
- `teste_renomeacao_tempo.py` - Testa performance de renomeação

#### Formatação e Limpeza de Dados
- `teste_limpeza_datas.py` - Testa remoção de aspas/apóstrofos em datas
- `teste_limpeza_virgulas.py` - Testa remoção de vírgulas em datas
- `teste_aspas.py` - Testa limpeza de aspas em geral
- `teste_aspas_simples.py` - Testa aspas simples
- `teste_novos_ids.py` - Testa identificação de novos registros

#### Fórmulas do Google Sheets
- `teste_formulas_genesys.py` - Testa aplicação de fórmulas Genesys
- `teste_formulas_salesforce.py` - Testa aplicação de fórmulas Salesforce
- `teste_formulas_resolvido.py` - Testa fórmulas da base RESOLVIDA
- `teste_formulas_linhas_novas.py` - Testa aplicação apenas em linhas novas
- `teste_copypaste_formulas.py` - Testa método copyPaste de fórmulas

#### Processamento de Dados
- `teste_base_tempo.py` - Testa processamento de base tempo
- `teste_produtividade_completo.py` - Teste completo de produtividade
- `teste_produtividade_final.py` - Teste final de produtividade
- `teste_kpis.py` - Testa cálculo e atualização de KPIs
- `processar-todos-csvs.py` - Processa todos os CSVs de teste
- `verificar_ids_completo.py` - Verifica IDs duplicados/novos

## 🚀 Como Executar os Testes

### **Executar Teste Individual**
```bash
# Executar um teste específico
python tests/teste_sistema_completo.py
python tests/teste-genesys.py
python tests/teste_credenciais.py
```

### **Executar Testes por Categoria**
```bash
# Testes de Genesys
python tests/teste-genesys.py
python tests/teste_formulas_genesys.py
python tests/teste-voz.py

# Testes de Salesforce
python tests/teste-salesforce.py
python tests/teste_formulas_salesforce.py
python tests/teste_formulas_resolvido.py

# Testes de Formatação
python tests/teste_limpeza_datas.py
python tests/teste_limpeza_virgulas.py
python tests/teste_aspas.py
```

### **Executar Todos os Testes**
```bash
# Processar todos os CSVs de teste
python tests/processar-todos-csvs.py
```

---

## ✅ Boas Práticas

### **Antes de Executar Testes**
1. ✅ Verificar se credenciais (`boletim.json`) estão configuradas
2. ✅ Garantir que arquivos CSV de teste existem em `data/`
3. ✅ Conferir se dependências estão instaladas (`pip install -r requirements.txt`)
4. ✅ Fazer backup das planilhas antes de testes destrutivos

### **Durante os Testes**
- 📊 Monitorar saída do console para erros
- 🔍 Verificar logs detalhados
- ⏱️ Observar tempo de execução
- 📈 Conferir resultados nas planilhas Google Sheets

### **Após os Testes**
- ✅ Validar dados nas planilhas de destino
- ✅ Verificar se fórmulas foram aplicadas corretamente
- ✅ Confirmar formatação (verde Leroy Merlin)
- ✅ Checar se não há dados duplicados

---

## 📝 Estrutura de um Teste Típico

```python
#!/usr/bin/env python3
"""
Descrição do teste
"""
import sys
import os

# Adicionar src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')
sys.path.append(src_dir)

# Importar módulos necessários
from processadores.genesys.processador_genesys import ProcessadorGenesys

def main():
    """Função principal do teste"""
    print("🧪 Iniciando teste...")
    
    # Executar teste
    # ... código de teste ...
    
    print("✅ Teste concluído!")

if __name__ == "__main__":
    main()
```

---

## 🐛 Troubleshooting

### **Erro: ModuleNotFoundError**
```bash
# Solução: Adicionar src ao Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"  # Linux/Mac
$env:PYTHONPATH += ";$(PWD)\src"              # Windows PowerShell
```

### **Erro: Credenciais não encontradas**
```bash
# Solução: Copiar boletim.json para a raiz
cp config/boletim.json ./boletim.json
```

### **Erro: Arquivo CSV não encontrado**
```bash
# Solução: Verificar se arquivos existem em data/
ls data/*.csv
```

---

## 📊 Resultados Esperados

### **Testes Bem-Sucedidos**
- ✅ Mensagem "✅ Teste concluído com sucesso!"
- ✅ Dados aparecem na planilha de destino
- ✅ Formatação verde aplicada
- ✅ Fórmulas funcionando corretamente
- ✅ Sem erros no console

### **Indicadores de Problemas**
- ❌ Exceções Python no console
- ❌ Dados não aparecem na planilha
- ❌ Formatação não aplicada
- ❌ Fórmulas com erro (#REF!, #VALUE!, etc.)
- ❌ Aspas/apóstrofos em datas

---

## 🔄 Atualização de Testes

Sempre que adicionar nova funcionalidade ao sistema:

1. **Criar teste específico** para a nova feature
2. **Atualizar testes existentes** se necessário
3. **Documentar** o novo teste neste arquivo
4. **Executar bateria completa** para garantir que nada quebrou
5. **Commitar** teste junto com o código

---

## 📚 Referências

- [pytest Documentation](https://docs.pytest.org/)
- [unittest - Python](https://docs.python.org/3/library/unittest.html)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

**Última atualização:** 21/10/2025  
**Versão:** 2.4.0  
**Mantido por:** Equipe RPA Leroy Merlin
