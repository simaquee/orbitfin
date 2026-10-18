# Tasks

## 1. Backend (requer Xano)

- [x] 1.1 Autenticar o Xano CLI (`xano auth`) e verificar com `xano profile me` que a instância e o workspace corretos estão selecionados
- [x] 1.2 Rodar `xano workspace push -d ./src/xano --dry-run`, corrigir erros apontados e verificar que o preview lista as 3 tabelas, a função e os 8 endpoints
- [ ] 1.3 Após confirmação explícita do usuário, publicar com `xano workspace push -d ./src/xano` e verificar com o cliente real: cadastro, login, criar transação e listar orçamentos

## 2. Repositório (requer GitHub)

- [x] 2.1 Inicializar o Git, conferir que `.streamlit/secrets.toml` e `.venv/` estão ignorados (`git check-ignore`) e fazer o commit inicial
- [x] 2.2 Criar o repositório privado `orbitfin` no GitHub e enviar a branch `main`, e verificar que o repositório remoto não contém `secrets.toml`

## 3. Frontend (requer Streamlit Cloud)

- [ ] 3.1 Criar o app no Streamlit Community Cloud (arquivo principal `src/app.py`, Python 3.12, secrets com a Base URL do Xano) e verificar que a URL pública abre a tela de login
- [ ] 3.2 Na URL pública, cadastrar um usuário, registrar uma transação e verificar que ela aparece no Dashboard
