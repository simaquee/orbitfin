"""Tela de cadastro (spec: autenticacao)."""
import streamlit as st

from components import sessao
from components.ui import cabecalho_auth, html, painel_marca
from services import api
from services.validacao import validar_cadastro


def _ir_para_login() -> None:
    st.session_state.tela_auth = "login"


def render() -> None:
    esquerda, direita = st.columns([1, 1.15], gap="large", vertical_alignment="center")
    with esquerda:
        with st.container(key="card_auth"):
            html(cabecalho_auth("Crie sua conta",
                                "Leva menos de um minuto para começar a organizar seu dinheiro."))
            with st.form("form_cadastro", border=False):
                nome = st.text_input("Nome completo", placeholder="Seu nome")
                email = st.text_input("E-mail", placeholder="voce@email.com")
                senha = st.text_input("Senha", type="password",
                                      placeholder="Mín. 8 caracteres, 1 letra e 1 número")
                confirmacao = st.text_input("Confirmar senha", type="password",
                                            placeholder="Repita a senha")
                enviar = st.form_submit_button("Criar conta", type="primary",
                                               width="stretch")

            if enviar:
                erro = validar_cadastro(nome, email, senha, confirmacao)
                if erro:
                    st.error(erro)
                else:
                    try:
                        resposta = api.cliente().cadastrar(nome.strip(), email.strip().lower(), senha)
                    except api.ErroApi as e:
                        st.error(str(e))
                    else:
                        sessao.abrir(resposta)
                        st.rerun()

            html('<div class="of-auth-alterna">Já tem uma conta?</div>')
            st.button("Fazer login", key="alternar_login", on_click=_ir_para_login,
                      width="stretch")
    with direita:
        html(painel_marca("Comece a organizar seu dinheiro.",
                          "Cadastro rápido, orçamentos prontos por categoria e um painel "
                          "que mostra para onde vai cada real."))
