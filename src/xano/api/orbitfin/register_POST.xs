// Cadastro e entrada automática (spec: autenticacao)
query register verb=POST {
  api_group = "OrbitFin"

  input {
    text name filters=trim
    email email filters=trim|lower
    text password
  }

  stack {
    precondition (($input.name|strlen) > 0 && ($input.password|strlen) > 0) {
      error_type = "inputerror"
      error = "Preencha todos os campos."
    }

    // Letra e número são exigidos pelo filtro do campo password da tabela user
    // (min:8|minAlpha:1|minDigit:1); o cliente valida antes com a mensagem em português.
    precondition (($input.password|strlen) >= 8) {
      error_type = "inputerror"
      error = "A senha deve ter no mínimo 8 caracteres, com pelo menos 1 letra e 1 número."
    }

    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $existente

    precondition ($existente == null) {
      error_type = "inputerror"
      error = "Já existe uma conta com este e-mail."
    }

    db.add user {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
      }
    } as $user

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {
    access_token: $authToken
    user_id     : $user.id
    name        : $user.name
    email       : $user.email
  }
  guid = "bVorz5168Cjsb3ttFiOoo5Oh2wQ"
}
