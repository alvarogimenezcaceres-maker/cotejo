# Decisiones

- 2026-10-17: Driver psycopg v3 (oficial, mantenido) para PostgreSQL.
- 2026-10-17: Puerto host 5433 para la BD; el 5432 lo ocupa otro PostgreSQL local.
- 2026-10-17: Clasificación en sources/media.yaml separada de sources.yaml (generado automáticamente); todo `revisado: false` hasta documentar evidencia.
- 2026-10-17: El Nacional y La Clave quedan sin ingerir: su robots.txt bloquea el feed para nuestro user-agent. Se respeta.
- 2026-10-17: fastembed (ONNX, sin PyTorch). multilingual-e5-small no está soportado; se usa paraphrase-multilingual-MiniLM-L12-v2 (384 dim, Apache-2.0), el esquema no cambia.
- 2026-10-17: Umbral de agrupación 0.75: con 0.80 agrupa poco (8 pares), con 0.70 mezcla notas de temas cercanos. Hay que recalibrarlo con más datos y revisión humana.
