"""Teile der Katalogseite (projekte.md) im Glas-Stil: Kopf mit Ortungsschirm der Themen, Themenleiste, Tasten.

Die Kacheln der Projekte liefert der gewählte Entwurf; diese Teile sind allen Entwürfen gemeinsam.
"""
from __future__ import annotations

from dataclasses import dataclass

from buehne.ergebnis import HALB, VOLL
from buehne.glas import (BEWEGUNG_GLAS, GLAS_LEISE, GLAS_TINTE, abtastung, defs_glas, kantenlicht, klammern,
                         rahmen)
from buehne.material import BERNSTEIN, CYAN, GRUEN, defs_grund, fase, led, spiegelung, svg, text, textbreite
from buehne.ortung import ortungsschirm
from projekte import Gruppe, Profil

PROFIL = "https://github.com/HalloWelt42"


@dataclass(frozen=True)
class Ziel:
    """Ein Punkt auf dem Ortungsschirm: hier ein Thema statt eines Projekts."""
    name: str
    akzent: str


def defs() -> str:
    return defs_grund() + defs_glas()


def kopf(profil: Profil) -> str:
    b, h = VOLL, 230
    fassung, glas = rahmen(b, h, 26, 8)
    gruppen = profil.katalog_gruppen
    anzahl = sum(len(g.projekte) for g in gruppen)
    teile = [fassung, abtastung(glas, h), kantenlicht(b, glas), klammern(34, 26, 772, 178, CYAN, 18)]
    teile.append(f'<path d="M46,50 l6,0 l-6,8z" fill="{CYAN}"/>')
    teile.append(text(60, 58, "KATALOG  ·  HALLOWELT42", 11, CYAN, 700, 4, extra='opacity=".85"'))
    teile.append(text(44, 112, "Alle Projekte", 50, GLAS_TINTE, 600, 1, extra='filter="url(#leuchten)"'))
    teile.append(text(46, 142, "Selbst gehostete Werkzeuge, nach Themen geordnet.", 16, GLAS_LEISE, 500))
    x = 46.0
    for beschriftung, farbe in ((f"{anzahl} PROJEKTE", CYAN), (f"{len(gruppen)} THEMEN", BERNSTEIN),
                                ("LOKAL · OHNE TRACKING", GRUEN)):
        breite = textbreite(beschriftung, 11, 1.4) + 38
        teile.append(f'<path d="{fase(x, 164, breite, 32, (8, 2, 8, 2))}" fill="#071016" stroke="{CYAN}" '
                     'stroke-opacity=".28"/>')
        teile.append(led(x + 15, 180, farbe, 3))
        teile.append(text(x + 27, 184, beschriftung, 11, "#c4e7ec", 700, 1.4))
        x += breite + 10
    # Die Themen als Ziele, nummeriert wie die Themenleisten darunter
    ziele = tuple(Ziel(g.titel, farbe) for g, farbe in zip(gruppen, _themenfarben(len(gruppen))))
    schirm, bewegung = ortungsschirm(694, 115, 86, ziele, kanalnummern=True)
    teile.append(schirm)
    teile.append(spiegelung(glas))
    return svg(b, h, f"Alle Projekte: {anzahl} Projekte in {len(gruppen)} Themen", "".join(teile), defs(),
               bewegung=BEWEGUNG_GLAS + bewegung, gewichte=(500, 600, 700))


def _themenfarben(anzahl: int) -> list[str]:
    reihe = (CYAN, BERNSTEIN, "#5b9dff", GRUEN, "#b76bff", "#ff8a4c", "#2ee6d6", "#ff5d8f")
    return [reihe[n % len(reihe)] for n in range(anzahl)]


def themenleiste(kennung: str, titel: str, zeile: str, rechts: str, farbe: str = CYAN) -> str:
    b, h = VOLL, 72
    fassung, glas = rahmen(b, h, 16, 4)
    teile = [fassung]
    teile.append(text(30, 47, kennung, 26, farbe, 700, 1, extra='filter="url(#leuchten)"'))
    teile.append(f'<path d="M74,18V54" stroke="{CYAN}" stroke-opacity=".3"/>')
    teile.append(text(90, 34, titel.upper(), 15, GLAS_TINTE, 700, 3))
    teile.append(text(90, 54, zeile, 13, GLAS_LEISE, 500))
    teile.append(text(b - 28, 40, rechts, 11, farbe, 700, 2, "end"))
    teile.append(spiegelung(glas))
    return svg(b, h, f"{titel}: {zeile}", "".join(teile), defs(), gewichte=(500, 700))


def themenleisten(profil: Profil) -> list[tuple[Gruppe, str, str]]:
    """Je Thema: (Gruppe, Kennung 01, 02 ..., Farbe wie auf dem Schirm)."""
    gruppen = profil.katalog_gruppen
    return [(g, f"{n + 1:02d}", farbe) for n, (g, farbe) in enumerate(zip(gruppen, _themenfarben(len(gruppen))))]


def taste(beschriftung: str, symbol: str) -> str:
    b, h = HALB, 64
    fassung, glas = rahmen(b, h, 14, 4)
    teile = [fassung, kantenlicht(b, glas)]
    breite = textbreite(beschriftung, 14, 3)
    mitte = b / 2 + 10
    teile.append(text(mitte, 38, beschriftung, 14, GLAS_TINTE, 700, 3, "middle"))
    sx = mitte - breite / 2 - 22
    if symbol == "herz":
        teile.append(f'<path d="M{sx},{h / 2 - 3} c-2-4-8-4-8 1 c0 4 5 7 8 9 c3-2 8-5 8-9 c0-5-6-5-8-1z" '
                     f'fill="none" stroke="{CYAN}" stroke-width="1.6" filter="url(#leuchten)"/>')
    else:
        teile.append(f'<path d="M{sx + 6},{h / 2}h-14m5,-5l-5,5l5,5" fill="none" stroke="{CYAN}" stroke-width="2" '
                     'stroke-linecap="round" stroke-linejoin="round" filter="url(#leuchten)"/>')
    return svg(b, h, beschriftung, "".join(teile), defs(), bewegung=BEWEGUNG_GLAS, gewichte=(700,))


def zielart(link: str) -> str:
    """Wohin ein Projekt führt, als kurzes Schild: Live-Seite, Store-Eintrag oder Repo."""
    if "github.io" in link:
        return "LIVE"
    if "chromewebstore" in link or "addons.mozilla" in link:
        return "STORE"
    return "REPO"
