# -*- coding: utf-8 -*-
# pip install beautifulsoup4 pandas lxml unidecode
import re
import sys
import json
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from typing import Tuple, Dict, List, Optional
from unidecode import unidecode

# ---------- Utilidades ----------

NUM_RE = re.compile(r"([\d.,]+)")
VD_RE = re.compile(r"(\d+)\s*%")


def norm_spaces(s: str) -> str:
    return " ".join(s.split()) if isinstance(s, str) else s


def get_text(el) -> str:
    return norm_spaces(el.get_text(" ", strip=True)) if el else ""


def comma_to_dot(num: str) -> str:
    """Convierte '1.234,56' -> '1234.56' y '0,8' -> '0.8' conservando enteros."""
    if not isinstance(num, str):
        return num
    # quita separadores de miles europeos y normaliza coma decimal
    return num.replace(".", "").replace(",", ".")


def safe_int(x) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None


def standardize_name(name: str) -> str:
    """Normaliza rotulos: capitaliza, quita tildes opcional, y homologa variantes."""
    if not name:
        return name
    base = norm_spaces(name.strip(" .:"))
    # Capitalización primera letra
    base = base[0].upper() + base[1:] if base else base

    # Mapeo de equivalencias comunes
    plain = unidecode(base.lower())
    mapping = {
        "valor energetico": "Valor energético",
        "carbohidratos": "Carbohidratos",
        "azucares": "Azúcares",
        "proteinas": "Proteínas",
        "grasas totales": "Grasas totales",
        "grasas saturadas": "Grasas saturadas",
        "grasas trans": "Grasas trans",
        "fibra": "Fibra",
        "sodio": "Sodio",
    }
    if plain in mapping:
        return mapping[plain]

    # Subnutrientes con prefijo "de los/las cuales" u otros textos
    base = re.sub(r"(?i)^\s*de\s+los?\s+cuales:?\s*", "", base)
    base = re.sub(r"(?i)^\s*de\s+las?\s+cuales:?\s*", "", base)
    base = re.sub(r"(?i)^margen-subnutrientes\s*", "", base)
    return base


def is_noise_left_cell(text: str) -> bool:
    if not text:
        return True
    if any(k in text for k in ["INGREDIENTES", "Actualizado", "Fuente"]):
        return True
    if "Valores Diarios" in text:
        return True
    if re.search(r"(?i)de\s+los?\s+cuales:?\s*$|de\s+las?\s+cuales:?\s*$", text):
        return True
    return False


def parse_left_cell(left: str) -> Optional[Tuple[str, str, str]]:
    """
    Extrae (nombre, cantidad, unidad) de la celda izquierda.
    Acepta decimales con coma/punto y unidades con letras o signos (%, µ, μ).
    """
    if not left:
        return None
    # Busca el último número y su unidad al final
    m = re.search(r"(.+?)\s*([\d.,]+)\s*([a-zA-Zµμ%]+)$", left)
    if not m:
        return None
    name = standardize_name(m.group(1))
    value = comma_to_dot(m.group(2))
    unit = m.group(3).strip()
    return name, value, unit


def extract_portion_from_soup(soup: BeautifulSoup) -> Optional[str]:
    for p in soup.find_all("p"):
        if p.find("strong") and "Porción" in p.get_text():
            return norm_spaces(p.get_text(" ", strip=True))
    return None


def parse_table_from_html(html: str) -> List[Dict]:
    """Devuelve lista de dicts con Nutriente, Cantidad, Unidad, %VD."""
    out = []
    if not isinstance(html, str) or not html.strip():
        return out
    # try to use lxml if available, else fallback to built-in parser
    parser_to_use = "lxml"
    try:
        BeautifulSoup("<html></html>", "lxml")
    except Exception:
        parser_to_use = "html.parser"
    soup = BeautifulSoup(html, parser_to_use)
    table = soup.find("table")
    if not table:
        # algunos CSV traen ya solo el <table> en columna 'tabla_nutricional'
        # si no hay <table> en modal_html, intenta parsear bloque suelto
        soup2 = BeautifulSoup(f"<div>{html}</div>", "lxml")
        table = soup2.find("table")
        if not table:
            return out

    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) != 2:
            continue
        left = get_text(tds[0])
        right = get_text(tds[1])
        if is_noise_left_cell(left):
            continue

        vd = None
        m_vd = VD_RE.search(right)
        if m_vd:
            vd = safe_int(m_vd.group(1))

        parsed = parse_left_cell(left)
        if not parsed:
            continue
        name, value, unit = parsed
        out.append({"Nutriente": name, "Cantidad": value, "Unidad": unit, "%VD": vd})
    return out


def pick_html_source(row: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    """
    Devuelve (html_para_parsear, origen) priorizando modal_html, sino tabla_nutricional.
    """
    if isinstance(row.get("modal_html"), str) and row["modal_html"].strip():
        return row["modal_html"], "modal_html"
    if (
        isinstance(row.get("tabla_nutricional"), str)
        and row["tabla_nutricional"].strip()
    ):
        return row["tabla_nutricional"], "tabla_nutricional"
    return None, None


def product_title_from_soup(soup: BeautifulSoup) -> Optional[str]:
    h = soup.select_one("#vademecum-item-title")
    if h:
        return get_text(h)
    # fallback: usa columna 'titulo' si existe afuera
    return None


# ---------- Pipeline ----------


def process_csv(
    input_csv: str,
    out_long: str = "nutricional_long.csv",
    out_wide: str = "nutricional_wide.csv",
    keep_cols: Optional[List[str]] = None,
) -> Dict[str, str]:
    df = pd.read_csv(input_csv)

    keep_cols = keep_cols or [
        "titulo",
        "descripcion",
        "imagen",
        "ingredientes",
        "fecha",
        "fuente",
    ]
    present_keep = [c for c in keep_cols if c in df.columns]

    records = []
    for idx, row in df.iterrows():
        html, origen = pick_html_source(row)
        if not html:
            continue

        # choose parser similarly here
        parser_to_use = "lxml"
        try:
            BeautifulSoup("<html></html>", "lxml")
        except Exception:
            parser_to_use = "html.parser"
        soup = BeautifulSoup(html, parser_to_use)
        portion = extract_portion_from_soup(soup)
        product = product_title_from_soup(soup) or (
            row["titulo"] if "titulo" in row else None
        )

        nutrients = parse_table_from_html(html)
        if not nutrients:
            # intenta también si la columna alternativa existe
            alt = "tabla_nutricional" if origen == "modal_html" else "modal_html"
            if alt in row and isinstance(row[alt], str):
                nutrients = parse_table_from_html(row[alt])

        base = {k: row.get(k) for k in present_keep}
        base.update(
            {
                "Producto": product,
                "Porción": portion,
                "_origen_html": origen,
                "_row": idx,
            }
        )

        for n in nutrients:
            rec = dict(base)
            rec.update(n)
            # agrega numérico cuando es viable
            rec["Cantidad_num"] = pd.to_numeric(rec["Cantidad"], errors="coerce")
            records.append(rec)

    long_df = pd.DataFrame.from_records(records)
    # orden de columnas
    col_order = present_keep + [
        "Producto",
        "Porción",
        "Nutriente",
        "Cantidad",
        "Unidad",
        "%VD",
        "Cantidad_num",
        "_origen_html",
        "_row",
    ]
    long_df = long_df.reindex(columns=[c for c in col_order if c in long_df.columns])

    # Wide: pivotea cantidades por Nutriente, preserva unidad en nombre para evitar ambigüedad
    if not long_df.empty:
        long_df["Nutriente_unidad"] = (
            long_df["Nutriente"].astype(str)
            + " ["
            + long_df["Unidad"].astype(str)
            + "]"
        )
        id_cols = present_keep + ["Producto", "Porción", "_row"]
        id_cols = [c for c in id_cols if c in long_df.columns]
        wide_df = long_df.pivot_table(
            index=id_cols,
            columns="Nutriente_unidad",
            values="Cantidad_num",
            aggfunc="first",
        ).reset_index()
        # %VD en wide: columnas separadas con sufijo (_%VD)
        vd_df = (
            long_df.pivot_table(
                index=id_cols, columns="Nutriente", values="%VD", aggfunc="first"
            )
            .add_suffix(" (%VD)")
            .reset_index()
        )
        wide_df = pd.merge(wide_df, vd_df, on=id_cols, how="left")
    else:
        wide_df = pd.DataFrame()

    long_df.to_csv(out_long, index=False, encoding="utf-8")
    wide_df.to_csv(out_wide, index=False, encoding="utf-8")

    return {
        "long_csv": out_long,
        "wide_csv": out_wide,
        "rows_long": str(len(long_df)),
        "rows_source": str(len(df)),
    }


# ---------- CLI ----------


def main():
    parser = argparse.ArgumentParser(
        description="Limpieza y normalización de tablas nutricionales desde CSV con HTML."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        help="Ruta al CSV de entrada (ej: productos_galletitas.csv). Si se omite, se intentará usar 'productos_galletitas.csv' en el directorio de trabajo.",
    )
    parser.add_argument(
        "--out-long", default="nutricional_long.csv", help="Salida long form"
    )
    parser.add_argument(
        "--out-wide", default="nutricional_wide.csv", help="Salida wide form"
    )
    parser.add_argument(
        "--keep-cols",
        default="titulo,descripcion,imagen,ingredientes,fecha,fuente",
        help="Columnas del CSV a conservar como contexto, separadas por coma",
    )
    args = parser.parse_args()

    # decide input path: prefer explicit arg, else try default file in CWD
    input_csv = args.input_csv
    if not input_csv:
        default_name = "productos_galletitas.csv"
        try:
            # prefer file in same directory as script/workspace
            import os

            cwd_path = os.path.join(os.getcwd(), default_name)
            if os.path.exists(cwd_path):
                input_csv = cwd_path
            else:
                parser.error(
                    f"No se especificó 'input_csv' y no se encontró '{default_name}' en {os.getcwd()}"
                )
        except Exception:
            parser.error(
                "No se especificó 'input_csv' y no se encontró el archivo por defecto."
            )

    keep = [c.strip() for c in args.keep_cols.split(",") if c.strip()]
    info = process_csv(input_csv, args.out_long, args.out_wide, keep_cols=keep)
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # Uso:
    # python script.py /ruta/productos_galletitas.csv --out-long out_long.csv --out-wide out_wide.csv
    main()
