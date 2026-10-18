# metas Specification

## Purpose
Mostra, para cada limite de categoria, quanto o usuário ainda pode gastar sem estourar o teto do mês e quanto conseguiu poupar das receitas, incentivando a contenção de gastos.

## Requirements

### Requirement: Status de contenção por categoria
Para cada orçamento do mês, o sistema SHALL calcular o restante (limite − gasto) e classificá-lo: "Teto atingido" quando o restante é menor ou igual a zero, "Em risco" quando o restante é de no máximo 10% do limite e "No caminho" nos demais casos.

#### Scenario: Em risco
- **WHEN** Saúde tem limite de R$ 200 e gasto de R$ 185
- **THEN** a meta de Saúde aparece como "Em risco" com "R$ 15,00 ainda cabem no teto"

#### Scenario: Teto atingido
- **WHEN** Transporte tem limite de R$ 400 e gasto de R$ 450
- **THEN** a meta aparece como "Teto atingido" com "Gastou R$ 450,00 de R$ 400,00 · ultrapassou R$ 50,00"

### Requirement: Barra de folga
A barra de cada meta SHALL representar a parcela do limite que ainda está disponível (restante ÷ limite, mínimo 0%), e a lista SHALL ser ordenada por: Em risco, Teto atingido, No caminho; dentro de cada grupo, da menor para a maior folga.

#### Scenario: Folga
- **WHEN** Educação tem limite de R$ 150 e gasto de R$ 30
- **THEN** a barra mostra 80% de folga e "R$ 120,00 / R$ 150,00"

### Requirement: Indicadores de metas
A página Metas SHALL exibir: "Poupança do mês" ((receitas − despesas) ÷ receitas × 100 do mês, ou 0% sem receitas), "Economia preservada" (soma dos restantes positivos), "No caminho" (quantidade) e "Atenção" (Em risco + Teto atingido).

#### Scenario: Poupança do mês
- **WHEN** em outubro de 2026 as receitas somam R$ 5.000 e as despesas R$ 3.500
- **THEN** "Poupança do mês" mostra "30%" com a dica "R$ 1.500,00 de saldo · out/2026"

#### Scenario: Mês sem receitas
- **WHEN** o mês não tem receitas
- **THEN** "Poupança do mês" mostra "0%"

### Requirement: Explicação e ajuste de meta
A página SHALL explicar que cada meta corresponde ao teto de gasto da categoria e SHALL permitir ajustar o teto, que altera o mesmo limite da página Orçamento.

#### Scenario: Ajuste pela página Metas
- **WHEN** o usuário altera o teto de Lazer para R$ 450 na página Metas
- **THEN** a página Orçamento também passa a mostrar o limite de Lazer como R$ 450,00
