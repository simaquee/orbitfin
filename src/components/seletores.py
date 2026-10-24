"""Seletores compartilhados entre páginas.

Spec (OpenSpec): openspec/specs/orcamentos/spec.md, openspec/specs/metas/spec.md
"""
from __future__ import annotations

import streamlit as st

from components import dados
from services.calculos import meses_ate
from services.formatacao import mes_abrev


def seletor_mes(chave: str, n: int = 12) -> tuple[int, int]:
    """Selectbox com os últimos n meses (padrão: mês atual)."""
    hoje = dados.hoje()
    opcoes = meses_ate(hoje.year, hoje.month, n)[::-1]
    return st.selectbox("Mês", opcoes, format_func=lambda p: mes_abrev(*p), key=chave,
                        label_visibility="collapsed")
