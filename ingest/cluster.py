"""Embeddings y agrupación por hecho de Cotejo.

Hace: calcula embeddings (título + fragmento) de las notas nuevas y las asigna al evento
más parecido (similitud coseno al centroide, ventana de 3 días) o crea un evento nuevo.
Recalcula qué tipos de medios cubrieron cada evento y cuáles no (punto ciego).
No hace: no genera resúmenes, no marca eventos sensibles, no descarga texto de las notas.

Uso: py ingest/cluster.py [umbral]   (por defecto 0.75)
"""
import os
import sys

import numpy as np
import psycopg
from fastembed import TextEmbedding

DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # 384 dim
WINDOW = "3 days"


def vec(v):
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


def parse(s):
    return np.array(s.strip("[]").split(","), dtype=np.float32)


def unit(a):
    return a / (np.linalg.norm(a) or 1.0)


def main(threshold):
    with psycopg.connect(DB) as conn:
        rows = conn.execute("SELECT id, title, coalesce(snippet,'') FROM articles WHERE embedding IS NULL").fetchall()
        if rows:
            model = TextEmbedding(MODEL)
            embs = model.embed([f"{t}. {s}" for _, t, s in rows], batch_size=32)
            for (aid, _, _), e in zip(rows, embs):
                conn.execute("UPDATE articles SET embedding=%s::vector WHERE id=%s", (vec(unit(e)), aid))
        print(f"embeddings: {len(rows)}")

        # centroides de eventos recientes
        cents = {}
        for eid, emb in conn.execute(
            """SELECT ea.event_id, a.embedding::text FROM event_articles ea
               JOIN articles a ON a.id=ea.article_id JOIN events e ON e.id=ea.event_id
               WHERE e.updated_at > now() - %s::interval""", (WINDOW,)):
            cents.setdefault(eid, []).append(parse(emb))
        cents = {k: unit(np.mean(v, axis=0)) for k, v in cents.items()}
        counts = {k: len(v) for k, v in cents.items()}

        pending = conn.execute(
            """SELECT a.id, a.title, a.embedding::text FROM articles a
               WHERE a.embedding IS NOT NULL AND NOT EXISTS (SELECT 1 FROM event_articles WHERE article_id=a.id)
               ORDER BY a.published_at NULLS LAST""").fetchall()
        new_ev = joined = 0
        touched = set()
        for aid, title, emb in pending:
            v = parse(emb)
            best, sim = None, 0.0
            for eid, c in cents.items():
                s = float(v @ c)
                if s > sim:
                    best, sim = eid, s
            if best is not None and sim >= threshold:
                n = counts[best]
                cents[best] = unit((cents[best] * n + v) / (n + 1))
                counts[best] = n + 1
                joined += 1
            else:
                best = conn.execute("INSERT INTO events (title) VALUES (%s) RETURNING id", (title,)).fetchone()[0]
                cents[best], counts[best] = v, 1
                new_ev += 1
            conn.execute("INSERT INTO event_articles VALUES (%s,%s)", (best, aid))
            touched.add(best)

        all_types = {r[0] for r in conn.execute("SELECT DISTINCT tipo FROM sources WHERE active")}
        for eid in touched:
            cov = {r[0] for r in conn.execute(
                """SELECT DISTINCT s.tipo FROM event_articles ea JOIN articles a ON a.id=ea.article_id
                   JOIN sources s ON s.id=a.source_id WHERE ea.event_id=%s""", (eid,))}
            conn.execute("UPDATE events SET covered_types=%s, missing_types=%s, updated_at=now() WHERE id=%s",
                         (sorted(cov), sorted(all_types - cov), eid))
        print(f"notas agrupadas: {joined} a eventos existentes, {new_ev} eventos nuevos")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 0.75)
