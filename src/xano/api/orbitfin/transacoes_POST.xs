// Cria uma transação (spec: transacoes)
query transacoes verb=POST {
  api_group = "OrbitFin"
  auth = "user"

  input {
    text tipo filters=trim
    decimal valor
    text data filters=trim
    text categoria filters=trim
    text descricao? filters=trim
    text status filters=trim
  }

  stack {
    function.run "OrbitFin/validar_transacao" {
      input = {
        tipo     : $input.tipo
        valor    : $input.valor
        categoria: $input.categoria
        status   : $input.status
      }
    }

    db.add transacao {
      data = {
        created_at: "now"
        user_id   : $auth.id
        tipo      : $input.tipo
        valor     : $input.valor
        data      : $input.data
        categoria : $input.categoria
        descricao : $input.descricao
        status    : $input.status
      }
    } as $transacao
  }

  response = $transacao
}
