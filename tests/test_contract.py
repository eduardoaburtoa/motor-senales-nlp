"""Pruebas de límites, abstención y preservación; sin ejecutar modelos."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evaluate import curva_umbral, metricas, normaliza_etiqueta
from verify_integrity import verify


class ContractTests(unittest.TestCase):
    def test_frozen(self):
        self.assertEqual(verify(), 13)

    def test_abstention(self):
        row = curva_umbral(["NEGATIVO"], ["POSITIVO"], [0.5], [0.9])[0]
        self.assertEqual(row["cobertura_pct"], 0)
        self.assertIsNone(row["exactitud_aceptadas_pct"])

    def test_perfect(self):
        labels = ["NEGATIVO", "NEUTRAL", "POSITIVO"]
        self.assertEqual(metricas(labels, labels)["f1_macro"], 1)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            metricas([], [])
        with self.assertRaises(ValueError):
            curva_umbral(["NEUTRAL"], ["NEUTRAL"], [float("nan")])
        with self.assertRaises(KeyError):
            normaliza_etiqueta("desconocida")
