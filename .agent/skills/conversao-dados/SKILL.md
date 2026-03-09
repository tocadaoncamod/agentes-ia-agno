---
name: conversao-dados
description: "Conversões de moeda, temperatura, unidades e cálculos utilitários. Use quando o usuário pedir conversões, cálculos de câmbio, temperatura ou variação percentual."
---

# Conversão de Dados e Cálculos

## Quando Usar
- Conversão de temperatura (°C ↔ °F)
- Conversão de moeda (USD ↔ BRL)
- Cálculo de variação percentual
- Qualquer conversão de unidades

## Ferramentas Disponíveis

### Temperatura
- `celsius_para_fahrenheit(temp_celsius)` → Fahrenheit
- `fahrenheit_para_celsius(temp_fahrenheit)` → Celsius
- **Sempre mostre ambos os valores** na resposta

### Câmbio
- `converter_moeda_brl(valor_usd, taxa_cambio)` → BRL
- **Busque a taxa atual** antes de converter (use DuckDuckGo)
- Informe a data/hora da taxa usada

### Variação Percentual
- `calcular_variacao_percentual(valor_anterior, valor_atual)` → "%"
- Use em comparações de preços, investimentos, etc.

## Formato de Resposta

### Para Conversões
```
## 🔄 Conversão

| De | Para |
|----|------|
| 100°C | 212°F |

**Fórmula:** °F = (°C × 9/5) + 32
```

### Para Câmbio
```
## 💱 Conversão de Moeda

| USD | BRL |
|-----|-----|
| $100.00 | R$ 570,00 |

**Taxa:** 1 USD = 5,70 BRL
**Atualizado em:** [data]
```

## Regras
- Busque taxa de câmbio atualizada sempre que possível
- Mostre a fórmula usada para transparência
- Use tabelas para múltiplas conversões
- Arredonde para 2 casas decimais
