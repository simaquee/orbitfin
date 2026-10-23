import pytest

from core.calculos import (
    estado_orcamento, filtrar, gastos_por_categoria, indicadores_metas, indicadores_orcamento,
    limites_mes, linhas_metas, linhas_orcamento, meses_ate, por_categoria, resumo_ano,
    resumo_mes, saldo_atual, serie_diaria, serie_mensal, status_meta, taxa_poupanca, totais,
    totais_mes,
)


def tx(tipo, valor, data, categoria="Outros", status="pago", id=None):
    return {"id": id, "tipo": tipo, "valor": valor, "data": data, "categoria": categoria,
            "status": status, "descricao": ""}


# --- períodos ------------------------------------------------------------
def test_limites_mes():
    assert limites_mes(2026, 10) == ("2026-10-01", "2026-10-31")
    assert limites_mes(2028, 2) == ("2028-02-01", "2028-02-29")


def test_meses_ate_vira_o_ano():
    assert meses_ate(2026, 2, 3) == [(2025, 12), (2026, 1), (2026, 2)]


# --- spec transacoes -----------------------------------------------------
def test_filtro_por_mes_e_tipo():
    txs = [tx("despesa", 10, "2026-10-02"), tx("receita", 20, "2026-10-03"),
           tx("despesa", 30, "2026-09-30")]
    assert filtrar(txs, (2026, 10), tipo="despesa") == [txs[0]]


def test_totais_do_filtro():
    txs = [tx("receita", 3000, "2026-10-05")] + [tx("despesa", 312.5, "2026-10-06")] * 4
    t = totais(txs)
    assert (t["receitas"], t["n_receitas"]) == (3000, 1)
    assert (t["despesas"], t["n_despesas"]) == (1250, 4)
    assert t["saldo"] == 1750


# --- spec dashboard ------------------------------------------------------
def test_saldo_considera_apenas_pagos():
    txs = [tx("receita", 5000, "2026-09-01"), tx("despesa", 3200, "2026-09-10"),
           tx("despesa", 400, "2026-10-10", status="pendente")]
    assert saldo_atual(txs) == 1800


def test_pendentes_no_mes():
    txs = [tx("despesa", 3200, "2026-10-01"), tx("despesa", 400, "2026-10-15", status="pendente")]
    t = totais_mes(txs, 2026, 10)
    assert t["despesas"] == 3600 and t["despesas_pendentes"] == 400


def test_resultado_negativo():
    txs = [tx("receita", 2000, "2026-10-01"), tx("despesa", 2300, "2026-10-02")]
    assert totais_mes(txs, 2026, 10)["resultado"] == -300


def test_meses_sem_lancamentos():
    txs = [tx("receita", 100, "2026-09-01"), tx("despesa", 50, "2026-10-01")]
    serie = serie_mensal(txs, 2026, 10, 6)
    assert [(p["ano"], p["mes"]) for p in serie] == [(2026, m) for m in range(5, 11)]
    assert [p["receitas"] for p in serie] == [0, 0, 0, 0, 100, 0]
    assert [p["despesas"] for p in serie] == [0, 0, 0, 0, 0, 50]


def test_distribuicao_por_categoria():
    txs = [tx("despesa", 1200, "2026-10-01", "Moradia"), tx("despesa", 600, "2026-10-02", "Alimentação"),
           tx("despesa", 200, "2026-10-03", "Lazer"), tx("receita", 999, "2026-10-03", "Salário")]
    assert gastos_por_categoria(txs, 2026, 10) == [("Moradia", 1200), ("Alimentação", 600),
                                                   ("Lazer", 200)]


# --- spec orcamentos -----------------------------------------------------
def test_estados_de_orcamento():
    assert estado_orcamento(270, 300) == "atencao"      # 90%
    assert estado_orcamento(450, 400) == "estourado"
    assert estado_orcamento(560, 800) == "ok"           # 70%
    assert estado_orcamento(255, 300) == "atencao"      # exatamente 85%


def test_linhas_ordenadas_por_percentual():
    orcs = [{"id": 1, "categoria": "Lazer", "limite": 300, "gasto": 270},
            {"id": 2, "categoria": "Transporte", "limite": 400, "gasto": 450},
            {"id": 3, "categoria": "Saúde", "limite": 200, "gasto": 0}]
    linhas = linhas_orcamento(orcs)
    assert [l["categoria"] for l in linhas] == ["Transporte", "Lazer", "Saúde"]
    assert linhas[0]["restante"] == -50 and linhas[1]["restante"] == 30


def test_indicadores_orcamento():
    orcs = [{"categoria": "Moradia", "limite": 1200, "gasto": 1200},
            {"categoria": "Transporte", "limite": 400, "gasto": 450},
            {"categoria": "Alimentação", "limite": 800, "gasto": 125},
            {"categoria": "Outros", "limite": 1150, "gasto": 0}]
    ind = indicadores_orcamento(orcs)
    assert ind["limite_total"] == 3550 and ind["gasto_total"] == 1775
    assert ind["percentual"] == 50 and ind["disponivel"] == 1775 and ind["estouradas"] == 1


# --- spec metas ----------------------------------------------------------
def test_status_meta():
    assert status_meta(185, 200) == "risco"
    assert status_meta(450, 400) == "teto"
    assert status_meta(400, 400) == "teto"
    assert status_meta(30, 150) == "ok"
    assert status_meta(0, 0) == "sem"


def test_folga_e_ordem_das_metas():
    orcs = [{"categoria": "Educação", "limite": 150, "gasto": 30},
            {"categoria": "Transporte", "limite": 400, "gasto": 450},
            {"categoria": "Saúde", "limite": 200, "gasto": 185},
            {"categoria": "Lazer", "limite": 300, "gasto": 0}]
    linhas = linhas_metas(orcs)
    assert [l["categoria"] for l in linhas] == ["Saúde", "Transporte", "Educação", "Lazer"]
    educacao = linhas[2]
    assert educacao["folga"] == pytest.approx(80) and educacao["restante"] == 120


def test_poupanca_do_mes_e_mes_sem_receitas():
    assert taxa_poupanca(5000, 3500) == pytest.approx(30)
    assert taxa_poupanca(0, 100) == 0
    ind = indicadores_metas([{"categoria": "Saúde", "limite": 200, "gasto": 185}], 5000, 3500)
    assert ind["poupanca"] == pytest.approx(30) and ind["saldo_mes"] == 1500
    assert ind["economia_preservada"] == 15 and ind["atencao"] == 1


# --- spec relatorios -----------------------------------------------------
def test_resumo_mes():
    txs = [tx("receita", 4000, "2026-09-05"), tx("despesa", 3000, "2026-09-20")]
    assert resumo_mes(txs, 2026, 9) == {"receitas": 4000, "despesas": 3000, "saldo": 1000,
                                        "poupanca": 25}


def test_poupanca_negativa():
    txs = [tx("receita", 2000, "2026-09-05"), tx("despesa", 2500, "2026-09-20")]
    assert resumo_mes(txs, 2026, 9)["poupanca"] == -25


def test_visao_mensal_fevereiro_bissexto():
    serie = serie_diaria([tx("receita", 10, "2028-02-29")], 2028, 2)
    assert len(serie) == 29 and serie[-1]["receitas"] == 10


def test_rosca_de_receitas():
    txs = [tx("receita", 4500, "2026-10-05", "Salário"), tx("receita", 500, "2026-10-09", "Freelance")]
    assert por_categoria(txs, "receita", 2026, 10) == [("Salário", 4500), ("Freelance", 500)]


def test_totais_anuais():
    txs = [tx("receita", 4000, f"2026-{m:02d}-05") for m in range(1, 13)]
    txs += [tx("despesa", 3250, f"2026-{m:02d}-10") for m in range(1, 13)]
    ano = resumo_ano(txs, 2026)
    assert len(ano) == 12
    assert sum(m["receitas"] for m in ano) == 48000
    assert sum(m["despesas"] for m in ano) == 39000
    assert sum(m["saldo"] for m in ano) == 9000
