# OrbitFin

Organizador financeiro pessoal (identidade Grupo Marte): receitas e despesas, limites por categoria, metas de contenção, dashboard com sugestões automáticas e relatórios.

**Produção:** <https://orbitfin-tech.streamlit.app>

- **Frontend:** Python + Streamlit + Plotly
- **Backend:** Xano (API REST + PostgreSQL + JWT), versionado em XanoScript em `src/xano/`
- **Metodologia:** [OpenSpec](https://openspec.dev), com a mesma organização de pastas do [repositório do OpenSpec](https://github.com/Fission-AI/OpenSpec)

## Início rápido

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run src/app.py
pytest
```

Passo a passo completo, incluindo o backend no Xano: [docs/getting-started.md](docs/getting-started.md).

## Estrutura

```
orbitfin/
├── openspec/            # specs por capacidade e changes (formato da CLI do OpenSpec)
├── src/
│   ├── app.py           # entrypoint e roteamento
│   ├── commands/        # telas: login, cadastro, dashboard, transações, orçamento, metas, relatórios
│   ├── core/            # cliente do Xano, cálculos, categorias, sugestões, validação, dados, sessão
│   ├── ui/              # tema, barra lateral, cabeçalho, blocos, gráficos, seletores
│   ├── utils/           # formatação pt-BR
│   └── xano/            # backend: tabelas, endpoints e funções em XanoScript
├── test/                # pytest espelhando src/ (core, ui, utils) + helpers
├── docs/                # guias
├── scripts/             # teste de integração contra o Xano real
├── .streamlit/          # config.toml (tema) e secrets.toml (não versionado)
├── AGENTS.md            # instruções para agentes de IA
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── PRODUCT.md           # contexto de produto (skill de design Impeccable)
```

## Documentação

| Guia | Conteúdo |
|---|---|
| [docs/getting-started.md](docs/getting-started.md) | Backend no Xano, frontend local e testes |
| [docs/architecture.md](docs/architecture.md) | O que fica em cada pasta e regras de dependência |
| [docs/deployment.md](docs/deployment.md) | Produção e o que fazer se o app parar de funcionar |
| [docs/workflow.md](docs/workflow.md) | Fluxo OpenSpec: propor, aplicar e arquivar mudanças |

As especificações oficiais do sistema ficam em [`openspec/specs/`](openspec/specs): 8 capacidades (`interface-base`, `autenticacao`, `transacoes`, `orcamentos`, `metas`, `dashboard`, `sugestoes`, `relatorios`).
