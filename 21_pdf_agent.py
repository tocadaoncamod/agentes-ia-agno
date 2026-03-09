# ============================================================
# NÍVEL 4 - Agente de PDF com RAG (Retrieval Augmented Generation)
# CORREÇÕES: knowledge.load() automático na primeira execução,
#            criação da pasta tmp/ automática, path relativo correto
# MELHORIAS: instruções detalhadas, melhor descrição, tratamento
#            de erro se o PDF não existir
# ============================================================
from agno.agent import Agent
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

os.makedirs("tmp/chromadb", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

# === CONFIGURAÇÃO DO PDF ===
PDF_PATH = "GlobalEVOutlook2025.pdf"
CHROMA_PATH = "tmp/chromadb"

# Verifica se o PDF existe
if not Path(PDF_PATH).exists():
    print(f"⚠️  PDF não encontrado: {PDF_PATH}")
    print("   Coloque o PDF na mesma pasta e reinicie.")

# === RAG - BASE DE CONHECIMENTO ===
vector_db = ChromaDb(
    collection="pdf_agent",
    path=CHROMA_PATH,
    persistent_client=True
)

knowledge = PDFKnowledgeBase(
    path=PDF_PATH,
    vector_db=vector_db,
    reader=PDFReader(chunk=True)
)

# CORREÇÃO CRÍTICA: Detecta automaticamente se precisa carregar o PDF
# Na primeira execução carrega; nas seguintes usa o cache do ChromaDB
def carregar_conhecimento_se_necessario():
    try:
        # Tenta verificar se já tem dados no ChromaDB
        collection = vector_db._client.get_collection("pdf_agent")
        if collection.count() == 0:
            print("📚 Carregando PDF no banco de vetores (primeira vez)...")
            knowledge.load(recreate=False)
            print("✅ PDF carregado com sucesso!")
        else:
            print(f"✅ Base de conhecimento pronta ({collection.count()} chunks)")
    except Exception:
        print("📚 Carregando PDF...")
        knowledge.load(recreate=False)

carregar_conhecimento_se_necessario()

# === AGENTE ===
db = SqliteStorage(table_name="pdf_agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-4.1-mini"),
    storage=db,
    knowledge=knowledge,
    description="Especialista em análise de documentos PDF com busca semântica (RAG). Responde perguntas, resume e extrai dados.",
    instructions=[
        "Você é um especialista em análise documental. SEMPRE busque no documento antes de responder.",
        "Cite o trecho relevante do documento usando blockquotes: > 'trecho...'",
        "Se a informação NÃO está no documento, diga claramente: 'Essa informação não consta no documento.'",
        "Para resumos: use o formato — Tema Principal → Pontos-Chave → Dados → Conclusão.",
        "Para dados numéricos: extraia e organize em tabelas sempre que possível.",
        "Se a pergunta é ampla, faça múltiplas buscas com termos diferentes no documento.",
        "Chame o usuário de 'senhor' e mantenha tom respeitoso e profissional.",
        "Organize respostas longas com títulos (##) e tópicos.",
        "Responda em português brasileiro.",
    ],
    add_history_to_messages=True,
    search_knowledge=True,
    num_history_runs=3,
    markdown=True,
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("21_pdf_agent:app", reload=True, port=8002)
