"""Validações de formulário (as mesmas regras são aplicadas no backend).

Spec (OpenSpec): openspec/specs/autenticacao/spec.md, openspec/specs/transacoes/spec.md, openspec/specs/orcamentos/spec.md
"""
from __future__ import annotations

from services.categorias import STATUS, TIPOS, categoria_valida

MSG_CAMPOS = "Preencha todos os campos."
MSG_SENHAS = "As senhas não coincidem."
MSG_SENHA_FRACA = "A senha deve ter no mínimo 8 caracteres, com pelo menos 1 letra e 1 número."
MSG_LOGIN_VAZIO = "Preencha e-mail e senha."
MSG_VALOR = "O valor deve ser maior que zero."
MSG_CATEGORIA = "Categoria inválida para o tipo informado."
MSG_LIMITE = "O limite deve ser maior que zero."


def senha_valida(senha: str) -> bool:
    return (len(senha) >= 8 and any(c.isalpha() for c in senha)
            and any(c.isdigit() for c in senha))


def validar_cadastro(nome: str, email: str, senha: str, confirmacao: str) -> str | None:
    if not (nome.strip() and email.strip() and senha and confirmacao):
        return MSG_CAMPOS
    if senha != confirmacao:
        return MSG_SENHAS
    if not senha_valida(senha):
        return MSG_SENHA_FRACA
    return None


def validar_login(email: str, senha: str) -> str | None:
    return MSG_LOGIN_VAZIO if not (email.strip() and senha) else None


def validar_transacao(tipo: str, valor: float, categoria: str, status: str) -> str | None:
    if valor is None or valor <= 0:
        return MSG_VALOR
    if tipo not in TIPOS or status not in STATUS or not categoria_valida(tipo, categoria):
        return MSG_CATEGORIA
    return None


def validar_limite(limite: float) -> str | None:
    return MSG_LIMITE if limite is None or limite <= 0 else None
