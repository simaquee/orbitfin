# Como contribuir

1. **Proponha antes de codar.** Mudanças de comportamento começam com uma change do OpenSpec (`/opsx:propose "ideia"` ou `openspec new change <nome>`). Veja [docs/workflow.md](docs/workflow.md).
2. **Implemente seguindo as tasks** e a organização de [docs/architecture.md](docs/architecture.md): telas em `src/commands/`, regras puras em `src/core/`, visual em `src/ui/`.
3. **Teste:**
   ```powershell
   pytest
   openspec validate --all --strict
   ```
   Mudou o backend? Rode `xano workspace push -d ./src/xano --dry-run` e não publique com *Destructive Operations*.
4. **Arquive** a change concluída (`/opsx:archive <nome>`) e registre a mudança no [CHANGELOG.md](CHANGELOG.md).
5. **Commit e push na `main`.** O Streamlit Cloud publica sozinho; o backend é publicado à parte (ver [docs/deployment.md](docs/deployment.md)).

Mensagens de commit: prefixo do tipo (`fix:`, `docs:`, `openspec:`, `refactor:`) e resumo em português.
