"""
Ferramentas para execução de Python com acesso total.
O AgenteMaestro pode escrever e executar qualquer código Python.
"""
import subprocess
import sys
import os
import tempfile
from pathlib import Path


def executar_python(codigo: str, timeout: int = 60) -> str:
    """
    Executa código Python e retorna o resultado completo (stdout + stderr).

    Args:
        codigo: Código Python a ser executado
        timeout: Tempo máximo em segundos (padrão: 60)

    Returns:
        String com a saída do código
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(codigo)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )
        saida = ""
        if result.stdout:
            saida += f"✅ SAÍDA:\n{result.stdout}"
        if result.stderr:
            saida += f"\n⚠️ STDERR:\n{result.stderr}"
        if result.returncode != 0:
            saida += f"\n❌ Código de retorno: {result.returncode}"
        return saida or "✅ Executado sem saída."
    except subprocess.TimeoutExpired:
        return f"❌ Timeout: o código demorou mais de {timeout} segundos."
    except Exception as e:
        return f"❌ Erro ao executar: {str(e)}"
    finally:
        os.unlink(tmp_path)


def instalar_pacote(nome_pacote: str) -> str:
    """
    Instala um pacote Python usando pip.

    Args:
        nome_pacote: Nome do pacote (ex: 'requests', 'pandas==2.0.0')

    Returns:
        Resultado da instalação
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', nome_pacote, '--quiet'],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return f"✅ Pacote '{nome_pacote}' instalado com sucesso!"
        else:
            return f"❌ Erro ao instalar '{nome_pacote}':\n{result.stderr}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def listar_pacotes() -> str:
    """
    Lista todos os pacotes Python instalados no ambiente.

    Returns:
        Lista de pacotes instalados
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=columns'],
            capture_output=True,
            text=True
        )
        return f"📦 Pacotes instalados:\n{result.stdout}"
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def executar_comando_shell(comando: str, timeout: int = 30) -> str:
    """
    Executa um comando no terminal do sistema.

    Args:
        comando: Comando a executar (ex: 'git status', 'dir', 'ls')
        timeout: Tempo máximo em segundos

    Returns:
        Saída do comando
    """
    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        saida = result.stdout or ""
        erro = result.stderr or ""
        if saida and erro:
            return f"✅ {saida}\n⚠️ {erro}"
        return saida or erro or "✅ Comando executado sem saída."
    except subprocess.TimeoutExpired:
        return f"❌ Timeout após {timeout}s"
    except Exception as e:
        return f"❌ Erro: {str(e)}"
