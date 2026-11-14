"""Leuchtfarbe eines Projekts: die Angabe aus projekte.toml, sonst die kräftigste häufige Farbe seines Icons."""
from __future__ import annotations

import colorsys
import pathlib
import re
from collections import Counter
from functools import lru_cache

from buehne.material import CYAN
from projekte import Projekt

MINDEST_SAETTIGUNG = .35
MINDEST_HELLIGKEIT = .35
MINDEST_LEUCHTEN = .85


def _kraeftig(farbe: tuple[int, int, int]) -> float:
    """Wert für Leuchtkraft: satt und hell zählt, Grau und Schwarz fallen heraus."""
    h, s, v = colorsys.rgb_to_hsv(*(k / 255 for k in farbe))
    return 0.0 if s < MINDEST_SAETTIGUNG or v < MINDEST_HELLIGKEIT else s * v


def _hex(farbe: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*farbe)


def _farben_svg(pfad: pathlib.Path) -> Counter:
    zaehler: Counter = Counter()
    for treffer in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", pfad.read_text(encoding="utf-8")):
        voll = treffer if len(treffer) == 6 else "".join(z * 2 for z in treffer)
        zaehler[tuple(int(voll[i:i + 2], 16) for i in (0, 2, 4))] += 1
    return zaehler


def _farben_png(pfad: pathlib.Path) -> Counter:
    from PIL import Image

    bild = Image.open(pfad).convert("RGBA").resize((48, 48))
    zaehler: Counter = Counter()
    for r, g, b, a in bild.getdata():
        if a > 200:
            zaehler[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
    return zaehler


@lru_cache(maxsize=None)
def aus_icon(pfad: pathlib.Path) -> str:
    zaehler = _farben_svg(pfad) if pfad.suffix == ".svg" else _farben_png(pfad)
    kandidaten = [(anzahl * _kraeftig(farbe), farbe) for farbe, anzahl in zaehler.items() if _kraeftig(farbe) > 0]
    if not kandidaten:
        return CYAN
    # Leuchtfarbe: Farbton und Sättigung vom Icon, Helligkeit angehoben, damit sie auf dunklem Glas trägt
    h, sat, v = colorsys.rgb_to_hsv(*(k / 255 for k in max(kandidaten)[1]))
    return _hex(tuple(round(k * 255) for k in colorsys.hsv_to_rgb(h, min(sat, .85), max(v, MINDEST_LEUCHTEN))))


def akzent(projekt: Projekt) -> str:
    return projekt.akzent or aus_icon(projekt.icon_pfad)
