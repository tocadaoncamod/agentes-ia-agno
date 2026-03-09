# ============================================================
# NÍVEL 3 - Agente com Ferramentas Próprias
# MELHORIAS: mais ferramentas custom, melhor descrição,
#            storage, dotenv carregado, porta explícita
# ============================================================
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("tmp", exist_ok=True)


# === FERRAMENTAS CUSTOMIZADAS ===

def celsius_para_fahrenheit(temperatura_celsius: float) -> float:
    """
    Converte temperatura de Celsius para Fahrenheit.

    Args:
        temperatura_celsius: Temperatura em graus Celsius

    Returns:
        Temperatura em Fahrenheit
    """
    return (temperatura_celsius * 9 / 5) + 32


def fahrenheit_para_celsius(temperatura_fahrenheit: float) -> float:
    """
    Converte temperatura de Fahrenheit para Celsius.

    Args:
        temperatura_fahrenheit: Temperatura em graus Fahrenheit

    Returns:
        Temperatura em Celsius
    """
    return (temperatura_fahrenheit - 32) * 5 / 9


def calcular_variacao_percentual(valor_anterior: float, valor_atual: float) -> str:
    """
    Calcula a variação percentual entre dois valores.

    Args:
        valor_anterior: Valor inicial
        valor_atual: Valor final

    Returns:
        String com a variação percentual formatada
    """
    if valor_anterior == 0:
        return "Erro: valor anterior não pode ser zero"
    variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
    sinal = "+" if variacao >= 0 else ""
    return f"{sinal}{variacao:.2f}%"


def converter_moeda_brl(valor_usd: float, taxa_cambio: float = 5.70) -> str:
    """
    Converte valor em dólares para reais brasileiros.

    Args:
        valor_usd: Valor em dólares americanos
        taxa_cambio: Taxa de câmbio USD/BRL (padrão: 5.70)

    Returns:
        Valor convertido em reais
    """
    valor_brl = valor_usd * taxa_cambio
    return f"R$ {valor_brl:.2f} (taxa: {taxa_cambio})"


# === AGENTE ===

db = SqliteStorage(table_name="own_tools_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente Multifunções",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[
        TavilyTools(),
        DuckDuckGoTools(),
        celsius_para_fahrenheit,
        fahrenheit_para_celsius,
        calcular_variacao_percentual,
        converter_moeda_brl,
    ],
    description="Agente versátil com ferramentas de conversão, câmbio, clima e cálculos utilitários.",
    instructions=[
        "Você é um assistente com ferramentas especializadas. Escolha a ferramenta certa para cada tarefa.",
        "Para temperatura: use as funções de conversão e sempre mostre °C e °F lado a lado.",
        "Para câmbio: busque a taxa de câmbio atualizada na web antes de converter.",
        "Para variações: calcule a variação percentual e apresente em tabela quando houver múltiplos valores.",
        "Quando usar ferramentas de pesquisa (Tavily/DuckDuckGo), cite as fontes.",
        "Arredonde valores numéricos para 2 casas decimais.",
        "Mostre a fórmula usada quando fizer cálculos, para transparência.",
        "Responda sempre em português brasileiro.",
    ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("13_own_tools:app", reload=True, port=8001)
