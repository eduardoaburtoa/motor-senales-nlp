# results/ — Salidas de la corrida

Todo lo que hay en esta carpeta lo escribió el cuaderno
`notebooks/01_comparacion_modelos_hf.ipynb` en una sola ejecución, el **9 de
octubre de 2026**, sobre GPU **NVIDIA Tesla T4 (15.6 GB)** en Google Colab.

Nada de aquí se escribió a mano ni se tomó de la tarjeta de un modelo. Si una
cifra del reporte no se puede reconstruir desde estos archivos, es un error del
reporte y hay que corregirlo. Esa es la razón de que la carpeta esté versionada
en lugar de ignorada.

La corrida que las produjo está completa, con sus veinte salidas y cero errores,
en `notebooks/01_comparacion_modelos_hf_EJECUTADO.ipynb`.

---

## Qué hay en cada archivo

| Archivo | Qué contiene | De dónde sale |
|---|---|---|
| `tabla_comparativa.csv` | Una fila por modelo con familia, arquitectura, parámetros, licencia, accuracy, precision / recall / F1 macro, dos medidas de latencia, rendimiento y tiempo de carga | Celda 8 |
| `metricas_por_clase.csv` | Las 12 combinaciones modelo × clase con precision, recall, F1 y soporte | Celda 9 |
| `desempeno_por_dificultad.csv` | F1 por nivel de dificultad y exactitud en los subconjuntos de negación y contraste | Celda 10 |
| `curva_umbral.csv` | Siete umbrales de confianza con su cobertura automática y su exactitud sobre las notas aceptadas | Celda 11 |
| `condiciones_ejecucion.json` | GPU, versiones de biblioteca, fecha, semilla del corpus, sha256 del CSV y modelo recomendado | Celda 12 |
| `matrices_confusion.png` | Figura 1 del reporte: las cuatro matrices 3 × 3, ordenadas por F1 macro | Celda 9 |
| `tradeoff_precision_latencia.png` | Figura 2 del reporte: F1 macro contra latencia, y F1 macro contra accuracy | Celda 10 |

---

## Cómo leer los dos números que mandan

**F1-score macro** es el criterio de decisión, no la exactitud. El corpus está
desbalanceado (158 NEGATIVO, 158 POSITIVO, 84 NEUTRAL), así que un modelo que se
apoye en una clase mayoritaria puede verse decente en *accuracy* y ser inútil en
la mesa. El F1 macro promedia las tres clases con el mismo peso y obliga al
modelo a responder por todas.

**La cobertura a cada umbral** dice cuántas notas podría clasificar el motor sin
intervención humana. La exactitud asociada dice qué tan bien lo haría sobre ese
subconjunto. Las dos se leen juntas o no se leen: 77.7 % de exactitud suena bien
hasta que uno ve que es sobre el 34.8 % de las notas.

---

## Resumen de lo que dicen

| | |
|---|---|
| Modelo con mejor F1 macro | `cardiffnlp/twitter-xlm-roberta-base-sentiment` · 0.5544 |
| Segundo lugar | `finiteautomata/beto-sentiment-analysis` · 0.4719 |
| Línea base del azar (tres clases) | ≈ 0.333 |
| Mejor punto de operación | Umbral 0.70 → 77.7 % de exactitud sobre 34.8 % de cobertura |
| Exactitud en notas con negación | 40.5 % (30 aciertos de 74) |
| Umbrales de operación cumplidos | 2 de 5 — **U2, U3 y U4 no se cumplen** |

La conclusión operativa, desarrollada en el reporte: ningún modelo preentrenado
sin *fine-tuning* califica hoy para emitir señales automáticas en este caso de
uso. El prototipo arranca en modo asistido, priorizando la lectura del día para
el asesor, y la emisión automática queda condicionada a un modelo ajustado sobre
corpus etiquetado por varias personas de la mesa.

---

## Reproducibilidad

El corpus se genera con semilla `20261008` y el cuaderno verifica su huella
`sha256` (`cfde77a9fc80add4…`) antes de usarlo, además de comprobar que trae los
400 registros, las nueve columnas y el reparto 158 / 158 / 84. Si algo no
coincide, la celda 4b levanta un error y detiene la corrida.

Ese control no es decorativo. Lo agregué después de que una herramienta de apoyo
sustituyera el corpus por uno inventado de siete frases repetidas: el reporte
habría salido con un desempeño mejor que el real y yo no me habría enterado.

Correr de nuevo el cuaderno en otra GPU debería reproducir las métricas y mover
las latencias, que dependen del hardware. Si cambian las métricas, lo primero que
hay que revisar es la versión de `transformers`: el mapeo de etiquetas de los
cuatro modelos está fijado en la celda 5 y es lo único que podría desalinearse.

---

Eduardo Aburto Angulo · AL07182743 · Universidad Tecmilenio
Gestión de Proyectos de Inteligencia Artificial · Actividad 4

## Integridad

Esta carpeta conserva exactamente ocho archivos: este README y siete salidas históricas. Ejecuta `python src/verify_integrity.py` desde la raíz para comprobar sus hashes sin regenerarlos.
