# Design

## Context

No original, `GET /budgets` já devolvia `gastoAtual` e `percentual` (de todo o histórico), mas as páginas Orçamento e Metas ignoravam esses campos e recalculavam no cliente. Este clone usa a tabela `transacao` e as categorias de `add-transacoes`.

## Goals / Non-Goals

**Goals:**
- Uma única fonte de cálculo do gasto do mês, usada por Orçamento, Metas e Dashboard.

**Non-Goals:**
- Histórico de limites por mês.

## Decisions

- **Tabela `budget`:** `id`, `updated_at`, `user_id` (FK), `categoria` text, `limite` decimal; índice único (`user_id`, `categoria`).
- **`GET /budgets?inicio=AAAA-MM-DD&fim=AAAA-MM-DD`** (primeiro e último dia do mês, calculados pelo cliente).
  - Cria os 7 orçamentos padrão se o usuário não tiver nenhum (*seed* preguiçoso, como no original). Assim o cadastro não precisa conhecer orçamentos.
  - Devolve `[{id, categoria, limite, gasto, percentual}]` com o gasto das despesas entre `inicio` e `fim`.
  - Datas explícitas evitam aritmética de calendário em XanoScript e problemas de fuso horário.
- **`PUT /budgets/{id} {limite}`:** valida `limite > 0` e a posse. Um orçamento de outro usuário responde "não encontrado".
- **Classificação no cliente:** `src/services/calculos.py` recebe a lista do endpoint e aplica as regras puras `estado_orcamento` (85% / estouro) e `status_meta` (10% / teto). Assim as regras de UI ficam testáveis sem Xano.
- **Pendentes contam no gasto do orçamento.** Uma despesa pendente já é dinheiro comprometido. Isso é diferente do saldo (ver `add-dashboard`), que considera apenas lançamentos pagos.
- **Metas fiel ao original, como uma visão sobre `budget`:** não há tabela própria. Metas de acúmulo ficam para uma mudança futura (ver o "Fora do escopo" na proposta).

## Risks / Trade-offs

- [Fuso horário no cálculo do mês] → o cliente sempre envia `inicio` e `fim` explicitamente.
- [Usuários confundirem Metas com metas de acúmulo] → texto explicativo fixo na página (requisito da spec).
