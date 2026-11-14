"""Entwurf A "Studio-Rack": das Profil als 19-Zoll-Gerät, jedes Projekt ein Einschub."""
from __future__ import annotations

import pfad  # noqa: F401  (macht werkzeug/ importierbar)
from buehne.auswahl import Auswahl
from buehne.ergebnis import HALB, VOLL, Ergebnis
from steckbrief import Steckbrief
from buehne.material import (BERNSTEIN, BERNSTEIN_HELL, CYAN, GRAVUR, GRAVUR_LEISE, GRAVUR_STUMM, GRUEN, KANTE_DUNKEL, avatar,
                             drehknopf, fase, gravurtext, icon, led, mulde, platte, schraube, spiegelung, svg, text,
                             umbrechen)
from buehne.rack import OHR, abschnitt, defs, gestell, schild, steckfeld, taste_breit, vu
from projekte import Projekt

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


def kopf(auswahl: Auswahl) -> str:
    b, h = VOLL, 300
    teile = [gestell(b, h)]
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
        grafik, grund, bewegung = vu(x, 42, 140, 140, kanal, nummer)
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
    return svg(b, h, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", "".join(teile), defs(), stil, bewegung)


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
    teile.append(icon(projekt.icon_pfad, 50, 54, 60))
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
        marke, breite = schild(x, 128, wort)
        if x + breite > b - 92:
            break
        teile.append(marke)
        x += breite + 6
    # Taste
    taste = fase(b - 82, 124, 58, 27, 3)
    teile.append(f'<path d="{fase(b - 84, 122, 62, 31, 4)}" fill="#000" opacity=".7"/>')
    teile.append(f'<path d="{taste}" fill="url(#taste)"/>')
    teile.append(f'<path d="M{b - 79},126H{b - 27}" stroke="#fff" stroke-opacity=".6"/>')
    teile.append(f'<path d="M{b - 72},132 l7,5.5 l-7,5.5z" fill="#2a1700"/>')
    teile.append(text(b - 44, 141.5, "ÖFFNEN", 8.5, "#2a1700", 700, .8, "middle"))
    teile.append(led(b - 53, 166, BERNSTEIN, 1.8))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), defs())


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

