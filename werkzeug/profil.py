#!/usr/bin/env python3
"""Erzeugt die Profilseite (readme.md, Rack "Regie") und den Katalog aller Projekte (projekte.md, Rack-Einschübe).

Aufruf: python3 werkzeug/profil.py               Profilseite, Katalog, Logo als bewegtes SVG
        python3 werkzeug/profil.py --profilbild  zusätzlich Profilbilder als PNG und GIF (nur Mac)

Alles entsteht aus projekte.toml. Die Grafiken sind SVGs unter grafik/ (Profil) und katalog/ (Katalog), gebaut
von werkzeug/buehne. Jede Grafik bettet Icons und Schrift ein, weil ein als Bild geladenes SVG keine weiteren
Dateien nachladen darf.
"""
from __future__ import annotations

import sys

from buehne import auswahl, katalog, regie
from buehne.ergebnis import Ergebnis
from buehne.kern import LOGOFARBEN, profilbild_kern
from projekte import WURZEL, Profil, icon_fehler, laden, ungenutzte_icons

README = WURZEL / "readme.md"
KATALOG = WURZEL / "projekte.md"
GRAFIK = "grafik"  # Grafiken der Profilseite, relativ zur README
KATALOG_GRAFIK = "katalog"  # Grafiken des Katalogs, relativ zu projekte.md
ICON_FORMATE = {".svg", ".png"}
HINWEIS = "<!-- Erzeugt aus projekte.toml mit werkzeug/profil.py - nicht von Hand bearbeiten. -->"


def _ablegen(ergebnis: Ergebnis, ordner: str) -> int:
    """Schreibt die Grafiken eines Ergebnisses; alte SVGs des Ordners werden ersetzt. Liefert ihre Zahl."""
    ziel = WURZEL / ordner
    ziel.mkdir(exist_ok=True)
    for alt in ziel.glob("*.svg"):
        alt.unlink()
    grafiken = {n: i for n, i in ergebnis.dateien.items() if n != "avatar.svg"}
    for name, inhalt in grafiken.items():
        (ziel / name).write_text(inhalt, encoding="utf-8")
    return len(grafiken)


def readme_schreiben(profil: Profil) -> int:
    ergebnis = regie.bauen(auswahl.laden(profil), GRAFIK)
    anzahl = _ablegen(ergebnis, GRAFIK)
    README.write_text(f"{HINWEIS}\n\n{ergebnis.readme}", encoding="utf-8")
    # Das Logo als bewegtes SVG, außen transparent: für READMEs und Seiten. Als Profilbild nimmt GitHub nur
    # PNG, JPG und GIF, dafür gibt es --profilbild.
    for name, (farbe, hell) in LOGOFARBEN.items():
        endung = "" if name == "cyan" else f"-{name}"
        (WURZEL / GRAFIK / f"logo{endung}.svg").write_text(profilbild_kern(None, farbe=farbe, hell=hell),
                                                          encoding="utf-8")
    return anzahl


def katalog_schreiben(profil: Profil) -> int:
    ergebnis = katalog.bauen(profil, KATALOG_GRAFIK)
    anzahl = _ablegen(ergebnis, KATALOG_GRAFIK)
    KATALOG.write_text(f"{HINWEIS}\n\n{ergebnis.readme}", encoding="utf-8")
    return anzahl


def profilbild_schreiben() -> list[str]:
    from buehne import profilbild  # braucht Pillow und die Schnellansicht von macOS

    meldungen = []
    for name, (farbe, hell) in LOGOFARBEN.items():
        endung = "" if name == "cyan" else f"-{name}"
        png = WURZEL / GRAFIK / f"profilbild{endung}.png"
        gif = WURZEL / GRAFIK / f"profilbild{endung}.gif"
        profilbild.png_schreiben(png, farbe=farbe, hell=hell)
        kante, farben, groesse = profilbild.gif_schreiben(gif, farbe=farbe, hell=hell)
        meldungen.append(f"Profilbild {name}: {GRAFIK}/{png.name} (still) und {GRAFIK}/{gif.name} "
                         f"({kante} px, {farben} Farben, {groesse // 1024} KB)")
    return meldungen


def main() -> int:
    profil = laden()
    fehler = icon_fehler(profil, ICON_FORMATE) + auswahl.fehler(profil)
    if fehler:
        print("\n".join(fehler), file=sys.stderr)
        return 1
    grafiken = readme_schreiben(profil)
    katalog_grafiken = katalog_schreiben(profil)
    if "--profilbild" in sys.argv[1:]:
        print("\n".join(profilbild_schreiben()))
    for name in ungenutzte_icons(profil):
        print(f"Hinweis: icons/{name} wird von keinem Projekt genutzt", file=sys.stderr)
    gezeigt = sum(len(g.projekte) for g in profil.katalog_gruppen)
    print(f"Profil: {grafiken} Grafiken unter {GRAFIK}/, Top-Projekte: "
          f"{', '.join(p.name for p in auswahl.laden(profil).projekte)}")
    print(f"Katalog: {katalog_grafiken} Grafiken unter {KATALOG_GRAFIK}/, {gezeigt} Projekte in "
          f"{len(profil.katalog_gruppen)} Themen ({len(profil.projekte) - gezeigt} ausgeblendet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
