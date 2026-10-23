"""Página Orçamento (spec: orcamentos)."""
from __future__ import annotations

import streamlit as st

from components import dados
from components.header import cabecalho
from components.seletores import seletor_mes
from components.ui import chip, html, kpi, linha_kpis, linha_progresso, titulo_card, vazio
from services import api
from services.calculos import indicadores_orcamento, linhas_orcamento
from services.formatacao import mes_abrev, moeda, percentual
from services.validacao import validar_limite


def formulario_limite(linha: dict, rotulo_mes: str, campo: str) -> None:
    """Corpo compartilhado pelos diálogos de Orçamento e Metas."""
    st.markdown(f"**{linha['categoria']}**")
    st.caption(f"Gasto em {rotulo_mes}: {moeda(linha['gasto'])} · o novo limite vale para todos os meses.")
    novo = st.number_input(campo, min_value=0.0, step=50.0, format="%.2f",
                           value=float(linha["limite"]), key=f"limite_{linha['id']}")
    salvar, cancelar = st.columns(2)
    if cancelar.button("Cancelar", width="stretch", key="limite_cancelar"):
        st.rerun()
    if salvar.button("Salvar", type="primary", width="stretch", key="limite_salvar"):
        erro = validar_limite(novo)
        if erro:
            st.error(erro)
            return
        try:
            api.cliente().alterar_limite(linha["id"], round(novo, 2))
        except api.ErroApi as e:
            st.error(str(e))
            return
        dados.invalidar()
        st.rerun()


@st.dialog("Ajustar limite")
def _dialogo_limite(linha: dict, rotulo_mes: str) -> None:
    formulario_limite(linha, rotulo_mes, "Novo limite (R$)")


def _selo(linha: dict) -> str:
    if linha["estado"] == "estourado":
        return chip("Estourou", "tc")
    return chip(percentual(linha["percentual"]), "t" if linha["estado"] == "atencao" else "m")


def _sub(linha: dict) -> tuple[str, bool]:
    if linha["estado"] == "estourado":
        return f"Ultrapassou {moeda(-linha['restante'])}", True
    return f"{moeda(max(linha['restante'], 0))} disponível", False


def render() -> None:
    acao = cabecalho("orcamento", "Limites mensais de gasto por categoria.", com_acao=True)
    with acao:
        ano, mes = seletor_mes("mes_orcamento")
    rotulo_mes = mes_abrev(ano, mes)

    try:
        orcs = dados.orcamentos(ano, mes)
    except api.ErroApi as e:
        st.error(str(e))
        return

    ind = indicadores_orcamento(orcs)
    linha_kpis([
        kpi("Limite total", moeda(ind["limite_total"]), f"{ind['categorias']} categorias", "wallet",
            destaque=True),
        kpi("Gasto total", moeda(ind["gasto_total"]), f"{percentual(ind['percentual'])} do limite",
            "shopping-cart", tom="t"),
        kpi("Disponível", moeda(ind["disponivel"]), "Limite total − gasto total", "piggy-bank",
            negativo=ind["disponivel"] < 0, tom="t" if ind["disponivel"] < 0 else "m"),
        kpi("Estouradas", str(ind["estouradas"]), "categorias acima do limite", "triangle-warning",
            tom="t" if ind["estouradas"] else "m", negativo=ind["estouradas"] > 0),
    ])
    html('<div style="height:.9rem"></div>')

    with st.container(key="card_orcamento"):
        html(titulo_card("Por categoria", rotulo_mes))
        linhas = linhas_orcamento(orcs)
        if not linhas:
            html(vazio("Nenhum orçamento carregado.", "wallet"))
            return
        for linha in linhas:
            corpo, botao = st.columns([10, 1.2], vertical_alignment="center", gap="small")
            sub, destaque = _sub(linha)
            corpo.markdown(linha_progresso(
                linha["categoria"], f"{moeda(linha['gasto'])} / {moeda(linha['limite'])}",
                linha["percentual"], linha["estado"], _selo(linha), sub, destaque),
                unsafe_allow_html=True)
            if botao.button("Ajustar", key=f"ajustar_{linha['id']}", type="tertiary"):
                _dialogo_limite(linha, rotulo_mes)
