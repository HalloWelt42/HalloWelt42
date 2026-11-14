"""Rack "Regie" der Profilseite: Kopf mit Ortungsschirm, Signalmonitor, Fokus-Einschub, flache Einschübe,
Steckfeld und Tasten, dicht gestapelt. Liefert Bilder und README-Ausschnitt über buehne.ergebnis."""
from __future__ import annotations

from buehne.auswahl import Auswahl
from buehne.ergebnis import HALB, VOLL, Ergebnis
from buehne.kern import profilbild_kern
from buehne.material import (BERNSTEIN, BERNSTEIN_HELL, CYAN, GRAVUR, GRAVUR_LEISE, GRAVUR_STUMM, GRUEN,
                             KANTE_DUNKEL, bild, defs_grund, drehknopf, fase, gravurtext, icon, led, mulde, platte,
                             schraube, spiegelung, svg, text, umbrechen)
from buehne.ortung import UMLAUF, defs_glas, ortungsschirm, peilung
from buehne.rack import OHR, abschnitt, defs_rack, gestell, schild, steckfeld, taste_breit, vu
from projekte import Projekt

ZIEL_TINTE = "#d8f4f8"


BEWEGUNG_RACK = (".puls{animation:puls 1.6s steps(2,jump-none) infinite}"
                 "@keyframes puls{0%{opacity:1}50%{opacity:.25}100%{opacity:1}}")


def _defs() -> str:
    return defs_grund() + defs_rack() + defs_glas()


def _fassungsplatte(x: float, y: float, b: float, h: float) -> str:
    """Eingesetzte Unterplatte mit vier Schrauben, etwa für Schirm oder Bildschirmfoto."""
    return (
        f'<path d="{fase(x - 2, y - 2, b + 4, h + 4, 12)}" fill="{KANTE_DUNKEL}"/>'
        + platte(fase(x, y, b, h, 11))
        + "".join(schraube(sx, sy, 20 + 30 * i, 4.4) for i, (sx, sy) in enumerate(
            ((x + 12, y + 12), (x + b - 12, y + 12), (x + b - 12, y + h - 12), (x + 12, y + h - 12))))
    )


def kopf(auswahl: Auswahl) -> str:
    b, h = VOLL, 300
    teile = [gestell(b, h), _fassungsplatte(52, 34, 236, 236)]
    schirm, schirm_bewegung = ortungsschirm(170, 152, 92, auswahl.projekte, kanalnummern=True)
    teile.append(schirm)
    teile.append(led(70, 24, GRUEN, 2.6))
    teile.append(gravurtext(80, 28, "BETRIEB", 9.5, GRAVUR_STUMM, 700, 2))
    teile.append(gravurtext(b - OHR - 34, 28, "HW-42  ·  REGIE  ·  2026", 9.5, GRAVUR_STUMM, 700, 2, "end"))
    # Leuchtanzeige
    anzeige = fase(310, 42, 462, 124, 5)
    teile.append(f'<path d="{fase(304, 36, 474, 136, 7)}" fill="#0b0c0e"/>')
    teile.append(mulde(anzeige))
    teile.append(f'<path d="{anzeige}" fill="url(#punktraster)"/>')
    teile.append(text(332, 68, "PROFIL", 9, BERNSTEIN, 700, 3, extra='opacity=".55"'))
    teile.append(text(330, 122, "HALLOWELT42", 46, "#ffb547", 700, 3, extra='filter="url(#leuchten)"'))
    teile.append(text(333, 150, "SOFTWARE  ·  HIFI-OBERFLÄCHEN  ·  LOKALE KI", 12, BERNSTEIN_HELL, 600, 1.6,
                      extra='opacity=".7"'))
    teile.append(spiegelung(anzeige))
    # Leitsatz und Anzeigen
    teile.append(gravurtext(310, 206, "Werkzeuge mit Studio-Optik.", 16, GRAVUR, 600))
    teile.append(gravurtext(310, 230, "Selbst gehostet, ohne Cloud,", 13, GRAVUR_LEISE, 500))
    teile.append(gravurtext(310, 248, "ohne Tracking, auf eigener Hardware.", 13, GRAVUR_LEISE, 500))
    for n, (beschriftung, farbe, blinken) in enumerate((("LOKAL", GRUEN, None), ("OFFEN", BERNSTEIN, None),
                                                         ("SIGNAL", CYAN, "puls"))):
        x = 622 + n * 66
        teile.append(led(x, 206, farbe, 3.4, blinken=blinken))
        teile.append(gravurtext(x, 229, beschriftung, 9.5, GRAVUR_STUMM, 700, 1.2, "middle"))
    teile.append(f'<path d="M596,252H772" stroke="#000" stroke-opacity=".6"/><path d="M596,253H772" stroke="#fff" '
                 'stroke-opacity=".07"/>')
    teile.append(gravurtext(684, 272, f"{auswahl.anzahl_gesamt} PROJEKTE  ·  {auswahl.anzahl_themen} THEMEN",
                            9.5, GRAVUR_STUMM, 700, 1.6, "middle"))
    return svg(b, h, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", "".join(teile), _defs(),
               bewegung=schirm_bewegung + BEWEGUNG_RACK)


def signalmonitor(auswahl: Auswahl) -> str:
    b, h = VOLL, 252
    teile = [gestell(b, h)]
    teile.append(gravurtext(62, 26, "SIGNALMONITOR", 9.5, GRAVUR_STUMM, 700, 2.5))
    teile.append(gravurtext(b - OHR - 26, 26, "ORTUNG  ·  PEGEL", 9.5, GRAVUR_STUMM, 700, 2.5, "end"))
    # Zielliste zum Ortungsschirm im Kopf, Peilung aus derselben Quelle
    lx, lb = 56, 452
    links, rechts = lx + 16, lx + lb - 16
    liste = fase(lx, 38, lb, 196, 5)
    teile.append(f'<path d="{fase(lx - 5, 33, lb + 10, 206, 7)}" fill="#0b0c0e"/>')
    teile.append(mulde(liste, "#040a0d"))
    teile.append(text(links, 62, "ORTUNG", 10, CYAN, 700, 3))
    teile.append(text(links + 182, 62, "TECHNIK", 10, CYAN, 700, 3, extra='opacity=".7"'))
    teile.append(text(rechts, 62, f"{len(auswahl.projekte):02d} ZIELE", 10, CYAN, 700, 2, "end",
                      'opacity=".7"'))
    teile.append(f'<path d="M{links},72H{rechts}" stroke="{CYAN}" stroke-opacity=".25"/>')
    stile = []
    zeilenhoehe = min(36, 150 / max(len(auswahl.projekte), 1))
    for n, p in enumerate(auswahl.projekte):
        y = 80 + n * zeilenhoehe
        winkel, _ = peilung(n)
        teile.append(f'<rect class="zeile{n}" x="{lx + 8}" y="{y:.1f}" width="{lb - 16}" height="{zeilenhoehe - 4:.1f}" rx="2" '
                     f'fill="{p.akzent}" fill-opacity=".1"/>')
        mitte = y + (zeilenhoehe - 4) / 2
        teile.append(text(links + 2, mitte + 6, f"{n + 1:02d}", 16, "#ffb547", 700, 1, extra='filter="url(#leuchten)"'))
        teile.append(f'<circle cx="{links + 36}" cy="{mitte:.1f}" r="3.2" fill="{p.akzent}" filter="url(#leuchten)"/>')
        teile.append(text(links + 48, mitte + 4.5, p.name.upper(), 12, ZIEL_TINTE, 700, .6))
        teile.append(text(links + 182, mitte + 4.5, "  ·  ".join(t.upper() for t in p.technik), 10, GRAVUR_LEISE,
                          600, 1.2))
        teile.append(text(rechts, mitte + 4.5, f"{winkel % 360:03.0f}°", 11, CYAN, 600, .5, "end", 'opacity=".8"'))
        stile.append(f".zeile{n}{{animation:zeile {UMLAUF:g}s linear infinite;"
                     f"animation-delay:{winkel % 360 / 360 * UMLAUF - UMLAUF:.2f}s}}")
    teile.append(spiegelung(liste))
    # VU-Meter
    grund, bewegung = [], []
    # Ein VU-Meter statt zwei, eine Listenzeile niedriger als die Zielliste, Breite im Verhältnis
    vu_hoehe = 140 - 36
    vu_breite = round(256 * vu_hoehe / 140)
    vu_x = 528 + (256 - vu_breite) / 2
    grafik, ruhe, nadel = vu(vu_x, 40, vu_breite, vu_hoehe, "L · R", 1)
    teile.append(grafik)
    grund.append(ruhe)
    bewegung.append(nadel)
    led_y = 40 + vu_hoehe + 30
    teile.append(led(vu_x + 14, led_y, GRUEN, 3))
    teile.append(gravurtext(vu_x + 26, led_y + 4, "SIGNAL", 9.5, GRAVUR_STUMM, 700, 1.4))
    teile.append(led(vu_x + vu_breite - 72, led_y, "#ff3b30", 3, blinken="spitze"))
    teile.append(gravurtext(vu_x + vu_breite - 60, led_y + 4, "SPITZE", 9.5, GRAVUR_STUMM, 700, 1.4))
    teile.append(drehknopf(vu_x + vu_breite / 2, led_y + 38, 13, 40))
    bewegung_gesamt = (
        "".join(bewegung) + "".join(stile)
        + "@keyframes zeile{0%{fill-opacity:.32}8%{fill-opacity:.32}50%{fill-opacity:.06}100%{fill-opacity:.32}}"
        + ".spitze{animation:spitze 3.55s steps(1) infinite}"
        "@keyframes spitze{0%{opacity:.15}44%{opacity:1}52%{opacity:.15}100%{opacity:.15}}"
    )
    return svg(b, h, "Signalmonitor: " + ", ".join(p.name for p in auswahl.projekte), "".join(teile), _defs(),
               "".join(grund), bewegung_gesamt)


def fokus(projekt: Projekt) -> str:
    b, h = VOLL, 330
    teile = [gestell(b, h)]
    teile.append(gravurtext(62, 52, "IM FOKUS  ·  KANAL 01", 10, BERNSTEIN, 700, 3))
    teile.append(gravurtext(60, 100, projekt.name, 40, GRAVUR, 700, .5))
    for n, zeile in enumerate(umbrechen(projekt.info, 40, 3)):  # bis zu drei Zeilen, bevor die Stärken beginnen
        teile.append(gravurtext(62, 128 + n * 19, zeile, 15, GRAVUR_LEISE, 500))
    for n, punkt in enumerate(projekt.punkte):
        y = 196 + n * 25
        teile.append(led(68, y - 5, BERNSTEIN, 3))
        teile.append(gravurtext(82, y, punkt, 14, "#d9dee3", 500))
    x = 62.0
    for wort in projekt.technik:
        marke, breite = schild(x, 270, wort)
        teile.append(marke)
        x += breite + 6
    taste = fase(x + 8, 266, 70, 27, 3)
    teile.append(f'<path d="{fase(x + 6, 264, 74, 31, 4)}" fill="#000" opacity=".7"/>')
    teile.append(f'<path d="{taste}" fill="url(#taste)"/>')
    teile.append(f'<path d="M{x + 12},268H{x + 74}" stroke="#fff" stroke-opacity=".6"/>')
    teile.append(f'<path d="M{x + 18},274 l7,5.5 l-7,5.5z" fill="#2a1700"/>')
    teile.append(text(x + 52, 283.5, "ÖFFNEN", 8.5, "#2a1700", 700, .8, "middle"))
    # Bildschirmfoto im Rack-Fenster
    if projekt.bild_pfad:
        teile.append(_fassungsplatte(394, 30, 394, 252))
        fx, fy, fb, fh = 410, 46, 362, 211
        fenster = fase(fx, fy, fb, fh, 5)
        teile.append(f'<path d="{fase(fx - 4, fy - 4, fb + 8, fh + 8, 7)}" fill="#0b0c0e"/>')
        teile.append(f'<clipPath id="foto"><path d="{fenster}"/></clipPath>')
        teile.append(f'<path d="{fenster}" fill="#111418"/>')
        teile.append(bild(projekt.bild_pfad, fx, fy, fb, fh, "foto"))
        teile.append(f'<path d="{fenster}" fill="none" stroke="url(#mulde)" stroke-width="2.4"/>')
        teile.append(spiegelung(fenster))
        teile.append(gravurtext(fx, 304, "VORSCHAU  ·  RECHNER, HANDY UND UHR", 9.5, GRAVUR_STUMM, 700, 1.6))
        teile.append(led(fx + fb - 4, 300, GRUEN, 2.6))
    return svg(b, h, f"Im Fokus: {projekt.name}, {projekt.info}", "".join(teile), _defs(), bewegung="")


def einschub_flach(projekt: Projekt, kanal: int) -> str:
    """Flacher Einschub über die volle Breite: Icon, Kanal, Name und Text, rechts Schlagworte und Taste."""
    b, h = VOLL, 100
    teile = [gestell(b, h)]
    teile.append(f'<path d="{fase(56, 10, 80, 80, 7)}" fill="#0b0c0e"/>')
    fenster = fase(60, 14, 72, 72, 5)
    teile.append(mulde(fenster))
    teile.append(f'<circle cx="96" cy="50" r="30" fill="{projekt.akzent}" opacity=".08" filter="url(#leuchten_weit)"/>')
    teile.append(icon(projekt.icon_pfad, 71, 25, 50))
    teile.append(spiegelung(fenster))
    teile.append(mulde(fase(156, 20, 50, 26, 3)))
    teile.append(text(181, 40, f"{kanal:02d}", 19, "#ffb547", 700, 2, "middle", 'filter="url(#leuchten)"'))
    teile.append(gravurtext(181, 66, "KANAL", 9.5, GRAVUR_STUMM, 700, 2, "middle"))
    teile.append(led(181, 80, BERNSTEIN, 2))
    teile.append(gravurtext(232, 40, projekt.name, 22, GRAVUR, 700))
    for n, zeile in enumerate(umbrechen(projekt.info, 56)):
        teile.append(gravurtext(232, 63 + n * 17, zeile, 13, GRAVUR_LEISE, 500))
    # Schlagworte rechtsbündig über der Taste
    rechts = b - OHR - 28
    marken, x = [], float(rechts)
    for wort in reversed(projekt.technik):
        breite = schild(0, 0, wort)[1]
        if x - breite < 440:  # bis an den Namen heran, nie darüber
            break
        x -= breite
        marken.append(schild(x, 18, wort)[0])
        x -= 6
    teile += marken
    taste = fase(rechts - 76, 54, 76, 28, 3)
    teile.append(f'<path d="{fase(rechts - 78, 52, 80, 32, 4)}" fill="#000" opacity=".7"/>')
    teile.append(f'<path d="{taste}" fill="url(#taste)"/>')
    teile.append(f'<path d="M{rechts - 72},56H{rechts - 4}" stroke="#fff" stroke-opacity=".6"/>')
    teile.append(f'<path d="M{rechts - 64},62.5 l7,5.5 l-7,5.5z" fill="#2a1700"/>')
    teile.append(text(rechts - 34, 72, "ÖFFNEN", 9, "#2a1700", 700, .8, "middle"))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), _defs())


def bauen(auswahl: Auswahl, ordner: str) -> Ergebnis:
    """ordner: Ablage der Bilder, relativ zur README (Pfadanfang der Bildadressen)."""
    e = Ergebnis(ordner, stapeln=True)
    e.dateien["avatar.svg"] = profilbild_kern()
    e.zeile((e.bild("kopf.svg", kopf(auswahl)), VOLL, "HalloWelt42: Software, HiFi-Oberflächen, lokale KI", None))
    e.zeile((e.bild("monitor.svg", signalmonitor(auswahl)), VOLL,
             "Signalmonitor: " + ", ".join(p.name for p in auswahl.projekte), None))
    e.zeile((e.bild("abschnitt.svg", abschnitt("AUSGEWÄHLTE PROJEKTE", f"{len(auswahl.projekte):02d} KANÄLE")),
             VOLL, "Ausgewählte Projekte", None))
    f = auswahl.fokus
    e.zeile((e.bild(f"{f.schluessel}.svg", fokus(f)), VOLL, f"{f.name}: {f.info}", f.ziel))
    for kanal, p in enumerate(auswahl.ohne_fokus, start=2):
        e.zeile((e.bild(f"{p.schluessel}.svg", einschub_flach(p, kanal)), VOLL, f"{p.name}: {p.info}", p.ziel))
    e.zeile((e.bild("technik.svg", steckfeld(auswahl)), VOLL, "Technik: " + ", ".join(auswahl.technik), None))
    e.zeile((e.bild("alle.svg", taste_breit("ALLE PROJEKTE", "pfeil")), HALB, "Alle Projekte", auswahl.link_alle),
            (e.bild("unterstuetzen.svg", taste_breit("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             auswahl.link_unterstuetzen))
    return e
