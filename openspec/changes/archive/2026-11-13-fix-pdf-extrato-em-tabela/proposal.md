# Proposal

## Why

Em 13/11/2026 o extrato de teste `extrato_mercado_pago_simulado_outubro_2026.pdf` (129 lançamentos) era recusado com "Nenhum lançamento encontrado no arquivo.". O `pypdf` extrai esse PDF em formato de tabela: data, hora, descrição, valor (`-R$ 166,12`) e saldo, cada um em uma linha. A leitura de PDF só reconhecia lançamentos com todos os campos na mesma linha.

## What Changes

- A leitura de PDF ganha um segundo modo, por blocos: uma linha só com data (com ou sem hora) abre um lançamento; a hora é ignorada; o texto até o primeiro valor é a descrição; o primeiro valor é a movimentação e o segundo (saldo) é descartado.
- O app roda os dois modos (por linha e por bloco) e fica com o que encontrar mais lançamentos.
- Valores com sinal antes do símbolo (`-R$ 166,12`, `+R$ 10,00`) passam a ser reconhecidos como valor isolado.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `transacoes`: o requisito "Importação de extrato" ganha o cenário de PDF em formato de tabela.

## Impact

- Frontend: `src/services/extrato.py` (sem mudança de tela nem de backend).
- Testes: `tests/test_extrato.py` (1 novo; 103 no total).
- Documentação: `README.md`.

## Fora do escopo

- PDF escaneado (imagem), que continua exigindo CSV ou OFX.
- Layouts em que a descrição vem depois do valor.
