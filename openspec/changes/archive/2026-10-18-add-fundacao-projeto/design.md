# Design

## Context

Projeto novo. O original tinha dois modos de armazenamento (SQLite local e Xano) escolhidos por uma flag, dois grupos de API no Xano (`api:orbitfin` e `api:FODf7XFO`) e o tema divergia da paleta oficial. Veja proposal.md para a motivação.

## Goals / Non-Goals

**Goals:**
- Um único caminho de dados (Xano), com cliente HTTP centralizado e testável.
- Casca visual reutilizável e fiel à paleta oficial.

**Non-Goals:**
- Modo offline, cache local ou persistência da sessão entre recarregamentos do navegador.

## Decisions

- **Somente Xano, um único grupo de API (`orbitfin`).** Elimina a flag SQLite/Xano e o grupo `api:FODf7XFO`, que no original não era usado. Alternativa considerada: manter o fallback SQLite, descartada porque duplicava toda a lógica e quebrava o isolamento por usuário.
- **Estrutura de pastas:**
  ```
  src/
    app.py               # entrypoint e roteamento
    components/          # theme.py, sidebar.py, header.py, ui.py (cards, KPIs, chips)
    views/               # uma tela por arquivo
    services/
      api.py             # cliente HTTP Xano (único ponto de I/O)
      formatacao.py      # moeda, datas, meses pt-BR (funções puras)
    xano/                # XanoScript versionado (table/, api/orbitfin/)
  tests/
  ```
- **`src/services/api.py` com exceções tipadas** (`ErroConexao`, `ErroValidacao`, `SessaoExpirada`). As views capturam e exibem; o 401 é tratado num único lugar que limpa a sessão. No original cada função engolia exceções e retornava `None`, o que escondia erros (por exemplo, falha de rede aparecia como "senha incorreta").
- **Formatação sem depender de `locale`.** `strftime("%b")` no original dependia da localidade do servidor; usaremos uma tabela fixa de meses em português.
- **Tema via CSS injetado** (`st.markdown` com `<style>`) mais `.streamlit/config.toml` (`primaryColor = "#E05638"`), e Flaticon UIcons carregado via CDN.

## Sistema visual

Direção: "painel de controle de missão", sóbrio e financeiro, com o Terracota como única cor de ação. Tudo dentro da paleta oficial; variações só por opacidade.

- **Tokens (CSS custom properties em `src/components/theme.py`):**
  - Cores: `--terracota #E05638`, `--terracota-10` (rgba 10%), `--terracota-25`, `--marinho #1A2238`, `--marinho-70` (texto secundário), `--marinho-10` (bordas e trilhas de barras), `--fundo #F4F6F8`, `--card #FFFFFF`.
  - Raios 14px (cards) e 10px (inputs/botões). Sombra única `0 1px 2px rgba(26,34,56,.06), 0 8px 24px rgba(26,34,56,.06)`.
- **Tipografia:** "Schibsted Grotesk" (Google Fonts) com fallback `system-ui`. Plus Jakarta Sans foi descartada no polimento Impeccable por ser uma fonte saturada. Algarismos proporcionais: nesta fonte, os tabulares dão largura fixa também à vírgula e ao ponto. Hierarquia: título de página 28px/800, valor de KPI 26px/800, rótulos 12px/700 em caixa alta; selos com no mínimo 11,5px.
- **Barra lateral Azul Marinho** com texto branco: marca (pentágono Terracota + "OrbitFin"), itens com ícone UIcons, item ativo com fundo branco 10% e ícone Terracota (sem filete lateral); rodapé com avatar, nome, e-mail e "Sair". Até 768px, a barra lateral some e a navegação vira pílulas no topo da página.
- **Contraste (WCAG AA):** `--terracota-texto` `#C54C31` para texto pequeno e fundo de botões; `#A9402A` para rótulos sobre o fundo cinza e selos; texto de apoio em marinho com 65% de opacidade (5,0:1). O `#E05638` oficial fica em fundos, barras, gráficos e ícones.
- **Cards de KPI:** rótulo em caixa alta, valor grande, dica em `--marinho-70`; um ícone em pastilha (`--terracota-10` ou `--marinho-10`) no canto.
- **Selos (chips):** pílulas com fundo 10% e texto da cor cheia: PAGO (marinho), PENDENTE (terracota).
- **Barras de progresso:** trilha `--marinho-10`, preenchimento marinho (ok), `--terracota` a 60% (atenção) ou terracota cheio (estourado).
- **Telas de login/cadastro:** duas colunas; à esquerda o formulário em card branco; à direita um painel Azul Marinho com ilustração SVG de órbitas concêntricas em torno de um planeta pentagonal Terracota e a frase da marca. Abaixo de 900px o painel some.
- **Gráficos Plotly:** fundo transparente, grade `--marinho-10`, fonte do tema, sem barra de ferramentas, rótulos em pt-BR.

## Risks / Trade-offs

- [CSS customizado pode quebrar com atualizações do Streamlit] → fixar a versão mínima no `requirements.txt` e concentrar seletores em `src/components/theme.py`.
- [Sessão não persiste ao recarregar a página] → aceito no MVP (igual ao original); pode virar mudança futura.
