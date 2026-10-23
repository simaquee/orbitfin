# Publicação

| Parte | Onde | Como atualiza |
|---|---|---|
| Frontend | Streamlit Community Cloud: <https://orbitfin-tech.streamlit.app> (repositório `simaquee/orbitfin`, branch `main`, arquivo `src/app.py`, secrets com `[xano] base_url`) | Sozinho, a cada push na `main` |
| Backend | Xano, instância `x8ki-letl-twmt`, workspace "Gabriel's Workspace", grupo `api:orbitfingm` | `xano workspace push -d ./src/xano` após dry-run limpo |

## Se o app parar de funcionar

1. **"This app has gone to sleep"**: o plano gratuito desliga o app sem uso. Clique em *Yes, get this app back up!* e aguarde cerca de 1 minuto.
2. **Erro ou carregamento infinito**: em <https://share.streamlit.io> (GitHub `simaquee`), menu ⋮ do app > *Reboot app*. O log fica em *Manage app*.
3. **Login ou cadastro falham ("Não foi possível conectar" ou "Erro inesperado")**: abra
   `https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm/transacoes`.
   - 401/Unauthorized: o backend está no ar; volte ao passo 2.
   - 404: o backend sumiu. Republique conforme [getting-started.md](getting-started.md#1-backend-no-xano). Tabelas recriadas voltam vazias.
