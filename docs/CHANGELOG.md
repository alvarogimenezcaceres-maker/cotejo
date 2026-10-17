# Changelog

- 2026-10-17: Estructura inicial (db, ingest, web, docs, sources), CLAUDE.md y permisos. Base del proyecto.
- 2026-10-17: Verificación de fuentes: 7/14 medios con RSS válido. Define qué medios ingerir en la Fase 3.
- 2026-10-17: db/schema.sql y docker-compose.yml (PostgreSQL + pgvector, vector 384). Base de datos de la Fase 2; sin aplicar porque Docker no está instalado.
- 2026-10-17: Esquema aplicado en Docker (6 tablas, pgvector 0.8.7). Puerto host 5433 porque el 5432 lo ocupa otro PostgreSQL local.
- 2026-10-17: ingest/ingest.py (RSS -> título, fragmento <=300, enlace, fecha; robots.txt y pausa 2 s) y sources/media.yaml (clasificación provisional). Primera carga: 272 notas de 5 medios.
- 2026-10-17: ingest/cluster.py: embeddings (fastembed, paraphrase-multilingual-MiniLM-L12-v2, 384 dim) y agrupación por similitud coseno (umbral 0.75, ventana 3 días). Calcula tipos cubiertos y punto ciego.
