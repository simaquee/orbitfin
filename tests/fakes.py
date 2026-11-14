"""Respostas HTTP simuladas para testar services.api sem rede e PDFs mínimos para services.extrato."""
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


def pdf_com_linhas(linhas: list[str]) -> bytes:
    """PDF de uma página com uma linha de texto por item (fonte Helvetica, WinAnsi)."""
    def escapar(t: str) -> str:
        return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    corpo = "BT /F1 10 Tf 40 800 Td 14 TL\n"
    corpo += "".join(f"({escapar(l)}) Tj T*\n" for l in linhas) + "ET"
    stream = corpo.encode("latin-1")
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    saida = bytearray(b"%PDF-1.4\n")
    posicoes = []
    for i, obj in enumerate(objetos, start=1):
        posicoes.append(len(saida))
        saida += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    saida += b"".join(f"{p:010d} 00000 n \n".encode() for p in posicoes)
    saida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(saida)
