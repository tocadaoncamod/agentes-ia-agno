# 🤖 AgenteMaestro

Agente autônomo com auto-melhoria, painel web e extensão Chrome.
**Exclusivo — pasta própria — não misturado com outros projetos.**

---

## 🚀 Como iniciar

1. **Dê duplo clique em `INICIAR.bat`**
2. Na primeira vez, preencha o `.env` com suas API keys
3. Acesse **http://localhost:8000**

---

## 🛠️ O que ele pode fazer

| Capacidade | Descrição |
|---|---|
| 🐍 **Executar Python** | Escreve e roda qualquer código Python |
| 📁 **Criar Arquivos** | Cria, lê e edita arquivos no projeto |
| 💻 **VS Code** | Abre arquivos e pastas direto no editor |
| 🤖 **Criar Agentes** | Gera novos agentes especializados |
| 🛠️ **Gerenciar Skills** | Adiciona novas habilidades dinamicamente |
| 🌐 **Pesquisa Web** | DuckDuckGo + Tavily (sem e com API key) |
| 📈 **Dados Financeiros** | Cotações, empresas, mercado |
| 🧠 **Memória Persistente** | Lembra conversas e preferências |
| 🔧 **Instalar Pacotes** | `pip install` automático |

---

## 🌐 Extensão Chrome

Localização: pasta `extension/`

**Como instalar:**
1. Abra Chrome → `chrome://extensions`
2. Ative "Modo do desenvolvedor" (canto superior direito)
3. Clique "Carregar sem compactação"
4. Selecione a pasta `extension/`

**O que faz:**
- 🤖 Botão flutuante em todas as páginas (clique para enviar ao agente)
- 📄 Envia conteúdo da página atual
- ✂️ Envia texto selecionado
- 🛍️ Captura produtos automaticamente
- 🖱️ Menu de contexto (clique direito → "Enviar para AgenteMaestro")

---

## 📁 Estrutura

```
AgenteMaestro/
├── INICIAR.bat          ← Duplo clique para iniciar
├── main.py              ← Servidor web (porta 8000)
├── agent.py             ← Definição do agente
├── .env                 ← Suas API keys (não compartilhe!)
├── tools/
│   ├── python_executor.py  ← Executa código Python
│   ├── vscode_tool.py      ← Integração VS Code
│   ├── agent_factory.py    ← Cria novos agentes
│   └── skill_manager.py    ← Gerencia skills
├── agents_criados/      ← Agentes gerados pelo Maestro
├── extension/           ← Extensão Chrome
├── memory/              ← Banco de dados de memória
├── knowledge/           ← Base de conhecimento
└── skills/              ← Skills customizadas
```

---

## 🔑 API Keys necessárias

| Key | Onde obter | Obrigatório |
|---|---|---|
| `OPENAI_API_KEY` | platform.openai.com | ✅ Sim |
| `TAVILY_API_KEY` | tavily.com | Opcional |
| `GROQ_API_KEY` | console.groq.com | Opcional |

---

## 💬 Exemplos de uso

**No painel web (http://localhost:8000):**

```
"Cria um agente especialista em precificação de produtos"
"Escreve um script Python para baixar imagens do AliExpress"
"Lista todas as skills disponíveis"
"Instala o pacote selenium"
"Abre o VS Code neste projeto"
```
