# Design

## Context

Usa o cliente `src/services/api.py` e a casca visual de `add-fundacao-projeto`. O original tinha dois conjuntos de endpoints de autenticação (`/auth/*` do quick-start do Xano e `/login` e `/register` do grupo `orbitfin`), com formatos de resposta diferentes (`authToken` e `access_token`).

## Goals / Non-Goals

**Goals:**
- Um único contrato de autenticação.
- Mensagens de erro corretas para cada causa de falha.

**Non-Goals:**
- Papéis de usuário (`admin`/`member`) e logs de eventos (`event_log`) do quick-start do Xano.

## Decisions

- **Contrato único no grupo `orbitfin`.**
  - `POST /register {name, email, password}` → `{access_token, user_id, name, email}`.
  - `POST /login {email, password}` → mesmo formato.
  - Senha com o tipo nativo `password` do Xano (hash), com o filtro `min:8|minAlpha:1|minDigit:1`; e-mail com os filtros `trim|lower` e índice único.
- **Mensagens de erro em português no próprio backend** ("Já existe uma conta com este e-mail.", "E-mail ou senha incorretos."). O cliente apenas as exibe.
- **Validação duplicada (cliente e servidor).** O cliente dá retorno imediato; o servidor é a garantia. A regra fica em `src/services/validacao.py` (função pura `senha_valida`).
- **Sessão em `st.session_state`** com as chaves `token`, `usuario` (`{id, nome, email}`), `pagina` e `tela_auth`. O primeiro nome é derivado de `nome.split()[0]` (o nome completo vem do cadastro).
- **Credenciais inválidas e servidor fora do ar são tratados de forma diferente:** `ErroValidacao` (HTTP 403) exibe a mensagem de credenciais; `ErroConexao` exibe a mensagem de conexão.

## Risks / Trade-offs

- [Token de 24 h sem renovação] → ao expirar, o tratamento de HTTP 401 da fundação leva o usuário ao login.
- [Registrar e-mail diferenciando maiúsculas] → mitigado pelo filtro `lower` no Xano e pelo `strip()` no cliente.
