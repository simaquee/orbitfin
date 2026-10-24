# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Pessoas físicas — jovens adultos, estudantes e profissionais — que querem organizar as próprias finanças sem depender de planilhas. Usam o app várias vezes por semana para registrar receitas e despesas e, de tempos em tempos, para conferir se o mês está sob controle.

O trabalho principal é **lançar rápido**: registrar um gasto ou recebimento em segundos, logo depois que ele acontece. Consultar o painel, os limites e os relatórios é secundário e vem depois.

## Product Purpose

Dar a cada pessoa um retrato claro e confiável do próprio dinheiro: quanto entrou, quanto saiu, quanto sobra e onde está o excesso, com limites por categoria e sugestões automáticas para fechar o mês no azul. Sucesso é o usuário manter o hábito de registrar (porque é rápido) e tomar decisões melhores a partir do que vê.

## Positioning

Um organizador financeiro pessoal deliberadamente simples, com categorias fixas e limites mensais prontos desde o cadastro. As sugestões são geradas por regras transparentes sobre os dados do próprio usuário (limite estourado, perto do limite, pendências, taxa de poupança), sem depender de IA externa nem de conexão com bancos.

## Operating Context

- Uso individual, em navegador (desktop e celular), com sessão por login; cada usuário vê apenas os próprios dados.
- Fluxo típico: lançar transação → conferir Dashboard → ajustar limites no Orçamento → revisar Metas e Relatórios no fim do mês.
- Lançamentos podem ficar "pendentes" (a pagar/receber); o saldo considera só os pagos, enquanto gastos do mês e orçamentos contam pagos e pendentes.

## Capabilities and Constraints

- Telas: Login, Cadastro, Dashboard, Transações, Orçamento, Metas, Relatórios.
- Categorias fixas por tipo. Despesa: Alimentação, Moradia, Transporte, Lazer, Saúde, Educação, Outros. Receita: Salário, Freelance, Investimentos, Outros.
- 7 orçamentos padrão por usuário (R$ 800, 1.200, 400, 300, 200, 150, 500); alerta a partir de 85% do limite; "Metas" é a visão de contenção sobre esses mesmos limites (não há metas de acúmulo).
- Valores em BRL no formato pt-BR (R$ 1.234,56); datas DD/MM/AAAA; interface em português.
- Stack existente: Python + Streamlit + Plotly (frontend, em `src/`), Xano (backend REST + JWT, em `src/xano/`), hospedagem no Streamlit Community Cloud. O visual é feito com CSS injetado sobre componentes do Streamlit, o que limita o controle fino de layout e interação.
- Requisitos formais e mudanças ficam no OpenSpec (`openspec/`): 8 capacidades em `openspec/specs/` (fonte da verdade do comportamento) e o histórico de mudanças em `openspec/changes/archive/`. Cada arquivo de `src/` cita a spec que implementa.
- Fora do escopo atual (decisão em aberto): contas bancárias, categorias personalizadas, metas de acúmulo, transações recorrentes, importação de extratos.

## Brand Commitments

- Nome: **OrbitFin**, identidade "Grupo Marte". Obrigatória.
- Paleta obrigatória de 3 cores + branco para superfícies: Terracota `#E05638` (primária, ações, despesas, alertas), Azul Marinho `#1A2238` (navegação, texto, receitas), Cinza Claro `#F4F6F8` (fundo), Branco `#FFFFFF` (cards).
- Acessibilidade da paleta (decisão confirmada): o terracota oficial `#E05638` tem só 3,8:1 sobre branco. Ele continua em fundos, barras, gráficos, ícones e destaques; textos pequenos e o fundo de botões com texto branco usam o tom derivado `#C54C31` (mesmo matiz, 12% mais escuro, 4,7:1), para cumprir WCAG AA.
- Ícones: Flaticon UIcons (`fi-rr-*` / `fi-br-*`), nunca emojis coloridos. Obrigatório.
- Símbolo: planeta em forma de pentágono (Marte) em terracota, com anel de órbita.

## Evidence on Hand

- Projeto de referência: github.com/lucianocsjunior13-gif/OrbitFin (documentos PRODUCT.md, SPECIFICATION.md do original).
- Não há depoimentos, clientes, números de uso ou imprensa. Não inventar.

## Product Principles

1. **Lançar primeiro.** Registrar uma transação deve ser a ação mais rápida e acessível de qualquer tela.
2. **Números confiáveis.** O mesmo valor aparece igual em todas as telas; a regra de cálculo (pago × pendente, mês × histórico) é sempre explícita.
3. **Simples por padrão.** Categorias e limites prontos; nada exige configuração antes do primeiro uso.
4. **Alertas acionáveis.** Toda sugestão diz o que aconteceu e quanto; nada de mensagens vagas.
