"""
AgenteMaestro - Ponto de entrada
Inicia o painel web na porta 8000.
Acesse: http://localhost:8000
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from agno.playground import Playground, serve_playground_app
from agent import maestro

porta = int(os.getenv("AGENTE_PORTA", "8000"))

app = Playground(agents=[maestro]).get_app()

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════╗
║       🤖  AGENTE MAESTRO  🤖         ║
║                                      ║
║  Painel Web: http://localhost:{porta}  ║
║  Pressione CTRL+C para parar         ║
╚══════════════════════════════════════╝
    """)
    serve_playground_app("main:app", reload=True, port=porta)
