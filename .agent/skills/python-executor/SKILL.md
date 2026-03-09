---
name: python-executor
description: "Boas práticas para escrever, testar e executar código Python de forma segura. Use quando precisar executar código Python, instalar pacotes ou automatizar tarefas."
---

# Execução de Python

## Quando Usar
- Usuário pede para executar, escrever ou testar código Python
- Cálculos complexos que precisam de código
- Automação de tarefas com scripts
- Instalação de pacotes

## Boas Práticas

### 1. Antes de Executar
- Planeje o código mentalmente antes de escrever
- Identifique dependências necessárias
- Instale pacotes faltantes com `instalar_pacote()` ANTES de executar

### 2. Escrevendo Código
```python
# SEMPRE inclua:
# 1. Imports no topo
# 2. Tratamento de erros (try/except)
# 3. Print do resultado
# 4. Encoding UTF-8 para strings

try:
    # Seu código aqui
    resultado = funcao()
    print(f"✅ Resultado: {resultado}")
except Exception as e:
    print(f"❌ Erro: {e}")
```

### 3. Segurança
- ⛔ NUNCA execute `rm -rf`, `del *`, ou comandos destrutivos
- ⛔ NUNCA acesse arquivos fora do diretório do projeto
- ⛔ NUNCA faça requests para APIs desconhecidas sem permissão
- ✅ Use `tempfile` para arquivos temporários
- ✅ Use timeout para evitar loops infinitos

### 4. Formato de Resposta
```
## 🐍 Código Executado

[Breve descrição do que o código faz]

### Resultado
[Output do código formatado]

### Código Fonte
```python
[código usado]
```
```

## Instalação de Pacotes
- Use `instalar_pacote("nome")` em vez de `pip install` direto
- Verifique se o pacote já está instalado com `listar_pacotes()`
- Pacotes comuns já instalados: agno, openai, groq, yfinance, pandas
