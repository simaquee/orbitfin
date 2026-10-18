// Regras de validação de transação compartilhadas por POST e PUT (spec: transacoes)
// A lista de categorias espelha services/categorias.py.
function "OrbitFin/validar_transacao" {
  input {
    text tipo
    decimal valor
    text categoria
    text status
  }

  stack {
    var $categorias {
      value = {
        despesa: ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Outros"]
        receita: ["Salário", "Freelance", "Investimentos", "Outros"]
      }
    }

    precondition ($input.valor > 0) {
      error_type = "inputerror"
      error = "O valor deve ser maior que zero."
    }

    precondition ($input.status == "pago" || $input.status == "pendente") {
      error_type = "inputerror"
      error = "Status deve ser pago ou pendente."
    }

    precondition ($input.tipo == "receita" || $input.tipo == "despesa") {
      error_type = "inputerror"
      error = "Categoria inválida para o tipo informado."
    }

    var $categoria_ok {
      value = false
    }

    foreach ($categorias|get:$input.tipo) {
      each as $c {
        conditional {
          if ($c == $input.categoria) {
            var.update $categoria_ok {
              value = true
            }
          }
        }
      }
    }

    precondition ($categoria_ok) {
      error_type = "inputerror"
      error = "Categoria inválida para o tipo informado."
    }
  }

  response = null
  guid = "_RfrKsAwjvbPJuKIzM-VE40YvY8"
}
