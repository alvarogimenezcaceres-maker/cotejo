"""Criterio temático de Cotejo, a partir de sources/temas.yaml.

Hace: decide si una nota es relevante (economía de Paraguay, con prioridad al mercado de valores)
y a qué sección pertenece un hecho (bolsa o economia).
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
        self.bolsa = term_regex(t["bolsa"])
        self.eco = term_regex(t["economia"])
        self.inst = term_regex(t["institucional"])
        self.pol = term_regex(t["politica"])
        self.foreign = term_regex(t["internacional"])

    def relevant(self, title, snippet):
        text = norm(f"{title} {snippet or ''}")
        fuerte = self.bolsa.search(text) or self.eco.search(text)
        debil = self.inst.search(text) and not self.pol.search(text)
        if not (fuerte or debil):
            return False
        return bool(self.py.search(text)) if self.foreign.search(text) else True

    def section(self, notes):
        """notes: lista de (título, fragmento) de un hecho. Devuelve bolsa | economia."""
        text = norm(" ".join(f"{t} {s or ''}" for t, s in notes))
        return "bolsa" if self.bolsa.search(text) else "economia"
