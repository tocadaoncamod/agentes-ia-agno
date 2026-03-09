---
name: analise-pdf
description: "Extração inteligente de insights, resumos e dados de documentos PDF usando RAG. Use quando o usuário pedir para analisar, resumir ou responder perguntas sobre um documento PDF."
---

# Análise de PDF com RAG

## Quando Usar
- Usuário envia um PDF ou pede para analisar um documento
- Perguntas sobre conteúdo de um documento carregado
- Resumo ou extração de dados de PDFs

## Fluxo de Trabalho

### 1. Verificar o Documento
- Confirme que o PDF está carregado no ChromaDB
- Se não estiver, carregue com `knowledge.load()`
- Informe quantos chunks foram indexados

### 2. Buscar no Documento
- Use `search_knowledge=True` para buscar trechos relevantes
- Sempre busque ANTES de responder
- Se a pergunta é ampla, faça múltiplas buscas com termos diferentes

### 3. Tipos de Análise

#### Resumo Executivo
```
## 📄 Resumo: [Nome do Documento]

### Tema Principal
[1-2 frases sobre o assunto central]

### Pontos-Chave
1. [ponto 1]
2. [ponto 2]
3. [ponto 3]

### Dados Importantes
| Métrica | Valor |
|---------|-------|
| ...     | ...   |

### Conclusão do Documento
[2-3 frases com a conclusão principal]
```

#### Resposta a Pergunta Específica
```
## 🔍 Resposta

[Resposta direta e objetiva]

> 📖 Trecho do documento: "[citação relevante]"

### Contexto
[Informações adicionais do documento que complementam a resposta]
```

#### Extração de Dados
```
## 📊 Dados Extraídos: [Tema]

| Coluna 1 | Coluna 2 | Coluna 3 |
|----------|----------|----------|
| dado     | dado     | dado     |

*Fonte: [nome do documento], página/seção X*
```

## Regras Importantes
- **Cite trechos** — sempre mostre de onde veio a informação
- **Honestidade** — se a resposta não está no documento, diga claramente
- **Não invente** — nunca adicione informações que não estão no PDF
- **Formate bem** — use tabelas para dados numéricos, listas para pontos-chave
- **Chame "senhor"** — trate o usuário com respeito formal
