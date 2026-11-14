"""Entwurf A "Studio-Rack": das Profil als 19-Zoll-Gerät, jedes Projekt ein Einschub."""
from __future__ import annotations

from daten import Auswahl, Projekt
from entwurf import HALB, VOLL, Ergebnis, Steckbrief
from material import (avatar, BERNSTEIN, BERNSTEIN_HELL, CYAN, GRAVUR, GRAVUR_LEISE, GRAVUR_STUMM, GRUEN, KANTE_DUNKEL,
                      bogen, defs_grund, drehknopf, fase, gravurtext, icon, led, mulde, platte, polar,
                      schraube, spiegelung, svg, text, textbreite, umbrechen)

STECKBRIEF = Steckbrief(
    kennung="a",
    titel="Studio-Rack",
    idee="Das Profil als Gerät im 19-Zoll-Gestell: gebürstetes Anthrazit, Schrauben, Bernstein-Anzeige, "
         "VU-Meter mit schwingender Nadel. Jedes Top-Projekt ist ein Einschub mit eigenem Kanal.",
    merkmale=(
        "Kopf als Frontplatte mit Leuchtanzeige und zwei VU-Metern",
        "Projekte als Einschübe: Icon im Glasfenster, Kanalnummer, Schlagworte als Gravurschilder",
        "Technik als Steckfeld mit gesteckten Kabeln",
        "Am nächsten an der Vorlage HiFi, warm und handfest",
    ),
)

OHR = 36


def _defs() -> str:
    return defs_grund() + (
        '<linearGradient id="ohr" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#17191c"/><stop offset=".5" stop-color="#26292d"/>'
        '<stop offset="1" stop-color="#141618"/></linearGradient>'
        '<radialGradient id="vu" cx=".5" cy="1.05" r="1.15">'
        '<stop offset="0" stop-color="#fff0c4"/><stop offset=".45" stop-color="#f6c766"/>'
        '<stop offset="1" stop-color="#9c5f08"/></radialGradient>'
        '<linearGradient id="taste" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BERNSTEIN_HELL}"/><stop offset="1" stop-color="#e08600"/></linearGradient>'
        '<linearGradient id="taste_dunkel" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#40454b"/><stop offset="1" stop-color="#25282c"/></linearGradient>'
        '<pattern id="punktraster" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r=".7" fill="{BERNSTEIN}" opacity=".07"/></pattern>'
    )


def _gestell(breite: int, hoehe: int) -> str:
    """Frontplatte mit Rack-Ohren und Langlöchern samt Schrauben."""
    teile = [f'<path d="{fase(0, 0, breite, hoehe, 6)}" fill="{KANTE_DUNKEL}"/>']
    for x in (0, breite - OHR):
        teile.append(platte(fase(x + 1, 1, OHR - 2, hoehe - 2, 5), "url(#ohr)", buerste=False))
        loecher = (hoehe / 2,) if hoehe < 120 else (hoehe * .22, hoehe * .78)
        for y in loecher:
            mx = x + OHR / 2
            teile.append(f'<rect x="{mx - 11:g}" y="{y - 6.5:g}" width="22" height="13" rx="6.5" fill="#050506"/>'
                         f'<rect x="{mx - 11:g}" y="{y - 6.5:g}" width="22" height="13" rx="6.5" fill="none" '
                         f'stroke="url(#mulde)" stroke-width="1.4"/>')
            teile.append(schraube(mx - 3, y, 35 + y % 50))
    teile.append(platte(fase(OHR, 3, breite - 2 * OHR, hoehe - 6, 4)))
    return "".join(teile)


def _vu(x: float, y: float, b: float, h: float, kanal: str, nummer: int) -> tuple[str, str, str]:
    """VU-Meter: liefert Grafik, Grundstil (Ruhelage) und Bewegung (Nadel)."""
    px, py = x + b / 2, y + h + 22
    r = h * .98
    skala = [("20", -44), ("10", -31), ("7", -21), ("5", -12), ("3", -3), ("0", 14), ("3", 48)]
    striche, ziffern = [], []
    for zahl, winkel in skala:
        x1, y1 = polar(px, py, r - 26, winkel)
        x2, y2 = polar(px, py, r - 16, winkel)
        tx, ty = polar(px, py, r - 6, winkel)
        farbe = "#b3200f" if winkel > 10 else "#2a1803"
        striche.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="{farbe}" stroke-width="1.6"/>')
        ziffern.append(text(tx, ty + 3, zahl, 9, farbe, 700, anker="middle"))
    for winkel in range(-48, 49, 6):
        x1, y1 = polar(px, py, r - 22, winkel)
        x2, y2 = polar(px, py, r - 16, winkel)
        striche.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="#2a1803" stroke-width=".8"/>')
    fenster = fase(x, y, b, h, 4)
    nx, ny = polar(px, py, r - 10, 0)
    grafik = (
        f'<clipPath id="vu{nummer}"><path d="{fenster}"/></clipPath>'
        f'<path d="{fase(x - 5, y - 5, b + 10, h + 10, 6)}" fill="#0b0c0e"/>'
        f'<path d="{fenster}" fill="url(#vu)"/>'
        f'<g clip-path="url(#vu{nummer})">'
        f'<path d="{bogen(px, py, r - 18, -48, 14)}" fill="none" stroke="#2a1803" stroke-width="1.4"/>'
        f'<path d="{bogen(px, py, r - 18, 14, 48)}" fill="none" stroke="#b3200f" stroke-width="4"/>'
        + "".join(striche) + "".join(ziffern)
        + text(px, y + h - 30, "VU", 15, "#2a1803", 700, 1, "middle")
        + text(x + 10, y + h - 9, kanal, 10, "#2a1803", 700)
        + f'<path class="nadel{nummer}" d="M{px:g},{py:g} L{nx:.1f},{ny:.1f}" stroke="#141414" stroke-width="1.6"/>'
        f'<ellipse cx="{px:g}" cy="{y + h + 4:g}" rx="{b * .2:g}" ry="16" fill="#1a1b1d"/>'
        f'<path d="{fase(x, y, b, h * .48, (4, 4, 0, 0))}" fill="#fff" opacity=".1"/>'
        "</g>"
        f'<path d="{fenster}" fill="none" stroke="url(#mulde)" stroke-width="2.4"/>'
    )
    ursprung = f"transform-box:view-box;transform-origin:{px:g}px {py:g}px"
    grund = f".nadel{nummer}{{{ursprung};transform:rotate(-18deg)}}"
    bewegung = (
        f".nadel{nummer}{{animation:pendel{nummer} {3.1 + nummer * .45:.2f}s ease-in-out infinite}}"
        f"@keyframes pendel{nummer}{{0%{{transform:rotate(-34deg)}}18%{{transform:rotate(-6deg)}}"
        f"30%{{transform:rotate(-22deg)}}46%{{transform:rotate({6 + nummer * 3}deg)}}60%{{transform:rotate(-14deg)}}"
        f"78%{{transform:rotate(-2deg)}}100%{{transform:rotate(-34deg)}}}}"
    )
    return grafik, grund, bewegung


def kopf(auswahl: Auswahl) -> str:
    b, h = VOLL, 300
    teile = [_gestell(b, h)]
    # Typenschild und Betriebsanzeige
    teile.append(led(70, 24, GRUEN, 2.6))
    teile.append(gravurtext(80, 28, "BETRIEB", 9.5, GRAVUR_STUMM, 700, 2))
    teile.append(gravurtext(b - OHR - 34, 27.5, "HW-42  ·  EIGENBAU  ·  2026", 9.5, GRAVUR_STUMM, 700, 2, "end"))
    # Leuchtanzeige
    anzeige = fase(62, 42, 404, 140, 5)
    teile.append(f'<path d="{fase(56, 36, 416, 152, 7)}" fill="#0b0c0e"/>')
    teile.append(mulde(anzeige))
    teile.append(f'<path d="{anzeige}" fill="url(#punktraster)"/>')
    teile.append(text(84, 68, "PROFIL", 9, BERNSTEIN, 700, 3, extra='opacity=".55"'))
    teile.append(text(84, 124, "HALLOWELT42", 46, "#ffb547", 700, 3, extra='filter="url(#leuchten)"'))
    teile.append(text(85, 156, "SOFTWARE  ·  HIFI-OBERFLÄCHEN  ·  LOKALE KI", 12, BERNSTEIN_HELL, 600, 1.6,
                      extra='opacity=".7"'))
    teile.append(spiegelung(anzeige))
    # Zwei VU-Meter
    stile, bewegungen = [], []
    for nummer, (x, kanal) in enumerate(((494, "L"), (650, "R")), start=1):
        grafik, grund, bewegung = _vu(x, 42, 140, 140, kanal, nummer)
        teile.append(grafik)
        stile.append(grund)
        bewegungen.append(bewegung)
    # Trennfuge
    teile.append(f'<path d="M{OHR + 22},205H{b - OHR - 22}" stroke="#000" stroke-opacity=".7"/>'
                 f'<path d="M{OHR + 22},206H{b - OHR - 22}" stroke="#fff" stroke-opacity=".08"/>')
    teile.append(gravurtext(62, 240, "Selbst gehostete Werkzeuge mit Studio-Optik.", 16, GRAVUR, 600))
    teile.append(gravurtext(62, 264, "Keine Cloud, kein Tracking. Läuft auf eigener Hardware,", 12.5, GRAVUR_LEISE, 500))
    teile.append(gravurtext(62, 281, "vom Raspberry Pi bis zum Mac.", 12.5, GRAVUR_LEISE, 500))
    # Anzeigen
    for n, (beschriftung, farbe, blinken) in enumerate((("LOKAL", GRUEN, None), ("OFFEN", BERNSTEIN, None),
                                                         ("WERBEFREI", GRUEN, None), ("SIGNAL", CYAN, "puls"))):
        x = 470 + n * 64
        teile.append(led(x, 236, farbe, 3.4, blinken=blinken))
        teile.append(gravurtext(x, 259, beschriftung, 9.5, GRAVUR_STUMM, 700, 1.2, "middle"))
    teile.append(drehknopf(b - OHR - 52, 246, 22, 62))
    stil = "".join(stile)
    bewegung = "".join(bewegungen) + ".puls{animation:puls 1.6s steps(2,jump-none) infinite}" \
                                     "@keyframes puls{0%{opacity:1}50%{opacity:.25}100%{opacity:1}}"
    return svg(b, h, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", "".join(teile), _defs(), stil, bewegung)


def abschnitt(titel: str, rechts: str) -> str:
    b, h = VOLL, 54
    teile = [_gestell(b, h), gravurtext(62, 33, titel, 13, GRAVUR, 700, 4)]
    teile.append(gravurtext(b - OHR - 118, 32, rechts, 10, GRAVUR_STUMM, 700, 2, "end"))
    for n in range(6):
        teile.append(led(b - OHR - 100 + n * 13, 28, BERNSTEIN, 2.4, an=n < 6))
    return svg(b, h, titel, "".join(teile), _defs())


def _schild(x: float, y: float, inhalt: str) -> tuple[str, float]:
    breite = textbreite(inhalt.upper(), 9.5, 1) + 14
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{breite:.1f}" height="19" rx="2.5" fill="#101215"/>'
        f'<rect x="{x:g}" y="{y:g}" width="{breite:.1f}" height="19" rx="2.5" fill="none" stroke="url(#mulde)"/>'
        + text(x + breite / 2, y + 13, inhalt.upper(), 9.5, "#c3cad2", 700, 1, "middle")
    ), breite


def einschub(projekt: Projekt, kanal: int) -> str:
    b, h = HALB, 172
    teile = [f'<path d="{fase(0, 0, b, h, 8)}" fill="{KANTE_DUNKEL}"/>', platte(fase(2, 2, b - 4, h - 4, 7))]
    for x, y, w in ((16, 16, 20), (b - 16, 16, 70), (16, h - 16, 115), (b - 16, h - 16, 160)):
        teile.append(schraube(x, y, w, 4.6))
    # Icon im Glasfenster
    fenster = fase(32, 36, 96, 96, 6)
    teile.append(f'<path d="{fase(28, 32, 104, 104, 8)}" fill="#0b0c0e"/>')
    teile.append(mulde(fenster))
    teile.append(f'<circle cx="80" cy="84" r="40" fill="{projekt.akzent}" opacity=".08" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon, 50, 54, 60))
    teile.append(spiegelung(fenster))
    # Kanalanzeige
    teile.append(gravurtext(b - 84, 45, "KANAL", 9.5, GRAVUR_STUMM, 700, 2, "end"))
    kanalfenster = fase(b - 76, 27, 50, 26, 3)
    teile.append(mulde(kanalfenster))
    teile.append(text(b - 51, 47, f"{kanal:02d}", 19, "#ffb547", 700, 2, "middle", 'filter="url(#leuchten)"'))
    # Name und Beschreibung
    teile.append(gravurtext(150, 66, projekt.name, 22, GRAVUR, 700))
    for n, zeile in enumerate(umbrechen(projekt.info, 36)):
        teile.append(gravurtext(150, 90 + n * 17, zeile, 13, GRAVUR_LEISE, 500))
    # Schlagworte, solange sie vor die Taste passen
    x = 150.0
    for wort in projekt.technik:
        schild, breite = _schild(x, 128, wort)
        if x + breite > b - 92:
            break
        teile.append(schild)
        x += breite + 6
    # Taste
    taste = fase(b - 82, 124, 58, 27, 3)
    teile.append(f'<path d="{fase(b - 84, 122, 62, 31, 4)}" fill="#000" opacity=".7"/>')
    teile.append(f'<path d="{taste}" fill="url(#taste)"/>')
    teile.append(f'<path d="M{b - 79},126H{b - 27}" stroke="#fff" stroke-opacity=".6"/>')
    teile.append(f'<path d="M{b - 72},132 l7,5.5 l-7,5.5z" fill="#2a1700"/>')
    teile.append(text(b - 44, 141.5, "ÖFFNEN", 8.5, "#2a1700", 700, .8, "middle"))
    teile.append(led(b - 53, 166, BERNSTEIN, 1.8))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), _defs())


def _buchse(x: float, y: float, gesteckt: str | None) -> str:
    teile = [f'<circle cx="{x:g}" cy="{y + 1.5:g}" r="15" fill="#000" opacity=".55"/>',
             f'<circle cx="{x:g}" cy="{y:g}" r="14" fill="url(#knopfmetall)"/>',
             f'<circle cx="{x:g}" cy="{y:g}" r="10.5" fill="#2b2e33"/>',
             f'<circle cx="{x:g}" cy="{y:g}" r="10.5" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="1.5"/>',
             f'<circle cx="{x:g}" cy="{y:g}" r="5.5" fill="#030304"/>']
    if gesteckt:
        teile.append(f'<circle cx="{x:g}" cy="{y:g}" r="9" fill="{gesteckt}"/>'
                     f'<circle cx="{x:g}" cy="{y:g}" r="9" fill="url(#mulde)" opacity=".6"/>'
                     f'<circle cx="{x - 2.5:g}" cy="{y - 3:g}" r="2.5" fill="#fff" opacity=".55"/>')
    return "".join(teile)


def steckfeld(auswahl: Auswahl) -> str:
    b, h = VOLL, 158
    teile = [_gestell(b, h), gravurtext(62, 34, "TECHNIK", 11, GRAVUR, 700, 4),
             gravurtext(b - OHR - 26, 34, "STECKFELD  ·  8 KANÄLE", 10, GRAVUR_STUMM, 700, 2, "end")]
    teile.append(f'<path d="M62,46H{b - OHR - 26}" stroke="#000" stroke-opacity=".6"/>'
                 f'<path d="M62,47H{b - OHR - 26}" stroke="#fff" stroke-opacity=".07"/>')
    anzahl = len(auswahl.technik)
    abstand = (b - 2 * OHR - 80) / (anzahl - 1)
    xs = [OHR + 40 + n * abstand for n in range(anzahl)]
    kabel = {0: (2, BERNSTEIN), 4: (7, CYAN)}
    gesteckt = {i: farbe for start, (ende, farbe) in kabel.items() for i in (start, ende)}
    for n, (x, wort) in enumerate(zip(xs, auswahl.technik)):
        teile.append(gravurtext(x, 72, wort.upper(), 9.5, GRAVUR_LEISE, 700, 1.2, "middle"))
        teile.append(_buchse(x, 100, gesteckt.get(n)))
    for start, (ende, farbe) in kabel.items():
        x1, x2 = xs[start], xs[ende]
        d = f"M{x1:.1f},104 C{x1:.1f},160 {x2:.1f},160 {x2:.1f},104"
        teile.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="8" '
                     f'transform="translate(0,4)"/>')
        teile.append(f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="5" stroke-linecap="round"/>')
        teile.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.2" '
                     f'transform="translate(-1,-1.5)"/>')
    return svg(b, h, "Technik: " + ", ".join(auswahl.technik), "".join(teile), _defs())


def _herz(x: float, y: float, farbe: str) -> str:
    return (f'<path d="M{x},{y + 4} c-2-4-8-4-8 1 c0 4 5 7 8 9 c3-2 8-5 8-9 c0-5-6-5-8-1z" '
            f'fill="{farbe}" transform="translate(0,-7)"/>')


def taste_breit(beschriftung: str, symbol: str) -> str:
    b, h = HALB, 66
    teile = [f'<path d="{fase(0, 0, b, h, 7)}" fill="{KANTE_DUNKEL}"/>', platte(fase(2, 2, b - 4, h - 4, 6))]
    for x, y in ((16, 33), (b - 16, 33)):
        teile.append(schraube(x, y, 40, 4.6))
    teile.append(led(48, 33, BERNSTEIN, 3))
    taste = fase(68, 15, b - 106, 36, 4)
    teile.append(f'<path d="{fase(66, 13, b - 102, 41, 5)}" fill="#000" opacity=".7"/>')
    teile.append(f'<path d="{taste}" fill="url(#taste_dunkel)"/>')
    teile.append(f'<path d="M72,16H{b - 42}" stroke="#fff" stroke-opacity=".28"/>')
    mitte = 68 + (b - 106) / 2
    teile.append(text(mitte + 8, 38, beschriftung, 13, GRAVUR, 700, 3, "middle"))
    breite = textbreite(beschriftung, 13, 3)
    sx = mitte - breite / 2 - 14
    if symbol == "herz":
        teile.append(_herz(sx, 33, BERNSTEIN))
    else:
        teile.append(f'<path d="M{sx - 5:g},27 l9,6 l-9,6z" fill="{BERNSTEIN}"/>')
    return svg(b, h, beschriftung, "".join(teile), _defs())


def bauen(auswahl: Auswahl) -> Ergebnis:
    e = Ergebnis(STECKBRIEF.kennung)
    e.dateien["avatar.svg"] = avatar(BERNSTEIN)
    e.zeile((e.bild("kopf.svg", kopf(auswahl)), VOLL, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", None))
    e.zeile((e.bild("abschnitt.svg", abschnitt("AUSGEWÄHLTE PROJEKTE", f"{len(auswahl.projekte):02d} EINSCHÜBE")),
             VOLL, "Ausgewählte Projekte", None))
    projekte = auswahl.projekte
    for i in range(0, len(projekte), 2):
        paar = projekte[i:i + 2]
        e.zeile(*((e.bild(f"{p.schluessel}.svg", einschub(p, i + n + 1)), HALB, f"{p.name}: {p.info}", p.ziel)
                  for n, p in enumerate(paar)))
    e.zeile((e.bild("technik.svg", steckfeld(auswahl)), VOLL, "Technik: " + ", ".join(auswahl.technik), None))
    e.zeile((e.bild("alle.svg", taste_breit("ALLE PROJEKTE", "pfeil")), HALB, "Alle Projekte", auswahl.link_alle),
            (e.bild("unterstuetzen.svg", taste_breit("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             auswahl.link_unterstuetzen))
    return e

