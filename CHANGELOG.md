# Changelog

## 2026-10-23

- Estrutura de pastas igual à do repositório do OpenSpec: `src/{commands,core,ui,utils}`, `test/`, `docs/`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md` (change `refactor-estrutura-openspec`).
- Backend republicado no Xano sem perda de dados: `user.xs` preserva `role` e `password_reset` do Quick Start (change `fix-republicacao-xano-e-eixo-vazio`).
- Gráficos sem dados usam o eixo de R$ 0 a R$ 100, sem rótulos repetidos.
- Teste de integração contra o Xano real (`scripts/teste_integracao.py`) e guia de recuperação do app.

## 2026-10-18

- Primeira versão: app Streamlit e backend Xano com autenticação, transações, orçamentos, metas, dashboard com sugestões e relatórios (8 changes arquivadas).
- Publicação no Streamlit Community Cloud (orbitfin-tech.streamlit.app) e no Xano (`api:orbitfingm`).
- Auditoria e polimento de design com a skill Impeccable.
