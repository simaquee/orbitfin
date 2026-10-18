# Design

## Context

Usa `GET /transacoes` e as funções de `src/services/calculos.py` criadas nas mudanças anteriores. No original, os resumos mensais e anuais eram calculados no cliente quando o modo Xano estava ativo; o comportamento visual da página é mantido, com a paleta oficial.

## Goals / Non-Goals

**Goals:**
- Reaproveitar os cálculos existentes, sem duplicar fórmulas na view.

**Non-Goals:**
- Agregações no servidor.

## Decisions

- **Novas funções puras em `src/services/calculos.py`:** `resumo_mes(transacoes, ano, mes)`, `resumo_ano(transacoes, ano)` (sempre 12 meses, com zero nos vazios), `serie_diaria(transacoes, ano, mes)` (com `calendar.monthrange` para o último dia) e `por_categoria(transacoes, tipo, ano, mes)`.
- **Cores dentro da paleta:**
  - receitas em Azul Marinho;
  - despesas em Terracota;
  - saldo em Azul Marinho pontilhado;
  - faixas do medidor com opacidades crescentes de Terracota (10%, 25% e 45%).
  - O original usava azul `#3B82F6` e laranja `#F97316`, fora da paleta.
- **Plotly** para todos os gráficos (`go.Scatter`, `go.Bar`, `go.Pie` com `hole=0.62` e `go.Indicator` para o medidor), sem barra de ferramentas (`displayModeBar=False`).

## Risks / Trade-offs

- [Muitos gráficos em uma página deixam o carregamento lento] → uma única chamada a `/transacoes`, com cálculos em memória.
- [Faixas do medidor só em tons de Terracota podem ficar pouco distintas] → reforçar com o texto do percentual sob o medidor.
