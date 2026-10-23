from datetime import date

from utils.formatacao import data_br, mes_abrev, moeda, percentual


def test_valor_positivo():
    assert moeda(1234.5) == "R$ 1.234,50"


def test_valor_negativo():
    assert moeda(-80) == "-R$ 80,00"


def test_valores_grandes_e_zero():
    assert moeda(1234567.891) == "R$ 1.234.567,89"
    assert moeda(0) == "R$ 0,00"
    assert moeda(-0.001) == "R$ 0,00"


def test_mes_abreviado():
    assert mes_abrev(2026, 10) == "out/2026"


def test_data_br():
    assert data_br("2026-10-05") == "05/10/2026"
    assert data_br(date(2026, 1, 9)) == "09/01/2026"


def test_percentual():
    assert percentual(29.6) == "30%"
