// Altera o limite de um orçamento do usuário (spec: orcamentos)
query "budgets/{budget_id}" verb=PUT {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int budget_id
    decimal limite
  }

  stack {
    precondition ($input.limite > 0) {
      error_type = "inputerror"
      error = "O limite deve ser maior que zero."
    }

    db.get budget {
      field_name = "id"
      field_value = $input.budget_id
    } as $existente

    precondition ($existente != null && $existente.user_id == $auth.id) {
      error_type = "notfound"
      error = "Orçamento não encontrado."
    }

    db.edit budget {
      field_name = "id"
      field_value = $input.budget_id
      data = {
        limite    : $input.limite
        updated_at: "now"
      }
    } as $budget
  }

  response = $budget
}
