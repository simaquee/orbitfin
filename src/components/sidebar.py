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
