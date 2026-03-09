# ============================================================
# AGENTE MAESTRO — Agente central com auto-melhoria
# Executa Python, cria agentes, usa 17 skills instaladas,
# lembra tudo entre conversas.
# Painel web: http://localhost:8000
# ============================================================

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import subprocess, sys, os, tempfile, json
from pathlib import Path

load_dotenv()
os.makedirs("tmp", exist_ok=True)
os.makedirs("agentes_criados", exist_ok=True)

# ============================================================
# DIRETÓRIO DAS SKILLS
# ============================================================
SKILLS_DIR = Path(__file__).parent / ".agent" / "skills"


# ============================================================
# FERRAMENTAS: PYTHON E SISTEMA
# ============================================================

def executar_python(codigo: str, timeout: int = 60) -> str:
    """
    Escreve e executa código Python. Retorna stdout e stderr.

    Args:
        codigo: Código Python para executar
        timeout: Tempo limite em segundos (padrão 60)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(codigo)
        tmp = f.name
    try:
        r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=timeout)
        out = (f"✅ SAÍDA:\n{r.stdout}" if r.stdout else "") + \
              (f"\n⚠️ ERROS:\n{r.stderr}" if r.stderr else "")
        return out or "✅ Executado sem saída."
    except subprocess.TimeoutExpired:
        return f"❌ Timeout de {timeout}s atingido."
    except Exception as e:
        return f"❌ Erro: {e}"
    finally:
        os.unlink(tmp)


def executar_comando(comando: str) -> str:
    """
    Executa um comando no terminal (shell).

    Args:
        comando: Comando a executar (ex: 'pip list', 'dir', 'ls -la')
    """
    try:
        r = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        return (f"✅ SAÍDA:\n{r.stdout}" if r.stdout else "") + \
               (f"\n⚠️ ERROS:\n{r.stderr}" if r.stderr else "") or "✅ Comando executado."
    except subprocess.TimeoutExpired:
        return "❌ Timeout de 60s atingido."
    except Exception as e:
        return f"❌ Erro: {e}"


def instalar_pacote(pacote: str) -> str:
    """
    Instala um pacote Python com pip.

    Args:
        pacote: Nome do pacote (ex: 'pandas', 'requests==2.31.0')
    """
    try:
        r = subprocess.run([sys.executable, "-m", "pip", "install", pacote],
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            return f"✅ Pacote '{pacote}' instalado com sucesso!"
        return f"❌ Erro ao instalar '{pacote}':\n{r.stderr}"
    except Exception as e:
        return f"❌ Erro: {e}"


# ============================================================
# FERRAMENTAS: ARQUIVOS E VS CODE
# ============================================================

def criar_arquivo(caminho: str, conteudo: str) -> str:
    """
    Cria ou sobrescreve um arquivo com o conteúdo fornecido.

    Args:
        caminho: Caminho do arquivo (ex: 'meu_script.py', 'pasta/arquivo.txt')
        conteudo: Conteúdo a escrever no arquivo
    """
    try:
        p = Path(caminho)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding='utf-8')
        return f"✅ Arquivo '{caminho}' criado ({len(conteudo)} chars)."
    except Exception as e:
        return f"❌ Erro: {e}"


def ler_arquivo(caminho: str) -> str:
    """
    Lê o conteúdo de um arquivo.

    Args:
        caminho: Caminho do arquivo a ler
    """
    try:
        p = Path(caminho)
        if not p.exists():
            return f"❌ Arquivo '{caminho}' não encontrado."
        return p.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return f"❌ Erro: {e}"


def listar_arquivos(pasta: str = ".") -> str:
    """
    Lista arquivos e pastas em um diretório.

    Args:
        pasta: Caminho da pasta (padrão: pasta atual)
    """
    try:
        p = Path(pasta)
        if not p.exists():
            return f"❌ Pasta '{pasta}' não encontrada."
        itens = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        linhas = [f"📁 {pasta}:"]
        for item in itens:
            icon = "📄" if item.is_file() else "📂"
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            linhas.append(f"  {icon} {item.name}{size}")
        return "\n".join(linhas)
    except Exception as e:
        return f"❌ Erro: {e}"


def abrir_vscode(caminho: str = ".") -> str:
    """
    Abre um arquivo ou pasta no VS Code.

    Args:
        caminho: Caminho do arquivo ou pasta (padrão: pasta atual)
    """
    try:
        subprocess.Popen(["code", caminho], shell=True)
        return f"✅ VS Code aberto em: {caminho}"
    except Exception as e:
        return f"❌ Erro ao abrir VS Code: {e}\nDica: certifique-se que o VS Code está instalado e 'code' está no PATH."


# ============================================================
# FERRAMENTAS: CRIAR AGENTES
# ============================================================

agentes_criados = []

def criar_agente(nome: str, descricao: str, instrucoes: list, porta: int = 9000) -> str:
    """
    Cria um novo agente especializado e salva o código em agentes_criados/.

    Args:
        nome: Nome do agente (ex: 'AgenteVendas')
        descricao: Descrição do que o agente faz
        instrucoes: Lista de instruções para o agente
        porta: Porta do servidor (padrão 9000)
    """
    codigo = f'''# Agente: {nome}
# {descricao}
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv

load_dotenv()

agente = Agent(
    name="{nome}",
    model=OpenAIChat(id="gpt-4.1-mini"),
    description="{descricao}",
    instructions={json.dumps(instrucoes, ensure_ascii=False)},
    tools=[DuckDuckGoTools()],
    markdown=True,
    show_tool_calls=True,
)

app = Playground(agents=[agente]).get_app()

if __name__ == "__main__":
    print("🤖 {nome} rodando em http://localhost:{porta}")
    serve_playground_app("{nome.lower()}:app", port={porta}, reload=True)
'''
    caminho = f"agentes_criados/{nome}.py"
    Path("agentes_criados").mkdir(exist_ok=True)
    Path(caminho).write_text(codigo, encoding='utf-8')
    agentes_criados.append(type('Agente', (), {'name': nome})())
    return f"✅ Agente '{nome}' criado em {caminho}!\nRode com: python {caminho}"


def listar_agentes_criados() -> str:
    """Lista todos os agentes que já foram criados."""
    pasta = Path("agentes_criados")
    if not pasta.exists():
        return "📭 Nenhum agente criado ainda."
    arquivos = list(pasta.glob("*.py"))
    if not arquivos:
        return "📭 Nenhum agente criado ainda. Use criar_agente() para criar um."
    return "🤖 Agentes criados:\n" + "\n".join(f"  • {a.stem}" for a in sorted(arquivos))


# ============================================================
# FERRAMENTAS: SKILLS (lê as 17 skills instaladas)
# ============================================================

def listar_skills() -> str:
    """
    Lista todas as 17 skills instaladas e disponíveis para usar.
    Cada skill tem instruções especializadas para tarefas específicas.
    """
    if not SKILLS_DIR.exists():
        return "❌ Pasta de skills não encontrada em .claude/skills/"

    skills = []
    for pasta in sorted(SKILLS_DIR.iterdir()):
        if pasta.is_dir():
            skill_file = pasta / "SKILL.md"
            if skill_file.exists():
                # Ler frontmatter para pegar description
                conteudo = skill_file.read_text(encoding='utf-8', errors='replace')
                desc = ""
                for linha in conteudo.split('\n'):
                    if linha.startswith('description:'):
                        desc = linha.replace('description:', '').strip().strip('"').strip("'")
                        desc = desc[:80] + "..." if len(desc) > 80 else desc
                        break
                skills.append(f"  🛠️  [{pasta.name}] {desc}")

    if not skills:
        return "📭 Nenhuma skill encontrada."

    return f"📚 {len(skills)} Skills instaladas:\n" + "\n".join(skills) + \
           "\n\nUse usar_skill('nome-da-skill') para carregar as instruções de uma skill específica."


def usar_skill(nome_skill: str) -> str:
    """
    Carrega as instruções completas de uma skill específica.
    Use isto quando precisar de orientações especializadas para uma tarefa.

    Args:
        nome_skill: Nome da skill (use listar_skills() para ver as disponíveis)
                   Exemplos: 'pdf', 'docx', 'xlsx', 'pptx', 'frontend-design',
                             'mcp-builder', 'algorithmic-art', 'canvas-design',
                             'claude-api', 'webapp-testing', 'skill-creator',
                             'brand-guidelines', 'doc-coauthoring',
                             'internal-comms', 'slack-gif-creator',
                             'theme-factory', 'web-artifacts-builder'
    """
    skill_file = SKILLS_DIR / nome_skill / "SKILL.md"
    if not skill_file.exists():
        return (f"❌ Skill '{nome_skill}' não encontrada.\n"
                f"Use listar_skills() para ver as disponíveis.")

    conteudo = skill_file.read_text(encoding='utf-8', errors='replace')
    return f"📖 Skill carregada: [{nome_skill}]\n\n{conteudo}"


def criar_skill_personalizada(nome: str, descricao: str, instrucoes: str) -> str:
    """
    Cria uma nova skill personalizada e salva em .claude/skills/.

    Args:
        nome: Nome da skill (ex: 'toca-da-onca-produto')
        descricao: Quando esta skill deve ser usada
        instrucoes: Instruções detalhadas da skill em markdown
    """
    skill_dir = SKILLS_DIR / nome
    skill_dir.mkdir(parents=True, exist_ok=True)
    conteudo = f"""---
name: {nome}
description: {descricao}
---

{instrucoes}
"""
    (skill_dir / "SKILL.md").write_text(conteudo, encoding='utf-8')
    return f"✅ Skill '{nome}' criada em .claude/skills/{nome}/SKILL.md!"


# ============================================================
# CARREGAR NOMES DAS SKILLS PARA O CONTEXTO DO AGENTE
# ============================================================

def _get_skills_nomes() -> str:
    """Retorna lista de nomes das skills para incluir nas instruções."""
    if not SKILLS_DIR.exists():
        return "nenhuma skill instalada"
    nomes = [d.name for d in SKILLS_DIR.iterdir()
             if d.is_dir() and (d / "SKILL.md").exists()]
    return ", ".join(sorted(nomes))

skills_instaladas = _get_skills_nomes()


# ============================================================
# AGENTE MAESTRO
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
        extra_headers={
            "HTTP-Referer": "https://agentes-ia-agno.vercel.app",
            "X-Title": "AgenteMaestro Local"
        }
    )

memory = Memory(
    model=get_model("openai/gpt-4o-mini"),
    db=SqliteMemoryDb(table_name="maestro_memory", db_file="tmp/agent.db"),
)

storage = SqliteStorage(table_name="maestro_session", db_file="tmp/agent.db")

maestro = Agent(
    name="AgenteMaestro",
    model=get_model("openai/gpt-4o-mini"),
    description=(
        "Sou o AgenteMaestro — agente central autônomo do projeto Toca da Onça. "
        "Tenho 17 skills instaladas, posso criar agentes especializados, "
        "executar Python e criar qualquer tipo de conteúdo solicitado."
    ),
    instructions=[
        "Você é o AgenteMaestro — agente autônomo central do projeto Toca da Onça.",
        "Você tem acesso TOTAL ao Python — escreva e execute qualquer código.",
        "Você pode criar novos agentes especializados com criar_agente().",
        "",
        "=== SKILLS INSTALADAS ===",
        f"Skills disponíveis: {skills_instaladas}",
        "Use usar_skill('nome') para carregar instruções antes de tarefas especializadas:",
        "  • Pesquisa na web → usar_skill('pesquisa-web')",
        "  • Análise financeira → usar_skill('analise-financeira')",
        "  • Análise de PDF → usar_skill('analise-pdf')",
        "  • Criar agente → usar_skill('criador-agentes')",
        "  • Executar Python → usar_skill('python-executor')",
        "  • Conversões/cálculos → usar_skill('conversao-dados')",
        "  • Gestão de memória → usar_skill('memoria-contexto')",
        "  • Redigir textos → usar_skill('escrita-profissional')",
        "",
        "=== COMO TRABALHAR ===",
        "1. Antes de qualquer tarefa especializada, carregue a skill relevante",
        "2. Siga as instruções da skill para produzir resultados profissionais",
        "3. Teste todo código antes de entregar ao usuário",
        "4. Seja proativo: se vir uma melhoria, implemente e explique",
        "5. Lembre-se das preferências e projetos do usuário entre conversas",
        "6. Responda SEMPRE em português brasileiro",
        "7. Use DuckDuckGoTools para pesquisar quando precisar de informações atuais",
        "8. Use YFinanceTools para dados financeiros e cotações",
        "9. Use tabelas para dados numéricos e listas para pontos-chave",
    ],
    tools=[
        # Python e Sistema
        executar_python,
        executar_comando,
        instalar_pacote,
        # Arquivos e VS Code
        criar_arquivo,
        ler_arquivo,
        listar_arquivos,
        abrir_vscode,
        # Criação de Agentes
        criar_agente,
        listar_agentes_criados,
        # Skills (as 17 instaladas)
        listar_skills,
        usar_skill,
        criar_skill_personalizada,
        # Ferramentas externas
        DuckDuckGoTools(),
        TavilyTools(),
        YFinanceTools(stock_price=True, company_info=True),
    ],
    memory=memory,
    enable_agentic_memory=True,
    storage=storage,
    add_history_to_messages=True,
    num_history_runs=10,
    markdown=True,
    show_tool_calls=True,
)

app = Playground(agents=[maestro]).get_app()

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║         🤖  AGENTE MAESTRO  🤖               ║
║                                              ║
║  Painel web: http://localhost:8000           ║
║  17 Skills instaladas e prontas para usar!  ║
║                                              ║
║  Pressione CTRL+C para parar                 ║
╚══════════════════════════════════════════════╝
    """)
    serve_playground_app("AgenteMaestro:app", reload=True, port=8000)
