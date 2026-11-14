"""Página Transações.

Spec (OpenSpec): openspec/specs/transacoes/spec.md
"""
from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from components import dados
from components.header import cabecalho
from components.ui import chip, html, info, kpi, linha_kpis, linha_transacao, titulo_card, vazio
from services import api, extrato
from services.calculos import filtrar, ordenar_recentes, totais
from services.categorias import CATEGORIAS, STATUS, TIPOS
from services.formatacao import data_br, mes_abrev, moeda, parse_data
from services.validacao import validar_transacao

TODOS = "Todos"
IMPORTACAO = "importacao"  # estado da revisão em st.session_state


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


# ------------------------------------------------- importação de extrato
def _abrir_importacao() -> None:
    st.session_state.setdefault(IMPORTACAO, {"lote": 0, "arquivo": "", "linhas": []})


def _fechar_importacao() -> None:
    st.session_state.pop(IMPORTACAO, None)


def _ler_arquivo(imp: dict) -> None:
    arquivo = st.file_uploader("Arquivo do extrato (PDF, CSV ou OFX)", type=list(extrato.FORMATOS),
                               key=f"imp_arquivo_{imp['lote']}")
    if arquivo is not None:
        try:
            linhas = extrato.ler_extrato(arquivo.name, arquivo.getvalue())
        except extrato.ErroExtrato as e:
            st.error(str(e))
        else:
            # Novo número de lote: os widgets dos cards não herdam valores de outro arquivo
            imp["lote"] += 1
            imp["arquivo"] = arquivo.name
            imp["linhas"] = [{**l, "id": i, "confirmado": False} for i, l in enumerate(linhas)]
            st.rerun()
    html(info("A leitura acontece aqui no app, sem IA e sem enviar o arquivo a terceiros. "
              "PDF escaneado (imagem) não tem texto para ler: exporte em CSV ou OFX."))
    if st.button("Cancelar", key="imp_cancelar_arquivo"):
        _fechar_importacao()
        st.rerun()


def _campos_atuais(imp: dict, linha: dict) -> tuple[str, float, str, str]:
    """Descrição, valor, tipo e categoria como estão nos campos do card (ou os lidos do extrato)."""
    k = f"imp_{imp['lote']}_{linha['id']}"
    descricao = st.session_state.get(f"{k}_desc", linha["descricao"])
    valor = st.session_state.get(f"{k}_valor", linha["valor"])
    tipo = "receita" if valor > 0 else "despesa"
    padrao = linha.get("categoria")
    if padrao not in CATEGORIAS[tipo]:  # o sinal do valor mudou: sugere de novo para o tipo
        padrao = extrato.sugerir_categoria(descricao, valor)
    return descricao, valor, tipo, st.session_state.get(f"{k}_cat_{tipo}", padrao)


def _card_linha(imp: dict, linha: dict) -> None:
    k = f"imp_{imp['lote']}_{linha['id']}"
    confirmado = linha["confirmado"]
    _, _, tipo, categoria_atual = _campos_atuais(imp, linha)
    with st.container(border=True, key=f"{k}_linha"):
        c_info, c_desc, c_valor, c_cat, c_ok, c_fora = st.columns(
            [1.3, 2.6, 1.8, 1.7, 1.1, 1.0], vertical_alignment="bottom")
        selo = chip("Confirmado", "m") if confirmado else chip("Pendente", "t")
        c_info.markdown(f"**{data_br(linha['data'])}**<br>{TIPOS[tipo]}<br>{selo}",
                        unsafe_allow_html=True)
        descricao = c_desc.text_input("Descrição", value=linha["descricao"], key=f"{k}_desc",
                                      disabled=confirmado)
        valor = c_valor.number_input("Valor (R$)", value=float(linha["valor"]), step=0.01,
                                     format="%.2f", key=f"{k}_valor", disabled=confirmado)
        opcoes = CATEGORIAS[tipo]
        categoria = c_cat.selectbox("Categoria", opcoes, index=opcoes.index(categoria_atual),
                                    key=f"{k}_cat_{tipo}", disabled=confirmado)
        if confirmado:
            if c_ok.button("Editar", key=f"{k}_editar", type="tertiary", width="stretch"):
                linha["confirmado"] = False
                st.rerun()
        elif c_ok.button("Confirmar", key=f"{k}_confirmar", type="primary", width="stretch"):
            erro = extrato.validar_linha(valor)
            if erro:
                st.error(erro)
            else:
                linha.update(descricao=descricao.strip(), valor=round(valor, 2),
                             categoria=categoria, confirmado=True)
                st.rerun()
        if c_fora.button("Descartar", key=f"{k}_descartar", type="tertiary", width="stretch"):
            imp["linhas"].remove(linha)
            st.rerun()


def _revisao(imp: dict) -> None:
    linhas = imp["linhas"]
    faltam = extrato.pendentes(linhas)
    resumo, tudo = st.columns([4, 1], vertical_alignment="center")
    with resumo:
        html(f'<div class="of-subtitulo">{escape(imp["arquivo"])} · {len(linhas)} lançamentos · '
             f'{len(linhas) - faltam} confirmados</div>')
    if tudo.button("Confirmar tudo", key="imp_confirmar_tudo", width="stretch", disabled=not faltam):
        atuais = {}
        for linha in linhas:
            descricao, valor, _, categoria = _campos_atuais(imp, linha)
            atuais[linha["id"]] = (descricao, valor, categoria)
        if extrato.confirmar_todas(linhas, atuais):
            st.session_state["aviso_confirmar_tudo"] = True
        st.rerun()
    if st.session_state.pop("aviso_confirmar_tudo", False):
        st.warning(f"{extrato.MSG_VALOR_ZERO} Corrija os cards que continuam pendentes.")
    for linha in list(linhas):
        _card_linha(imp, linha)

    if faltam:
        st.caption(f"Confirme todos os lançamentos para importar "
                   f"({'faltam' if faltam > 1 else 'falta'} {faltam}).")
    cancelar, confirmar = st.columns(2)
    if cancelar.button("Cancelar importação", width="stretch", key="imp_cancelar"):
        _fechar_importacao()
        st.rerun()
    if confirmar.button("Confirmar importação", type="primary", width="stretch",
                        key="imp_confirmar", disabled=not extrato.pode_importar(linhas)):
        try:
            resposta = api.cliente().criar_transacoes_lote(extrato.montar_lote(linhas))
        except api.ErroApi as e:
            st.error(str(e))
            return
        criadas = int(resposta.get("criadas", len(linhas)))
        ano, mes = extrato.mes_mais_recente(linhas)
        dados.invalidar()
        _fechar_importacao()
        # A lista abre no mês do extrato (senão um extrato de outro mês parece não ter sido salvo)
        st.session_state["filtro_mes"] = (ano, mes)
        st.session_state["aviso_importacao"] = (
            f"{criadas} transações importadas. Mostrando {mes_abrev(ano, mes)}." if criadas != 1
            else f"1 transação importada. Mostrando {mes_abrev(ano, mes)}.")
        st.rerun()


def _painel_importacao() -> None:
    imp = st.session_state.get(IMPORTACAO)
    if not imp:
        return
    with st.container(key="card_importacao"):
        html(titulo_card("Importar extrato", "PDF, CSV ou OFX"))
        if imp["linhas"]:
            _revisao(imp)
        else:
            _ler_arquivo(imp)
    html('<div style="height:.9rem"></div>')


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
        if st.button("Importar extrato", width="stretch", key="abrir_importacao"):
            _abrir_importacao()
    if st.session_state.pop("abrir_nova_transacao", False):
        _dialogo_nova()
    if aviso := st.session_state.pop("aviso_importacao", None):
        st.success(aviso)
    _painel_importacao()

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
    if st.session_state.get("filtro_mes") not in opcoes_mes:
        st.session_state["filtro_mes"] = (hoje.year, hoje.month)
    periodo = f1.selectbox("Mês", opcoes_mes, key="filtro_mes",
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
