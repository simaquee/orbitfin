# Tasks

## 1. Backend (requer Xano)

- [x] 1.1 Nenhuma mudança no Xano (o endpoint `POST /transacoes/lote` continua igual)

## 2. Frontend

- [x] 2.1 Leitura de PDF por blocos em `src/services/extrato.py` (`_pdf_por_bloco`) e escolha automática entre os dois modos
- [x] 2.2 Conferir com o PDF real: 129 lançamentos, entradas R$ 63.638,84, saídas −R$ 14.494,87 e saldo final R$ 57.494,42, iguais ao resumo do extrato
- [x] 2.3 Teste do formato de tabela em `tests/test_extrato.py`; `pytest` passando (103)

## 3. Documentação

- [x] 3.1 README: formatos de PDF aceitos
