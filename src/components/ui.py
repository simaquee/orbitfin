"""Blocos visuais reutilizáveis (HTML + classes de components/theme.py)."""
from __future__ import annotations

from html import escape
from typing import Sequence

import streamlit as st

from components.theme import MARINHO, TERRACOTA
from services.formatacao import data_br, moeda


def html(conteudo: str) -> None:
    st.markdown(conteudo, unsafe_allow_html=True)


def icone(nome: str) -> str:
    return f'<i class="fi fi-rr-{nome}"></i>'


def logo_svg(tamanho: int = 30) -> str:
    """Planeta pentagonal Terracota com anel de órbita."""
    return (
        f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 40 40" aria-hidden="true">'
        '<polygon points="20,7 32,15.5 27.5,29.5 12.5,29.5 8,15.5" fill="#E05638"/>'
        '<ellipse cx="20" cy="19.5" rx="18" ry="6.5" fill="none" stroke="currentColor" '
        'stroke-width="2" opacity=".55" transform="rotate(-18 20 19.5)"/>'
        "</svg>"
    )


def kpi(rotulo: str, valor: str, dica: str = "", ico: str = "", tom: str = "m",
        negativo: bool = False, destaque: bool = False, extra: str = "") -> str:
    classes = "of-kpi destaque" if destaque else "of-kpi"
    ico_html = f'<span class="of-ico {tom}">{icone(ico)}</span>' if ico else ""
    return (
        f'<div class="{classes}"><div class="of-kpi-topo">'
        f'<span class="of-kpi-rotulo">{escape(rotulo)}</span>{ico_html}</div>'
        f'<div class="of-kpi-valor{" neg" if negativo else ""}">{escape(valor)}</div>'
        f'<div class="of-kpi-dica">{escape(dica)}</div>{extra}</div>'
    )


def linha_kpis(cards: Sequence[str]) -> None:
    for coluna, card in zip(st.columns(len(cards), gap="small"), cards):
        with coluna:
            html(card)


def chip(texto: str, tom: str = "m") -> str:
    return f'<span class="of-chip {tom}">{escape(texto)}</span>'


def barra(percentual: float, estado: str = "ok") -> str:
    largura = max(0.0, min(percentual, 100.0))
    classe = "" if estado == "ok" else estado
    return f'<div class="of-barra"><span class="{classe}" style="width:{largura:.1f}%"></span></div>'


def linha_progresso(nome: str, valores: str, percentual: float, estado: str,
                    selo: str = "", sub: str = "", sub_destaque: bool = False) -> str:
    sub_html = f'<div class="sub{" t" if sub_destaque else ""}">{escape(sub)}</div>' if sub else ""
    return (
        f'<div class="of-linha-orc"><div class="cab"><span class="nome">{escape(nome)} {selo}</span>'
        f'<span class="valores">{escape(valores)}</span></div>'
        f"{barra(percentual, estado)}{sub_html}</div>"
    )


ICONES_CATEGORIA = {
    "Alimentação": "utensils", "Moradia": "home", "Transporte": "car-side", "Lazer": "ticket",
    "Saúde": "heart", "Educação": "graduation-cap", "Outros": "apps", "Salário": "briefcase",
    "Freelance": "laptop", "Investimentos": "chart-line-up",
}


def linha_transacao(tx: dict, mostrar_status: bool = False) -> str:
    receita = tx.get("tipo") == "receita"
    tom = "r" if receita else "d"
    categoria = tx.get("categoria") or "—"
    descricao = tx.get("descricao") or ("Receita" if receita else "Despesa")
    sinal = "+" if receita else "−"
    selo = ""
    if mostrar_status:
        selo = chip("Pago", "m") if tx.get("status") == "pago" else chip("Pendente", "t")
    ico = ICONES_CATEGORIA.get(categoria, "coins")
    return (
        f'<div class="of-tx"><span class="av {tom}">{icone(ico)}</span>'
        f'<div class="info"><div class="cat">{escape(categoria)} {selo}</div>'
        f'<div class="meta">{data_br(tx["data"])} · {escape(descricao)}</div></div>'
        f'<span class="val {tom}">{sinal} {moeda(float(tx["valor"]))}</span></div>'
    )


def vazio(texto: str, ico: str = "folder-open") -> str:
    return f'<div class="of-vazio">{icone(ico)}{escape(texto)}</div>'


def titulo_card(titulo: str, detalhe: str = "") -> str:
    det = f"<small>{escape(detalhe)}</small>" if detalhe else ""
    return f'<div class="of-card-titulo"><span>{escape(titulo)}</span>{det}</div>'


def info(texto: str) -> str:
    return f'<div class="of-info">{icone("info")}<span>{escape(texto)}</span></div>'


def sparkline(valores: Sequence[float], cor: str = MARINHO) -> str:
    """Minilinha SVG (sem eixos) para cards de KPI."""
    if not valores:
        return ""
    largura, altura = 200, 34
    minimo, maximo = min(valores), max(valores)
    faixa = (maximo - minimo) or 1
    passo = largura / max(len(valores) - 1, 1)
    pontos = " ".join(
        f"{i * passo:.1f},{altura - 3 - (v - minimo) / faixa * (altura - 6):.1f}"
        for i, v in enumerate(valores)
    )
    return (
        f'<svg class="of-spark" viewBox="0 0 {largura} {altura}" preserveAspectRatio="none" '
        f'width="100%"><polyline points="{pontos}" fill="none" stroke="{cor}" '
        'stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" '
        'vector-effect="non-scaling-stroke"/></svg>'
    )


def cor_tipo(tipo: str) -> str:
    return MARINHO if tipo == "receita" else TERRACOTA


_ORBITAS_SVG = (
    '<svg viewBox="0 0 560 560" aria-hidden="true">'
    '<g fill="none" stroke="#fff">'
    '<circle cx="300" cy="260" r="250" stroke-opacity=".06"/>'
    '<circle cx="300" cy="260" r="190" stroke-opacity=".09"/>'
    '<circle cx="300" cy="260" r="130" stroke-opacity=".12" stroke-dasharray="4 8"/>'
    '<ellipse cx="300" cy="260" rx="230" ry="80" stroke-opacity=".18" transform="rotate(-20 300 260)"/>'
    "</g>"
    '<polygon points="300,200 357,241 335,309 265,309 243,241" fill="#E05638"/>'
    '<polygon points="300,200 357,241 335,309 265,309 243,241" fill="url(#brilho)"/>'
    '<circle cx="516" cy="182" r="9" fill="#E05638"/><circle cx="96" cy="330" r="5" fill="#fff" fill-opacity=".7"/>'
    '<circle cx="300" cy="70" r="4" fill="#fff" fill-opacity=".45"/>'
    '<defs><linearGradient id="brilho" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/>'
    "</linearGradient></defs></svg>"
)


def painel_marca(titulo: str, texto: str) -> str:
    return (f'<div class="of-painel">{_ORBITAS_SVG}'
            f"<h2>{escape(titulo)}</h2><p>{escape(texto)}</p></div>")


def cabecalho_auth(titulo: str, subtitulo: str) -> str:
    return (f'<div class="of-auth-marca">{logo_svg(30)}<span>OrbitFin</span></div>'
            f'<div class="of-auth-titulo">{escape(titulo)}</div>'
            f'<div class="of-auth-sub">{escape(subtitulo)}</div>')
