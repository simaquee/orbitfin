# Scripts

| Script | Uso |
|---|---|
| `teste_integracao.py` | Percorre cadastro, login, transações (criar, listar, editar, excluir) e orçamentos contra o Xano real, com o mesmo cliente do app. |

```powershell
python scripts/teste_integracao.py https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm
```

Cria um usuário descartável (`teste-…@orbitfin.test`) que deve ser apagado em Xano > Database > user.
