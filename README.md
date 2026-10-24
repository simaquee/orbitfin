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
├── scripts/                     # teste de integração contra o Xano real
├── .streamlit/                  # config.toml (tema) e secrets.toml (não versionado)
├── pyproject.toml
└── requirements.txt
```

`openspec/specs/` é a documentação oficial do sistema: 8 capacidades (`interface-base`, `autenticacao`, `transacoes`, `orcamentos`, `metas`, `dashboard`, `sugestoes`, `relatorios`), com os requisitos e cenários de cada uma. Cada `openspec archive <mudança>` incorpora ali os requisitos de uma mudança concluída e move a mudança para `changes/archive/`. Novas mudanças começam com `/opsx:propose`.

O `PRODUCT.md` da raiz guarda o contexto de produto usado pela skill de design Impeccable: público, propósito, marca e princípios.

## Como este projeto foi construído (OpenSpec)

O OrbitFin é *spec-driven*: os requisitos foram escritos primeiro no OpenSpec e o código foi implementado a partir deles, uma change por vez (`/opsx:propose` → `/opsx:apply` → `/opsx:archive`). O OpenSpec gera os artefatos de planejamento e os comandos do agente; o código-fonte é escrito seguindo as specs. Como verificar:

| Onde | O que mostra |
|---|---|
| `openspec/config.yaml` | `schema: spec-driven`, contexto e regras do projeto lidos pelo OpenSpec |
| `openspec/specs/` | 8 capacidades com requisitos (`SHALL`/`MUST`) e cenários (`WHEN`/`THEN`) |
| `openspec/changes/archive/` | Todas as mudanças, com `proposal.md`, `design.md`, `tasks.md` e deltas de spec: `add-fundacao-projeto`, `add-autenticacao`, `add-transacoes`, `add-orcamentos`, `add-dashboard`, `add-relatorios`, `refactor-estrutura-src`, `add-deploy-producao` (18/10/2026) e `fix-republicacao-xano-e-eixo-vazio` (23/10/2026) |
| `.claude/skills/openspec-*/SKILL.md` | Gerados pela CLI do OpenSpec: `metadata.author: openspec`, `generatedBy: "1.14.3"` |
| `.claude/commands/opsx/*.md` | Comandos `/opsx:*` gerados pela mesma CLI (idênticos à saída de `openspec init --tools claude` na versão 1.14.3) |
| Cabeçalho de cada arquivo em `src/` e `scripts/` | `Spec (OpenSpec): openspec/specs/<capacidade>/spec.md`, a spec que o arquivo implementa |
| `src/xano/**/*.xs` | Comentário `(spec: <capacidade>)` em tabelas, funções e endpoints |
| `git log --reverse` | Primeiro commit: "OrbitFin: app Streamlit + backend Xano estruturados com OpenSpec" |

```powershell
npm install -g @fission-ai/openspec
openspec list --specs                 # 8 capacidades e número de requisitos
openspec validate --all --strict      # specs válidas no formato oficial
git log --reverse --oneline | Select-Object -First 1
```

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
