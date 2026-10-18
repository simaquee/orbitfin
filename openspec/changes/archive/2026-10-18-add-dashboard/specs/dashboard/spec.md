# Spec Delta

## Purpose

Painel inicial do OrbitFin que resume a situação financeira do usuário no mês atual: saldo, receitas, despesas, distribuição de gastos, orçamentos, últimas transações e sugestões.

## ADDED Requirements

### Requirement: Indicadores principais
O Dashboard SHALL exibir quatro indicadores:
- "Saldo atual": receitas pagas − despesas pagas de todo o histórico.
- "Receitas do mês": soma das receitas do mês atual, pagas e pendentes.
- "Despesas do mês": soma das despesas do mês atual, pagas e pendentes.
- "Resultado do mês": receitas do mês − despesas do mês.

Quando houver pendentes no mês, os indicadores mensais MUST informar o valor pendente na dica.

#### Scenario: Saldo considera apenas pagos
- **WHEN** o histórico tem receitas pagas de R$ 5.000, despesas pagas de R$ 3.200 e uma despesa pendente de R$ 400
- **THEN** "Saldo atual" mostra R$ 1.800,00

#### Scenario: Pendentes no mês
- **WHEN** em outubro de 2026 as despesas somam R$ 3.600, das quais R$ 400 estão pendentes
- **THEN** "Despesas do mês" mostra R$ 3.600,00 com a dica "R$ 400,00 pendente · out/2026"

#### Scenario: Resultado negativo
- **WHEN** as receitas do mês são R$ 2.000 e as despesas R$ 2.300
- **THEN** "Resultado do mês" mostra -R$ 300,00 em Terracota

### Requirement: Gráfico de receitas e despesas
O Dashboard SHALL exibir o gráfico de linhas "Receitas vs despesas" com os últimos 6 meses, incluindo o atual, mesmo os meses sem lançamentos (valor zero). Receitas em Azul Marinho e despesas em Terracota.

#### Scenario: Meses sem lançamentos
- **WHEN** em outubro de 2026 o usuário só tem transações em setembro e outubro
- **THEN** o eixo mostra mai/2026 a out/2026, com zero de maio a agosto

### Requirement: Gastos por categoria
O Dashboard SHALL exibir um gráfico de rosca "Gastos por categoria" com as despesas do mês atual agrupadas por categoria, mostrando o percentual de cada uma.

#### Scenario: Distribuição
- **WHEN** as despesas do mês são Moradia R$ 1.200, Alimentação R$ 600 e Lazer R$ 200
- **THEN** o gráfico mostra Moradia 60%, Alimentação 30% e Lazer 10%

#### Scenario: Mês sem despesas
- **WHEN** não há despesas no mês atual
- **THEN** o sistema exibe "Sem despesas neste mês." no lugar do gráfico

### Requirement: Resumo de orçamentos
O Dashboard SHALL exibir os orçamentos do mês atual com categoria, "gasto / limite" e barra de progresso, usando os mesmos estados e cores da página Orçamento e ordenados do maior para o menor percentual (no máximo 6).

#### Scenario: Orçamento estourado no resumo
- **WHEN** Transporte tem gasto de R$ 450 e limite de R$ 400 no mês
- **THEN** Transporte aparece no topo do resumo com a barra cheia em Terracota

### Requirement: Últimas transações
O Dashboard SHALL exibir as 6 transações mais recentes com categoria, "data · descrição" (ou o tipo, se não houver descrição) e o valor com sinal e cor por tipo, além de um link "Ver todas" para a página Transações.

#### Scenario: Sem transações
- **WHEN** o usuário não tem transações
- **THEN** o sistema exibe "Nenhuma transação ainda. Adicione a primeira em Transações."
