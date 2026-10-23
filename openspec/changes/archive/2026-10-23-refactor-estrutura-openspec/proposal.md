# Proposal

## Why

O repositório deve ter a mesma organização do repositório do OpenSpec (github.com/Fission-AI/OpenSpec), para que quem conhece o OpenSpec encontre cada coisa no mesmo lugar: código em `src/` dividido em `commands/`, `core/`, `ui/` e `utils/`, testes em `test/` espelhando `src/`, guias em `docs/` e os arquivos-padrão da raiz (`AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`).

## What Changes

- `src/views/` → `src/commands/` (uma tela por arquivo, como os comandos do OpenSpec).
- `src/services/` (exceto formatação) e o estado/dados de `src/components/` (`dados.py`, `sessao.py`) → `src/core/`.
- Peças visuais de `src/components/` → `src/ui/`; `components/ui.py` passa a se chamar `ui/blocos.py`.
- `src/services/formatacao.py` → `src/utils/formatacao.py`.
- `tests/` → `test/` com subpastas `core/`, `ui/`, `utils/` e `helpers/` (auxiliares).
- README enxuto na raiz; guias em `docs/`; `scripts/README.md`; `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md` e `SECURITY.md`.
- `openspec/config.yaml` atualizado com a nova estrutura.

Fora do escopo:
- Pastas do OpenSpec sem equivalente num app Streamlit em Python: `bin/`, `schemas/`, `website/`, `docs-lab/`, `assets/`, `skills/` e arquivos de build do Node.
- `LICENSE`: a escolha da licença é do dono do repositório.
- Mover `src/app.py` (o Streamlit Cloud está configurado para esse caminho) ou `.streamlit/` (lido na raiz).
- Mover `src/xano/` (caminho usado pelo Xano CLI e pela documentação de publicação).
- Qualquer mudança de comportamento.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
<!-- Nenhuma: reorganização de pastas e documentação, sem mudança de requisitos. -->

## Impact

- Imports: `components.*`, `services.*` e `views.*` passam a `ui.*`, `core.*`, `utils.*` e `commands.*`.
- `pyproject.toml`: `testpaths = ["test"]`, `pythonpath = ["src", "test"]`.
- Deploy: nenhum ajuste no Streamlit Cloud nem no Xano.
