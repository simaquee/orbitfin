# Tasks

## 1. Backend Xano

- [x] 1.1 Definir `src/xano/table/budget.xs` com índice único (user_id, categoria) e verificar com `xano workspace push -d ./src/xano --dry-run`
- [x] 1.2 Criar `budgets_GET.xs` (seed preguiçoso dos 7 padrões, gasto do período via `inicio`/`fim`) e `budgets/budget_id_PUT.xs` (limite > 0, isolamento), e verificar com o dry-run
- [ ] 1.3 (requer Xano) Publicar após confirmação do usuário e verificar no Run do Xano os cenários "Primeiro acesso", "Gasto do mês", "Limite inválido" e "Orçamento de outro usuário"

## 2. Serviços

- [x] 2.1 Adicionar `listar_orcamentos(mes)` e `alterar_limite(id, limite)` em `src/services/api.py` e verificar com testes simulados
- [x] 2.2 Implementar em `src/services/calculos.py` as funções `estado_orcamento`, `indicadores_orcamento`, `status_meta`, `ordenar_metas` e `taxa_poupanca`, e verificar com testes para os cenários "Atenção", "Estourado", "Indicadores", "Em risco", "Teto atingido", "Folga", "Poupança do mês" e "Mês sem receitas"

## 3. Páginas

- [x] 3.1 Implementar `src/views/orcamento.py` (seletor de mês, indicadores, lista ordenada com selos e cores, diálogo "Ajustar limite") e verificar manualmente os cenários da spec `orcamentos`
- [x] 3.2 Implementar `src/views/metas.py` (indicadores, texto explicativo, lista com barra de folga, diálogo "Ajustar meta") e verificar manualmente os cenários da spec `metas`, incluindo "Ajuste pela página Metas"

## Workflow follow-up

- Arquivar com `/opsx:archive` após a revisão; em seguida aplicar `add-dashboard`.
