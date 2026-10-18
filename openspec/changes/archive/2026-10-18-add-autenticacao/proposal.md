# Proposal

## Why

Todos os dados do OrbitFin são pessoais. Sem cadastro e login não é possível isolar as transações e os orçamentos de cada usuário. No original, falhas de rede apareciam como "senha incorreta", a regra de senha só era aplicada no servidor e o primeiro nome do usuário, exigido pela especificação, nunca era exibido.

Depende de: `add-fundacao-projeto`.

## What Changes

- Tabela `user` e endpoints `POST /register` e `POST /login` no Xano (grupo `orbitfin`), com token JWT válido por 24 horas.
- Tela de login: e-mail e senha.
- Tela de cadastro: nome completo, e-mail, senha e confirmação de senha.
- Validação da senha também no cliente (mínimo de 8 caracteres, com pelo menos 1 letra e 1 número).
- Sessão em memória (`st.session_state`), botão "Sair" e saudação pelo primeiro nome.
- Mensagens distintas para credenciais inválidas e falha de conexão.

## Capabilities

### New Capabilities
- `autenticacao`: cadastro, login, sessão, logout e identificação do usuário na interface.

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Backend: `src/xano/table/user.xs`, `src/xano/api/orbitfin/register_POST.xs`, `src/xano/api/orbitfin/login_POST.xs`.
- Frontend: `src/views/login.py`, `src/views/cadastro.py`, ajustes em `src/app.py` e `src/components/sidebar.py`.

## Fora do escopo

- Recuperação de senha, login social e verificação de e-mail.
- Campos CPF, telefone e sobrenome separado (citados nos documentos do original, mas nunca implementados).
- Persistir a sessão ao recarregar o navegador.
