"""
Fábrica de agentes - o AgenteMaestro pode criar novos agentes especializados.
"""
import json
import os
from pathlib import Path
from datetime import datetime

AGENTS_DIR = Path(__file__).parent.parent / "agents_criados"
AGENTS_DIR.mkdir(exist_ok=True)

TEMPLATE_AGENTE = '''"""
Agente: {nome}
Criado em: {data}
Descrição: {descricao}
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

import os, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

db = SqliteStorage(table_name="{nome_slug}_session", db_file="../memory/agentes.db")

agent = Agent(
    name="{nome}",
    model=OpenAIChat(id=os.getenv("AGENTE_MODELO", "gpt-4.1-mini")),
    description="{descricao}",
    instructions={instrucoes},
    tools={ferramentas},
    storage=db,
    add_history_to_messages=True,
    num_history_runs=5,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("{arquivo}:app", reload=True, port={porta})
'''


def criar_novo_agente(
    nome: str,
    descricao: str,
    instrucoes: list[str],
    ferramentas: list[str] | None = None,
    porta: int = 8001
) -> str:
    """
    Cria um novo agente especializado com código Python gerado automaticamente.

    Args:
        nome: Nome do agente (ex: 'Agente de Vendas')
        descricao: O que esse agente faz
        instrucoes: Lista de instruções de comportamento
        ferramentas: Lista de ferramentas (ex: ['TavilyTools()'])
        porta: Porta do servidor web (padrão: 8001)

    Returns:
        Caminho do arquivo criado e instruções de uso
    """
    if ferramentas is None:
        ferramentas = ["TavilyTools()"]

    nome_slug = nome.lower().replace(" ", "_").replace("-", "_")
    arquivo = f"agente_{nome_slug}"
    filepath = AGENTS_DIR / f"{arquivo}.py"

    instrucoes_str = json.dumps(instrucoes, ensure_ascii=False)
    ferramentas_str = "[" + ", ".join(ferramentas) + "]"

    codigo = TEMPLATE_AGENTE.format(
        nome=nome,
        nome_slug=nome_slug,
        descricao=descricao,
        instrucoes=instrucoes_str,
        ferramentas=ferramentas_str,
        arquivo=arquivo,
        porta=porta,
        data=datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    filepath.write_text(codigo, encoding='utf-8')

    # Salvar metadados
    meta = {
        "nome": nome,
        "descricao": descricao,
        "arquivo": str(filepath),
        "porta": porta,
        "criado_em": datetime.now().isoformat()
    }
    meta_path = AGENTS_DIR / f"{arquivo}.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    return (
        f"✅ Agente '{nome}' criado!\n"
        f"   📄 Arquivo: {filepath}\n"
        f"   🌐 Porta: {porta}\n"
        f"   ▶️  Para iniciar: cd agents_criados && python {arquivo}.py"
    )


def listar_agentes_criados() -> str:
    """
    Lista todos os agentes criados pelo AgenteMaestro.

    Returns:
        Lista formatada de agentes
    """
    agentes = list(AGENTS_DIR.glob("*.json"))
    if not agentes:
        return "📭 Nenhum agente criado ainda."

    resultado = ["🤖 Agentes criados:"]
    for meta_file in sorted(agentes):
        try:
            meta = json.loads(meta_file.read_text(encoding='utf-8'))
            resultado.append(
                f"\n  • {meta['nome']}\n"
                f"    📝 {meta['descricao']}\n"
                f"    🌐 Porta {meta['porta']} | 📅 {meta['criado_em'][:10]}"
            )
        except Exception:
            continue
    return "\n".join(resultado)


def carregar_agente(nome: str) -> str:
    """
    Retorna o código Python de um agente já criado.

    Args:
        nome: Nome do agente

    Returns:
        Código fonte do agente
    """
    nome_slug = nome.lower().replace(" ", "_").replace("-", "_")
    arquivo = AGENTS_DIR / f"agente_{nome_slug}.py"
    if not arquivo.exists():
        return f"❌ Agente '{nome}' não encontrado."
    return arquivo.read_text(encoding='utf-8')
