# Tasks

## 1. Backend (requer Xano)

- [x] 1.1 Confirmar que `api:orbitfingm` responde 404 e autenticar o Xano CLI no workspace "Gabriel's Workspace" (`xano auth`, `xano profile me`)
- [x] 1.2 Rodar `xano workspace push -d ./src/xano --dry-run` e identificar as operações destrutivas na tabela `user`
- [x] 1.3 Ajustar `src/xano/table/user.xs` ao schema do workspace e repetir o dry-run até não haver *Destructive Operations*
- [x] 1.4 Após confirmação explícita do usuário, publicar com `xano workspace push -d ./src/xano`
- [x] 1.5 Rodar `scripts/teste_integracao.py` contra o Xano real: cadastro, cadastro duplicado, login, CRUD de transação e orçamentos

## 2. Frontend

- [x] 2.1 Fixar o eixo Y em 0..100 quando o gráfico não tem valores (`src/components/graficos.py`)
- [x] 2.2 Cobrir com `tests/test_graficos.py` e rodar `pytest` (61 passando)
- [x] 2.3 Verificar na URL pública que o cadastro abre o Dashboard com o eixo corrigido

## 3. Documentação

- [x] 3.1 Guia "Se o app parar de funcionar" e teste de integração no README
