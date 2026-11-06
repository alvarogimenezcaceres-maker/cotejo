"""Ingesta de Cotejo: lee los RSS de sources/ y guarda título, fragmento (<=300), enlace y fecha.

Hace: respeta robots.txt, pausa de 2 s por sitio, user-agent propio, inserta sin duplicar.
Filtra por tema (sources/temas.yaml): solo política y economía de Paraguay y sus nexos internacionales.
No hace: no descarga el texto completo de las notas, no agrupa ni resume, no hace scraping.

Uso: py ingest/ingest.py   (BD: variable COTEJO_DB, por defecto localhost:5433)
"""
import html
import os
import re
import time
import unicodedata
from calendar import timegm
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import feedparser
import psycopg
import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "CotejoBot/0.1 (+https://github.com/TU-USUARIO/cotejo; agregador abierto sin fines de lucro)"
PAUSE = 2.0
TIMEOUT = 15
DB = os.environ.get("COTEJO_DB", "postgresql://cotejo:cotejo_dev@127.0.0.1:5433/cotejo")


def snippet(entry):
    raw = entry.get("summary") or ""
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()
    return text[:300] or None


def norm(text):
    t = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def term_regex(terms):
    return re.compile(r"\b(?:" + "|".join(re.escape(norm(t)) for t in terms) + r")\b")


def topic_filter():
    t = yaml.safe_load((ROOT / "sources/temas.yaml").read_text(encoding="utf-8"))
    py, own = term_regex(t["paraguay"]), term_regex(t["propios"])
    gen, foreign = term_regex(t["generales"]), term_regex(t["internacional"])

    def relevant(title, snip):
        text = norm(f"{title} {snip or ''}")
        if own.search(text):
            return True
        if foreign.search(text):
            return bool(py.search(text))
        return bool(gen.search(text))

    return relevant


def published(entry):
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    return datetime.fromtimestamp(timegm(t), timezone.utc) if t else None


def allowed(url, cache):
    host = urlparse(url).netloc
    if host not in cache:
        rp = RobotFileParser(f"{urlparse(url).scheme}://{host}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None
        cache[host] = rp
    rp = cache[host]
    return rp is None or rp.can_fetch(USER_AGENT, url)


def main():
    srcs = yaml.safe_load((ROOT / "sources/sources.yaml").read_text(encoding="utf-8"))["media"]
    cls = yaml.safe_load((ROOT / "sources/media.yaml").read_text(encoding="utf-8"))["media"]
    relevant = topic_filter()
    robots = {}
    with psycopg.connect(DB) as conn:
        for m in srcs:
            feeds = [f["url"] for f in m.get("feeds", []) if f.get("ok")]
            if m["id"] not in cls or not feeds:
                continue
            row = conn.execute(
                """INSERT INTO sources (slug, name, tipo, feed_url) VALUES (%s,%s,%s,%s)
                   ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name, tipo=EXCLUDED.tipo, feed_url=EXCLUDED.feed_url
                   RETURNING id""",
                (m["id"], m["name"], cls[m["id"]]["tipo"], feeds[0]),
            ).fetchone()
            sid, new, skipped = row[0], 0, 0
            for url in feeds:
                if not allowed(url, robots):
                    print(f"{m['id']}: robots.txt bloquea {url}")
                    continue
                time.sleep(PAUSE)
                try:
                    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
                    r.raise_for_status()
                except Exception as e:
                    print(f"{m['id']}: error {e}")
                    continue
                for e in feedparser.parse(r.content).entries:
                    if not e.get("link") or not e.get("title"):
                        continue
                    if not relevant(e.title, snippet(e)):
                        skipped += 1
                        continue
                    new += conn.execute(
                        """INSERT INTO articles (source_id, url, title, snippet, published_at)
                           VALUES (%s,%s,%s,%s,%s) ON CONFLICT (url) DO NOTHING""",
                        (sid, e.link, e.title.strip(), snippet(e), published(e)),
                    ).rowcount
            print(f"{m['id']}: {new} nuevas, {skipped} fuera de tema")


if __name__ == "__main__":
    main()
