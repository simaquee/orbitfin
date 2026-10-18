"""Tela de login (spec: autenticacao)."""
import streamlit as st

from components import sessao
from components.ui import cabecalho_auth, html, painel_marca
from services import api
from services.validacao import validar_login


def _ir_para_cadastro() -> None:
    st.session_state.tela_auth = "cadastro"


def render() -> None:
    esquerda, direita = st.columns([1, 1.15], gap="large", vertical_alignment="center")
    with esquerda:
        with st.container(key="card_auth"):
            html(cabecalho_auth("Bem-vindo de volta",
                                "Entre para acompanhar saldo, orçamentos e metas."))
            if st.session_state.aviso:
                st.info(st.session_state.aviso)
                st.session_state.aviso = None

            with st.form("form_login", border=False):
                email = st.text_input("E-mail", placeholder="voce@email.com")
                senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                enviar = st.form_submit_button("Entrar", type="primary", width="stretch")

            if enviar:
                erro = validar_login(email, senha)
                if erro:
                    st.error(erro)
                else:
                    try:
                        resposta = api.cliente().entrar(email.strip().lower(), senha)
                    except api.ErroApi as e:
                        st.error(str(e))
                    else:
                        sessao.abrir(resposta)
                        st.rerun()

            html('<div class="of-auth-alterna">Ainda não tem uma conta?</div>')
            st.button("Criar conta", key="alternar_cadastro", on_click=_ir_para_cadastro,
                      width="stretch")
    with direita:
        html(painel_marca("Suas finanças em órbita.",
                          "Receitas, despesas e limites por categoria em um só painel — "
                          "com sugestões automáticas para fechar o mês no azul."))
