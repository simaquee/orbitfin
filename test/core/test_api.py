import pytest
import requests

from core.api import Cliente, ErroConexao, ErroValidacao, SessaoExpirada
from helpers.fakes import HttpFalso, RespostaFalsa

BASE = "https://x.xano.io/api:orbitfin"


def test_sucesso_envia_bearer_e_timeout():
    http = HttpFalso(RespostaFalsa(200, [{"id": 1}]))
    resultado = Cliente(BASE, token="abc", http=http).requisitar("GET", "/transacoes")

    assert resultado == [{"id": 1}]
    chamada = http.chamadas[0]
    assert chamada["url"] == f"{BASE}/transacoes"
    assert chamada["headers"]["Authorization"] == "Bearer abc"
    assert chamada["timeout"] == 30


def test_sem_token_nao_envia_authorization():
    http = HttpFalso(RespostaFalsa(200, {}))
    Cliente(BASE, http=http).requisitar("POST", "/login", json={})
    assert "Authorization" not in http.chamadas[0]["headers"]


def test_resposta_vazia_vira_dict():
    http = HttpFalso(RespostaFalsa(204))
    assert Cliente(BASE, token="t", http=http).requisitar("DELETE", "/x") == {}


def test_erro_400_exibe_mensagem_do_backend():
    http = HttpFalso(RespostaFalsa(400, {"code": "ERROR_CODE_INPUT_ERROR",
                                         "message": "O valor deve ser maior que zero."}))
    with pytest.raises(ErroValidacao, match="O valor deve ser maior que zero."):
        Cliente(BASE, token="t", http=http).requisitar("POST", "/transacoes", json={})


def test_erro_sem_mensagem_usa_texto_generico():
    http = HttpFalso(RespostaFalsa(500))
    with pytest.raises(ErroValidacao, match=r"código 500"):
        Cliente(BASE, token="t", http=http).requisitar("GET", "/transacoes")


def test_401_vira_sessao_expirada():
    http = HttpFalso(RespostaFalsa(401, {"message": "Invalid token"}))
    with pytest.raises(SessaoExpirada, match="Sua sessão expirou. Entre novamente."):
        Cliente(BASE, token="velho", http=http).requisitar("GET", "/transacoes")


@pytest.mark.parametrize("excecao", [requests.Timeout(), requests.ConnectionError()])
def test_timeout_e_falha_de_conexao(excecao):
    http = HttpFalso(excecao)
    with pytest.raises(ErroConexao, match="Não foi possível conectar ao servidor."):
        Cliente(BASE, http=http).requisitar("GET", "/transacoes")


# --- spec autenticacao ---------------------------------------------------
def test_cadastrar_envia_contrato():
    resposta = {"access_token": "tok", "user_id": 1, "name": "Ana Souza", "email": "ana@email.com"}
    http = HttpFalso(RespostaFalsa(200, resposta))
    assert Cliente(BASE, http=http).cadastrar("Ana Souza", "ana@email.com", "orbita2026") == resposta
    assert http.chamadas[0]["json"] == {"name": "Ana Souza", "email": "ana@email.com",
                                        "password": "orbita2026"}


def test_email_duplicado():
    http = HttpFalso(RespostaFalsa(400, {"message": "Já existe uma conta com este e-mail."}))
    with pytest.raises(ErroValidacao, match="Já existe uma conta com este e-mail."):
        Cliente(BASE, http=http).cadastrar("Ana", "ana@email.com", "orbita2026")


def test_credenciais_invalidas_nao_viram_sessao_expirada():
    http = HttpFalso(RespostaFalsa(403, {"message": "E-mail ou senha incorretos."}))
    with pytest.raises(ErroValidacao, match="E-mail ou senha incorretos."):
        Cliente(BASE, http=http).entrar("ana@email.com", "errada")


def test_login_servidor_indisponivel():
    http = HttpFalso(requests.ConnectionError())
    with pytest.raises(ErroConexao):
        Cliente(BASE, http=http).entrar("ana@email.com", "orbita2026")


# --- spec transacoes / orcamentos ----------------------------------------
def test_crud_transacoes_usa_rotas_do_contrato():
    http = HttpFalso(RespostaFalsa(200, [{"id": 7}]), RespostaFalsa(200, {"id": 8}),
                     RespostaFalsa(200, {"id": 7}), RespostaFalsa(200, {"success": True}))
    c = Cliente(BASE, token="t", http=http)
    assert c.listar_transacoes() == [{"id": 7}]
    c.criar_transacao({"tipo": "despesa"})
    c.editar_transacao(7, {"status": "pago"})
    c.excluir_transacao(7)
    assert [(ch["metodo"], ch["url"].removeprefix(BASE)) for ch in http.chamadas] == [
        ("GET", "/transacoes"), ("POST", "/transacoes"), ("PUT", "/transacoes/7"),
        ("DELETE", "/transacoes/7")]


def test_orcamentos_enviam_periodo_e_aceitam_items():
    http = HttpFalso(RespostaFalsa(200, {"items": [{"id": 1}]}), RespostaFalsa(200, {"id": 1}))
    c = Cliente(BASE, token="t", http=http)
    assert c.listar_orcamentos("2026-10-01", "2026-10-31") == [{"id": 1}]
    assert http.chamadas[0]["params"] == {"inicio": "2026-10-01", "fim": "2026-10-31"}
    c.alterar_limite(1, 450)
    assert http.chamadas[1]["json"] == {"limite": 450}


def test_spinner_recebe_texto():
    textos = []

    class Spinner:
        def __init__(self, texto):
            textos.append(texto)

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    http = HttpFalso(RespostaFalsa(200, {}))
    Cliente(BASE, http=http, spinner=Spinner).requisitar("GET", "/x", texto="Salvando...")
    assert textos == ["Salvando..."]
