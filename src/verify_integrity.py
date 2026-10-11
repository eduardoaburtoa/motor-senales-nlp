"""Verifica la evidencia histórica sin escribir ni ejecutar los artefactos."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify(root: Path = ROOT) -> int:
    """Falla ante cambios de tamaño, contenido o archivos faltantes."""
    manifest = json.loads((root / "integrity.json").read_text())
    for name, expected in manifest.items():
        content = (root / name).read_bytes()
        if (
            len(content) != expected["bytes"]
            or hashlib.sha256(content).hexdigest() != expected["sha256"]
        ):
            raise ValueError(f"Evidencia alterada: {name}")
    results = {p.name for p in (root / "results").iterdir() if p.is_file()}
    expected_results = {Path(p).name for p in manifest if p.startswith("results/")} | {"README.md"}
    if results != expected_results:
        raise ValueError("results/ debe contener exactamente sus ocho archivos")
    return len(manifest)


if __name__ == "__main__":
    print(f"Integridad verificada: {verify()} archivos congelados; results/: 8 archivos.")
