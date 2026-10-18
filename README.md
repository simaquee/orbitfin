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

`openspec/specs/` começa vazia: cada `openspec archive <mudança>` copia os requisitos da mudança para lá, e essa pasta vira a documentação oficial do sistema.

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
4. No Xano, abra **API > OrbitFin** e copie a **Base URL** (algo como `https://xxxx.xano.io/api:orbitfin`).

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
pytest
```

## Fluxo OpenSpec

```powershell
openspec list                      # mudanças em andamento
openspec view                      # painel interativo
openspec validate --all --strict
```

No Claude Code: `/opsx:propose "ideia"` → revisar → `/opsx:apply <mudança>` → `/opsx:archive <mudança>`.
