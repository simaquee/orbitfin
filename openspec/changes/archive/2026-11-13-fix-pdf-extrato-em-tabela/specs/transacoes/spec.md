## MODIFIED Requirements

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

#### Scenario: Extrato em PDF no formato de tabela
- **WHEN** o usuário envia um PDF em que data, hora, descrição, valor e saldo aparecem em linhas separadas, como "01/10/2026" / "10:53" / "Pagamento de boleto - internet" / "-R$ 166,12" / "R$ 8.184,33"
- **THEN** o sistema lista "Pagamento de boleto - internet" em 01/10/2026 com R$ −166,12, ignora a hora e o saldo e não inclui cabeçalhos ou rodapés de página na descrição

#### Scenario: PDF escaneado
- **WHEN** o usuário envia um PDF sem texto (imagem digitalizada)
- **THEN** o sistema exibe "Não foi possível ler o texto deste PDF (pode ser uma imagem escaneada). Exporte o extrato em CSV ou OFX no app do banco."

#### Scenario: Formato não suportado
- **WHEN** o usuário envia um arquivo "extrato.xlsx"
- **THEN** o sistema exibe "Formato não suportado. Envie um extrato em PDF, CSV ou OFX."
