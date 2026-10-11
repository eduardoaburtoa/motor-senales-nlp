# Motor de señales · Comparación de modelos preentrenados de Hugging Face

Clasificación del impacto de notas de mercado en español para la capa de lectura
de mercado de un motor de señales de rotación de fondos de inversión.

**Actividad 4 — Gestión de Proyectos de Inteligencia Artificial**
Universidad Tecmilenio · Módulo 2 / Semana 5 (Temas 9 y 10)

| | |
|---|---|
| **Autor** | Eduardo Aburto Angulo |
| **Matrícula** | AL07182743 |
| **Rol** | Banquero Patrimonial Sr., BBVA México · plaza Xalapa |
| **Docente** | M. en C. Luis Ariel Vázquez Piña |
| **Fecha** | 9 de octubre de 2026 |

---

## Arranque rápido y preservación de evidencia

[![Verificación](https://github.com/eduardoaburtoa/motor-senales-nlp/actions/workflows/verify.yml/badge.svg)](https://github.com/eduardoaburtoa/motor-senales-nlp/actions/workflows/verify.yml)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make test
```

Estas comprobaciones no descargan modelos, no ejecutan el notebook histórico y
no escriben en `data/` ni en `results/`. `integrity.json` registra los SHA-256
completos de los 13 archivos congelados del ZIP entregado por el autor.

Para una nueva medición, abre únicamente el [cuaderno limpio en Colab](https://colab.research.google.com/github/eduardoaburtoa/motor-senales-nlp/blob/main/notebooks/01_comparacion_modelos_hf.ipynb),
selecciona una GPU y ejecuta sus celdas en orden. Sus nuevas salidas son otra corrida;
no sustituyas con ellas los archivos históricos. La celda 4b valida el corpus.

La licencia MIT de este repositorio cubre el código propio. No relicencia modelos,
marcas, plantillas institucionales ni materiales de terceros. Las licencias de
modelos que aparecen abajo se conservan como declaraciones del material recibido;
su autorización de uso comercial requiere confirmación en la fuente original.
Consulta [las notas de revisión](docs/REVISION_TECNICA.md).

## 1. Descripción del proyecto

Un banquero patrimonial atiende alrededor de 150 clientes con posiciones de cinco
a veinte millones de pesos repartidas en fondos de inversión. Todos los días
llegan a la mesa notas de análisis y titulares de prensa financiera, pero esa
información llega de forma desigual: el asesor que alcanzó a leer la nota
reacciona y el que estaba en cita, no. La misma oportunidad le llega a unos
clientes y a otros no, y no por criterio de asesoría sino por la agenda del
asesor.

Este repositorio contiene el prototipo de la **primera capa** de un motor que
busca cerrar ese hueco: un clasificador que lee cada nota de mercado y determina
si su impacto sobre una clase de activo es **POSITIVO**, **NEUTRAL** o
**NEGATIVO**. La señal resultante se cruza después con el anaquel de rendimientos
y con el umbral de costo del 2 % de corretaje antes de proponer cualquier
movimiento. El motor nunca ejecuta órdenes: el asesor revisa y firma.

**Lo que se compara:** cuatro modelos preentrenados de Hugging Face, dos
especializados en español y dos multilingües, evaluados sobre un corpus propio de
400 notas con `accuracy`, `precision`, `recall`, `F1-score` y latencia.

| Modelo | Familia | Parámetros | Licencia |
|---|---|---|---|
| `pysentimiento/robertuito-sentiment-analysis` | Español específico | ≈109 M | Apache-2.0 |
| `finiteautomata/beto-sentiment-analysis` | Español específico | ≈110 M | Apache-2.0 |
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Multilingüe | ≈278 M | MIT |
| `nlptown/bert-base-multilingual-uncased-sentiment` | Multilingüe | ≈167 M | MIT |

### Por qué un dataset propio

El Tema 9 lo plantea sin rodeos: las métricas que publica un modelo se calculan
sobre conjuntos de datos estándar que no representan el caso de uso. Un modelo
entrenado con reseñas de restaurantes puede tener 92 % de exactitud publicada y
fallar en *«la prima por plazo no se comprimió»*. Esa frase no se parece a nada de
su entrenamiento, y es exactamente el tipo de frase que el motor va a leer todos
los días.

---

## 2. Entorno de ejecución

Estas son las versiones **de la corrida que se reporta** (9 de octubre de 2026),
tal como el propio cuaderno las registró en `results/condiciones_ejecucion.json`:

| Componente | Versión en la corrida |
|---|---|
| Plataforma | Google Colab con **GPU NVIDIA Tesla T4 (15.6 GB)** |
| Python | 3.13.15 |
| PyTorch | 2.11.0+cu130 |
| transformers | 5.18.0 |
| huggingface_hub | 1.33.0 |
| scikit-learn | 1.6.1 |
| pandas | 2.2.3 |

El cuaderno tolera tanto `transformers` 4.x como 5.x: detecta en qué versión
corre y ajusta la forma de llamar al *pipeline*. `requirements.txt` fija los
mínimos, no las versiones exactas, para que siga corriendo en un Colab que se
actualiza solo.

Los cuatro modelos son **públicos y de acceso abierto**: el cuaderno corre sin
token de Hugging Face. La autenticación está incluida y documentada porque el
Tema 10 la requiere y porque en un despliegue real dentro del banco sí haría
falta, para trazabilidad y para consumir artefactos de un Hub privado.

Toda la corrida cabe en una sola GPU T4. El costo del prototipo no lo determina
el modelo que se elija, sino el volumen de inferencia.

---

## 3. Pasos de ejecución

### Opción A — Google Colab (la recomendada; es lo que pide la actividad)

1. Abrir `notebooks/01_comparacion_modelos_hf.ipynb` en Google Colab.
2. Menú **Entorno de ejecución → Cambiar tipo de entorno de ejecución →
   Acelerador por hardware: GPU (T4)**.
3. En la celda 4, ajustar `USUARIO_GITHUB` al usuario donde esté publicado este
   repositorio. Si se deja sin cambiar, el cuaderno pide el archivo por el
   selector de subida: también funciona.
4. **Entorno de ejecución → Ejecutar todas.** Tarda entre 8 y 12 minutos.
5. Los resultados quedan en `resultados/` dentro de la sesión de Colab y se
   imprimen al final en formato de tabla, listos para copiar al reporte.

### Opción B — Regenerar los datos desde cero

```bash
git clone https://github.com/<usuario>/motor-senales-nlp.git
cd motor-senales-nlp
pip install -r requirements.txt

# 1. Catálogo real de fondos, a partir del PDF público de BBVA
pdftotext -layout "Hoja de rendimientos 8 de octubre.pdf" anaquel.txt
python3 src/parse_anaquel.py anaquel.txt data/catalogo_fondos.csv

# 2. Corpus etiquetado y cartera simulada (deterministas, semilla 20261008)
python3 src/build_dataset.py

# 3. Verificar que el cuaderno es ejecutable sin descargar modelos
python3 src/evaluate.py --verificar
```

---

## 4. Estructura del repositorio

```
motor-senales-nlp/
├── README.md                     Este archivo
├── requirements.txt              Dependencias con versión mínima
├── .gitignore
├── data/
│   ├── README.md                 Diccionario de datos y origen de cada archivo
│   ├── catalogo_fondos.csv       484 series · 59 fondos · REAL (BBVA, 08/10/2026)
│   ├── notas_mercado.csv         400 notas etiquetadas · SINTÉTICO declarado
│   └── clientes_simulados.csv    150 clientes · SINTÉTICO declarado
├── notebooks/
│   ├── 01_comparacion_modelos_hf.ipynb            Versión limpia, para re-ejecutar
│   └── 01_comparacion_modelos_hf_EJECUTADO.ipynb  La corrida que se reporta, con salidas
├── src/
│   ├── parse_anaquel.py          PDF de BBVA → CSV estructurado
│   ├── build_dataset.py          Genera el corpus y la cartera
│   └── evaluate.py               Métricas y validación reutilizables
├── results/                      Las siete salidas de la corrida del 09/10/2026
│   ├── tabla_comparativa.csv           Las 13 columnas de los 4 modelos
│   ├── metricas_por_clase.csv          Precision, recall y F1 de las 12 combinaciones
│   ├── desempeno_por_dificultad.csv    F1 por nivel y exactitud en negación y contraste
│   ├── curva_umbral.csv                Cobertura y exactitud en 7 umbrales
│   ├── condiciones_ejecucion.json      GPU, versiones, semilla y sha256 del corpus
│   ├── matrices_confusion.png          Figura 1 del reporte
│   └── tradeoff_precision_latencia.png Figura 2 del reporte
└── docs/
    ├── analisis_comparativo.docx Reporte técnico comparativo (14 tablas, 2 figuras)
    └── vertice_logo.png
```

---

## 5. Datos: qué es real y qué es simulado

Esta distinción es deliberada y conviene decirla de frente.

**Real.** Los nombres de los fondos, sus categorías, calificaciones, inversiones
mínimas y rendimientos provienen del *Anaquel con Rendimientos Históricos* que
BBVA México publica todos los días; se usó la edición del **8 de octubre de
2026**. Ninguna cifra de rendimiento fue estimada ni inventada.

**Sintético y declarado.** Las notas de mercado y la cartera de clientes. Las
notas de análisis de la mesa son material propietario y no pueden publicarse en
un repositorio académico; las carteras reales son datos personales y financieros
protegidos por la LFPDPPP. Para fines didácticos y por privacidad de los datos
usamos nombres de superhéroes y villanos, ya que les puedo simular
características individuales relacionadas con la ficción para poder comprobar la
lógica de los resultados.

Los generadores son **deterministas**: con la semilla `20261008` reproducen
exactamente el mismo corpus.

---

## 6. Resultados de la corrida

Una sola corrida, el 9 de octubre de 2026, GPU Tesla T4, las 400 notas completas.
Ninguna cifra de aquí proviene de la tarjeta de un modelo: todas salen de
`results/`, y el cuaderno ejecutado con sus 20 salidas está en `notebooks/`.

| Modelo | Familia | Params | F1 macro | Accuracy | ms/nota | notas/s |
|---|---|---:|---:|---:|---:|---:|
| **cardiffnlp/twitter-xlm-roberta-base-sentiment** | Multilingüe | 278.0 M | **0.5544** | 0.550 | 3.02 | 331 |
| finiteautomata/beto-sentiment-analysis | Español | 109.9 M | 0.4719 | 0.470 | 6.31 | 159 |
| nlptown/bert-base-multilingual-uncased-sentiment | Multilingüe | 167.4 M | 0.4515 | 0.475 | 3.04 | 329 |
| pysentimiento/robertuito-sentiment-analysis | Español | 108.8 M | 0.3547 | 0.405 | 2.98 | 335 |

### Los tres hallazgos

**1. La hipótesis se refutó.** Dejé escrito antes de medir que esperaba ganar con
un modelo entrenado en español. Ganó un multilingüe, por 8.3 puntos de F1 macro,
y el último lugar también fue un modelo en español. El cuello de botella aquí no
es el idioma sino el dominio: los cuatro aprendieron de tuits y reseñas, y el
registro de una mesa de dinero les resulta ajeno por igual.

**2. La degradación de dominio es grande.** 0.5544 de F1 macro sobre tres clases,
cuando elegir al azar daría 0.333. Los tres modelos de sentimiento colapsan hacia
NEUTRAL en cuanto leen lenguaje financiero formal —recall de 0.988, 0.976 y 0.940
en esa clase— y RoBERTuito acertó **una sola** de las 158 notas positivas. Es
exactamente el riesgo R-01 que había declarado en el reporte antes de correr nada.

**3. El punto de operación que exigí no existe.** Había fijado que el motor solo
emitiría señales si cubría ≥ 70 % de las notas con ≥ 90 % de exactitud. La curva
completa dice que no hay tal punto:

| Umbral | Cobertura | Exactitud en aceptadas |
|---:|---:|---:|
| 0.00 | 100.0 % | 55.0 % |
| 0.50 | 89.0 % | 56.7 % |
| 0.60 | 63.5 % | 61.4 % |
| **0.70** | **34.8 %** | **77.7 %** |
| 0.80 | 13.2 % | 77.4 % |
| 0.90 | 0.0 % | — (no emite nada) |

Y en el subconjunto crítico es peor: de las 74 notas con negación, el modelo
recomendado acierta 30 y falla 44 (40.5 %, contra el 85 % que había exigido). Un
caso del corpus lo resume: *«La calificadora no modificó la nota soberana y
retiró la perspectiva negativa»* —una buena noticia, etiquetada POSITIVO— salió
clasificada **NEGATIVO con 0.78 de confianza**.

### Qué se concluye

No bajé los umbrales para que el resultado cupiera dentro. La conclusión es que
**ningún modelo preentrenado sin fine-tuning califica hoy para emitir señales
automáticas** en este caso de uso, y que el prototipo arranca en modo asistido:
a 331 notas por segundo el motor ordena y prioriza la lectura del día para el
asesor —qué notas tocan a qué clientes y en qué orden— sin afirmar nada sobre su
signo. La emisión automática queda como fase dos, condicionada a un corpus
etiquetado por al menos tres personas de la mesa.

### Lo que el ejercicio confirma, gane quien gane

1. **Elegir por popularidad no funciona.** Los cuatro modelos tienen métricas
   publicadas que se ven bien, y ninguna se calculó sobre notas financieras en
   español. La única medición que sirve para decidir es la del propio caso de uso.

2. **La exactitud sola engaña.** Con NEUTRAL sub-representada, un modelo que se
   apoye en la clase mayoritaria puede verse decente en *accuracy* y ser inútil.
   El criterio de decisión es el **F1-score macro**, y por debajo de él, el
   desempeño por clase.

3. **Las negaciones son el riesgo operativo concreto**, y aquí quedó cuantificado:
   44 errores de 74 casos, con confianza alta. Una señal invertida emitida con
   seguridad es el error más caro que puede cometer este motor.

4. **El ajuste que más valor agrega no es técnico sino de proceso.** El umbral con
   abstención convierte la incertidumbre del modelo en una decisión explícita
   sobre quién atiende cada nota. En banca eso no es opcional.

---

## 7. Limitaciones declaradas

- El corpus lo etiquetó **una sola persona**. Mi criterio de qué es POSITIVO
  queda incrustado en la medición. Antes de cualquier *fine-tuning* haría falta
  etiquetado por al menos tres personas de la mesa, con medición de acuerdo entre
  evaluadores.
- Las notas son sintéticas. Reproducen el registro y la estructura de las notas
  reales, pero no su distribución exacta de temas.
- No se hizo *fine-tuning*: con 400 notas etiquetadas por un solo criterio, el
  riesgo de sobreajustar es mayor que el beneficio esperado.
- Los modelos entregan una etiqueta y una confianza, no una razón. Por eso toda
  señal se entrega junto con la nota que la originó, su fuente y su fecha.
- **Los resultados corresponden a una sola corrida.** No se repitió con varias
  semillas ni se calcularon intervalos de confianza. Para las diferencias grandes
  del ejercicio (8.3 puntos entre el primero y el segundo) eso no cambia el orden;
  para diferencias de uno o dos puntos no alcanzaría, y así queda dicho.
- La confianza que devuelven estos modelos **no está calibrada**. Un 0.78 no
  significa 78 % de probabilidad de acierto, y el ejemplo de la nota soberana lo
  demuestra. El umbral se usa como filtro ordinal, no como probabilidad.

---

## 8. Licencia y uso

Código bajo licencia MIT. Los modelos evaluados conservan sus propias licencias
(Apache-2.0 y MIT), verificadas en la tarjeta de cada uno. Los datos sintéticos
son de libre uso académico. Los datos de fondos son información pública de BBVA
México y se citan como tal.

Este trabajo es un **ejercicio académico**. No constituye recomendación de
inversión ni refleja posición oficial de BBVA México.

---

*La inteligencia artificial no sustituye el criterio del banquero; lo aumenta.*

**Eduardo Aburto Angulo** · Banquero Patrimonial Sr., BBVA México · plaza Xalapa
