"""
Integração com VS Code - o agente pode criar, editar e abrir arquivos diretamente.
"""
import subprocess
import os
from pathlib import Path


WORKSPACE = Path(os.getenv("WORKSPACE_PATH", ".")).resolve()


def abrir_vscode(caminho: str = ".") -> str:
    """
    Abre o VS Code em um caminho específico ou no projeto atual.

    Args:
        caminho: Pasta ou arquivo para abrir (padrão: pasta atual)

    Returns:
        Confirmação
    """
    try:
        path = Path(caminho).resolve() if caminho != "." else WORKSPACE
        subprocess.Popen(
            ["code", str(path)],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        return f"✅ VS Code aberto em: {path}"
    except FileNotFoundError:
        return "❌ VS Code não encontrado. Instale e adicione 'code' ao PATH."
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def criar_arquivo(caminho: str, conteudo: str) -> str:
    """
    Cria ou sobrescreve um arquivo com o conteúdo fornecido.

    Args:
        caminho: Caminho do arquivo (relativo ao workspace)
        conteudo: Conteúdo do arquivo

    Returns:
        Confirmação com o path completo
    """
    try:
        path = Path(caminho)
        if not path.is_absolute():
            path = WORKSPACE / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(conteudo, encoding='utf-8')
        return f"✅ Arquivo criado: {path}\n   Tamanho: {len(conteudo)} chars"
    except Exception as e:
        return f"❌ Erro ao criar arquivo: {str(e)}"


def ler_arquivo(caminho: str) -> str:
    """
    Lê o conteúdo de um arquivo.

    Args:
        caminho: Caminho do arquivo

    Returns:
        Conteúdo do arquivo
    """
    try:
        path = Path(caminho)
        if not path.is_absolute():
            path = WORKSPACE / path
        if not path.exists():
            return f"❌ Arquivo não encontrado: {path}"
        conteudo = path.read_text(encoding='utf-8')
        return f"📄 {path}\n{'='*50}\n{conteudo}"
    except Exception as e:
        return f"❌ Erro ao ler arquivo: {str(e)}"


def abrir_arquivo(caminho: str) -> str:
    """
    Abre um arquivo específico no VS Code.

    Args:
        caminho: Caminho do arquivo

    Returns:
        Confirmação
    """
    try:
        path = Path(caminho)
        if not path.is_absolute():
            path = WORKSPACE / path
        subprocess.Popen(
            ["code", str(path)],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        return f"✅ Arquivo aberto no VS Code: {path}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def listar_arquivos(pasta: str = ".") -> str:
    """
    Lista arquivos e pastas em um diretório.

    Args:
        pasta: Pasta a listar (padrão: workspace)

    Returns:
        Árvore de arquivos
    """
    try:
        path = Path(pasta)
        if not path.is_absolute():
            path = WORKSPACE / path
        if not path.exists():
            return f"❌ Pasta não encontrada: {path}"

        resultado = [f"📁 {path}"]
        for item in sorted(path.iterdir()):
            if item.name.startswith('.') or item.name == '__pycache__':
                continue
            icon = "📁" if item.is_dir() else "📄"
            resultado.append(f"  {icon} {item.name}")
        return "\n".join(resultado)
    except Exception as e:
        return f"❌ Erro: {str(e)}"
