#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dataset.py — genera los dos conjuntos de datos sintéticos del prototipo.

1) notas_mercado.csv    Corpus etiquetado de notas de mercado en español.
                        Es el dataset que se usa para comparar los modelos.
2) clientes_simulados.csv  Cartera simulada de 150 clientes del banquero.

POR QUÉ SON SINTÉTICOS
----------------------
No es posible usar notas de análisis internas ni carteras reales de clientes:
las primeras son material propietario de la mesa y las segundas son datos
personales y financieros protegidos por la LFPDPPP. Para fines didácticos y por
privacidad de los datos usamos nombres de superhéroes y villanos, ya que les
puedo simular características individuales relacionadas con la ficción para
poder comprobar la lógica de los resultados.

LO QUE SÍ ES REAL
-----------------
Los nombres de fondo, sus categorías y sus rendimientos provienen del Anaquel
con Rendimientos Históricos de BBVA México del 08/10/2026 (documento público),
procesado por parse_anaquel.py. Ninguna cifra de rendimiento fue inventada.

Ejecución:
    python3 build_dataset.py
"""

import argparse
import logging
from pathlib import Path
import csv
import os
import random
import unicodedata

SEMILLA = 20261008
RNG = random.Random(SEMILLA)

AQUI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(AQUI, "..", "data")

CLASES_ACTIVO = [
    "Deuda Corto Plazo",
    "Deuda Largo Plazo",
    "Renta Variable Nacional",
    "Renta Variable Internacional",
    "Divisas",
]

# ---------------------------------------------------------------------------
# Plantillas. Cada entrada es (clase_activo, impacto, fenomeno, texto).
# El impacto es el efecto esperado sobre ESA clase de activo, con el criterio
# que usaría un banquero patrimonial al preparar una revisión de portafolio.
# Los marcadores {pb}, {pct}, {mes} se sustituyen más abajo.
# ---------------------------------------------------------------------------
PLANTILLAS = [
    # ---------------- DEUDA CORTO PLAZO ----------------
    (
        "Deuda Corto Plazo",
        "POSITIVO",
        "directo",
        "Banxico recortó la tasa de referencia en {pb} puntos base; las tasas de fondeo a un día siguen en niveles atractivos para los fondos de liquidez.",
    ),
    (
        "Deuda Corto Plazo",
        "POSITIVO",
        "directo",
        "La subasta primaria de Cetes a 28 días se colocó por arriba de lo esperado, con demanda sólida de inversionistas institucionales.",
    ),
    (
        "Deuda Corto Plazo",
        "POSITIVO",
        "negacion",
        "El banco central no modificará la tasa en la reunión de {mes}, lo que da visibilidad al carry de los fondos de deuda de corto plazo.",
    ),
    (
        "Deuda Corto Plazo",
        "POSITIVO",
        "negacion",
        "La inflación subyacente no sorprendió al alza y se mantuvo dentro del rango objetivo.",
    ),
    (
        "Deuda Corto Plazo",
        "POSITIVO",
        "contraste",
        "Aunque la volatilidad cambiaria repuntó, los instrumentos de deuda gubernamental de corto plazo conservaron su rendimiento devengado.",
    ),
    (
        "Deuda Corto Plazo",
        "NEGATIVO",
        "directo",
        "La inflación general se aceleró a {pct} por ciento anual y presiona las expectativas de tasa de corto plazo.",
    ),
    (
        "Deuda Corto Plazo",
        "NEGATIVO",
        "directo",
        "Se registraron salidas netas de recursos en fondos de liquidez durante la última semana.",
    ),
    (
        "Deuda Corto Plazo",
        "NEGATIVO",
        "negacion",
        "El comité no descartó un ajuste restrictivo adicional si la inflación no cede en los próximos meses.",
    ),
    (
        "Deuda Corto Plazo",
        "NEGATIVO",
        "contraste",
        "A pesar del buen dato de empleo, el componente de servicios de la inflación volvió a presionar las tasas de corto plazo.",
    ),
    (
        "Deuda Corto Plazo",
        "NEUTRAL",
        "directo",
        "Banxico publicará la minuta de su última decisión de política monetaria el jueves de la próxima semana.",
    ),
    (
        "Deuda Corto Plazo",
        "NEUTRAL",
        "directo",
        "La operadora informó un cambio administrativo en el horario de corte de las órdenes de los fondos de liquidez.",
    ),
    (
        "Deuda Corto Plazo",
        "NEUTRAL",
        "cifra_mixta",
        "La tasa objetivo se mantuvo sin cambio en la decisión de {mes}, en línea con el consenso del mercado.",
    ),
    (
        "Deuda Corto Plazo",
        "NEUTRAL",
        "condicional",
        "Los analistas mantienen sin cambio su pronóstico de tasa para el cierre de año a la espera del próximo dato de inflación.",
    ),
    # ---------------- DEUDA LARGO PLAZO ----------------
    (
        "Deuda Largo Plazo",
        "POSITIVO",
        "directo",
        "La curva de bonos M se aplanó tras el recorte de tasa, con ganancias de capital en los plazos largos.",
    ),
    (
        "Deuda Largo Plazo",
        "POSITIVO",
        "directo",
        "El rendimiento del bono a diez años cedió {pb} puntos base en la semana ante la expectativa de un ciclo de recortes.",
    ),
    (
        "Deuda Largo Plazo",
        "POSITIVO",
        "negacion",
        "La calificadora no modificó la nota soberana y retiró la perspectiva negativa que mantenía desde el año pasado.",
    ),
    (
        "Deuda Largo Plazo",
        "POSITIVO",
        "contraste",
        "Si bien el entorno global sigue incierto, los udibonos capturaron la compresión de spreads de la semana.",
    ),
    (
        "Deuda Largo Plazo",
        "POSITIVO",
        "cifra_mixta",
        "El fondo cerró el mes con minusvalía de {pct} por ciento, pero el devengo acumulado del año sigue en terreno positivo y la duración juega a favor.",
    ),
    (
        "Deuda Largo Plazo",
        "NEGATIVO",
        "directo",
        "El rendimiento del bono a treinta años subió {pb} puntos base y generó minusvalías en los fondos de larga duración.",
    ),
    (
        "Deuda Largo Plazo",
        "NEGATIVO",
        "directo",
        "La calificadora puso en perspectiva negativa la deuda corporativa del sector y advirtió sobre el nivel de apalancamiento.",
    ),
    (
        "Deuda Largo Plazo",
        "NEGATIVO",
        "negacion",
        "El gobierno no logró colocar el monto objetivo de la subasta de bonos largos y tuvo que ofrecer una sobretasa.",
    ),
    (
        "Deuda Largo Plazo",
        "NEGATIVO",
        "negacion",
        "La prima por plazo no se comprimió pese al recorte y la parte larga de la curva sigue castigada.",
    ),
    (
        "Deuda Largo Plazo",
        "NEGATIVO",
        "contraste",
        "Aunque la inflación se moderó, el aumento de la prima de riesgo soberano empujó al alza los rendimientos de largo plazo.",
    ),
    (
        "Deuda Largo Plazo",
        "NEUTRAL",
        "directo",
        "La Secretaría de Hacienda publicó el calendario de subastas del próximo trimestre sin cambios relevantes.",
    ),
    (
        "Deuda Largo Plazo",
        "NEUTRAL",
        "directo",
        "El fondo actualizó su prospecto para precisar la metodología de valuación de instrumentos de deuda.",
    ),
    (
        "Deuda Largo Plazo",
        "NEUTRAL",
        "condicional",
        "El mercado descuenta un escenario de tasas estables, aunque el consenso está dividido sobre el momento del próximo movimiento.",
    ),
    # ---------------- RENTA VARIABLE NACIONAL ----------------
    (
        "Renta Variable Nacional",
        "POSITIVO",
        "directo",
        "El índice de referencia de la bolsa mexicana avanzó {pct} por ciento impulsado por el sector consumo.",
    ),
    (
        "Renta Variable Nacional",
        "POSITIVO",
        "directo",
        "La emisora reportó utilidades por arriba del consenso y elevó su guía para el cierre del año.",
    ),
    (
        "Renta Variable Nacional",
        "POSITIVO",
        "negacion",
        "La empresa no recortó su dividendo pese al entorno y confirmó el calendario de pago.",
    ),
    (
        "Renta Variable Nacional",
        "POSITIVO",
        "contraste",
        "A pesar de la jornada negativa en Wall Street, el mercado local cerró al alza por flujos de inversionistas extranjeros.",
    ),
    (
        "Renta Variable Nacional",
        "POSITIVO",
        "cifra_mixta",
        "Las ventas cayeron {pct} por ciento en el trimestre, pero el margen operativo se expandió y la acción reaccionó al alza.",
    ),
    (
        "Renta Variable Nacional",
        "NEGATIVO",
        "directo",
        "El índice retrocedió {pct} por ciento en la sesión, con el sector financiero liderando las pérdidas.",
    ),
    (
        "Renta Variable Nacional",
        "NEGATIVO",
        "directo",
        "La emisora recortó su guía de ingresos para el año y anunció el retraso de su plan de inversión.",
    ),
    (
        "Renta Variable Nacional",
        "NEGATIVO",
        "negacion",
        "La compañía no alcanzó las estimaciones de utilidad por acción y tampoco dio una guía para el siguiente trimestre.",
    ),
    (
        "Renta Variable Nacional",
        "NEGATIVO",
        "negacion",
        "El plan de expansión no obtuvo la autorización regulatoria esperada.",
    ),
    (
        "Renta Variable Nacional",
        "NEGATIVO",
        "contraste",
        "Aunque el reporte trimestral superó lo esperado, la acción cayó por el deterioro de la perspectiva del sector.",
    ),
    (
        "Renta Variable Nacional",
        "NEUTRAL",
        "directo",
        "La emisora convocó a su asamblea ordinaria de accionistas para el próximo {mes}.",
    ),
    (
        "Renta Variable Nacional",
        "NEUTRAL",
        "directo",
        "La bolsa informó la recomposición trimestral de su índice principal, sin cambios en los pesos de las emisoras mayores.",
    ),
    (
        "Renta Variable Nacional",
        "NEUTRAL",
        "cifra_mixta",
        "El índice cerró prácticamente sin cambio, con avances en consumo y retrocesos en materiales.",
    ),
    # ---------------- RENTA VARIABLE INTERNACIONAL ----------------
    (
        "Renta Variable Internacional",
        "POSITIVO",
        "directo",
        "Los principales índices accionarios de Estados Unidos cerraron con ganancias tras un dato de empleo favorable.",
    ),
    (
        "Renta Variable Internacional",
        "POSITIVO",
        "directo",
        "El sector tecnológico lideró el avance global con reportes trimestrales por arriba del consenso.",
    ),
    (
        "Renta Variable Internacional",
        "POSITIVO",
        "negacion",
        "La Reserva Federal no endureció su discurso y el mercado accionario global reaccionó al alza.",
    ),
    (
        "Renta Variable Internacional",
        "POSITIVO",
        "contraste",
        "Pese al repunte de la volatilidad implícita, los índices globales sostuvieron las ganancias de la semana.",
    ),
    (
        "Renta Variable Internacional",
        "NEGATIVO",
        "directo",
        "Las bolsas europeas retrocedieron {pct} por ciento ante la revisión a la baja del crecimiento de la región.",
    ),
    (
        "Renta Variable Internacional",
        "NEGATIVO",
        "directo",
        "La escalada de tensiones comerciales golpeó a los mercados accionarios de economías emergentes.",
    ),
    (
        "Renta Variable Internacional",
        "NEGATIVO",
        "negacion",
        "El acuerdo comercial no se concretó en la fecha prevista y las bolsas asiáticas cerraron a la baja.",
    ),
    (
        "Renta Variable Internacional",
        "NEGATIVO",
        "contraste",
        "Aunque la inflación estadounidense cedió, el mercado accionario cayó por el temor a una desaceleración más profunda.",
    ),
    (
        "Renta Variable Internacional",
        "NEUTRAL",
        "directo",
        "La temporada de reportes trimestrales en Estados Unidos inicia la próxima semana con el sector financiero.",
    ),
    (
        "Renta Variable Internacional",
        "NEUTRAL",
        "directo",
        "El proveedor del índice global anunció su revisión semestral de componentes, programada para {mes}.",
    ),
    (
        "Renta Variable Internacional",
        "NEUTRAL",
        "condicional",
        "Los estrategas mantienen su objetivo de cierre de año y esperan el dato de inflación antes de ajustar posiciones.",
    ),
    # ---------------- DIVISAS ----------------
    (
        "Divisas",
        "POSITIVO",
        "directo",
        "El peso se apreció {pct} por ciento frente al dólar tras la entrada de flujos de inversión de cartera.",
    ),
    (
        "Divisas",
        "POSITIVO",
        "negacion",
        "La agencia no degradó la calificación soberana y el tipo de cambio recuperó terreno.",
    ),
    (
        "Divisas",
        "POSITIVO",
        "contraste",
        "Si bien el diferencial de tasas se estrechó, el peso mantuvo su fortaleza frente al dólar durante la semana.",
    ),
    (
        "Divisas",
        "NEGATIVO",
        "directo",
        "El tipo de cambio se depreció {pct} por ciento en la jornada ante la aversión al riesgo global.",
    ),
    (
        "Divisas",
        "NEGATIVO",
        "directo",
        "El índice del dólar alcanzó su nivel más alto del año y presionó a las divisas de mercados emergentes.",
    ),
    (
        "Divisas",
        "NEGATIVO",
        "negacion",
        "El banco central no intervino en el mercado cambiario y la moneda extendió su racha de pérdidas.",
    ),
    (
        "Divisas",
        "NEGATIVO",
        "cifra_mixta",
        "El peso cerró con una ganancia marginal de {pct} por ciento en la sesión, pero acumula una depreciación relevante en el mes.",
    ),
    (
        "Divisas",
        "NEUTRAL",
        "directo",
        "El banco central publicó el calendario de subastas de coberturas cambiarias para el próximo trimestre.",
    ),
    (
        "Divisas",
        "NEUTRAL",
        "directo",
        "El tipo de cambio operó en un rango estrecho a la espera del dato de inflación de Estados Unidos.",
    ),
    (
        "Divisas",
        "NEUTRAL",
        "condicional",
        "El consenso no anticipa movimientos relevantes en el tipo de cambio mientras no cambie el diferencial de tasas.",
    ),
]

# Variantes de redacción para ampliar el corpus sin perder la etiqueta.
PREFIJOS = [
    "",
    "",
    "",
    "",
    "Nota de la mesa de análisis: ",
    "Resumen diario de mercados: ",
    "Flash informativo: ",
    "Cierre de mercado: ",
    "Comentario semanal: ",
]
SUFIJOS = [
    "",
    "",
    "",
    "",
    "",
    " Se recomienda revisar la exposición de las carteras afectadas.",
    " El equipo de inversiones dará seguimiento en la sesión del lunes.",
    " El movimiento es consistente con lo observado en la región.",
    " La información se actualizará con el cierre oficial.",
]

PB = [10, 15, 25, 35, 50, 75]
PCT = ["0.4", "0.7", "1.1", "1.6", "2.3", "3.2", "4.8", "5.5"]
MESES = ["noviembre", "diciembre", "enero", "febrero", "marzo"]

CATEGORIA_A_CLASE = {
    "Deuda Corto Plazo": "Deuda Corto Plazo",
    "Deuda Mediano Plazo": "Deuda Corto Plazo",
    "Deuda Largo Plazo": "Deuda Largo Plazo",
    "Retorno Absoluto": "Deuda Largo Plazo",
    "Fondos de Liquidez en Divisas": "Divisas",
    "Renta Variable Nacional": "Renta Variable Nacional",
    "Renta Variable Internacional": "Renta Variable Internacional",
}

DIFICULTAD = {
    "directo": "facil",
    "cifra_mixta": "media",
    "condicional": "media",
    "negacion": "dificil",
    "contraste": "dificil",
}


def normaliza(s: str) -> str:
    return unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()


def fondos_por_clase():
    """Agrupa los fondos reales del anaquel por clase de activo."""
    ruta = os.path.join(DATA, "catalogo_fondos.csv")
    mapa = {c: set() for c in CLASES_ACTIVO}
    with open(ruta, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            clase = CATEGORIA_A_CLASE.get(r["categoria"])
            if clase:
                mapa[clase].add(r["fondo"])
    return {k: sorted(v) for k, v in mapa.items()}


def construir_notas(objetivo: int = 400) -> list[dict]:
    """Genera el corpus histórico con una secuencia aleatoria reiniciable."""
    RNG.seed(SEMILLA)
    mapa = fondos_por_clase()
    vistos, filas = set(), []
    intentos = 0
    while len(filas) < objetivo and intentos < objetivo * 60:
        intentos += 1
        clase, impacto, fenomeno, base = RNG.choice(PLANTILLAS)
        texto = (
            base.replace("{pb}", str(RNG.choice(PB)))
            .replace("{pct}", RNG.choice(PCT))
            .replace("{mes}", RNG.choice(MESES))
        )
        texto = RNG.choice(PREFIJOS) + texto + RNG.choice(SUFIJOS)
        clave = normaliza(texto)
        if clave in vistos:
            continue
        vistos.add(clave)
        candidatos = mapa.get(clase) or []
        fondos = ", ".join(RNG.sample(candidatos, min(2, len(candidatos)))) if candidatos else ""
        filas.append(
            dict(
                id=f"N{len(filas) + 1:04d}",
                fecha=f"2026-10-{RNG.randint(1, 8):02d}",
                fuente=RNG.choice(
                    [
                        "Nota de análisis",
                        "Prensa financiera",
                        "Comunicado oficial",
                        "Resumen de mesa",
                    ]
                ),
                clase_activo=clase,
                texto=texto,
                impacto=impacto,
                fenomeno=fenomeno,
                dificultad=DIFICULTAD[fenomeno],
                fondos_relacionados=fondos,
            )
        )
    return filas


# ---------------------------------------------------------------------------
# Cartera simulada: 150 clientes por banquero, posiciones de 5 a 20 millones.
# ---------------------------------------------------------------------------
HEROES = [
    "Clark Kent",
    "Bruce Wayne",
    "Diana Prince",
    "Barry Allen",
    "Hal Jordan",
    "Arthur Curry",
    "Victor Stone",
    "Oliver Queen",
    "Dinah Lance",
    "Kara Danvers",
    "Barbara Gordon",
    "Dick Grayson",
    "John Stewart",
    "Kate Kane",
    "Billy Batson",
    "Peter Parker",
    "Tony Stark",
    "Steve Rogers",
    "Natasha Romanoff",
    "Bruce Banner",
    "Thor Odinson",
    "Carol Danvers",
    "Stephen Strange",
    "Scott Lang",
    "Wanda Maximoff",
    "Sam Wilson",
    "Bucky Barnes",
    "Matt Murdock",
    "Jessica Jones",
    "Luke Cage",
    "Danny Rand",
    "Shuri Udaku",
    "Monica Rambeau",
    "Kamala Khan",
    "Miles Morales",
    "Jean Grey",
    "Scott Summers",
    "Ororo Munroe",
    "Logan Howlett",
    "Kurt Wagner",
    "Charles Xavier",
    "Remy LeBeau",
    "Anna Marie",
    "Hank McCoy",
    "Piotr Rasputin",
    "Reed Richards",
    "Susan Storm",
    "Johnny Storm",
    "Ben Grimm",
    "Matt Hawkins",
    "Helena Bertinelli",
    "Zatanna Zatara",
    "Jaime Reyes",
    "Cassandra Cain",
    "Ted Kord",
    "Rick Tyler",
    "Courtney Whitmore",
    "Jefferson Pierce",
    "Mari McCabe",
    "Ryan Choi",
    "Wally West",
    "Garfield Logan",
    "Rachel Roth",
    "Koriandr Anders",
    "Donna Troy",
    "Jennifer Walters",
    "Robert Reynolds",
    "Marc Spector",
    "Elektra Natchios",
    "Frank Castle",
    "Eric Brooks",
    "Jennifer Kale",
    "Adam Brashear",
    "Riri Williams",
    "Peter Quill",
]
VILLANOS = [
    "Lex Luthor",
    "Oswald Cobblepot",
    "Harvey Dent",
    "Pamela Isley",
    "Edward Nygma",
    "Victor Fries",
    "Jonathan Crane",
    "Selina Kyle",
    "Slade Wilson",
    "Sinestro",
    "Vandal Savage",
    "Ra's al Ghul",
    "Floyd Lawton",
    "Leonard Snart",
    "Eobard Thawne",
    "Black Manta",
    "Cheetah Minerva",
    "Deathstroke Grim",
    "Solomon Grundy",
    "Hugo Strange",
    "Norman Osborn",
    "Otto Octavius",
    "Wilson Fisk",
    "Erik Lehnsherr",
    "Victor Von Doom",
    "Thanos Titan",
    "Loki Laufeyson",
    "Ultron Prime",
    "Helmut Zemo",
    "Emil Blonsky",
    "Quentin Beck",
    "Adrian Toomes",
    "Max Dillon",
    "Flint Marko",
    "Cletus Kasady",
    "Eddie Brock",
    "Mystique Darkholme",
    "Sebastian Shaw",
    "Emma Frost",
    "Cain Marko",
    "Nathaniel Essex",
    "En Sabah Nur",
    "Ajax Francis",
    "Cable Summers",
    "Domino Neena",
    "Killmonger Stevens",
    "Ulysses Klaue",
    "Ronan Accuser",
    "Nebula Luphomoid",
    "Yondu Udonta",
    "Taskmaster Masters",
    "Crossbones Rumlow",
    "Baron Mordo",
    "Dormammu Faltine",
    "Kaecilius Adria",
    "Mister Sinister",
    "Arcade Gamesmith",
    "Bullseye Poindexter",
    "Typhoid Mary",
    "Purple Man",
    "Scarecrow Mason",
    "Clayface Hagen",
    "Killer Croc",
    "Harley Quinzel",
    "Poison Lily",
    "Deadshot Lawton",
    "Captain Boomerang",
    "Killer Frost",
    "Gorilla Grodd",
    "Reverse Flash",
    "Red Skull",
    "Baron Strucker",
    "Arnim Zola",
    "Madame Hydra",
    "Bulldozer Brooks",
]
PERFILES = [("Conservador", 0.34), ("Moderado", 0.43), ("Agresivo", 0.23)]
MENU_PERFIL = {
    "Conservador": ["Deuda Corto Plazo", "Deuda Mediano Plazo", "Retorno Absoluto"],
    "Moderado": [
        "Deuda Corto Plazo",
        "Deuda Mediano Plazo",
        "Deuda Largo Plazo",
        "Fondos de MultiActivos",
        "Fondos de Estrategias Pesos",
    ],
    "Agresivo": [
        "Deuda Largo Plazo",
        "Renta Variable Nacional",
        "Renta Variable Internacional",
        "Fondos de MultiActivos",
    ],
}


def construir_clientes(n=150):
    ruta = os.path.join(DATA, "catalogo_fondos.csv")
    por_cat = {}
    with open(ruta, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["publico"] != "Personas Físicas":
                continue
            if float(r["rend_1_anio"]) == 0.0:  # series sin historia
                continue
            por_cat.setdefault(r["categoria"], []).append(r)

    nombres = HEROES + VILLANOS
    RNG.shuffle(nombres)
    nombres = nombres[:n]
    perfiles = (
        [PERFILES[0][0]] * round(n * PERFILES[0][1])
        + [PERFILES[1][0]] * round(n * PERFILES[1][1])
        + [PERFILES[2][0]] * round(n * PERFILES[2][1])
    )
    perfiles = (perfiles + ["Moderado"] * n)[:n]
    RNG.shuffle(perfiles)

    filas = []
    for i, (nombre, perfil) in enumerate(zip(nombres, perfiles), start=1):
        cats = [c for c in MENU_PERFIL[perfil] if c in por_cat]
        cat = RNG.choice(cats)
        elegibles = [f for f in por_cat[cat] if int(f["minimo_inversion"]) <= 5_000_000]
        fondo = RNG.choice(elegibles or por_cat[cat])
        posicion = round(RNG.uniform(5_000_000, 20_000_000), -3)
        filas.append(
            dict(
                cliente_id=f"C{i:03d}",
                nombre=nombre,
                arquetipo="Héroe" if nombre in HEROES else "Villano",
                perfil_riesgo=perfil,
                posicion_mxn=int(posicion),
                fondo_actual=fondo["fondo"],
                serie_actual=fondo["serie"],
                categoria_actual=fondo["categoria"],
                rend_1_anio_actual=float(fondo["rend_1_anio"]),
                clase_activo=CATEGORIA_A_CLASE.get(fondo["categoria"], "Deuda Corto Plazo"),
                meses_sin_revision=RNG.randint(0, 11),
            )
        )
    return filas


def escribir(nombre, filas, output_dir):
    ruta = Path(output_dir) / nombre
    if ruta.resolve().parent == Path(DATA).resolve():
        raise ValueError("data/ es evidencia congelada; usa otra carpeta")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    return ruta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", default="scratch/generated")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    notas = construir_notas(400)
    escribir("notas_mercado.csv", notas, args.output_dir)
    logging.info(f"notas_mercado.csv        {len(notas)} registros")
    for etiqueta in ("POSITIVO", "NEUTRAL", "NEGATIVO"):
        n = sum(1 for f in notas if f["impacto"] == etiqueta)
        logging.info(f"   {etiqueta:9s} {n:4d}  ({100 * n / len(notas):4.1f} %)")
    for d in ("facil", "media", "dificil"):
        n = sum(1 for f in notas if f["dificultad"] == d)
        logging.info(f"   dificultad {d:8s} {n:4d}  ({100 * n / len(notas):4.1f} %)")

    clientes = construir_clientes(150)
    escribir("clientes_simulados.csv", clientes, args.output_dir)
    total = sum(c["posicion_mxn"] for c in clientes)
    logging.info(
        f"\nclientes_simulados.csv   {len(clientes)} clientes · "
        f"AUM simulado ${total:,.0f} MXN · ticket promedio ${total / len(clientes):,.0f}"
    )


if __name__ == "__main__":
    main()
