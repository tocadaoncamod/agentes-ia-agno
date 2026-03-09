// Background Service Worker - AgenteMaestro Extension

// Menu de contexto (clique direito na página)
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'send-to-maestro',
    title: '🤖 Enviar para AgenteMaestro',
    contexts: ['selection', 'page', 'link', 'image']
  });
  chrome.contextMenus.create({
    id: 'analyze-page',
    title: '🔍 Analisar esta página',
    contexts: ['page']
  });
  chrome.contextMenus.create({
    id: 'analyze-product',
    title: '🛍️ Analisar produto (Toca da Onça)',
    contexts: ['selection', 'page']
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  const AGENT_URL = 'http://localhost:8000';

  let message = '';

  if (info.menuItemId === 'send-to-maestro') {
    message = info.selectionText
      ? `Analise: "${info.selectionText}"`
      : `Analise esta página: ${tab.url}`;
  } else if (info.menuItemId === 'analyze-page') {
    message = `Analise a página: ${tab.url} — Título: ${tab.title}`;
  } else if (info.menuItemId === 'analyze-product') {
    const text = info.selectionText || tab.title;
    message = `Analise este produto para a Toca da Onça: "${text}"\nURL: ${tab.url}`;
  }

  if (!message) return;

  try {
    await fetch(`${AGENT_URL}/v1/playground/agent/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        agent_id: 'agente-maestro',
        stream: false
      })
    });
    // Notifica o usuário
    chrome.notifications?.create({
      type: 'basic',
      iconUrl: 'icon48.png',
      title: 'AgenteMaestro',
      message: 'Mensagem enviada! Abra o painel para ver a resposta.'
    });
  } catch {
    console.log('AgenteMaestro offline');
  }
});
