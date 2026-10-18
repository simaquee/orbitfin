# Proposal

## Why

O OrbitFin só roda localmente e com um Xano simulado. Para ser usado de verdade, o backend precisa estar publicado no Xano do usuário e o frontend hospedado na internet com uma URL pública.

Depende de: todas as mudanças `add-*` implementadas (frontend) e dos arquivos XanoScript em `src/xano/`.

## What Changes

- Publicar o backend XanoScript no workspace Xano do usuário (após dry-run revisado e confirmação explícita).
- Versionar o projeto em Git e publicá-lo num repositório privado no GitHub.
- Hospedar o frontend no Streamlit Community Cloud, com `src/app.py` como arquivo principal e a URL do Xano configurada nos *secrets* da plataforma.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
<!-- Nenhuma: infraestrutura de publicação, sem mudança de comportamento (skip_specs: true). -->

## Impact

- Contas necessárias: Xano (já existente), GitHub e Streamlit Community Cloud (login via GitHub).
- Nenhum segredo vai para o repositório: a URL do Xano fica só nos secrets do Streamlit Cloud.

## Fora do escopo

- Domínio próprio, CI/CD e ambientes separados de homologação.
- Migração de dados (o backend começa vazio).
