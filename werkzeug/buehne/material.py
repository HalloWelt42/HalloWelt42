"""Gemeinsame Bausteine aller Entwurfs-SVGs: Schrift, Kanten, Material, Licht, kleine Bauteile.

Jedes SVG muss für sich stehen, weil GitHub es als <img> lädt: keine Nachladungen, Schrift und
Bilder werden eingebettet. Animationen laufen per CSS oder SMIL im SVG selbst.
"""
from __future__ import annotations

import base64
import html
import math
import pathlib

from projekte import WURZEL

SCHRIFTORDNER = WURZEL / "portfolio/node_modules/@fontsource/chakra-petch/files"
SCHRIFT = "'Chakra Petch',sans-serif"
MEDIENTYPEN = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".woff2": "font/woff2"}

# Palette Anthrazit, eine Wahrheit für alle drei Entwürfe
KANTE_DUNKEL = "#08090a"
PLATTE_OBEN = "#34383d"
PLATTE_MITTE = "#25282c"
PLATTE_UNTEN = "#1b1d20"
GRAVUR = "#e9edf1"
GRAVUR_LEISE = "#9aa3ad"
GRAVUR_STUMM = "#8a929b"
BERNSTEIN = "#ffae1a"
BERNSTEIN_HELL = "#ffcf6b"
CYAN = "#5ff2ff"
GRUEN = "#36e46f"
MESSING = "#c9a86a"
MESSING_HELL = "#ecd3a0"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def daten_url(pfad: pathlib.Path) -> str:
    inhalt = base64.b64encode(pathlib.Path(pfad).read_bytes()).decode("ascii")
    return f"data:{MEDIENTYPEN[pfad.suffix]};base64,{inhalt}"


def schriften(*gewichte: int) -> str:
    regeln = "".join(
        "@font-face{font-family:'Chakra Petch';font-style:normal;"
        f"font-weight:{g};src:url({daten_url(SCHRIFTORDNER / f'chakra-petch-latin-{g}-normal.woff2')}) format('woff2')}}"
        for g in gewichte
    )
    return regeln


def svg(breite: int, hoehe: int, titel: str, inhalt: str, defs: str = "", stil: str = "",
        bewegung: str = "", gewichte: tuple[int, ...] = (400, 600, 700)) -> str:
    """bewegung: CSS-Animationen; sie laufen nur, wenn der Betrachter Bewegung nicht abgeschaltet hat."""
    bewegt = f"@media (prefers-reduced-motion:no-preference){{{bewegung}}}" if bewegung else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" '
        f'viewBox="0 0 {breite} {hoehe}" role="img" aria-label="{esc(titel)}">'
        f"<title>{esc(titel)}</title>"
        f"<style>{schriften(*gewichte)}text{{font-family:{SCHRIFT}}}{stil}{bewegt}</style>"
        f"<defs>{defs}</defs>{inhalt}</svg>\n"
    )


def umbrechen(text: str, zeichen: int, zeilen: int = 2) -> list[str]:
    """Bricht an Wortgrenzen um; kürzt die letzte Zeile mit Auslassung, wenn der Platz endet."""
    woerter, ergebnis, zeile = text.split(), [], ""
    for wort in woerter:
        probe = f"{zeile} {wort}".strip()
        if len(probe) <= zeichen:
            zeile = probe
            continue
        ergebnis.append(zeile)
        zeile = wort
    ergebnis.append(zeile)
    if len(ergebnis) > zeilen:
        rest = " ".join(ergebnis[zeilen - 1:])
        ergebnis = ergebnis[: zeilen - 1] + [rest[: zeichen - 3].rstrip(" ,:") + " ..."]
    return ergebnis


def textbreite(text: str, groesse: float, sperrung: float = 0, faktor: float = 0.58) -> float:
    """Schätzt die Laufweite von Chakra Petch; reicht für Abstände, nicht für Satz."""
    return len(text) * (groesse * faktor + sperrung)


# ---------- Geometrie ----------

def fase(x: float, y: float, b: float, h: float, ecken: float | tuple[float, float, float, float]) -> str:
    """Pfad eines Rechtecks mit 45-Grad-Fasen; ecken: oben links, oben rechts, unten rechts, unten links."""
    ol, or_, ur, ul = (ecken,) * 4 if isinstance(ecken, (int, float)) else ecken
    return (
        f"M{x + ol:g},{y:g} H{x + b - or_:g} L{x + b:g},{y + or_:g} V{y + h - ur:g} "
        f"L{x + b - ur:g},{y + h:g} H{x + ul:g} L{x:g},{y + h - ul:g} V{y + ol:g} Z"
    )


def polar(cx: float, cy: float, r: float, grad: float) -> tuple[float, float]:
    w = math.radians(grad - 90)
    return cx + r * math.cos(w), cy + r * math.sin(w)


def bogen(cx: float, cy: float, r: float, von: float, bis: float) -> str:
    x1, y1 = polar(cx, cy, r, von)
    x2, y2 = polar(cx, cy, r, bis)
    gross = 1 if (bis - von) % 360 > 180 else 0
    return f"M{x1:.2f},{y1:.2f} A{r},{r} 0 {gross} 1 {x2:.2f},{y2:.2f}"


# ---------- Material und Licht (defs) ----------

def defs_grund() -> str:
    """Verläufe und Filter, die fast jedes Teil braucht."""
    return (
        # Pulverlack-Anthrazit, Licht von oben
        f'<linearGradient id="platte" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{PLATTE_OBEN}"/><stop offset=".45" stop-color="{PLATTE_MITTE}"/>'
        f'<stop offset="1" stop-color="{PLATTE_UNTEN}"/></linearGradient>'
        # Lichtkante: oben links hell, unten rechts dunkel
        '<linearGradient id="lichtkante" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".35" stop-color="#fff" stop-opacity=".07"/>'
        '<stop offset=".65" stop-color="#000" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".75"/>'
        '</linearGradient>'
        # Vertiefung: oben dunkel, unten Lichtkante
        '<linearGradient id="mulde" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#000" stop-opacity=".9"/><stop offset=".6" stop-color="#000" stop-opacity=".3"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity=".22"/></linearGradient>'
        '<radialGradient id="glas" cx=".3" cy=".2" r="1.1">'
        '<stop offset="0" stop-color="#11161b"/><stop offset="1" stop-color="#040506"/></radialGradient>'
        '<linearGradient id="spiegelung" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity=".09"/><stop offset=".5" stop-color="#fff" stop-opacity=".02"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="schraubenkopf" cx=".35" cy=".3" r=".9">'
        '<stop offset="0" stop-color="#d9dde2"/><stop offset=".55" stop-color="#7d848c"/>'
        '<stop offset="1" stop-color="#363a3f"/></radialGradient>'
        '<radialGradient id="knopfmetall" cx=".38" cy=".28" r=".85">'
        '<stop offset="0" stop-color="#f1f3f5"/><stop offset=".5" stop-color="#9aa1a8"/>'
        '<stop offset="1" stop-color="#4c5258"/></radialGradient>'
        # Bürstung: feine waagrechte Riefen als Rauschen, nur innerhalb der Form
        '<filter id="buerste" x="0" y="0" width="1" height="1">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.0025 0.95" numOctaves="2" seed="7" result="rauschen"/>'
        '<feColorMatrix in="rauschen" type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0.34 0 0 0 -0.13" result="riefen"/>'
        '<feComposite in="riefen" in2="SourceGraphic" operator="in"/></filter>'
        '<filter id="leuchten" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="2.4" result="hof"/>'
        '<feMerge><feMergeNode in="hof"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="leuchten_weit" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="6" result="hof"/>'
        '<feMerge><feMergeNode in="hof"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="gravur" x="-5%" y="-20%" width="110%" height="140%">'
        '<feDropShadow dx="0" dy="1" stdDeviation="0" flood-color="#000" flood-opacity=".85"/></filter>'
        '<filter id="schatten" x="-10%" y="-10%" width="120%" height="140%">'
        '<feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".6"/></filter>'
    )


def platte(d: str, fuellung: str = "url(#platte)", buerste: bool = True, kante: bool = True) -> str:
    """Eine Metallplatte: Fläche, Bürstung, Lichtkante."""
    teile = [f'<path d="{d}" fill="{fuellung}"/>']
    if buerste:
        teile.append(f'<path d="{d}" fill="#fff" filter="url(#buerste)"/>')
    if kante:
        teile.append(f'<path d="{d}" fill="none" stroke="url(#lichtkante)" stroke-width="1.6"/>')
    return "".join(teile)


def mulde(d: str, innen: str = "url(#glas)") -> str:
    """In die Platte eingelassenes Fenster: dunkler Rand oben, Lichtkante unten."""
    return (
        f'<path d="{d}" fill="{innen}"/>'
        f'<path d="{d}" fill="none" stroke="url(#mulde)" stroke-width="2.2"/>'
    )


def spiegelung(d: str) -> str:
    return f'<path d="{d}" fill="url(#spiegelung)"/>'


def schraube(x: float, y: float, winkel: float = 20, r: float = 5) -> str:
    return (
        f'<g transform="translate({x:g},{y:g})">'
        f'<circle r="{r + 1.2:g}" fill="#000" opacity=".55"/>'
        f'<circle r="{r:g}" fill="url(#schraubenkopf)"/>'
        f'<g transform="rotate({winkel:g})" stroke="#2b2e32" stroke-width="1.3" stroke-linecap="round">'
        f'<path d="M{-r * .62:g},0H{r * .62:g}M0,{-r * .62:g}V{r * .62:g}"/></g></g>'
    )


def led(x: float, y: float, farbe: str, r: float = 3.2, an: bool = True, blinken: str | None = None) -> str:
    if not an:
        return (f'<circle cx="{x:g}" cy="{y:g}" r="{r + 1:g}" fill="#000" opacity=".6"/>'
                f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{farbe}" opacity=".18"/>')
    klasse = f' class="{blinken}"' if blinken else ""
    return (
        f'<circle cx="{x:g}" cy="{y:g}" r="{r + 1:g}" fill="#000" opacity=".6"/>'
        f'<g{klasse}><circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{farbe}" filter="url(#leuchten)"/>'
        f'<circle cx="{x - r * .3:g}" cy="{y - r * .35:g}" r="{r * .35:g}" fill="#fff" opacity=".75"/></g>'
    )


def text(x: float, y: float, inhalt: str, groesse: float, farbe: str, gewicht: int = 600,
         sperrung: float = 0, anker: str = "start", extra: str = "") -> str:
    return (
        f'<text x="{x:g}" y="{y:g}" font-size="{groesse:g}" font-weight="{gewicht}" fill="{farbe}" '
        f'letter-spacing="{sperrung:g}" text-anchor="{anker}" {extra}>{esc(inhalt)}</text>'
    )


def gravurtext(x: float, y: float, inhalt: str, groesse: float, farbe: str = GRAVUR, gewicht: int = 600,
               sperrung: float = 0, anker: str = "start") -> str:
    return text(x, y, inhalt, groesse, farbe, gewicht, sperrung, anker, 'filter="url(#gravur)"')


def icon(pfad: pathlib.Path, x: float, y: float, kante: float) -> str:
    return (f'<image href="{daten_url(pfad)}" x="{x:g}" y="{y:g}" width="{kante:g}" height="{kante:g}" '
            'preserveAspectRatio="xMidYMid meet"/>')


def bild(pfad: pathlib.Path, x: float, y: float, b: float, h: float, clip: str) -> str:
    return (f'<image href="{daten_url(pfad)}" x="{x:g}" y="{y:g}" width="{b:g}" height="{h:g}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip})"/>')


def drehknopf(cx: float, cy: float, r: float, stellung: float, akzent: str = BERNSTEIN) -> str:
    """Metallknopf mit Riffelrand und Skalenkranz; stellung in Grad (-135 bis 135)."""
    striche = "".join(
        f'<path d="M{polar(cx, cy, r + 5, g)[0]:.1f},{polar(cx, cy, r + 5, g)[1]:.1f} '
        f'L{polar(cx, cy, r + 9, g)[0]:.1f},{polar(cx, cy, r + 9, g)[1]:.1f}" stroke="{GRAVUR_STUMM}" stroke-width="1.2"/>'
        for g in range(-135, 136, 27)
    )
    zx, zy = polar(cx, cy, r * .72, stellung)
    return (
        f'{striche}<path d="{bogen(cx, cy, r + 7, -135, stellung)}" fill="none" stroke="{akzent}" '
        f'stroke-width="2" stroke-linecap="round" filter="url(#leuchten)" opacity=".9"/>'
        f'<circle cx="{cx:g}" cy="{cy + 2:g}" r="{r + 1:g}" fill="#000" opacity=".6"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="#2a2d31"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - 1:g}" fill="none" stroke="#5d636a" stroke-width="2.4" '
        f'stroke-dasharray="1.2 1.6"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .78:g}" fill="url(#knopfmetall)"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .78:g}" fill="none" stroke="#fff" stroke-opacity=".35"/>'
        f'<path d="M{cx:g},{cy:g} L{zx:.1f},{zy:.1f}" stroke="#1d1f22" stroke-width="2.6" stroke-linecap="round"/>'
    )


def avatar(akzent: str, gewicht: int = 700) -> str:
    """Profilbild-Vorschlag: Metallknopf mit leuchtendem Kranz und der 42 in der Mitte."""
    k, m = 460, 230
    kranz = "".join(
        f'<path d="M{polar(m, m, 196, g)[0]:.1f},{polar(m, m, 196, g)[1]:.1f} '
        f'L{polar(m, m, 212, g)[0]:.1f},{polar(m, m, 212, g)[1]:.1f}" stroke="{akzent if g <= 60 else "#4a5058"}" '
        f'stroke-width="5" stroke-linecap="round"/>'
        for g in range(-135, 136, 15)
    )
    inhalt = (
        f'<rect width="{k}" height="{k}" fill="#16181b"/>'
        f'<circle cx="{m}" cy="{m}" r="{m}" fill="url(#platte)"/>'
        f'<circle cx="{m}" cy="{m}" r="{m}" fill="#fff" filter="url(#buerste)"/>'
        f'<g filter="url(#leuchten)">{kranz}</g>'
        f'<circle cx="{m}" cy="{m + 6}" r="170" fill="#000" opacity=".55"/>'
        f'<circle cx="{m}" cy="{m}" r="168" fill="#24272b"/>'
        f'<circle cx="{m}" cy="{m}" r="164" fill="none" stroke="#5d636a" stroke-width="8" stroke-dasharray="3 5"/>'
        f'<circle cx="{m}" cy="{m}" r="140" fill="url(#glas)"/>'
        f'<circle cx="{m}" cy="{m}" r="140" fill="none" stroke="url(#mulde)" stroke-width="5"/>'
        + text(m, m + 52, "42", 150, akzent, gewicht, -4, "middle", 'filter="url(#leuchten_weit)"')
        + f'<path d="M{m - 140},{m} A140,140 0 0 1 {m + 140},{m} Z" fill="#fff" opacity=".05"/>'
    )
    return svg(k, k, "HalloWelt42", inhalt, defs_grund(), gewichte=(gewicht,))
