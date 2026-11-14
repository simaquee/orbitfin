## ADDED Requirements

### Requirement: Importação de extrato
O sistema SHALL oferecer o botão "Importar extrato" na página Transações, que aceita extratos bancários em PDF, CSV ou OFX. A leitura MUST acontecer no próprio app, sem IA e sem enviar o arquivo a serviços externos. Cada lançamento lido vira uma linha com data, descrição e valor; valores negativos são despesas e positivos são receitas.

#### Scenario: Extrato em CSV
- **WHEN** o usuário envia um CSV com o cabeçalho "Data;Descrição;Valor" e as linhas "05/11/2026;Mercado Bom Preço;-45,90" e "06/11/2026;Salário Empresa X;3.000,00"
- **THEN** o sistema lista 2 lançamentos: "Mercado Bom Preço" com R$ −45,90 (Despesa) e "Salário Empresa X" com R$ 3.000,00 (Receita)

#### Scenario: Extrato em OFX
- **WHEN** o usuário envia um OFX com uma transação `TRNAMT -120.50`, `DTPOSTED 20261103` e `MEMO CONTA DE LUZ`
- **THEN** o sistema lista "CONTA DE LUZ" em 03/11/2026 com R$ −120,50

#### Scenario: Extrato em PDF
- **WHEN** o usuário envia um PDF com a linha "07/11/2026 PIX ENVIADO JOAO 150,00- 1.200,00"
- **THEN** o sistema lista "PIX ENVIADO JOAO" em 07/11/2026 com R$ −150,00 e ignora o saldo R$ 1.200,00

#### Scenario: PDF escaneado
- **WHEN** o usuário envia um PDF sem texto (imagem digitalizada)
- **THEN** o sistema exibe "Não foi possível ler o texto deste PDF (pode ser uma imagem escaneada). Exporte o extrato em CSV ou OFX no app do banco."

#### Scenario: Formato não suportado
- **WHEN** o usuário envia um arquivo "extrato.xlsx"
- **THEN** o sistema exibe "Formato não suportado. Envie um extrato em PDF, CSV ou OFX."

### Requirement: Revisão dos lançamentos importados
Antes de gravar, o sistema SHALL exibir cada lançamento lido num card com a data, os campos editáveis "Descrição" e "Valor" e o botão "Confirmar" ao lado. Um card confirmado MUST travar seus campos e oferecer "Editar" para destravá-los. O botão "Descartar" SHALL remover o card da importação. O valor MUST ser diferente de zero para confirmar.

#### Scenario: Confirmar um card
- **WHEN** o usuário altera a descrição "PIX ENVIADO JOAO" para "Aluguel garagem" e clica em "Confirmar"
- **THEN** o card passa a mostrar "Confirmado" com os campos travados e a descrição "Aluguel garagem"

#### Scenario: Valor zero
- **WHEN** o usuário zera o valor de um card e clica em "Confirmar"
- **THEN** o sistema exibe "O valor deve ser diferente de zero." e o card continua pendente

### Requirement: Confirmação da importação
O sistema SHALL exibir, ao final da lista, o botão "Confirmar importação". Ele MUST ficar desabilitado enquanto existir algum card não confirmado ou nenhum card. Ao confirmar, todos os lançamentos são criados de uma vez como transações com status "Pago" e categoria "Outros", e o painel de importação é fechado.

#### Scenario: Card pendente bloqueia a importação
- **WHEN** a revisão tem 12 cards e 11 estão confirmados
- **THEN** "Confirmar importação" fica desabilitado e o sistema informa "Confirme todos os lançamentos para importar (falta 1)."

#### Scenario: Importação concluída
- **WHEN** os 12 cards estão confirmados e o usuário clica em "Confirmar importação"
- **THEN** as 12 transações aparecem na lista e o sistema exibe "12 transações importadas."

### Requirement: Criação em lote no backend
O backend SHALL oferecer `POST /transacoes/lote`, que recebe de 1 a 500 transações e as cria para o usuário autenticado. Todas as linhas MUST passar pelas mesmas regras de validação da criação unitária antes de qualquer gravação; se uma linha for inválida, nenhuma transação é criada.

#### Scenario: Lote válido
- **WHEN** o backend recebe 3 transações válidas
- **THEN** cria as 3 transações com o `user_id` do usuário autenticado e responde `{"criadas": 3}`

#### Scenario: Uma linha inválida
- **WHEN** o backend recebe 3 transações e a segunda tem valor 0
- **THEN** a operação é recusada com "O valor deve ser maior que zero." e nenhuma das 3 é criada
