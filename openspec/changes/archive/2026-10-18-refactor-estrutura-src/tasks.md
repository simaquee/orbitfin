# Tasks

## 1. Reorganização

- [x] 1.1 Mover `app.py`, `components/`, `views/`, `services/` para `src/` e `xano/` para `src/xano/`, e verificar que a raiz contém apenas `openspec/`, `src/`, `tests/`, `.streamlit/`, `.claude/` e arquivos de configuração
- [x] 1.2 Criar `pyproject.toml` com `pythonpath = ["src", "."]` para o pytest, remover o ajuste de `sys.path` de `tests/conftest.py`, e verificar que `pytest` passa com os mesmos 59 testes

## 2. Documentação

- [x] 2.1 Atualizar `README.md` e `openspec/config.yaml` com os novos caminhos e comandos, e verificar com busca que não restam referências a `streamlit run app.py` nem a `-d ./xano`
- [x] 2.2 Atualizar os caminhos citados nos artefatos das mudanças em andamento e verificar com `openspec validate --all --strict`

## 3. Verificação

- [x] 3.1 Subir o app com `streamlit run src/app.py` e verificar com o teste de ponta a ponta (Xano simulado) que todos os fluxos continuam passando
