# OrbitFin

Organizador financeiro pessoal (identidade Grupo Marte): receitas e despesas, limites por categoria, metas de contenção, dashboard com sugestões automáticas e relatórios.

- **Frontend:** Python + Streamlit + Plotly
- **Backend:** Xano (API REST + PostgreSQL + JWT), versionado em XanoScript em `src/xano/`
- **Metodologia:** [OpenSpec](https://openspec.dev)

## Estrutura

```
orbitfin/
├── openspec/                    # Planejamento (formato da CLI do OpenSpec)
│   ├── config.yaml              # contexto do projeto lido pela IA
│   ├── specs/                   # specs consolidadas: specs/<capacidade>/spec.md
│   └── changes/                 # uma pasta por mudança
│       ├── add-transacoes/
│       │   ├── proposal.md      # por quê e o quê
│       │   ├── design.md        # como (decisões técnicas)
│       │   ├── tasks.md         # checklist de implementação
│       │   └── specs/transacoes/spec.md   # delta: requisitos que entram/mudam
│       └── archive/             # mudanças concluídas e arquivadas
├── src/                         # Todo o código-fonte
│   ├── app.py                   # entrypoint e roteamento
│   ├── components/              # tema, barra lateral, cabeçalho, gráficos, blocos de UI
│   ├── views/                   # uma tela por arquivo
│   ├── services/                # cliente da API Xano e regras de negócio (funções puras)
│   └── xano/                    # backend: tabelas, endpoints e funções em XanoScript
├── tests/                       # pytest (sem rede: respostas HTTP simuladas)
├── .streamlit/                  # config.toml (tema) e secrets.toml (não versionado)
├── pyproject.toml
└── requirements.txt
```

`openspec/specs/` é a documentação oficial do sistema: 8 capacidades (`interface-base`, `autenticacao`, `transacoes`, `orcamentos`, `metas`, `dashboard`, `sugestoes`, `relatorios`), com os requisitos e cenários de cada uma. Cada `openspec archive <mudança>` incorpora ali os requisitos de uma mudança concluída e move a mudança para `changes/archive/`. Novas mudanças começam com `/opsx:propose`.

O `PRODUCT.md` da raiz guarda o contexto de produto usado pela skill de design Impeccable: público, propósito, marca e princípios.

## 1. Backend no Xano

1. Crie uma conta em <https://xano.com> (o plano gratuito serve) e um workspace.
2. Autentique o Xano CLI (requer Node.js):
   ```powershell
   npm install -g @xano/cli
   xano auth
   xano profile me
   ```
3. Confira as mudanças sem aplicar nada, e só depois publique:
   ```powershell
   xano workspace push -d ./src/xano --dry-run
   xano workspace push -d ./src/xano
   ```
4. No Xano, abra **API > OrbitFin** e copie a **Base URL**: `https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm`.
   O grupo usa o canonical `orbitfingm` porque a instância gratuita é compartilhada e `api:orbitfin` já pertence ao projeto original.

> Faça `git commit` antes de publicar, e evite `--force`, `--delete` ou `--truncate` sem revisar.

## 2. Frontend

Rode os comandos a partir da raiz do projeto (o Streamlit procura `.streamlit/` no diretório atual):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # cole a Base URL do Xano
streamlit run src/app.py
```

Acesse <http://localhost:8501>. Sem `secrets.toml` configurado, o app mostra como configurá-lo.

## Testes

```powershell
pytest                                                                  # sem rede
python scripts/teste_integracao.py https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm   # contra o Xano real
```

O teste de integração cria um usuário descartável (`teste-…@orbitfin.test`); apague-o em Xano > Database > user.

## Se o app parar de funcionar

Produção: <https://orbitfin-tech.streamlit.app> (Streamlit Community Cloud, branch `main`, arquivo `src/app.py`).

1. **"This app has gone to sleep"**: o plano gratuito desliga o app sem uso. Clique em *Yes, get this app back up!* e aguarde cerca de 1 minuto.
2. **Erro ou carregamento infinito**: em <https://share.streamlit.io> (GitHub `simaquee`), menu ⋮ do app > *Reboot app*. O log fica em *Manage app*.
3. **Login/cadastro falham ("Não foi possível conectar" ou "Erro inesperado")**: abra
   `https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm/transacoes`.
   - 401/Unauthorized: o backend está no ar; volte ao passo 2.
   - 404: o backend sumiu. Republique com `xano auth`, `xano workspace push -d ./src/xano --dry-run` e, se não houver *Destructive Operations*, `xano workspace push -d ./src/xano` (ver seção 1). Tabelas recriadas voltam vazias.

> A tabela `user` é compartilhada com a API *authentication* do Quick Start do Xano no mesmo workspace. Mantenha em `src/xano/table/user.xs` os campos `role` e `password_reset`; sem eles o push os apaga.

## Fluxo OpenSpec

```powershell
openspec list                      # mudanças em andamento
openspec view                      # painel interativo
openspec validate --all --strict
```

No Claude Code: `/opsx:propose "ideia"` → revisar → `/opsx:apply <mudança>` → `/opsx:archive <mudança>`.
