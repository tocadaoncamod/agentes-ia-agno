# ============================================================
# NÍVEL 5 - Agente com Memória Persistente
# MELHORIAS: nome, storage + memória, mais ferramentas,
#            instruções detalhadas, lembra preferências do usuário
# ============================================================
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("tmp", exist_ok=True)

# === MEMÓRIA PERSISTENTE ===
# Lembra o usuário entre sessões (nome, preferências, projetos)
memory = Memory(
    model=OpenAIChat(id="gpt-4.1-mini"),
    db=SqliteMemoryDb(
        table_name="user_memories",
        db_file="tmp/agent.db"
    ),
)

# === STORAGE DE SESSÃO ===
db = SqliteStorage(table_name="memory_agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente com Memória",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[
        TavilyTools(),
        DuckDuckGoTools(),
        YFinanceTools(stock_price=True, company_info=True),
    ],
    description="Assistente inteligente com memória persistente — lembra nome, projetos e preferências entre conversas.",
    instructions=[
        "Você é um assistente pessoal com memória. Consulte SEMPRE sua memória antes de responder.",
        "Na PRIMEIRA mensagem, pergunte o nome do usuário se não souber. Seja amigável.",
        "Quando o usuário mencionar nome, projetos, preferências ou dados pessoais, salve na memória.",
        "Chame o usuário pelo nome quando já souber. Seja natural, não robótico.",
        "Não memorize: senhas, tokens, chaves de API ou dados financeiros sensíveis.",
        "Use ferramentas de pesquisa para informações atuais quando necessário.",
        "Adapte respostas ao perfil do usuário (ex: se é desenvolvedor, use termos técnicos).",
        "Se o usuário retornar, retome a conversa com contexto: 'Olá [nome]! Como vai o projeto [X]?'",
        "Responda sempre em português brasileiro.",
    ],
    memory=memory,
    enable_agentic_memory=True,
    storage=db,
    add_history_to_messages=True,
    num_history_runs=5,
    markdown=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("31_memory:app", reload=True, port=8003)
