# Fluxo de trabalho (OpenSpec)

Toda mudança de comportamento passa por uma change em `openspec/changes/<nome>/`:

| Arquivo | Papel |
|---|---|
| `proposal.md` | Por quê, o que muda e o que fica fora do escopo |
| `design.md` | Decisões técnicas |
| `tasks.md` | Checklist de implementação (backend e frontend em grupos separados) |
| `specs/<capacidade>/spec.md` | Delta: requisitos `ADDED`, `MODIFIED` ou `REMOVED` |

No Claude Code: `/opsx:propose "ideia"` → revisar → `/opsx:apply <change>` → `/opsx:archive <change>`. O archive incorpora o delta em `openspec/specs/` e move a change para `openspec/changes/archive/AAAA-MM-DD-<nome>/`.

Comandos úteis da CLI (`npm install -g @fission-ai/openspec`):

```powershell
openspec list                        # changes em andamento
openspec list --specs                # capacidades e número de requisitos
openspec view                        # painel interativo
openspec validate --all --strict     # valida specs e changes
```

Regras do projeto (em `openspec/config.yaml`): artefatos em pt-BR, cenários com valores concretos e push real no Xano só com confirmação humana.
