"""Cliente HTTP do Xano: único ponto de I/O do OrbitFin.

Spec (OpenSpec): openspec/specs/autenticacao/spec.md, openspec/specs/transacoes/spec.md, openspec/specs/orcamentos/spec.md
"""
from __future__ import annotations

import contextlib
from typing import Any, Callable, ContextManager

import requests

TIMEOUT_SEGUNDOS = 30
MSG_CONEXAO = "Não foi possível conectar ao servidor. Tente novamente."
MSG_SESSAO = "Sua sessão expirou. Entre novamente."
MSG_CONFIG = "Configure a URL do Xano em .streamlit/secrets.toml (veja secrets.toml.example)."


class ErroApi(Exception):
    """Base dos erros exibíveis ao usuário."""


class ErroConexao(ErroApi):
    def __init__(self) -> None:
        super().__init__(MSG_CONEXAO)


class ErroValidacao(ErroApi):
    """O backend recusou a operação; a mensagem vem do próprio backend."""


class SessaoExpirada(Exception):
    """Não herda de ErroApi: as telas não a capturam; o app.py encerra a sessão."""

    def __init__(self) -> None:
        super().__init__(MSG_SESSAO)


class Cliente:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        spinner: Callable[[str], ContextManager] | None = None,
        http: Any = requests,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._spinner = spinner or (lambda _texto: contextlib.nullcontext())
        self._http = http

    def requisitar(self, metodo: str, caminho: str, *, json: dict | None = None,
                   params: dict | None = None, texto: str = "Carregando...") -> Any:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            with self._spinner(texto):
                resp = self._http.request(
                    metodo, f"{self.base_url}{caminho}", json=json, params=params,
                    headers=headers, timeout=TIMEOUT_SEGUNDOS,
                )
        except (requests.Timeout, requests.ConnectionError):
            raise ErroConexao() from None

        if resp.status_code == 401:
            raise SessaoExpirada()
        if not 200 <= resp.status_code < 300:
            raise ErroValidacao(_mensagem_erro(resp))
        if not resp.content:
            return {}
        return resp.json()

    # --- Autenticação ---------------------------------------------------
    def cadastrar(self, nome: str, email: str, senha: str) -> dict:
        return self.requisitar("POST", "/register", texto="Criando conta...",
                               json={"name": nome, "email": email, "password": senha})

    def entrar(self, email: str, senha: str) -> dict:
        return self.requisitar("POST", "/login", texto="Entrando...",
                               json={"email": email, "password": senha})

    # --- Transações -----------------------------------------------------
    def listar_transacoes(self) -> list[dict]:
        return _como_lista(self.requisitar("GET", "/transacoes"))

    def criar_transacao(self, dados: dict) -> dict:
        return self.requisitar("POST", "/transacoes", json=dados, texto="Salvando...")

    def editar_transacao(self, transacao_id: int, dados: dict) -> dict:
        return self.requisitar("PUT", f"/transacoes/{transacao_id}", json=dados,
                               texto="Atualizando...")

    def excluir_transacao(self, transacao_id: int) -> None:
        self.requisitar("DELETE", f"/transacoes/{transacao_id}", texto="Excluindo...")

    # --- Orçamentos -----------------------------------------------------
    def listar_orcamentos(self, inicio: str, fim: str) -> list[dict]:
        return _como_lista(self.requisitar("GET", "/budgets",
                                           params={"inicio": inicio, "fim": fim}))

    def alterar_limite(self, orcamento_id: int, limite: float) -> dict:
        return self.requisitar("PUT", f"/budgets/{orcamento_id}", json={"limite": limite},
                               texto="Atualizando...")


def _como_lista(resposta: Any) -> list[dict]:
    if isinstance(resposta, dict):
        return list(resposta.get("items", []))
    return list(resposta or [])


def _mensagem_erro(resp: Any) -> str:
    try:
        corpo = resp.json()
    except ValueError:
        corpo = None
    if isinstance(corpo, dict) and corpo.get("message"):
        return str(corpo["message"])
    return f"Erro inesperado no servidor (código {resp.status_code})."


# --- Integração com o Streamlit ------------------------------------------
def base_url_configurada() -> str | None:
    import streamlit as st

    try:
        url = st.secrets["xano"]["base_url"]
    except (KeyError, FileNotFoundError):
        return None
    if not url or "<instancia>" in url:
        return None
    return url


def cliente() -> Cliente:
    """Cliente com a URL dos secrets e o token da sessão atual."""
    import streamlit as st

    return Cliente(base_url_configurada() or "", token=st.session_state.get("token"),
                   spinner=st.spinner)
