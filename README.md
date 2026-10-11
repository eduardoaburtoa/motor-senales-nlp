<p align="center"><img src="docs/vertice_logo.png" width="135" alt="Vértice AI Consulting"></p>

# Asistente de preparación de revisiones de portafolio

**Actividad 4 · Módulo 2 / Semana 5 · Temas 9 y 10**  
Eduardo Aburto Angulo · Universidad Tecmilenio

Desde mi enfoque de Banquero Patrimonial Sr., comparo cuatro modelos de Hugging Face para organizar notas de mercado que ayuden a preparar revisiones de portafolio. Mi prioridad es el beneficio neto del cliente y el respeto a su perfil, horizonte y liquidez. El prototipo es académico: no emite órdenes ni representa un producto autorizado de BBVA.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eduardoaburtoa/motor-senales-nlp/blob/main/notebooks/01_comparacion_modelos_hf.ipynb)

## Entregables

- [Notebook corregido y reejecutable](notebooks/01_comparacion_modelos_hf.ipynb).
- [Evidencia original ejecutada en GPU T4](notebooks/evidencia/colab_t4_original.ipynb), con código y salidas de texto originales; copia ligera sin widgets ni gráficos incrustados.
- [Reporte en Word](docs/Actividad4_Eduardo_Aburto.docx).
- [CSV de evaluación](data/notas_mercado.csv), [cartera simulada corregida](data/clientes_simulados.csv) y [Excel original como referencia](docs/originales/dataset_original.xlsx).
- [Resultados y trazabilidad](results/README.md).
- [Diccionario y origen de datos](data/README.md).

## Resultado y decisión

| Modelo | Accuracy | Precision macro | Recall macro | F1 macro | ms/nota en lote |
|---|---:|---:|---:|---:|---:|
| XLM-R Twitter | 0.5500 | 0.6857 | 0.6184 | **0.5544** | 3.02 |
| BETO | 0.4700 | 0.7214 | 0.5434 | 0.4719 | 6.31 |
| mBERT nlptown | 0.4750 | 0.4597 | 0.4566 | 0.4515 | 3.04 |
| RoBERTuito | 0.4050 | 0.7086 | 0.4942 | 0.3547 | 2.98 |

Son mediciones de las salidas del notebook ejecutado aportado por el autor, sobre 400 notas sintéticas. No son cifras inventadas ni una nueva corrida de la versión corregida. XLM-R es la base experimental recomendada, **no un candidato aprobado para producción**. Ningún umbral ensayado cumple exactitud >90% y cobertura ≥70%. Todas las notas requieren revisión humana. En negaciones, XLM-R acierta 40.5% y nlptown 52.7%; ambos quedan por debajo del objetivo de 85%.

## Ecosistema Hugging Face

- **Models:** pesos, configuración, tokenizador y tarjeta de cada candidato.
- **Datasets:** infraestructura para cargar y versionar conjuntos de datos; este proyecto usa un CSV sintético propio, no un dataset publicado en el Hub.
- **Spaces:** alojamiento de demostraciones. No se ha desplegado un Space; Colab es el entorno de prototipado.

## Ejecución en Google Colab

1. Abrir el botón de Colab y guardar una copia en Drive.
2. Seleccionar **Entorno de ejecución → Cambiar tipo de entorno → GPU T4**.
3. Ejecutar de arriba hacia abajo en un entorno nuevo. La verificación se detiene si no hay GPU.
4. Instalar dependencias de la celda inicial. Si Colab solicita reinicio, reiniciar y continuar desde arriba.
5. Autenticación opcional: guardar un token de lectura en **Secretos → HF_TOKEN**. Nunca escribirlo en el notebook ni en GitHub. Los checkpoints públicos permiten ejecución anónima; el token puede mejorar los límites de descarga.
6. El corpus se busca localmente, en este repositorio y, como respaldo, en una copia comprimida incrustada con SHA-256. Se validan columnas, 400 textos únicos y distribución de clases.
7. Ejecutar inferencia, métricas, análisis de errores y exportación. `results/` incluirá las predicciones individuales de la nueva corrida y las revisiones resueltas. Descargar esa carpeta antes de cerrar el entorno temporal.

La evidencia aportada usa Python 3.13.15, PyTorch 2.11.0+cu130, transformers 5.18.0, huggingface_hub 1.33.0, scikit-learn 1.6.1 y pandas 2.2.3. Se fijan las bibliotecas principales observadas; se conserva PyTorch CUDA suministrado por Colab y se registra su versión. El notebook corregido fija revisiones de pesos verificadas para futuras corridas. Las revisiones de la corrida original no fueron registradas, por lo que no prometo reproducción bit a bit de sus resultados.

## Verificación local y regeneración

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/validate.py
python src/build_dataset.py
```

La validación no descarga modelos ni fabrica predicciones: comprueba la reproducción exacta del corpus y clientes, métricas sobre casos conocidos, abstención sin aceptados, cobertura de fichas y reglas económicas. Para inferencia local se necesita instalar PyTorch adecuado a su equipo; la actividad se mide en Colab GPU.

Para reconstruir el catálogo desde el PDF proporcionado del 8 de octubre:

```bash
pdftotext -layout "Hoja de rendimientos 8 de octubre.pdf" anaquel.txt
python src/parse_anaquel.py anaquel.txt data/catalogo_fondos.csv
```

Se comprobó que la extracción produce 484 registros. El enlace público diario cambia: conservar el PDF fechado y su huella, no reemplazar silenciosamente el corte histórico por el último.

## Datos y comisiones

- 400 notas de 60 plantillas con variantes; 158 POSITIVO, 158 NEGATIVO y 84 NEUTRAL. Etiquetas sintéticas que requieren validación de expertos.
- 150 clientes ficticios, superhéroes y villanos, con posiciones de MXN 5–20 millones. AUM simulado: **MXN 1,831,243,000**. Los personajes permiten personalidades didácticas sin usar carteras reales.
- 484 registros de 59 fondos del anaquel. No confundir filas con instrumentos únicos ni mezclar cotizaciones en distintas monedas.
- Se consultaron **61 DICI**, cubriendo los 59 fondos del anaquel, el 11 de octubre de 2026. [Índice con enlaces y huellas](data/fichas_bbva.csv) y [693 registros de gastos por serie](data/comisiones_por_serie.csv). Son extracción documental; debe validarse vigencia, periodicidad y serie antes de utilizarlos comercialmente.

El **1% por venta + 1% por compra** es un supuesto didáctico, no una tarifa general de BBVA. Los gastos del fondo no equivalen íntegramente a ingreso del banco. Si el rendimiento es neto de gastos, restarlos otra vez duplica costos. La capa `src/portfolio_rules.py` exige perfil y liquidez compatibles, límite de rotaciones y beneficio neto del escenario positivo; jamás autoriza órdenes. Una brecha histórica de 3pp multiplicada por persistencia supuesta de 35% da 1.05pp: no cubre el costo de 2% y se bloquea. Los rendimientos pasados no garantizan resultados futuros.

## Método y límites

Lote de 32, truncamiento a 256 tokens, calentamiento de 8 notas, sincronización CUDA y latencia individual sobre 30 notas. Una sola corrida, sin intervalos de variabilidad ni pico de VRAM medido. Carga del modelo y latencia de inferencia se reportan separadas.

Los modelos solo reciben `texto`; no incorporan la clase de activo como entrada independiente ni el perfil. Sentimiento general es una aproximación insuficiente al impacto financiero. Para nlptown se mapea la estrella top-1 a tres clases: su confianza no equivale a sumar probabilidades por clase. Se conserva ese método porque es el medido.

La curva de umbral usa el mismo corpus de comparación y no constituye validación externa. La comparación con/sin prefijo es observacional, no una ablación. Una fase posterior debe separar por plantilla los conjuntos de validación y prueba, incorporar notas autorizadas y medir acuerdo entre especialistas. No se concluye que 400 textos únicos sean 400 escenarios independientes.

## Licencias y mantenimiento

| Checkpoint | Condición verificada en tarjeta |
|---|---|
| pysentimiento/robertuito-sentiment-analysis | Sin licencia permisiva declarada en la tarjeta consultada; revisar derechos de pesos/datos |
| finiteautomata/beto-sentiment-analysis | Uso científico no comercial; aviso de próximo retiro |
| cardiffnlp/twitter-xlm-roberta-base-sentiment | Sin licencia declarada en la tarjeta consultada |
| nlptown/bert-base-multilingual-uncased-sentiment | MIT |

No se redistribuyen pesos. Los permisos de este trabajo no sustituyen los de los modelos, textos o marcas de terceros. Revisión trimestral propuesta: notas nuevas, errores por clase/activo, versiones y disponibilidad; caída >5 puntos de F1 dispara investigación. No actualizar pesos silenciosamente. Acceso público no equivale a permiso comercial.

## Estructura

```text
data/        CSV, Excel, diccionarios, fichas y comisiones
notebooks/   notebook corregido y evidencia original
results/     métricas, gráficos, condiciones y ejemplos económicos
src/         generación, extracción, evaluación y validación
docs/        reporte, identidad y registro de revisión
```

La inteligencia artificial no sustituye el criterio del banquero; lo aumenta.
