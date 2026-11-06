"""Depuración única de Cotejo: borra las notas guardadas que no pasan el filtro de sources/temas.yaml.

Hace: sin --aplicar solo cuenta; con --aplicar borra las notas fuera de tema, los hechos que
quedan sin notas y recalcula tipos cubiertos / punto ciego de los hechos afectados.
No hace: no vuelve a ingerir ni agrupa; la sección de los hechos la asigna cluster.py.

Uso: py ingest/purge_offtopic.py [--aplicar]   (BD: variable COTEJO_DB)
"""
import os
import sys

import psycopg

from temas import Temas

DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")


def main(aplicar):
    temas = Temas()
    with psycopg.connect(DB) as conn:
        rows = conn.execute("SELECT id, title, snippet FROM articles").fetchall()
        fuera = [r[0] for r in rows if not temas.relevant(r[1], r[2])]
        print(f"notas: {len(rows)}; fuera de tema: {len(fuera)}")
        if not aplicar or not fuera:
            print("sin cambios" if not aplicar else "nada que borrar")
            return
        afectados = [r[0] for r in conn.execute(
            "SELECT DISTINCT event_id FROM event_articles WHERE article_id = ANY(%s)", (fuera,))]
        conn.execute("DELETE FROM articles WHERE id = ANY(%s)", (fuera,))
        vacios = conn.execute(
            "DELETE FROM events e WHERE NOT EXISTS (SELECT 1 FROM event_articles ea WHERE ea.event_id=e.id)").rowcount
        all_types = {r[0] for r in conn.execute("SELECT DISTINCT tipo FROM sources WHERE active")}
        for eid in afectados:
            cov = {r[0] for r in conn.execute(
                """SELECT DISTINCT s.tipo FROM event_articles ea JOIN articles a ON a.id=ea.article_id
                   JOIN sources s ON s.id=a.source_id WHERE ea.event_id=%s""", (eid,))}
            conn.execute("UPDATE events SET covered_types=%s, missing_types=%s WHERE id=%s",
                         (sorted(cov), sorted(all_types - cov), eid))
        print(f"borradas {len(fuera)} notas y {vacios} hechos vacíos; {len(afectados)} hechos recalculados")


if __name__ == "__main__":
    main("--aplicar" in sys.argv)
