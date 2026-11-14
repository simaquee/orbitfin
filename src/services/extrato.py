"""Leitura local de extratos bancários (PDF, CSV e OFX), sem IA e sem serviço externo.

Cada leitor devolve linhas {"data": "AAAA-MM-DD", "descricao": str, "valor": float},
com valor negativo para saídas e positivo para entradas.

Spec (OpenSpec): openspec/specs/transacoes/spec.md
"""
from __future__ import annotations

import csv
import io
import re
import unicodedata
from collections import Counter
from datetime import date

FORMATOS = ("pdf", "csv", "ofx")
CATEGORIA_IMPORTADA = "Outros"  # válida para receita e despesa
MAX_LINHAS = 500  # limite do endpoint /transacoes/lote

MSG_FORMATO = "Formato não suportado. Envie um extrato em PDF, CSV ou OFX."
MSG_VAZIO = "Nenhum lançamento encontrado no arquivo."
MSG_PDF_IMAGEM = ("Não foi possível ler o texto deste PDF (pode ser uma imagem escaneada). "
                  "Exporte o extrato em CSV ou OFX no app do banco.")
MSG_PDF_INVALIDO = "Não foi possível abrir este PDF. Verifique se o arquivo não está corrompido ou protegido por senha."
MSG_CSV_COLUNAS = "Não encontrei as colunas de data, descrição e valor no CSV."
MSG_LIMITE = f"O extrato tem mais de {MAX_LINHAS} lançamentos. Divida o período e importe em partes."
MSG_VALOR_ZERO = "O valor deve ser diferente de zero."


class ErroExtrato(Exception):
    """Arquivo que não pôde ser lido; a mensagem é exibida ao usuário."""


# ---------------------------------------------------------------- utilidades
def _sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


_VALOR = re.compile(r"\d[\d.,]*")


def parse_valor(texto: str) -> float | None:
    """'1.234,56' -> 1234.56; '-45,90', '45,90-', '(45,90)' e '45,90 D' -> -45.9; '-45.90' -> -45.9."""
    if texto is None:
        return None
    s = str(texto).strip().upper().replace("R$", "").replace(" ", " ").strip()
    if not s:
        return None
    negativo = (s.startswith("-") or s.endswith("-") or (s.startswith("(") and s.endswith(")"))
                or bool(re.search(r"\d\s*D$", s)))  # "45,90 D" = débito
    achado = _VALOR.search(s)
    if not achado:
        return None
    numero = achado.group().rstrip(".,")
    if "," in numero and "." in numero:
        decimal = "," if numero.rfind(",") > numero.rfind(".") else "."
    elif "," in numero:
        decimal = ","
    elif "." in numero:
        # "1.234" (milhar brasileiro) x "45.90" (decimal com ponto)
        partes = numero.split(".")
        decimal = "" if len(partes[-1]) == 3 else "."
    else:
        decimal = ""
    milhar = {",": ".", ".": ","}.get(decimal, ".")
    numero = numero.replace(milhar, "")
    if decimal:
        numero = numero.replace(decimal, ".")
    try:
        valor = float(numero)
    except ValueError:
        return None
    return -valor if negativo else valor


def parse_data_extrato(texto: str, ano_padrao: int | None = None) -> date | None:
    """'05/11/2026', '05/11/26', '05/11' (+ano_padrao), '2026-11-05' ou '20261105...' (OFX)."""
    s = str(texto).strip()
    try:
        if m := re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})", s):
            d, mes, a = (int(x) for x in m.groups())
            return date(a + 2000 if a < 100 else a, mes, d)
        if m := re.fullmatch(r"(\d{1,2})/(\d{1,2})", s):
            return date(ano_padrao or date.today().year, int(m.group(2)), int(m.group(1)))
        if m := re.match(r"(\d{4})-(\d{2})-(\d{2})", s):
            return date(*(int(x) for x in m.groups()))
        if m := re.match(r"(\d{4})(\d{2})(\d{2})", s):
            return date(*(int(x) for x in m.groups()))
    except ValueError:
        return None
    return None


def _linha(d: date | None, descricao: str, valor: float | None) -> dict | None:
    if d is None or valor is None or round(valor, 2) == 0:
        return None
    descricao = re.sub(r"\s+", " ", descricao or "").strip()
    return {"data": d.isoformat(), "descricao": descricao, "valor": round(valor, 2)}


# ---------------------------------------------------------------------- CSV
_COLUNAS = {
    "data": ("data", "date", "dt "),
    "descricao": ("descricao", "historico", "lancamento", "description", "memo", "title",
                  "titulo", "detalhe", "estabelecimento"),
    "valor": ("valor", "amount", "quantia", "montante"),
    "credito": ("credito", "entrada"),
    "debito": ("debito", "saida"),
}


def _decodificar(conteudo: bytes) -> str:
    for codificacao in ("utf-8-sig", "latin-1"):
        try:
            return conteudo.decode(codificacao)
        except UnicodeDecodeError:
            continue
    return conteudo.decode("utf-8", errors="replace")


def _mapear_colunas(cabecalho: list[str]) -> dict[str, int]:
    normal = [_sem_acento(c).strip().lower() + " " for c in cabecalho]
    mapa: dict[str, int] = {}
    for campo, nomes in _COLUNAS.items():
        for i, coluna in enumerate(normal):
            if i not in mapa.values() and any(coluna.startswith(n) or f" {n}" in f" {coluna}" for n in nomes):
                mapa[campo] = i
                break
    return mapa


def ler_csv(conteudo: bytes) -> list[dict]:
    texto = _decodificar(conteudo)
    linhas_texto = [l for l in texto.splitlines() if l.strip()]
    if not linhas_texto:
        raise ErroExtrato(MSG_VAZIO)
    # O separador é o que mais aparece no cabeçalho (vírgula aparece nos valores, ponto e vírgula não)
    primeira = linhas_texto[0]
    separador = max(";\t,", key=primeira.count)
    leitor = list(csv.reader(io.StringIO("\n".join(linhas_texto)), delimiter=separador))

    # O cabeçalho pode vir depois de linhas de título do banco
    for inicio, cabecalho in enumerate(leitor[:15]):
        mapa = _mapear_colunas(cabecalho)
        if "data" in mapa and "descricao" in mapa and ("valor" in mapa or "credito" in mapa or "debito" in mapa):
            break
    else:
        raise ErroExtrato(MSG_CSV_COLUNAS)

    def celula(campos: list[str], chave: str) -> str:
        i = mapa.get(chave)
        return campos[i] if i is not None and i < len(campos) else ""

    resultado = []
    for campos in leitor[inicio + 1:]:
        if "valor" in mapa:
            valor = parse_valor(celula(campos, "valor"))
        else:
            credito = parse_valor(celula(campos, "credito")) or 0.0
            debito = parse_valor(celula(campos, "debito")) or 0.0
            valor = abs(credito) - abs(debito)
        descricao = celula(campos, "descricao")
        if "saldo" in _sem_acento(descricao).lower():
            continue
        if linha := _linha(parse_data_extrato(celula(campos, "data")), descricao, valor):
            resultado.append(linha)
    return resultado


# ---------------------------------------------------------------------- OFX
_BLOCO_OFX = re.compile(r"<STMTTRN>(.*?)(?:</STMTTRN>|(?=<STMTTRN>)|(?=</BANKTRANLIST>))",
                        re.IGNORECASE | re.DOTALL)


def _tag_ofx(bloco: str, tag: str) -> str:
    m = re.search(rf"<{tag}>([^<\r\n]*)", bloco, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def ler_ofx(conteudo: bytes) -> list[dict]:
    texto = _decodificar(conteudo)
    resultado = []
    for bloco in _BLOCO_OFX.findall(texto):
        valor_txt = _tag_ofx(bloco, "TRNAMT").replace(",", ".")
        try:
            valor = float(valor_txt)
        except ValueError:
            continue
        descricao = _tag_ofx(bloco, "MEMO") or _tag_ofx(bloco, "NAME")
        if linha := _linha(parse_data_extrato(_tag_ofx(bloco, "DTPOSTED")), descricao, valor):
            resultado.append(linha)
    return resultado


# ---------------------------------------------------------------------- PDF
_NUM_BR = r"\(?[-+]?\s?(?:R\$\s?)?\d{1,3}(?:\.\d{3})*,\d{2}\)?(?:\s?-|\s?[DC](?![A-Za-z]))?"
_LINHA_PDF = re.compile(
    rf"^\s*(\d{{2}}/\d{{2}}(?:/\d{{2,4}})?)\s+(.+?)\s+({_NUM_BR})(?:\s+{_NUM_BR})?\s*$")
# Layout em tabela (um campo por linha): data [hora] / descrição / valor / saldo
_SO_DATA = re.compile(r"^\s*(\d{2}/\d{2}(?:/\d{2,4})?)(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\s*$")
_SO_HORA = re.compile(r"^\s*\d{1,2}:\d{2}(?::\d{2})?\s*$")
_SO_VALOR = re.compile(rf"^\s*{_NUM_BR}\s*$")


def _ano_do_documento(texto: str) -> int:
    anos = Counter(int(a) for a in re.findall(r"\b\d{2}/\d{2}/(\d{4})\b", texto))
    return anos.most_common(1)[0][0] if anos else date.today().year


def texto_pdf(conteudo: bytes) -> str:
    from pypdf import PdfReader  # import local: só quem lê PDF paga o custo

    try:
        leitor = PdfReader(io.BytesIO(conteudo))
        if leitor.is_encrypted:
            leitor.decrypt("")
        return "\n".join(pagina.extract_text() or "" for pagina in leitor.pages)
    except Exception:  # pypdf lança vários tipos para arquivos inválidos
        raise ErroExtrato(MSG_PDF_INVALIDO) from None


def _pdf_por_linha(linhas: list[str], ano: int) -> list[dict]:
    """Um lançamento por linha: 'data descrição valor [saldo]'."""
    resultado = []
    for linha_txt in linhas:
        m = _LINHA_PDF.match(linha_txt)
        if not m:
            continue
        data_txt, descricao, valor_txt = m.groups()
        if "saldo" in _sem_acento(descricao).lower():
            continue
        if linha := _linha(parse_data_extrato(data_txt, ano), descricao, parse_valor(valor_txt)):
            resultado.append(linha)
    return resultado


def _pdf_por_bloco(linhas: list[str], ano: int) -> list[dict]:
    """Tabela com um campo por linha: uma linha só com data abre o lançamento; a hora é
    ignorada; o texto até o primeiro valor é a descrição; o 1º valor é a movimentação e o
    2º (saldo) é descartado. Cabeçalhos e rodapés de página ficam depois dos valores e não
    entram na descrição."""
    resultado = []
    blocos: list[dict] = []
    for linha_txt in linhas:
        if m := _SO_DATA.match(linha_txt):
            blocos.append({"data": m.group(1), "descricao": [], "valores": []})
        elif not blocos:
            continue
        elif _SO_VALOR.match(linha_txt):
            blocos[-1]["valores"].append(linha_txt)
        elif _SO_HORA.match(linha_txt) and not blocos[-1]["descricao"]:
            continue
        elif not blocos[-1]["valores"] and linha_txt.strip():
            blocos[-1]["descricao"].append(linha_txt.strip())
    for b in blocos:
        descricao = " ".join(b["descricao"])
        if not b["valores"] or not descricao or "saldo" in _sem_acento(descricao).lower():
            continue
        if linha := _linha(parse_data_extrato(b["data"], ano), descricao, parse_valor(b["valores"][0])):
            resultado.append(linha)
    return resultado


def ler_pdf(conteudo: bytes) -> list[dict]:
    texto = texto_pdf(conteudo)
    if not texto.strip():
        raise ErroExtrato(MSG_PDF_IMAGEM)
    ano = _ano_do_documento(texto)
    linhas = texto.splitlines()
    # Cada banco diagrama o PDF de um jeito: fica a leitura que encontrar mais lançamentos
    return max(_pdf_por_linha(linhas, ano), _pdf_por_bloco(linhas, ano), key=len)


# ----------------------------------------------------------- entrada única
def ler_extrato(nome_arquivo: str, conteudo: bytes) -> list[dict]:
    extensao = nome_arquivo.rsplit(".", 1)[-1].lower() if "." in nome_arquivo else ""
    leitores = {"csv": ler_csv, "ofx": ler_ofx, "pdf": ler_pdf}
    if extensao not in leitores:
        raise ErroExtrato(MSG_FORMATO)
    linhas = leitores[extensao](conteudo)
    if not linhas:
        raise ErroExtrato(MSG_VAZIO)
    if len(linhas) > MAX_LINHAS:
        raise ErroExtrato(MSG_LIMITE)
    return linhas


# ------------------------------------------------------- revisão e envio
def validar_linha(valor: float | None) -> str | None:
    return MSG_VALOR_ZERO if valor is None or round(valor, 2) == 0 else None


def pendentes(linhas: list[dict]) -> int:
    return sum(1 for l in linhas if not l.get("confirmado"))


def confirmar_todas(linhas: list[dict], atuais: dict[int, tuple[str, float]]) -> int:
    """'Confirmar tudo': confirma cada card pendente com os valores atuais dos campos
    (id -> (descrição, valor)). Card com valor zero continua pendente. Devolve quantos sobraram."""
    for linha in linhas:
        if linha.get("confirmado"):
            continue
        descricao, valor = atuais.get(linha["id"], (linha["descricao"], linha["valor"]))
        if validar_linha(valor) is None:
            linha.update(descricao=(descricao or "").strip(), valor=round(valor, 2), confirmado=True)
    return pendentes(linhas)


def pode_importar(linhas: list[dict]) -> bool:
    return bool(linhas) and pendentes(linhas) == 0


def transacao_importada(linha: dict) -> dict:
    """Linha revisada -> payload de transação (mesmo contrato do POST /transacoes)."""
    valor = round(float(linha["valor"]), 2)
    return {"tipo": "despesa" if valor < 0 else "receita", "valor": abs(valor),
            "data": linha["data"], "categoria": CATEGORIA_IMPORTADA,
            "descricao": (linha.get("descricao") or "").strip(), "status": "pago"}


def montar_lote(linhas: list[dict]) -> list[dict]:
    return [transacao_importada(l) for l in linhas]
