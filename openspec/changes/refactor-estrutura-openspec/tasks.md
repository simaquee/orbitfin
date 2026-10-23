# Tasks

## 1. Código (frontend)

- [x] 1.1 Mover com `git mv`: `views/` → `commands/`; `services/` e `components/{dados,sessao}.py` → `core/`; peças visuais → `ui/` (`ui.py` → `blocos.py`); `formatacao.py` → `utils/`
- [x] 1.2 Reescrever os imports e confirmar que não restou `components.`, `services.`, `views.` nem `tests.`
- [x] 1.3 Mover `tests/` → `test/{core,ui,utils,helpers}` e ajustar `pyproject.toml` (`testpaths`, `pythonpath`)
- [x] 1.4 Rodar `pytest` (61 passando) e importar todas as telas
- [x] 1.5 Rodar o app, cadastrar um usuário e abrir as 5 páginas do menu sem erro

## 2. Documentação

- [x] 2.1 README enxuto; guias em `docs/` (início, arquitetura, publicação, fluxo OpenSpec)
- [x] 2.2 `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` e `scripts/README.md`
- [x] 2.3 Atualizar a seção de arquitetura do `openspec/config.yaml`

## 3. Publicação

- [x] 3.1 Confirmar com `xano workspace push --dry-run` que o backend não muda (requer Xano)
- [ ] 3.2 Push na `main` e verificação do app público
