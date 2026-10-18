// Edita uma transação do usuário (spec: transacoes)
query "transacoes/{transacao_id}" verb=PUT {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int transacao_id
    text tipo filters=trim
    decimal valor
    text data filters=trim
    text categoria filters=trim
    text descricao? filters=trim
    text status filters=trim
  }

  stack {
    db.get transacao {
      field_name = "id"
      field_value = $input.transacao_id
    } as $existente

    // Registro de outro usuário responde como inexistente
    precondition ($existente != null && $existente.user_id == $auth.id) {
      error_type = "notfound"
      error = "Transação não encontrada."
    }

    function.run "OrbitFin/validar_transacao" {
      input = {
        tipo     : $input.tipo
        valor    : $input.valor
        categoria: $input.categoria
        status   : $input.status
      }
    }

    db.edit transacao {
      field_name = "id"
      field_value = $input.transacao_id
      data = {
        tipo     : $input.tipo
        valor    : $input.valor
        data     : $input.data
        categoria: $input.categoria
        descricao: $input.descricao
        status   : $input.status
      }
    } as $transacao
  }

  response = $transacao
}
