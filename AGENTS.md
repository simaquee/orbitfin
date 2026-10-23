# Instruções para agentes de IA

O OrbitFin é desenvolvido com OpenSpec. Antes de mudar comportamento, crie uma change (`/opsx:propose`); o contexto e as regras do projeto estão em `openspec/config.yaml`.

## Mapa

- `src/app.py`: entrypoint. `src/commands/`: telas. `src/core/`: API do Xano e regras. `src/ui/`: visual. `src/utils/`: formatação. `src/xano/`: backend.
- `test/` espelha `src/`. Detalhes e regras de dependência em `docs/architecture.md`.

## Comandos

```powershell
pytest                                   # 61+ testes, sem rede
streamlit run src/app.py                 # app local (requer .streamlit/secrets.toml)
openspec validate --all --strict         # specs e changes
xano workspace push -d ./src/xano --dry-run
```

## Regras

- Push real no Xano (`xano workspace push` sem `--dry-run`), `--force`, `--delete` e `--truncate` só com confirmação explícita do usuário, e nunca com *Destructive Operations* no dry-run.
- Nunca versionar `.streamlit/secrets.toml`, tokens ou credenciais do Xano.
- Regras de cálculo ficam em funções puras em `src/core/`, nunca nas telas.
- Não mover `src/app.py`, `.streamlit/` nem `src/xano/`: o Streamlit Cloud e o Xano CLI dependem desses caminhos.
- Commits feitos com ajuda de IA declaram isso na mensagem.
