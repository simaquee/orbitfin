from datetime import date

from core.sugestoes import MSG_SEM_DADOS, gerar_sugestoes

HOJE = date(2026, 10, 18)


def tx(tipo, valor, categoria="Outros", status="pago", data="2026-10-10"):
    return {"tipo": tipo, "valor": valor, "data": data, "categoria": categoria, "status": status}


def test_limite_estourado():
    s = gerar_sugestoes([tx("despesa", 450, "Transporte")],
                        [{"categoria": "Transporte", "limite": 400, "gasto": 450}], HOJE)
    assert s[0] == "Você ultrapassou o limite de Transporte em R$ 50,00 este mês."


def test_perto_do_limite():
    s = gerar_sugestoes([tx("despesa", 270, "Lazer")],
                        [{"categoria": "Lazer", "limite": 300, "gasto": 270}], HOJE)
    assert s[0] == "Lazer já usou 90% do limite. Restam R$ 30,00."


def test_pendentes():
    txs = [tx("despesa", 150, status="pendente"), tx("despesa", 250, status="pendente")]
    assert "Você tem R$ 400,00 em despesas pendentes este mês." in gerar_sugestoes(txs, [], HOJE)


def test_mes_positivo():
    txs = [tx("receita", 5000, "Salário"), tx("despesa", 3500, "Moradia")]
    assert gerar_sugestoes(txs, [], HOJE) == ["Você poupou 30% das suas receitas este mês."]


def test_mes_negativo():
    txs = [tx("receita", 2000, "Salário"), tx("despesa", 2300, "Moradia")]
    assert gerar_sugestoes(txs, [], HOJE) == [
        "Suas despesas superaram as receitas em R$ 300,00 este mês."]


def test_limite_de_3_sugestoes_em_ordem_de_prioridade():
    txs = [tx("despesa", 450, "Transporte"), tx("despesa", 210, "Saúde"),
           tx("despesa", 270, "Lazer"), tx("despesa", 100, "Outros", status="pendente"),
           tx("receita", 5000, "Salário")]
    orcs = [{"categoria": "Transporte", "limite": 400, "gasto": 450},
            {"categoria": "Saúde", "limite": 200, "gasto": 210},
            {"categoria": "Lazer", "limite": 300, "gasto": 270}]
    s = gerar_sugestoes(txs, orcs, HOJE)
    assert len(s) == 3
    assert s[0].startswith("Você ultrapassou o limite de Transporte")
    assert s[1].startswith("Você ultrapassou o limite de Saúde")
    assert s[2].startswith("Lazer já usou")


def test_mes_vazio():
    assert gerar_sugestoes([tx("despesa", 10, data="2026-09-01")], [], HOJE) == [MSG_SEM_DADOS]
    assert MSG_SEM_DADOS == "Registre suas transações do mês para receber sugestões."
