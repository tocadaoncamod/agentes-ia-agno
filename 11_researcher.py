# ============================================================
# NÍVEL 1 - Agente Pesquisador com busca na web
# MELHORIAS: nome, instruções em PT-BR, storage, sem debug_mode,
#            DuckDuckGo como fallback gratuito, Playground UI
# ============================================================
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("tmp", exist_ok=True)

db = SqliteStorage(table_name="researcher_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente Pesquisador",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        TavilyTools(),       # Busca premium (requer TAVILY_API_KEY)
        DuckDuckGoTools(),   # Busca gratuita — funciona sem API key
    ],
    description="Pesquisador especialista que busca, valida e organiza informações atuais da internet.",
    instructions=[
        "Você é um pesquisador profissional. Sempre pesquise ANTES de responder.",
        "Faça pelo menos 2 buscas com termos diferentes para validação cruzada.",
        "Use TavilyTools como fonte primária e DuckDuckGoTools como fallback.",
        "SEMPRE cite as fontes com nome e URL ao final da resposta.",
        "Avalie a confiabilidade: priorize fontes oficiais, acadêmicas e jornalísticas.",
        "Organize resultados com: resumo → detalhes → fontes.",
        "Se a informação é controversa, apresente múltiplos pontos de vista.",
        "Se não encontrar dados confiáveis, diga claramente em vez de inventar.",
        "Responda sempre em português brasileiro.",
    ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    # Modo interativo via terminal
    # agent.print_response("Qual a temperatura agora em Porto Alegre?", stream=True)

    # Modo Playground (painel web)
    serve_playground_app("11_researcher:app", reload=True)
