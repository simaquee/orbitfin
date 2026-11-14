// Cria várias transações de uma vez, tudo ou nada (spec: transacoes, importação de extrato)
query "transacoes/lote" verb=POST {
  api_group = "OrbitFin"
  auth = "user"

  input {
    object[1:500] transacoes {
      schema {
        text tipo filters=trim
        decimal valor
        text data filters=trim
        text categoria filters=trim
        text descricao? filters=trim
        text status filters=trim
      }
    }
  }

  stack {
    // Valida todas as linhas antes de gravar qualquer uma
    foreach ($input.transacoes) {
      each as $t {
        function.run "OrbitFin/validar_transacao" {
          input = {
            tipo     : $t.tipo
            valor    : $t.valor
            categoria: $t.categoria
            status   : $t.status
          }
        }
      }
    }

    db.transaction {
      stack {
        foreach ($input.transacoes) {
          each as $t {
            db.add transacao {
              data = {
                created_at: "now"
                user_id   : $auth.id
                tipo      : $t.tipo
                valor     : $t.valor
                data      : $t.data
                categoria : $t.categoria
                descricao : $t.descricao
                status    : $t.status
              }
            }
          }
        }
      }
    }
  }

  response = {criadas: $input.transacoes|count}
}
