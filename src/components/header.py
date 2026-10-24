"""Cabeçalho das páginas: rótulo da seção, título, subtítulo e ação principal.

Spec (OpenSpec): openspec/specs/interface-base/spec.md
"""
from __future__ import annotations

from html import escape

import streamlit as st

from components.ui import html

CABECALHOS = {
    "dashboard": ("Visão geral", "Dashboard"),
    "transacoes": ("Movimentações", "Transações"),
    "orcamento": ("Planejamento", "Orçamento"),
    "metas": ("Planejamento", "Metas"),
    "relatorios": ("Análises", "Relatórios"),
}


def cabecalho(pagina: str, subtitulo: str = "", com_acao: bool = False):
    """Desenha rótulo + título; com_acao=True devolve a coluna da direita para um botão."""
    kicker, titulo = CABECALHOS[pagina]
    sub = f'<div class="of-subtitulo">{escape(subtitulo)}</div>' if subtitulo else ""
    bloco = (f'<div class="of-header"><div class="of-kicker">{kicker}</div>'
             f'<div class="of-titulo">{titulo}</div>{sub}</div>')
    if not com_acao:
        html(bloco)
        return None
    esquerda, direita = st.columns([3, 1], vertical_alignment="center")
    with esquerda:
        html(bloco)
    return direita
