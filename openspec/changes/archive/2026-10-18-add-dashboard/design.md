# Design

## Context

Consome `GET /transacoes` (`add-transacoes`) e `GET /budgets?inicio=&fim=` (`add-orcamentos`). O original tinha a tabela `insight` com um único texto por usuário, gravado no cadastro e nunca atualizado, e um endpoint `/saldo` que não era usado.

## Goals / Non-Goals

**Goals:**
- Todo cálculo do Dashboard em funções puras e testáveis.
- Sugestões úteis sem custo nem dependência externa.

**Non-Goals:**
- Endpoints agregados no Xano para o Dashboard.

## Decisions

- **Saldo só com pagos; totais do mês com pagos e pendentes.** O saldo segue a regra de negócio do original ("despesa subtrai do saldo quando pago"). Os totais do mês mostram o compromisso real e destacam o pendente na dica. Alternativa considerada: ignorar o status como o código original fazia, descartada por contrariar a especificação de negócio.
- **Duas chamadas por carregamento** (`/transacoes` e `/budgets`), feitas uma vez por renderização e reaproveitadas pelos blocos da tela.
- **`src/services/sugestoes.py`** com `gerar_sugestoes(transacoes, orcamentos, hoje) -> list[str]`: regras ordenadas, corte em 3 e textos formatados por `src/services/formatacao.py`.
- **Sem tabela `insight` nem endpoints `/insights` e `/saldo`.** As sugestões são derivadas dos dados e não precisam ser guardadas.
- **Plotly com a paleta oficial:** linhas Azul Marinho/Terracota; rosca com tons da paleta (Terracota, Azul Marinho e variações de opacidade de cada um), sem cores fora da paleta.

## Risks / Trade-offs

- [Rosca com mais de 4 categorias e só 2 cores-base] → usar variações de opacidade e rótulos com percentual; a legenda identifica cada fatia.
- [Sugestões repetitivas] → aceito no MVP; regras novas podem entrar em mudanças futuras.
