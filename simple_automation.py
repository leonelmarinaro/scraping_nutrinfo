"""
Script simple de automatización con Playwright para Nutrinfo
Basado en el código original del usuario, pero con mejoras
"""

from playwright.sync_api import Playwright, sync_playwright
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from typing import Any


def parse_nutrition_table(modal) -> dict:
    """
    Parsea la tabla nutricional dentro del modal (locator) y devuelve
    un dict estructurado: porcion, nutrientes (dict de name->{value,unit}), porcentajes_VD (by name).
    """
    result: dict = {}

    try:
        # Porción
        portion_loc = modal.locator("p:has-text('Porción')")
        if portion_loc.count() > 0:
            text = portion_loc.first.inner_text()
            result["porcion"] = text.split("Porción:")[-1].strip()

        table = modal.locator("table").first
        if not table or table.count() == 0:
            return result

        nutrients: dict = {}
        porcentajes: dict = {}

        rows = table.locator("tr").all()
        for row in rows:
            # Skip separator rows (contain hr)
            if row.locator("hr").count() > 0:
                continue

            tds = row.locator("td")
            if tds.count() == 0:
                continue

            left = tds.nth(0).inner_text().strip()
            right = ""
            if tds.count() > 1:
                right = tds.nth(1).inner_text().strip()

            # Normalize left text
            left = re.sub(r"\s+", " ", left)

            # Try to extract a nutrient name and value
            # Example matches: 'Valor Energético 129 kcal', 'Carbohidratos 20 g', 'azúcares 0,8 g'
            m = re.search(
                r"(?P<name>[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+?)\s+(?P<value>[0-9]+(?:[.,][0-9]+)?)\s*(?P<unit>kcal|g|mg)?",
                left,
            )
            if m:
                name = m.group("name").strip().lower()
                name_key = re.sub(r"\s+", "_", name)
                val_s = m.group("value").replace(",", ".")
                try:
                    value = float(val_s) if "." in val_s else int(val_s)
                except Exception:
                    value = val_s
                unit = m.group("unit") or ""
                nutrients[name_key] = {"value": value, "unit": unit}
                # parse %VD from right column if present
                m_pct = re.search(r"([0-9]{1,3})%", right)
                if m_pct:
                    porcentajes[name_key] = int(m_pct.group(1))
            else:
                # Could be a sub-nutrient line like 'azúcares 0,8 g' without strong
                m2 = re.search(
                    r"(?P<name>[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+?)\s+(?P<value>[0-9]+(?:[.,][0-9]+)?)\s*(?P<unit>g|mg)?",
                    left,
                )
                if m2:
                    name = m2.group("name").strip().lower()
                    name_key = re.sub(r"\s+", "_", name)
                    val_s = m2.group("value").replace(",", ".")
                    try:
                        value = float(val_s) if "." in val_s else int(val_s)
                    except Exception:
                        value = val_s
                    unit = m2.group("unit") or ""
                    nutrients[name_key] = {"value": value, "unit": unit}
                    m_pct = re.search(r"([0-9]{1,3})%", right)
                    if m_pct:
                        porcentajes[name_key] = int(m_pct.group(1))

        result["nutrientes"] = nutrients
        result["porcentajes_VD"] = porcentajes

    except Exception as e:
        # On parse errors, return what we have
        result["_parse_error"] = str(e)

    return result


def run_simple_automation(playwright: Playwright) -> None:
    """
    Ejecuta una automatización simple en Nutrinfo

    Args:
        playwright: Instancia de Playwright
    """
    print("🚀 Iniciando navegador...")

    # Configurar navegador
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()

    try:
        print("📍 Navegando a Nutrinfo...")
        page.goto("https://www.nutrinfo.com/vademecum")

        # Esperar a que la página cargue
        # page.wait_for_load_state("networkidle")
        print("✅ Página cargada")

        print("🔍 Aplicando filtro de categoría...")
        # Hacer clic en el filtro de categorías
        page.get_by_placeholder("Filtrar por categorias").click()

        # Seleccionar "Galletitas"
        page.get_by_role("option", name="Galletitas", exact=True).click()

        # Esperar a que se apliquen los resultados del filtro
        page.wait_for_selector("article[data-key]", timeout=15000)
        print("✅ Filtro aplicado: Galletitas")

        # Usar Locator para evitar problemas de elementos "detached"
        items_locator = page.locator("article[data-key]")
        items_count = items_locator.count()
        print(f"🔎 Se encontraron {items_count} productos. Procesando los primeros 4.")

        productos: list[dict[str, str]] = []

        for idx in range(min(8, items_count)):
            try:
                print(f"➡️  Procesando producto {idx + 1}/{min(8, items_count)}")
                article_nth = items_locator.nth(idx)
                # Click en el card interno (zona clickeable)
                clickable = article_nth.locator("div.vademecum-item-card")
                # Asegurar visibilidad antes del click
                clickable.scroll_into_view_if_needed()
                clickable.click()

                # Esperar a que el modal visible aparezca
                page.wait_for_selector("div.modal.show", state="visible", timeout=12000)
                modal = page.locator("div.modal.show").first

                # Extraer datos del modal visible
                titulo = ""
                titulo_loc = modal.locator("h5.modal-title")
                if titulo_loc.count() > 0:
                    titulo = titulo_loc.first.inner_text()

                descripcion = ""
                desc_loc = modal.locator("#vademecum-item-content p")
                if desc_loc.count() > 0:
                    descripcion = desc_loc.first.inner_text()

                # Imagen
                imagen = ""
                img_loc = modal.locator(".vademecuum-modal-img")
                if img_loc.count() > 0:
                    imagen = img_loc.first.get_attribute("src") or ""

                # Ingredientes: buscar el <p> que contiene 'INGREDIENTES:'
                ingredientes = ""
                for p in modal.locator("p").all():
                    txt = p.inner_text()
                    if "INGREDIENTES:" in txt:
                        ingredientes = txt
                        break

                # Fecha de actualización
                fecha = ""
                for p in modal.locator("p").all():
                    txt = p.inner_text()
                    if "Actualizado:" in txt:
                        fecha = txt.replace("Actualizado:", "").strip()
                        break

                # Fuente
                fuente = ""
                for p in modal.locator("p").all():
                    txt = p.inner_text()
                    if "Fuente:" in txt:
                        fuente = txt.replace("Fuente:", "").strip()
                        break

                # Tabla nutricional: obtener el HTML completo (outerHTML) y almacenarlo tal cual
                tabla = ""
                tabla_loc = modal.locator("table").first
                if tabla_loc and tabla_loc.count() > 0:
                    try:
                        # outerHTML para conservar la etiqueta <table> también
                        tabla = tabla_loc.evaluate("el => el.outerHTML")
                    except Exception:
                        # Fallback a inner_html
                        try:
                            tabla = tabla_loc.inner_html()
                        except Exception:
                            tabla = ""

                # Guardar el HTML completo del modal para parseo posterior
                modal_html = modal.evaluate("el => el.outerHTML") if modal else ""

                # Guardar el archivo debug para tests
                with open(f"debug_modal_{idx}.html", "w", encoding="utf-8") as f:
                    f.write(modal_html)

                productos.append(
                    {
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "imagen": imagen,
                        "ingredientes": ingredientes,
                        "fecha": fecha,
                        "fuente": fuente,
                        "tabla_nutricional": tabla,
                        # Guardar el HTML completo del modal para parseo posterior
                        "modal_html": modal_html,
                    }
                )

                # Cerrar el modal
                close_btn = modal.locator("button.btn-close")
                if close_btn.count() > 0:
                    close_btn.first.click()
                else:
                    # Alternativa: presionar Escape
                    page.keyboard.press("Escape")
                # Esperar a que el modal desaparezca para evitar overlay sobre siguientes clicks
                page.wait_for_selector("div.modal.show", state="hidden", timeout=8000)
                time.sleep(0.3)
            except Exception as e:
                print(f"⚠️  Error procesando producto {idx + 1}: {e}")
                # Intentar cerrar modal si quedó abierto
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
                time.sleep(0.5)

        # Guardar resultados en un DataFrame
        df = pd.DataFrame(productos)
        df.to_csv("productos_galletitas.csv", index=False)
        print("💾 Datos guardados en productos_galletitas.csv")

        print("✅ Automatización completada exitosamente")

    except Exception as e:
        print(f"❌ Error durante la automatización: {e}")
        raise
    finally:
        print("🧹 Cerrando navegador...")
        context.close()
        browser.close()


def parse_modal_html(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "",
        "MARCA": "",
        "DENOMINACIÓN DE VENTA": "",
        "CANTIDAD PORCIÓN (g)": "",
        "VALOR ENERGÉTICO (Kcal/ porción)": "",
        "CARBOHIDRATOS (g/porción)": "",
        "AZÚCARES TOTALES  (g/ porción)": "",
        "AZÚCARES AÑADIDOS (g/ porción)": "",
        "PROTEÍNAS  (g/ porción)": "",
        "GRASAS TOTALES (g/ porción)": "",
        "GRASAS SATURADAS (g/ porción)": "",
        "GRASAS TRANS (g/ porción)": "",
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": "",
        "SODIO  (mg/ porción)": "",
        "Ingredientes": "",
        "Actualizado": "",
        "Fuente": "",
    }

    # Title
    title_elem = soup.find("h5", class_="modal-title")
    if title_elem:
        title = title_elem.get_text().strip()
        if " - " in title:
            name, marca = title.split(" - ", 1)
        else:
            # assume last word is marca
            parts = title.rsplit(" ", 1)
            if len(parts) == 2:
                name, marca = parts
            else:
                name = title
                marca = ""
        result["GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)"] = name.strip()
        result["MARCA"] = marca.strip(".").strip()
        # Corrección de errores comunes en el HTML
        if result["MARCA"] == "Golsfish":
            result["MARCA"] = "Goldfish"

    # Description
    desc_elem = soup.find("div", id="vademecum-item-content")
    if desc_elem:
        p = desc_elem.find("p")
        if p:
            result["DENOMINACIÓN DE VENTA"] = p.get_text().strip()

    # Ingredientes, Actualizado, Fuente
    for p in soup.find_all("p"):
        text = p.get_text()
        if "INGREDIENTES:" in text:
            result["Ingredientes"] = re.sub(
                r"\s+", " ", text.replace("INGREDIENTES:", "").strip()
            )
        elif "Actualizado:" in text:
            result["Actualizado"] = text.replace("Actualizado:", "").strip()
        elif "Fuente:" in text:
            result["Fuente"] = text.replace("Fuente:", "").strip()

    # Portion
    portion_p = None
    for p in soup.find_all("p"):
        if "Porción" in p.get_text():
            portion_p = p
            break
    if portion_p:
        m = re.search(r"Porción[:\s]*(\d+)\s*g", portion_p.get_text())
        if m:
            result["CANTIDAD PORCIÓN (g)"] = int(m.group(1))

    # Table
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) == 2:
                left = tds[0].get_text().strip()
                right = tds[1].get_text().strip()
                # normalize
                left = re.sub(r"\s+", " ", left)
                right = re.sub(r"\s+", " ", right)
                # extract name from left, remove "de las cuales:" if present
                name_part = left.split("de las cuales:")[0].strip()
                # text = name_part + " " + right
                text = name_part + " " + right
                # parse
                m = re.search(
                    r"([A-Za-zÁÉÍÓÚáéíóúÑñ\s]+?)\s+(\d+(?:[.,]\d+)?)\s*(kcal|g|mg)?",
                    text,
                    re.IGNORECASE,
                )
                if m:
                    nut_name = m.group(1).strip().lower()
                    val_str = m.group(2).replace(",", ".")
                    try:
                        val = float(val_str) if "." in val_str else int(val_str)
                    except Exception:
                        val = val_str
                    mapping = {
                        "valor energético": "VALOR ENERGÉTICO (Kcal/ porción)",
                        "carbohidratos": "CARBOHIDRATOS (g/porción)",
                        "hidratos de carbono disponibles": "CARBOHIDRATOS (g/porción)",
                        "azúcares": "AZÚCARES TOTALES  (g/ porción)",
                        "azucares": "AZÚCARES TOTALES  (g/ porción)",
                        "azúcares añadidos": "AZÚCARES AÑADIDOS (g/ porción)",
                        "azucares añadidos": "AZÚCARES AÑADIDOS (g/ porción)",
                        "proteínas": "PROTEÍNAS  (g/ porción)",
                        "grasas totales": "GRASAS TOTALES (g/ porción)",
                        "grasas saturadas": "GRASAS SATURADAS (g/ porción)",
                        "grasas trans": "GRASAS TRANS (g/ porción)",
                        "grasas monoinsaturadas": "GRASAS MONOINSATURADAS (g/ porción)",
                        "grasas poliinsaturadas": "GRASAS POLINSATURADAS (g/ porción)",
                        "colesterol": "COLESTEROL (g/ porción)",
                        "fibra": "FIBRA ALIMENTARIA  (g/ porción)",
                        "sodio": "SODIO  (mg/ porción)",
                    }
                    if nut_name in mapping:
                        result[mapping[nut_name]] = val

    return result


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        run_simple_automation(playwright)
