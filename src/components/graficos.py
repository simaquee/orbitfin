"""Gráficos Plotly com a paleta oficial e formatação pt-BR.

Spec (OpenSpec): openspec/specs/dashboard/spec.md, openspec/specs/relatorios/spec.md
"""
from __future__ import annotations

from typing import Sequence

import plotly.graph_objects as go
import streamlit as st

from components.theme import FONTE as FONTE_MARCA
from components.theme import MARINHO, TERRACOTA, rgba
from services.formatacao import moeda

FONTE = f"{FONTE_MARCA}, system-ui, sans-serif"
CORES_ROSCA = [TERRACOTA, MARINHO, rgba(TERRACOTA, .6), rgba(MARINHO, .6), rgba(TERRACOTA, .32),
               rgba(MARINHO, .32), rgba(MARINHO, .14)]


def _layout(fig: go.Figure, altura: int, legenda: bool = True) -> go.Figure:
    fig.update_layout(
        height=altura, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", separators=",.",
        font=dict(family=FONTE, color=rgba(MARINHO, .7), size=12),
        hoverlabel=dict(font_family=FONTE, bgcolor="#fff", bordercolor=rgba(MARINHO, .15)),
        showlegend=legenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(color=MARINHO)),
    )
    fig.update_xaxes(showgrid=False, linecolor=rgba(MARINHO, .12), tickfont=dict(size=11),
                     fixedrange=True)
    fig.update_yaxes(gridcolor=rgba(MARINHO, .07), zeroline=False, tickprefix="R$ ",
                     tickformat=",.0f", tickfont=dict(size=11), fixedrange=True)
    if _sem_valores(fig):
        # Sem dados o Plotly usa o intervalo -1..1, que com ",.0f" repete "R$ 1" e "R$ −1".
        fig.update_yaxes(range=[0, 100])
    return fig


def _sem_valores(fig: go.Figure) -> bool:
    valores = [v for trace in fig.data if getattr(trace, "y", None) is not None for v in trace.y]
    return all(abs(v or 0) < 1 for v in valores)


def mostrar(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def _linha(nome: str, x, y, cor: str, **extra) -> go.Scatter:
    # Linhas retas: a suavização (spline) desenha valores que não existem, como mergulhos abaixo de zero.
    return go.Scatter(
        name=nome, x=list(x), y=list(y), mode="lines", line=dict(color=cor, width=3, shape="linear"),
        customdata=[moeda(v) for v in y], hovertemplate=f"{nome}: %{{customdata}}<extra></extra>",
        **extra,
    )


def receitas_despesas(x: Sequence[str], receitas: Sequence[float], despesas: Sequence[float],
                      saldo: Sequence[float] | None = None, altura: int = 300) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(_linha("Receitas", x, receitas, MARINHO, fill="tozeroy",
                         fillcolor=rgba(MARINHO, .06)))
    fig.add_trace(_linha("Despesas", x, despesas, TERRACOTA, fill="tozeroy",
                         fillcolor=rgba(TERRACOTA, .06)))
    if saldo is not None:
        fig.add_trace(go.Scatter(
            name="Saldo", x=list(x), y=list(saldo), mode="lines",
            line=dict(color=MARINHO, width=2, dash="dot"),
            customdata=[moeda(v) for v in saldo], hovertemplate="Saldo: %{customdata}<extra></extra>"))
    fig.update_layout(hovermode="x unified")
    return _layout(fig, altura)


def rosca(rotulos: Sequence[str], valores: Sequence[float], altura: int = 260) -> go.Figure:
    # Percentual na legenda (texto marinho legível), não em branco dentro de fatias claras ou terracota.
    total = sum(valores) or 1
    legendas = [f"{r} · {v / total:.0%}" for r, v in zip(rotulos, valores)]
    fig = go.Figure(go.Pie(
        labels=legendas, values=list(valores), hole=0.62, sort=False, textinfo="none",
        marker=dict(colors=CORES_ROSCA[:len(valores)], line=dict(color="#fff", width=2)),
        customdata=[moeda(v) for v in valores],
        hovertemplate="%{label}: %{customdata}<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{moeda(sum(valores))}</b><br><span style='font-size:11px'>total</span>",
                       showarrow=False, font=dict(size=12, color=MARINHO, family=FONTE))
    fig = _layout(fig, altura)
    fig.update_layout(legend=dict(orientation="v", y=0.5, yanchor="middle", x=1.02, xanchor="left"))
    return fig


def medidor(despesas: float, receitas: float, altura: int = 250) -> go.Figure:
    teto = max(receitas, despesas, 1)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=despesas,
        number=dict(prefix="R$ ", valueformat=",.0f", font=dict(size=30, color=MARINHO, family=FONTE)),
        gauge=dict(
            axis=dict(range=[0, teto], tickformat=",.0f", tickfont=dict(size=10),
                      tickcolor=rgba(MARINHO, .3)),
            bar=dict(color=TERRACOTA, thickness=0.32), bgcolor="rgba(0,0,0,0)", borderwidth=0,
            steps=[dict(range=[0, teto * .6], color=rgba(TERRACOTA, .08)),
                   dict(range=[teto * .6, teto * .9], color=rgba(TERRACOTA, .18)),
                   dict(range=[teto * .9, teto], color=rgba(TERRACOTA, .32))],
            threshold=dict(line=dict(color=MARINHO, width=3), thickness=0.85,
                           value=receitas if receitas > 0 else teto),
        ),
    ))
    fig = _layout(fig, altura, legenda=False)
    fig.update_layout(margin=dict(l=24, r=24, t=16, b=0))
    return fig


def comparativo(x: Sequence[str], receitas: Sequence[float], despesas: Sequence[float],
                saldo: Sequence[float], altura: int = 320) -> go.Figure:
    fig = go.Figure()
    for nome, valores, cor in (("Receitas", receitas, MARINHO), ("Despesas", despesas, TERRACOTA)):
        fig.add_trace(go.Bar(name=nome, x=list(x), y=list(valores), marker_color=cor,
                             marker_cornerradius=4, customdata=[moeda(v) for v in valores],
                             hovertemplate=f"{nome}: %{{customdata}}<extra></extra>"))
    fig.add_trace(go.Scatter(name="Saldo", x=list(x), y=list(saldo), mode="lines+markers",
                             line=dict(color=MARINHO, width=2, dash="dot"),
                             marker=dict(size=6, color="#fff", line=dict(color=MARINHO, width=2)),
                             customdata=[moeda(v) for v in saldo],
                             hovertemplate="Saldo: %{customdata}<extra></extra>"))
    fig.update_layout(barmode="group", bargap=0.35, bargroupgap=0.12, hovermode="x unified")
    return _layout(fig, altura)
