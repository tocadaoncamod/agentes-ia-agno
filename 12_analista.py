# ============================================================
# NÍVEL 2 - Agente Analista Financeiro
# CORREÇÕES: nome correto do arquivo (era 12._nalista.py)
# MELHORIAS: mais dados financeiros, recomendações, notícias,
#            instruções detalhadas, storage, Playground UI
# ============================================================
from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("tmp", exist_ok=True)

db = SqliteStorage(table_name="analista_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente Analista Financeiro",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            stock_fundamentals=True,
            income_statements=True,
            key_financial_ratios=True,
        ),
        DuckDuckGoTools(),  # Para notícias recentes sobre a empresa
    ],
    description="Analista financeiro especializado em ações, criptomoedas e mercado de capitais.",
    instructions=[
        "Você é um analista financeiro profissional. Use SEMPRE tabelas para dados numéricos.",
        "Para cada ativo, mostre: preço atual, variação do dia, mín/máx 52 semanas.",
        "Inclua indicadores fundamentalistas: P/L, EV/EBITDA, ROE, Dividend Yield.",
        "Busque recomendações dos analistas (Compra/Manter/Venda) e notícias recentes.",
        "Finalize com análise resumida: pontos positivos, riscos e visão geral.",
        "Ações brasileiras usam .SA (ex: PETR4.SA). Americanas são diretas (ex: AAPL).",
        "Se o usuário pedir comparação, faça tabela comparativa lado a lado.",
        "IMPORTANTE: Nunca dê conselho direto de investimento. Apresente dados para decisão.",
        "Informe que cotações podem ter delay de 15-20 minutos.",
        "Responda sempre em português brasileiro.",
    ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    # Modo terminal
    # agent.print_response("Analise as ações da Apple (AAPL)", stream=True)
    # agent.print_response("Compare PETR4.SA e VALE3.SA", stream=True)

    # Modo Playground
    serve_playground_app("12_analista:app", reload=True)
