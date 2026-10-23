# Design

## Context

Ver proposal.md. O workspace do Xano já tinha a API `authentication` do Quick Start, que usa a mesma tabela `user` do OrbitFin. O push do Xano CLI sincroniza o schema declarado no repositório e remove campos que não estão nele.

## Goals / Non-Goals

**Goals:**
- Republicar o backend sem perda de dados e sem quebrar outras APIs do workspace.
- Eixo legível nos gráficos de um usuário novo.

**Non-Goals:**
- Separar o OrbitFin em um workspace próprio do Xano.
- Excluir usuários pelo app (as contas de teste são removidas pelo painel do Xano).

## Decisions

- **`user.xs` espelha o workspace.** Declarar `role` e `password_reset` e manter `email`/`password` opcionais faz o dry-run sair sem operações destrutivas. A regra "e-mail e senha obrigatórios" fica onde já era aplicada: no `input` do endpoint `register` (campo `email` obrigatório) e nas preconditions de senha.
- **Push só após dry-run limpo.** Sequência: `xano workspace push -d ./src/xano --dry-run`, revisão da seção *Destructive Operations*, confirmação do usuário e `xano workspace push -d ./src/xano`.
- **Eixo fixo só sem dados.** `_sem_valores` considera "sem dados" quando todos os pontos de todas as séries têm módulo menor que 1; nesse caso o eixo Y usa `range=[0, 100]`. Com qualquer valor real o Plotly continua escalando sozinho.

## Risks / Trade-offs

- Se o Quick Start do workspace mudar o schema de `user`, `user.xs` precisa ser atualizado antes do próximo push → mitigação: o dry-run lista qualquer `DROP_FIELD` e o README avisa.
