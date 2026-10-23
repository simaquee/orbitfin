"""Página Metas — contenção de gastos sobre os limites (spec: metas)."""
from __future__ import annotations

import streamlit as st

from core import dados
from ui.header import cabecalho
from ui.seletores import seletor_mes
from ui.blocos import chip, html, info, kpi, linha_kpis, linha_progresso, titulo_card, vazio
from core import api
from core.calculos import indicadores_metas, linhas_metas, totais_mes
from utils.formatacao import mes_abrev, moeda, percentual
from commands.orcamento import formulario_limite

SELOS = {"ok": ("No caminho", "m"), "risco": ("Em risco", "t"), "teto": ("Teto atingido", "tc"),
         "sem": ("Sem meta", "m")}
BARRAS = {"ok": "ok", "risco": "atencao", "teto": "estourado", "sem": "ok"}


@st.dialog("Ajustar meta")
def _dialogo_meta(linha: dict, rotulo_mes: str) -> None:
    formulario_limite(linha, rotulo_mes, "Teto da meta (R$)")


def _sub(linha: dict) -> tuple[str, bool]:
    if linha["status"] == "teto":
        texto = f"Gastou {moeda(linha['gasto'])} de {moeda(linha['limite'])}"
        if linha["gasto"] > linha["limite"]:
            texto += f" · ultrapassou {moeda(-linha['restante'])}"
        return texto, True
    if linha["status"] == "sem":
        return "Defina um limite para acompanhar esta meta", False
    return f"{moeda(linha['restante'])} ainda cabem no teto", linha["status"] == "risco"


def render() -> None:
    acao = cabecalho("metas", "Quanto ainda cabe em cada teto de gasto.", com_acao=True)
    with acao:
        ano, mes = seletor_mes("mes_metas")
    rotulo_mes = mes_abrev(ano, mes)

    try:
        orcs = dados.orcamentos(ano, mes)
        txs = dados.transacoes()
    except api.ErroApi as e:
        st.error(str(e))
        return

    t = totais_mes(txs, ano, mes)
    ind = indicadores_metas(orcs, t["receitas"], t["despesas"])
    linha_kpis([
        kpi("Poupança do mês", percentual(ind["poupanca"]),
            f"{moeda(ind['saldo_mes'])} de saldo · {rotulo_mes}", "piggy-bank",
            negativo=ind["poupanca"] < 0, destaque=True),
        kpi("Economia preservada", moeda(ind["economia_preservada"]),
            "Soma do que ainda cabe nos tetos", "shield-check"),
        kpi("No caminho", str(ind["no_caminho"]), "metas com folga acima de 10%", "check-circle"),
        kpi("Atenção", str(ind["atencao"]), "em risco ou teto atingido", "triangle-warning",
            tom="t", negativo=ind["atencao"] > 0),
    ])
    html('<div style="height:.9rem"></div>')
    html(info("Cada meta corresponde ao teto de gasto da categoria no mês. A barra mostra quanto "
              "ainda cabe no teto — quanto mais cheia, melhor a contenção. Ajustar uma meta "
              "altera o mesmo limite da página Orçamento."))
    html('<div style="height:.9rem"></div>')

    with st.container(key="card_metas"):
        html(titulo_card("Metas por categoria", rotulo_mes))
        linhas = linhas_metas(orcs)
        if not linhas:
            html(vazio("Nenhuma meta disponível. Cadastre limites em Orçamento.", "bullseye-arrow"))
            return
        for linha in linhas:
            corpo, botao = st.columns([10, 1.2], vertical_alignment="center", gap="small")
            sub, destaque = _sub(linha)
            texto_selo, tom = SELOS[linha["status"]]
            corpo.markdown(linha_progresso(
                linha["categoria"],
                f"{moeda(max(linha['restante'], 0))} / {moeda(linha['limite'])}",
                linha["folga"], BARRAS[linha["status"]], chip(texto_selo, tom), sub, destaque),
                unsafe_allow_html=True)
            if botao.button("Ajustar", key=f"meta_{linha['id']}", type="tertiary"):
                _dialogo_meta(linha, rotulo_mes)
