# Proposal

## Why

Transações (receitas e despesas) são o dado central do OrbitFin: saldo, orçamentos, dashboard e relatórios derivam delas. No original, a categoria era texto livre (então "alimentação" e "Alimentação" viravam categorias diferentes e não batiam com os orçamentos), a edição não validava campos e não havia filtro por período, embora a especificação o exigisse.

Depende de: `add-autenticacao`.

## What Changes

- Tabela `transacao` e endpoints de listar, criar, editar e excluir no Xano, sempre restritos ao usuário autenticado.
- Página Transações: botão "Adicionar transação", lista com filtros (mês, tipo, status, categoria), indicadores do filtro, edição e exclusão com confirmação.
- **Categorias padronizadas** (lista fixa por tipo) no lugar do texto livre.
- Mesmas validações na criação e na edição.

## Capabilities

### New Capabilities
- `transacoes`: registro, consulta, filtragem, edição e exclusão de receitas e despesas do usuário, com suas regras de validação e categorias.

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Backend: `src/xano/table/transacao.xs` e `src/xano/api/orbitfin/transacoes_*.xs`.
- Frontend: `src/views/transacoes.py`, `src/services/api.py`, `src/services/categorias.py`, `src/services/calculos.py`.
- As categorias de despesa definidas aqui são as mesmas usadas pelos orçamentos (`add-orcamentos`).

## Fora do escopo

- Contas/carteiras (`Account`), categorias personalizadas, transações recorrentes e importação de extratos (OFX/CSV): possíveis mudanças futuras.
- Paginação no servidor (o volume esperado por usuário é pequeno).
