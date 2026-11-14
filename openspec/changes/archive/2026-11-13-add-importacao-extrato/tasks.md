# Tasks

## 1. Backend (requer Xano)

- [x] 1.1 Criar `src/xano/api/orbitfin/transacoes/lote_POST.xs` (`POST /transacoes/lote`, até 500 itens, validação de todas as linhas antes de gravar, gravação em `db.transaction`)
- [x] 1.2 Rodar `xano workspace push -d ./src/xano --dry-run` e confirmar que não há *Destructive Operations* (resultado: 1 endpoint criado, grupo `OrbitFin` atualizado)
- [x] 1.3 Após confirmação explícita do usuário, publicar com `xano workspace push -d ./src/xano`
- [x] 1.4 Rodar `scripts/teste_integracao.py` (já cobre o lote válido e o lote com linha inválida) contra o Xano real (lote válido cria 2; lote com valor 0 recusado sem gravar nada)

## 2. Frontend

- [x] 2.1 `src/services/extrato.py`: leitura local de CSV, OFX e PDF (`pypdf`) e montagem do lote
- [x] 2.2 `src/services/api.py`: `criar_transacoes_lote`
- [x] 2.3 `src/views/transacoes.py`: botão "Importar extrato", cards de revisão (Descrição, Valor, Confirmar, Descartar) e "Confirmar importação" desabilitado até tudo estar confirmado
- [x] 2.4 `requirements.txt`: adicionar `pypdf`
- [x] 2.5 Testes em `tests/test_extrato.py` e `tests/test_api.py`; `pytest` passando (102)
- [x] 2.6 Conferir o fluxo no app rodando localmente (`streamlit run src/app.py`): leitura de PDF e CSV, edição, valor zero recusado, Confirmar/Editar/Descartar e botão final travado/liberado
- [x] 2.7 Após o 1.3, importar pelo app local e conferir as transações na lista

## 3. Documentação

- [x] 3.1 README: importação de extrato e formatos aceitos
