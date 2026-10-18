# Tasks

## 1. Estrutura e configuração

- [x] 1.1 Criar `requirements.txt` (streamlit>=1.39, requests, pandas, plotly, pytest), `.gitignore` (`.streamlit/secrets.toml`, `.venv/`, `__pycache__/`) e as pastas `src/components/`, `src/views/`, `src/services/`, `tests/`, e verificar que `pip install -r requirements.txt` e `pytest` rodam sem erro
- [x] 1.2 Criar `.streamlit/secrets.toml.example` com `[xano] base_url = "https://<instancia>.xano.io/api:orbitfin"` e `.streamlit/config.toml` com a paleta, e verificar que `secrets.toml` está ignorado pelo Git

## 2. Backend Xano

- [ ] 2.1 (requer Xano) Instalar o Xano CLI, autenticar (`xano auth`) e criar o API group `orbitfin`, e verificar com `xano profile me`
- [ ] 2.2 (requer Xano) Rodar `xano workspace pull -d ./src/xano` e verificar que a pasta `src/xano/` contém a tabela `user` padrão

## 3. Serviços

- [x] 3.1 Implementar `src/services/formatacao.py` (moeda BRL, data DD/MM/AAAA, mês abreviado pt-BR) e verificar com testes cobrindo os cenários "Valor positivo", "Valor negativo" e "Mês abreviado"
- [x] 3.2 Implementar `src/services/api.py` (URL base dos secrets, Bearer, timeout de 30 s, spinner, exceções `ErroConexao`/`ErroValidacao`/`SessaoExpirada`) e verificar com testes usando respostas HTTP simuladas para sucesso, erro 400 com mensagem, 401 e timeout

## 4. Casca visual

- [x] 4.1 Implementar `src/components/theme.py` e `src/components/ui.py` (cards, KPI, chip de status) com a paleta oficial e Flaticon UIcons, e verificar visualmente que fundo, cards e botão primário usam as cores da spec
- [x] 4.2 Implementar `src/components/sidebar.py`, `src/components/header.py` e o roteamento em `src/app.py` (com páginas provisórias), e verificar manualmente a ordem dos itens, o destaque da página ativa e os cabeçalhos de cada página
- [x] 4.3 Tratar a ausência de `xano.base_url` e o `SessaoExpirada` em `src/app.py`, e verificar que, sem secrets, a mensagem de configuração aparece no lugar das telas
- [x] 4.4 Escrever `README.md` com instalação, configuração dos secrets e comando `streamlit run src/app.py`, e verificar que seguir o README do zero sobe a aplicação

## Workflow follow-up

- Arquivar com `/opsx:archive` após a revisão; em seguida aplicar `add-autenticacao`.
