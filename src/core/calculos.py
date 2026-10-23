"""Regras de cálculo do OrbitFin (funções puras, sem Streamlit nem rede)."""
from __future__ import annotations

import calendar
from collections import defaultdict
from typing import Iterable

from utils.formatacao import parse_data

LIMIAR_ATENCAO = 85.0     # % do limite (Orçamento)
LIMIAR_RISCO = 0.10       # fração do limite restante (Metas)


# ---------------------------------------------------------------- períodos
def limites_mes(ano: int, mes: int) -> tuple[str, str]:
    ultimo = calendar.monthrange(ano, mes)[1]
    return f"{ano}-{mes:02d}-01", f"{ano}-{mes:02d}-{ultimo:02d}"


def meses_ate(ano: int, mes: int, n: int) -> list[tuple[int, int]]:
    """Os n meses terminando em (ano, mes), em ordem cronológica."""
    resultado = []
    for _ in range(n):
        resultado.append((ano, mes))
        ano, mes = (ano - 1, 12) if mes == 1 else (ano, mes - 1)
    return resultado[::-1]


def no_mes(tx: dict, ano: int, mes: int) -> bool:
    d = parse_data(tx["data"])
    return d.year == ano and d.month == mes


# ------------------------------------------------------------- transações
def filtrar(txs: Iterable[dict], periodo: tuple[int, int] | None = None, tipo: str | None = None,
            status: str | None = None, categoria: str | None = None) -> list[dict]:
    return [
        t for t in txs
        if (periodo is None or no_mes(t, *periodo))
        and (tipo is None or t["tipo"] == tipo)
        and (status is None or t["status"] == status)
        and (categoria is None or t["categoria"] == categoria)
    ]


def ordenar_recentes(txs: Iterable[dict]) -> list[dict]:
    return sorted(txs, key=lambda t: (str(t["data"])[:10], t.get("id") or 0), reverse=True)


def totais(txs: Iterable[dict]) -> dict:
    r = {"receitas": 0.0, "despesas": 0.0, "n_receitas": 0, "n_despesas": 0}
    for t in txs:
        chave = "receitas" if t["tipo"] == "receita" else "despesas"
        r[chave] += float(t["valor"])
        r["n_" + chave] += 1
    r["saldo"] = r["receitas"] - r["despesas"]
    return r


def saldo_atual(txs: Iterable[dict]) -> float:
    """Receitas pagas − despesas pagas de todo o histórico."""
    return totais(filtrar(txs, status="pago"))["saldo"]


def totais_mes(txs: list[dict], ano: int, mes: int) -> dict:
    do_mes = filtrar(txs, (ano, mes))
    t = totais(do_mes)
    pend = totais(filtrar(do_mes, status="pendente"))
    return {"receitas": t["receitas"], "despesas": t["despesas"], "resultado": t["saldo"],
            "receitas_pendentes": pend["receitas"], "despesas_pendentes": pend["despesas"],
            "quantidade": len(do_mes)}


def serie_mensal(txs: list[dict], ano: int, mes: int, n: int = 6) -> list[dict]:
    serie = []
    for a, m in meses_ate(ano, mes, n):
        t = totais(filtrar(txs, (a, m)))
        serie.append({"ano": a, "mes": m, "receitas": t["receitas"], "despesas": t["despesas"],
                      "saldo": t["saldo"]})
    return serie


def por_categoria(txs: list[dict], tipo: str, ano: int, mes: int) -> list[tuple[str, float]]:
    soma: dict[str, float] = defaultdict(float)
    for t in filtrar(txs, (ano, mes), tipo=tipo):
        soma[t["categoria"] or "Outros"] += float(t["valor"])
    return sorted(soma.items(), key=lambda kv: kv[1], reverse=True)


def gastos_por_categoria(txs: list[dict], ano: int, mes: int) -> list[tuple[str, float]]:
    return por_categoria(txs, "despesa", ano, mes)


def taxa_poupanca(receitas: float, despesas: float) -> float:
    return (receitas - despesas) / receitas * 100 if receitas > 0 else 0.0


# ------------------------------------------------------------- relatórios
def resumo_mes(txs: list[dict], ano: int, mes: int) -> dict:
    t = totais(filtrar(txs, (ano, mes)))
    return {"receitas": t["receitas"], "despesas": t["despesas"], "saldo": t["saldo"],
            "poupanca": taxa_poupanca(t["receitas"], t["despesas"])}


def resumo_ano(txs: list[dict], ano: int) -> list[dict]:
    """Sempre 12 meses (zero nos vazios)."""
    return [{"mes": m, **resumo_mes(txs, ano, m)} for m in range(1, 13)]


def serie_diaria(txs: list[dict], ano: int, mes: int) -> list[dict]:
    dias = calendar.monthrange(ano, mes)[1]
    serie = [{"dia": d, "receitas": 0.0, "despesas": 0.0} for d in range(1, dias + 1)]
    for t in filtrar(txs, (ano, mes)):
        chave = "receitas" if t["tipo"] == "receita" else "despesas"
        serie[parse_data(t["data"]).day - 1][chave] += float(t["valor"])
    for ponto in serie:
        ponto["saldo"] = ponto["receitas"] - ponto["despesas"]
    return serie


# ------------------------------------------------------------- orçamentos
def percentual_uso(gasto: float, limite: float) -> float:
    return gasto / limite * 100 if limite > 0 else 0.0


def estado_orcamento(gasto: float, limite: float) -> str:
    if limite > 0 and gasto > limite:
        return "estourado"
    if percentual_uso(gasto, limite) >= LIMIAR_ATENCAO:
        return "atencao"
    return "ok"


def linhas_orcamento(orcamentos: Iterable[dict]) -> list[dict]:
    linhas = []
    for o in orcamentos:
        gasto, limite = float(o.get("gasto") or 0), float(o["limite"])
        linhas.append({**o, "gasto": gasto, "limite": limite,
                       "percentual": percentual_uso(gasto, limite),
                       "restante": limite - gasto, "estado": estado_orcamento(gasto, limite)})
    return sorted(linhas, key=lambda l: l["percentual"], reverse=True)


def indicadores_orcamento(orcamentos: Iterable[dict]) -> dict:
    linhas = linhas_orcamento(orcamentos)
    limite = sum(l["limite"] for l in linhas)
    gasto = sum(l["gasto"] for l in linhas)
    return {"limite_total": limite, "gasto_total": gasto,
            "percentual": percentual_uso(gasto, limite), "disponivel": limite - gasto,
            "estouradas": sum(l["estado"] == "estourado" for l in linhas),
            "categorias": len(linhas)}


# ------------------------------------------------------------------ metas
ORDEM_METAS = {"risco": 0, "teto": 1, "ok": 2, "sem": 3}


def status_meta(gasto: float, limite: float) -> str:
    if limite <= 0:
        return "sem"
    restante = limite - gasto
    if restante <= 0:
        return "teto"
    if restante <= limite * LIMIAR_RISCO:
        return "risco"
    return "ok"


def linhas_metas(orcamentos: Iterable[dict]) -> list[dict]:
    linhas = []
    for o in orcamentos:
        gasto, limite = float(o.get("gasto") or 0), float(o["limite"])
        restante = limite - gasto
        folga = max(restante / limite * 100, 0.0) if limite > 0 else 0.0
        linhas.append({**o, "gasto": gasto, "limite": limite, "restante": restante,
                       "folga": folga, "status": status_meta(gasto, limite)})
    return sorted(linhas, key=lambda l: (ORDEM_METAS[l["status"]], l["folga"]))


def indicadores_metas(orcamentos: Iterable[dict], receitas: float, despesas: float) -> dict:
    linhas = linhas_metas(orcamentos)
    return {
        "poupanca": taxa_poupanca(receitas, despesas),
        "saldo_mes": receitas - despesas,
        "economia_preservada": sum(max(l["restante"], 0) for l in linhas if l["limite"] > 0),
        "no_caminho": sum(l["status"] == "ok" for l in linhas),
        "atencao": sum(l["status"] in ("risco", "teto") for l in linhas),
    }
