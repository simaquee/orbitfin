"""Teste de integração contra o Xano real, usando o mesmo cliente do app.

Uso: python scripts/teste_integracao.py <base_url>
Cria um usuário descartável, exercita transações e orçamentos e limpa o que criou.

Spec (OpenSpec): openspec/specs/autenticacao/spec.md, openspec/specs/transacoes/spec.md, openspec/specs/orcamentos/spec.md
"""
import secrets
import sys
from datetime import date

sys.path.insert(0, "src")
from services.api import Cliente, ErroValidacao  # noqa: E402

base = sys.argv[1]
email = f"teste-{secrets.token_hex(4)}@orbitfin.test"
senha = "Teste" + secrets.token_hex(4) + "9"


def etapa(nome, fn):
    try:
        r = fn()
        print(f"OK   {nome}")
        return r
    except Exception as e:  # noqa: BLE001
        print(f"FALHA {nome}: {type(e).__name__}: {e}")
        raise SystemExit(1)


def _espera_erro(fn):
    try:
        fn()
    except ErroValidacao as e:
        return str(e)
    raise AssertionError("esperava recusa do backend")


anon = Cliente(base)
cad = etapa("cadastro", lambda: anon.cadastrar("Teste Integração", email, senha))
etapa("cadastro duplicado é recusado", lambda: _espera_erro(lambda: anon.cadastrar("X", email, senha)))
login = etapa("login", lambda: anon.entrar(email, senha))
cli = Cliente(base, token=login["access_token"])

hoje = date.today().isoformat()
lista0 = etapa("listar transações (vazio)", cli.listar_transacoes)
print(f"     -> {len(lista0)} transações")
nova = etapa("criar transação", lambda: cli.criar_transacao({
    "tipo": "despesa", "valor": 123.45, "categoria": "Alimentação",
    "descricao": "Teste integração", "data": hoje, "status": "pago"}))
print(f"     -> resposta: { {k: nova.get(k) for k in ('id', 'tipo', 'valor', 'categoria', 'data')} }")
lista1 = etapa("listar transações", cli.listar_transacoes)
assert any(t.get("id") == nova.get("id") for t in lista1), "transação criada não aparece na lista"
etapa("editar transação", lambda: cli.editar_transacao(nova["id"], {
    "tipo": "despesa", "valor": 99.9, "categoria": "Alimentação",
    "descricao": "Teste editado", "data": hoje, "status": "pendente"}))
orc = etapa("listar orçamentos", lambda: cli.listar_orcamentos(hoje[:8] + "01", hoje))
print(f"     -> {len(orc)} orçamentos")
if orc:
    etapa("alterar limite", lambda: cli.alterar_limite(orc[0]["id"], 500))
etapa("excluir transação", lambda: cli.excluir_transacao(nova["id"]))
print("TUDO OK")


