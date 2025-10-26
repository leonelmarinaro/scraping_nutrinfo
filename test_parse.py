"""
Tests para el parseo de modal HTML.
Completa los diccionarios 'expected' con los valores correctos que deberían extraerse de cada modal.
Ejecuta con: python test_parse.py
"""

import json
from simple_automation import parse_modal_html


# def test_parse_0():
#     with open("debug_modal_0.html", "r", encoding="utf-8") as f:
#         html = f.read()
#     parsed = parse_modal_html(html)
#     expected = {
#         "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Bizcochos Salados Tradicionales Libre de Gluten",
#         "MARCA": "Delicel",
#         "DENOMINACIÓN DE VENTA": "Bizcocho salado libre de gluten con aromatizante idéntico al natural sabor pan. Contenido graso 17%",
#         "CANTIDAD PORCIÓN (g)": 30,
#         "VALOR ENERGÉTICO (Kcal/ porción)": 129,
#         "CARBOHIDRATOS (g/porción)": 20,
#         "AZÚCARES TOTALES  (g/ porción)": 0.8,
#         "AZÚCARES AÑADIDOS (g/ porción)": "",
#         "PROTEÍNAS  (g/ porción)": 0.7,
#         "GRASAS TOTALES (g/ porción)": 5.1,
#         "GRASAS SATURADAS (g/ porción)": 2.2,
#         "GRASAS TRANS (g/ porción)": 0,
#         "GRASAS MONOINSATURADAS (g/ porción)": "",
#         "GRASAS POLINSATURADAS (g/ porción)": "",
#         "COLESTEROL (g/ porción)": "",
#         "FIBRA ALIMENTARIA  (g/ porción)": 0.2,
#         "SODIO  (mg/ porción)": 242,
#         "Ingredientes": "Harina de arroz, almidón de maíz, aceite vegetal interesterificado, fécula de mandioca, glucosa, sal, leudantes químicos INS 503ii, INS 500ii, INS 341i), emulsionante (INS 471), estabilizante (INS 415), aromatizante idéntico al natural pan, colorante natural (INS 160b).",
#         "Actualizado": "26-07-2025",
#         "Fuente": "Rótulo",
#     }
#     assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_1():
    with open("debug_modal_1.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galletitas Crackers Mix de Semillas",
        "MARCA": "Shiva",
        "DENOMINACIÓN DE VENTA": "Galletitas snack libre de gluten",
        "CANTIDAD PORCIÓN (g)": 30,
        "VALOR ENERGÉTICO (Kcal/ porción)": 129,
        "CARBOHIDRATOS (g/porción)": 20,
        "AZÚCARES TOTALES  (g/ porción)": 0.4,
        "AZÚCARES AÑADIDOS (g/ porción)": "",
        "PROTEÍNAS  (g/ porción)": 2.9,
        "GRASAS TOTALES (g/ porción)": 4.2,
        "GRASAS SATURADAS (g/ porción)": 1.4,
        "GRASAS TRANS (g/ porción)": 0,
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 1,
        "SODIO  (mg/ porción)": 89,
        "Ingredientes": "Harina de arroz integral, fécula de mandioca, semillas de girasol peladas, lino dorado molido, aceite de coco, semillas de sésamo integral, aceite de girasol, sal fina modificad en sodio, masa madre de harina de arroz, ANT: tocoferoles.",
        "Actualizado": "26-07-2025",
        "Fuente": "Rótulo",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_2():
    with open("debug_modal_2.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galletitas Dulces con Avena y Pasas",
        "MARCA": "Frutigran",
        "DENOMINACIÓN DE VENTA": "Galletitas dulces con avena y pasas",
        "CANTIDAD PORCIÓN (g)": 30,
        "VALOR ENERGÉTICO (Kcal/ porción)": 131,
        "CARBOHIDRATOS (g/porción)": 21,
        "AZÚCARES TOTALES  (g/ porción)": "",
        "AZÚCARES AÑADIDOS (g/ porción)": "",
        "PROTEÍNAS  (g/ porción)": 5.1,
        "GRASAS TOTALES (g/ porción)": 4.2,
        "GRASAS SATURADAS (g/ porción)": 0.5,
        "GRASAS TRANS (g/ porción)": 0,
        "GRASAS MONOINSATURADAS (g/ porción)": 3.3,
        "GRASAS POLINSATURADAS (g/ porción)": 0.4,
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 1.2,
        "SODIO  (mg/ porción)": 81,
        "Ingredientes": "harina de trigo enriquecida Ley Nº 25.630, aceite de girasol de alto oleico, pasas de uva, avena arrollada, azúcar, almidon de maíz, harina integral, fibra soluble, jarabe de maíz, sal, emulsionante (monoglicéridos de ácidos grasos), regulador de la acidez (bicarbonato de sodio), saborizante natural vainilla, aromatizantes naturales melaza y manteca, leudante químico (bicarbonato de amonio), antioxidante (tocoferoles).",
        "Actualizado": "30-06-2025",
        "Fuente": "Página web empresa oficial",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_3():
    with open("debug_modal_3.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galletitas Dulces con Avena y Pasas",
        "MARCA": "Frutigran",
        "DENOMINACIÓN DE VENTA": "Galletitas dulces con avena y pasas de uva.",
        "CANTIDAD PORCIÓN (g)": 39,
        "VALOR ENERGÉTICO (Kcal/ porción)": 169,
        "CARBOHIDRATOS (g/porción)": 27,
        "AZÚCARES TOTALES  (g/ porción)": "",
        "AZÚCARES AÑADIDOS (g/ porción)": "",
        "PROTEÍNAS  (g/ porción)": 2.9,
        "GRASAS TOTALES (g/ porción)": 5.5,
        "GRASAS SATURADAS (g/ porción)": 0.6,
        "GRASAS TRANS (g/ porción)": 0,
        "GRASAS MONOINSATURADAS (g/ porción)": 4.3,
        "GRASAS POLINSATURADAS (g/ porción)": 0.5,
        "COLESTEROL (g/ porción)": 0,
        "FIBRA ALIMENTARIA  (g/ porción)": 1.6,
        "SODIO  (mg/ porción)": 105,
        "Ingredientes": "harina de trigo enriquecida Ley Nº 25.630, aceite de girasol de alto oleico, pasas de uva, avena arrollada, azúcar, almidon de maíz, harina integral, fibra soluble, jarabe de maíz, sal, emulsionante (monoglicéridos de ácidos grasos), regulador de la acidez (bicarbonato de sodio), saborizante natural vainilla, aromatizantes naturales melaza y manteca, leudante químico (bicarbonato de amonio), antioxidante (tocoferoles).",
        "Actualizado": "30-06-2025",
        "Fuente": "Empresa",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_4():
    with open("debug_modal_4.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galletitas con Avena y Pasas",
        "MARCA": "Granolitas",
        "DENOMINACIÓN DE VENTA": "Galletitas dulces con harina integral, pasas de uva y avena. 13% mayeria grasa",
        "CANTIDAD PORCIÓN (g)": 30,
        "VALOR ENERGÉTICO (Kcal/ porción)": 129,
        "CARBOHIDRATOS (g/porción)": 21,
        "AZÚCARES TOTALES  (g/ porción)": 4.5,
        "AZÚCARES AÑADIDOS (g/ porción)": "",
        "PROTEÍNAS  (g/ porción)": 2.2,
        "GRASAS TOTALES (g/ porción)": 4,
        "GRASAS SATURADAS (g/ porción)": 0.4,
        "GRASAS TRANS (g/ porción)": 0,
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 1.3,
        "SODIO  (mg/ porción)": 87,
        "Ingredientes": "harina integral, harina de trigo enriquecida Ley N° 25.630 (hierro: mg/kg, niacina: 13 mg/kg, vitamina B1: 6,3 mg/kg, acido folico: 2,2 mg/kg, vitamina B2: 1,3 mg/kg), pasas de uva, avena arrollada, aceite de girasol de alto oleico, azucar, almidon de maiz, crispines de arroz, copos de maiz, fibra soluble, almidon modificado, sal, emulsionante (monogliceridos de acidos grasos), regulador de la acidez (bicarbonato de sodio), leudante quimico (bicarbonato de amonio), aromatizantes naturales vainilla, melaza y manteca, antioxidante (tocoferoles).",
        "Actualizado": "30-06-2025",
        "Fuente": "Rótulo",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_5():
    with open("debug_modal_5.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galleta Horneada de Vainilla",
        "MARCA": "Golsfish",
        "DENOMINACIÓN DE VENTA": "Galleta horneada de vainilla.",
        "CANTIDAD PORCIÓN (g)": 100,
        "VALOR ENERGÉTICO (Kcal/ porción)": 444,
        "CARBOHIDRATOS (g/porción)": 66,
        "AZÚCARES TOTALES  (g/ porción)": 25,
        "AZÚCARES AÑADIDOS (g/ porción)": 24,
        "PROTEÍNAS  (g/ porción)": 4.7,
        "GRASAS TOTALES (g/ porción)": 17,
        "GRASAS SATURADAS (g/ porción)": 4.1,
        "GRASAS TRANS (g/ porción)": 0.1,
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 4.1,
        "SODIO  (mg/ porción)": 475,
        "Ingredientes": "HARINA DE TRIGO DE GRANO ENTERO, HARINA DE TRIGO, ACEITE VEGETAL (DE SOYA Y/O DE CANOLA, Y/O DE GIRASOL, Y/O PALMISTE, Y/O PALMA), AZUCARES AÑADIDOS (AZÚCAR, AZÚCAR MORENA, SÓLIDOS DE JARABE DE MAÍZ), ALMIDÓN DE MAÍZ, SABORIZANTES NATURALES (0,8%) (VAINILLA), SAL YODADA, LECHE DESCREMADA, BICARBONATO DE SODIO, POLVO PARA HORNEAR (PIROFOSFATO ÁCIDO DE SODIO, BICARBONATO DE SODIO, FOSFATO MONOCÁLCICO), COLORANTES NATURALES, CREMA (LECHE), LECITINA DE SOYA, EXTRACTO DE VAINILLA (0,02%). CONTIENE: TRIGO (GLUTEN), LECHE, PRODUCTO DE LA LECHE.",
        "Actualizado": "06-05-2025",
        "Fuente": "Rótulo",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_6():
    with open("debug_modal_6.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galleta Horneada sabor Queso Cheddar",
        "MARCA": "Goldfish",
        "DENOMINACIÓN DE VENTA": "gallleta horneada de queso cheddar",
        "CANTIDAD PORCIÓN (g)": 100,
        "VALOR ENERGÉTICO (Kcal/ porción)": 455,
        "CARBOHIDRATOS (g/porción)": 66,
        "AZÚCARES TOTALES  (g/ porción)": "1.7",
        "AZÚCARES AÑADIDOS (g/ porción)": "0.7",
        "PROTEÍNAS  (g/ porción)": 10,
        "GRASAS TOTALES (g/ porción)": 16,
        "GRASAS SATURADAS (g/ porción)": 3.4,
        "GRASAS TRANS (g/ porción)": 0.1,
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 2.6,
        "SODIO  (mg/ porción)": 950,
        "Ingredientes": "Harina de trigo, queso cheddar, cultivos lácticos, sal, enzimas, extracto de annato, aceite vegetal (de canola, de girasol y/o de soya), sal yodada, levadura, azúcares añadidos (azúcar), hidrolizado de levadura, paprika, especias, apio. Condimento (cebolla en polvo), fosfato mono cálcico, bicarbonato de sodio.",
        "Actualizado": "06-05-2025",
        "Fuente": "rótulo",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


def test_parse_7():
    with open("debug_modal_7.html", "r", encoding="utf-8") as f:
        html = f.read()
    parsed = parse_modal_html(html)
    expected = {
        "GALLETITAS CON GLUTEN (NOMBRE COMERCIAL)": "Galleta Horneada Extra Cheddar",
        "MARCA": "Goldfish",
        "DENOMINACIÓN DE VENTA": "Galleta horneada extra cheddar",
        "CANTIDAD PORCIÓN (g)": 100,
        "VALOR ENERGÉTICO (Kcal/ porción)": 454,
        "CARBOHIDRATOS (g/porción)": 68,
        "AZÚCARES TOTALES  (g/ porción)": 3.7,
        "AZÚCARES AÑADIDOS (g/ porción)": 0,
        "PROTEÍNAS  (g/ porción)": 10.7,
        "GRASAS TOTALES (g/ porción)": 15.3,
        "GRASAS SATURADAS (g/ porción)": 3.4,
        "GRASAS TRANS (g/ porción)": 0.1,
        "GRASAS MONOINSATURADAS (g/ porción)": "",
        "GRASAS POLINSATURADAS (g/ porción)": "",
        "COLESTEROL (g/ porción)": "",
        "FIBRA ALIMENTARIA  (g/ porción)": 2.6,
        "SODIO  (mg/ porción)": 985,
        "Ingredientes": "HARINA DE TRIGO, QUESO CHEDDAR (12%) (LECHE ENTERA DE VACA, CULTIVOS LÁCTICOS, SAL, ENZIMAS, EXTRACTO DE ANNATO), ACEITE VEGETAL (DE CANOLA, DE GIRASOL Y/O DE SOYA), SAL YODADA, AZUCARES ANADIDOS (AZUCAR), HIDROLIZADO DE LEVADURA, SÓLIDOS DE LA LECHE, HARINA DE MAIZ, EXTRACTO DE LEVADURA AUTOLIZADA, LEVADURA TORULA, EXTRACTO DE PAPRIKA, ESPECIAS, APIO, QUESO CHEDDAR CON ENZIMAS MODIFICADAS, CONDIMENTOS (CEBOLLA Y AJO EN POLVO), ÁCIDO CÍTRICO, ÁCIDO LÁCTICO, LACTATO DE CALCIO, SABORIZANTE NATURAL (QUESO CHEDDAR), GRASA BUTÍRICA, FOSFATO MONOCÁLCICO, BICARBONATO DE SODIO. CONTIENE: TRIGO (GLUTEN), LECHE, PRODUCTO DE LA LECHE.",
        "Actualizado": "06-05-2025",
        "Fuente": "Rótulo",
    }
    assert parsed == expected, f"Parsed: {parsed}\nExpected: {expected}"


if __name__ == "__main__":
    # test_parse_0()
    tests = [
        # test_parse_0,
        test_parse_1,
        test_parse_2,
        test_parse_3,
        test_parse_4,
        test_parse_5,
        test_parse_6,
        test_parse_7,
    ]

    for test in tests:
        test()
        print(f"{test.__name__} passed")
    print("All tests passed!")
