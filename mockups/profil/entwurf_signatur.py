"""Entwurf C "Signatur": reduziert wie ein Katalog edler Audiogeräte, Anthrazit mit Messing."""
from __future__ import annotations

import pfad  # noqa: F401  (macht werkzeug/ importierbar)
from buehne.auswahl import Auswahl
from projekte import Projekt
from buehne.ergebnis import DRITTEL, HALB, VOLL, Ergebnis
from steckbrief import Steckbrief, reihen_teilen
from buehne.material import (MESSING, MESSING_HELL, avatar, bild, defs_grund, fase, icon, polar, svg, text,
                      textbreite, umbrechen)

STECKBRIEF = Steckbrief(
    kennung="c",
    titel="Signatur",
    idee="Das Profil als Katalog eines edlen Audioherstellers: viel Ruhe, feine polierte Fasen, Messing als einziger "
         "Akzent, ein Plattenteller im Kopf. Ein Projekt steht im Fokus, mit echtem Bildschirmfoto.",
    merkmale=(
        "Kopf mit Schriftzug, Kennzahlen wie ein Datenblatt und Plattenteller mit Tonarm",
        "Fokus-Projekt groß mit Bildschirmfoto, danach Karten in zwei Größen",
        "Ein Lichtschimmer läuft langsam über die Messinglinie",
        "Am ruhigsten und edelsten, wirkt eher Manufaktur als Labor",
    ),
)

TINTE = "#eef0f2"
LEISE = "#9ba3ab"
STUMM = "#7c848c"


def _defs() -> str:
    return defs_grund() + (
        '<linearGradient id="tief" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#25282c"/><stop offset=".5" stop-color="#1a1c1f"/>'
        '<stop offset="1" stop-color="#121315"/></linearGradient>'
        '<linearGradient id="facette" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{MESSING_HELL}" stop-opacity=".55"/>'
        '<stop offset=".25" stop-color="#fff" stop-opacity=".08"/><stop offset=".7" stop-color="#000" stop-opacity=".1"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".7"/></linearGradient>'
        '<linearGradient id="schimmer" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{MESSING_HELL}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff6e0" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="{MESSING_HELL}" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="etikett" cx=".4" cy=".35" r=".8">'
        f'<stop offset="0" stop-color="{MESSING_HELL}"/><stop offset="1" stop-color="#8a6a32"/></radialGradient>'
        '<linearGradient id="arm" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{MESSING_HELL}"/><stop offset="1" stop-color="#7d5f2a"/></linearGradient>'
    )


BEWEGUNG = (".schimmer{animation:schimmer 9s ease-in-out infinite}"
            "@keyframes schimmer{0%{transform:translateX(0)}60%{transform:translateX(1000px)}100%{transform:translateX(1000px)}}")


def _platte(b: float, h: float, ecke: float = 12) -> str:
    """Platte mit polierter Fase: dunkle Außenkante, feine Bürstung, Messinglicht oben links."""
    return (
        f'<path d="{fase(0, 0, b, h, ecke)}" fill="#050607"/>'
        f'<path d="{fase(1, 1, b - 2, h - 2, ecke - 1)}" fill="url(#tief)"/>'
        f'<path d="{fase(1, 1, b - 2, h - 2, ecke - 1)}" fill="#fff" filter="url(#buerste)" opacity=".55"/>'
        f'<path d="{fase(2, 2, b - 4, h - 4, ecke - 1.5)}" fill="none" stroke="url(#facette)" stroke-width="1.4"/>'
    )


def _messinglinie(x1: float, x2: float, y: float, nummer: int = 0) -> str:
    return (
        f'<clipPath id="linie{nummer}"><rect x="{x1:g}" y="{y - 2:g}" width="{x2 - x1:g}" height="4"/></clipPath>'
        f'<path d="M{x1:g},{y:g}H{x2:g}" stroke="{MESSING}" stroke-opacity=".45"/>'
        f'<g clip-path="url(#linie{nummer})"><rect class="schimmer" x="{x1 - 160:g}" y="{y - 1.5:g}" width="160" '
        f'height="3" fill="url(#schimmer)"/></g>'
    )


def _plattenteller(cx: float, cy: float, r: float) -> str:
    rillen = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="#fff" stroke-opacity="{.025 + (i % 3) * .012:.3f}"/>'
        for i, rr in enumerate(range(int(r * .38), int(r - 6), 3))
    )
    ax, ay = cx + 8, cy - r - 4
    kx, ky = polar(cx, cy, r * .62, -58)
    return (
        f'<circle cx="{cx}" cy="{cy + 4}" r="{r + 6}" fill="#000" opacity=".5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="#2a2d31"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="url(#lichtkante)" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0b0b0c"/>{rillen}'
        f'<path d="M{cx},{cy} L{polar(cx, cy, r, -70)[0]:.1f},{polar(cx, cy, r, -70)[1]:.1f} '
        f'A{r},{r} 0 0 1 {polar(cx, cy, r, -40)[0]:.1f},{polar(cx, cy, r, -40)[1]:.1f} Z" fill="#fff" opacity=".05"/>'
        f'<path d="M{cx},{cy} L{polar(cx, cy, r, 110)[0]:.1f},{polar(cx, cy, r, 110)[1]:.1f} '
        f'A{r},{r} 0 0 1 {polar(cx, cy, r, 140)[0]:.1f},{polar(cx, cy, r, 140)[1]:.1f} Z" fill="#fff" opacity=".04"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r * .3:.1f}" fill="url(#etikett)"/>'
        + text(cx, cy + 9, "42", r * .2, "#3a2a10", 600, 1, "middle")
        + f'<circle cx="{cx}" cy="{cy}" r="3" fill="#d9dde2"/>'
        # Tonarm
        f'<circle cx="{ax}" cy="{ay + 30}" r="15" fill="#2a2d31" stroke="url(#lichtkante)"/>'
        f'<circle cx="{ax}" cy="{ay + 30}" r="8" fill="url(#arm)"/>'
        f'<path d="M{ax},{ay + 30} C{ax - 20},{ay + 90} {kx + 30},{ky - 20} {kx + 4:.1f},{ky:.1f}" fill="none" '
        f'stroke="#000" stroke-opacity=".5" stroke-width="6" transform="translate(2,4)"/>'
        f'<path d="M{ax},{ay + 30} C{ax - 20},{ay + 90} {kx + 30},{ky - 20} {kx + 4:.1f},{ky:.1f}" fill="none" '
        f'stroke="url(#arm)" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="{fase(kx - 10, ky - 6, 20, 13, 3)}" fill="url(#arm)" transform="rotate(-30 {kx:.1f} {ky:.1f})"/>'
    )


def kopf(auswahl: Auswahl) -> str:
    b, h = VOLL, 340
    teile = [_platte(b, h, 14)]
    teile.append(f'<clipPath id="flaeche"><path d="{fase(2, 2, b - 4, h - 4, 13)}"/></clipPath>')
    teile.append(f'<g clip-path="url(#flaeche)">{_plattenteller(800, 176, 168)}</g>')
    teile.append(text(60, 70, "SOFTWARE  ·  HIFI  ·  LOKALE KI", 11, MESSING, 600, 6))
    teile.append(_messinglinie(60, 560, 90))
    teile.append(
        f'<text x="56" y="170" font-size="68" fill="{TINTE}" letter-spacing="1">'
        f'<tspan font-weight="300">HalloWelt</tspan><tspan font-weight="600" fill="{MESSING}">42</tspan></text>'
    )
    teile.append(text(60, 208, "Selbst gehostete Software für alle,", 16.5, LEISE, 400))
    teile.append(text(60, 230, "die wissen wollen, wo ihre Daten liegen.", 16.5, LEISE, 400))
    kennzahlen = ((str(auswahl.anzahl_gesamt), "PROJEKTE"), (str(auswahl.anzahl_themen), "THEMEN"),
                  ("100 %", "SELBST GEHOSTET"), ("0", "TRACKER"))
    for n, (wert, beschriftung) in enumerate(kennzahlen):
        x = 60 + n * 150
        if n:
            teile.append(f'<path d="M{x - 16},262V308" stroke="{MESSING}" stroke-opacity=".3"/>')
        teile.append(text(x, 292, wert, 30, TINTE, 300))
        teile.append(text(x, 312, beschriftung, 9.5, STUMM, 600, 2.5))
    return svg(b, h, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", "".join(teile), _defs(),
               bewegung=BEWEGUNG, gewichte=(300, 400, 600))


def abschnitt(titel: str) -> str:
    b, h = VOLL, 48
    breite = textbreite(titel, 11.5, 6)
    teile = [_platte(b, h, 8), text(b / 2, 29, titel, 11.5, MESSING, 600, 6, "middle"),
             f'<path d="M40,24H{b / 2 - breite / 2 - 20:g}M{b / 2 + breite / 2 + 14:g},24H{b - 40}" '
             f'stroke="{MESSING}" stroke-opacity=".3"/>']
    return svg(b, h, titel, "".join(teile), _defs(), gewichte=(600,))


def _raute(x: float, y: float) -> str:
    return f'<path d="M{x},{y - 4}l4,4l-4,4l-4,-4z" fill="{MESSING}"/>'


def fokus(projekt: Projekt) -> str:
    b, h = VOLL, 330
    teile = [_platte(b, h, 14)]
    teile.append(text(50, 62, "IM FOKUS", 11, MESSING, 600, 6))
    teile.append(_messinglinie(50, 360, 78))
    teile.append(text(47, 128, projekt.name, 44, TINTE, 300, .5))
    for n, zeile in enumerate(umbrechen(projekt.info, 38)):
        teile.append(text(50, 160 + n * 21, zeile, 15, LEISE, 400))
    for n, punkt in enumerate(projekt.punkte):
        y = 220 + n * 26
        teile.append(_raute(54, y - 5))
        teile.append(text(68, y, punkt, 14.5, "#d7dbdf", 400))
    teile.append(text(50, 302, "  ·  ".join(t.upper() for t in projekt.technik), 10, STUMM, 600, 2.5))
    # Bildschirmfoto in gefasstem Rahmen
    if projekt.bild_pfad:
        bx, by, bb, bh = 404, 46, 404, 236
        teile.append(f'<path d="{fase(bx - 8, by - 8, bb + 16, bh + 16, 9)}" fill="#050607"/>')
        teile.append(f'<path d="{fase(bx - 7, by - 7, bb + 14, bh + 14, 8.5)}" fill="#2a2d31"/>')
        teile.append(f'<path d="{fase(bx - 6, by - 6, bb + 12, bh + 12, 8)}" fill="none" stroke="url(#facette)" stroke-width="1.4"/>')
        teile.append(f'<clipPath id="foto"><path d="{fase(bx, by, bb, bh, 5)}"/></clipPath>')
        teile.append(f'<path d="{fase(bx, by, bb, bh, 5)}" fill="#111418"/>')
        teile.append(bild(projekt.bild_pfad, bx, by, bb, bh, "foto"))
        teile.append(f'<path d="{fase(bx, by, bb, bh, 5)}" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="1.5"/>')
        teile.append(f'<path d="M{bx},{by} H{bx + bb * .55} L{bx},{by + bh * .7} Z" fill="#fff" opacity=".04"/>')
    teile.append(f'<path d="M{b - 54},300h18m-6,-6l6,6l-6,6" fill="none" stroke="{MESSING}" stroke-width="1.8" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(b, h, f"Im Fokus: {projekt.name}, {projekt.info}", "".join(teile), _defs(), bewegung=BEWEGUNG,
               gewichte=(300, 400, 600))


def karte(projekt: Projekt, nummer: int, b: int) -> str:
    schmal = b < HALB
    h = 240 if schmal else 220
    teile = [_platte(b, h, 12)]
    teile.append(f'<path d="M28,28h34" stroke="{MESSING}" stroke-width="2"/>')
    teile.append(text(b - 28, 34, f"{nummer:02d}", 12, MESSING, 600, 3, "end"))
    teile.append(icon(projekt.icon_pfad, 28, 48, 44))
    teile.append(text(27, 120, projekt.name, 23 if schmal else 26, TINTE, 300, .3))
    zeichen = int((b - 56) / 7.1)
    for n, zeile in enumerate(umbrechen(projekt.info, zeichen, 3 if schmal else 2)):
        teile.append(text(28, 145 + n * 19, zeile, 13.5, LEISE, 400))
    teile.append(f'<path d="M28,{h - 44}H{b - 28}" stroke="#fff" stroke-opacity=".07"/>')
    marken = projekt.technik[:2] if schmal else projekt.technik
    teile.append(text(28, h - 20, "  ·  ".join(t.upper() for t in marken), 10, STUMM, 600, 2.2))
    teile.append(f'<path d="M{b - 46},{h - 24}h16m-5,-5l5,5l-5,5" fill="none" stroke="{MESSING}" stroke-width="1.7" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), _defs(), gewichte=(300, 400, 600))


def technik(auswahl: Auswahl) -> str:
    b, h = VOLL, 64
    teile = [_platte(b, h, 10), text(40, 37, "TECHNIK", 11, MESSING, 600, 5)]
    rest = [w.upper() for w in auswahl.technik]
    breiten = [textbreite(w, 10.5, 2) for w in rest]
    abstand = (b - 160 - 40 - sum(breiten)) / (len(rest) - 1)
    x = 160.0
    for n, (wort, breite) in enumerate(zip(rest, breiten)):
        teile.append(text(x, 37, wort, 10.5, "#c9ced3", 600, 2))
        if n < len(rest) - 1:
            teile.append(_raute(x + breite + abstand / 2 - 1, 33))
        x += breite + abstand
    return svg(b, h, "Technik: " + ", ".join(auswahl.technik), "".join(teile), _defs(), gewichte=(600,))


def taste(beschriftung: str, symbol: str) -> str:
    b, h = HALB, 64
    teile = [_platte(b, h, 10), text(b / 2, 37, beschriftung, 12.5, TINTE, 600, 4.5, "middle")]
    breite = textbreite(beschriftung, 12.5, 4.5)
    x = b / 2 + breite / 2 + 6
    if symbol == "herz":
        teile.append(f'<path d="M{x + 8},{h / 2 - 3} c-2-4-8-4-8 1 c0 4 5 7 8 9 c3-2 8-5 8-9 c0-5-6-5-8-1z" '
                     f'fill="none" stroke="{MESSING}" stroke-width="1.5"/>')
    else:
        teile.append(f'<path d="M{x},{h / 2}h16m-5,-5l5,5l-5,5" fill="none" stroke="{MESSING}" stroke-width="1.7" '
                     'stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(b, h, beschriftung, "".join(teile), _defs(), gewichte=(600,))


def bauen(auswahl: Auswahl) -> Ergebnis:
    e = Ergebnis(STECKBRIEF.kennung)
    e.dateien["avatar.svg"] = avatar(MESSING, 300)
    e.zeile((e.bild("kopf.svg", kopf(auswahl)), VOLL, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", None))
    e.zeile((e.bild("abschnitt.svg", abschnitt("AUSGEWÄHLTE PROJEKTE")), VOLL, "Ausgewählte Projekte", None))
    f = auswahl.fokus
    e.zeile((e.bild(f"{f.schluessel}.svg", fokus(f)), VOLL, f"{f.name}: {f.info}", f.ziel))
    uebrige = auswahl.ohne_fokus
    reihen = reihen_teilen(uebrige)
    nummer = 2
    for reihe in reihen:
        breite = DRITTEL if len(reihe) == 3 else HALB
        eintraege = []
        for p in reihe:
            eintraege.append((e.bild(f"{p.schluessel}.svg", karte(p, nummer, breite)), breite, f"{p.name}: {p.info}",
                              p.ziel))
            nummer += 1
        e.zeile(*eintraege)
    e.zeile((e.bild("technik.svg", technik(auswahl)), VOLL, "Technik: " + ", ".join(auswahl.technik), None))
    e.zeile((e.bild("alle.svg", taste("ALLE PROJEKTE", "pfeil")), HALB, "Alle Projekte", auswahl.link_alle),
            (e.bild("unterstuetzen.svg", taste("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             auswahl.link_unterstuetzen))
    return e



