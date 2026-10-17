#!/usr/bin/env python3
"""Verifica las fuentes candidatas de Cotejo y genera sources.yaml.

Para cada medio:
  1. Revisa robots.txt (si bloquea nuestro user-agent en la home, queda marcado).
  2. Prueba los feeds conocidos; si no hay, descubre feeds desde <link rel="alternate">.
  3. Valida que el feed sea RSS/Atom, tenga entradas y fechas recientes.
Las fuentes primarias solo se comprueban por disponibilidad de la home.

Uso:
    pip install requests feedparser pyyaml
    python check_sources.py candidates.yaml sources.yaml
"""
import re
import sys
import time
import datetime as dt
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import feedparser
import requests
import yaml

USER_AGENT = "CotejoBot/0.1 (+https://github.com/TU-USUARIO/cotejo; agregador abierto sin fines de lucro)"
TIMEOUT = 15
PAUSE = 2.0  # segundos entre pedidos al mismo sitio, para no cargar a los medios
FRESH_DAYS = 3

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})

LINK_RE = re.compile(r"<link[^>]+>", re.I)
ATTR_RE = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']')


def robots_allows(url):
    parts = urlparse(url)
    rp = RobotFileParser()
    rp.set_url(f"{parts.scheme}://{parts.netloc}/robots.txt")
    try:
        resp = session.get(rp.url, timeout=TIMEOUT)
        if resp.status_code >= 400:
            return True  # sin robots.txt útil: se asume permitido
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(USER_AGENT, url)
    except requests.RequestException:
        return True


def discover_feeds(home):
    try:
        resp = session.get(home, timeout=TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException:
        return []
    found = []
    for tag in LINK_RE.findall(resp.text):
        attrs = {k.lower(): v for k, v in ATTR_RE.findall(tag)}
        if attrs.get("rel", "").lower() == "alternate" and "xml" in attrs.get("type", "").lower():
            if attrs.get("href"):
                found.append(urljoin(home, attrs["href"]))
    return list(dict.fromkeys(found))


def check_feed(url):
    result = {"url": url, "ok": False}
    try:
        resp = session.get(url, timeout=TIMEOUT)
        result["http_status"] = resp.status_code
        if resp.status_code != 200:
            return result
        parsed = feedparser.parse(resp.content)
        entries = parsed.entries
        result["entries"] = len(entries)
        if parsed.bozo and not entries:
            result["error"] = "xml inválido"
            return result
        newest = None
        for e in entries:
            ts = e.get("published_parsed") or e.get("updated_parsed")
            if ts:
                d = dt.datetime(*ts[:6])
                newest = d if newest is None or d > newest else newest
        if newest:
            result["newest"] = newest.isoformat()
            result["fresh"] = (dt.datetime.utcnow() - newest).days <= FRESH_DAYS
        result["ok"] = len(entries) > 0
    except requests.RequestException as exc:
        result["error"] = type(exc).__name__
    return result


def check_medium(m):
    out = {"id": m["id"], "name": m["name"], "home": m["home"], "type": m.get("type", "sin-clasificar")}
    out["robots_ok"] = robots_allows(m["home"])
    time.sleep(PAUSE)
    candidates = list(m.get("feeds", []))
    if not candidates:
        candidates = discover_feeds(m["home"])
        time.sleep(PAUSE)
    checked = []
    for url in candidates[:6]:
        checked.append(check_feed(url))
        time.sleep(PAUSE)
    out["feeds"] = checked
    working = [f for f in checked if f["ok"]]
    if not out["robots_ok"]:
        out["status"] = "bloqueado-por-robots"
    elif working:
        out["status"] = "rss-ok"
    elif candidates:
        out["status"] = "rss-con-problemas"
    else:
        out["status"] = "sin-rss"  # requeriría scraping: revisar términos de uso antes
    return out


def check_primary(p):
    out = {"id": p["id"], "name": p["name"], "home": p["home"]}
    try:
        resp = session.get(p["home"], timeout=TIMEOUT, allow_redirects=True)
        out["http_status"] = resp.status_code
        out["status"] = "disponible" if resp.status_code == 200 else "revisar"
    except requests.RequestException as exc:
        out["status"] = "no-responde"
        out["error"] = type(exc).__name__
    time.sleep(PAUSE)
    return out


def main():
    src, dst = (sys.argv + ["candidates.yaml", "sources.yaml"][len(sys.argv) - 1:])[1:3]
    with open(src, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    report = {
        "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "media": [],
        "primary_sources": [],
    }
    for m in data.get("media", []):
        print(f"Medio: {m['name']}")
        res = check_medium(m)
        print(f"  -> {res['status']}")
        report["media"].append(res)
    for p in data.get("primary_sources", []):
        print(f"Fuente primaria: {p['name']}")
        res = check_primary(p)
        print(f"  -> {res['status']}")
        report["primary_sources"].append(res)
    with open(dst, "w", encoding="utf-8") as fh:
        yaml.safe_dump(report, fh, allow_unicode=True, sort_keys=False)
    ok = sum(1 for m in report["media"] if m["status"] == "rss-ok")
    print(f"\nListo: {ok}/{len(report['media'])} medios con RSS válido. Resultado en {dst}")


if __name__ == "__main__":
    main()
