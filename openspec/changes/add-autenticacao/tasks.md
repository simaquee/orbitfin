# Tasks

## 1. Backend Xano

- [x] 1.1 Definir `src/xano/table/user.xs` (name, email único com trim/lower, password com min:8|minAlpha:1|minDigit:1, created_at) e verificar com `xano workspace push -d ./src/xano --dry-run` sem erros
- [x] 1.2 Criar `src/xano/api/orbitfin/register_POST.xs` e `login_POST.xs` com o contrato `{access_token, user_id, name, email}`, expiração de 86400 s e mensagens em português, e verificar com o dry-run
- [x] 1.3 (requer Xano) Publicar com `xano workspace push -d ./src/xano` após confirmação do usuário, e verificar no Run do Xano: cadastro, cadastro duplicado, login correto e login com senha errada

## 2. Frontend

- [x] 2.1 Implementar `src/services/validacao.py` (`senha_valida`, `validar_cadastro`) e verificar com testes para os cenários "Campos vazios", "Senhas diferentes" e "Senha fraca"
- [x] 2.2 Adicionar `cadastrar()` e `entrar()` em `src/services/api.py` e verificar com testes simulados: sucesso, e-mail duplicado, credenciais inválidas e falha de conexão
- [x] 2.3 Implementar `src/views/login.py` e `src/views/cadastro.py` com a alternância entre as telas e a barra lateral oculta, e verificar manualmente todos os cenários da spec
- [x] 2.4 Adicionar saudação "Olá, {primeiro nome}", rodapé da barra lateral (avatar, nome, e-mail) e botão "Sair", e verificar manualmente os cenários "Saudação pelo primeiro nome" e "Sair"

## Workflow follow-up

- Arquivar com `/opsx:archive` após a revisão; em seguida aplicar `add-transacoes`.
