from services.categorias import CATEGORIAS
from services.validacao import (
    MSG_CAMPOS, MSG_CATEGORIA, MSG_LIMITE, MSG_LOGIN_VAZIO, MSG_SENHA_FRACA, MSG_SENHAS,
    MSG_VALOR, senha_valida, validar_cadastro, validar_limite, validar_login, validar_transacao,
)


# --- spec autenticacao ---------------------------------------------------
def test_cadastro_valido():
    assert validar_cadastro("Ana Souza", "ana@email.com", "orbita2026", "orbita2026") is None


def test_campos_vazios():
    assert validar_cadastro("", "ana@email.com", "orbita2026", "orbita2026") == MSG_CAMPOS
    assert MSG_CAMPOS == "Preencha todos os campos."


def test_senhas_diferentes():
    assert validar_cadastro("Ana", "a@b.com", "orbita2026", "orbita2027") == MSG_SENHAS
    assert MSG_SENHAS == "As senhas não coincidem."


def test_senha_fraca():
    assert validar_cadastro("Ana", "a@b.com", "abcdefgh", "abcdefgh") == MSG_SENHA_FRACA
    assert MSG_SENHA_FRACA == ("A senha deve ter no mínimo 8 caracteres, "
                               "com pelo menos 1 letra e 1 número.")


def test_regra_de_senha():
    assert senha_valida("orbita2026")
    assert not senha_valida("abc123")      # curta
    assert not senha_valida("12345678")    # sem letra
    assert not senha_valida("abcdefgh")    # sem número


def test_login_campos_vazios():
    assert validar_login("", "x") == MSG_LOGIN_VAZIO == "Preencha e-mail e senha."
    assert validar_login("ana@email.com", "") == MSG_LOGIN_VAZIO
    assert validar_login("ana@email.com", "x") is None


# --- spec transacoes -----------------------------------------------------
def test_categorias_por_tipo():
    assert CATEGORIAS["despesa"] == ["Alimentação", "Moradia", "Transporte", "Lazer",
                                     "Saúde", "Educação", "Outros"]
    assert CATEGORIAS["receita"] == ["Salário", "Freelance", "Investimentos", "Outros"]


def test_valor_zero():
    assert validar_transacao("despesa", 0, "Alimentação", "pago") == MSG_VALOR
    assert MSG_VALOR == "O valor deve ser maior que zero."


def test_categoria_incompativel():
    assert validar_transacao("despesa", 10, "Salário", "pago") == MSG_CATEGORIA


def test_transacao_valida():
    assert validar_transacao("receita", 3000, "Salário", "pendente") is None


# --- spec orcamentos -----------------------------------------------------
def test_limite_invalido():
    assert validar_limite(0) == MSG_LIMITE == "O limite deve ser maior que zero."
    assert validar_limite(450) is None
