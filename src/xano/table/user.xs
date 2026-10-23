// Usuários do OrbitFin (spec: autenticacao)
// Compartilhada com a API "authentication" do Quick Start do Xano no mesmo workspace:
// mantém role, password_reset e email/password opcionais como no workspace, para o push
// não apagar campos nem quebrar aquela API. A obrigatoriedade de e-mail e senha do
// OrbitFin é garantida no endpoint register_POST.
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1

    // The role of the user within their company (e.g., 'admin', 'member').
    enum role? {
      values = ["admin", "member"]
    }

    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "dAP-YbgShWOf-1UU9Dyq5E3Amsc"
}
