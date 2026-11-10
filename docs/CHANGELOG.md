# Changelog

- 2026-10-17: Estructura inicial (db, ingest, web, docs, sources), CLAUDE.md y permisos. Base del proyecto.
- 2026-10-17: Verificación de fuentes: 7/14 medios con RSS válido. Define qué medios ingerir en la Fase 3.
- 2026-10-17: db/schema.sql y docker-compose.yml (PostgreSQL + pgvector, vector 384). Base de datos de la Fase 2; sin aplicar porque Docker no está instalado.
- 2026-10-17: Esquema aplicado en Docker (6 tablas, pgvector 0.8.7). Puerto host 5433 porque el 5432 lo ocupa otro PostgreSQL local.
- 2026-10-17: ingest/ingest.py (RSS -> título, fragmento <=300, enlace, fecha; robots.txt y pausa 2 s) y sources/media.yaml (clasificación provisional). Primera carga: 272 notas de 5 medios.
- 2026-10-17: ingest/cluster.py: embeddings (fastembed, paraphrase-multilingual-MiniLM-L12-v2, 384 dim) y agrupación por similitud coseno (umbral 0.75, ventana 3 días). Calcula tipos cubiertos y punto ciego.
- 2026-10-17: Sitio Astro (web/): portada con hechos de 2+ notas, página por evento con titulares y enlaces, registro de cobertura y punto ciego, formulario de reporte (activo con PUBLIC_REPORT_URL). Estilo editorial sobrio, fuentes del sistema.
- 2026-10-17: ingest/unpublish.py: despublicar/republicar un evento (el sitio lo omite en el próximo build).
- 2026-10-19: .github/workflows/cycle.yml: ciclo horario en GitHub Actions (ingesta, agrupación, build) publicado en Pages; BD en Neon vía secreto COTEJO_DB. Quita la dependencia de la compu local.
- 2026-10-19: Astro con base '/cotejo' y enlaces vía BASE_URL, para que el sitio funcione en usuario.github.io/cotejo/.
- 2026-11-06: Filtro temático al ingerir (sources/temas.yaml + ingest.py): solo política y economía de Paraguay y nexos internacionales. Enfoca el producto; descarta deportes, policiales sin vínculo político y noticias extranjeras sin vínculo con Paraguay.
- 2026-11-06: Portada por secciones (Política, Economía, Nexos internacionales) y solo hechos con 2+ medios distintos. cluster.py asigna la sección (migración idempotente del CHECK de events.topic). Nuevo ingest/purge_offtopic.py y entrada `purgar` del workflow para borrar una vez las notas viejas fuera de tema.
- 2026-11-06: purge_offtopic.py: índice en event_articles(article_id), borrado explícito y statement_timeout de 120 s. La primera depuración se colgó más de 10 min sin ese índice; ahora falla rápido si algo se atasca.
- 2026-11-06: purge_offtopic.py imprime cada paso con hora (flush) y revisa sesiones 'idle in transaction' ajenas, para diagnosticar el atasco de la depuración.
- 2026-11-06: purge_offtopic.py recalcula tipos con un solo UPDATE y cluster.py clasifica en bloque los hechos viejos: antes eran ~2 consultas por hecho (miles) y el ciclo se atascaba. Datos reales: 9.887 notas, 8.072 fuera de tema.
- 2026-11-10: Giro editorial: solo economía de Paraguay con prioridad al mercado de valores (bolsa, casas de bolsa, bonos, SIV, BCP). Nuevo sources/temas.yaml (bolsa/economia), secciones Mercado de valores y Economía, 1 medio basta en bolsa. Se quita la política.
- 2026-11-10: Última Hora (economia.atom) agregada como fuente en sources.yaml y media.yaml (clasificación provisional, revisado: false).
- 2026-11-10: CLAUDE.md: descripción del proyecto actualizada al enfoque en economía y mercado de valores.
