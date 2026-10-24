"""Formatação pt-BR independente da localidade do servidor.

Spec (OpenSpec): openspec/specs/interface-base/spec.md
"""
from __future__ import annotations

from datetime import date

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]
MESES_ABREV = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def moeda(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50'; -80 -> '-R$ 80,00'."""
    sinal = "-" if round(valor, 2) < 0 else ""
    inteiro, centavos = f"{abs(valor):,.2f}".split(".")
    return f"{sinal}R$ {inteiro.replace(',', '.')},{centavos}"


def data_br(valor: date | str) -> str:
    """date(2026, 10, 5) ou '2026-10-05' -> '05/10/2026'."""
    d = parse_data(valor)
    return d.strftime("%d/%m/%Y")


def mes_abrev(ano: int, mes: int) -> str:
    """(2026, 10) -> 'out/2026'."""
    return f"{MESES_ABREV[mes - 1]}/{ano}"


def percentual(valor: float) -> str:
    """29.6 -> '30%'."""
    return f"{valor:.0f}%"


def parse_data(valor: date | str) -> date:
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor)[:10])
