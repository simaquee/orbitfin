# Design

## Context

Ver proposal.md. O app lê a URL do Xano de `st.secrets["xano"]["base_url"]` e o tema de `.streamlit/config.toml`, ambos na raiz do repositório.

## Goals / Non-Goals

**Goals:**
- Publicação reprodutível e sem segredos versionados.

**Non-Goals:**
- Automação de deploy (o Streamlit Cloud já redeploya a cada push na branch `main`).

## Decisions

- **Streamlit Community Cloud.** É gratuito, feito para Streamlit e redeploya sozinho a cada push. Configuração:
  - repositório: `<usuario>/orbitfin` (privado), branch `main`;
  - arquivo principal: `src/app.py`;
  - Python 3.12;
  - secrets: `[xano] base_url = "https://<instancia>.xano.io/api:orbitfin"`.
- **Repositório privado.** O código não tem segredos, mas não há motivo para expô-lo; o Streamlit Cloud acessa repositórios privados com autorização do GitHub.
- **Ordem: backend antes do frontend.** Sem o Xano publicado, o site no ar só mostraria a mensagem de configuração.
- **Push no Xano só após o dry-run revisado** e confirmação explícita do usuário (regra do `config.yaml` e do próprio Xano CLI).

## Risks / Trade-offs

- [XanoScript nunca validado pelo Xano] → o dry-run aponta erros de sintaxe antes de qualquer alteração; corrigir e repetir.
- [Plano gratuito do Xano limita requisições] → o app já usa cache em sessão; aceitável para uso pessoal.
- [Apps gratuitos do Streamlit Cloud "dormem" sem uso] → o primeiro acesso após dias parados leva alguns segundos para acordar.
