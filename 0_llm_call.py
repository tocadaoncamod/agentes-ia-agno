# ============================================================
# NÍVEL 0 - Chamada direta ao LLM (sem agente)
# CORREÇÕES: resposta agora é impressa + tratamento de erro
# + suporte a OpenAI e Groq com seleção fácil
# ============================================================
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.models.message import Message
from dotenv import load_dotenv

load_dotenv()


def chamar_modelo(texto: str, usar_openai: bool = False) -> str:
    """Chama o LLM e retorna a resposta como string."""
    try:
        model = OpenAIChat(id="gpt-4.1-mini") if usar_openai else Groq(id="llama-3.3-70b-versatile")
        msg = Message(role="user", content=[{"type": "text", "text": texto}])
        response = model.invoke([msg])
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erro ao chamar modelo: {e}"


if __name__ == "__main__":
    # --- TESTE COM GROQ (gratuito) ---
    pergunta = "Olá! Me diga qual é a capital do Brasil em uma linha."
    resposta = chamar_modelo(pergunta)
    print(f"[Groq] {resposta}")

    # --- DESCOMENTE para testar OpenAI ---
    # resposta = chamar_modelo("Quanto é 2+2?", usar_openai=True)
    # print(f"[OpenAI] {resposta}")
