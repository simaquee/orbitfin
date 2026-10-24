"""Categorias padronizadas (espelhadas na validação do backend xano/).

Spec (OpenSpec): openspec/specs/transacoes/spec.md
"""

CATEGORIAS = {
    "despesa": ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Outros"],
    "receita": ["Salário", "Freelance", "Investimentos", "Outros"],
}

TIPOS = {"despesa": "Despesa", "receita": "Receita"}
STATUS = {"pago": "Pago", "pendente": "Pendente"}


def categoria_valida(tipo: str, categoria: str) -> bool:
    return categoria in CATEGORIAS.get(tipo, [])
