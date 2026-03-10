"""
🤖 AgenteMaestro — Servidor do Painel Web
==========================================
Servidor FastAPI que conecta o painel web aos agentes Agno.
Cada agente já tem suas APIs configuradas — este servidor
atua como gateway unificado.

Uso:
    python painel/server.py
    Acesse: http://localhost:8080
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Adicionar raiz do projeto ao path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ============================================================
# IMPORTAR AGENTES
# ============================================================
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
from agno.memory.v2 import Memory
from agno.memory.db.sqlite import SqliteMemoryDb

os.makedirs("tmp", exist_ok=True)

# ============================================================
# CRIAR AGENTES
# ============================================================

# ============================================================
# CONFIGURAÇÃO OPENROUTER
# ============================================================
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_model(model_id: str):
    """Retorna um modelo configurado para OpenRouter"""
    return OpenAIChat(
        id=model_id,
        api_key=OPENROUTER_KEY,
        base_url=OPENROUTER_BASE_URL,
        # OpenRouter exige headers específicos para identificação
        extra_headers={
            "HTTP-Referer": "https://agentes-ia-agno.vercel.app", 
            "X-Title": "AgenteMaestro Portal"
        }
    )

# Banco de memória compartilhado
memory = Memory(
    db=SqliteMemoryDb(table_name="painel_memory", db_file="tmp/painel.db"),
    model=get_model("openai/gpt-4o-mini"),
)

def criar_storage(nome: str) -> SqliteDb:
    return SqliteDb(table_name=f"painel_{nome}", db_file="tmp/painel.db")


# 1. AgenteMaestro
maestro = Agent(
    name="AgenteMaestro",
    model=get_model("openai/gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description="Agente central autônomo do projeto Toca da Onça.",
    instructions=[
        "Você é o AgenteMaestro — agente autônomo e versátil.",
        "Use DuckDuckGoTools para pesquisar e YFinanceTools para dados financeiros.",
        "Use tabelas para dados numéricos.",
        "Sempre cite fontes quando pesquisar na web.",
        "Responda SEMPRE em português brasileiro.",
    ],
    storage=criar_storage("maestro"),
    memory=memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=5,
    markdown=True,
)

# 2. Pesquisador
pesquisador = Agent(
    name="Pesquisador",
    model=get_model("google/gemini-2.0-flash-001"),
    tools=[DuckDuckGoTools()],
    description="Pesquisador que busca, valida e organiza informações.",
    instructions=[
        "Você é um pesquisador profissional. Sempre pesquise ANTES de responder.",
        "SEMPRE cite fontes com nome e URL.",
        "Organize: resumo → detalhes → fontes.",
        "Responda em português brasileiro.",
    ],
    storage=criar_storage("pesquisador"),
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

# 3. Analista Financeiro
analista = Agent(
    name="Analista Financeiro",
    model=get_model("meta-llama/llama-3.3-70b-instruct"),
    tools=[DuckDuckGoTools()],
    description="Analista financeiro especializado em ações e mercado.",
    instructions=[
        "Use SEMPRE tabelas para dados numéricos.",
        "Mostre: preço, variação, P/L, ROE, recomendações.",
        "Nunca dê conselho direto de investimento.",
        "Responda em português brasileiro.",
    ],
    storage=criar_storage("analista"),
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

# 4. Multifunções
multifuncoes = Agent(
    name="Multifunções",
    model=get_model("openai/gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description="Agente versátil para conversões, cálculos e tarefas gerais.",
    instructions=[
        "Você é um assistente versátil para cálculos, conversões e tarefas gerais.",
        "Arredonde valores para 2 casas decimais.",
        "Mostre fórmulas usadas nos cálculos.",
        "Responda em português brasileiro.",
    ],
    storage=criar_storage("multifuncoes"),
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

# 5. Agente PDF (sem knowledge base neste contexto, mas funcional)
pdf_agent = Agent(
    name="Agente de PDF",
    model=get_model("openai/gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description="Especialista em análise de documentos.",
    instructions=[
        "Você é um especialista em análise documental.",
        "Organize resumos: Tema → Pontos-Chave → Conclusão.",
        "Chame o usuário de 'senhor'.",
        "Responda em português brasileiro.",
    ],
    storage=criar_storage("pdf"),
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

# 6. Memória
memoria = Agent(
    name="Memória",
    model=get_model("openai/gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description="Assistente com memória persistente entre conversas.",
    instructions=[
        "Consulte SEMPRE sua memória antes de responder.",
        "Na primeira mensagem, pergunte o nome do usuário se não souber.",
        "Salve nome, projetos e preferências na memória.",
        "Chame pelo nome quando souber. Seja natural.",
        "Responda em português brasileiro.",
    ],
    storage=criar_storage("memoria"),
    memory=memory,
    enable_agentic_memory=True,
    add_history_to_messages=True,
    num_history_runs=5,
    markdown=True,
)

# 7. Teams (agente multilingual simples)
teams = Agent(
    name="Time Multilingual",
    model=get_model("openai/gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    description="Responde em 4 idiomas: PT, EN, ES, FR.",
    instructions=[
        "Detecte o idioma da mensagem e responda no MESMO idioma.",
        "Idiomas suportados: Português, English, Español, Français.",
        "Se idioma não for suportado, responda em inglês.",
        "Seja amigável e profissional.",
    ],
    storage=criar_storage("teams"),
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

# Mapeamento de agentes
AGENTS = {
    "maestro": maestro,
    "pesquisador": pesquisador,
    "analista": analista,
    "multifuncoes": multifuncoes,
    "pdf": pdf_agent,
    "memoria": memoria,
    "teams": teams,
}

# ============================================================
# SERVIDOR FASTAPI
# ============================================================
app = FastAPI(title="AgenteMaestro Painel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos do painel
PAINEL_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(PAINEL_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    """Servir o painel HTML"""
    html_path = PAINEL_DIR / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "ok",
        "agents": list(AGENTS.keys()),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/chat")
async def chat(request: Request):
    """Endpoint de chat — recebe mensagem e retorna resposta do agente"""
    try:
        body = await request.json()
        message = body.get("message", "")
        agent_id = body.get("agent", "maestro")
        session_id = body.get("session_id", "default")

        if not message:
            return JSONResponse(
                status_code=400,
                content={"error": "Mensagem vazia"}
            )

        agent = AGENTS.get(agent_id)
        if not agent:
            return JSONResponse(
                status_code=404,
                content={"error": f"Agente '{agent_id}' não encontrado"}
            )

        # Executar agente
        response = agent.run(message, session_id=session_id)

        # Extrair texto da resposta
        response_text = ""
        if hasattr(response, 'content'):
            response_text = response.content
        elif hasattr(response, 'messages') and response.messages:
            for msg in reversed(response.messages):
                if hasattr(msg, 'content') and msg.content and msg.role == 'assistant':
                    response_text = msg.content
                    break
        else:
            response_text = str(response)

        return {
            "response": response_text,
            "agent": agent_id,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/agents")
async def list_agents():
    """Listar agentes disponíveis"""
    return {
        "agents": [
            {
                "id": k,
                "name": v.name,
                "description": v.description,
            }
            for k, v in AGENTS.items()
        ]
    }


# ============================================================
# INICIAR
# ============================================================
if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  🤖 AgenteMaestro — Painel de Controle")
    print("=" * 50)
    print()
    print(f"  🌐 Abra no navegador: http://localhost:8080")
    print(f"  📡 API: http://localhost:8080/health")
    print(f"  🤖 Agentes: {', '.join(AGENTS.keys())}")
    print()
    print("  Pressione Ctrl+C para parar")
    print("=" * 50)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
