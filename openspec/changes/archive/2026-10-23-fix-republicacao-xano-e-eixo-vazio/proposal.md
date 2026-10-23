# Proposal

## Why

Em 23/10/2026 o app publicado (orbitfin-tech.streamlit.app) não funcionava: o grupo de API `api:orbitfingm` não existia mais no Xano e todos os endpoints respondiam 404. Ao preparar a republicação, o `xano workspace push --dry-run` apontou duas operações destrutivas: a tabela `user` do workspace, criada pelo Quick Start do Xano e usada pela API `authentication` do mesmo workspace, perderia os campos `role` e `password_reset`.

Na mesma verificação, o gráfico "Receitas vs despesas" de um usuário sem lançamentos mostrava o eixo Y com rótulos repetidos ("R$ 1", "R$ 1", "R$ 0", "R$ −1", "R$ −1").

## What Changes

- `src/xano/table/user.xs` passa a declarar os mesmos campos do workspace (`role`, `password_reset`, `email` e `password` opcionais), para o push não remover dados nem quebrar a API `authentication`. A obrigatoriedade de e-mail e senha do OrbitFin continua garantida pelo endpoint `register`.
- Backend republicado no workspace "Gabriel's Workspace" da instância `x8ki-letl-twmt`.
- Gráficos de linhas e barras sem nenhum valor usam o eixo Y fixo de R$ 0 a R$ 100.
- Novo `scripts/teste_integracao.py`: percorre cadastro, login, transações e orçamentos contra o Xano real.
- README com o guia de recuperação do app.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `dashboard`: o gráfico "Receitas vs despesas" ganha o cenário sem lançamentos no período.

## Impact

- Backend: `src/xano/table/user.xs` (sem mudança de comportamento da API do OrbitFin).
- Frontend: `src/components/graficos.py` (afeta todos os gráficos que passam por `_layout`).
- Testes: `tests/test_graficos.py` (2 novos; 61 no total) e `scripts/teste_integracao.py`.
- Documentação: `README.md`.
