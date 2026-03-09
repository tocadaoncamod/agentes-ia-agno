"""
Gerenciador de Skills - adiciona novas capacidades ao AgenteMaestro dinamicamente.
Inspirado em skills.sh - catálogo de habilidades para agentes IA.
"""
import json
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"
SKILLS_DIR.mkdir(exist_ok=True)

# Catálogo de skills disponíveis (compatíveis com Agno)
CATALOGO_SKILLS = {
    "web_search": {
        "nome": "Busca na Web",
        "descricao": "Pesquisa informações atuais na internet",
        "import": "from agno.tools.tavily import TavilyTools",
        "uso": "TavilyTools()",
        "requer": ["TAVILY_API_KEY"]
    },
    "financeiro": {
        "nome": "Dados Financeiros",
        "descricao": "Cotações de ações, criptos e dados de mercado",
        "import": "from agno.tools.yfinance import YFinanceTools",
        "uso": "YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)",
        "requer": []
    },
    "calculadora": {
        "nome": "Calculadora",
        "descricao": "Cálculos matemáticos avançados",
        "import": "from agno.tools.calculator import CalculatorTools",
        "uso": "CalculatorTools()",
        "requer": []
    },
    "email": {
        "nome": "Email",
        "descricao": "Enviar e receber emails",
        "import": "from agno.tools.email import EmailTools",
        "uso": "EmailTools()",
        "requer": ["EMAIL_ADDRESS", "EMAIL_PASSWORD"]
    },
    "github": {
        "nome": "GitHub",
        "descricao": "Criar repos, commits, PRs e ler código",
        "import": "from agno.tools.github import GithubTools",
        "uso": "GithubTools()",
        "requer": ["GITHUB_ACCESS_TOKEN"]
    },
    "arxiv": {
        "nome": "ArXiv Papers",
        "descricao": "Buscar e ler artigos científicos",
        "import": "from agno.tools.arxiv import ArxivTools",
        "uso": "ArxivTools()",
        "requer": []
    },
    "duckduckgo": {
        "nome": "DuckDuckGo",
        "descricao": "Busca na web sem API key",
        "import": "from agno.tools.duckduckgo import DuckDuckGoTools",
        "uso": "DuckDuckGoTools()",
        "requer": []
    },
    "python": {
        "nome": "Execução Python",
        "descricao": "Escrever e executar código Python",
        "import": "from agno.tools.python import PythonTools",
        "uso": "PythonTools()",
        "requer": []
    },
    "shell": {
        "nome": "Shell/Terminal",
        "descricao": "Executar comandos no terminal",
        "import": "from agno.tools.shell import ShellTools",
        "uso": "ShellTools()",
        "requer": []
    },
    "wikipedia": {
        "nome": "Wikipedia",
        "descricao": "Buscar informações na Wikipedia",
        "import": "from agno.tools.wikipedia import WikipediaTools",
        "uso": "WikipediaTools()",
        "requer": []
    },
    "sql": {
        "nome": "Banco de Dados SQL",
        "descricao": "Criar e consultar bancos SQLite",
        "import": "from agno.tools.sql import SQLTools",
        "uso": "SQLTools(db_url='sqlite:///database.db')",
        "requer": []
    },
    "pdf": {
        "nome": "Leitura de PDF",
        "descricao": "Ler, analisar e extrair texto de PDFs",
        "import": "from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader",
        "uso": "PDFKnowledgeBase(path='arquivo.pdf', vector_db=ChromaDb(...))",
        "requer": []
    },
    "imagem_ai": {
        "nome": "Geração de Imagens IA",
        "descricao": "Gerar imagens com DALL-E 3",
        "import": "from agno.tools.dalle import DalleTools",
        "uso": "DalleTools(model='dall-e-3', size='1024x1024')",
        "requer": ["OPENAI_API_KEY"]
    },
    "whatsapp": {
        "nome": "WhatsApp",
        "descricao": "Enviar mensagens via WhatsApp Business API",
        "import": "# Usar requests com WhatsApp Cloud API",
        "uso": "# Implementar CustomTool com WhatsApp API",
        "requer": ["WHATSAPP_TOKEN", "WHATSAPP_PHONE_ID"]
    },
    "supabase": {
        "nome": "Supabase Database",
        "descricao": "Ler e escrever no banco Supabase",
        "import": "from supabase import create_client",
        "uso": "# CustomTool com supabase-py",
        "requer": ["SUPABASE_URL", "SUPABASE_KEY"]
    }
}


def listar_skills_disponiveis() -> str:
    """
    Lista todas as skills disponíveis para adicionar ao agente.

    Returns:
        Catálogo completo de skills
    """
    resultado = ["🛠️  Skills disponíveis para o AgenteMaestro:\n"]
    for key, skill in CATALOGO_SKILLS.items():
        requer = f" (requer: {', '.join(skill['requer'])})" if skill['requer'] else " (sem API key)"
        resultado.append(f"  [{key}] {skill['nome']}{requer}\n    → {skill['descricao']}")
    return "\n".join(resultado)


def descrever_skill(nome_skill: str) -> str:
    """
    Retorna detalhes completos de como usar uma skill específica.

    Args:
        nome_skill: Chave da skill (ex: 'financeiro', 'github')

    Returns:
        Detalhes de implementação
    """
    if nome_skill not in CATALOGO_SKILLS:
        disponiveis = ", ".join(CATALOGO_SKILLS.keys())
        return f"❌ Skill '{nome_skill}' não encontrada.\nDisponíveis: {disponiveis}"

    s = CATALOGO_SKILLS[nome_skill]
    return (
        f"🔧 Skill: {s['nome']}\n"
        f"📝 Descrição: {s['descricao']}\n"
        f"📦 Import: {s['import']}\n"
        f"⚙️  Uso: tools=[{s['uso']}]\n"
        f"🔑 Requer: {', '.join(s['requer']) if s['requer'] else 'Nada'}"
    )


def adicionar_skill(nome_skill: str, codigo_personalizado: str = "") -> str:
    """
    Adiciona uma nova skill ao catálogo personalizado do AgenteMaestro.

    Args:
        nome_skill: Nome único da skill
        codigo_personalizado: Código Python da skill customizada

    Returns:
        Confirmação
    """
    skill_path = SKILLS_DIR / f"{nome_skill}.py"
    if codigo_personalizado:
        skill_path.write_text(codigo_personalizado, encoding='utf-8')
        return f"✅ Skill '{nome_skill}' adicionada em: {skill_path}"
    elif nome_skill in CATALOGO_SKILLS:
        s = CATALOGO_SKILLS[nome_skill]
        codigo = f"# Skill: {s['nome']}\n# {s['descricao']}\n{s['import']}\n\n# Uso: tools=[{s['uso']}]\n"
        skill_path.write_text(codigo, encoding='utf-8')
        return f"✅ Skill '{nome_skill}' salva em: {skill_path}"
    else:
        return f"❌ Skill '{nome_skill}' não encontrada no catálogo."
