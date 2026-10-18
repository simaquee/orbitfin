# Tasks

## 1. Cálculos e sugestões

- [x] 1.1 Implementar em `src/services/calculos.py` as funções `saldo_atual`, `totais_mes` (com pendentes), `serie_mensal(meses=6)` e `gastos_por_categoria`, e verificar com testes para os cenários "Saldo considera apenas pagos", "Pendentes no mês", "Resultado negativo", "Meses sem lançamentos" e "Distribuição"
- [x] 1.2 Implementar `src/services/sugestoes.py` (`gerar_sugestoes`) e verificar com testes para os cenários "Limite estourado", "Perto do limite", "Mês positivo", "Limite de 3 sugestões" e "Mês vazio"

## 2. Página Dashboard

- [x] 2.1 Implementar a saudação e os 4 indicadores em `src/views/dashboard.py` e verificar manualmente com dados de teste que os valores batem com os cenários
- [x] 2.2 Implementar os gráficos "Receitas vs despesas" e "Gastos por categoria" com a paleta oficial e os estados vazios, e verificar manualmente
- [x] 2.3 Implementar o card "Sugestões", o resumo de orçamentos e as últimas transações com "Ver todas", e verificar manualmente os cenários "Orçamento estourado no resumo" e "Sem transações"

## Workflow follow-up

- Arquivar com `/opsx:archive` após a revisão; em seguida aplicar `add-relatorios`.
