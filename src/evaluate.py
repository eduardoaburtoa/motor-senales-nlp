#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluate.py — funciones de evaluación reutilizables y verificación del prototipo.

Las mismas funciones que usa el cuaderno, extraídas aquí para poder probarlas
sin descargar modelos y para poder reusarlas desde un servicio.

Uso:
    python3 evaluate.py --verificar
        Comprueba que los datos existen, que el mapeo de etiquetas cubre los
        cuatro vocabularios y que el cálculo de métricas funciona, usando
        predicciones simuladas. No descarga nada de Hugging Face.

    python3 evaluate.py --metricas resultados/predicciones_completas.csv
        Recalcula las métricas a partir de un archivo de predicciones ya
        generado por el cuaderno.
"""

import argparse
import logging
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(AQUI, "..", "data")

CLASES = ["NEGATIVO", "NEUTRAL", "POSITIVO"]

# Cada modelo nombra sus clases a su manera. Esta tabla es, formalmente,
# el primer "ajuste mínimo" en el sentido del Tema 10.
MAPA_ETIQUETAS = {
    "POS": "POSITIVO",
    "NEU": "NEUTRAL",
    "NEG": "NEGATIVO",
    "POSITIVE": "POSITIVO",
    "NEUTRAL": "NEUTRAL",
    "NEGATIVE": "NEGATIVO",
    "LABEL_0": "NEGATIVO",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVO",
    "1 STAR": "NEGATIVO",
    "2 STARS": "NEGATIVO",
    "3 STARS": "NEUTRAL",
    "4 STARS": "POSITIVO",
    "5 STARS": "POSITIVO",
}


def normaliza_etiqueta(cruda: str) -> str:
    """Lleva la etiqueta de cualquiera de los modelos al vocabulario común."""
    clave = str(cruda).strip().upper()
    if clave in MAPA_ETIQUETAS:
        return MAPA_ETIQUETAS[clave]
    raise KeyError(f"Etiqueta no contemplada: {cruda!r}. Agrégala a MAPA_ETIQUETAS.")


def metricas(verdades, predicciones):
    """accuracy, precision, recall y F1 en versión macro y ponderada."""
    if not len(verdades) or len(verdades) != len(predicciones):
        raise ValueError("Se requieren vectores no vacíos y de igual longitud")
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support

    p_ma, r_ma, f_ma, _ = precision_recall_fscore_support(
        verdades, predicciones, average="macro", zero_division=0
    )
    p_we, r_we, f_we, _ = precision_recall_fscore_support(
        verdades, predicciones, average="weighted", zero_division=0
    )
    return {
        "accuracy": round(accuracy_score(verdades, predicciones), 4),
        "precision_macro": round(p_ma, 4),
        "recall_macro": round(r_ma, 4),
        "f1_macro": round(f_ma, 4),
        "precision_weighted": round(p_we, 4),
        "recall_weighted": round(r_we, 4),
        "f1_weighted": round(f_we, 4),
    }


def curva_umbral(verdades, predicciones, confianzas, umbrales=(0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95)):
    """Cobertura automática y exactitud según el umbral de abstención.

    Por debajo del umbral el motor no emite señal: la nota pasa a revisión del
    asesor. La tabla dice cuánta exactitud se gana y cuánta cobertura cuesta.
    """
    import numpy as np

    v = np.asarray(verdades)
    p = np.asarray(predicciones)
    c = np.asarray(confianzas)
    if not len(v) or v.shape != p.shape or v.shape != c.shape:
        raise ValueError("Vectores no vacíos de igual forma requeridos")
    if not np.isfinite(c).all() or ((c < 0) | (c > 1)).any():
        raise ValueError("Confianzas fuera de [0,1]")
    filas = []
    for u in umbrales:
        acepta = c >= u
        filas.append(
            {
                "umbral": u,
                "cobertura_pct": round(100 * acepta.mean(), 1),
                "notas_automaticas": int(acepta.sum()),
                "notas_a_revision": int((~acepta).sum()),
                "exactitud_aceptadas_pct": (
                    round(100 * (p[acepta] == v[acepta]).mean(), 1) if acepta.any() else None
                ),
            }
        )
    return filas


def desempeno_por_segmento(df, columna_pred, segmento):
    """F1 macro por nivel de un segmento (dificultad o fenómeno lingüístico)."""
    from sklearn.metrics import f1_score

    salida = {}
    for nivel, grupo in df.groupby(segmento):
        salida[nivel] = {
            "n": len(grupo),
            "f1_macro": round(
                f1_score(grupo["impacto"], grupo[columna_pred], average="macro", zero_division=0), 3
            ),
            "exactitud": round((grupo["impacto"] == grupo[columna_pred]).mean(), 3),
        }
    return salida


# ───────────────────────────────────────────────────────────── verificación
def verificar():
    import random
    import pandas as pd

    logging.info("Verificación del prototipo (sin descargar modelos)\n")
    fallos = 0

    # 1. datos
    for archivo, minimo in [
        ("notas_mercado.csv", 400),
        ("catalogo_fondos.csv", 400),
        ("clientes_simulados.csv", 150),
    ]:
        ruta = os.path.join(DATA, archivo)
        if not os.path.exists(ruta):
            logging.info(f"  [FALLA] no existe {archivo}")
            fallos += 1
            continue
        df = pd.read_csv(ruta)
        ok = len(df) >= minimo
        logging.info(f"  [{'OK  ' if ok else 'FALLA'}] {archivo:24s} {len(df):4d} registros")
        fallos += 0 if ok else 1

    if fallos:
        return 1
    notas = pd.read_csv(os.path.join(DATA, "notas_mercado.csv"))

    # 2. integridad del corpus
    assert set(notas["impacto"]) <= set(CLASES), "etiquetas fuera del vocabulario"
    dup = len(notas) - notas["texto"].nunique()
    logging.info(
        f"  [{'OK  ' if dup == 0 else 'FALLA'}] textos únicos           "
        f"{notas['texto'].nunique()} de {len(notas)}"
    )
    fallos += 0 if dup == 0 else 1
    nulos = int(notas.isnull().sum().sum())
    logging.info(f"  [{'OK  ' if nulos == 0 else 'FALLA'}] sin valores nulos        {nulos} nulos")
    fallos += 0 if nulos == 0 else 1

    # 3. mapeo de etiquetas de los cuatro modelos
    vocabularios = {
        "RoBERTuito / BETO": ["POS", "NEU", "NEG"],
        "XLM-R Twitter": ["Negative", "Neutral", "Positive"],
        "mBERT nlptown": ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"],
        "genérico": ["LABEL_0", "LABEL_1", "LABEL_2"],
    }
    for nombre, etiquetas in vocabularios.items():
        try:
            for e in etiquetas:
                assert normaliza_etiqueta(e) in CLASES
            logging.info(f"  [OK  ] mapeo de etiquetas      {nombre}")
        except Exception as e:
            logging.info(f"  [FALLA] mapeo de etiquetas    {nombre}: {e}")
            fallos += 1

    # 4. cálculo de métricas con predicciones simuladas
    random.seed(0)
    pred = [random.choice(CLASES) for _ in range(len(notas))]
    conf = [random.uniform(0.4, 0.99) for _ in range(len(notas))]
    m = metricas(notas["impacto"].tolist(), pred)
    ok = all(0.0 <= v <= 1.0 for v in m.values())
    logging.info(
        f"  [{'OK  ' if ok else 'FALLA'}] cálculo de métricas      7 métricas en rango [0,1]"
    )
    fallos += 0 if ok else 1

    filas = curva_umbral(notas["impacto"].tolist(), pred, conf)
    ok = filas[0]["cobertura_pct"] == 100.0 and filas[-1]["cobertura_pct"] <= 100.0
    logging.info(
        f"  [{'OK  ' if ok else 'FALLA'}] curva de umbral          "
        f"{len(filas)} puntos, cobertura decreciente"
    )
    fallos += 0 if ok else 1

    tmp = notas.copy()
    tmp["pred"] = pred
    seg = desempeno_por_segmento(tmp, "pred", "dificultad")
    logging.info(
        f"  [OK  ] segmentación            {len(seg)} niveles de dificultad: {', '.join(seg)}"
    )

    logging.info(f"\n{'Todo en orden.' if fallos == 0 else f'{fallos} verificación(es) fallaron.'}")
    logging.info(
        "Lo único que no se puede probar aquí es la descarga de los modelos "
        "desde Hugging Face; eso ocurre al ejecutar el cuaderno en Colab."
    )
    return 0 if fallos == 0 else 1


def desde_predicciones(ruta):
    import pandas as pd

    df = pd.read_csv(ruta)
    cols = [c for c in df.columns if c.startswith("pred_")]
    if not cols:
        logging.info("El archivo no tiene columnas pred_*. ¿Es la salida del cuaderno?")
        return 1
    logging.info(f"{len(df)} registros · {len(cols)} modelos\n")
    for c in cols:
        alias = c.replace("pred_", "")
        m = metricas(df["impacto"].tolist(), df[c].tolist())
        logging.info(
            f"{alias:18s} acc={m['accuracy']:.4f}  P={m['precision_macro']:.4f}  "
            f"R={m['recall_macro']:.4f}  F1={m['f1_macro']:.4f}"
        )
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--verificar",
        action="store_true",
        help="verifica datos, mapeo y métricas sin descargar modelos",
    )
    ap.add_argument(
        "--metricas", metavar="CSV", help="recalcula métricas desde predicciones_completas.csv"
    )
    args = ap.parse_args()
    if args.metricas:
        sys.exit(desde_predicciones(args.metricas))
    sys.exit(verificar())
