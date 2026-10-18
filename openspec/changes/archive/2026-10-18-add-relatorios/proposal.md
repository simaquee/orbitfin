# Proposal

## Why

O Dashboard mostra só o mês atual. Para entender a evolução das finanças, o usuário precisa analisar qualquer mês ou ano passado: fluxo de caixa, taxa de poupança, quanto da receita foi consumido e onde o dinheiro foi gasto. O original tinha essa página; ela é recriada com a paleta oficial e com cálculos centralizados.

Depende de: `add-dashboard`, que reaproveita os cálculos de `src/services/calculos.py`.

## What Changes

- Página Relatórios com filtros de ano, mês e visão do gráfico (Mensal ou Anual).
- Indicadores do mês (Receitas, Despesas, Saldo e Poupança), cada um com uma minilinha (*sparkline*) dos 12 meses do ano.
- Gráfico principal (diário no modo Mensal, mensal no modo Anual) com receitas, despesas e saldo.
- Medidor "Gasto vs receita", roscas de despesas e receitas por categoria e comparativo mensal do ano.
- Totais anuais e lista dos lançamentos do mês.

## Capabilities

### New Capabilities
- `relatorios`: análises históricas por mês e por ano das receitas, despesas, saldo e poupança do usuário.

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Frontend: `src/views/relatorios.py` e funções novas em `src/services/calculos.py`.
- Backend: nenhum endpoint novo (usa `GET /transacoes`).

## Fora do escopo

- Exportação em PDF ou planilha.
- Comparação entre anos diferentes no mesmo gráfico.
