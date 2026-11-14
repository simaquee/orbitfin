# Proposal

## Why

Hoje cada lançamento entra no OrbitFin pelo formulário "Nova transação", um por vez. Quem quer registrar o mês inteiro precisa redigitar o extrato do banco linha a linha. Os bancos já entregam esse extrato em arquivo (PDF, CSV ou OFX); o app deve aproveitar esse arquivo e deixar o usuário só revisar e confirmar.

## What Changes

- Botão "Importar extrato" na página Transações, ao lado de "Adicionar transação".
- Leitura do extrato no próprio app, sem IA e sem serviço externo, em três formatos:
  - **CSV**: separador e colunas (data, descrição, valor ou crédito/débito) detectados pelo cabeçalho;
  - **OFX**: blocos `STMTTRN` (data, valor e descrição);
  - **PDF**: texto extraído localmente com `pypdf` e convertido em linhas data · descrição · valor.
- Revisão: cada lançamento lido vira um card com os campos **Descrição** e **Valor** editáveis e o botão **Confirmar** ao lado (e **Descartar** para tirar uma linha da importação).
- Botão final **Confirmar importação**, desabilitado enquanto houver card não confirmado.
- Backend: novo endpoint `POST /transacoes/lote` que cria várias transações de uma vez, com as mesmas regras de validação, tudo ou nada.

## Capabilities

### New Capabilities
<!-- Nenhuma: a importação faz parte da capacidade de transações. -->

### Modified Capabilities
- `transacoes`: ganha a importação de extrato e a criação em lote.

## Impact

- Backend: `src/xano/api/orbitfin/transacoes/lote_POST.xs` (novo); reaproveita `OrbitFin/validar_transacao`.
- Frontend: `src/views/transacoes.py`, `src/services/extrato.py` (novo), `src/services/api.py`.
- Dependência nova: `pypdf` (leitura local de PDF, pura Python).
- Testes: `tests/test_extrato.py` (novo), `tests/test_api.py`, `scripts/teste_integracao.py`.

## Fora do escopo

- Leitura de PDF escaneado (imagem): exige OCR; o app orienta exportar em CSV ou OFX.
- Categorização automática: toda linha importada entra como categoria "Outros" (válida para receita e despesa) e pode ser editada depois.
- Detecção de lançamentos duplicados (importar o mesmo extrato duas vezes cria duplicatas).
- Extratos de cartão de crédito com sinal invertido e extratos de investimentos.
- Exportar transações do OrbitFin para arquivo.
