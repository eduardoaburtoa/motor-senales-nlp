# Evidencia de resultados

Las tablas y gráficos se extrajeron de `notebooks/evidencia/colab_t4_original.ipynb`, aportado ya ejecutado. La huella del archivo original completo, antes de retirar metadatos y vistas redundantes para GitHub, está en `condiciones_ejecucion.json`. `tabla_comparativa_original.csv` conserva las licencias declaradas en aquella corrida (incorrectas); `tabla_comparativa.csv` corrige solo esa metadata, conservando todas las cifras medidas.

No se adjuntó `predicciones_completas.csv` de la corrida original. No lo reconstruimos inventando observaciones a partir de los totales. Una nueva ejecución del notebook corregido lo exporta. La fecha exacta y las revisiones de pesos de aquella corrida no figuran en sus salidas y se reportan como no registradas.

`salida_colab.txt` conserva las salidas de texto; las figuras se extrajeron de las imágenes incrustadas. `ejemplos_control_economico.json` son escenarios didácticos de reglas, no predicciones ni resultados de inversión.

Los F1 por dificultad originales usan las clases presentes en cada segmento. No deben confundirse con un macro fijo sobre tres clases cuando un segmento no contiene alguna. Las métricas globales sí cubren las tres clases.
