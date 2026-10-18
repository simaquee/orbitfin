"""Respostas HTTP simuladas para testar services.api sem rede."""
from __future__ import annotations

import json as jsonlib


class RespostaFalsa:
    def __init__(self, status_code: int, corpo=None):
        self.status_code = status_code
        self.content = b"" if corpo is None else jsonlib.dumps(corpo).encode()
        self._corpo = corpo

    def json(self):
        if self._corpo is None:
            raise ValueError("sem corpo")
        return self._corpo


class HttpFalso:
    """Substitui o módulo requests; guarda as chamadas e devolve respostas em fila."""

    def __init__(self, *respostas):
        self.respostas = list(respostas)
        self.chamadas = []

    def request(self, metodo, url, **kwargs):
        self.chamadas.append({"metodo": metodo, "url": url, **kwargs})
        resp = self.respostas.pop(0)
        if isinstance(resp, Exception):
            raise resp
        return resp
