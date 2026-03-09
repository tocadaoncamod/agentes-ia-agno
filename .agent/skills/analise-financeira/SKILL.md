---
name: analise-financeira
description: "Análise técnica e fundamentalista de ações, criptomoedas e mercado financeiro. Use quando o usuário perguntar sobre cotações, investimentos, comparações de ativos ou análise de mercado."
---

# Análise Financeira Profissional

## Quando Usar
- Cotação de ações, criptos ou commodities
- Análise fundamentalista (P/L, EV/EBITDA, ROE, etc.)
- Comparação entre ativos
- Recomendações de analistas
- Notícias que impactam o mercado

## Fluxo de Trabalho

### 1. Identificar o Ativo
- Converta nomes populares para ticker correto
- Ações brasileiras: adicione `.SA` (ex: `PETR4.SA`, `VALE3.SA`)
- Ações americanas: use direto (ex: `AAPL`, `GOOGL`, `MSFT`)
- Se o usuário mencionar a empresa sem ticker, pesquise o ticker correto

### 2. Coletar Dados com YFinanceTools
Sempre colete:
- `stock_price` — Preço atual e variação do dia
- `company_info` — Informações da empresa
- `analyst_recommendations` — Recomendações dos analistas
- `stock_fundamentals` — Dados fundamentalistas
- `key_financial_ratios` — Indicadores financeiros

### 3. Buscar Notícias Recentes
- Use DuckDuckGoTools para notícias dos últimos 7 dias
- Busque: `"[empresa] ações notícias [ano atual]"`
- Identifique catalisadores positivos e negativos

### 4. Apresentar Análise

#### Formato Padrão:
```
## 📈 Análise: [Nome da Empresa] ([TICKER])

### Cotação Atual
| Indicador | Valor |
|-----------|-------|
| Preço     | R$ XX,XX |
| Variação dia | +X,XX% |
| Volume    | XX.XXX |
| Mín/Máx 52s | R$ XX / R$ XX |

### Indicadores Fundamentalistas
| Indicador | Valor | Interpretação |
|-----------|-------|---------------|
| P/L       | XX,X  | [bom/alto/baixo] |
| EV/EBITDA | XX,X  | [análise] |
| ROE       | XX%   | [análise] |
| Div. Yield| X,X%  | [análise] |

### Recomendações dos Analistas
🟢 Compra: X | 🟡 Manter: X | 🔴 Venda: X

### Notícias Recentes
- [notícia 1] *(data)*
- [notícia 2] *(data)*

### Análise Resumida
**Pontos positivos:** [lista]
**Riscos:** [lista]
**Visão geral:** [conclusão em 2-3 frases]
```

## Regras Importantes
- **Use SEMPRE tabelas** para dados numéricos
- **Nunca dê conselho de investimento direto** — apresente dados para o usuário decidir
- **Mencione riscos** — todo investimento tem risco
- **Dados em tempo real** — informe que cotações podem ter delay de 15-20 min
- **Compare quando possível** — se o usuário mencionar 2+ ativos, faça comparativo
