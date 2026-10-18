# Proposal

## Why

O Dashboard é a tela inicial e deve responder em segundos "como estão minhas finanças?". No original:
- o saldo misturava lançamentos pagos e pendentes, contrariando a regra de negócio da especificação;
- o gráfico de rosca por categoria pedido para o Dashboard só existia em Relatórios;
- o card "Sugestões da IA" mostrava um texto fixo salvo no banco que nunca era atualizado.

Depende de: `add-orcamentos`.

## What Changes

- Saudação "Olá, {primeiro nome}" e 4 indicadores: Saldo atual (somente pagos), Receitas do mês, Despesas do mês e Resultado do mês.
- Gráfico de linhas "Receitas vs despesas" dos últimos 6 meses.
- Gráfico de rosca "Gastos por categoria" do mês atual.
- Resumo dos orçamentos do mês e das 6 últimas transações.
- **Card "Sugestões"** gerado por regras a partir das transações e dos orçamentos (sem modelo de IA e sem chave de API), substituindo o texto fixo do original.

## Capabilities

### New Capabilities
- `dashboard`: painel principal com indicadores, gráficos e resumos do mês.
- `sugestoes`: geração de recomendações financeiras automáticas a partir dos dados do usuário.

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Frontend: `src/views/dashboard.py`, `src/services/sugestoes.py`, funções novas em `src/services/calculos.py`.
- Backend: nenhum endpoint novo (usa `GET /transacoes` e `GET /budgets`). A tabela `insight` e os endpoints `/insights` e `/saldo` do original **não** são recriados.

## Fora do escopo

- Sugestões geradas por modelo de linguagem (LLM).
- Marcar sugestões como lidas ou guardar seu histórico.
- Contas bancárias no resumo do Dashboard.
