// Lista as transações do usuário autenticado (spec: transacoes)
query transacoes verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
  }

  stack {
    db.query transacao {
      where = $db.transacao.user_id == $auth.id
      sort = {transacao.data: "desc"}
      return = {type: "list"}
    } as $transacoes
  }

  response = $transacoes
  guid = "LzmzEFJM7GGc1Gdb0iT_15oAVp8"
}
