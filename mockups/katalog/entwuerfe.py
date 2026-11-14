"""Drei Entwürfe für die Katalogseite (projekte.md) im Glas-Stil. Gemeinsam: Kopf mit Ortungsschirm der Themen,
Themenleisten, Archivlisten und Tasten aus werkzeug/buehne/katalog.py; verschieden sind die Projektkacheln."""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import Callable

from buehne import katalog
from buehne.akzent import akzent
from buehne.ergebnis import FUENFTEL, HALB, VIERTEL, VOLL, Ergebnis
from buehne.glas import BEWEGUNG_GLAS, GLAS_LEISE, GLAS_TINTE, kantenlicht, klammern, rahmen
from buehne.material import bogen, icon, mulde, polar, spiegelung, svg, text, textbreite, umbrechen
from profil import liste_md
from projekte import Profil, Projekt


@dataclass(frozen=True)
class Entwurf:
    kennung: str
    titel: str
    idee: str
    merkmale: tuple[str, ...]
    kachel: Callable[[Projekt, str], str]  # (Projekt, Nummer wie 01.03) -> SVG
    breite: int
    je_zeile: int


def _ring(cx: float, cy: float, r: float, farbe: str, kante: float, bild: pathlib.Path) -> str:
    """Icon im Skalenring: Striche, leuchtender Bogen, Metallfassung, dunkle Mulde."""
    teile = []
    for g in range(-135, 136, 15):
        x1, y1 = polar(cx, cy, r + 9, g)
        x2, y2 = polar(cx, cy, r + 9 - (5 if g % 45 == 0 else 3), g)
        teile.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="#46596a" stroke-width="1.1"/>')
    teile.append(f'<path d="{bogen(cx, cy, r + 12, -135, 135)}" fill="none" stroke="#1d2a33" stroke-width="2.4"/>')
    teile.append(f'<path d="{bogen(cx, cy, r + 12, -135, 75)}" fill="none" stroke="{farbe}" stroke-width="2.4" '
                 'stroke-linecap="round" filter="url(#leuchten)"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#rahmen)"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#lichtkante)" stroke-width="1.3"/>')
    innen = r - 5
    teile.append(mulde(f"M{cx - innen},{cy} a{innen},{innen} 0 1,0 {2 * innen},0 a{innen},{innen} 0 1,0 {-2 * innen},0",
                       "#05090c"))
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="{innen * .8:.1f}" fill="{farbe}" opacity=".12" '
                 'filter="url(#leuchten_weit)"/>')
    return "".join(teile) + icon(bild, cx - kante / 2, cy - kante / 2, kante)


# ---------- K1 Instrumente: vier je Zeile, Icon im Skalenring ----------

def kachel_instrument(projekt: Projekt, nummer: str) -> str:
    b, h = VIERTEL, 198
    a = akzent(projekt)
    fassung, glas = rahmen(b, h, 14, 3)
    teile = [fassung, kantenlicht(b, glas, farbe=a), klammern(10, 10, b - 20, h - 20, a, 10)]
    teile.append(text(18, 28, nummer, 10, a, 700, 1.5, extra='opacity=".85"'))
    teile.append(text(b - 18, 28, katalog.zielart(projekt.ziel), 9.5, GLAS_LEISE, 700, 1.5, "end"))
    teile.append(_ring(b / 2, 70, 30, a, 34, projekt.icon_pfad))
    teile.append(text(b / 2, 132, projekt.name, 15 if len(projekt.name) < 17 else 13, GLAS_TINTE, 600, .3, "middle"))
    for n, zeile in enumerate(umbrechen(projekt.info, 30, 3)):
        teile.append(text(b / 2, 152 + n * 15, zeile, 11.5, GLAS_LEISE, 500, 0, "middle"))
    teile.append(spiegelung(glas))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs(),
                         bewegung=BEWEGUNG_GLAS, gewichte=(500, 600, 700))


# ---------- K2 Konsole: eine Zeile je Projekt über die volle Breite ----------

def kachel_konsole(projekt: Projekt, nummer: str) -> str:
    b, h = VOLL, 66
    a = akzent(projekt)
    fassung, glas = rahmen(b, h, 12, 3)
    teile = [fassung]
    teile.append(f'<path d="M7,14V{h - 14}" stroke="{a}" stroke-width="3" filter="url(#leuchten)"/>')
    teile.append(text(26, 38, nummer, 12, a, 700, 1))
    teile.append(_ring(108, h / 2, 15, a, 20, projekt.icon_pfad))
    teile.append(text(146, 30, projekt.name, 17, GLAS_TINTE, 600, .3))
    zeile = umbrechen(projekt.info, 84, 1)[0]
    teile.append(text(146, 50, zeile, 13, GLAS_LEISE, 500))
    art = katalog.zielart(projekt.ziel)
    breite = textbreite(art, 10, 1.5) + 24
    x = b - 70 - breite
    teile.append(f'<path d="M{x + 6},21H{x + breite - 6}L{x + breite},33L{x + breite - 6},45H{x + 6}L{x},33Z" '
                 f'fill="{a}" fill-opacity=".08" stroke="{a}" stroke-opacity=".5"/>')
    teile.append(text(x + breite / 2, 37.5, art, 10, "#d6e8ee", 700, 1.5, "middle"))
    teile.append(f'<path d="M{b - 54},19H{b - 24}L{b - 18},25V47H{b - 48}L{b - 54},41Z" fill="{a}" fill-opacity=".14" '
                 f'stroke="{a}" stroke-opacity=".8"/>')
    teile.append(f'<path d="M{b - 43},33h12m-4,-4l4,4l-4,4" fill="none" stroke="{a}" stroke-width="1.8" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    teile.append(spiegelung(glas))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs(),
                         gewichte=(500, 600, 700))


# ---------- K3 Matrix: fünf je Zeile, Icon groß, Text beim Darüberfahren ----------

def kachel_matrix(projekt: Projekt, nummer: str) -> str:
    b, h = FUENFTEL, 156
    a = akzent(projekt)
    fassung, glas = rahmen(b, h, 14, 3)
    teile = [fassung, kantenlicht(b, glas, farbe=a)]
    teile.append(text(16, 26, nummer, 9.5, a, 700, 1.2, extra='opacity=".8"'))
    cx, cy = b / 2, 72
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{a}" stroke-opacity=".45" '
                 'stroke-dasharray="3 4"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="{a}" opacity=".14" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon_pfad, cx - 26, cy - 26, 52))
    namen = umbrechen(projekt.name, 15, 2) if len(projekt.name) > 15 else [projekt.name]
    for n, zeile in enumerate(namen):
        y = 132 + n * 15 - (7 if len(namen) == 2 else 0)
        teile.append(text(cx, y, zeile, 13.5, GLAS_TINTE, 600, .3, "middle"))
    teile.append(spiegelung(glas))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs(),
                         bewegung=BEWEGUNG_GLAS, gewichte=(600, 700))


ENTWUERFE = (
    Entwurf("k1", "Instrumente",
            "Jedes Projekt als kleines Glasinstrument: Icon im Skalenring, Bogen in der Farbe des Icons, Name "
            "und Kurztext. Vier je Zeile, über jedem Thema eine Leiste mit Nummer wie auf dem Schirm im Kopf.",
            ("Kopf mit Ortungsschirm: die Themen als Ziele 01 bis 08",
             "Kacheln mit Skalenring, Kantenlicht und Ziel-Schild (REPO, LIVE, STORE)",
             "Kurztext steht auf der Kachel, nichts versteckt sich hinter dem Darüberfahren",
             "Am nächsten an der Leitwarte aus Entwurf B"),
            kachel_instrument, VIERTEL, 4),
    Entwurf("k2", "Konsole",
            "Der Katalog als Anzeige einer Leitwarte: jedes Projekt eine flache Glaszeile über die volle Breite, "
            "mit Nummer, Icon im Ring, Name, Beschreibung und Ziel-Schild. Am besten lesbar, auch am Telefon.",
            ("Kopf mit Ortungsschirm: die Themen als Ziele 01 bis 08",
             "Eine Zeile je Projekt, Farbstreifen links in der Farbe des Icons",
             "Beschreibung in voller Breite lesbar, Ziel-Schild und Pfeiltaste rechts",
             "Wirkt wie eine Systemliste, ruhig und technisch"),
            kachel_konsole, VOLL, 1),
    Entwurf("k3", "Matrix",
            "Kompakte Glaskacheln, fünf je Zeile, das Icon groß im Lichtkreis, nur der Name darunter. Die "
            "Beschreibung erscheint beim Darüberfahren. Am nächsten an der heutigen Übersicht, nur im Cyber-Stil.",
            ("Kopf mit Ortungsschirm: die Themen als Ziele 01 bis 08",
             "Fünf Kacheln je Zeile, Icon groß, gestrichelter Lichtkreis in der Farbe des Icons",
             "Beschreibung als Hinweis beim Darüberfahren",
             "Am kompaktesten, alle Projekte auf wenigen Bildschirmseiten"),
            kachel_matrix, FUENFTEL, 5),
)


def bauen(entwurf: Entwurf, profil: Profil) -> Ergebnis:
    e = Ergebnis(entwurf.kennung, stapeln=True)
    e.zeile((e.bild("kopf.svg", katalog.kopf(profil)), VOLL, "Alle Projekte", None))
    for gruppe, kennung, farbe in katalog.themenleisten(profil):
        e.zeile((e.bild(f"thema-{kennung}.svg", katalog.themenleiste(
            kennung, gruppe.titel, gruppe.text, f"{len(gruppe.projekte):02d} PROJEKTE", farbe)),
            VOLL, f"{gruppe.titel}: {gruppe.text}", None))
        projekte = gruppe.projekte
        for start in range(0, len(projekte), entwurf.je_zeile):
            e.zeile(*((e.bild(f"{p.schluessel}.svg", entwurf.kachel(p, f"{kennung}.{start + n + 1:02d}")),
                       entwurf.breite, f"{p.name}: {p.info}", p.ziel)
                      for n, p in enumerate(projekte[start:start + entwurf.je_zeile])))
    for n, liste in enumerate(profil.listen, start=1):
        e.zeile((e.bild(f"archiv-{n}.svg", katalog.themenleiste(
            f"A{n}", liste.titel, "Kleinere Werkzeuge und Übungen, zum Aufklappen", f"{len(liste.eintraege):02d} REPOS",
            GLAS_LEISE)), VOLL, liste.titel, None))
        e.text(liste_md(liste))
    e.zeile((e.bild("profil.svg", katalog.taste("ZUM PROFIL", "zurueck")), HALB, "Zurück zum Profil", katalog.PROFIL),
            (e.bild("unterstuetzen.svg", katalog.taste("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             profil.angaben.unterstuetzen))
    return e

