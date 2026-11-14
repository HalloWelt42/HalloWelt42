"""Der Kern: Logo als leuchtende Drahtkugel mit Ringen, Reaktorkranz und der 42 in der Mitte.

Ein Baustein für Kopf und Profilbild. Liefert Grafik, Grundstil (Ruhelage) und Bewegung getrennt, damit das
Profilbild still bleibt (GitHub nimmt dort nur PNG) und die Kopfgrafik sich dreht.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from material import BERNSTEIN, CYAN, bogen, polar, text

KERN_HELL = "#e9fdff"


@dataclass(frozen=True)
class Kern:
    grafik: str
    stil: str
    bewegung: str


def kern_defs(p: str) -> str:
    return (
        f'<radialGradient id="{p}schein" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".32"/><stop offset=".55" stop-color="{CYAN}" stop-opacity=".08"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="{p}herz" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="#0d3a44"/><stop offset=".7" stop-color="#04161c"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".9"/></radialGradient>'
        f'<radialGradient id="{p}kugel" cx=".38" cy=".3" r=".75">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="#021015" stop-opacity=".2"/>'
        '</radialGradient>'
    )


def _ursprung(cx: float, cy: float) -> str:
    return f"transform-box:view-box;transform-origin:{cx:g}px {cy:g}px"


def kern(cx: float, cy: float, r: float, p: str = "k") -> Kern:
    """r ist der Außenradius der Ringe; alles bleibt innerhalb davon."""
    teile, stile, bewegung = [], [], []
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#{p}schein)"/>')

    # Ring 1: Skala mit 72 Strichen, langsam rechts herum
    striche = []
    for n in range(72):
        g = n * 5
        lang = n % 6 == 0
        x1, y1 = polar(cx, cy, r * .97, g)
        x2, y2 = polar(cx, cy, r * (.88 if lang else .92), g)
        farbe = BERNSTEIN if n in (0, 36) else CYAN
        striche.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="{farbe}" '
                       f'stroke-opacity="{.95 if lang else .45}" stroke-width="{r * (.014 if lang else .009):.2f}"/>')
    teile.append(f'<g class="{p}r1">{"".join(striche)}</g>')
    stile.append(f".{p}r1{{{_ursprung(cx, cy)}}}")
    bewegung.append(f".{p}r1{{animation:{p}dreh 60s linear infinite}}")

    # Ring 2: gestrichelter Datenring, gegenläufig
    r2 = r * .83
    umfang = 2 * math.pi * r2
    teile.append(f'<circle class="{p}r2" cx="{cx:g}" cy="{cy:g}" r="{r2:.1f}" fill="none" stroke="{CYAN}" '
                 f'stroke-opacity=".75" stroke-width="{r * .035:.2f}" '
                 f'stroke-dasharray="{umfang * .09:.1f} {umfang * .015:.1f} {umfang * .03:.1f} {umfang * .015:.1f} '
                 f'{umfang * .012:.1f} {umfang * .03:.1f}" filter="url(#leuchten)"/>')
    stile.append(f".{p}r2{{{_ursprung(cx, cy)}}}")
    bewegung.append(f".{p}r2{{animation:{p}dreh 28s linear infinite reverse}}")

    # Ring 3: dünner Kreis mit drei Bögen und Markern, schneller
    r3 = r * .73
    boegen = "".join(
        f'<path d="{bogen(cx, cy, r3, s, s + 46)}" fill="none" stroke="{CYAN}" stroke-width="{r * .02:.2f}" '
        f'stroke-linecap="round"/>' for s in (10, 130, 250)
    )
    marker = "".join(
        f'<path d="M{polar(cx, cy, r3 + r * .05, g)[0]:.1f},{polar(cx, cy, r3 + r * .05, g)[1]:.1f} '
        f'L{polar(cx, cy, r3 + r * .1, g - 4)[0]:.1f},{polar(cx, cy, r3 + r * .1, g - 4)[1]:.1f} '
        f'L{polar(cx, cy, r3 + r * .1, g + 4)[0]:.1f},{polar(cx, cy, r3 + r * .1, g + 4)[1]:.1f}Z" fill="{BERNSTEIN}"/>'
        for g in (80, 200, 320)
    )
    teile.append(f'<g class="{p}r3"><circle cx="{cx:g}" cy="{cy:g}" r="{r3:.1f}" fill="none" stroke="{CYAN}" '
                 f'stroke-opacity=".3" stroke-width="{r * .007:.2f}"/>{boegen}{marker}</g>')
    stile.append(f".{p}r3{{{_ursprung(cx, cy)}}}")
    bewegung.append(f".{p}r3{{animation:{p}dreh 14s linear infinite}}")

    # Drahtkugel: Breitenkreise fest, Längenkreise drehen sich als gestauchte Ellipsen
    rk = r * .6
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rk:.1f}" fill="url(#{p}kugel)"/>')
    kugel = []
    for breite in (-60, -35, -12, 12, 35, 60):
        w = math.radians(breite)
        kugel.append(f'<ellipse cx="{cx:g}" cy="{cy + rk * math.sin(w):.1f}" rx="{rk * math.cos(w):.1f}" '
                     f'ry="{rk * math.cos(w) * .16:.1f}" fill="none" stroke="{CYAN}" stroke-opacity=".28" '
                     f'stroke-width="{r * .006:.2f}"/>')
    for n in range(6):
        phase = n * 30
        ruhe = math.cos(math.radians(phase))
        kugel.append(f'<ellipse class="{p}m{n}" cx="{cx:g}" cy="{cy:g}" rx="{rk:.1f}" ry="{rk:.1f}" fill="none" '
                     f'stroke="{CYAN}" stroke-opacity=".42" stroke-width="{r * .007:.2f}"/>')
        stile.append(f".{p}m{n}{{{_ursprung(cx, cy)};transform:scaleX({ruhe:.3f})}}")
        bewegung.append(f".{p}m{n}{{animation:{p}meridian 12s infinite;animation-delay:{-12 * phase / 360:.2f}s}}")
    teile.append("".join(kugel))
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rk:.1f}" fill="none" stroke="{CYAN}" stroke-opacity=".6" '
                 f'stroke-width="{r * .012:.2f}" filter="url(#leuchten)"/>')

    # Reaktorkranz um das Herz
    kranz = []
    for n in range(10):
        g = n * 36
        a1, a2 = g - 13, g + 13
        innen, aussen = r * .3, r * .42
        pkt = [polar(cx, cy, innen, a1), polar(cx, cy, aussen, a1 + 2), polar(cx, cy, aussen, a2 - 2),
               polar(cx, cy, innen, a2)]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pkt) + "Z"
        kranz.append(f'<path d="{d}" fill="{CYAN}" fill-opacity=".16" stroke="{CYAN}" stroke-opacity=".85" '
                     f'stroke-width="{r * .008:.2f}"/>')
    teile.append(f'<g class="{p}kranz" filter="url(#leuchten)">{"".join(kranz)}</g>')
    stile.append(f".{p}kranz{{{_ursprung(cx, cy)}}}")
    bewegung.append(f".{p}kranz{{animation:{p}dreh 40s linear infinite reverse}}")

    # Herz mit der 42
    rh = r * .25
    teile.append(f'<circle class="{p}puls" cx="{cx:g}" cy="{cy:g}" r="{rh * 1.18:.1f}" fill="{CYAN}" opacity=".25" '
                 f'filter="url(#leuchten_weit)"/>')
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rh:.1f}" fill="url(#{p}herz)"/>')
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rh:.1f}" fill="none" stroke="{KERN_HELL}" '
                 f'stroke-width="{r * .014:.2f}" filter="url(#leuchten)"/>')
    teile.append(text(cx, cy + rh * .36, "42", rh * 1.02, KERN_HELL, 600, 0, "middle", 'filter="url(#leuchten)"'))
    stile.append(f".{p}puls{{{_ursprung(cx, cy)}}}")
    bewegung.append(f".{p}puls{{animation:{p}puls 3.2s ease-in-out infinite}}")

    # Glanz oben links: die Kugel sitzt hinter Glas
    teile.append(f'<path d="M{cx - r * .7:.1f},{cy - r * .2:.1f} A{r * .72:.1f},{r * .72:.1f} 0 0 1 {cx + r * .2:.1f},'
                 f'{cy - r * .7:.1f}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="{r * .05:.2f}" '
                 'stroke-linecap="round"/>')

    bewegung.append(
        f"@keyframes {p}dreh{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}"
        f"@keyframes {p}meridian{{0%{{transform:scaleX(1);animation-timing-function:ease-in}}"
        f"25%{{transform:scaleX(0);animation-timing-function:ease-out}}"
        f"50%{{transform:scaleX(-1);animation-timing-function:ease-in}}"
        f"75%{{transform:scaleX(0);animation-timing-function:ease-out}}100%{{transform:scaleX(1)}}}}"
        f"@keyframes {p}puls{{0%,100%{{opacity:.18;transform:scale(1)}}50%{{opacity:.4;transform:scale(1.08)}}}}"
    )
    return Kern("".join(teile), "".join(stile), "".join(bewegung))


def kern_in_fassung(cx: float, cy: float, r: float, p: str = "k") -> Kern:
    """Kern hinter Glas in einer Rack-Fassung: Fasenplatte mit vier Schrauben, Riffelring, Mulde.

    r ist der Radius des Riffelrings; die Fasenplatte reicht etwas weiter."""
    from material import fase, platte, schraube

    k = kern(cx, cy, r * .86, p)
    halb = r + 14
    fassung = (
        f'<path d="{fase(cx - halb - 2, cy - halb - 2, 2 * halb + 4, 2 * halb + 4, 16)}" fill="#08090a"/>'
        + platte(fase(cx - halb, cy - halb, 2 * halb, 2 * halb, 15))
        + "".join(schraube(cx + dx * (halb - 12), cy + dy * (halb - 12), 30 + 25 * i, 4.6)
                  for i, (dx, dy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))))
        + f'<circle cx="{cx:g}" cy="{cy + 2:g}" r="{r + 2:g}" fill="#000" opacity=".7"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#knopfmetall)"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - 1.5:g}" fill="none" stroke="#3a3f45" stroke-width="3" '
        f'stroke-dasharray="1.4 1.8"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .9:g}" fill="#020607"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .9:g}" fill="none" stroke="url(#mulde)" stroke-width="3"/>'
    )
    return Kern(fassung + k.grafik, k.stil, k.bewegung)


def profilbild_kern() -> str:
    """Profilbild: der Kern füllt den Kreis, den GitHub ausschneidet; still, weil GitHub dort nur Bilder zeigt."""
    from material import defs_grund, svg

    k, m = 460, 230
    fassung = kern_in_fassung(m, m, 208, "p")
    inhalt = (f'<rect width="{k}" height="{k}" fill="#16181b"/>' + fassung.grafik)
    return svg(k, k, "HalloWelt42", inhalt, defs_grund() + kern_defs("p"), stil=fassung.stil, gewichte=(600,))
