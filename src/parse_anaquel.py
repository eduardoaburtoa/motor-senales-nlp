#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_anaquel.py — convierte el "Anaquel con Rendimientos Históricos del Día Actual"
de BBVA México (PDF público) en un CSV estructurado.

Fuente: BBVA México, Anaquel con Rendimientos Históricos, 08/10/2026.
https://portal.bbva.mx/siabinternet/Repositorio/import/doctos/analisis/00003776.pdf

Uso:
    pdftotext -layout "Hoja de rendimientos 8 de octubre.pdf" anaquel.txt
    python3 parse_anaquel.py anaquel.txt ../data/catalogo_fondos.csv

Salida: un renglón por serie de fondo, con su categoría, calificación,
inversión mínima, rendimientos y precio. Todos los datos son los publicados
por BBVA; este script no calcula ni estima ninguna cifra.
"""

import csv
import re
import argparse
import logging
from pathlib import Path

# 6 rendimientos en porcentaje + precio al final del renglón
NUMS = re.compile(
    r"(-?\d+\.\d{2})%\s+(-?\d+\.\d{2})%\s+(-?\d+\.\d{2})%\s+"
    r"(-?\d+\.\d{2})%\s+(-?\d+\.\d{2})%\s+(-?\d+\.\d{2})%\s+(\d+\.\d+)\s*$"
)
CALIF = re.compile(r"^(AAA|AA|A|BBB|BB)/\d+$")

# Encabezados que aparecen centrados y definen la categoría en curso
FAMILIAS = {
    "Fondos de Deuda",
    "Fondos de Renta Variable",
    "Fondos de Estrategias",
    "Fondos de MultiEstrategias",
    "Fondos de MultiActivos",
    "Fondos de Liquidez en Divisas",
}
CATEGORIAS = [
    "Deuda Corto Plazo",
    "Deuda Mediano Plazo",
    "Deuda Largo Plazo",
    "Retorno Absoluto",
    "Fondos de Liquidez en Divisas",
    "Renta Variable Nacional",
    "Renta Variable Internacional",
    "Fondos de Estrategias Pesos",
    "Fondos de Estrategias Dolarizados",
    "Fondos de MultiEstrategias Pesos",
    "Fondos de MultiEstrategias Dolarizados",
    "Fondos de MultiActivos",
]


def parse(path_txt):
    filas, familia, categoria, publico = [], "", "", "Personas Físicas"
    for raw in Path(path_txt).read_text(encoding="utf-8").splitlines():
        linea = raw.rstrip("\n")
        texto = linea.strip()
        if not texto:
            continue

        if texto.startswith("Personas Morales"):
            publico = "Personas Morales"
            continue
        if texto.startswith("Personas Físicas"):
            publico = "Personas Físicas"
            continue

        if texto in FAMILIAS:
            familia = texto
            if texto == "Fondos de Liquidez en Divisas":
                categoria = texto
            continue
        for c in CATEGORIAS:
            if texto.startswith(c):
                categoria = c
                break

        m = NUMS.search(linea)
        if not m:
            continue
        cabeza = linea[: m.start()].split()
        if len(cabeza) < 3:
            continue

        fondo, serie, minimo = cabeza[0], cabeza[1], cabeza[2].replace(",", "")
        calificacion = cabeza[3] if len(cabeza) > 3 and CALIF.match(cabeza[3]) else ""
        if not minimo.isdigit():
            continue

        d, sem, mes, anio, a1, a2, precio = m.groups()
        filas.append(
            dict(
                fondo=fondo,
                serie=serie,
                publico=publico,
                familia=familia or "Fondos de Deuda",
                categoria=categoria,
                calificacion=calificacion,
                minimo_inversion=int(minimo),
                rend_diario=float(d),
                rend_semanal=float(sem),
                rend_acum_mes=float(mes),
                rend_acum_anio=float(anio),
                rend_1_anio=float(a1),
                rend_2_anios=float(a2),
                precio=float(precio),
            )
        )
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("entrada")
    ap.add_argument("salida", nargs="?", default="scratch/catalogo_fondos.csv")
    args = ap.parse_args()
    entrada, salida = args.entrada, Path(args.salida)
    if salida.resolve().parent == Path(__file__).resolve().parents[1] / "data":
        ap.error("data/ está congelada; usa otra carpeta")
    salida.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    filas = parse(entrada)
    if not filas:
        ap.error("No se encontraron series: usa texto extraído con pdftotext -layout")
    campos = [
        "fondo",
        "serie",
        "publico",
        "familia",
        "categoria",
        "calificacion",
        "minimo_inversion",
        "rend_diario",
        "rend_semanal",
        "rend_acum_mes",
        "rend_acum_anio",
        "rend_1_anio",
        "rend_2_anios",
        "precio",
    ]
    with open(salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)
    fondos = sorted({f["fondo"] for f in filas})
    logging.info(f"{len(filas)} series · {len(fondos)} fondos · {salida}")
    for cat in CATEGORIAS:
        n = sum(1 for f in filas if f["categoria"] == cat)
        if n:
            logging.info(f"   {cat:42s} {n:4d}")


if __name__ == "__main__":
    main()
