# Tasks

## 1. Backend Xano

- [x] 1.1 Definir `src/xano/table/transacao.xs` conforme o design e verificar com `xano workspace push -d ./src/xano --dry-run`
- [x] 1.2 Criar `transacoes_GET.xs`, `transacoes_POST.xs`, `transacoes/transacao_id_PUT.xs` e `transacoes/transacao_id_DELETE.xs` com validação de tipo, status, valor e categoria e isolamento por usuário, e verificar com o dry-run
- [ ] 1.3 (requer Xano) Publicar após confirmação do usuário e verificar no Run do Xano: criar, listar, editar, excluir, valor zero, categoria incompatível e acesso a transação de outro usuário

## 2. Serviços

- [x] 2.1 Implementar `src/services/categorias.py` e verificar com teste que as listas por tipo correspondem exatamente às da spec
- [x] 2.2 Implementar `src/services/calculos.py` (`filtrar` por mês/tipo/status/categoria e `totais`) e verificar com testes para os cenários "Filtro por mês e tipo" e "Totais do filtro"
- [x] 2.3 Adicionar `listar_transacoes`, `criar_transacao`, `editar_transacao` e `excluir_transacao` em `src/services/api.py` e verificar com testes simulados

## 3. Página Transações

- [x] 3.1 Implementar o formulário "Nova transação"/edição (padrões, categoria dependente do tipo, validação) e verificar manualmente os cenários "Valores padrão do formulário", "Troca de tipo" e "Valor zero"
- [x] 3.2 Implementar filtros, indicadores e lista (estados vazios, selo de status, cores, sinal) e verificar manualmente os cenários de listagem
- [x] 3.3 Implementar edição e exclusão com confirmação e verificar manualmente os cenários "Marcar como pago", "Confirmar exclusão" e "Cancelar exclusão"

## Workflow follow-up

- Arquivar com `/opsx:archive` após a revisão; em seguida aplicar `add-orcamentos`.
