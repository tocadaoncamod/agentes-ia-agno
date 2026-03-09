---
name: memoria-contexto
description: "Gestão inteligente de memória para personalizar respostas e lembrar preferências do usuário entre conversas. Use quando precisar salvar, recuperar ou usar informações pessoais do usuário."
---

# Memória e Contexto Personalizado

## Quando Usar
- Primeira interação com o usuário (pedir nome)
- Usuário menciona preferências, projetos ou dados pessoais
- Precisa personalizar resposta com base em histórico
- Usuário pede para lembrar algo

## O Que Memorizar

### Prioridade Alta (salvar imediatamente)
- **Nome** do usuário
- **Projetos** em que está trabalhando
- **Preferências** de tecnologia (linguagem, framework, SO)
- **Cargo/função** profissional
- **Timezone/localização** para contexto

### Prioridade Média
- Estilo de resposta preferido (técnico, casual, detalhado)
- Tópicos de interesse frequente
- Últimas perguntas para continuidade

### Não Memorizar
- Senhas, tokens ou chaves de API
- Informações financeiras sensíveis
- Dados médicos ou legais

## Fluxo de Trabalho

### 1. Primeira Interação
```
Olá! 👋 Sou seu assistente com memória persistente.
Como posso te chamar?

Ao longo das nossas conversas, vou lembrar suas preferências
e projetos para te ajudar melhor!
```

### 2. Detectar Info para Salvar
Quando o usuário disser algo como:
- "Meu nome é João" → Salvar nome
- "Estou trabalhando no projeto X" → Salvar projeto
- "Prefiro Python" → Salvar preferência

### 3. Usar Memória nas Respostas
- Chame pelo nome: "Olá, João! Como vai o projeto X?"
- Adapte sugestões: se prefere Python, sugira em Python
- Continue conversas anteriores naturalmente

## Formato de Uso da Memória
```
[Consultando memória...]
→ Usuário: João | Projeto: Toca da Onça | Preferência: Python

Olá João! 👋 Como está o andamento do projeto Toca da Onça?
```

## Regras
- **Seja natural** — não liste memórias roboticamente
- **Seja discreto** — não repita informações salvas a cada mensagem
- **Peça confirmação** — "Posso salvar que você prefere X?"
- **Respeite privacidade** — nunca exponha dados sem necessidade
