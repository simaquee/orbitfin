# Spec Delta

## Purpose

Gera automaticamente recomendações financeiras curtas e práticas a partir das transações e dos orçamentos do usuário, sem depender de serviços externos de IA.

## ADDED Requirements

### Requirement: Sugestão de limite estourado
Para cada categoria com gasto do mês acima do limite, o sistema SHALL gerar a sugestão "Você ultrapassou o limite de {categoria} em {valor excedente} este mês." (prioridade 1).

#### Scenario: Limite estourado
- **WHEN** Transporte tem gasto de R$ 450 e limite de R$ 400 no mês
- **THEN** uma sugestão diz "Você ultrapassou o limite de Transporte em R$ 50,00 este mês."

### Requirement: Sugestão de limite próximo
Para cada categoria com 85% ou mais do limite consumido, sem estourar, o sistema SHALL gerar a sugestão "{categoria} já usou {percentual}% do limite. Restam {valor restante}." (prioridade 2).

#### Scenario: Perto do limite
- **WHEN** Lazer tem gasto de R$ 270 e limite de R$ 300
- **THEN** uma sugestão diz "Lazer já usou 90% do limite. Restam R$ 30,00."

### Requirement: Sugestão de despesas pendentes
Se houver despesas pendentes no mês atual, o sistema SHALL gerar a sugestão "Você tem {total} em despesas pendentes este mês." (prioridade 3).

#### Scenario: Pendentes
- **WHEN** o mês tem despesas pendentes de R$ 150 e R$ 250
- **THEN** uma sugestão diz "Você tem R$ 400,00 em despesas pendentes este mês."

### Requirement: Sugestão de resultado do mês
O sistema SHALL gerar uma sugestão sobre o resultado do mês (prioridade 4): se positivo, "Você poupou {taxa}% das suas receitas este mês."; se negativo, "Suas despesas superaram as receitas em {valor} este mês."

#### Scenario: Mês positivo
- **WHEN** as receitas do mês são R$ 5.000 e as despesas R$ 3.500
- **THEN** uma sugestão diz "Você poupou 30% das suas receitas este mês."

#### Scenario: Mês negativo
- **WHEN** as receitas do mês são R$ 2.000 e as despesas R$ 2.300
- **THEN** uma sugestão diz "Suas despesas superaram as receitas em R$ 300,00 este mês."

### Requirement: Exibição das sugestões
O card "Sugestões" do Dashboard SHALL exibir no máximo 3 sugestões, as de maior prioridade, com ícone de lâmpada em Terracota; sem nenhuma transação no mês, MUST exibir "Registre suas transações do mês para receber sugestões."

#### Scenario: Limite de 3 sugestões
- **WHEN** as regras geram 5 sugestões
- **THEN** o card exibe apenas as 3 primeiras pela ordem de prioridade

#### Scenario: Mês vazio
- **WHEN** o usuário não tem transações no mês atual
- **THEN** o card exibe "Registre suas transações do mês para receber sugestões."
