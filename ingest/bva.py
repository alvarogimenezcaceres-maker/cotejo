"""Lectura de las novedades de la Bolsa de Valores de Asunción (BVA), que no tiene RSS ni API.

Hace: lee solo tres listados públicos (hechos de relevancia, nuevas emisiones, avisos de interés),
respeta robots.txt, pausa de 2 s, user-agent propio; guarda título, fragmento fijo, enlace y fecha
de los últimos 90 días, sin duplicar. Es fuente primaria (tipo fuente_primaria).
No hace: no abre las fichas de cada comunicado, no guarda su contenido, no lee otras páginas de la BVA.

Uso: py ingest/bva.py   (BD: variable COTEJO_DB, por defecto localhost:5433)
"""
import re
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import psycopg
import requests
import yaml

from ingest import DB, PAUSE, ROOT, TIMEOUT, USER_AGENT, allowed

BASE = "https://www.bolsadevalores.com.py"
PAGES = [
    ("hechos-de-relevancia", "Hecho de relevancia"),
    ("nuevas-emisiones", "Nueva emisión"),
    ("avisos-de-interes", "Aviso de interés"),
]
DIAS = 90
SNIPPET = "Comunicado publicado por la Bolsa de Valores de Asunción (BVA), mercado de valores."
MESES = {m: i + 1 for i, m in enumerate(
    "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}
FECHA = re.compile(r"(" + "|".join(MESES) + r")\s+(\d{1,2}),\s+(\d{4})", re.I)
TITULO = re.compile(r'<h\d class="elementor-heading-title[^"]*">([^<]+)<')


def parse_fecha(m):
    return datetime(int(m.group(3)), MESES[m.group(1).lower()], int(m.group(2)), tzinfo=timezone.utc)


def nombre_de_slug(href):
    slug = href.rstrip("/").rsplit("/", 1)[-1]
    slug = re.sub(r"(-\d+)+$", "", slug)
    return slug.replace("-", " ").upper()


def leer(path, etiqueta, desde):
    """Devuelve [(título, url, fecha)] de un listado, del más nuevo al más viejo."""
    html = requests.get(f"{BASE}/{path}/", headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT).text
    enlace = re.compile(r'class="elementor-button elementor-button-link[^"]*"\s+href="(/' + path + r'/[^"]+)"')
    out, previo = [], 0
    for m in enlace.finditer(html):
        tramo = html[previo:m.start()]
        previo = m.end()
        fechas = list(FECHA.finditer(tramo))
        if not fechas:
            continue
        fecha = parse_fecha(fechas[-1])
        if fecha < desde:
            continue
        titulos = [t.strip() for t in TITULO.findall(tramo) if t.strip()]
        nombre = titulos[-1] if titulos and path != "nuevas-emisiones" else nombre_de_slug(m.group(1))
        out.append((f"{etiqueta}: {nombre}", urljoin(BASE, m.group(1)), fecha))
    return out


def main():
    cls = yaml.safe_load((ROOT / "sources/media.yaml").read_text(encoding="utf-8"))["media"]["bva"]
    desde = datetime.now(timezone.utc) - timedelta(days=DIAS)
    robots = {}
    with psycopg.connect(DB) as conn:
        sid = conn.execute(
            """INSERT INTO sources (slug, name, tipo, feed_url) VALUES ('bva','Bolsa de Valores de Asunción',%s,%s)
               ON CONFLICT (slug) DO UPDATE SET tipo=EXCLUDED.tipo, feed_url=EXCLUDED.feed_url RETURNING id""",
            (cls["tipo"], f"{BASE}/hechos-de-relevancia/")).fetchone()[0]
        new = 0
        for path, etiqueta in PAGES:
            if not allowed(f"{BASE}/{path}/", robots):
                print(f"bva: robots.txt bloquea {path}")
                continue
            time.sleep(PAUSE)
            try:
                items = leer(path, etiqueta, desde)
            except Exception as e:
                print(f"bva: error en {path}: {e}")
                continue
            for titulo, url, fecha in items:
                new += conn.execute(
                    """INSERT INTO articles (source_id, url, title, snippet, published_at)
                       VALUES (%s,%s,%s,%s,%s) ON CONFLICT (url) DO NOTHING""",
                    (sid, url, titulo, SNIPPET, fecha)).rowcount
            print(f"bva/{path}: {len(items)} en ventana")
        print(f"bva: {new} nuevas")


if __name__ == "__main__":
    main()
