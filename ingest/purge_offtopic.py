"""Depuración única de Cotejo: borra las notas guardadas que no pasan el filtro de sources/temas.yaml.

Hace: sin --aplicar solo cuenta; con --aplicar borra las notas fuera de tema, los hechos que
quedan sin notas y recalcula tipos cubiertos / punto ciego de los hechos afectados.
No hace: no vuelve a ingerir ni agrupa; la sección de los hechos la asigna cluster.py.

Uso: py ingest/purge_offtopic.py [--aplicar]   (BD: variable COTEJO_DB)
"""
import os
import sys
import time

import psycopg

from temas import Temas

DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")


def paso(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main(aplicar):
    temas = Temas()
    with psycopg.connect(DB, connect_timeout=30) as conn:
        conn.execute("SET statement_timeout = '120s'")
        paso("conectado")
        otras = conn.execute(
            "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid() "
            "AND state LIKE 'idle in transaction%%'").fetchone()[0]
        paso(f"sesiones 'idle in transaction' ajenas: {otras}")
        rows = conn.execute("SELECT id, title, snippet FROM articles").fetchall()
        fuera = [r[0] for r in rows if not temas.relevant(r[1], r[2])]
        paso(f"notas: {len(rows)}; fuera de tema: {len(fuera)}")
        if not aplicar or not fuera:
            print("sin cambios" if not aplicar else "nada que borrar")
            return
        afectados = [r[0] for r in conn.execute(
            "SELECT DISTINCT event_id FROM event_articles WHERE article_id = ANY(%s)", (fuera,))]
        paso(f"hechos afectados: {len(afectados)}")
        conn.execute("CREATE INDEX IF NOT EXISTS event_articles_article_idx ON event_articles (article_id)")
        paso("índice listo")
        conn.execute("DELETE FROM event_articles WHERE article_id = ANY(%s)", (fuera,))
        paso("enlaces borrados")
        conn.execute("DELETE FROM articles WHERE id = ANY(%s)", (fuera,))
        vacios = conn.execute(
            "DELETE FROM events e WHERE NOT EXISTS (SELECT 1 FROM event_articles ea WHERE ea.event_id=e.id)").rowcount
        paso("notas y hechos vacíos borrados")
        all_types = sorted(r[0] for r in conn.execute("SELECT DISTINCT tipo FROM sources WHERE active"))
        conn.execute(
            """UPDATE events e SET covered_types = c.cov,
                      missing_types = ARRAY(SELECT t FROM unnest(%s::text[]) t WHERE t <> ALL(c.cov))
               FROM (SELECT ea.event_id, array_agg(DISTINCT s.tipo ORDER BY s.tipo) AS cov
                     FROM event_articles ea JOIN articles a ON a.id=ea.article_id JOIN sources s ON s.id=a.source_id
                     GROUP BY ea.event_id) c
               WHERE c.event_id = e.id AND e.id = ANY(%s)""", (all_types, afectados))
        paso("tipos recalculados")
        print(f"borradas {len(fuera)} notas y {vacios} hechos vacíos; {len(afectados)} hechos recalculados")


if __name__ == "__main__":
    main("--aplicar" in sys.argv)
