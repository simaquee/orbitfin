# interface-base Specification

## Purpose
Define a casca visual e os comportamentos transversais do OrbitFin (identidade visual, navegação, formatação e comunicação com o backend) compartilhados por todas as telas.

## Requirements

### Requirement: Paleta oficial e ícones
A interface SHALL usar exclusivamente as cores Terracota `#E05638`, Azul Marinho `#1A2238`, Cinza Claro `#F4F6F8` e Branco `#FFFFFF`, e ícones Flaticon UIcons no lugar de emojis. Texto pequeno em terracota e fundos de botão com texto branco MUST usar o tom derivado `#C54C31` (mesmo matiz) para atingir contraste WCAG AA (4,5:1).

#### Scenario: Fundo e botão primário
- **WHEN** qualquer tela é exibida
- **THEN** o fundo da aplicação é `#F4F6F8`, os cards são `#FFFFFF` e os botões primários têm fundo `#C54C31` com texto branco

#### Scenario: Cores de receita e despesa
- **WHEN** um valor de receita ou despesa é exibido em lista ou gráfico
- **THEN** receitas usam `#1A2238`; despesas usam `#E05638` em gráficos e ícones e `#C54C31` em valores de texto

#### Scenario: Contraste de textos
- **WHEN** qualquer texto de interface é exibido sobre branco ou sobre o fundo `#F4F6F8`
- **THEN** o contraste é de no mínimo 4,5:1

### Requirement: Navegação lateral
Para usuários autenticados, o sistema SHALL exibir uma barra lateral com a marca "OrbitFin" e os itens, nesta ordem: Dashboard, Transações, Orçamento, Metas e Relatórios, destacando o item da página atual. Em telas com até 768px de largura, a barra lateral MUST dar lugar a uma navegação no topo com os mesmos itens, na mesma ordem, e o botão "Sair".

#### Scenario: Troca de página
- **WHEN** o usuário clica em "Transações" na barra lateral
- **THEN** a página de transações é exibida e o item "Transações" fica destacado

#### Scenario: Navegação no celular
- **WHEN** o usuário acessa o app numa tela de 390px de largura
- **THEN** a barra lateral não cobre o conteúdo e os itens de navegação aparecem no topo da página, com o item atual destacado

#### Scenario: Página inicial
- **WHEN** o usuário acaba de entrar no sistema
- **THEN** a página exibida é o Dashboard

### Requirement: Cabeçalho por página
Cada página SHALL exibir um cabeçalho com um rótulo superior e um título: Dashboard ("Visão geral" / "Dashboard"), Transações ("Movimentações" / "Transações"), Orçamento ("Planejamento" / "Orçamento"), Metas ("Planejamento" / "Metas") e Relatórios ("Análises" / "Relatórios").

#### Scenario: Cabeçalho do orçamento
- **WHEN** o usuário abre a página Orçamento
- **THEN** o cabeçalho mostra "Planejamento" acima do título "Orçamento"

### Requirement: Formatação monetária e de datas
O sistema SHALL exibir valores monetários no formato brasileiro com duas casas decimais, datas como DD/MM/AAAA e meses abreviados em português, independentemente da localidade do servidor.

#### Scenario: Valor positivo
- **WHEN** o valor 1234.5 é exibido
- **THEN** o texto mostrado é "R$ 1.234,50"

#### Scenario: Valor negativo
- **WHEN** o valor -80 é exibido
- **THEN** o texto mostrado é "-R$ 80,00"

#### Scenario: Mês abreviado
- **WHEN** o mês de outubro de 2026 é exibido de forma abreviada
- **THEN** o texto mostrado é "out/2026"

### Requirement: Configuração do backend
O sistema MUST ler a URL base da API Xano a partir de `.streamlit/secrets.toml` e exibir uma mensagem orientando a configuração quando ela estiver ausente, sem quebrar com erro técnico.

#### Scenario: Secrets ausentes
- **WHEN** a aplicação é iniciada sem `xano.base_url` configurado
- **THEN** o sistema exibe "Configure a URL do Xano em .streamlit/secrets.toml (veja secrets.toml.example)." e não exibe nenhuma outra tela

### Requirement: Feedback de comunicação com o backend
Durante chamadas ao backend, o sistema SHALL exibir um indicador de carregamento; em falhas, MUST exibir uma mensagem em português sem detalhes técnicos brutos.

#### Scenario: Falha de conexão
- **WHEN** o backend não responde em até 30 segundos ou a conexão falha
- **THEN** o sistema exibe "Não foi possível conectar ao servidor. Tente novamente."

#### Scenario: Erro de validação do backend
- **WHEN** o backend recusa uma operação com uma mensagem de erro
- **THEN** o sistema exibe essa mensagem ao usuário

#### Scenario: Sessão expirada
- **WHEN** o backend responde que o token é inválido ou expirou (HTTP 401)
- **THEN** o sistema encerra a sessão, volta para a tela de login e exibe "Sua sessão expirou. Entre novamente."
