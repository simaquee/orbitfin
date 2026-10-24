"""Leituras da API com cache na sessão (evita chamadas repetidas a cada interação).

Spec (OpenSpec): openspec/specs/interface-base/spec.md
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from services import api
from services.calculos import limites_mes


def _cache(chave: str, carregar):
    cache = st.session_state.cache
    if chave not in cache:
        cache[chave] = carregar()
    return cache[chave]


def transacoes() -> list[dict]:
    return _cache("transacoes", lambda: api.cliente().listar_transacoes())


def orcamentos(ano: int, mes: int) -> list[dict]:
    inicio, fim = limites_mes(ano, mes)
    return _cache(f"orcamentos:{ano}-{mes:02d}",
                  lambda: api.cliente().listar_orcamentos(inicio, fim))


def invalidar() -> None:
    """Chamar após qualquer escrita."""
    st.session_state.cache = {}


def hoje() -> date:
    return date.today()
