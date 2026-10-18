# Proposal

## Why

Definir tetos de gasto por categoria é o principal instrumento de controle do OrbitFin. No original, o gasto de cada orçamento somava despesas de todo o histórico (não só do mês), cada tela recalculava o gasto de um jeito diferente e, por causa da categoria em texto livre, o gasto às vezes não aparecia.

Depende de: `add-transacoes`, que define as categorias de despesa.

## What Changes

- Tabela `budget` e endpoints `GET /budgets` (com gasto e percentual do mês calculados no servidor) e `PUT /budgets/{id}` no Xano.
- Orçamentos padrão criados automaticamente para cada usuário (as 7 categorias de despesa).
- Página **Orçamento**: indicadores, barras por categoria com alertas (85% e estouro) e ajuste de limite.
- Página **Metas**, fiel ao original: mostra cada limite como uma "meta de contenção", com quanto ainda cabe no teto, a taxa de poupança do mês e o status (No caminho, Em risco, Teto atingido).
- **O gasto passa a considerar somente o mês selecionado** (padrão: mês atual).

## Capabilities

### New Capabilities
- `orcamentos`: limites mensais de gasto por categoria, cálculo de consumo e alertas.
- `metas`: acompanhamento da contenção de gastos frente aos limites e da taxa de poupança do mês.

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Backend: `src/xano/table/budget.xs`, `src/xano/api/orbitfin/budgets_GET.xs` e `src/xano/api/orbitfin/budgets/budget_id_PUT.xs`.
- Frontend: `src/views/orcamento.py`, `src/views/metas.py` e funções novas em `src/services/calculos.py`.

## Fora do escopo

- Criar ou remover categorias de orçamento (dependem de categorias personalizadas).
- Metas financeiras de acúmulo (por exemplo, "Reserva de emergência: R$ 10.000 até dez/2027"), citadas nos documentos do original mas nunca implementadas: candidata a mudança futura.
- Limites diferentes por mês (o mesmo limite vale para todos os meses).
