"""Tema visual OrbitFin (paleta oficial Grupo Marte). Ver design.md > Sistema visual.

Spec (OpenSpec): openspec/specs/interface-base/spec.md
"""
from __future__ import annotations

import streamlit as st

TERRACOTA = "#E05638"
# Tom derivado (mesmo matiz, 12% mais escuro) para texto pequeno e fundo de botões:
# #E05638 dá 3,8:1 sobre branco; #C54C31 dá 4,7:1 (WCAG AA). Ver PRODUCT.md > Brand Commitments.
TERRACOTA_TEXTO = "#C54C31"
MARINHO = "#1A2238"
FUNDO = "#F4F6F8"
BRANCO = "#FFFFFF"

UICONS_CSS = "https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css"
FONTE = "Schibsted Grotesk"
FONTE_CSS = "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&display=swap"


def rgba(hex_cor: str, alfa: float) -> str:
    r, g, b = (int(hex_cor[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alfa})"


def configurar_pagina() -> None:
    # "auto": aberta no desktop, recolhida no celular (onde a navegação vai para o topo)
    st.set_page_config(page_title="OrbitFin", page_icon="◆", layout="wide",
                       initial_sidebar_state="auto")


_CSS_BASE = f"""
@import url('{FONTE_CSS}');
@import url('{UICONS_CSS}');

:root {{
  --terracota: {TERRACOTA};
  --terracota-10: {rgba(TERRACOTA, .10)};
  --terracota-25: {rgba(TERRACOTA, .25)};
  --terracota-60: {rgba(TERRACOTA, .60)};
  --terracota-texto: {TERRACOTA_TEXTO};
  --terracota-texto-hover: #A9402A;
  --marinho: {MARINHO};
  --marinho-70: {rgba(MARINHO, .70)};
  --texto-suave: {rgba(MARINHO, .65)};  /* 5,0:1 sobre branco; 4,85:1 sobre o fundo */
  --marinho-10: {rgba(MARINHO, .08)};
  --marinho-06: {rgba(MARINHO, .06)};
  --fundo: {FUNDO};
  --card: {BRANCO};
  --sombra: 0 1px 2px rgba(26,34,56,.06), 0 8px 24px rgba(26,34,56,.06);
  --raio: 14px;
}}

html, body, .stApp *:not([data-testid="stIconMaterial"]):not(.fi) {{
  font-family: '{FONTE}', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
}}
.stApp {{ background: var(--fundo); color: var(--marinho); caret-color: var(--terracota-texto);
  scrollbar-color: rgba(26,34,56,.22) transparent; }}
.stApp ::selection {{ background: var(--terracota-25); color: var(--marinho); }}
.stApp :focus-visible {{ outline: 2px solid var(--terracota-texto); outline-offset: 2px; }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none; }}
[data-testid="stMainBlockContainer"] {{ padding: 2.2rem 2.6rem 4rem; max-width: 1280px; }}
.fi {{ display: inline-flex; line-height: 1; }}
@media (max-width: 768px) {{
  [data-testid="stMainBlockContainer"] {{ padding: 1rem 1rem 3rem; }}
}}

/* ---------- Botões ---------- */
.stApp button[kind="primary"], .stApp button[data-testid="stBaseButton-primary"],
.stApp button[data-testid="stBaseButton-primaryFormSubmit"] {{
  background: var(--terracota-texto); border: 1px solid var(--terracota-texto); color: #fff;
  border-radius: 10px; font-weight: 600; box-shadow: 0 1px 2px rgba(26,34,56,.12);
}}
.stApp button[kind="primary"]:hover, .stApp button[data-testid="stBaseButton-primary"]:hover,
.stApp button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
  background: var(--terracota-texto-hover); border-color: var(--terracota-texto-hover); color: #fff;
}}
.stApp button[data-testid="stBaseButton-secondary"],
.stApp button[data-testid="stBaseButton-secondaryFormSubmit"] {{
  background: var(--card); color: var(--marinho); border: 1px solid var(--marinho-10);
  border-radius: 10px; font-weight: 600;
}}
.stApp button[data-testid="stBaseButton-secondary"]:hover {{
  border-color: var(--terracota-texto); color: var(--terracota-texto);
}}
.stApp button[data-testid="stBaseButton-tertiary"],
.stApp button[data-testid="stBaseButton-tertiary"] p {{ color: var(--terracota-texto); font-weight: 600; }}

/* ---------- Campos ---------- */
.stApp [data-baseweb="input"], .stApp [data-baseweb="select"] > div, .stApp [data-baseweb="textarea"] {{
  border-radius: 10px; border-color: var(--marinho-10); background: var(--card);
}}
.stApp [data-baseweb="input"]:focus-within, .stApp [data-baseweb="select"] > div:focus-within {{
  border-color: var(--terracota); box-shadow: 0 0 0 3px var(--terracota-10);
}}
.stApp label p {{ font-weight: 600; color: var(--marinho-70); font-size: .82rem; }}
[data-testid="stForm"] {{ border: none; padding: 0; }}
[data-testid="stAlert"] {{ border-radius: 10px; }}
[data-testid="stDialog"] [role="dialog"] {{ border-radius: 18px; }}
.stApp [data-testid="stRadio"] label p {{ color: var(--marinho); }}

/* ---------- Cards (st.container(key="card_...")) ---------- */
.stApp [class*="st-key-card"] {{
  background: var(--card); border-radius: var(--raio); box-shadow: var(--sombra);
  border: 1px solid var(--marinho-06); padding: 1.2rem 1.35rem 1.25rem;
}}
.of-card-titulo {{ display: flex; align-items: center; justify-content: space-between;
  font-weight: 700; font-size: 1rem; color: var(--marinho); margin-bottom: .35rem; }}
.of-card-titulo small {{ font-weight: 500; color: var(--texto-suave); font-size: .8rem; }}

/* ---------- Cabeçalho ---------- */
.of-header {{ margin: 0 0 1.4rem; }}
.of-kicker {{ text-transform: uppercase; letter-spacing: .08em; font-size: .72rem;
  font-weight: 700; color: var(--terracota-texto-hover); }}
.of-titulo {{ font-size: 1.85rem; font-weight: 800; color: var(--marinho);
  letter-spacing: -.02em; line-height: 1.15; margin-top: .15rem; }}
.of-subtitulo {{ color: var(--marinho-70); font-size: .95rem; margin-top: .3rem; }}

/* ---------- KPIs ---------- */
.of-kpi {{ background: var(--card); border-radius: var(--raio); box-shadow: var(--sombra);
  border: 1px solid var(--marinho-06); padding: 1.05rem 1.2rem 1.1rem; height: 100%;
  position: relative; overflow: hidden; }}
.of-kpi-topo {{ display: flex; justify-content: space-between; align-items: center; }}
.of-kpi-rotulo {{ text-transform: uppercase; letter-spacing: .06em; font-size: .7rem;
  font-weight: 700; color: var(--texto-suave); }}
.of-kpi-valor {{ font-size: 1.55rem; font-weight: 800; letter-spacing: -.02em;
margin-top: .55rem; color: var(--marinho); white-space: nowrap; }}
.of-kpi-valor.neg {{ color: var(--terracota-texto); }}
.of-kpi-dica {{ color: var(--texto-suave); font-size: .78rem; margin-top: .2rem; }}
.of-kpi.destaque {{ background: var(--marinho); border-color: var(--marinho); }}
.of-kpi.destaque .of-kpi-rotulo, .of-kpi.destaque .of-kpi-dica {{ color: rgba(255,255,255,.6); }}
.of-kpi.destaque .of-kpi-valor {{ color: #fff; }}
.of-kpi.destaque .of-kpi-valor.neg {{ color: #ff9a85; }}
.of-kpi.destaque::after {{ content: ""; position: absolute; right: -40px; bottom: -60px;
  width: 160px; height: 160px; border-radius: 50%; border: 1px solid rgba(255,255,255,.08);
  box-shadow: 0 0 0 22px rgba(255,255,255,.02), 0 0 0 44px rgba(255,255,255,.015); }}
.of-ico {{ width: 34px; height: 34px; border-radius: 10px; display: inline-flex;
  align-items: center; justify-content: center; font-size: 1rem; }}
.of-ico.t {{ background: var(--terracota-10); color: var(--terracota); }}
.of-ico.m {{ background: var(--marinho-10); color: var(--marinho); }}
.of-kpi.destaque .of-ico {{ background: rgba(255,255,255,.1); color: #fff; }}
.of-spark {{ margin-top: .5rem; height: 34px; }}

/* ---------- Selos, barras, listas ---------- */
.of-chip {{ display: inline-block; padding: .14rem .55rem; border-radius: 999px;
  font-size: .72rem; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
  vertical-align: middle; white-space: nowrap; }}
.of-chip.m {{ background: var(--marinho-10); color: var(--marinho); }}
.of-chip.t {{ background: var(--terracota-10); color: var(--terracota-texto-hover); }}
.of-chip.tc {{ background: var(--terracota-texto); color: #fff; }}

.of-barra {{ height: 8px; border-radius: 999px; background: var(--marinho-10); overflow: hidden; }}
.of-barra > span {{ display: block; height: 100%; border-radius: 999px; background: var(--marinho); }}
.of-barra > span.atencao {{ background: var(--terracota-60); }}
.of-barra > span.estourado {{ background: var(--terracota); }}

.of-linha-orc {{ padding: .7rem 0; border-bottom: 1px solid var(--marinho-06); }}
.of-linha-orc:last-child {{ border-bottom: none; }}
.of-linha-orc .cab {{ display: flex; justify-content: space-between; align-items: center;
  gap: .6rem; margin-bottom: .45rem; }}
.of-linha-orc .nome {{ font-weight: 700; font-size: .92rem; }}
.of-linha-orc .valores {{ font-size: .82rem;
  color: var(--marinho-70); white-space: nowrap; }}
.of-linha-orc .sub {{ font-size: .76rem; color: var(--texto-suave); margin-top: .35rem; }}
.of-linha-orc .sub.t {{ color: var(--terracota-texto); font-weight: 600; }}

.of-tx {{ display: flex; align-items: center; gap: .85rem; padding: .7rem 0;
  border-bottom: 1px solid var(--marinho-06); }}
.of-tx:last-child {{ border-bottom: none; }}
.of-tx .av {{ width: 38px; height: 38px; border-radius: 11px; flex: none; display: inline-flex;
  align-items: center; justify-content: center; font-size: .95rem; }}
.of-tx .av.r {{ background: var(--marinho-10); color: var(--marinho); }}
.of-tx .av.d {{ background: var(--terracota-10); color: var(--terracota); }}
.of-tx .info {{ flex: 1; min-width: 0; }}
.of-tx .cat {{ font-weight: 700; font-size: .9rem; display: flex; gap: .45rem; align-items: center; }}
.of-tx .meta {{ font-size: .78rem; color: var(--texto-suave); white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; }}
.of-tx .val {{ font-weight: 800; white-space: nowrap; }}
.of-tx .val.r {{ color: var(--marinho); }}
.of-tx .val.d {{ color: var(--terracota-texto); }}

.of-vazio {{ text-align: center; color: var(--texto-suave); padding: 1.6rem .5rem; font-size: .9rem; }}
.of-vazio .fi {{ font-size: 1.6rem; color: var(--marinho-10); display: block; margin-bottom: .5rem; }}

.of-sugestao {{ display: flex; gap: .7rem; align-items: flex-start; padding: .6rem 0;
  font-size: .88rem; line-height: 1.45; border-bottom: 1px dashed var(--marinho-10); }}
.of-sugestao:last-child {{ border-bottom: none; }}
.of-sugestao .fi {{ color: var(--terracota); margin-top: .2rem; }}
.of-info {{ background: var(--marinho-06); border-radius: 12px; padding: .8rem 1rem;
  font-size: .85rem; color: var(--marinho-70); display: flex; gap: .6rem; align-items: flex-start; }}
.of-info .fi {{ color: var(--terracota); margin-top: .15rem; }}
"""

_CSS_APP = """
/* ---------- Barra lateral ---------- */
section[data-testid="stSidebar"] { background: var(--marinho); border-right: none; }
section[data-testid="stSidebar"] > div { background: var(--marinho); }
section[data-testid="stSidebar"] * { color: #fff; }
[data-testid="stSidebarHeader"] { display: none; }
[data-testid="stSidebarUserContent"] { padding: 1.6rem 1rem 1rem; }
.of-marca { display: flex; align-items: center; gap: .65rem; padding: 0 .35rem 1.6rem; }
.of-marca-nome { font-weight: 800; font-size: 1.25rem; letter-spacing: -.02em; }
.of-menu-rotulo { text-transform: uppercase; letter-spacing: .1em; font-size: .72rem;
  font-weight: 700; color: rgba(255,255,255,.6) !important; padding: 0 .6rem .4rem; }

.stApp [class*="st-key-nav_"] { position: relative; gap: 0; margin-bottom: .2rem; }
.stApp [class*="st-key-nav_"] > [data-testid="stElementContainer"]:first-child {
  position: absolute; left: .95rem; top: 50%; transform: translateY(-62%);
  z-index: 2; pointer-events: none; width: auto !important;
}
.stApp [class*="st-key-nav_"] > [data-testid="stElementContainer"]:first-child p { margin: 0; }
.stApp [class*="st-key-nav_"] .fi { font-size: 1rem; color: rgba(255,255,255,.6); }
.stApp [class*="st-key-nav_"] button {
  width: 100%; justify-content: flex-start; background: transparent; border: none;
  border-radius: 10px; padding: .62rem .9rem .62rem 2.75rem; min-height: 0; box-shadow: none;
}
.stApp [class*="st-key-nav_"] button > div { justify-content: flex-start; width: 100%; }
.stApp [class*="st-key-nav_"] button p { color: rgba(255,255,255,.72); font-weight: 600; font-size: .92rem; }
.stApp [class*="st-key-nav_"] button:hover { background: rgba(255,255,255,.06); }
.stApp [class*="st-key-nav_"][class*="_on"] button {
  background: rgba(255,255,255,.1);
}
.stApp [class*="st-key-nav_"][class*="_on"] button p { color: #fff; }
.stApp [class*="st-key-nav_"][class*="_on"] .fi { color: var(--terracota); }
.stApp [class*="st-key-nav_"] [data-testid="stElementContainer"],
.stApp [class*="st-key-nav_"] .element-container { margin: 0; }

.of-usuario { display: flex; align-items: center; gap: .7rem; padding: 1rem .45rem .8rem;
  border-top: 1px solid rgba(255,255,255,.1); margin-top: 1.4rem; }
.of-avatar { width: 38px; height: 38px; border-radius: 12px; background: var(--terracota-texto);
  display: inline-flex; align-items: center; justify-content: center; font-weight: 800; flex: none; }
.of-usuario .nome { font-weight: 700; font-size: .88rem; line-height: 1.2; }
.of-usuario .email { font-size: .76rem; color: rgba(255,255,255,.62) !important;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 170px; }
.stApp .st-key-sair button { background: transparent; border: 1px solid rgba(255,255,255,.14);
  width: 100%; border-radius: 10px; }
.stApp .st-key-sair button p { color: rgba(255,255,255,.8); font-weight: 600; }
.stApp .st-key-sair button:hover { border-color: var(--terracota); background: var(--terracota-10); }

/* ---------- Navegação no celular (substitui a barra lateral abaixo de 768px) ---------- */
.stApp .st-key-navmovel { display: none; }
@media (max-width: 768px) {
  section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
  [data-testid="stExpandSidebarButton"] { display: none !important; }
  .stApp .st-key-navmovel { display: flex; gap: .55rem; margin: -.25rem 0 1.1rem;
    padding-bottom: .9rem; border-bottom: 1px solid var(--marinho-10); }
  .of-marca-movel { display: flex; align-items: center; justify-content: space-between; }
  .of-marca-movel .marca { display: flex; align-items: center; gap: .5rem; font-weight: 800;
    font-size: 1.1rem; letter-spacing: -.02em; }
  .of-marca-movel .usuario { font-size: .8rem; color: var(--texto-suave); }
  /* marca e "Sair" na mesma linha (o Streamlit empilha colunas no celular) */
  .stApp .st-key-navmovel [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; gap: .5rem; }
  .stApp .st-key-navmovel [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; }
  .stApp .st-key-navmovel [data-testid="stColumn"]:last-child { flex: 0 0 auto; }
  /* pílulas: botões role="radio" dentro do grupo */
  .stApp .st-key-navmovel div:has(> button[role="radio"]) {
    display: flex; flex-direction: row; flex-wrap: wrap; gap: .4rem; }
  .stApp .st-key-navmovel button[role="radio"] {
    border-radius: 999px; border: 1px solid rgba(26,34,56,.14); background: var(--card);
    min-height: 40px; padding: .3rem .9rem; width: auto; }
  .stApp .st-key-navmovel button[role="radio"] p { color: var(--marinho); font-weight: 600; }
  .stApp .st-key-navmovel button[role="radio"][aria-checked="true"] {
    background: var(--marinho); border-color: var(--marinho); }
  .stApp .st-key-navmovel button[role="radio"][aria-checked="true"] p { color: #fff; }
  .stApp .st-key-sair_movel button { min-height: 40px; }
}
"""

_CSS_AUTH = """
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"] { display: none; }
[data-testid="stMainBlockContainer"] { max-width: 1120px; padding-top: 3.2rem; }
.stApp .st-key-card_auth { padding: 2.2rem 2.2rem 1.8rem; }
.of-auth-marca { display: flex; align-items: center; gap: .6rem; margin-bottom: 1.6rem;
  font-weight: 800; font-size: 1.2rem; letter-spacing: -.02em; }
.of-auth-titulo { font-size: 1.7rem; font-weight: 800; letter-spacing: -.02em; line-height: 1.2; }
.of-auth-sub { color: var(--marinho-70); margin: .35rem 0 1.3rem; font-size: .93rem; }
.of-auth-alterna { text-align: center; color: var(--texto-suave); font-size: .86rem; margin-top: .4rem; }
.stApp [class*="st-key-alternar"] button { width: 100%; }
.of-painel { background: var(--marinho); border-radius: 22px; min-height: 560px; height: 100%;
  position: relative; overflow: hidden; color: #fff; padding: 2.6rem; display: flex;
  flex-direction: column; justify-content: flex-end; box-shadow: var(--sombra); }
.of-painel svg { position: absolute; top: -40px; right: -80px; width: 560px; height: 560px; }
.of-painel h2 { color: #fff; font-size: 1.9rem; font-weight: 800; letter-spacing: -.02em;
  line-height: 1.2; margin: 0 0 .7rem; position: relative; padding: 0; }
.of-painel p { color: rgba(255,255,255,.7); font-size: .98rem; line-height: 1.55; margin: 0;
  position: relative; max-width: 420px; }
@media (max-width: 900px) { .of-painel { display: none; } }
"""


def aplicar_tema(auth: bool = False) -> None:
    css = _CSS_BASE + (_CSS_AUTH if auth else _CSS_APP)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
