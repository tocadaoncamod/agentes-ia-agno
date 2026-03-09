// Content Script - injeta botão flutuante em todas as páginas

(function() {
  if (document.getElementById('maestro-fab')) return;

  const fab = document.createElement('div');
  fab.id = 'maestro-fab';
  fab.innerHTML = '🤖';
  fab.title = 'AgenteMaestro — Enviar para o agente';
  fab.style.cssText = `
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    cursor: pointer;
    z-index: 999999;
    box-shadow: 0 4px 20px rgba(124,58,237,0.5);
    transition: transform 0.2s, box-shadow 0.2s;
    user-select: none;
  `;

  fab.addEventListener('mouseenter', () => {
    fab.style.transform = 'scale(1.15)';
    fab.style.boxShadow = '0 6px 25px rgba(124,58,237,0.7)';
  });
  fab.addEventListener('mouseleave', () => {
    fab.style.transform = 'scale(1)';
    fab.style.boxShadow = '0 4px 20px rgba(124,58,237,0.5)';
  });

  fab.addEventListener('click', () => {
    const sel = window.getSelection().toString().trim();
    const context = sel
      ? `Texto selecionado: "${sel}"\nPágina: ${window.location.href}`
      : `Página: ${window.location.href}\nTítulo: ${document.title}\n\n${document.body.innerText.slice(0, 1500)}`;

    fetch('http://localhost:8000/v1/playground/agent/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: context,
        agent_id: 'agente-maestro',
        stream: false
      })
    }).then(() => {
      fab.innerHTML = '✅';
      setTimeout(() => { fab.innerHTML = '🤖'; }, 2000);
    }).catch(() => {
      fab.innerHTML = '❌';
      setTimeout(() => { fab.innerHTML = '🤖'; }, 2000);
    });
  });

  document.body.appendChild(fab);
})();
