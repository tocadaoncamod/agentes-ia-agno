---
name: criador-agentes
description: "Guia para criar novos agentes especializados de alta qualidade com Agno. Use quando o usuário pedir para criar um novo agente, bot ou assistente especializado."
---

# Criação de Agentes Especializados

## Quando Usar
- Usuário pede para criar um novo agente/bot/assistente
- Necessidade de automatizar uma tarefa específica
- Criação de time de agentes

## Princípios de Design

### 1. Nome Descritivo
- Use nomes que descrevam a função: "Agente de Vendas", "Analista de SEO"
- Evite nomes genéricos como "Bot1" ou "Agente2"

### 2. Descrição Clara
- Escreva em 1-2 frases O QUE o agente faz
- Inclua o domínio de atuação
- Exemplo: "Analista de marketing digital especializado em métricas de redes sociais e ROI de campanhas."

### 3. Instruções Detalhadas (mínimo 5)
Cada agente deve ter instruções que cubram:
1. **Identidade** — Quem ele é e o que faz
2. **Especialidade** — Domínio de conhecimento
3. **Formato** — Como apresentar respostas
4. **Tom** — Formal, casual, técnico
5. **Idioma** — Sempre especifique "Responda em português brasileiro"
6. **Limitações** — O que NÃO deve fazer

### 4. Ferramentas Adequadas
Escolha ferramentas que façam sentido para a função:
- Pesquisa: `DuckDuckGoTools()`, `TavilyTools()`
- Finanças: `YFinanceTools()`
- Web scraping: ferramentas customizadas
- Cálculos: funções Python customizadas

### 5. Modelo Adequado
- **Tarefas simples/gratuitas**: `Groq(id="llama-3.3-70b-versatile")`
- **Tarefas complexas**: `OpenAIChat(id="gpt-4.1-mini")`
- **Máxima qualidade**: `OpenAIChat(id="gpt-4.1")`

## Template de Código

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()
os.makedirs("tmp", exist_ok=True)

db = SqliteStorage(table_name="NOME_session", db_file="tmp/agent.db")

agent = Agent(
    name="NOME DO AGENTE",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[],  # Adicionar ferramentas relevantes
    description="DESCRIÇÃO CLARA DO AGENTE",
    instructions=[
        "INSTRUÇÃO 1 — identidade",
        "INSTRUÇÃO 2 — especialidade",
        "INSTRUÇÃO 3 — formato de resposta",
        "INSTRUÇÃO 4 — tom e estilo",
        "INSTRUÇÃO 5 — limitações",
        "Responda sempre em português brasileiro.",
    ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=5,
    markdown=True,
    show_tool_calls=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("ARQUIVO:app", reload=True, port=8XXX)
```

## Checklist Antes de Entregar
- [ ] Nome descritivo definido
- [ ] Mínimo 5 instruções escritas
- [ ] Ferramentas adequadas configuradas
- [ ] Storage configurado para persistir sessões
- [ ] Playground configurado com porta única
- [ ] Testado com pelo menos 1 pergunta
