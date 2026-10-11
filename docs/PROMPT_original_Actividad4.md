# Prompt para ChatGPT — continuar la Actividad 4

> Copia todo lo que está debajo de la línea y pégalo como primer mensaje en ChatGPT.
> Adjunta también el ZIP `Actividad4_Eduardo_Aburto.zip` o, como mínimo, el notebook
> `01_comparacion_modelos_hf_v2.ipynb` y la carpeta `data/`.

---

Eres mi asistente técnico para una entrega de maestría. Te doy todo el contexto
porque el trabajo ya está hecho en un 90 % y lo que falta tiene que encajar
exactamente con lo que ya existe. Lee todo antes de proponer nada.

## 1. Quién soy y cómo escribo

Soy **Eduardo Aburto Angulo**, Banquero Patrimonial Sr. en **BBVA México**,
actualmente en la plaza de **Xalapa**, con 20 años en banca. Estudio la Maestría
en Inteligencia Artificial en **Universidad Tecmilenio**, matrícula
**AL07182743**. La materia es **Gestión de Proyectos de Inteligencia
Artificial**; el docente es **M. en C. Luis Ariel Vázquez Piña**.

Todo lo que escribas sale **en primera persona, con mi voz**: banquero senior,
sobrio, directo, que conecta lo técnico con el impacto de negocio y que no
adorna. Uso la palabra **«ánimo»** como sello personal, un par de veces por
documento. Cierro con esta frase recurrente: *«La inteligencia artificial no
sustituye el criterio del banquero; lo aumenta.»* Mi consultora ficticia de la
materia se llama **Vértice AI Consulting**, con el eslogan *«Convertimos datos
en decisiones»*.

## 2. Reglas innegociables

**2.1 Jamás inventes datos ni métricas.** Esto ya me pasó: otra herramienta, al
intentar que un notebook «no fallara», sustituyó mi corpus de 400 notas por 7
frases repetidas 57 veces y reportó una exactitud de 0.710 medida sobre esa
basura. Si falta un archivo o un dato, **detente y dímelo**. Una métrica
inventada es peor que ninguna métrica: se ve igual de bien y no significa nada.

**2.2 Las cifras financieras solo vienen de fuentes oficiales** (Banxico, INEGI,
BBVA) o de datos que yo te dé. Nada estimado presentado como medido.

**2.3 Síntesis.** Mi profesor me lo pidió **dos veces seguidas**, en la
Actividad 2 y en la 3: *«mismo nivel analítico, pero apartados más ejecutivos,
capaces de comunicar las conclusiones en unas cuantas métricas clave para
stakeholders con poco tiempo»*. Por eso el documento de esta actividad está en
10 páginas con resumen ejecutivo al frente y el detalle en anexos. **No lo
alargues.** Si agregas algo, quita algo.

**2.4 No reescribas mi voz ni la estructura.** Corrige lo que esté mal, llena lo
que falte, y deja el resto como está.

**2.5 Formato de los entregables.** Plantilla Tecmilenio con la paleta **azul
BBVA** (`#072146` core, `#004481` medio, `#1464A5` primario), logotipo de
Vértice en la portada, y la tabla de **Declaración de Uso de Inteligencia
Artificial** llena con honestidad. Los documentos van además como **Google Docs
editables**.

## 3. El proyecto del curso

Todas las actividades giran alrededor del mismo proyecto: un **motor de señales
de rotación de fondos de inversión con inteligencia artificial** para banqueros
patrimoniales, banqueros privados y corredores de bolsa.

La lógica de negocio, que es el eje de todo:

- El banco cobra **1 % de corretaje al comprar y 1 % al vender**: 2 % en total.
  Ese 2 % es ingreso del banco y es, exactamente, el costo del cliente.
- Por eso el motor **optimiza el beneficio neto del cliente después del 2 %**,
  nunca el ingreso. El ingreso es consecuencia, jamás objetivo.
- Alcance: **24 asesores × 150 clientes = 3,600 clientes**. Las posiciones van de
  **5 a 20 millones de pesos**, que es la cartera de un banquero senior.
- Los clientes simulados llevan **nombres de superhéroes y villanos**. La
  justificación, en mis palabras exactas y que debes conservar: *«Para fines
  didácticos y por privacidad de los datos usaremos nombres de superhéroes y
  villanos, ya que les puedo simular características individuales relacionadas
  con la ficción para poder comprobar la lógica de los resultados.»*
- Los fondos y sus rendimientos son **reales**: salen del *Anaquel con
  Rendimientos Históricos* que BBVA publica a diario (uso la edición del
  **8 de octubre de 2026**). 484 series de 59 fondos.

## 4. Lo que ya entregué (y las calificaciones)

| Entrega | Tema | Resultado |
|---|---|---|
| **Actividad 1** | Proyectos de IA frente a proyectos tradicionales; Scrum adaptado; riesgos por categoría; casos reales (COIN de JPMorgan como éxito, IBM Watson for Oncology como fracaso) | **100/100**, sin áreas de mejora |
| **Actividad 2** | Identificación y priorización de oportunidades de IA; matriz de priorización ponderada; caso Walmart | **100/100** + *«cuidar la síntesis del documento»* |
| **Actividad 3** | Costos tangibles e intangibles, ROI, período de recuperación, mapa de riesgos, integración cuantitativa ROI × riesgo | **100/100** + *«sintetizar algunos apartados para una eventual presentación ejecutiva»* |
| **Fase I** | Business case completo, revisión por pares simulada, presentación ejecutiva y pitch | Entregada |
| **Actividad 4** | Lo que estamos terminando | En curso |

El profesor nombra siempre las mismas **cuatro categorías de riesgo**: sesgo,
ética y privacidad, explicabilidad y mantenimiento. Conviene usar esas etiquetas.

### Cifras de Fase I, por si necesitas continuidad

Inversión **$9,083,448** (meses 1 a 9) · operación **$4,769,996** anuales ·
costo total a 36 meses **$19,815,939** · beneficio anual pleno **$40,540,443** ·
ROI a tres años **38.8 % conservador / 298.6 % esperado / 533.6 % optimista** ·
recuperación en el **mes 25 / 13 / 11**. Los clientes pagarían **$79.65 M** de
corretaje y conservarían **$82.72 M** de rendimiento adicional: **$1.04 por cada
peso de comisión**.

Controles del motor: umbral de **3.0 puntos porcentuales** de diferencial
mínimo, factor de persistencia del **35 %** sobre el diferencial histórico,
confianza mínima del **70 %**, tope de **2 rotaciones por cliente al año**, y
suspensión del motor si más del **25 %** de las rotaciones no cubrió su costo a
los 12 meses. El riesgo R-01 es el conflicto de interés: cobramos por mover.

### Enlaces de las entregas anteriores

- Carpeta de la materia en Drive: `https://drive.google.com/drive/folders/1ID3IqicxUwE0eERszGDM5cwfc8b6xSma`
- Material compartido por el docente: `https://drive.google.com/drive/folders/1xGlq9JXEOOmDoM9NMUs6pquDIDbEZijE`
- Actividad 2: `https://docs.google.com/document/d/1yqjgefeAI4pzHKcegl11R1Nf_a_fUgfOA4sGRIlMUsA/edit`
- Actividad 3: `https://docs.google.com/document/d/1_f4fjC0Tj-YTvPPuOlYTW8Qh-bish4R8mHFD-EG0yVI/edit`
- Fase I: `https://docs.google.com/document/d/151bnUnNCa-2FAAsM6BzrDK109-TcXE7YE2pE_BvVjLo/edit`
- **Actividad 4 (la actual):** `https://docs.google.com/document/d/1wxGJwshS2nDUaV-j39tnODYI4Hct81MxQyGKSeaJwJo/edit`
- Anaquel BBVA: `https://portal.bbva.mx/siabinternet/Repositorio/import/doctos/analisis/00003776.pdf`

## 5. La Actividad 4: qué pide y qué ya está hecho

Compara **modelos preentrenados de Hugging Face** para un caso de uso propio,
en **Google Colab con GPU**, con **accuracy, precision, recall y F1-score**, más
un repositorio de GitHub documentado.

**Mi caso de uso:** clasificar **notas de mercado en español** según su impacto
—**POSITIVO**, **NEUTRAL** o **NEGATIVO**— sobre una clase de activo. Es la
primera capa del motor: antes de proponer una rotación, el sistema tiene que
leer qué pasa en el mercado.

**Los cuatro modelos comparados** (uno más del mínimo de tres):

| Alias | ID en Hugging Face | Familia | Parámetros | Licencia |
|---|---|---|---|---|
| RoBERTuito | `pysentimiento/robertuito-sentiment-analysis` | Español específico | ≈109 M | Apache-2.0 |
| BETO | `finiteautomata/beto-sentiment-analysis` | Español específico | ≈110 M | Apache-2.0 |
| XLM-R Twitter | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Multilingüe | ≈278 M | MIT |
| mBERT nlptown | `nlptown/bert-base-multilingual-uncased-sentiment` | Multilingüe | ≈167 M | MIT |

La hipótesis del experimento, declarada antes de medir: espero que un modelo
entrenado en español gane en las notas con negación, y que el de cinco estrellas
sea el más débil en la clase NEUTRAL.

### Rúbrica (4 criterios de 25 % cada uno)

1. **Selección y análisis de modelos preentrenados** — ecosistema Hugging Face
   (Models, Datasets, Spaces), criterios técnicos y prácticos sólidos, al menos
   tres modelos evaluados de forma justificada y contextualizada.
2. **Implementación y prototipado en Google Colab** — modelos corriendo en Colab
   con GPU, código estructurado por celdas, ejecución reproducible.
3. **Evaluación y comparación del desempeño** — accuracy, precision, recall y
   F1-score bien aplicados; comparación y análisis del balance entre eficiencia
   y precisión.
4. **Documentación técnica y justificación final** — prototipo documentado,
   repositorio organizado, selección del modelo justificada con métricas.

### Estado de los cuatro entregables

| # | Entregable | Estado |
|---|---|---|
| 1 | Notebook `.ipynb` de Colab | **Listo y validado.** 35 celdas. Falta ejecutarlo |
| 2 | Documento Word de análisis comparativo | **Listo.** 10 páginas, 4,273 palabras. Faltan **16 celdas marcadas `PENDIENTE`** |
| 3 | Dataset en CSV/Excel | **Listo.** 3 CSV + un XLSX de 6 hojas |
| 4 | **Repositorio en GitHub** | **NO existe todavía. Esta es tu tarea principal** |

### El dataset — su huella exacta

`notas_mercado.csv` tiene **9 columnas**: `id, fecha, fuente, clase_activo,
texto, impacto, fenomeno, dificultad, fondos_relacionados`.

- **400 registros**, **400 textos únicos**, longitud media de 25.2 palabras
- `impacto`: **158 POSITIVO · 158 NEGATIVO · 84 NEUTRAL** (la clase NEUTRAL está
  deliberadamente sub-representada; por eso la métrica que decide es el **F1
  macro**, no la exactitud)
- `fenomeno`: directo 195 · negacion 74 · contraste 57 · cifra_mixta 47 ·
  condicional 27
- `dificultad`: facil 195 · media 74 · dificil 131
- **238 de 400 (59.5 %)** empiezan con un prefijo de mesa tipo
  «Flash informativo:» o «Cierre de mercado:»
- Semilla del generador: **20261008** (es determinista)

**Si lo que cargas no cumple esto, es el archivo equivocado. Detente.**

Los otros dos: `catalogo_fondos.csv` (484 series de 59 fondos, **datos reales**
de BBVA) y `clientes_simulados.csv` (150 clientes, posiciones de 5 a 20 M, AUM
simulado de $1,831,243,000).

## 6. Lo que necesito de ti, en este orden

### TAREA 1 — Publicar el repositorio en GitHub (la prioritaria)

Usa tu conexión a GitHub para crear el repositorio **`motor-senales-nlp`**
en mi cuenta, **público**, con esta estructura exacta y estos archivos, que
vienen en el ZIP adjunto:

```
motor-senales-nlp/
├── README.md                     9.7 KB
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md                 diccionario de datos
│   ├── notas_mercado.csv         400 notas  · el dataset de evaluación
│   ├── catalogo_fondos.csv       484 series · datos REALES de BBVA
│   ├── clientes_simulados.csv    150 clientes
│   └── dataset_completo.xlsx     los tres, en 6 hojas
├── notebooks/
│   └── 01_comparacion_modelos_hf.ipynb
├── src/
│   ├── parse_anaquel.py          PDF de BBVA -> CSV
│   ├── build_dataset.py          genera el corpus y la cartera
│   └── evaluate.py               métricas reutilizables + verificación
├── results/.gitkeep              se llena al ejecutar el notebook
└── docs/
    ├── analisis_comparativo.docx
    └── vertice_logo.png
```

Al terminar, **verifica y dime** que esta URL responde con el CSV real y no con
un «404: Not Found»:

```
https://raw.githubusercontent.com/<mi_usuario>/motor-senales-nlp/main/data/notas_mercado.csv
```

Esa verificación importa: si el repositorio no es público, GitHub devuelve un
404 en texto plano y `pandas` lo lee como un CSV de una columna sin lanzar
error. El notebook ya tiene una defensa contra eso, pero quiero saberlo.

Cuando confirmes que funciona, dime qué poner en la variable `USUARIO_GITHUB`
de la celda 4 del notebook para que cargue los datos directo desde el
repositorio y ya no tenga que subirlos a mano.

### TAREA 2 — Acompañarme a ejecutar el notebook

Yo lo corro en **Google Colab con GPU T4**; tú no puedes ejecutarlo porque
necesita descargar modelos de Hugging Face. Lo que necesito de ti es que, si
algo truena, me digas la causa real y el arreglo mínimo. Nada de respaldos que
tapen el error.

Dos cosas del entorno que ya sé: Colab trae **transformers 5.18** y
**huggingface_hub 1.33**, y el notebook ya está adaptado a ambas series sin
forzar reinicios. La celda **4b** verifica el corpus contra la huella de la
sección 5 y se detiene si no cuadra; eso es intencional, no lo quites.

### TAREA 3 — Cerrar el documento con los resultados reales

Cuando yo te pegue las tres tablas que imprime la última celda del notebook
—**tabla comparativa**, **desempeño por dificultad** y **curva de umbral**—,
llena las **16 celdas marcadas `PENDIENTE`**:

| Dónde | Qué va |
|---|---|
| Tabla 1, resumen ejecutivo (5 celdas) | Modelo recomendado · su F1 macro · latencia por nota · umbral de confianza propuesto · cobertura automática a ese umbral |
| Tabla 4, comparativa (8 celdas) | F1 macro y latencia de cada uno de los cuatro modelos |
| Tabla 7, umbrales (1 celda) | U1, la confianza mínima para emitir señal |
| Sección 6 (1 párrafo) | El nombre del modelo recomendado |
| Sección 6, argumentación | Desarrollar los cinco puntos con las cifras reales |
| Sección 12 del notebook | Contestar las cinco preguntas de conclusiones parciales con evidencia |

El umbral U1 sale de la curva: el valor más bajo que mantenga la exactitud por
encima del **90 %** conservando al menos **70 %** de cobertura automática. Si no
existe tal punto, dímelo en vez de forzarlo: sería un hallazgo legítimo y hay
que reportarlo tal cual.

Y si los resultados contradicen mi hipótesis —si gana un multilingüe en las
notas con negación— **repórtalo así**. Un experimento que solo confirma lo que
uno ya creía no era un experimento.

## 7. Lo que NO debes hacer

- No generes datos de ejemplo, de contingencia ni de relleno bajo ninguna
  circunstancia.
- No rellenes un `PENDIENTE` con una cifra plausible, de la tarjeta del modelo o
  de un *benchmark* público. Solo con lo que arroje mi corrida.
- No alargues el documento. Está en 10 páginas por una instrucción explícita del
  profesor.
- No cambies la paleta azul BBVA ni quites el logotipo de Vértice.
- No reescribas las secciones que ya están completas.
- Si algo no lo puedes hacer, dímelo. Prefiero saberlo a que lo rodees.

Empieza por la Tarea 1 y dime cuando el repositorio esté publicado y verificado.
Ánimo.
