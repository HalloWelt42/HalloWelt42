"""Entwurf B "Leitwarte": Glasanzeigen in gefrästen Rahmen, Kantenlicht in Cyan, ein Hauch Zukunft."""
from __future__ import annotations

import pfad  # noqa: F401  (macht werkzeug/ importierbar)
from buehne.auswahl import Auswahl
from buehne.ergebnis import HALB, VOLL, Ergebnis
from steckbrief import Steckbrief
from buehne.material import (BERNSTEIN, CYAN, GRUEN, avatar, bogen, defs_grund, fase, icon, led, mulde, platte,
                             polar, schraube, spiegelung, svg, text, textbreite, umbrechen)
from buehne.ortung import defs_glas, ortungsschirm
from projekte import Projekt

STECKBRIEF = Steckbrief(
    kennung="b",
    titel="Leitwarte",
    idee="Das Profil als Leitstand: dunkles Glas in gefrästen Metallrahmen mit schrägen Ecken, Kantenlicht in Cyan, "
         "ein Ortungsschirm mit den Top-Projekten. Technisch und futuristisch, aber mit echtem Material.",
    merkmale=(
        "Kopf mit Ortungsschirm: der Strahl kreist, die Projekte leuchten als Ziele auf",
        "Projekte als Instrumente: Icon im Skalenring, jede Karte in der Farbe ihres Projekts",
        "Lichtlauf auf der Glaskante, langsame Abtastlinie",
        "Am stärksten futuristisch, bleibt durch Rahmen und Schrauben edel",
    ),
)

TINTE = "#eef6f8"
LEISE = "#93a8b6"
STUMM = "#6f8594"


def defs() -> str:
    return defs_grund() + defs_glas()


BEWEGUNG_GRUND = (
    ".lauf{animation:lauf 6s linear infinite}"
    "@keyframes lauf{from{transform:translateX(0)}to{transform:translateX(1100px)}}"
    ".abtasten{animation:abtasten 7s linear infinite}"
    "@keyframes abtasten{from{transform:translateY(-60px)}to{transform:translateY(320px)}}"
)


def _rahmen(b: float, h: float, gross: float, klein: float) -> tuple[str, str]:
    """Gefräster Rahmen mit Glasfläche; liefert Grafik und den Pfad der Glasfläche."""
    aussen = fase(0, 0, b, h, (gross, klein, gross, klein))
    glas = fase(6, 6, b - 12, h - 12, (gross - 4, max(klein - 2, 1), gross - 4, max(klein - 2, 1)))
    teile = [
        f'<path d="{aussen}" fill="#050607"/>',
        platte(fase(1, 1, b - 2, h - 2, (gross, klein, gross, klein)), "url(#rahmen)"),
        mulde(glas, "url(#tiefglas)"),
        f'<path d="{glas}" fill="url(#gitter)"/>',
        f'<path d="{glas}" fill="url(#vignette)"/>',
    ]
    return "".join(teile), glas


def _kantenlicht(b: float, glas: str, nummer: int = 0, farbe: str = CYAN) -> str:
    return (
        f'<clipPath id="kante{nummer}"><rect x="0" y="5" width="{b:g}" height="3"/></clipPath>'
        f'<path d="M30,6.6H{b - 20:g}" stroke="{farbe}" stroke-opacity=".28"/>'
        f'<g clip-path="url(#kante{nummer})"><rect class="lauf" x="-220" y="5" width="220" height="3" '
        f'fill="url(#lauflicht)" filter="url(#leuchten)"/></g>'
    )


def _abtastung(glas: str, h: float, nummer: int = 0) -> str:
    return (
        f'<clipPath id="glas{nummer}"><path d="{glas}"/></clipPath>'
        f'<g clip-path="url(#glas{nummer})"><rect class="abtasten" x="0" y="0" width="100%" height="60" '
        f'fill="url(#abtastung)"/></g>'
    )


def _klammern(x: float, y: float, b: float, h: float, farbe: str, laenge: float = 16) -> str:
    """Eckwinkel oben rechts und unten links, wie Markierungen auf einer Anzeige."""
    return (
        f'<path d="M{x + b - laenge:g},{y:g}H{x + b:g}V{y + laenge:g}M{x:g},{y + h - laenge:g}V{y + h:g}H{x + laenge:g}" '
        f'fill="none" stroke="{farbe}" stroke-width="1.6" stroke-opacity=".75" filter="url(#leuchten)"/>'
    )


def kopf(auswahl: Auswahl) -> str:
    b, h = VOLL, 300
    rahmen, glas = _rahmen(b, h, 26, 8)
    teile = [rahmen, _abtastung(glas, h), _kantenlicht(b, glas)]
    teile += [schraube(18, h / 2, 30, 4), schraube(b - 18, h / 2, 75, 4)]
    teile.append(_klammern(34, 30, 772, 240, CYAN, 20))
    # Schriftzug
    teile.append(f'<path d="M46,52 l6,0 l-6,8z" fill="{CYAN}"/>')
    teile.append(text(60, 60, "PROFIL  ·  LEITSTAND 42", 11, CYAN, 700, 4, extra='opacity=".85"'))
    teile.append(text(44, 124, "HalloWelt42", 56, TINTE, 600, 1, extra='filter="url(#leuchten)"'))
    teile.append(text(46, 156, "Selbst gehostete Software mit HiFi-Oberflächen", 16, LEISE, 500))
    teile.append(text(46, 177, "und lokaler KI. Läuft im eigenen Netz.", 16, LEISE, 500))
    # Statusfelder
    x = 46.0
    for beschriftung, farbe in (("BETRIEB · LOKAL", GRUEN), ("KI · EIGENE HARDWARE", CYAN), ("DATEN · IM HAUS", BERNSTEIN)):
        breite = textbreite(beschriftung, 11, 1.4) + 38
        feld = fase(x, 208, breite, 32, (8, 2, 8, 2))
        teile.append(f'<path d="{feld}" fill="#071016" stroke="{CYAN}" stroke-opacity=".28"/>')
        teile.append(led(x + 15, 224, farbe, 3))
        teile.append(text(x + 27, 228, beschriftung, 11, "#c4e7ec", 700, 1.4))
        x += breite + 10
    schirm, schirm_bewegung = ortungsschirm(680, 150, 104, auswahl.projekte)
    teile.append(schirm)
    teile.append(spiegelung(glas))
    return svg(b, h, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", "".join(teile), defs(),
               bewegung=BEWEGUNG_GRUND + schirm_bewegung, gewichte=(500, 600, 700))


def abschnitt(titel: str, rechts: str) -> str:
    b, h = VOLL, 52
    rahmen, glas = _rahmen(b, h, 14, 4)
    teile = [rahmen,
             f'<path d="M30,{h / 2}l6,-6l6,6l-6,6z" fill="{CYAN}" filter="url(#leuchten)"/>',
             text(52, h / 2 + 5, titel, 13, TINTE, 700, 4)]
    start = 52 + textbreite(titel, 13, 4) + 16
    ende = b - 40 - textbreite(rechts, 10, 2)
    teile.append(f'<path d="M{start:g},{h / 2}H{ende:g}" stroke="{CYAN}" stroke-opacity=".3"/>')
    x = start
    while x < ende:
        teile.append(f'<path d="M{x:.1f},{h / 2 - 3}v6" stroke="{CYAN}" stroke-opacity=".35"/>')
        x += 12
    teile.append(text(b - 26, h / 2 + 4, rechts, 10, CYAN, 700, 2, "end"))
    return svg(b, h, titel, "".join(teile), defs(), gewichte=(700,))


def _chip(x: float, y: float, inhalt: str, farbe: str) -> tuple[str, float]:
    breite = textbreite(inhalt.upper(), 10, 1) + 22
    h = 21
    d = f"M{x + 6:g},{y:g}H{x + breite - 6:g}L{x + breite:g},{y + h / 2:g}L{x + breite - 6:g},{y + h:g}H{x + 6:g}L{x:g},{y + h / 2:g}Z"
    return (
        f'<path d="{d}" fill="{farbe}" fill-opacity=".09" stroke="{farbe}" stroke-opacity=".5"/>'
        + text(x + breite / 2, y + 14.5, inhalt.upper(), 10, "#d6e8ee", 700, 1, "middle")
    ), breite


def instrument(projekt: Projekt, nummer: int, anzahl: int) -> str:
    b, h = HALB, 196
    rahmen, glas = _rahmen(b, h, 18, 4)
    a = projekt.akzent
    teile = [rahmen, _abtastung(glas, h), _kantenlicht(b, glas, farbe=a)]
    teile.append(_klammern(14, 14, b - 28, h - 28, a, 12))
    # Skalenring mit Icon
    cx, cy = 82, 98
    for g in range(-135, 136, 9):
        x1, y1 = polar(cx, cy, 52, g)
        x2, y2 = polar(cx, cy, 52 - (7 if g % 45 == 0 else 4), g)
        teile.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="#46596a" stroke-width="1.2"/>')
    teile.append(f'<path d="{bogen(cx, cy, 57, -135, 135)}" fill="none" stroke="#1d2a33" stroke-width="3"/>')
    teile.append(f'<path d="{bogen(cx, cy, 57, -135, 60 + nummer * 9)}" fill="none" stroke="{a}" '
                 f'stroke-width="3" stroke-linecap="round" filter="url(#leuchten)"/>')
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="39" fill="url(#rahmen)"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="39" fill="none" stroke="url(#lichtkante)" stroke-width="1.5"/>')
    teile.append(mulde(f"M{cx - 33},{cy} a33,33 0 1,0 66,0 a33,33 0 1,0 -66,0", "#05090c"))
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{a}" opacity=".1" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon_pfad, cx - 21, cy - 21, 42))
    teile.append(f'<path d="M{cx - 33},{cy} A33,33 0 0 1 {cx + 33},{cy} Z" fill="#fff" opacity=".05"/>')
    # Text
    teile.append(text(160, 44, f"{nummer:02d} / {anzahl:02d}", 11, a, 700, 2.5, extra='opacity=".9"'))
    teile.append(text(159, 74, projekt.name, 24, TINTE, 600, .5))
    for n, zeile in enumerate(umbrechen(projekt.info, 35, 3)):
        teile.append(text(160, 96 + n * 17, zeile, 13, LEISE, 500))
    x = 160.0
    for wort in projekt.technik:
        chip, breite = _chip(x, 148, wort, a)
        if x + breite > b - 70:
            break
        teile.append(chip)
        x += breite + 6
    knopf = fase(b - 60, 144, 40, 29, (9, 2, 9, 2))
    teile.append(f'<path d="{knopf}" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-opacity=".8"/>')
    teile.append(f'<path d="M{b - 47},158.5h14m-5,-5l5,5l-5,5" fill="none" stroke="{a}" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round" filter="url(#leuchten)"/>')
    teile.append(spiegelung(glas))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), defs(), bewegung=BEWEGUNG_GRUND,
               gewichte=(500, 600, 700))


def technik(auswahl: Auswahl) -> str:
    b, h = VOLL, 92
    rahmen, glas = _rahmen(b, h, 18, 4)
    teile = [rahmen, text(32, 40, "TECHNIK", 12, CYAN, 700, 4), text(32, 60, "IM EINSATZ", 10, STUMM, 700, 2)]
    breiten = [textbreite(w.upper(), 10, 1) + 22 for w in auswahl.technik]
    frei = b - 170 - 28
    abstand = (frei - sum(breiten)) / (len(breiten) - 1)
    x = 170.0
    for wort, breite in zip(auswahl.technik, breiten):
        chip, _ = _chip(x, 36, wort, CYAN)
        teile.append(chip)
        x += breite + abstand
    return svg(b, h, "Technik: " + ", ".join(auswahl.technik), "".join(teile), defs(), gewichte=(700,))


def taste(beschriftung: str, symbol: str) -> str:
    b, h = HALB, 64
    rahmen, glas = _rahmen(b, h, 14, 4)
    teile = [rahmen, _kantenlicht(b, glas)]
    breite = textbreite(beschriftung, 14, 3)
    mitte = b / 2 + 10
    teile.append(text(mitte, 38, beschriftung, 14, TINTE, 700, 3, "middle"))
    sx = mitte - breite / 2 - 22
    if symbol == "herz":
        teile.append(f'<path d="M{sx},{h / 2 - 3} c-2-4-8-4-8 1 c0 4 5 7 8 9 c3-2 8-5 8-9 c0-5-6-5-8-1z" '
                     f'fill="none" stroke="{CYAN}" stroke-width="1.6" filter="url(#leuchten)"/>')
    else:
        teile.append(f'<path d="M{sx - 8},{h / 2}h14m-5,-5l5,5l-5,5" fill="none" stroke="{CYAN}" stroke-width="2" '
                     f'stroke-linecap="round" stroke-linejoin="round" filter="url(#leuchten)"/>')
    return svg(b, h, beschriftung, "".join(teile), defs(), bewegung=BEWEGUNG_GRUND, gewichte=(700,))


def bauen(auswahl: Auswahl) -> Ergebnis:
    e = Ergebnis(STECKBRIEF.kennung)
    e.dateien["avatar.svg"] = avatar(CYAN, 600)
    e.zeile((e.bild("kopf.svg", kopf(auswahl)), VOLL, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", None))
    anzahl = len(auswahl.projekte)
    e.zeile((e.bild("abschnitt.svg", abschnitt("AUSGEWÄHLTE PROJEKTE", f"{anzahl:02d} SYSTEME AKTIV")),
             VOLL, "Ausgewählte Projekte", None))
    for i in range(0, anzahl, 2):
        e.zeile(*((e.bild(f"{p.schluessel}.svg", instrument(p, i + n + 1, anzahl)), HALB, f"{p.name}: {p.info}",
                   p.ziel) for n, p in enumerate(auswahl.projekte[i:i + 2])))
    e.zeile((e.bild("technik.svg", technik(auswahl)), VOLL, "Technik: " + ", ".join(auswahl.technik), None))
    e.zeile((e.bild("alle.svg", taste("ALLE PROJEKTE", "pfeil")), HALB, "Alle Projekte", auswahl.link_alle),
            (e.bild("unterstuetzen.svg", taste("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             auswahl.link_unterstuetzen))
    return e
