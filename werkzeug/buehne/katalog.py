"""Katalogseite projekte.md im Rack-Stil der Profilseite (Entwurf K5 "Einschübe").

Aufbau: Kopf mit Themen-Radar und Bernstein-Anzeige, je Thema eine Leiste mit Kanalanzeige und einer LED je
Projekt, darunter die Projekte als Einschübe in halber Breite, am Ende die Archivlisten zum Aufklappen und die
Tasten "Zum Profil" und "Unterstützen".
"""
from __future__ import annotations

import html
from dataclasses import dataclass

from buehne.akzent import akzent
from buehne.ergebnis import HALB, VOLL, Ergebnis
from buehne.glas import defs_glas
from buehne.material import (BERNSTEIN, BERNSTEIN_HELL, CYAN, GRAVUR, GRAVUR_LEISE, GRAVUR_STUMM, GRUEN,
                             KANTE_DUNKEL, defs_grund, fase, gravurtext, icon, led, mulde, platte, schraube,
                             spiegelung, svg, text, umbrechen)
from buehne.ortung import ortungsschirm
from buehne.rack import OHR, abspielfeld, defs_rack, fassungsplatte, gestell, taste_breit
from projekte import Gruppe, Liste, Profil, Projekt, repo_adresse

PROFIL = "https://github.com/HalloWelt42"
JE_ZEILE = 2
ARCHIVTEXT = "Kleinere Werkzeuge und Übungen, zum Aufklappen"
THEMENFARBEN = (CYAN, BERNSTEIN, "#5b9dff", GRUEN, "#b76bff", "#ff8a4c", "#2ee6d6", "#ff5d8f")
BEWEGUNG_PULS = (".puls{animation:puls 1.6s steps(2,jump-none) infinite}"
                 "@keyframes puls{0%{opacity:1}50%{opacity:.25}100%{opacity:1}}")


@dataclass(frozen=True)
class Ziel:
    """Ein Punkt auf dem Ortungsschirm: hier ein Thema statt eines Projekts."""
    name: str
    akzent: str


def defs() -> str:
    return defs_grund() + defs_rack() + defs_glas()


def themenleisten(profil: Profil) -> list[tuple[Gruppe, str, str]]:
    """Je Thema: (Gruppe, Kennung 01, 02 ..., Farbe wie auf dem Schirm)."""
    gruppen = profil.katalog_gruppen
    return [(g, f"{n + 1:02d}", THEMENFARBEN[n % len(THEMENFARBEN)]) for n, g in enumerate(gruppen)]


def zielart(link: str) -> str:
    """Wohin ein Projekt führt, als kurzes Schild: Live-Seite, Store-Eintrag oder Repo."""
    if "github.io" in link:
        return "LIVE"
    if "chromewebstore" in link or "addons.mozilla" in link:
        return "STORE"
    return "REPO"


def passende_groesse(inhalt: str, groesse: float, breite: float, sperrung: float = 0) -> float:
    """Schriftgröße, bei der inhalt in breite passt (höchstens groesse)."""
    return min(groesse, breite / max(len(inhalt), 1) / (.6 + sperrung / max(groesse, 1)))


def kopf(profil: Profil, musik: str | None = None, dauer: str | None = None) -> str:
    """Kopf als Rack-Frontplatte: Themen-Radar in der Fassung, daneben die Bernstein-Anzeige.

    musik: Titel für das Abspielfeld in der Freifläche unter der Anzeige; ohne Titel steht dort der Leitsatz."""
    b, h = VOLL, 240
    gruppen = profil.katalog_gruppen
    anzahl = sum(len(g.projekte) for g in gruppen)
    teile = [gestell(b, h), fassungsplatte(52, 26, 200, 200)]
    ziele = tuple(Ziel(g.titel, farbe) for g, _, farbe in themenleisten(profil))
    schirm, bewegung = ortungsschirm(152, 126, 76, ziele, kanalnummern=True)
    teile.append(schirm)
    teile.append(led(282, 28, GRUEN, 2.6))
    teile.append(gravurtext(292, 32, "KATALOG", 9.5, GRAVUR_STUMM, 700, 2))
    teile.append(gravurtext(b - OHR - 26, 32, "HW-42  ·  ALLE KANÄLE", 9.5, GRAVUR_STUMM, 700, 2, "end"))
    anzeige = fase(282, 44, 494, 104, 5)
    teile.append(f'<path d="{fase(276, 38, 506, 116, 7)}" fill="#0b0c0e"/>')
    teile.append(mulde(anzeige))
    teile.append(f'<path d="{anzeige}" fill="url(#punktraster)"/>')
    teile.append(text(302, 106, "ALLE PROJEKTE", 42, "#ffb547", 700, 3, extra='filter="url(#leuchten)"'))
    teile.append(text(304, 134, f"{anzahl} PROJEKTE  ·  {len(gruppen)} THEMEN  ·  SELBST GEHOSTET", 12, BERNSTEIN_HELL,
                      600, 1.6, extra='opacity=".7"'))
    teile.append(spiegelung(anzeige))
    teile.append(gravurtext(282, 184, "Werkzeuge mit Studio-Optik.", 15, GRAVUR, 600))
    musik_bewegung = ""
    if musik:
        feld, musik_bewegung = abspielfeld(282, 194, 330, musik, dauer or "")
        teile.append(feld)
    else:
        teile.append(gravurtext(282, 206, "Die Nummern am Schirm sind die Themen.", 13, GRAVUR_LEISE, 500))
    for n, (beschriftung, farbe) in enumerate((("LOKAL", GRUEN), ("OFFEN", BERNSTEIN), ("SIGNAL", CYAN))):
        x = 650 + n * 54
        teile.append(led(x, 184, farbe, 3.2, blinken="puls" if farbe == CYAN else None))
        teile.append(gravurtext(x, 206, beschriftung, 9.5, GRAVUR_STUMM, 700, 1.2, "middle"))
    return svg(b, h, f"Alle Projekte: {anzahl} Projekte in {len(gruppen)} Themen", "".join(teile), defs(),
               bewegung=bewegung + BEWEGUNG_PULS + musik_bewegung)


def leiste(kennung: str, titel: str, zeile: str, anzahl: int, farbe: str) -> str:
    """Themenleiste als flache Rack-Platte: Kanalanzeige, Gravur, je Projekt eine LED."""
    b, h = VOLL, 64
    teile = [gestell(b, h)]
    teile.append(mulde(fase(56, 14, 54, 36, 4)))
    teile.append(text(83, 40, kennung, 22, farbe, 700, 1.5, "middle", 'filter="url(#leuchten)"'))
    teile.append(gravurtext(128, 30, titel.upper(), 15, GRAVUR, 700, 3))
    teile.append(gravurtext(128, 50, zeile, 12.5, GRAVUR_LEISE, 500))
    rechts = b - OHR - 30
    for n in range(anzahl):
        teile.append(led(rechts - n * 13, 32, farbe, 2.6))
    return svg(b, h, f"{titel}: {zeile}", "".join(teile), defs(), gewichte=(500, 700))


def _taste_klein(x: float, y: float, b: float, h: float, beschriftung: str) -> str:
    return (
        f'<path d="{fase(x - 2, y - 2, b + 4, h + 4, 4)}" fill="#000" opacity=".7"/>'
        f'<path d="{fase(x, y, b, h, 3)}" fill="url(#taste)"/>'
        f'<path d="M{x + 4},{y + 2}H{x + b - 4}" stroke="#fff" stroke-opacity=".6"/>'
        f'<path d="M{x + 8},{y + h / 2 - 5} l6,5 l-6,5z" fill="#2a1700"/>'
        + text(x + b / 2 + 6, y + h / 2 + 3.5, beschriftung, 9, "#2a1700", 700, .8, "middle")
    )


def einschub(projekt: Projekt, nummer: str) -> str:
    """Einschub in halber Breite: Icon im Glasfenster, Kanal, LED in der Projektfarbe, Taste mit dem Ziel."""
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
    teile.append(_taste_klein(b - 92, 14, 66, 24, zielart(projekt.ziel)))
    teile.append(gravurtext(108, 60, projekt.name, passende_groesse(projekt.name, 18, b - 130), GRAVUR, 700))
    for n, zeile in enumerate(umbrechen(projekt.info, 44, 2)):
        teile.append(gravurtext(108, 78 + n * 15, zeile, 12, GRAVUR_LEISE, 500))
    return svg(b, h, f"{projekt.name}: {projekt.info}", "".join(teile), defs(), gewichte=(500, 700))


def liste_md(liste: Liste) -> str:
    punkte = "\n".join(f"- [{e.repo}]({repo_adresse(e.repo)}) - {e.info}" for e in liste.eintraege)
    return (
        f"<details>\n<summary><b>{html.escape(liste.titel)}</b> ({len(liste.eintraege)})</summary>\n\n"
        f"{punkte}\n\n</details>"
    )


def bauen(profil: Profil, ordner: str) -> Ergebnis:
    """ordner: Ablage der Bilder, relativ zu projekte.md (Pfadanfang der Bildadressen)."""
    e = Ergebnis(ordner, stapeln=True)
    musik = profil.angaben.musik if profil.angaben.musik and profil.angaben.musik.an("katalog") else None
    e.zeile((e.bild("kopf.svg", kopf(profil, musik.titel.upper() if musik else None, musik.dauer if musik else None)),
             VOLL, f"Alle Projekte{' - Musik abspielen' if musik else ''}", musik.link if musik else None))
    for gruppe, kennung, farbe in themenleisten(profil):
        e.zeile((e.bild(f"thema-{kennung}.svg", leiste(kennung, gruppe.titel, gruppe.text, len(gruppe.projekte),
                                                        farbe)), VOLL, f"{gruppe.titel}: {gruppe.text}", None))
        projekte = gruppe.projekte
        for start in range(0, len(projekte), JE_ZEILE):
            e.zeile(*((e.bild(f"{p.schluessel}.svg", einschub(p, f"{kennung}.{start + n + 1:02d}")), HALB,
                       f"{p.name}: {p.info}", p.ziel)
                      for n, p in enumerate(projekte[start:start + JE_ZEILE])))
    for n, liste in enumerate(profil.listen, start=1):
        e.zeile((e.bild(f"archiv-{n}.svg", leiste(f"A{n}", liste.titel, ARCHIVTEXT, 0, GRAVUR_LEISE)), VOLL,
                 liste.titel, None))
        e.text(liste_md(liste))
    e.zeile((e.bild("profil.svg", taste_breit("ZUM PROFIL", "pfeil")), HALB, "Zurück zum Profil", PROFIL),
            (e.bild("unterstuetzen.svg", taste_breit("UNTERSTÜTZEN", "herz")), HALB, "Unterstützen",
             profil.angaben.unterstuetzen))
    return e
