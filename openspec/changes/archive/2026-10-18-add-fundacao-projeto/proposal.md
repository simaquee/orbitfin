# Proposal

## Why

O OrbitFin está sendo reconstruído do zero a partir do projeto de referência. Antes de qualquer funcionalidade, é preciso uma base comum: estrutura de pastas, conexão configurável com o backend Xano, cliente HTTP com tratamento de erros padronizado e a casca visual (tema, navegação e cabeçalho) que todas as telas vão reutilizar. Esta é a primeira mudança da sequência; as demais dependem dela.

## What Changes

- Estrutura do projeto Python/Streamlit (`src/app.py`, `src/views/`, `src/components/`, `src/services/`, `tests/`) e da pasta `src/xano/` para o backend em XanoScript.
- Configuração do Xano via `.streamlit/secrets.toml` (com `secrets.toml.example` versionado e `.gitignore` adequado).
- Cliente HTTP único para o Xano: URL base vinda dos secrets, envio do token Bearer, timeout, indicador de carregamento e mensagens de erro em português.
- Tema visual com a paleta oficial do Grupo Marte (Terracota `#E05638`, Azul Marinho `#1A2238`, Cinza Claro `#F4F6F8`, Branco) e ícones Flaticon UIcons.
- Barra lateral de navegação (Dashboard, Transações, Orçamento, Metas, Relatórios) e cabeçalho por página.
- Utilitários de formatação: moeda BRL (`R$ 1.234,56`, incluindo negativos `-R$ 1.234,56`) e meses em português (`out/2026`).

## Capabilities

### New Capabilities
- `interface-base`: casca visual e comportamentos transversais da aplicação: identidade visual, navegação, cabeçalho, formatação de valores e datas, comunicação com o backend e feedback de erro/carregamento.

### Modified Capabilities
<!-- Nenhuma: projeto novo. -->

## Impact

- Cria toda a estrutura inicial do repositório `D:\orbitfin`.
- Dependências Python: `streamlit`, `requests`, `pandas`, `plotly`, `pytest`.
- Requer uma conta e um workspace Xano do usuário, e o Xano CLI (`npm install -g @xano/cli`) para versionar o backend.

## Fora do escopo

- Telas funcionais (login, transações, orçamento, dashboard, relatórios): cada uma tem sua própria mudança.
- Modo offline/SQLite do projeto original: o clone usa apenas o Xano.
- Deploy em Streamlit Community Cloud.
