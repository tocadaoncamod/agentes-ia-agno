@echo off
title AgenteMaestro - Iniciando...
color 0D
cls
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║      🤖  AGENTE MAESTRO  🤖              ║
echo  ║   Agente Autonomo com Auto-Melhoria      ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Vai para o diretório do script
cd /d "%~dp0"

:: Verifica .env
if not exist ".env" (
    echo [SETUP] Criando .env a partir do exemplo...
    copy ".env.example" ".env" >nul
    echo [AVISO] Edite o arquivo .env e adicione suas API keys!
    echo         Abrindo para editar...
    notepad .env
    pause
)

:: Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo        Instale Python 3.12+ em python.org
    pause
    exit /b 1
)

:: Instala dependências se não instalado
if not exist ".venv" (
    echo [SETUP] Criando ambiente virtual...
    python -m venv .venv
    echo [SETUP] Instalando dependencias ^(pode demorar 1-2 min^)...
    call .venv\Scripts\activate.bat
    pip install -q agno openai groq tavily-python yfinance duckduckgo-search chromadb pypdf python-dotenv uvicorn fastapi psutil
    echo [OK] Dependencias instaladas!
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo  Iniciando AgenteMaestro...
echo  Painel web: http://localhost:8000
echo  Pressione CTRL+C para parar
echo.

:: Inicia o agente
python main.py

pause
