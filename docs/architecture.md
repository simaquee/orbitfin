# Arquitetura

A organização segue a do [repositório do OpenSpec](https://github.com/Fission-AI/OpenSpec), adaptada a um app Streamlit em Python.

| Pasta | Equivalente no OpenSpec | Conteúdo |
|---|---|---|
| `src/app.py` | `src/index.ts` | Entrypoint: configura a página, aplica o tema e roteia para a tela certa |
| `src/commands/` | `src/commands/` | Uma tela por arquivo: `login`, `cadastro`, `dashboard`, `transacoes`, `orcamento`, `metas`, `relatorios` |
| `src/core/` | `src/core/` | `api` (único ponto de I/O com o Xano), `calculos`, `categorias`, `sugestoes`, `validacao`, `dados` (carregamento com cache) e `sessao` (estado do usuário) |
| `src/ui/` | `src/ui/` | `theme`, `sidebar`, `header`, `blocos` (cartões, KPIs, linhas), `graficos` (Plotly) e `seletores` |
| `src/utils/` | `src/utils/` | `formatacao`: moeda, datas e meses em pt-BR |
| `src/xano/` | (sem equivalente) | Backend em XanoScript: `table/`, `api/orbitfin/`, `function/orbitfin/` |
| `test/` | `test/` | Testes espelhando `src/`: `core/`, `ui/`, `utils/`; auxiliares em `helpers/` |
| `scripts/` | `scripts/` | Teste de integração contra o Xano real |
| `docs/` | `docs/` | Guias |
| `openspec/` | `openspec/` | Specs por capacidade e changes |

Pastas do OpenSpec sem equivalente aqui: `bin/`, `schemas/`, `website/`, `docs-lab/`, `assets/`, `skills/` e os arquivos de build do Node.

## Regras de dependência

- `commands/` pode importar `core/`, `ui/` e `utils/`.
- `ui/` pode importar `utils/` e `core/` (para dados), nunca `commands/`.
- `core/` não importa `ui/` nem `commands/`. Regras de cálculo são funções puras em `core/`, nunca dentro das telas.
- `utils/` não importa nada do projeto.
- Imports sem prefixo `src.`: o `pythonpath` do `pyproject.toml` inclui `src/` (código) e `test/` (para `from helpers.fakes import ...`).

## Dados e segurança

- Toda rota de dados exige `Authorization: Bearer <token>` e isola os dados por `user_id` no Xano.
- A URL do Xano fica só em `.streamlit/secrets.toml` (fora do Git); versiona-se apenas `secrets.toml.example`.
