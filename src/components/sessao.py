"""Estado de sessão do Streamlit (token, usuário, navegação, cache de dados).

Spec (OpenSpec): openspec/specs/autenticacao/spec.md
"""
from __future__ import annotations

import streamlit as st

PADROES = {"token": None, "usuario": None, "pagina": "dashboard", "tela_auth": "login",
           "aviso": None, "cache": {}}


def iniciar() -> None:
    for chave, valor in PADROES.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor.copy() if isinstance(valor, dict) else valor


def autenticado() -> bool:
    return bool(st.session_state.token)


def abrir(resposta: dict) -> None:
    """Inicia a sessão com a resposta de /login ou /register."""
    st.session_state.token = resposta["access_token"]
    st.session_state.usuario = {"id": resposta.get("user_id"), "nome": resposta.get("name") or "",
                                "email": resposta.get("email") or ""}
    st.session_state.pagina = "dashboard"
    st.session_state.cache = {}


def encerrar(aviso: str | None = None) -> None:
    st.session_state.token = None
    st.session_state.usuario = None
    st.session_state.pagina = "dashboard"
    st.session_state.tela_auth = "login"
    st.session_state.cache = {}
    st.session_state.aviso = aviso


def primeiro_nome() -> str:
    nome = (st.session_state.usuario or {}).get("nome", "").strip()
    return nome.split()[0] if nome else "Usuário"


def ir_para(pagina: str) -> None:
    st.session_state.pagina = pagina
