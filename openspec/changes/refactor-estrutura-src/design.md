# Design

## Context

Ver proposal.md. Os imports Python são absolutos a partir da pasta do app (`from components import ...`, `from services.api import ...`). O Streamlit coloca a pasta do script principal no `sys.path`, então esses imports continuam funcionando com `streamlit run src/app.py`, sem renomear nada.

## Goals / Non-Goals

**Goals:**
- Raiz do repositório com: `openspec/`, `src/`, `tests/`, `.streamlit/`, `README.md`, `pyproject.toml`, `requirements.txt`.

**Non-Goals:**
- Transformar o app em pacote instalável (`pip install -e .`).

## Decisions

- **Estrutura final:**
  ```
  orbitfin/
  ├── openspec/            # OpenSpec (formato exigido pela CLI)
  │   ├── config.yaml
  │   ├── specs/           # specs consolidadas (preenchidas pelo archive)
  │   └── changes/         # mudanças ativas + archive/
  ├── src/                 # todo o código-fonte
  │   ├── app.py
  │   ├── components/
  │   ├── views/
  │   ├── services/
  │   └── xano/            # backend XanoScript
  ├── tests/
  ├── .streamlit/          # config.toml + secrets (na raiz: exigência do Streamlit)
  ├── pyproject.toml
  ├── requirements.txt
  └── README.md
  ```
- **Imports sem prefixo `src.`.** Mantém o código inalterado. O pytest recebe `pythonpath = ["src", "."]` no `pyproject.toml` (o `.` mantém `from tests.fakes import ...`). Alternativa considerada: imports `from src.services...`, descartada por exigir editar todos os arquivos e quebrar o `streamlit run`.
- **Backend em `src/xano/`.** O Xano CLI aceita qualquer pasta via `-d`.

## Risks / Trade-offs

- [Documentos citando caminhos antigos] → atualizar config.yaml, README e os artefatos das mudanças em andamento na mesma mudança.
- [Comando antigo `streamlit run app.py` deixa de funcionar] → README atualizado.
