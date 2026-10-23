"""Dashboard (specs: dashboard, sugestoes, autenticacao > saudação)."""
from html import escape

import streamlit as st

from components import dados, graficos, sessao
from components.header import cabecalho
from components.ui import (html, icone, kpi, linha_kpis, linha_progresso, linha_transacao,
                           titulo_card, vazio)
from services.api import ErroApi
from services.calculos import (gastos_por_categoria, linhas_orcamento, ordenar_recentes,
                               saldo_atual, serie_mensal, totais_mes)
from services.formatacao import MESES, mes_abrev, moeda
from services.sugestoes import gerar_sugestoes


def _nova_transacao() -> None:
    st.session_state.pagina = "transacoes"
    st.session_state.abrir_nova_transacao = True


def _ver_todas() -> None:
    st.session_state.pagina = "transacoes"


def _dica_mes(pendente: float, rotulo_mes: str) -> str:
    return f"{moeda(pendente)} pendente · {rotulo_mes}" if pendente > 0 else rotulo_mes


def render() -> None:
    hoje = dados.hoje()
    ano, mes = hoje.year, hoje.month
    rotulo_mes = mes_abrev(ano, mes)

    acao = cabecalho("dashboard", f"Olá, {sessao.primeiro_nome()}. Este é o resumo de "
                                  f"{MESES[mes - 1].lower()} de {ano}.", com_acao=True)
    with acao:
        st.button("Nova transação", type="primary", on_click=_nova_transacao,
                  width="stretch")

    try:
        txs = dados.transacoes()
        orcs = dados.orcamentos(ano, mes)
    except ErroApi as e:
        st.error(str(e))
        return

    saldo = saldo_atual(txs)
    t = totais_mes(txs, ano, mes)
    linha_kpis([
        kpi("Saldo atual", moeda(saldo), "Somente lançamentos pagos", "wallet",
            negativo=saldo < 0, destaque=True),
        kpi("Receitas do mês", moeda(t["receitas"]), _dica_mes(t["receitas_pendentes"], rotulo_mes),
            "arrow-trend-up", tom="m"),
        kpi("Despesas do mês", moeda(t["despesas"]), _dica_mes(t["despesas_pendentes"], rotulo_mes),
            "arrow-trend-down", tom="t"),
        kpi("Resultado do mês", moeda(t["resultado"]), "Receitas − despesas", "scale",
            tom="t" if t["resultado"] < 0 else "m", negativo=t["resultado"] < 0),
    ])
    html('<div style="height:.9rem"></div>')

    grafico, lateral = st.columns([1.75, 1], gap="medium")
    with grafico:
        with st.container(key="card_evolucao"):
            html(titulo_card("Receitas vs despesas", "Últimos 6 meses"))
            serie = serie_mensal(txs, ano, mes, 6)
            graficos.mostrar(graficos.receitas_despesas(
                [mes_abrev(p["ano"], p["mes"]) for p in serie],
                [p["receitas"] for p in serie], [p["despesas"] for p in serie], altura=290))
    with lateral:
        with st.container(key="card_sugestoes"):
            html(titulo_card("Sugestões", rotulo_mes))
            html("".join(f'<div class="of-sugestao">{icone("bulb")}<span>{escape(s)}</span></div>'
                         for s in gerar_sugestoes(txs, orcs, hoje)))

    html('<div style="height:.9rem"></div>')
    c1, c2, c3 = st.columns([1, 1, 1.15], gap="medium")
    with c1:
        with st.container(key="card_categorias"):
            html(titulo_card("Gastos por categoria", rotulo_mes))
            gastos = gastos_por_categoria(txs, ano, mes)
            if gastos:
                graficos.mostrar(graficos.rosca([c for c, _ in gastos], [v for _, v in gastos]))
            else:
                html(vazio("Sem despesas neste mês.", "chart-pie-alt"))
    with c2:
        with st.container(key="card_orcamentos"):
            html(titulo_card("Orçamentos do mês", rotulo_mes))
            linhas = linhas_orcamento(orcs)[:6]
            if linhas:
                html("".join(
                    linha_progresso(l["categoria"], f"{moeda(l['gasto'])} / {moeda(l['limite'])}",
                                    l["percentual"], l["estado"]) for l in linhas))
            else:
                html(vazio("Sem orçamentos carregados.", "wallet"))
    with c3:
        with st.container(key="card_ultimas"):
            html(titulo_card("Últimas transações"))
            recentes = ordenar_recentes(txs)[:6]
            if recentes:
                html("".join(linha_transacao(tx) for tx in recentes))
                st.button("Ver todas", type="tertiary", on_click=_ver_todas, key="ver_todas")
            else:
                html(vazio("Nenhuma transação ainda. Adicione a primeira em Transações.", "receipt"))
