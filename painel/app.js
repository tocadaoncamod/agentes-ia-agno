// ============================================
// AGENTE MAESTRO — PAINEL PREMIUM
// Lógica de Chat + Conexão com API
// ============================================

// Estado global
const state = {
  currentAgent: 'maestro',
  currentAgentName: '🎯 AgenteMaestro',
  apiBase: window.location.origin,
  isLoading: false,
  sessionId: 'painel-' + Date.now(),
  conversations: {},
};

// Elementos DOM
const elements = {
  chatMessages: () => document.getElementById('chat-messages'),
  msgInput: () => document.getElementById('msg-input'),
  btnSend: () => document.getElementById('btn-send'),
  welcomeScreen: () => document.getElementById('welcome-screen'),
  currentAgentName: () => document.getElementById('current-agent-name'),
  topbarStatus: () => document.getElementById('topbar-status'),
  connectionText: () => document.getElementById('connection-text'),
  pulseDot: () => document.querySelector('.pulse-dot'),
  hintAgent: () => document.getElementById('hint-agent'),
};

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', () => {
  setupAgentListeners();
  setupInputListeners();
  autoResize(elements.msgInput());
  checkConnection();
});

// ===== SELEÇÃO DE AGENTE =====
function setupAgentListeners() {
  document.querySelectorAll('.agent-item').forEach(btn => {
    btn.addEventListener('click', () => {
      // Salvar conversa atual
      saveCurrentConversation();

      // Atualizar UI
      document.querySelectorAll('.agent-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const agentId = btn.dataset.agent;
      const agentName = btn.querySelector('.agent-name').textContent;
      const agentIcon = btn.querySelector('.agent-icon').textContent;

      state.currentAgent = agentId;
      state.currentAgentName = `${agentIcon} ${agentName}`;

      elements.currentAgentName().textContent = state.currentAgentName;
      elements.hintAgent().textContent = agentName;
      elements.topbarStatus().textContent = 'Pronto para conversar';

      // Restaurar conversa ou mostrar welcome
      loadConversation(agentId);

      // Fechar sidebar no mobile
      document.getElementById('sidebar').classList.remove('open');
    });
  });
}

// ===== INPUT =====
function setupInputListeners() {
  const input = elements.msgInput();

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  input.addEventListener('input', () => autoResize(input));
}

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// ===== ENVIAR MENSAGEM =====
async function sendMessage() {
  const input = elements.msgInput();
  const text = input.value.trim();
  if (!text || state.isLoading) return;

  // Esconder welcome
  const welcome = elements.welcomeScreen();
  if (welcome) welcome.style.display = 'none';

  // Mostrar mensagem do usuário
  appendMessage('user', text);

  // Limpar input
  input.value = '';
  autoResize(input);

  // Mostrar typing
  const typingEl = showTyping();

  // Desabilitar envio
  state.isLoading = true;
  elements.btnSend().disabled = true;
  elements.topbarStatus().textContent = 'Pensando...';

  try {
    const response = await callAgent(text);
    removeTyping(typingEl);
    appendMessage('agent', response);
    elements.topbarStatus().textContent = 'Pronto';
  } catch (error) {
    removeTyping(typingEl);
    appendMessage('agent', `❌ **Erro de conexão**\n\nNão consegui conectar ao agente. Verifique se o servidor está rodando.\n\n\`${error.message}\`\n\n💡 Rode \`python painel/server.py\` para iniciar o servidor.`);
    elements.topbarStatus().textContent = 'Erro de conexão';
  } finally {
    state.isLoading = false;
    elements.btnSend().disabled = false;
    input.focus();
  }
}

function sendQuick(text) {
  elements.msgInput().value = text;
  sendMessage();
}

// ===== API =====
async function callAgent(message) {
  const response = await fetch(`${state.apiBase}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      agent: state.currentAgent,
      session_id: state.sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  return data.response || data.message || 'Sem resposta do agente.';
}

async function checkConnection() {
  try {
    const response = await fetch(`${state.apiBase}/health`);
    if (response.ok) {
      setConnected(true);
    } else {
      setConnected(false);
    }
  } catch {
    setConnected(false);
  }
}

function setConnected(connected) {
  const dot = elements.pulseDot();
  const text = elements.connectionText();

  if (connected) {
    dot.className = 'pulse-dot connected';
    text.textContent = 'Conectado';
    elements.topbarStatus().textContent = 'Pronto para conversar';
  } else {
    dot.className = 'pulse-dot error';
    text.textContent = 'Offline';
    elements.topbarStatus().textContent = 'Servidor offline — rode python painel/server.py';
  }
}

// ===== RENDERIZAÇÃO =====
function appendMessage(role, text) {
  const container = elements.chatMessages();
  const now = new Date();
  const time = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  const msgEl = document.createElement('div');
  msgEl.className = `message ${role}`;

  const avatar = role === 'user' ? '👤' : getAgentIcon();
  const htmlContent = role === 'agent' ? renderMarkdown(text) : escapeHtml(text);

  msgEl.innerHTML = `
    <div class="message-avatar">${avatar}</div>
    <div>
      <div class="message-content">${htmlContent}</div>
      <div class="message-time">${time}</div>
    </div>
  `;

  container.appendChild(msgEl);
  container.scrollTop = container.scrollHeight;

  // Salvar na conversa
  if (!state.conversations[state.currentAgent]) {
    state.conversations[state.currentAgent] = [];
  }
  state.conversations[state.currentAgent].push({ role, text, time });
}

function showTyping() {
  const container = elements.chatMessages();
  const el = document.createElement('div');
  el.className = 'message agent';
  el.id = 'typing-indicator';
  el.innerHTML = `
    <div class="message-avatar">${getAgentIcon()}</div>
    <div class="message-content">
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>
  `;
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
  return el;
}

function removeTyping(el) {
  if (el && el.parentNode) el.parentNode.removeChild(el);
}

function getAgentIcon() {
  const active = document.querySelector('.agent-item.active');
  return active ? active.querySelector('.agent-icon').textContent : '🤖';
}

// ===== MARKDOWN SIMPLES =====
function renderMarkdown(text) {
  if (!text) return '';

  let html = escapeHtml(text);

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

  // Blockquotes
  html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

  // Tables
  html = renderTables(html);

  // Unordered lists
  html = html.replace(/^[\-\•] (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // Ordered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // Paragraphs (double newline)
  html = html.replace(/\n\n/g, '</p><p>');
  html = html.replace(/\n/g, '<br>');

  // Clean up
  html = '<p>' + html + '</p>';
  html = html.replace(/<p><\/p>/g, '');
  html = html.replace(/<p>(<h[1-3]>)/g, '$1');
  html = html.replace(/(<\/h[1-3]>)<\/p>/g, '$1');
  html = html.replace(/<p>(<pre>)/g, '$1');
  html = html.replace(/(<\/pre>)<\/p>/g, '$1');
  html = html.replace(/<p>(<ul>)/g, '$1');
  html = html.replace(/(<\/ul>)<\/p>/g, '$1');
  html = html.replace(/<p>(<blockquote>)/g, '$1');
  html = html.replace(/(<\/blockquote>)<\/p>/g, '$1');
  html = html.replace(/<p>(<table>)/g, '$1');
  html = html.replace(/(<\/table>)<\/p>/g, '$1');

  return html;
}

function renderTables(html) {
  const lines = html.split('\n');
  let inTable = false;
  let tableHtml = '';
  let result = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('|') && line.endsWith('|')) {
      if (!inTable) {
        inTable = true;
        tableHtml = '<table>';
      }
      // Skip separator lines
      if (/^\|[\s\-:|]+\|$/.test(line)) continue;

      const cells = line.split('|').filter(c => c.trim() !== '');
      const isHeader = !inTable || tableHtml === '<table>';
      const tag = tableHtml === '<table>' ? 'th' : 'td';

      tableHtml += '<tr>';
      cells.forEach(cell => {
        tableHtml += `<${tag}>${cell.trim()}</${tag}>`;
      });
      tableHtml += '</tr>';
    } else {
      if (inTable) {
        tableHtml += '</table>';
        result.push(tableHtml);
        tableHtml = '';
        inTable = false;
      }
      result.push(line);
    }
  }

  if (inTable) {
    tableHtml += '</table>';
    result.push(tableHtml);
  }

  return result.join('\n');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ===== CONVERSA MANAGEMENT =====
function saveCurrentConversation() {
  // Already saved in appendMessage
}

function loadConversation(agentId) {
  const container = elements.chatMessages();
  container.innerHTML = '';

  const conv = state.conversations[agentId];
  if (conv && conv.length > 0) {
    conv.forEach(msg => {
      const msgEl = document.createElement('div');
      msgEl.className = `message ${msg.role}`;
      const avatar = msg.role === 'user' ? '👤' : getAgentIcon();
      const htmlContent = msg.role === 'agent' ? renderMarkdown(msg.text) : escapeHtml(msg.text);

      msgEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div>
          <div class="message-content">${htmlContent}</div>
          <div class="message-time">${msg.time}</div>
        </div>
      `;
      container.appendChild(msgEl);
    });
    container.scrollTop = container.scrollHeight;
  } else {
    // Show welcome screen
    container.innerHTML = `
      <div class="welcome-screen" id="welcome-screen">
        <div class="welcome-icon">${getAgentIcon()}</div>
        <h2 class="welcome-title">${state.currentAgentName}</h2>
        <p class="welcome-text">Comece a conversar com este agente. Ele está pronto para te ajudar!</p>
        <div class="quick-actions">
          <button class="quick-btn" onclick="sendQuick('Olá! O que você sabe fazer?')">
            👋 Apresentação
          </button>
          <button class="quick-btn" onclick="sendQuick('Me ajude com uma tarefa')">
            🎯 Começar
          </button>
        </div>
      </div>
    `;
  }
}

function clearChat() {
  state.conversations[state.currentAgent] = [];
  state.sessionId = 'painel-' + Date.now();
  loadConversation(state.currentAgent);
}

// ===== SIDEBAR TOGGLE =====
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}
