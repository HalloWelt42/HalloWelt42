"""Drei Entwürfe für die Katalogseite (projekte.md) im Glas-Stil. Gemeinsam: Kopf mit Ortungsschirm der Themen,
Themenleisten, Archivlisten und Tasten aus werkzeug/buehne/katalog.py; verschieden sind die Projektkacheln."""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import Callable

from buehne import katalog
from buehne.akzent import akzent
from buehne.ergebnis import DRITTEL, FUENFTEL, HALB, VIERTEL, VOLL, Ergebnis
from buehne.glas import BEWEGUNG_GLAS, GLAS_LEISE, GLAS_TINTE, kantenlicht, klammern, rahmen
from buehne.material import (GRAVUR, GRAVUR_LEISE, GRAVUR_STUMM, KANTE_DUNKEL, bogen, drehknopf, fase, gravurtext, icon,
                             led, mulde, platte, polar, schraube, spiegelung, svg, text, textbreite, umbrechen)
from buehne.rack import taste_breit
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
    fassung: str = "glas"  # "glas": Kopf und Leisten im Leitwarten-Stil, "rack": wie die Profilseite


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


# ---------- gemeinsame Kleinteile der neuen Entwürfe ----------

def _hash(text_: str) -> int:
    wert = 7
    for zeichen in text_:
        wert = (wert * 31 + ord(zeichen)) % 1_000_003
    return wert


def _passend(inhalt: str, groesse: float, breite: float, sperrung: float = 0) -> float:
    """Schriftgröße, bei der inhalt in breite passt (höchstens groesse)."""
    return min(groesse, breite / max(len(inhalt), 1) / (.6 + sperrung / max(groesse, 1)))


def _taste_klein(x: float, y: float, b: float, h: float, beschriftung: str) -> str:
    return (
        f'<path d="{fase(x - 2, y - 2, b + 4, h + 4, 4)}" fill="#000" opacity=".7"/>'
        f'<path d="{fase(x, y, b, h, 3)}" fill="url(#taste)"/>'
        f'<path d="M{x + 4},{y + 2}H{x + b - 4}" stroke="#fff" stroke-opacity=".6"/>'
        f'<path d="M{x + 8},{y + h / 2 - 5} l6,5 l-6,5z" fill="#2a1700"/>'
        + text(x + b / 2 + 6, y + h / 2 + 3.5, beschriftung, 9, "#2a1700", 700, .8, "middle")
    )


# ---------- K4 Modulwand: hochkant wie Studio-Module, fünf je Zeile ----------

def kachel_modul(projekt: Projekt, nummer: str) -> str:
    b, h = FUENFTEL, 276
    a = akzent(projekt)
    teile = [f'<path d="{fase(0, 0, b, h, 6)}" fill="{KANTE_DUNKEL}"/>', platte(fase(2, 2, b - 4, h - 4, 5))]
    for y in (3, h - 19):
        teile.append(f'<rect x="3" y="{y}" width="{b - 6}" height="16" fill="#000" opacity=".25"/>')
    for x, y, w in ((16, 11, 20), (b - 16, 11, 70), (16, h - 11, 115), (b - 16, h - 11, 160)):
        teile.append(schraube(x, y, w, 4))
    groesse = _passend(projekt.name, 14, b - 24, 1)
    teile.append(gravurtext(b / 2, 40, projekt.name.upper(), groesse, GRAVUR, 700, 1, "middle"))
    teile.append(gravurtext(b / 2, 55, katalog.zielart(projekt.ziel), 9.5, GRAVUR_STUMM, 700, 2, "middle"))
    teile.append(_ring(b / 2, 104, 27, a, 36, projekt.icon_pfad))
    teile.append(drehknopf(b / 2, 166, 14, -100 + _hash(projekt.repo) % 200, a))
    for n, zeile in enumerate(umbrechen(projekt.info, 24, 3)):
        teile.append(gravurtext(b / 2, 198 + n * 13, zeile, 10.5, GRAVUR_LEISE, 500, 0, "middle"))
    teile.append(mulde(fase(b / 2 - 30, 236, 60, 20, 3)))
    teile.append(text(b / 2, 251, nummer, 13, "#ffb547", 700, 1, "middle", 'filter="url(#leuchten)"'))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs_rack_glas(),
               gewichte=(500, 700))


# ---------- K5 Einschübe: halbe Rack-Breite, zwei je Zeile ----------

def kachel_einschub(projekt: Projekt, nummer: str) -> str:
    b, h = HALB, 104
    a = akzent(projekt)
    teile = [f'<path d="{fase(0, 0, b, h, 7)}" fill="{KANTE_DUNKEL}"/>', platte(fase(2, 2, b - 4, h - 4, 6))]
    for x, y, w in ((13, 13, 20), (b - 13, 13, 70), (13, h - 13, 115), (b - 13, h - 13, 160)):
        teile.append(schraube(x, y, w, 4))
    teile.append(f'<path d="{fase(26, 18, 68, 68, 7)}" fill="#0b0c0e"/>')
    fenster = fase(29, 21, 62, 62, 5)
    teile.append(mulde(fenster))
    teile.append(f'<circle cx="60" cy="52" r="26" fill="{a}" opacity=".12" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon_pfad, 39, 31, 42))
    teile.append(spiegelung(fenster))
    teile.append(mulde(fase(108, 16, 58, 22, 3)))
    teile.append(text(137, 32, nummer, 13, "#ffb547", 700, 1, "middle", 'filter="url(#leuchten)"'))
    teile.append(led(178, 27, a, 3))
    teile.append(_taste_klein(b - 92, 14, 66, 24, katalog.zielart(projekt.ziel)))
    groesse = _passend(projekt.name, 18, b - 130)
    teile.append(gravurtext(108, 60, projekt.name, groesse, GRAVUR, 700))
    for n, zeile in enumerate(umbrechen(projekt.info, 44, 2)):
        teile.append(gravurtext(108, 78 + n * 15, zeile, 12, GRAVUR_LEISE, 500))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs_rack_glas(),
               gewichte=(500, 700))


# ---------- K6 Glas im Rack: Metallplatte mit Glasanzeige, drei je Zeile ----------

def kachel_glasrack(projekt: Projekt, nummer: str) -> str:
    b, h = DRITTEL, 250
    a = akzent(projekt)
    teile = [f'<path d="{fase(0, 0, b, h, 8)}" fill="{KANTE_DUNKEL}"/>', platte(fase(2, 2, b - 4, h - 4, 7))]
    for x, y, w in ((14, 14, 20), (b - 14, 14, 70), (14, h - 14, 115), (b - 14, h - 14, 160)):
        teile.append(schraube(x, y, w, 4.2))
    glas = fase(26, 24, b - 52, 146, (12, 3, 12, 3))
    teile.append(f'<path d="{fase(22, 20, b - 44, 154, (14, 4, 14, 4))}" fill="#0b0c0e"/>')
    teile.append(mulde(glas, "url(#tiefglas)"))
    teile.append(f'<path d="{glas}" fill="url(#gitter)"/>')
    teile.append(f'<path d="M46,25.5H{b - 40}" stroke="{a}" stroke-opacity=".55" filter="url(#leuchten)"/>')
    teile.append(klammern(34, 32, b - 68, 130, a, 10))
    teile.append(_ring(78, 82, 24, a, 30, projekt.icon_pfad))
    teile.append(text(124, 66, nummer, 11, a, 700, 1.5, extra='opacity=".9"'))
    teile.append(text(124, 86, katalog.zielart(projekt.ziel), 10, GLAS_LEISE, 700, 2))
    groesse = _passend(projekt.name, 18, b - 76)
    teile.append(text(40, 150, projekt.name, groesse, GLAS_TINTE, 600, .3, extra='filter="url(#leuchten)"'))
    teile.append(spiegelung(glas))
    for n, zeile in enumerate(umbrechen(projekt.info, 34, 3)):
        teile.append(gravurtext(28, 194 + n * 15, zeile, 12, GRAVUR_LEISE, 500))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs_rack_glas(),
               gewichte=(500, 600, 700))


# ---------- K7 Holo-Karten: Glas mit schillernder Kante, drei je Zeile ----------

HOLO = ('<linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#5ff2ff"/><stop offset=".35" stop-color="#b76bff"/>'
        '<stop offset=".65" stop-color="#ffae1a"/><stop offset="1" stop-color="#5ff2ff"/></linearGradient>'
        '<linearGradient id="holoschein" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')


def _sechseck(cx: float, cy: float, r: float) -> str:
    punkte = [polar(cx, cy, r, 30 + n * 60) for n in range(6)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in punkte) + "Z"


def kachel_holo(projekt: Projekt, nummer: str) -> str:
    b, h = DRITTEL, 188
    a = akzent(projekt)
    form = fase(1, 1, b - 2, h - 2, (18, 4, 18, 4))
    teile = [f'<path d="{form}" fill="#06090d"/>', f'<path d="{form}" fill="url(#gitter)"/>',
             f'<path d="{form}" fill="url(#vignette)"/>',
             f'<path d="{fase(1, 1, b - 2, h - 2, (18, 4, 18, 4))}" fill="none" stroke="url(#holo)" stroke-width="1.6" '
             'stroke-opacity=".85"/>',
             f'<path d="{fase(5, 5, b - 10, h - 10, (15, 3, 15, 3))}" fill="none" stroke="#fff" stroke-opacity=".05"/>',
             f'<path class="schein" d="M-60,0 L0,0 L-120,{h} L-180,{h}Z" fill="url(#holoschein)"/>']
    cx, cy = 54, 66
    teile.append(f'<path d="{_sechseck(cx, cy, 34)}" fill="#03070a" stroke="{a}" stroke-width="1.6" '
                 'filter="url(#leuchten)"/>')
    teile.append(f'<path d="{_sechseck(cx, cy, 40)}" fill="none" stroke="{a}" stroke-opacity=".35" '
                 'stroke-dasharray="4 5"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{a}" opacity=".14" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon_pfad, cx - 19, cy - 19, 38))
    teile.append(text(b - 18, 26, f"{nummer}  ·  {katalog.zielart(projekt.ziel)}", 10, a, 700, 1.2, "end"))
    groesse = _passend(projekt.name, 17, b - 116)
    teile.append(text(104, 58, projekt.name, groesse, GLAS_TINTE, 600, .3))
    for n, zeile in enumerate(umbrechen(projekt.info, 27, 4)):
        teile.append(text(104, 78 + n * 15, zeile, 11.5, GLAS_LEISE, 500))
    # Kennstreifen: Striche aus dem Repo-Namen, je Projekt eigen
    wert, x = _hash(projekt.repo), 20.0
    while x < 190:
        breite = 1 + wert % 3
        teile.append(f'<rect x="{x:.1f}" y="152" width="{breite}" height="16" fill="{a}" opacity="{.35 + (wert % 5) / 10:.2f}"/>')
        x += breite + 1.5 + (wert // 3) % 3
        wert = (wert * 1103515245 + 12345) % 2147483648
    teile.append(f'<path d="M{b - 52},150H{b - 26}L{b - 20},156V170H{b - 46}L{b - 52},164Z" fill="{a}" '
                 f'fill-opacity=".14" stroke="{a}" stroke-opacity=".8"/>')
    teile.append(f'<path d="M{b - 42},160h12m-4,-4l4,4l-4,4" fill="none" stroke="{a}" stroke-width="1.8" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    bewegung = (".schein{animation:schein 7s ease-in-out infinite}"
                "@keyframes schein{0%{transform:translateX(0)}60%{transform:translateX(560px)}100%{transform:translateX(560px)}}")
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), katalog.defs() + HOLO, bewegung=bewegung,
               gewichte=(500, 600, 700))


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
    Entwurf("k4", "Modulwand",
            "Jedes Projekt als hochkant stehendes Studio-Modul wie in einem Modularsystem: Name graviert oben, "
            "Icon im Skalenring, Drehknopf in der Projektfarbe, Kanalanzeige unten. Kopf und Leisten als Rack.",
            ("Kopf als Rack-Frontplatte mit Themen-Radar und Bernstein-Anzeige, wie die Profilseite",
             "Themenleisten mit Kanalanzeige und einer LED je Projekt",
             "Fünf Module je Zeile, Schrauben oben und unten, Kurztext graviert",
             "Am stärksten HiFi, spielerisch und trotzdem aufgeräumt"),
            kachel_modul, FUENFTEL, 5, "rack"),
    Entwurf("k5", "Einschübe",
            "Die flachen Einschübe der Profilseite in halber Breite, zwei je Zeile: Icon im Glasfenster, "
            "Kanalanzeige, LED in der Projektfarbe, Bernstein-Taste mit dem Ziel (REPO, LIVE, STORE).",
            ("Kopf als Rack-Frontplatte mit Themen-Radar, wie die Profilseite",
             "Zwei Einschübe je Zeile, Name und zweizeiliger Text graviert",
             "Gleiche Formensprache wie das Rack der Startseite, Profil und Katalog wirken wie ein Gerät",
             "Gut lesbar, ruhig"),
            kachel_einschub, HALB, 2, "rack"),
    Entwurf("k6", "Glas im Rack",
            "Metallplatten mit eingesetzter Glasanzeige: oben im Glas Icon im Skalenring, Nummer und leuchtender "
            "Name, darunter der Text graviert auf dem Metall. Die Mischung aus Regie und Leitwarte.",
            ("Kopf als Rack-Frontplatte mit Themen-Radar",
             "Drei Kacheln je Zeile: Glasanzeige mit Kantenlicht und Eckwinkeln in Metallfassung",
             "Beschreibung graviert unter dem Glas, zwei Zeilen",
             "Verbindet Material (HiFi) und Leuchtanzeige (Cyber)"),
            kachel_glasrack, DRITTEL, 3, "rack"),
    Entwurf("k7", "Holo-Karten",
            "Dunkle Glaskarten mit schillernder Kante von Cyan über Violett zu Bernstein, Icon im leuchtenden "
            "Sechseck, Kennstreifen je Projekt und ein langsamer Lichtschimmer. Am futuristischsten.",
            ("Kopf und Leisten im Leitwarten-Stil mit Themen-Radar",
             "Drei Karten je Zeile, Sechseck-Fassung, Kennstreifen aus dem Repo-Namen",
             "Beschreibung in drei Zeilen, Ziel und Nummer oben rechts",
             "Futuristisch, aber ohne Rack-Material"),
            kachel_holo, DRITTEL, 3),
)


def bauen(entwurf: Entwurf, profil: Profil) -> Ergebnis:
    e = Ergebnis(entwurf.kennung, stapeln=True)
    rack = entwurf.fassung == "rack"
    kopf = katalog.kopf_rack(profil) if rack else katalog.kopf(profil)
    e.zeile((e.bild("kopf.svg", kopf), VOLL, "Alle Projekte", None))
    for gruppe, kennung, farbe in katalog.themenleisten(profil):
        leiste = (katalog.leiste_rack(kennung, gruppe.titel, gruppe.text, len(gruppe.projekte), farbe) if rack else
                  katalog.themenleiste(kennung, gruppe.titel, gruppe.text, f"{len(gruppe.projekte):02d} PROJEKTE",
                                       farbe))
        e.zeile((e.bild(f"thema-{kennung}.svg", leiste), VOLL, f"{gruppe.titel}: {gruppe.text}", None))
        projekte = gruppe.projekte
        for start in range(0, len(projekte), entwurf.je_zeile):
            e.zeile(*((e.bild(f"{p.schluessel}.svg", entwurf.kachel(p, f"{kennung}.{start + n + 1:02d}")),
                       entwurf.breite, f"{p.name}: {p.info}", p.ziel)
                      for n, p in enumerate(projekte[start:start + entwurf.je_zeile])))
    for n, liste in enumerate(profil.listen, start=1):
        zeile = "Kleinere Werkzeuge und Übungen, zum Aufklappen"
        leiste = (katalog.leiste_rack(f"A{n}", liste.titel, zeile, 0, GLAS_LEISE) if rack else
                  katalog.themenleiste(f"A{n}", liste.titel, zeile, f"{len(liste.eintraege):02d} REPOS", GLAS_LEISE))
        e.zeile((e.bild(f"archiv-{n}.svg", leiste), VOLL, liste.titel, None))
        e.text(liste_md(liste))
    taste = taste_breit if rack else katalog.taste
    e.zeile((e.bild("profil.svg", taste("ZUM PROFIL", "pfeil" if rack else "zurueck")), HALB, "Zurück zum Profil",
             katalog.PROFIL),
            (e.bild("unterstuetzen.svg", taste("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             profil.angaben.unterstuetzen))
    return e

