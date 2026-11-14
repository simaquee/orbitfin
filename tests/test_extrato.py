"""Spec transacoes: importação de extrato (leitura local de CSV, OFX e PDF)."""
import re
from datetime import date

import pytest

from services.extrato import (
    MSG_CSV_COLUNAS, MSG_FORMATO, MSG_LIMITE, MSG_PDF_IMAGEM, MSG_PDF_INVALIDO, MSG_VALOR_ZERO,
    MSG_VAZIO, ErroExtrato, ler_extrato, montar_lote, parse_data_extrato, parse_valor, pendentes,
    pode_importar, validar_linha,
)
from tests.fakes import pdf_com_linhas


@pytest.mark.parametrize("texto, esperado", [
    ("1.234,56", 1234.56), ("-45,90", -45.9), ("45,90-", -45.9), ("(45,90)", -45.9),
    ("45,90 D", -45.9), ("45,90 C", 45.9), ("R$ 3.000,00", 3000.0), ("-45.90", -45.9),
    ("1,234.56", 1234.56), ("1.200", 1200.0), ("12", 12.0), ("", None), ("abc", None),
])
def test_parse_valor(texto, esperado):
    assert parse_valor(texto) == esperado


@pytest.mark.parametrize("texto, esperado", [
    ("05/11/2026", date(2026, 11, 5)), ("05/11/26", date(2026, 11, 5)),
    ("2026-11-05", date(2026, 11, 5)), ("20261105120000[-3:BRT]", date(2026, 11, 5)),
    ("31/02/2026", None), ("ontem", None),
])
def test_parse_data_extrato(texto, esperado):
    assert parse_data_extrato(texto) == esperado


def test_data_sem_ano_usa_ano_padrao():
    assert parse_data_extrato("07/11", 2025) == date(2025, 11, 7)


# --- CSV --------------------------------------------------------------------
def test_csv_cenario_da_spec():
    csv = "Data;Descrição;Valor\n05/11/2026;Mercado Bom Preço;-45,90\n06/11/2026;Salário Empresa X;3.000,00\n"
    assert ler_extrato("extrato.csv", csv.encode("utf-8")) == [
        {"data": "2026-11-05", "descricao": "Mercado Bom Preço", "valor": -45.9},
        {"data": "2026-11-06", "descricao": "Salário Empresa X", "valor": 3000.0},
    ]


def test_csv_latin1_com_titulo_e_colunas_credito_debito():
    csv = ("Banco Exemplo - Extrato de conta\n"
           "Data;Histórico;Crédito;Débito\n"
           "01/11/2026;SALDO ANTERIOR;;\n"
           "03/11/2026;CONTA DE LUZ;;120,50\n"
           "04/11/2026;TED RECEBIDA;1.000,00;\n")
    linhas = ler_extrato("extrato.CSV", csv.encode("latin-1"))
    assert [(l["descricao"], l["valor"]) for l in linhas] == [("CONTA DE LUZ", -120.5),
                                                              ("TED RECEBIDA", 1000.0)]


def test_csv_em_ingles_com_virgula():
    csv = 'date,description,amount\n2026-11-05,"Coffee, Shop",-4.50\n2026-11-06,Refund,10.00\n'
    assert [(l["data"], l["descricao"], l["valor"]) for l in ler_extrato("x.csv", csv.encode())] == [
        ("2026-11-05", "Coffee, Shop", -4.5), ("2026-11-06", "Refund", 10.0)]


def test_csv_sem_colunas_reconhecidas():
    with pytest.raises(ErroExtrato, match=MSG_CSV_COLUNAS):
        ler_extrato("x.csv", b"a;b;c\n1;2;3\n")


def test_csv_so_com_cabecalho():
    with pytest.raises(ErroExtrato, match=MSG_VAZIO):
        ler_extrato("x.csv", b"Data;Descricao;Valor\n")


# --- OFX --------------------------------------------------------------------
OFX = """OFXHEADER:100
<OFX><BANKMSGSRSV1><STMTTRNRS><STMTRS><BANKTRANLIST>
<STMTTRN>
<TRNTYPE>DEBIT
<DTPOSTED>20261103120000[-3:BRT]
<TRNAMT>-120.50
<MEMO>CONTA DE LUZ
<STMTTRN>
<TRNTYPE>CREDIT
<DTPOSTED>20261104
<TRNAMT>1000.00
<NAME>TED RECEBIDA
</BANKTRANLIST></STMTRS></STMTTRNRS></BANKMSGSRSV1></OFX>
"""


def test_ofx_cenario_da_spec_sem_tags_de_fechamento():
    assert ler_extrato("extrato.ofx", OFX.encode()) == [
        {"data": "2026-11-03", "descricao": "CONTA DE LUZ", "valor": -120.5},
        {"data": "2026-11-04", "descricao": "TED RECEBIDA", "valor": 1000.0},
    ]


def test_ofx_com_tags_fechadas():
    ofx = ("<OFX><STMTTRN><DTPOSTED>20261105</DTPOSTED><TRNAMT>-9,90</TRNAMT>"
           "<MEMO>Streaming</MEMO></STMTTRN></OFX>")
    assert ler_extrato("a.ofx", ofx.encode()) == [
        {"data": "2026-11-05", "descricao": "Streaming", "valor": -9.9}]


# --- PDF --------------------------------------------------------------------
def test_pdf_cenario_da_spec_ignora_saldo():
    pdf = pdf_com_linhas([
        "Extrato de conta corrente - periodo 01/11/2026 a 30/11/2026",
        "Data Historico Valor Saldo",
        "01/11/2026 SALDO ANTERIOR 1.350,00",
        "07/11/2026 PIX ENVIADO JOAO 150,00- 1.200,00",
        "08/11/2026 SALARIO EMPRESA X 3.000,00 4.200,00",
        "Total de lancamentos: 2",
    ])
    assert ler_extrato("extrato.pdf", pdf) == [
        {"data": "2026-11-07", "descricao": "PIX ENVIADO JOAO", "valor": -150.0},
        {"data": "2026-11-08", "descricao": "SALARIO EMPRESA X", "valor": 3000.0},
    ]


def test_pdf_em_tabela_um_campo_por_linha():
    # Layout de contas digitais (ex.: Mercado Pago): data, hora, descrição, valor e saldo em linhas
    # separadas, valores como "-R$ 166,12" e cabeçalho de página entre os lançamentos.
    pdf = pdf_com_linhas([
        "Extrato de movimentações", "Período", "01/10/2026 a 31/10/2026",
        "Saldo inicial", "R$ 8.350,45",
        "Data / hora", "Descrição", "Movimentação", "Saldo",
        "01/10/2026", "10:53", "Pagamento de boleto - internet", "-R$ 166,12", "R$ 8.184,33",
        "01/10/2026", "10:54", "Crédito de venda - marketplace", "R$ 515,49", "R$ 8.699,82",
        "Página 2", "Data / hora", "Descrição", "Movimentação", "Saldo",
        "02/10/2026 08:30", "Venda recebida", "- link de pagamento", "R$ 119,61", "R$ 8.819,43",
    ])
    assert ler_extrato("mercado_pago.pdf", pdf) == [
        {"data": "2026-10-01", "descricao": "Pagamento de boleto - internet", "valor": -166.12},
        {"data": "2026-10-01", "descricao": "Crédito de venda - marketplace", "valor": 515.49},
        {"data": "2026-10-02", "descricao": "Venda recebida - link de pagamento", "valor": 119.61},
    ]


def test_pdf_data_sem_ano_usa_ano_do_documento():
    pdf = pdf_com_linhas(["Periodo: 01/11/2025 a 30/11/2025", "05/11 MERCADO -45,90"])
    assert ler_extrato("e.pdf", pdf) == [{"data": "2025-11-05", "descricao": "MERCADO", "valor": -45.9}]


def test_pdf_sem_texto():
    with pytest.raises(ErroExtrato, match=re.escape(MSG_PDF_IMAGEM)):
        ler_extrato("scan.pdf", pdf_com_linhas([]))


def test_pdf_invalido():
    with pytest.raises(ErroExtrato, match=MSG_PDF_INVALIDO):
        ler_extrato("quebrado.pdf", b"isto nao e um pdf")


# --- regras gerais ----------------------------------------------------------
def test_formato_nao_suportado():
    with pytest.raises(ErroExtrato, match=MSG_FORMATO):
        ler_extrato("extrato.xlsx", b"PK")


def test_limite_de_linhas():
    corpo = "Data;Descricao;Valor\n" + "05/11/2026;X;-1,00\n" * 501
    with pytest.raises(ErroExtrato, match=MSG_LIMITE):
        ler_extrato("x.csv", corpo.encode())


def test_montar_lote_segue_contrato_do_post():
    linhas = [{"data": "2026-11-05", "descricao": " Mercado ", "valor": -45.9, "confirmado": True},
              {"data": "2026-11-06", "descricao": "Salário", "valor": 3000, "confirmado": True}]
    assert montar_lote(linhas) == [
        {"tipo": "despesa", "valor": 45.9, "data": "2026-11-05", "categoria": "Outros",
         "descricao": "Mercado", "status": "pago"},
        {"tipo": "receita", "valor": 3000.0, "data": "2026-11-06", "categoria": "Outros",
         "descricao": "Salário", "status": "pago"},
    ]


def test_card_pendente_bloqueia_importacao():
    linhas = [{"confirmado": True}] * 11 + [{"confirmado": False}]
    assert pendentes(linhas) == 1
    assert not pode_importar(linhas)
    assert pode_importar([{"confirmado": True}] * 12)
    assert not pode_importar([])


@pytest.mark.parametrize("valor, erro", [(0, MSG_VALOR_ZERO), (0.001, MSG_VALOR_ZERO),
                                         (None, MSG_VALOR_ZERO), (-45.9, None), (10, None)])
def test_validar_linha(valor, erro):
    assert validar_linha(valor) == erro
