# Design

## Context

Ver proposal.md. O OpenSpec é uma CLI em TypeScript; o OrbitFin é um app Streamlit em Python. A organização é adotada onde há equivalente direto e documentada onde não há.

## Goals / Non-Goals

**Goals:**
- Mesmo mapa de pastas do repositório do OpenSpec, com responsabilidades equivalentes.
- Histórico preservado (`git mv`) e nenhuma mudança de comportamento.

**Non-Goals:**
- Renomear funções, telas ou textos da interface.

## Decisions

- **Mapa de equivalência:**

  | OpenSpec | OrbitFin |
  |---|---|
  | `src/index.ts` | `src/app.py` (entrypoint, inalterado) |
  | `src/commands/` | telas (login, cadastro, dashboard, transações, orçamento, metas, relatórios) |
  | `src/core/` | cliente do Xano, cálculos, categorias, sugestões, validação, dados e sessão |
  | `src/ui/` | tema, barra lateral, cabeçalho, blocos, gráficos e seletores |
  | `src/utils/` | formatação pt-BR |
  | `test/<área>/` | testes espelhando `src/` |
  | `docs/`, `scripts/README.md`, `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` | mesmos papéis |

- **`dados.py` e `sessao.py` em `core/`:** carregam dados e guardam o estado da sessão; não desenham nada.
- **`components/ui.py` → `ui/blocos.py`:** evita o módulo `ui.ui`; "blocos de UI" já era a descrição usada no README.
- **Auxiliares de teste como `helpers.fakes`:** `test` é o nome de um pacote da biblioteca padrão do Python; importar `test.helpers` dependeria da ordem do `sys.path`. Com `test/` no `pythonpath`, o import é `from helpers.fakes import ...`.
- **Imports reescritos por regra explícita** (módulo antigo → novo), com verificação de que não sobra nenhum import antigo.

## Risks / Trade-offs

- Import esquecido quebra uma tela só quando ela é aberta → mitigação: importar todas as telas no teste, rodar `pytest` e abrir as 5 páginas do menu com um usuário real antes do push.
