# Design

## Context

Ver proposal.md. O OrbitFin não tem backend próprio: o Streamlit lê o arquivo e o Xano só recebe transações já estruturadas. Cada transação exige tipo, valor > 0, data, categoria válida para o tipo e status (spec `transacoes`).

## Goals / Non-Goals

**Goals:**
- Ler PDF, CSV e OFX localmente, sem IA e sem enviar o arquivo a terceiros.
- Revisão linha a linha antes de gravar; nada é gravado sem confirmação de todas as linhas.
- Gravar o lote numa única chamada ao Xano, tudo ou nada.

**Non-Goals:**
- OCR, categorização automática, deduplicação (ver "Fora do escopo" em proposal.md).

## Decisions

- **Leitura em `src/services/extrato.py`, funções puras.** `ler_extrato(nome, conteudo)` escolhe o leitor pela extensão e devolve linhas `{data, descricao, valor}` com valor com sinal (negativo = saída). Fica testável sem Streamlit, como o resto de `services/`.
- **CSV:** decodifica UTF-8 (com BOM) e cai para Latin-1; detecta `;`, `,` ou tabulação pelo cabeçalho; reconhece colunas por nome sem acento (`data/date`, `descricao/historico/lancamento/memo/title`, `valor/amount` ou o par `credito`/`debito`).
- **OFX:** expressão regular sobre os blocos `<STMTTRN>` (o OFX 1.x é SGML e não fecha tags); usa `DTPOSTED`, `TRNAMT` e `MEMO` (ou `NAME`).
- **PDF:** `pypdf` extrai o texto localmente. Uma linha é lançamento quando começa com data (`dd/mm` ou `dd/mm/aaaa`) e termina com valor em formato brasileiro; se houver dois valores no fim, o segundo é o saldo e é ignorado. Linhas de "saldo" são descartadas. Datas sem ano usam o ano mais frequente nas datas completas do documento (ou o ano atual). PDF sem texto (imagem) gera erro orientando exportar CSV/OFX.
- **Valores brasileiros e internacionais:** `parse_valor` aceita `1.234,56`, `-45,90`, `45,90-`, `(45,90)`, `45,90 D`, `R$ 1.234,56` e `-45.90`. Com `,` e `.` juntos, o último separador é o decimal.
- **Mapeamento para transação:** valor negativo → despesa, positivo → receita; `valor` enviado sempre positivo; categoria "Outros"; status "pago" (lançamento de extrato já aconteceu).
- **Estado da revisão em `st.session_state["importacao"]`.** Cada linha guarda `confirmado`. Confirmar copia os valores dos inputs para a linha e trava os campos; "Editar" destrava. Os `key` dos widgets levam um número por arquivo lido, para um novo upload não herdar valores do anterior.
- **Painel na própria página, não em `st.dialog`.** A lista pode ter dezenas de linhas; um painel (card "Importar extrato") aparece acima dos indicadores e funciona mesmo quando o usuário ainda não tem transações.
- **Endpoint `POST /transacoes/lote`.** Entrada `object[1:500] transacoes` com o mesmo schema do POST unitário. Primeiro valida todas as linhas com `OrbitFin/validar_transacao`; só então grava dentro de `db.transaction`, sempre com `user_id = $auth.id`. Resposta `{criadas: <quantidade>}`.

## Risks / Trade-offs

- Layouts de PDF variam por banco → a regra cobre o formato comum "data · descrição · valor [saldo]"; o que não casar não entra, e a revisão mostra exatamente o que foi lido. Se nada casar, o app sugere CSV/OFX.
- Lote de até 500 linhas por importação → extratos maiores devem ser divididos (mensagem clara do backend).
- Importar duas vezes o mesmo arquivo duplica lançamentos → fora do escopo; a revisão mostra a lista antes de gravar.
