# Design

## Context

Usa `src/services/api.py`, os componentes de UI da fundação e a sessão de `add-autenticacao`. No original, a tabela `transacao` do Xano já tinha o formato abaixo, com categoria em texto livre.

## Goals / Non-Goals

**Goals:**
- Categorias consistentes entre transações e orçamentos.
- Cálculos de totais em funções puras e testáveis.

**Non-Goals:**
- Filtro e agregação no servidor; o cliente filtra a lista completa do usuário.

## Decisions

- **Tabela `transacao`:** `id`, `created_at`, `user_id` (FK `user`), `tipo` enum(receita, despesa), `valor` decimal, `data` date, `categoria` text, `descricao` text opcional, `status` enum(pago, pendente). Índices em `user_id` e `data`.
- **Endpoints (grupo `orbitfin`, todos com `auth = "user"`):**
  - `GET /transacoes` → lista do usuário ordenada por `data` desc.
  - `POST /transacoes` → cria.
  - `PUT /transacoes/{id}` → edita.
  - `DELETE /transacoes/{id}` → `{success: true}`.
- **Registro de outro usuário responde "não encontrado".** O original respondia "não pertence ao usuário", o que revelava que o id existia.
- **Lista de categorias em dois lugares:** `src/services/categorias.py` (cliente) e uma validação no backend (precondition com a lista por tipo). Alternativa considerada: tabela `categoria` no Xano, adiada para a mudança futura de categorias personalizadas.
- **`src/services/calculos.py`** com funções puras (`filtrar`, `totais`) usadas pela página e reaproveitadas pelo dashboard e pelos relatórios.
- **Formulário em `st.dialog`.** O seletor de categoria depende do tipo, então o tipo fica fora do `st.form` para atualizar as opções na hora.

## Risks / Trade-offs

- [Lista de categorias duplicada no cliente e no backend] → teste no cliente comparando com a lista documentada na spec; mudanças futuras devem alterar os dois lados.
- [Carregar todas as transações a cada página] → aceitável para uso pessoal; pode virar paginação se necessário.
