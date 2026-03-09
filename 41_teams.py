# ============================================================
# NÍVEL 6 - Time de Agentes com Roteamento Inteligente
# MELHORIAS: modelo mais barato (gpt-4.1-mini em vez de gpt-4o),
#            agente em português adicionado, Playground UI,
#            storage, melhor lógica de roteamento
# ============================================================
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("tmp", exist_ok=True)

# === AGENTES ESPECIALIZADOS POR IDIOMA ===

agente_portugues = Agent(
    name="Agente Português",
    role="Você só responde em português brasileiro.",
    model=Groq(id="llama-3.3-70b-versatile"),  # Gratuito para PT-BR
    tools=[DuckDuckGoTools()],
    instructions=["Responda apenas em português brasileiro.", "Seja claro e objetivo."],
)

english_agent = Agent(
    name="English Agent",
    role="You only answer in English.",
    model=OpenAIChat(id="gpt-4.1-mini"),  # Mais barato que gpt-4o
    instructions=["Answer only in English.", "Be clear and concise."],
)

spanish_agent = Agent(
    name="Agente Español",
    role="Solo respondes en español.",
    model=OpenAIChat(id="gpt-4.1-mini"),
    instructions=["Responde solo en español.", "Sé claro y conciso."],
)

french_agent = Agent(
    name="Agent Français",
    role="Tu réponds uniquement en français.",
    model=OpenAIChat(id="gpt-4.1-mini"),
    instructions=["Répondre uniquement en français.", "Soyez clair et concis."],
)

# === TIME DE ROTEAMENTO ===
time_multilingual = Team(
    name="Time Multilingual",
    mode="route",
    model=OpenAIChat(id="gpt-4.1-mini"),
    members=[agente_portugues, english_agent, spanish_agent, french_agent],
    show_tool_calls=True,
    markdown=True,
    description="Roteador inteligente que detecta o idioma do usuário e direciona para o agente especializado correto.",
    instructions=[
        "Detecte o idioma da pergunta do usuário com precisão.",
        "Português ou pt-BR → Agente Português",
        "English → English Agent",
        "Español, castellano → Agente Español",
        "Français → Agent Français",
        "Se o idioma não for suportado, responda em inglês listando os 4 idiomas disponíveis.",
        "Se a mensagem contiver múltiplos idiomas, use o idioma predominante.",
        "Nunca traduza a mensagem — roteie para o agente do idioma correto.",
    ],
    show_members_responses=True,
    storage=SqliteStorage(table_name="team_session", db_file="tmp/agent.db"),
    add_history_to_messages=True,
)

app = Playground(agents=[], teams=[time_multilingual]).get_app()

if __name__ == "__main__":
    # Testes via terminal
    # time_multilingual.print_response("Olá! Como você está?", stream=True)
    # time_multilingual.print_response("How are you?", stream=True)
    # time_multilingual.print_response("¿Cómo estás?", stream=True)

    serve_playground_app("41_teams:app", reload=True, port=8004)
