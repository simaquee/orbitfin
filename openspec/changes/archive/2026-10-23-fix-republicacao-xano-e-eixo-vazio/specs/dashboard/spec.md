## MODIFIED Requirements

### Requirement: Gráfico de receitas e despesas
O Dashboard SHALL exibir o gráfico de linhas "Receitas vs despesas" com os últimos 6 meses, incluindo o atual, mesmo os meses sem lançamentos (valor zero). Receitas em Azul Marinho e despesas em Terracota. Quando não houver nenhum lançamento no período, o eixo de valores MUST ir de R$ 0 a R$ 100, sem rótulos repetidos.

#### Scenario: Meses sem lançamentos
- **WHEN** em outubro de 2026 o usuário só tem transações em setembro e outubro
- **THEN** o eixo mostra mai/2026 a out/2026, com zero de maio a agosto

#### Scenario: Nenhum lançamento no período
- **WHEN** um usuário recém-cadastrado abre o Dashboard
- **THEN** o eixo de valores mostra R$ 0, R$ 20, R$ 40, R$ 60, R$ 80 e R$ 100, e as duas linhas ficam em zero
