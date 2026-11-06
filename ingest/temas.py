"""Criterio temático de Cotejo, a partir de sources/temas.yaml.

Hace: decide si una nota es relevante (política y economía de Paraguay y sus nexos
internacionales) y a qué sección pertenece un hecho (politica, economia, internacional).
No hace: no toca la BD ni la red; solo compara palabras clave, sin tildes ni mayúsculas.
"""
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def norm(text):
    t = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def term_regex(terms):
    return re.compile(r"\b(?:" + "|".join(re.escape(norm(t)) for t in terms) + r")\b")


class Temas:
    def __init__(self):
        t = yaml.safe_load((ROOT / "sources/temas.yaml").read_text(encoding="utf-8"))
        self.py = term_regex(t["paraguay"])
        self.own = term_regex(t["propios"])
        self.pol = term_regex(t["politica"])
        self.eco = term_regex(t["economia"])
        self.foreign = term_regex(t["internacional"])

    def relevant(self, title, snippet):
        text = norm(f"{title} {snippet or ''}")
        if self.own.search(text):
            return True
        if self.foreign.search(text):
            return bool(self.py.search(text))
        return bool(self.pol.search(text) or self.eco.search(text))

    def section(self, notes):
        """notes: lista de (título, fragmento) de un hecho. Devuelve politica | economia | internacional."""
        text = norm(" ".join(f"{t} {s or ''}" for t, s in notes))
        if self.foreign.search(text) and (self.py.search(text) or self.own.search(text)):
            return "internacional"
        return "economia" if len(self.eco.findall(text)) > len(self.pol.findall(text)) else "politica"
