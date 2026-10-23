from __future__ import annotations

from html import escape

import streamlit as st

from components import sessao
from components.ui import html, icone, logo_svg

PAGINAS = [
    ("dashboard", "Dashboard", "apps"),
    ("transacoes", "Transações", "exchange"),
    ("orcamento", "Orçamento", "wallet"),
    ("metas", "Metas", "bullseye-arrow"),
    ("relatorios", "Relatórios", "chart-histogram"),
]


def barra_lateral() -> None:
    usuario = st.session_state.usuario or {}
    nome = usuario.get("nome") or "Usuário"
    with st.sidebar:
        html(f'<div class="of-marca">{logo_svg(32)}<span class="of-marca-nome">OrbitFin</span></div>'
             '<div class="of-menu-rotulo">Menu</div>')
        for chave, rotulo, ico in PAGINAS:
            ativo = st.session_state.pagina == chave
            with st.container(key=f"nav_{chave}_{'on' if ativo else 'off'}"):
                html(icone(ico))
                st.button(rotulo, key=f"btn_nav_{chave}", on_click=sessao.ir_para, args=(chave,),
                          width="stretch")
        html(f'<div class="of-usuario"><span class="of-avatar">{escape(nome[:1].upper())}</span>'
             f'<div><div class="nome">{escape(nome)}</div>'
             f'<div class="email">{escape(usuario.get("email", ""))}</div></div></div>')
        st.button("Sair", key="sair", on_click=sessao.encerrar, width="stretch")


def _trocar_pagina_movel() -> None:
    escolhida = st.session_state.get("nav_movel")
    if escolhida:  # clicar na pílula ativa desmarca; nesse caso a página não muda
        sessao.ir_para(escolhida)


def navegacao_movel() -> None:
    """Navegação no topo para telas estreitas; o CSS só a exibe abaixo de 768px."""
    usuario = st.session_state.usuario or {}
    rotulos = {chave: rotulo for chave, rotulo, _ in PAGINAS}
    st.session_state.nav_movel = st.session_state.pagina  # acompanha trocas feitas por outros botões
    with st.container(key="navmovel"):
        marca, sair = st.columns([3, 1], vertical_alignment="center")
        with marca:
            html(f'<div class="of-marca-movel"><span class="marca">{logo_svg(26)}OrbitFin</span>'
                 f'<span class="usuario">{escape(usuario.get("nome") or "")}</span></div>')
        with sair:
            st.button("Sair", key="sair_movel", on_click=sessao.encerrar, type="tertiary")
        st.pills("Navegação", list(rotulos), format_func=rotulos.get, selection_mode="single",
                 key="nav_movel", on_change=_trocar_pagina_movel, label_visibility="collapsed")
