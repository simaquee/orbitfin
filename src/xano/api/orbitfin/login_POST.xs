// Login com token de 24 horas (spec: autenticacao)
query login verb=POST {
  api_group = "OrbitFin"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "name", "email", "password"]
    } as $user

    // Mesma mensagem para e-mail inexistente e senha errada
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "E-mail ou senha incorretos."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $senha_ok

    precondition ($senha_ok) {
      error_type = "accessdenied"
      error = "E-mail ou senha incorretos."
    }

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
}
