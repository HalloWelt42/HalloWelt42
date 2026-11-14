"""Der Kern: Logo als leuchtende Drahtkugel mit Ringen, Reaktorkranz und der 42 in der Mitte.

Liefert Grafik, Stil und Bewegung getrennt. Mit zeit=None dreht sich alles per CSS; mit einer Zeit entsteht
das stille Bild genau dieses Augenblicks (Einzelbilder für das bewegte Profilbild). Jede Bewegung schließt nach
SCHLEIFE Sekunden nahtlos an, weil sie je Schleife genau um ein Vielfaches der Symmetrie ihres Teils weiterläuft.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from buehne.material import BERNSTEIN, CYAN, bogen, polar, text

KERN_HELL = "#e9fdff"

SCHLEIFE = 6.0  # Sekunden, nach denen alles wieder wie am Anfang steht
DREHUNG = {"r1": 30, "r2": -60, "r3": 120, "kranz": -36}  # Grad je Schleife, Vielfache der Symmetrie
LAENGE = 90  # Längengrade, um die sich die Drahtkugel je Schleife dreht (Längenkreise alle 30 Grad)
PULSE = 2  # Herzschläge je Schleife


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


def _drehung(teil: str, p: str, zeit: float) -> tuple[str, str]:
    """Stellung zur Zeit und CSS-Drehung eines Rings: (Transform, Animationsregel)."""
    grad = DREHUNG[teil]
    dauer = 360 / abs(grad) * SCHLEIFE
    richtung = "" if grad > 0 else " reverse"
    return (f"transform:rotate({grad * zeit / SCHLEIFE:.2f}deg)",
            f".{p}{teil}{{animation:{p}dreh {dauer:g}s linear infinite{richtung}}}")


def kern(cx: float, cy: float, r: float, p: str = "k", zeit: float | None = None) -> Kern:
    """r ist der Außenradius der Ringe; alles bleibt innerhalb davon. zeit: Augenblick für ein stilles Bild."""
    t = zeit or 0.0
    teile, stile, bewegung = [], [], []
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#{p}schein)"/>')

    # Ring 1: Skala mit 72 Strichen, langsam rechts herum
    striche = []
    for n in range(72):
        g = n * 5
        lang = n % 6 == 0
        x1, y1 = polar(cx, cy, r * .97, g)
        x2, y2 = polar(cx, cy, r * (.88 if lang else .92), g)
        farbe = CYAN
        striche.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="{farbe}" '
                       f'stroke-opacity="{.95 if lang else .45}" stroke-width="{r * (.014 if lang else .009):.2f}"/>')
    teile.append(f'<g class="{p}r1">{"".join(striche)}</g>')
    stellung, regel = _drehung("r1", p, t)
    stile.append(f".{p}r1{{{_ursprung(cx, cy)};{stellung}}}")
    bewegung.append(regel)

    # Ring 2: gestrichelter Datenring, gegenläufig; das Muster wiederholt sich genau sechsmal (alle 60 Grad)
    r2 = r * .83
    muster = (.09, .015, .03, .015, .012, .03)
    teil = 2 * math.pi * r2 / 6 / sum(muster)
    striche = " ".join(f"{m * teil:.2f}" for m in muster)
    teile.append(f'<circle class="{p}r2" cx="{cx:g}" cy="{cy:g}" r="{r2:.1f}" fill="none" stroke="{CYAN}" '
                 f'stroke-opacity=".75" stroke-width="{r * .035:.2f}" stroke-dasharray="{striche}" '
                 'filter="url(#leuchten)"/>')
    stellung, regel = _drehung("r2", p, t)
    stile.append(f".{p}r2{{{_ursprung(cx, cy)};{stellung}}}")
    bewegung.append(regel)

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
    stellung, regel = _drehung("r3", p, t)
    stile.append(f".{p}r3{{{_ursprung(cx, cy)};{stellung}}}")
    bewegung.append(regel)

    # Drahtkugel: Breitenkreise fest, Längenkreise drehen sich als gestauchte Ellipsen
    rk = r * .6
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rk:.1f}" fill="url(#{p}kugel)"/>')
    kugel = []
    for breite in (-60, -35, -12, 12, 35, 60):
        w = math.radians(breite)
        kugel.append(f'<ellipse cx="{cx:g}" cy="{cy + rk * math.sin(w):.1f}" rx="{rk * math.cos(w):.1f}" '
                     f'ry="{rk * math.cos(w) * .16:.1f}" fill="none" stroke="{CYAN}" stroke-opacity=".28" '
                     f'stroke-width="{r * .006:.2f}"/>')
    umlauf = 360 / LAENGE * SCHLEIFE  # Sekunden für eine volle Drehung der Kugel
    for n in range(6):
        phase = n * 30
        stauchung = math.cos(math.radians(phase + LAENGE * t / SCHLEIFE))
        kugel.append(f'<ellipse class="{p}m{n}" cx="{cx:g}" cy="{cy:g}" rx="{rk:.1f}" ry="{rk:.1f}" fill="none" '
                     f'stroke="{CYAN}" stroke-opacity=".42" stroke-width="{r * .007:.2f}"/>')
        stile.append(f".{p}m{n}{{{_ursprung(cx, cy)};transform:scaleX({stauchung:.3f})}}")
        bewegung.append(f".{p}m{n}{{animation:{p}meridian {umlauf:g}s infinite;"
                        f"animation-delay:{-umlauf * phase / 360:.2f}s}}")
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
    stellung, regel = _drehung("kranz", p, t)
    stile.append(f".{p}kranz{{{_ursprung(cx, cy)};{stellung}}}")
    bewegung.append(regel)

    # Herz mit der 42
    rh = r * .25
    teile.append(f'<circle class="{p}puls" cx="{cx:g}" cy="{cy:g}" r="{rh * 1.18:.1f}" fill="{CYAN}" opacity=".25" '
                 f'filter="url(#leuchten_weit)"/>')
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rh:.1f}" fill="url(#{p}herz)"/>')
    teile.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rh:.1f}" fill="none" stroke="{KERN_HELL}" '
                 f'stroke-width="{r * .014:.2f}" filter="url(#leuchten)"/>')
    teile.append(text(cx, cy + rh * .36, "42", rh * 1.02, KERN_HELL, 600, 0, "middle", 'filter="url(#leuchten)"'))
    schlag = (1 - math.cos(2 * math.pi * PULSE * t / SCHLEIFE)) / 2
    stile.append(f".{p}puls{{{_ursprung(cx, cy)};opacity:{.18 + .22 * schlag:.3f};transform:scale({1 + .08 * schlag:.3f})}}")
    bewegung.append(f".{p}puls{{animation:{p}puls {SCHLEIFE / PULSE:g}s ease-in-out infinite}}")

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
    return Kern("".join(teile), "".join(stile), "" if zeit is not None else "".join(bewegung))


def kern_im_ring(cx: float, cy: float, r: float, p: str = "k", zeit: float | None = None) -> Kern:
    """Kern hinter Glas, eingefasst von einem Riffelring; r ist der Außenradius des Rings, nichts ragt darüber."""
    k = kern(cx, cy, r * .86, p, zeit)
    ring = (
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="url(#knopfmetall)"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - r * .015:.1f}" fill="none" stroke="#3a3f45" '
        f'stroke-width="{r * .03:.1f}" stroke-dasharray="{r * .014:.2f} {r * .018:.2f}"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .9:g}" fill="#020607"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r * .9:g}" fill="none" stroke="url(#mulde)" stroke-width="{r * .03:.1f}"/>'
    )
    return Kern(ring + k.grafik, k.stil, k.bewegung)


def kern_in_fassung(cx: float, cy: float, r: float, p: str = "k") -> Kern:
    """Kern im Ring auf einer Rack-Fasenplatte mit vier Schrauben; die Platte reicht etwas über den Ring."""
    from buehne.material import fase, platte, schraube

    innen = kern_im_ring(cx, cy, r, p)
    halb = r + 14
    fassung = (
        f'<path d="{fase(cx - halb - 2, cy - halb - 2, 2 * halb + 4, 2 * halb + 4, 16)}" fill="#08090a"/>'
        + platte(fase(cx - halb, cy - halb, 2 * halb, 2 * halb, 15))
        + "".join(schraube(cx + dx * (halb - 12), cy + dy * (halb - 12), 30 + 25 * i, 4.6)
                  for i, (dx, dy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))))
        + f'<circle cx="{cx:g}" cy="{cy + 2:g}" r="{r + 2:g}" fill="#000" opacity=".7"/>'
    )
    return Kern(fassung + innen.grafik, innen.stil, innen.bewegung)


def profilbild_kern(zeit: float | None = 0.0, grund: str | None = None) -> str:
    """Profilbild: nur der Ring mit dem Kern. GitHub schneidet es rund aus.

    zeit: Augenblick des stillen Bilds (None: per CSS bewegt). grund: Farbe außerhalb des Rings, sonst transparent."""
    from buehne.material import defs_grund, svg

    k, m = 460, 230
    rund = kern_im_ring(m, m, m, "p", zeit)
    flaeche = f'<rect width="{k}" height="{k}" fill="{grund}"/>' if grund else ""
    return svg(k, k, "HalloWelt42", flaeche + rund.grafik, defs_grund() + kern_defs("p"), stil=rund.stil,
               bewegung=rund.bewegung, gewichte=(600,))
