import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path para encontrar o pacote painel e as outras ferramentas
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from painel.server import app

# Exporta o app para o Vercel
# O Vercel espera que a variável seja chamada de 'app' por padrão
handler = app
