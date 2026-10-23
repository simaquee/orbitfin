"""OrbitFin — entrypoint e roteamento."""
import streamlit as st

from core import sessao
from ui.sidebar import barra_lateral, navegacao_movel
from ui.theme import aplicar_tema, configurar_pagina
from ui.blocos import html
from core.api import MSG_CONFIG, MSG_SESSAO, SessaoExpirada, base_url_configurada
from commands import cadastro, dashboard, login, metas, orcamento, relatorios, transacoes

PAGINAS = {
    "dashboard": dashboard.render,
    "transacoes": transacoes.render,
    "orcamento": orcamento.render,
    "metas": metas.render,
    "relatorios": relatorios.render,
}

configurar_pagina()
sessao.iniciar()

if not base_url_configurada():
    aplicar_tema(auth=True)
    html('<div class="of-titulo">OrbitFin</div>')
    st.warning(MSG_CONFIG)
    st.stop()

expirou = False
try:
    if not sessao.autenticado():
        aplicar_tema(auth=True)
        (cadastro.render if st.session_state.tela_auth == "cadastro" else login.render)()
    else:
        aplicar_tema()
        barra_lateral()
        navegacao_movel()
        PAGINAS.get(st.session_state.pagina, dashboard.render)()
except SessaoExpirada:
    expirou = True

if expirou:
    sessao.encerrar(aviso=MSG_SESSAO)
    st.rerun()
