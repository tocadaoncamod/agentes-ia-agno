"""
AgenteMaestro - Agente autônomo com auto-melhoria
Tem acesso total a Python, VS Code, criação de agentes e skills.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

# Importa ferramentas customizadas
sys.path.insert(0, str(Path(__file__).parent))
from tools.python_executor import executar_python, instalar_pacote, listar_pacotes, executar_comando_shell
from tools.vscode_tool import abrir_vscode, criar_arquivo, ler_arquivo, abrir_arquivo, listar_arquivos
from tools.agent_factory import criar_novo_agente, listar_agentes_criados, carregar_agente
from tools.skill_manager import listar_skills_disponiveis, adicionar_skill, descrever_skill

# Diretório de memória
MEMORY_DIR = Path(__file__).parent / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

# Memória persistente - lembra o usuário entre sessões
memory = Memory(
    model=OpenAIChat(id="gpt-4.1-mini"),
    db=SqliteMemoryDb(
        table_name="maestro_memory",
        db_file=str(MEMORY_DIR / "maestro.db")
    ),
)

# Storage de sessão
storage = SqliteStorage(
    table_name="maestro_sessions",
    db_file=str(MEMORY_DIR / "maestro.db")
)

# Modelo principal
modelo = os.getenv("AGENTE_MODELO", "gpt-4.1-mini")

# === O AGENTE MAESTRO ===
maestro = Agent(
    name="AgenteMaestro",
    model=OpenAIChat(id=modelo),

    description=(
        "Sou o AgenteMaestro — agente autônomo central com acesso total ao Python, VS Code, "
        "skills especializadas e capacidade de criar novos agentes sob demanda."
    ),

    instructions=[
        "Você é o AgenteMaestro — agente desenvolvedor autônomo de IA.",
        "Você tem acesso TOTAL ao Python — escreva e execute qualquer código.",
        "Crie novos agentes com criar_novo_agente() — defina nome, descrição e instruções detalhadas.",
        "Abra e edite arquivos no VS Code com abrir_arquivo() e criar_arquivo().",
        "Liste skills disponíveis com listar_skills_disponiveis() e use descrever_skill() para detalhes.",
        "Sempre teste código Python antes de entregar ao usuário.",
        "Use DuckDuckGoTools para pesquisas e YFinanceTools para dados financeiros.",
        "Seja proativo: se vir uma melhoria, implemente e explique.",
        "Consulte sua memória para personalizar respostas e lembrar projetos do usuário.",
        "Instale pacotes faltantes com instalar_pacote() antes de executar código.",
        "Use tabelas para dados numéricos e listas para pontos-chave.",
        "Responda SEMPRE em português brasileiro.",
    ],

    tools=[
        # Ferramentas de Python e Sistema
        executar_python,
        instalar_pacote,
        listar_pacotes,
        executar_comando_shell,
        # Ferramentas de VS Code e Arquivos
        abrir_vscode,
        criar_arquivo,
        ler_arquivo,
        abrir_arquivo,
        listar_arquivos,
        # Fábrica de Agentes
        criar_novo_agente,
        listar_agentes_criados,
        carregar_agente,
        # Gerenciador de Skills
        listar_skills_disponiveis,
        adicionar_skill,
        descrever_skill,
        # Ferramentas externas
        DuckDuckGoTools(),
        TavilyTools(),
        YFinanceTools(stock_price=True, company_info=True),
    ],

    # Memória e histórico
    memory=memory,
    enable_agentic_memory=True,
    storage=storage,
    add_history_to_messages=True,
    num_history_runs=10,

    # Configurações de resposta
    markdown=True,
    show_tool_calls=True,
)
