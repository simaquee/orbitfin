# Spec Delta

## Purpose

Permite que o usuário defina um teto mensal de gastos para cada categoria de despesa e acompanhe quanto já consumiu, com alertas antes e depois de estourar.

## ADDED Requirements

### Requirement: Orçamentos padrão
Todo usuário SHALL ter um orçamento para cada categoria de despesa, criado automaticamente com os limites: Alimentação R$ 800, Moradia R$ 1.200, Transporte R$ 400, Lazer R$ 300, Saúde R$ 200, Educação R$ 150 e Outros R$ 500.

#### Scenario: Primeiro acesso
- **WHEN** um usuário recém-cadastrado abre a página Orçamento
- **THEN** são exibidas as 7 categorias com os limites padrão e gasto R$ 0,00

### Requirement: Gasto mensal por categoria
O gasto de um orçamento SHALL ser a soma das despesas do usuário naquela categoria com data dentro do mês consultado (padrão: mês atual), considerando despesas pagas e pendentes. O percentual consumido é gasto ÷ limite × 100.

#### Scenario: Gasto do mês
- **WHEN** em outubro de 2026 o usuário tem despesas de Alimentação de R$ 300 em 02/10 e R$ 260 (pendente) em 15/10, e de R$ 900 em 20/09
- **THEN** o orçamento de Alimentação de outubro mostra gasto de R$ 560,00 de R$ 800,00 (70%)

### Requirement: Estado e alerta de cada orçamento
Cada categoria SHALL ser classificada como "estourado" quando o gasto supera o limite, "atenção" quando consome 85% ou mais e "ok" nos demais casos. A barra de progresso usa largura de até 100% e as cores: Azul Marinho (ok), Terracota clara (atenção) e Terracota (estourado).

#### Scenario: Atenção
- **WHEN** Lazer tem limite de R$ 300 e gasto de R$ 270
- **THEN** a linha mostra o selo "90%", a barra em Terracota clara e "R$ 30,00 disponível"

#### Scenario: Estourado
- **WHEN** Transporte tem limite de R$ 400 e gasto de R$ 450
- **THEN** a linha mostra o selo "Estourou", a barra cheia em Terracota e "Ultrapassou R$ 50,00"

### Requirement: Página Orçamento
A página SHALL exibir um seletor de mês e os indicadores "Limite total", "Gasto total" (com % do limite), "Disponível" (limite total − gasto total) e "Estouradas" (quantidade de categorias acima do limite), seguidos da lista de categorias ordenada do maior para o menor percentual.

#### Scenario: Indicadores
- **WHEN** a soma dos limites é R$ 3.550, o gasto total é R$ 1.775 e uma categoria está estourada
- **THEN** os indicadores mostram R$ 3.550,00, R$ 1.775,00 (50% do limite), R$ 1.775,00 disponível e 1 estourada

### Requirement: Ajuste de limite
O usuário SHALL poder alterar o limite de uma categoria; o novo limite MUST ser maior que zero e vale para todos os meses.

#### Scenario: Novo limite
- **WHEN** o usuário altera o limite de Lazer para R$ 450
- **THEN** o orçamento de Lazer passa a mostrar o limite de R$ 450,00

#### Scenario: Limite inválido
- **WHEN** o usuário informa o limite R$ 0,00
- **THEN** o sistema exibe "O limite deve ser maior que zero." e mantém o valor anterior

### Requirement: Isolamento dos orçamentos
O backend MUST permitir consultar e alterar apenas os orçamentos do usuário autenticado.

#### Scenario: Orçamento de outro usuário
- **WHEN** um usuário tenta alterar o limite de um orçamento de outro usuário
- **THEN** o backend recusa com "Orçamento não encontrado."
