"""Ortungsschirm: kreisender Strahl, die Projekte als Ziele. Braucht die Verläufe aus buehne.glas.defs_glas."""
from __future__ import annotations

from buehne.material import CYAN, polar, text
from projekte import Projekt


UMLAUF = 6.0  # Sekunden je Umdrehung des Strahls


def peilung(nummer: int) -> tuple[float, float]:
    """Lage eines Ziels auf dem Schirm: Winkel in Grad und Abstand als Anteil des Radius."""
    return 25 + nummer * 80, .45 + .13 * (nummer % 3)


def ortungsschirm(cx: float, cy: float, r: float, projekte: tuple[Projekt, ...],
                  kanalnummern: bool = False) -> tuple[str, str]:
    """Ortungsschirm mit kreisendem Strahl; die Projekte leuchten auf, wenn der Strahl sie streift.

    kanalnummern: Ziele tragen 01, 02 ... statt des Namens (wenn daneben eine Zielliste steht)."""
    teile = [f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="url(#rahmen)" stroke-width="9"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 13.5}" fill="none" stroke="#000" stroke-opacity=".7"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 4.5}" fill="none" stroke="#000" stroke-opacity=".8"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="#03080b"/>']
    for ring in (r, r * .75, r * .5, r * .25):
        teile.append(f'<circle cx="{cx}" cy="{cy}" r="{ring:g}" fill="none" stroke="{CYAN}" stroke-opacity=".16"/>')
    teile.append(f'<path d="M{cx - r},{cy}H{cx + r}M{cx},{cy - r}V{cy + r}" stroke="{CYAN}" stroke-opacity=".14"/>')
    for g in range(0, 360, 6):
        x1, y1 = polar(cx, cy, r, g)
        x2, y2 = polar(cx, cy, r - (7 if g % 30 == 0 else 3.5), g)
        teile.append(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="{CYAN}" stroke-opacity=".4"/>')
    sx, sy = polar(cx, cy, r, 0)
    ex, ey = polar(cx, cy, r, 50)
    teile.append(f'<g class="kreisel"><path d="M{cx},{cy} L{sx:.1f},{sy:.1f} A{r},{r} 0 0 1 {ex:.1f},{ey:.1f} Z" '
                 f'fill="url(#strahl)" transform="rotate(-50 {cx} {cy})"/>'
                 f'<path d="M{cx},{cy}L{sx:.1f},{sy:.1f}" stroke="{CYAN}" stroke-width="1.5" filter="url(#leuchten)"/></g>')
    stile = []
    for n, p in enumerate(projekte):
        winkel, anteil = peilung(n)
        px, py = polar(cx, cy, r * anteil, winkel)
        anker = "start" if px >= cx else "end"
        versatz = 9 if anker == "start" else -9
        teile.append(f'<g class="ziel{n}"><circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="{p.akzent}" '
                     f'filter="url(#leuchten)"/>'
                     f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" stroke="{p.akzent}" stroke-opacity=".5"/></g>')
        marke = f"{n + 1:02d}" if kanalnummern else p.name.upper()
        teile.append(text(px + versatz, py + 3.5, marke, 9.5 if not kanalnummern else 11, "#bfe3ea", 700, .8, anker))
        stile.append(f".ziel{n}{{animation:ziel {UMLAUF:g}s linear infinite;"
                     f"animation-delay:{winkel % 360 / 360 * UMLAUF - UMLAUF:.2f}s}}")
    teile.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{CYAN}"/>')
    teile.append(f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy} Z" fill="#fff" opacity=".035"/>')
    bewegung = (
        f".kreisel{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:kreisen {UMLAUF:g}s linear infinite}}"
        "@keyframes kreisen{from{transform:rotate(0)}to{transform:rotate(360deg)}}"
        "@keyframes ziel{0%{opacity:1}6%{opacity:1}60%{opacity:.25}100%{opacity:1}}"
        + "".join(stile)
    )
    return "".join(teile), bewegung
