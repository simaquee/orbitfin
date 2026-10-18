// Exclui uma transação do usuário (spec: transacoes)
query "transacoes/{transacao_id}" verb=DELETE {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int transacao_id
  }

  stack {
    db.get transacao {
      field_name = "id"
      field_value = $input.transacao_id
    } as $existente

    precondition ($existente != null && $existente.user_id == $auth.id) {
      error_type = "notfound"
      error = "Transação não encontrada."
    }

    db.del transacao {
      field_name = "id"
      field_value = $input.transacao_id
    }
  }

  response = {success: true}
}
