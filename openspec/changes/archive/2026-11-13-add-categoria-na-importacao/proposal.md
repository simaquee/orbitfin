# Proposal

## Why

Em 13/11/2026, ao importar o extrato de outubro (129 lançamentos) o usuário não encontrou as transações: a lista de Transações abre sempre no mês atual (novembro) e a gravação, que tinha dado certo, parecia não ter acontecido. Além disso, toda linha importada entrava como "Outros", obrigando a recategorizar uma a uma depois.

## What Changes

- Categoria por lançamento já na leitura: a coluna de categoria do extrato (CSV), quando válida para o tipo; senão sugestão por palavras-chave da descrição (farmácia → Saúde, supermercado → Alimentação, condomínio/internet → Moradia, venda/serviços recebidos → Freelance etc.), sem IA; o resto fica em "Outros".
- Campo "Categoria" em cada card, ao lado do Valor, com as opções do tipo (despesa ou receita); "Confirmar" e "Confirmar tudo" levam a categoria escolhida.
- Após importar, o filtro Mês da lista vai para o mês do lançamento mais recente do extrato e a mensagem informa: "129 transações importadas. Mostrando out/2026.".

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `transacoes`: requisitos "Importação de extrato", "Revisão dos lançamentos importados" e "Confirmação da importação".

## Impact

- Frontend: `src/services/extrato.py` (`sugerir_categoria`, `mes_mais_recente`), `src/views/transacoes.py`. Sem mudança no Xano (o lote já recebia categoria).
- Testes: `tests/test_extrato.py` (117 no total).

## Fora do escopo

- Categorias personalizadas e aprendizado com as correções do usuário.
