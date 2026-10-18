# relatorios Specification

## Purpose
Permite analisar a evolução financeira do usuário em qualquer mês ou ano: fluxo de caixa, taxa de poupança, comprometimento da receita e distribuição por categoria.

## Requirements

### Requirement: Filtros do relatório
A página SHALL oferecer os filtros "Ano" (do ano atual até 5 anos antes, padrão: ano atual), "Mês" (Janeiro a Dezembro, padrão: mês atual) e "Visão do gráfico" (Mensal ou Anual, padrão: Mensal). Todos os valores consideram lançamentos pagos e pendentes.

#### Scenario: Filtros padrão
- **WHEN** o usuário abre Relatórios em 18/10/2026
- **THEN** os filtros vêm como 2026, Outubro e Mensal

### Requirement: Indicadores do mês com minilinhas
O sistema SHALL exibir, para o mês selecionado, "Receitas", "Despesas", "Saldo" (receitas − despesas) e "Poupança" (saldo ÷ receitas × 100, ou 0% sem receitas), cada um com uma minilinha dos 12 meses do ano selecionado.

#### Scenario: Poupança do mês
- **WHEN** em setembro de 2026 as receitas são R$ 4.000 e as despesas R$ 3.000
- **THEN** os indicadores mostram R$ 4.000,00, R$ 3.000,00, R$ 1.000,00 e "25%"

#### Scenario: Poupança negativa
- **WHEN** as receitas do mês são R$ 2.000 e as despesas R$ 2.500
- **THEN** "Poupança" mostra "-25%" em Terracota

### Requirement: Gráfico principal
O sistema SHALL exibir um gráfico de linhas com receitas, despesas e saldo. Na visão Mensal, o eixo vai do dia 1 ao último dia do mês (totais diários). Na visão Anual, vai de Jan a Dez (totais mensais). Períodos sem lançamentos aparecem como zero.

#### Scenario: Visão mensal
- **WHEN** o usuário seleciona Fevereiro de 2028 na visão Mensal
- **THEN** o eixo mostra os dias 1 a 29

#### Scenario: Mês vazio
- **WHEN** o mês selecionado não tem lançamentos
- **THEN** o gráfico mostra a grade zerada com o aviso "Sem lançamentos neste período."

### Requirement: Medidor de gasto vs receita
O sistema SHALL exibir um medidor das despesas do período (mês na visão Mensal, ano na visão Anual) com escala de 0 até o maior valor entre receitas e despesas, uma marca na receita, faixas até 60%, de 60% a 90% e acima de 90%, e o texto "{percentual}% das receitas" (ou "sem receitas no período").

#### Scenario: Comprometimento da receita
- **WHEN** no período as receitas são R$ 5.000 e as despesas R$ 4.600
- **THEN** o medidor mostra R$ 4.600 na faixa acima de 90% e o texto "92% das receitas"

### Requirement: Distribuição por categoria
O sistema SHALL exibir duas roscas do mês selecionado, "Despesas por categoria" e "Receitas por categoria", com o percentual de cada categoria e mensagens de estado vazio ("Sem despesas neste mês." / "Sem receitas neste mês.").

#### Scenario: Rosca de receitas
- **WHEN** as receitas do mês são Salário R$ 4.500 e Freelance R$ 500
- **THEN** a rosca de receitas mostra Salário 90% e Freelance 10%

### Requirement: Comparativo e totais anuais
O sistema SHALL exibir o gráfico "Comparativo mensal · {ano}" com barras de receitas e despesas e uma linha de saldo para os 12 meses, e os indicadores "Receitas anuais", "Despesas anuais" e "Saldo anual".

#### Scenario: Totais anuais
- **WHEN** em 2026 as receitas somam R$ 48.000 e as despesas R$ 39.000
- **THEN** os indicadores anuais mostram R$ 48.000,00, R$ 39.000,00 e R$ 9.000,00

### Requirement: Lançamentos do período
O sistema SHALL listar os lançamentos do mês selecionado, do mais recente ao mais antigo, até 40 itens; com mais itens, MUST informar "Mostrando 40 de {total} lançamentos.".

#### Scenario: Mais de 40 lançamentos
- **WHEN** o mês tem 55 lançamentos
- **THEN** a lista mostra 40 itens e o texto "Mostrando 40 de 55 lançamentos."

#### Scenario: Período sem lançamentos
- **WHEN** o mês não tem lançamentos
- **THEN** o sistema exibe "Nenhuma transação neste período. Cadastre em Transações."
