# Registro de revisión de la Actividad 4

Revisión del 11 de octubre de 2026.

## Evidencia y correcciones

- Se leyó el prompt entregado y se contrastó la rúbrica: cuatro criterios de 25%, mínimo tres modelos, Colab GPU, métricas y repositorio reproducible.
- Se revisaron T9/T10, el anaquel del 8 de octubre, el business case, el anexo de pares/pitch, la presentación ejecutiva y las hojas del análisis financiero. Sus proyecciones son supuestos del caso, no beneficios demostrados por este benchmark.
- El video de cinco minutos se comprobó como archivo H.264/AAC de 300 segundos y se inspeccionaron fotogramas del planteamiento, funcionamiento, beneficios y controles. No se realizó transcripción integral del audio.
- Los notebooks iniciales tenían listas de líneas sin saltos de línea, que concatenaban instrucciones. El nuevo notebook aportado contiene una ejecución completa, sin errores de celda, en T4; se usa como evidencia principal y se conserva en copia ligera con código y salidas de texto; el original completo está en el paquete local.
- Se recuperaron resultados y gráficos reales de esas salidas. No se inventaron predicciones individuales ausentes, tiempos de ejecución, revisiones de pesos ni memoria máxima.
- Se corrigieron licencias declaradas sin sustento, texto que confundía sentimiento con impacto financiero, falsa afirmación de mejora al quitar prefijos y aprobación automática no respaldada.
- Se fijan versiones principales y revisiones de pesos para las futuras corridas; estas últimas no se atribuyen retroactivamente al experimento original.
- Se reprodujeron exactamente los 400 registros del corpus. En clientes se corrigió el fallback que convertía multiactivos/estrategias en deuda de corto plazo; se mantienen los 150 nombres, perfiles, posiciones y AUM.
- El Excel del paquete original se conserva como referencia en docs/originales; los CSV son el dataset corregido entregable.
- Se consultaron los 61 DICI enlazados en las secciones normativas de BBVA, cubriendo los 59 fondos del anaquel. Se extrajeron 693 registros de comisiones por serie, sin asumir que todos los gastos sean ingreso del banco.
- Se implementaron controles económicos didácticos y pruebas de perfil, liquidez, límite anual y beneficio neto. El caso 3pp × 35% − 2% es negativo y queda bloqueado.
- Se preservaron la plantilla académica y la identidad Vértice con azul; se retiraron referencias no utilizadas y se actualizó la declaración de IA.

## Material del Drive

Se consultó la carpeta compartida y su estructura de material adicional. La carpeta Plantillas no devolvió archivos mediante el conector. Se mantuvo la plantilla real contenida en el DOCX del paquete, además de usar los temas y rúbrica adjuntos como materiales académicos de referencia.

## Verificación

`python src/validate.py`: comprobación del corpus, cartera, catálogo, cobertura de fichas, métricas en casos conocidos, abstención sin aceptados, reglas económicas y sintaxis del notebook. Pasó en la revisión local. No es una nueva inferencia GPU. La evidencia GPU está en el notebook original ejecutado.

La versión corregida requiere una nueva corrida para generar sus propios resultados con las revisiones fijadas. No hay validación externa ni autorización productiva; todas las notas permanecen bajo revisión humana.
