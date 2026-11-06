# Decisiones

- 2026-10-17: Driver psycopg v3 (oficial, mantenido) para PostgreSQL.
- 2026-10-17: Puerto host 5433 para la BD; el 5432 lo ocupa otro PostgreSQL local.
- 2026-10-17: Clasificación en sources/media.yaml separada de sources.yaml (generado automáticamente); todo `revisado: false` hasta documentar evidencia.
- 2026-10-17: El Nacional y La Clave quedan sin ingerir: su robots.txt bloquea el feed para nuestro user-agent. Se respeta.
- 2026-10-17: fastembed (ONNX, sin PyTorch). multilingual-e5-small no está soportado; se usa paraphrase-multilingual-MiniLM-L12-v2 (384 dim, Apache-2.0), el esquema no cambia.
- 2026-10-17: Umbral de agrupación 0.75: con 0.80 agrupa poco (8 pares), con 0.70 mezcla notas de temas cercanos. Hay que recalibrarlo con más datos y revisión humana.
- 2026-10-17: Sitio con astro y pg (únicas dependencias). Lee la BD solo al compilar; sin servidor. Diseño propio (papel, serif, acento único) en vez del hero genérico sugerido por la herramienta de diseño.
- 2026-10-17: El tipo de medio y el punto ciego solo se muestran si todos los medios del evento tienen `revisado: true`.
- 2026-10-17: Formulario de reportes sin endpoint todavía; se muestra solo si existe PUBLIC_REPORT_URL.
- 2026-10-19: Despliegue en GitHub Actions + Pages con BD en Neon en vez de VPS: gratis, sin servidor que mantener y compatible con AGPL (repo público). El worker/nginx de Docker queda como opción futura.
- 2026-10-19: Base '/cotejo' en Astro porque Pages sirve bajo subruta; con dominio propio se cambia a '/'.
- 2026-11-06: Enfoque editorial: política y economía de Paraguay y sus nexos internacionales. Filtro por palabras clave al ingerir (no al mostrar) para mantener chica la BD y el cómputo; lista pública en sources/temas.yaml. Se descartan noticias internacionales sin vínculo con Paraguay. Limitación: las palabras clave dejan pasar o pierden algunas notas; se afina revisando la lista, no con un modelo opaco. Las notas previas al filtro no se depuran.
- 2026-11-06: La sección de cada hecho sale de las mismas listas de sources/temas.yaml (módulo ingest/temas.py), no de un modelo: es auditable. La depuración de notas viejas es manual (`purgar` en workflow_dispatch), no automática, para que editar la lista por error no borre datos en cada ciclo.
