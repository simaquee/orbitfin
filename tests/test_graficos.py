from components import graficos


def test_eixo_sem_dados_usa_intervalo_fixo():
    fig = graficos.receitas_despesas(["mai", "jun"], [0, 0], [0, 0])
    assert tuple(fig.layout.yaxis.range) == (0, 100)


def test_eixo_com_dados_fica_automatico():
    fig = graficos.receitas_despesas(["mai", "jun"], [1500, 0], [320.5, 80])
    assert fig.layout.yaxis.range is None
