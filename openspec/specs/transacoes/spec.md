# transacoes Specification

## Purpose
Permite que o usuário registre e gerencie suas receitas e despesas, que são a base de todos os indicadores, orçamentos e relatórios do OrbitFin.

## Requirements

### Requirement: Campos de uma transação
Uma transação SHALL ter tipo (receita ou despesa), valor, data, categoria, descrição opcional e status (pago ou pendente).

#### Scenario: Valores padrão do formulário
- **WHEN** o usuário abre o formulário "Nova transação" em 18/10/2026
- **THEN** o tipo vem como "Despesa", a data como 18/10/2026 e o status como "Pago"

### Requirement: Categorias padronizadas
A categoria MUST ser escolhida numa lista fixa conforme o tipo. Despesa: Alimentação, Moradia, Transporte, Lazer, Saúde, Educação, Outros. Receita: Salário, Freelance, Investimentos, Outros.

#### Scenario: Categorias de despesa
- **WHEN** o usuário seleciona o tipo "Despesa" no formulário
- **THEN** o seletor de categoria oferece exatamente as 7 categorias de despesa

#### Scenario: Troca de tipo
- **WHEN** o usuário troca o tipo de "Despesa" para "Receita"
- **THEN** o seletor passa a oferecer Salário, Freelance, Investimentos e Outros

### Requirement: Validação de transações
O sistema MUST rejeitar, tanto na criação quanto na edição, valores menores ou iguais a zero, tipos ou status fora dos permitidos e categorias que não pertencem ao tipo escolhido. O backend MUST aplicar as mesmas regras.

#### Scenario: Valor zero
- **WHEN** o usuário tenta salvar uma transação com valor R$ 0,00
- **THEN** o sistema exibe "O valor deve ser maior que zero." e não salva

#### Scenario: Categoria incompatível no backend
- **WHEN** o backend recebe uma despesa com a categoria "Salário"
- **THEN** a operação é recusada com a mensagem "Categoria inválida para o tipo informado."

### Requirement: Registro de transação
O sistema SHALL permitir adicionar uma transação pelo botão "Adicionar transação", que abre o formulário "Nova transação".

#### Scenario: Nova despesa
- **WHEN** o usuário adiciona uma despesa de R$ 45,90, em 18/10/2026, categoria Alimentação, descrição "Mercado", status Pago
- **THEN** a transação aparece na lista com "− R$ 45,90" em Terracota

### Requirement: Listagem e filtros
O sistema SHALL listar as transações do usuário da mais recente para a mais antiga, com filtros combináveis: mês (padrão: mês atual, com a opção "Todos"), tipo (Todos, Receita, Despesa), status (Todos, Pago, Pendente) e categoria (Todas mais as categorias existentes).

#### Scenario: Filtro por mês e tipo
- **WHEN** o usuário filtra "out/2026" e "Despesa"
- **THEN** somente despesas com data em outubro de 2026 são exibidas

#### Scenario: Nenhum resultado
- **WHEN** nenhum lançamento atende aos filtros
- **THEN** o sistema exibe "Nenhuma transação com esses filtros."

#### Scenario: Usuário sem transações
- **WHEN** o usuário ainda não registrou nenhuma transação
- **THEN** o sistema exibe "Nenhuma transação ainda. Clique em Adicionar transação para começar."

#### Scenario: Linha da lista
- **WHEN** uma receita pendente de R$ 3.000,00 (Salário, 05/10/2026, "Empresa X") é listada
- **THEN** a linha mostra "Salário", o selo "PENDENTE", "05/10/2026 · Empresa X" e "+ R$ 3.000,00" em Azul Marinho

### Requirement: Indicadores do filtro
Acima da lista, o sistema SHALL exibir os totais das transações filtradas: "Receitas", "Despesas" e "Saldo filtrado" (receitas − despesas), cada um com a quantidade de lançamentos considerados.

#### Scenario: Totais do filtro
- **WHEN** o filtro contém receitas de R$ 3.000,00 (1 lançamento) e despesas de R$ 1.250,00 (4 lançamentos)
- **THEN** os indicadores mostram "R$ 3.000,00 · 1 no filtro", "R$ 1.250,00 · 4 no filtro" e saldo filtrado "R$ 1.750,00"

### Requirement: Edição de transação
O sistema SHALL permitir editar qualquer campo de uma transação do usuário num formulário pré-preenchido.

#### Scenario: Marcar como pago
- **WHEN** o usuário edita uma despesa pendente e altera o status para "Pago"
- **THEN** a transação passa a exibir o selo "PAGO"

### Requirement: Exclusão de transação
O sistema SHALL exigir confirmação antes de excluir uma transação, informando que a ação não pode ser desfeita.

#### Scenario: Confirmar exclusão
- **WHEN** o usuário clica em "Excluir" numa transação e confirma em "Excluir lançamento?"
- **THEN** a transação é removida da lista

#### Scenario: Cancelar exclusão
- **WHEN** o usuário cancela a confirmação
- **THEN** a transação permanece na lista

### Requirement: Isolamento por usuário
O backend MUST permitir listar, editar e excluir apenas as transações do usuário autenticado.

#### Scenario: Transação de outro usuário
- **WHEN** um usuário tenta editar ou excluir uma transação de outro usuário
- **THEN** o backend recusa com "Transação não encontrada." sem revelar que ela existe
