# Changelog

- 2026-10-17: Estructura inicial (db, ingest, web, docs, sources), CLAUDE.md y permisos. Base del proyecto.
- 2026-10-17: Verificación de fuentes: 7/14 medios con RSS válido. Define qué medios ingerir en la Fase 3.
- 2026-10-17: db/schema.sql y docker-compose.yml (PostgreSQL + pgvector, vector 384). Base de datos de la Fase 2; sin aplicar porque Docker no está instalado.
- 2026-10-17: Esquema aplicado en Docker (6 tablas, pgvector 0.8.7). Puerto host 5433 porque el 5432 lo ocupa otro PostgreSQL local.
