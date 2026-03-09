@echo off
chcp 65001 > nul
title 🤖 AGENTE MAESTRO — Toca da Onça
color 0A
cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║    🤖  AGENTE MAESTRO — TOCA DA ONCA    ║
echo  ║       17 Skills instaladas e prontas!   ║
echo  ╚══════════════════════════════════════════╝
echo.

:: ─── Verificar Python ───────────────────────────────────────
python --version > nul 2>&1
if errorlevel 1 (
    echo  ❌ Python nao encontrado!
    echo     Instale em: https://python.org/downloads/
    echo     Marque a opcao "Add Python to PATH"
    pause
    exit /b 1
)
echo  ✅ Python encontrado!

:: ─── Configurar .env ─────────────────────────────────────────
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" > nul
        echo  ⚠️  Arquivo .env criado! Adicione sua OPENAI_API_KEY
        echo.
        echo  📋 Abrindo .env para voce configurar...
        notepad .env
        echo.
        echo  Pressione qualquer tecla apos salvar o .env...
        pause > nul
    ) else (
        echo  ❌ Arquivo .env nao encontrado!
        echo     Crie um arquivo .env com: OPENAI_API_KEY=sk-...
        pause
        exit /b 1
    )
)
echo  ✅ Arquivo .env encontrado!

:: ─── Verificar OPENAI_API_KEY no .env ────────────────────────
findstr /i "OPENAI_API_KEY=sk-proj" .env > nul 2>&1
if errorlevel 1 (
    findstr /i "OPENAI_API_KEY=sk-" .env > nul 2>&1
    if errorlevel 1 (
        echo  ⚠️  OPENAI_API_KEY pode nao estar configurada!
        echo     Edite o arquivo .env e adicione sua chave.
        echo     Continuando mesmo assim...
    )
)

:: ─── Criar venv ou ativar existente ──────────────────────────
if not exist ".venv" (
    echo.
    echo  📦 Criando ambiente virtual Python...
    python -m venv .venv
    if errorlevel 1 (
        echo  ❌ Erro ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
echo  ✅ Ambiente virtual ativado!

:: ─── Instalar/atualizar dependências ─────────────────────────
echo.
echo  📦 Verificando dependencias (pode demorar na 1a vez)...
pip install -q --upgrade agno openai groq python-dotenv ^
    duckduckgo-search yfinance chromadb pypdf ^
    uvicorn fastapi sqlalchemy 2>&1 | findstr /V "already"
echo  ✅ Dependencias OK!

:: ─── Criar pastas necessárias ────────────────────────────────
if not exist "tmp" mkdir tmp
if not exist "agentes_criados" mkdir agentes_criados

:: ─── Abrir navegador e iniciar agente ────────────────────────
echo.
echo  🌐 Abrindo painel em: http://localhost:8000
echo  💬 Voce pode falar com o AgenteMaestro pelo navegador!
echo  ⏹️  Pressione CTRL+C para parar.
echo.
timeout /t 2 /nobreak > nul
start "" "http://localhost:8000"

python AgenteMaestro.py

echo.
echo  AgenteMaestro encerrado.
pause
