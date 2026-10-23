"""Página Transações (spec: transacoes)."""
from __future__ import annotations

from datetime import date

import streamlit as st

from components import dados
from components.header import cabecalho
from components.ui import html, kpi, linha_kpis, linha_transacao, titulo_card, vazio
from services import api
from services.calculos import filtrar, ordenar_recentes, totais
from services.categorias import CATEGORIAS, STATUS, TIPOS
from services.formatacao import data_br, mes_abrev, moeda, parse_data
from services.validacao import validar_transacao

TODOS = "Todos"


# ------------------------------------------------------------- formulário
def _formulario(tx: dict | None) -> None:
    prefixo = f"tx_{tx['id']}" if tx else "tx_nova"
    tipo = st.segmented_control("Tipo", options=list(TIPOS), format_func=TIPOS.get,
                                default=(tx or {}).get("tipo", "despesa"), key=f"{prefixo}_tipo",
                                selection_mode="single") or "despesa"
    c1, c2 = st.columns(2)
    valor = c1.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f",
                            value=float(tx["valor"]) if tx else 0.0, key=f"{prefixo}_valor")
    data = c2.date_input("Data", value=parse_data(tx["data"]) if tx else dados.hoje(),
                         format="DD/MM/YYYY", key=f"{prefixo}_data")
    opcoes = CATEGORIAS[tipo]
    atual = (tx or {}).get("categoria")
    categoria = st.selectbox("Categoria", opcoes,
                             index=opcoes.index(atual) if atual in opcoes else 0,
                             key=f"{prefixo}_cat_{tipo}")
    descricao = st.text_input("Descrição", value=(tx or {}).get("descricao") or "",
                              placeholder="Opcional", key=f"{prefixo}_desc")
    status = st.radio("Status", list(STATUS), format_func=STATUS.get, horizontal=True,
                      index=list(STATUS).index((tx or {}).get("status", "pago")),
                      key=f"{prefixo}_status")

    salvar, cancelar = st.columns(2)
    if cancelar.button("Cancelar", width="stretch", key=f"{prefixo}_cancelar"):
        st.rerun()
    if salvar.button("Salvar", type="primary", width="stretch", key=f"{prefixo}_salvar"):
        erro = validar_transacao(tipo, valor, categoria, status)
        if erro:
            st.error(erro)
            return
        payload = {"tipo": tipo, "valor": round(valor, 2), "data": data.isoformat(),
                   "categoria": categoria, "descricao": descricao.strip(), "status": status}
        try:
            if tx:
                api.cliente().editar_transacao(tx["id"], payload)
            else:
                api.cliente().criar_transacao(payload)
        except api.ErroApi as e:
            st.error(str(e))
            return
        dados.invalidar()
        st.rerun()


@st.dialog("Nova transação")
def _dialogo_nova() -> None:
    _formulario(None)


@st.dialog("Editar lançamento")
def _dialogo_editar(tx: dict) -> None:
    _formulario(tx)


@st.dialog("Excluir lançamento?")
def _dialogo_excluir(tx: dict) -> None:
    rotulo = f"{data_br(tx['data'])} · {tx['categoria']} · {moeda(float(tx['valor']))}"
    st.markdown(f"Tem certeza que deseja excluir **{rotulo}**? Essa ação não pode ser desfeita.")
    excluir, cancelar = st.columns(2)
    if cancelar.button("Cancelar", width="stretch", key="excluir_cancelar"):
        st.rerun()
    if excluir.button("Excluir", type="primary", width="stretch", key="excluir_ok"):
        try:
            api.cliente().excluir_transacao(tx["id"])
        except api.ErroApi as e:
            st.error(str(e))
            return
        dados.invalidar()
        st.rerun()


# ----------------------------------------------------------------- página
def _opcoes_mes(txs: list[dict], hoje: date) -> list:
    meses = {(hoje.year, hoje.month)} | {(parse_data(t["data"]).year, parse_data(t["data"]).month)
                                         for t in txs}
    return sorted(meses, reverse=True) + [TODOS]


def render() -> None:
    acao = cabecalho("transacoes", "Registre, filtre e acompanhe cada entrada e saída.",
                     com_acao=True)
    with acao:
        if st.button("Adicionar transação", type="primary", width="stretch"):
            _dialogo_nova()
    if st.session_state.pop("abrir_nova_transacao", False):
        _dialogo_nova()

    try:
        txs = dados.transacoes()
    except api.ErroApi as e:
        st.error(str(e))
        return

    if not txs:
        with st.container(key="card_vazio_tx"):
            html(vazio("Nenhuma transação ainda. Clique em Adicionar transação para começar.",
                       "receipt"))
        return

    hoje = dados.hoje()
    f1, f2, f3, f4 = st.columns(4)
    opcoes_mes = _opcoes_mes(txs, hoje)
    periodo = f1.selectbox("Mês", opcoes_mes, index=opcoes_mes.index((hoje.year, hoje.month)),
                           format_func=lambda p: p if p == TODOS else mes_abrev(*p))
    tipo = f2.selectbox("Tipo", [TODOS, *TIPOS], format_func=lambda v: TIPOS.get(v, v))
    status = f3.selectbox("Status", [TODOS, *STATUS], format_func=lambda v: STATUS.get(v, v))
    categorias = sorted({t["categoria"] for t in txs})
    categoria = f4.selectbox("Categoria", ["Todas", *categorias])

    filtradas = ordenar_recentes(filtrar(
        txs, periodo=None if periodo == TODOS else periodo,
        tipo=None if tipo == TODOS else tipo, status=None if status == TODOS else status,
        categoria=None if categoria == "Todas" else categoria))

    t = totais(filtradas)
    linha_kpis([
        kpi("Receitas", moeda(t["receitas"]), f"{t['n_receitas']} no filtro", "arrow-trend-up"),
        kpi("Despesas", moeda(t["despesas"]), f"{t['n_despesas']} no filtro", "arrow-trend-down",
            tom="t"),
        kpi("Saldo filtrado", moeda(t["saldo"]), "Receitas − despesas", "scale",
            tom="t" if t["saldo"] < 0 else "m", negativo=t["saldo"] < 0),
    ])
    html('<div style="height:.9rem"></div>')

    with st.container(key="card_lista_tx"):
        html(titulo_card("Lançamentos", f"{len(filtradas)} itens"))
        if not filtradas:
            html(vazio("Nenhuma transação com esses filtros.", "filter"))
            return
        for tx in filtradas:
            linha, editar, excluir = st.columns([10, 1.1, 1.1], vertical_alignment="center",
                                                gap="small")
            linha.markdown(linha_transacao(tx, mostrar_status=True), unsafe_allow_html=True)
            if editar.button("Editar", key=f"editar_{tx['id']}", type="tertiary"):
                _dialogo_editar(tx)
            if excluir.button("Excluir", key=f"excluir_{tx['id']}", type="tertiary"):
                _dialogo_excluir(tx)
