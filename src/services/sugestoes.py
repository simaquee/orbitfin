"""Sugestões financeiras geradas por regras.

Spec (OpenSpec): openspec/specs/sugestoes/spec.md
"""
from __future__ import annotations

from datetime import date

from services.calculos import filtrar, linhas_orcamento, taxa_poupanca, totais
from services.formatacao import moeda, percentual

MAX_SUGESTOES = 3
MSG_SEM_DADOS = "Registre suas transações do mês para receber sugestões."


def gerar_sugestoes(transacoes: list[dict], orcamentos: list[dict], hoje: date) -> list[str]:
    do_mes = filtrar(transacoes, (hoje.year, hoje.month))
    if not do_mes:
        return [MSG_SEM_DADOS]

    linhas = linhas_orcamento(orcamentos)
    sugestoes: list[str] = []

    for l in sorted((l for l in linhas if l["estado"] == "estourado"), key=lambda l: l["restante"]):
        sugestoes.append(f"Você ultrapassou o limite de {l['categoria']} em "
                         f"{moeda(-l['restante'])} este mês.")

    for l in (l for l in linhas if l["estado"] == "atencao"):
        sugestoes.append(f"{l['categoria']} já usou {percentual(l['percentual'])} do limite. "
                         f"Restam {moeda(l['restante'])}.")

    pendentes = totais(filtrar(do_mes, tipo="despesa", status="pendente"))["despesas"]
    if pendentes > 0:
        sugestoes.append(f"Você tem {moeda(pendentes)} em despesas pendentes este mês.")

    t = totais(do_mes)
    if t["saldo"] > 0:
        sugestoes.append(f"Você poupou {percentual(taxa_poupanca(t['receitas'], t['despesas']))} "
                         "das suas receitas este mês.")
    elif t["saldo"] < 0:
        sugestoes.append(f"Suas despesas superaram as receitas em {moeda(-t['saldo'])} este mês.")

    return sugestoes[:MAX_SUGESTOES]
