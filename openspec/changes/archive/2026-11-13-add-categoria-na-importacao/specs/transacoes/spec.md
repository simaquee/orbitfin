## MODIFIED Requirements

### Requirement: Importação de extrato
O sistema SHALL oferecer o botão "Importar extrato" na página Transações, que aceita extratos bancários em PDF, CSV ou OFX. A leitura MUST acontecer no próprio app, sem IA e sem enviar o arquivo a serviços externos. Cada lançamento lido vira uma linha com data, descrição, valor e categoria; valores negativos são despesas e positivos são receitas. A categoria MUST vir da coluna de categoria do extrato quando ela existe e é válida para o tipo; senão o sistema sugere uma pelas palavras da descrição, sem IA; o que não for reconhecido fica em "Outros".

#### Scenario: Extrato em CSV
- **WHEN** o usuário envia um CSV com o cabeçalho "Data;Descrição;Valor" e as linhas "05/11/2026;Mercado Bom Preço;-45,90" e "06/11/2026;Salário Empresa X;3.000,00"
- **THEN** o sistema lista 2 lançamentos: "Mercado Bom Preço" com R$ −45,90 (Despesa) e "Salário Empresa X" com R$ 3.000,00 (Receita)

#### Scenario: Extrato em OFX
- **WHEN** o usuário envia um OFX com uma transação `TRNAMT -120.50`, `DTPOSTED 20261103` e `MEMO CONTA DE LUZ`
- **THEN** o sistema lista "CONTA DE LUZ" em 03/11/2026 com R$ −120,50

#### Scenario: Extrato em PDF
- **WHEN** o usuário envia um PDF com a linha "07/11/2026 PIX ENVIADO JOAO 150,00- 1.200,00"
- **THEN** o sistema lista "PIX ENVIADO JOAO" em 07/11/2026 com R$ −150,00 e ignora o saldo R$ 1.200,00

#### Scenario: Extrato em PDF no formato de tabela
- **WHEN** o usuário envia um PDF em que data, hora, descrição, valor e saldo aparecem em linhas separadas, como "01/10/2026" / "10:53" / "Pagamento de boleto - internet" / "-R$ 166,12" / "R$ 8.184,33"
- **THEN** o sistema lista "Pagamento de boleto - internet" em 01/10/2026 com R$ −166,12, ignora a hora e o saldo e não inclui cabeçalhos ou rodapés de página na descrição

#### Scenario: Categoria sugerida pela descrição
- **WHEN** o extrato traz "Compra débito - farmácia" com R$ −112,55 e "Venda recebida - cartão" com R$ 567,50
- **THEN** os cards vêm com as categorias "Saúde" e "Freelance"

#### Scenario: PDF escaneado
- **WHEN** o usuário envia um PDF sem texto (imagem digitalizada)
- **THEN** o sistema exibe "Não foi possível ler o texto deste PDF (pode ser uma imagem escaneada). Exporte o extrato em CSV ou OFX no app do banco."

#### Scenario: Formato não suportado
- **WHEN** o usuário envia um arquivo "extrato.xlsx"
- **THEN** o sistema exibe "Formato não suportado. Envie um extrato em PDF, CSV ou OFX."

### Requirement: Revisão dos lançamentos importados
Antes de gravar, o sistema SHALL exibir cada lançamento lido num card com a data, os campos editáveis "Descrição", "Valor" e "Categoria" (opções conforme o tipo: despesa ou receita) e o botão "Confirmar" ao lado. Um card confirmado MUST travar seus campos e oferecer "Editar" para destravá-los. O botão "Descartar" SHALL remover o card da importação. O valor MUST ser diferente de zero para confirmar.

#### Scenario: Confirmar um card
- **WHEN** o usuário altera a descrição "PIX ENVIADO JOAO" para "Aluguel garagem" e clica em "Confirmar"
- **THEN** o card passa a mostrar "Confirmado" com os campos travados e a descrição "Aluguel garagem"

#### Scenario: Alterar a categoria
- **WHEN** o usuário troca a categoria de um card de "Outros" para "Lazer" e confirma
- **THEN** a transação é importada com a categoria "Lazer"

#### Scenario: Valor zero
- **WHEN** o usuário zera o valor de um card e clica em "Confirmar"
- **THEN** o sistema exibe "O valor deve ser diferente de zero." e o card continua pendente

### Requirement: Confirmação da importação
O sistema SHALL exibir, ao final da lista, o botão "Confirmar importação". Ele MUST ficar desabilitado enquanto existir algum card não confirmado ou nenhum card. Ao confirmar, todos os lançamentos são criados de uma vez como transações com status "Pago" e a categoria escolhida em cada card. O painel de importação é fechado e a lista MUST passar a mostrar o mês do lançamento mais recente importado.

#### Scenario: Card pendente bloqueia a importação
- **WHEN** a revisão tem 12 cards e 11 estão confirmados
- **THEN** "Confirmar importação" fica desabilitado e o sistema informa "Confirme todos os lançamentos para importar (falta 1)."

#### Scenario: Importação concluída
- **WHEN** os 12 cards estão confirmados e o usuário clica em "Confirmar importação"
- **THEN** as 12 transações aparecem na lista e o sistema exibe "12 transações importadas. Mostrando nov/2026."

#### Scenario: Extrato de outro mês
- **WHEN** em novembro de 2026 o usuário importa os 129 lançamentos de um extrato de outubro
- **THEN** o sistema exibe "129 transações importadas. Mostrando out/2026." e o filtro Mês fica em "out/2026"
