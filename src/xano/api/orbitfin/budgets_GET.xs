// Orçamentos do usuário com o gasto do período (spec: orcamentos)
// inicio/fim = primeiro e último dia do mês (AAAA-MM-DD), enviados pelo cliente.
query budgets verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
    text inicio filters=trim
    text fim filters=trim
  }

  stack {
    db.query budget {
      where = $db.budget.user_id == $auth.id
      sort = {budget.categoria: "asc"}
      return = {type: "list"}
    } as $budgets

    // Seed preguiçoso: 7 orçamentos padrão no primeiro acesso
    conditional {
      if (($budgets|count) == 0) {
        var $padroes {
          value = [
            {categoria: "Alimentação", limite: 800}
            {categoria: "Moradia", limite: 1200}
            {categoria: "Transporte", limite: 400}
            {categoria: "Lazer", limite: 300}
            {categoria: "Saúde", limite: 200}
            {categoria: "Educação", limite: 150}
            {categoria: "Outros", limite: 500}
          ]
        }

        foreach ($padroes) {
          each as $p {
            db.add budget {
              data = {
                user_id   : $auth.id
                categoria : $p.categoria
                limite    : $p.limite
                updated_at: "now"
              }
            }
          }
        }

        db.query budget {
          where = $db.budget.user_id == $auth.id
          sort = {budget.categoria: "asc"}
          return = {type: "list"}
        } as $budgets
      }
    }

    // Despesas pagas e pendentes do período
    db.query transacao {
      where = $db.transacao.user_id == $auth.id && $db.transacao.tipo == "despesa" && $db.transacao.data >= $input.inicio && $db.transacao.data <= $input.fim
      return = {type: "list"}
    } as $despesas

    var $resultado {
      value = []
    }

    foreach ($budgets) {
      each as $b {
        var $gasto {
          value = 0
        }

        foreach ($despesas) {
          each as $d {
            conditional {
              if ($d.categoria == $b.categoria) {
                math.add $gasto {
                  value = $d.valor
                }
              }
            }
          }
        }

        var $percentual {
          value = 0
        }

        conditional {
          if ($b.limite > 0) {
            var.update $percentual {
              value = ($gasto / $b.limite) * 100
            }
          }
        }

        array.push $resultado {
          value = {
            id        : $b.id
            categoria : $b.categoria
            limite    : $b.limite
            gasto     : $gasto
            percentual: $percentual
          }
        }
      }
    }
  }

  response = $resultado
  guid = "MXcVbwtkE1GHev8OmIXRQWBIiIE"
}
