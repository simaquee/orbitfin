"""Página Relatórios.

Spec (OpenSpec): openspec/specs/relatorios/spec.md
"""
from __future__ import annotations

import streamlit as st

from components import dados, graficos
from components.header import cabecalho
from components.theme import MARINHO, TERRACOTA
from components.ui import html, kpi, linha_kpis, linha_transacao, sparkline, titulo_card, vazio
from services import api
from services.calculos import filtrar, ordenar_recentes, por_categoria, resumo_ano, resumo_mes, serie_diaria
from services.formatacao import MESES, MESES_ABREV, moeda, percentual

MAX_LANCAMENTOS = 40


def _rosca(titulo: str, rotulo: str, itens: list[tuple[str, float]], msg_vazio: str, chave: str):
    with st.container(key=chave):
        html(titulo_card(titulo, rotulo))
        if itens:
            graficos.mostrar(graficos.rosca([c for c, _ in itens], [v for _, v in itens]))
        else:
            html(vazio(msg_vazio, "chart-pie-alt"))


def render() -> None:
    cabecalho("relatorios", "Evolução das suas finanças por mês e por ano.")
    hoje = dados.hoje()

    f1, f2, f3 = st.columns([1, 1, 1.4], vertical_alignment="bottom")
    anos = list(range(hoje.year, hoje.year - 6, -1))
    ano = f1.selectbox("Ano", anos)
    mes = f2.selectbox("Mês", range(1, 13), index=hoje.month - 1, format_func=lambda m: MESES[m - 1])
    visao = f3.segmented_control("Visão do gráfico", ["Mensal", "Anual"], default="Mensal",
                                 key="visao_relatorio") or "Mensal"

    try:
        txs = dados.transacoes()
    except api.ErroApi as e:
        st.error(str(e))
        return

    m = resumo_mes(txs, ano, mes)
    ano_meses = resumo_ano(txs, ano)
    rotulo = f"{MESES[mes - 1][:3]} · mês"
    linha_kpis([
        kpi("Receitas", moeda(m["receitas"]), rotulo, "arrow-trend-up",
            extra=sparkline([p["receitas"] for p in ano_meses], MARINHO)),
        kpi("Despesas", moeda(m["despesas"]), rotulo, "arrow-trend-down", tom="t",
            extra=sparkline([p["despesas"] for p in ano_meses], TERRACOTA)),
        kpi("Saldo", moeda(m["saldo"]), "receitas − despesas", "scale", negativo=m["saldo"] < 0,
            tom="t" if m["saldo"] < 0 else "m",
            extra=sparkline([p["saldo"] for p in ano_meses], MARINHO)),
        kpi("Poupança", percentual(m["poupanca"]), "sobre receitas do mês", "piggy-bank",
            negativo=m["poupanca"] < 0, tom="t" if m["poupanca"] < 0 else "m",
            extra=sparkline([p["poupanca"] for p in ano_meses], TERRACOTA)),
    ])
    html('<div style="height:.9rem"></div>')

    principal, lateral = st.columns([1.75, 1], gap="medium")
    with principal:
        with st.container(key="card_hero"):
            if visao == "Anual":
                x = [a.capitalize() for a in MESES_ABREV]
                pontos, titulo = ano_meses, f"Visão geral · {ano}"
                receitas_periodo = sum(p["receitas"] for p in ano_meses)
                despesas_periodo = sum(p["despesas"] for p in ano_meses)
            else:
                pontos = serie_diaria(txs, ano, mes)
                x, titulo = [p["dia"] for p in pontos], f"Visão geral · {MESES[mes - 1]} {ano}"
                receitas_periodo, despesas_periodo = m["receitas"], m["despesas"]
            html(titulo_card(titulo, f"{moeda(receitas_periodo)} em receitas"))
            graficos.mostrar(graficos.receitas_despesas(
                x, [p["receitas"] for p in pontos], [p["despesas"] for p in pontos],
                [p["saldo"] for p in pontos], altura=330))
            if not any(p["receitas"] or p["despesas"] for p in pontos):
                st.caption("Sem lançamentos neste período.")
    with lateral:
        with st.container(key="card_medidor"):
            html(titulo_card("Gasto vs receita", "Despesas no período"))
            graficos.mostrar(graficos.medidor(despesas_periodo, receitas_periodo))
            if receitas_periodo > 0:
                texto = f"{percentual(min(despesas_periodo / receitas_periodo * 100, 999))} das receitas"
            else:
                texto = "sem receitas no período"
            html(f'<div style="text-align:center;font-weight:700;margin-top:-.4rem">{texto}</div>')

    html('<div style="height:.9rem"></div>')
    d1, d2 = st.columns(2, gap="medium")
    rotulo_mes = f"{MESES[mes - 1]} {ano}"
    with d1:
        _rosca("Despesas por categoria", rotulo_mes, por_categoria(txs, "despesa", ano, mes),
               "Sem despesas neste mês.", "card_rosca_desp")
    with d2:
        _rosca("Receitas por categoria", rotulo_mes, por_categoria(txs, "receita", ano, mes),
               "Sem receitas neste mês.", "card_rosca_rec")

    html('<div style="height:.9rem"></div>')
    with st.container(key="card_comparativo"):
        html(titulo_card(f"Comparativo mensal · {ano}"))
        graficos.mostrar(graficos.comparativo(
            [a.capitalize() for a in MESES_ABREV], [p["receitas"] for p in ano_meses],
            [p["despesas"] for p in ano_meses], [p["saldo"] for p in ano_meses]))

    html('<div style="height:.9rem"></div>')
    rec_ano = sum(p["receitas"] for p in ano_meses)
    desp_ano = sum(p["despesas"] for p in ano_meses)
    linha_kpis([
        kpi("Receitas anuais", moeda(rec_ano), str(ano), "arrow-trend-up"),
        kpi("Despesas anuais", moeda(desp_ano), str(ano), "arrow-trend-down", tom="t"),
        kpi("Saldo anual", moeda(rec_ano - desp_ano), str(ano), "scale",
            negativo=rec_ano < desp_ano, tom="t" if rec_ano < desp_ano else "m"),
    ])

    html('<div style="height:.9rem"></div>')
    with st.container(key="card_lancamentos"):
        do_mes = ordenar_recentes(filtrar(txs, (ano, mes)))
        html(titulo_card(f"Lançamentos · {rotulo_mes}"))
        if not do_mes:
            html(vazio("Nenhuma transação neste período. Cadastre em Transações.", "receipt"))
        else:
            html("".join(linha_transacao(tx, mostrar_status=True)
                         for tx in do_mes[:MAX_LANCAMENTOS]))
            if len(do_mes) > MAX_LANCAMENTOS:
                st.caption(f"Mostrando {MAX_LANCAMENTOS} de {len(do_mes)} lançamentos.")
