const AGENT_URL = 'http://localhost:8000';
const chat = document.getElementById('chat');
const input = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const loading = document.getElementById('loading');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

// Carregar histórico salvo
chrome.storage.local.get(['chat_history'], (result) => {
  if (result.chat_history) {
    result.chat_history.forEach(m => addMessage(m.role, m.content, false));
  }
});

// Verificar se o agente está online
async function checkStatus() {
  try {
    const r = await fetch(`${AGENT_URL}/`, { signal: AbortSignal.timeout(2000) });
    if (r.ok) {
      statusDot.style.background = '#22c55e';
      statusDot.style.boxShadow = '0 0 6px #22c55e';
      statusText.textContent = 'Agente online ✓';
    }
  } catch {
    statusDot.style.background = '#ef4444';
    statusDot.style.boxShadow = '0 0 6px #ef4444';
    statusText.textContent = 'Agente offline — inicie main.py';
  }
}
checkStatus();
setInterval(checkStatus, 10000);

function addMessage(role, content, save = true) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = content;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;

  if (save) {
    chrome.storage.local.get(['chat_history'], (result) => {
      const history = result.chat_history || [];
      history.push({ role, content });
      if (history.length > 50) history.shift();
      chrome.storage.local.set({ chat_history: history });
    });
  }
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage('user', text);
  input.value = '';
  sendBtn.disabled = true;
  loading.style.display = 'block';

  try {
    const response = await fetch(`${AGENT_URL}/v1/playground/agent/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        agent_id: 'agente-maestro',
        stream: false
      })
    });

    if (response.ok) {
      const data = await response.json();
      const reply = data.content || data.message || JSON.stringify(data);
      addMessage('agent', reply);
    } else {
      addMessage('system', `Erro ${response.status} — verifique o painel`);
    }
  } catch (e) {
    addMessage('system', '❌ Não conectou ao agente. Inicie o main.py primeiro.');
  } finally {
    sendBtn.disabled = false;
    loading.style.display = 'none';
  }
}

// Enviar com Enter (Shift+Enter para nova linha)
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Ação: Enviar conteúdo da página atual
async function sendPageContent() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => ({
      url: window.location.href,
      title: document.title,
      text: document.body.innerText.slice(0, 3000)
    })
  });
  const data = results[0].result;
  const msg = `Analise esta página:\nURL: ${data.url}\nTítulo: ${data.title}\n\n${data.text}`;
  input.value = msg;
}

// Ação: Enviar texto selecionado
async function sendSelection() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => window.getSelection().toString()
  });
  const sel = results[0].result;
  if (sel) {
    input.value = `Analise este texto:\n"${sel}"`;
  } else {
    addMessage('system', 'Selecione um texto na página primeiro.');
  }
}

// Ação: Capturar produtos da página
async function captureProducts() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const produtos = [];
      // Tenta capturar produtos de lojas comuns
      const items = document.querySelectorAll('[class*="product"], [class*="item"], [class*="card"]');
      items.forEach((el, i) => {
        if (i >= 20) return;
        const nome = el.querySelector('h2,h3,h4,[class*="name"],[class*="title"]')?.innerText?.trim();
        const preco = el.querySelector('[class*="price"],[class*="valor"]')?.innerText?.trim();
        if (nome) produtos.push({ nome, preco: preco || 'N/A' });
      });
      return { url: window.location.href, total: produtos.length, produtos };
    }
  });
  const data = results[0].result;
  if (data.produtos.length > 0) {
    const lista = data.produtos.map(p => `- ${p.nome}: ${p.preco}`).join('\n');
    input.value = `Produtos capturados de ${data.url}:\n${lista}\n\nAnalise esses produtos para a Toca da Onça.`;
  } else {
    addMessage('system', 'Nenhum produto detectado nessa página.');
  }
}

// Abrir painel completo
function openPanel() {
  chrome.tabs.create({ url: `${AGENT_URL}` });
}
