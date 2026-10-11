# Datos

Tres archivos. Uno es real y dos son sintéticos, y la distinción está declarada
en cada caso porque importa para leer los resultados.

## catalogo_fondos.csv — REAL

484 registros de 59 fondos de inversión de BBVA México.

**Origen:** *Anaquel con Rendimientos Históricos del Día Actual*, edición del
**8 de octubre de 2026**, documento público de BBVA México. Procesado con
`src/parse_anaquel.py`. Ninguna cifra fue calculada ni estimada: son las que
publica el banco.

| Campo | Tipo | Descripción |
|---|---|---|
| `fondo` | texto | Clave del fondo (BBVAGUB, BBVARV, B+EDUCA…) |
| `serie` | texto | Serie accionaria (B, C, P, PV, UHN…) |
| `publico` | categórico | Personas Físicas / Personas Morales |
| `familia` | categórico | Deuda, Renta Variable, Estrategias, MultiActivos… |
| `categoria` | categórico | Deuda Corto Plazo, Renta Variable Nacional, etc. (12 categorías) |
| `calificacion` | texto | Calificación de la serie (AAA/1, AA/4…); vacío en renta variable |
| `minimo_inversion` | entero | Inversión mínima en pesos |
| `rend_diario` … `rend_2_anios` | decimal | Rendimientos en porcentaje |
| `precio` | decimal | Precio del título |

## notas_mercado.csv — SINTÉTICO, DECLARADO

400 notas de mercado en español etiquetadas por impacto. **Es el dataset de
evaluación de los modelos.**

Las notas de análisis de la mesa son material propietario y no pueden publicarse
en un repositorio académico, así que el corpus se construyó con
`src/build_dataset.py` a partir de 60 plantillas y variantes; no prueba representatividad de una mesa real.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | texto | N0001 a N0400 |
| `fecha` | fecha | Entre el 1 y el 8 de octubre de 2026 |
| `fuente` | categórico | Nota de análisis · Prensa financiera · Comunicado oficial · Resumen de mesa |
| `clase_activo` | categórico | Deuda Corto Plazo · Deuda Largo Plazo · Renta Variable Nacional · Renta Variable Internacional · Divisas |
| `texto` | texto | La nota. Longitud media de 25 palabras |
| **`impacto`** | categórico | **ETIQUETA OBJETIVO.** POSITIVO · NEUTRAL · NEGATIVO |
| `fenomeno` | categórico | directo · negacion · contraste · cifra_mixta · condicional |
| `dificultad` | categórico | facil · media · dificil |
| `fondos_relacionados` | texto | Claves reales de fondos BBVA de esa clase de activo |

**Sobre `fenomeno` y `dificultad`.** No son adorno: son el instrumento de
análisis. Alrededor de un tercio del corpus son casos con negación o contraste,
que es donde los modelos de sentimiento genérico se rompen. *«La inflación no
sorprendió al alza»* es una buena noticia y contiene dos palabras que suenan
mal. Medir el desempeño ahí por separado es el punto del experimento.

## clientes_simulados.csv — SINTÉTICO, DECLARADO

150 clientes, que es el tamaño de cartera de un banquero patrimonial senior, con
posiciones entre cinco y veinte millones de pesos.

Para fines didácticos y por privacidad de los datos usamos nombres de
superhéroes y villanos, ya que les puedo simular características individuales
relacionadas con la ficción para poder comprobar la lógica de los resultados.
Los fondos asignados y sus rendimientos sí son reales, tomados del anaquel.

| Campo | Tipo | Descripción |
|---|---|---|
| `cliente_id` | texto | C001 a C150 |
| `nombre` | texto | Nombre de ficción |
| `arquetipo` | categórico | Héroe / Villano |
| `perfil_riesgo` | categórico | Conservador / Moderado / Agresivo |
| `posicion_mxn` | entero | Posición entre 5 y 20 millones de pesos |
| `fondo_actual`, `serie_actual`, `categoria_actual` | texto | Asignación didáctica de un fondo real; no certifica idoneidad |
| `rend_1_anio_actual` | decimal | Rendimiento real a un año de esa serie |
| `clase_activo` | categórico | Clase a la que mapea el fondo, para cruzar con las señales |
| `meses_sin_revision` | entero | Meses desde la última revisión de portafolio |

## Reproducibilidad

Ambos generadores son deterministas con la semilla `20261008`:

```bash
python3 src/parse_anaquel.py anaquel.txt data/catalogo_fondos.csv
python3 src/build_dataset.py
```

## Límites del catálogo y de la cartera

El catálogo conserva la extracción del documento original. Fondo+serie no identifica necesariamente una fila única: el anaquel puede repetir instrumentos en bloques de presentación/moneda. No sumar filas como posiciones ni comparar rendimientos entre monedas sin revisión del PDF. El campo `minimo_inversion` conserva el número publicado; su moneda depende del bloque original. Los retornos cortos pueden estar anualizados según la convención del documento.

Se corrigió `clase_activo` de clientes: cuando la categoría no tiene mapeo explícito se conserva su nombre, en vez de asignarle erróneamente Deuda Corto Plazo. La cartera sigue siendo didáctica y **no certifica perfil o idoneidad**. La capa de reglas requiere compatibilidad verificada explícitamente. `fondos_relacionados` hereda categorías del anaquel y no es recomendación.

## Fichas y gastos por serie

`fichas_bbva.csv/json`: fondo, URL de página, prospecto y DICI, estado de consulta, SHA-256 del PDF, número de páginas, fecha de consulta y número de registros de comisiones extraídos.

`comisiones_por_serie.csv`: fondo, serie, total publicado en porcentaje, administración, distribución, URL DICI, fecha y nota metodológica. Valores vacíos significan no extraído, no cero. Se consultaron 61 fichas con 693 registros, cubriendo los 59 fondos del anaquel. Se preservan valores redondeados publicados; no inferir ingresos netos ni sumas exactas por redondeo.

Para actualizar el índice y extraer comisiones: `python src/fetch_fund_documents.py` y después `python src/extract_fees.py`. Cada actualización refleja el documento vigente, no reconstruye automáticamente la consulta histórica.
