# Proposal

## Why

Hoje o código-fonte fica espalhado pela raiz do repositório (`app.py`, `views/`, `components/`, `services/`, `xano/`), misturado com configuração, testes e o OpenSpec. Isso dificulta enxergar o que é código do sistema e o que é apoio. Concentrar todo o código-fonte em `src/` deixa a raiz só com planejamento (`openspec/`), testes e configuração.

## What Changes

- Mover o frontend (`app.py`, `views/`, `components/`, `services/`) para `src/`.
- Mover o backend XanoScript (`xano/`) para `src/xano/`.
- Adicionar `pyproject.toml` com a configuração do pytest (`pythonpath`), substituindo o ajuste manual de `sys.path` nos testes.
- Atualizar README, `openspec/config.yaml` e os caminhos citados nos artefatos das mudanças em andamento.
- Nenhum comportamento muda: specs, telas, endpoints e regras continuam idênticos.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
<!-- Nenhuma: reorganização de pastas, sem mudança de comportamento (skip_specs: true). -->

## Impact

- Comando para rodar o app: `streamlit run src/app.py`.
- Comandos do Xano CLI: `xano workspace push -d ./src/xano`.
- `.streamlit/` continua na raiz, porque o Streamlit procura essa pasta no diretório onde o comando é executado.

## Fora do escopo

- Renomear `openspec/` para `.openspec/` ou mudar a estrutura interna dele: a CLI do OpenSpec só reconhece `openspec/specs/<capacidade>/spec.md` e `openspec/changes/<mudança>/`.
- Qualquer alteração de comportamento ou de visual.
