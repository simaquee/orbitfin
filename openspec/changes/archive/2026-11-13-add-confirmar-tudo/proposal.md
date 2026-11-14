# Proposal

## Why

Um extrato de mês inteiro tem dezenas ou centenas de lançamentos (o de teste do Mercado Pago tem 129). Confirmar card por card para liberar "Confirmar importação" é lento quando a leitura já está correta.

## What Changes

- Botão "Confirmar tudo" ao lado do resumo da revisão: confirma todos os cards pendentes com os valores atuais dos campos.
- Cards com valor zero continuam pendentes, com aviso.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `transacoes`: novo requisito "Confirmar todos os lançamentos" na revisão da importação.

## Impact

- Frontend: `src/views/transacoes.py`, `src/services/extrato.py` (`confirmar_todas`). Sem mudança no Xano.
- Testes: `tests/test_extrato.py` (1 novo; 104 no total).

## Fora do escopo

- "Descartar tudo" e seleção de vários cards.