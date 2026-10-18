# autenticacao Specification

## Purpose
Permite que cada pessoa crie uma conta, entre e saia do OrbitFin, garantindo que somente ela acesse seus próprios dados financeiros.

## Requirements

### Requirement: Cadastro de usuário
O sistema SHALL permitir criar uma conta informando nome completo, e-mail, senha e confirmação de senha; após o cadastro bem-sucedido, o usuário MUST entrar automaticamente no sistema.

#### Scenario: Cadastro válido
- **WHEN** o usuário informa "Ana Souza", "ana@email.com", senha "orbita2026" e a mesma confirmação
- **THEN** a conta é criada, o usuário entra no sistema e vê o Dashboard

#### Scenario: E-mail já cadastrado
- **WHEN** o usuário tenta se cadastrar com um e-mail que já possui conta
- **THEN** o sistema exibe "Já existe uma conta com este e-mail." e não cria outra conta

### Requirement: Validação do formulário de cadastro
O sistema MUST validar o cadastro antes de enviá-lo: todos os campos são obrigatórios, a confirmação deve ser igual à senha e a senha deve ter no mínimo 8 caracteres, com pelo menos 1 letra e 1 número. O backend MUST aplicar a mesma regra de senha.

#### Scenario: Campos vazios
- **WHEN** o usuário envia o cadastro sem preencher o nome
- **THEN** o sistema exibe "Preencha todos os campos."

#### Scenario: Senhas diferentes
- **WHEN** a confirmação difere da senha
- **THEN** o sistema exibe "As senhas não coincidem."

#### Scenario: Senha fraca
- **WHEN** o usuário informa a senha "abcdefgh", que não tem números
- **THEN** o sistema exibe "A senha deve ter no mínimo 8 caracteres, com pelo menos 1 letra e 1 número."

### Requirement: Login
O sistema SHALL autenticar o usuário por e-mail e senha, sem diferenciar maiúsculas e minúsculas no e-mail, e iniciar uma sessão com um token válido por 24 horas.

#### Scenario: Credenciais corretas
- **WHEN** o usuário informa "ANA@email.com " e a senha correta
- **THEN** o usuário entra no sistema e vê o Dashboard

#### Scenario: Credenciais incorretas
- **WHEN** o usuário informa um e-mail inexistente ou a senha errada
- **THEN** o sistema exibe "E-mail ou senha incorretos." sem indicar qual dos dois está errado

#### Scenario: Campos vazios no login
- **WHEN** o usuário clica em "Entrar" sem preencher e-mail ou senha
- **THEN** o sistema exibe "Preencha e-mail e senha." e não chama o backend

#### Scenario: Servidor indisponível
- **WHEN** o backend não pode ser alcançado durante o login
- **THEN** o sistema exibe "Não foi possível conectar ao servidor. Tente novamente." em vez de "E-mail ou senha incorretos."

### Requirement: Alternância entre login e cadastro
A tela de login SHALL oferecer o link "Criar conta" e a tela de cadastro SHALL oferecer o link "Fazer login".

#### Scenario: Ir para o cadastro
- **WHEN** o usuário clica em "Criar conta" na tela de login
- **THEN** a tela de cadastro é exibida

### Requirement: Proteção das telas internas
Usuários sem sessão ativa MUST ver apenas as telas de login e cadastro, sem a barra lateral.

#### Scenario: Acesso sem login
- **WHEN** alguém abre a aplicação sem sessão ativa
- **THEN** a tela de login é exibida e a barra lateral fica oculta

### Requirement: Identificação do usuário
O sistema SHALL exibir o primeiro nome do usuário na saudação do Dashboard e o nome completo e o e-mail no rodapé da barra lateral, com um avatar contendo a inicial do nome.

#### Scenario: Saudação pelo primeiro nome
- **WHEN** a usuária "Ana Souza" abre o Dashboard
- **THEN** o sistema exibe "Olá, Ana" e, na barra lateral, o avatar "A", "Ana Souza" e "ana@email.com"

### Requirement: Logout
O sistema SHALL oferecer o botão "Sair" na barra lateral, que encerra a sessão e descarta o token.

#### Scenario: Sair
- **WHEN** o usuário clica em "Sair"
- **THEN** a sessão é encerrada e a tela de login é exibida
