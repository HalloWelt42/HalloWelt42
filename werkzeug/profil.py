#!/usr/bin/env python3
"""Erzeugt die Profilseite (readme.md mit dem Rack "Regie") und den Katalog aller Projekte (projekte.md).

Aufruf: python3 werkzeug/profil.py               Profilseite, Katalog, Kacheln
        python3 werkzeug/profil.py --profilbild  zusätzlich Profilbild als PNG und GIF (nur Mac)

Das Rack besteht aus SVG-Grafiken unter grafik/, gebaut von werkzeug/buehne aus den Top-Projekten in
projekte.toml. Im Katalog entstehen je Projekt zwei Kacheln (kacheln/hell, kacheln/dunkel); per <picture>
wählt GitHub die zum Farbschema passende. Jede Grafik bettet Icons und Schrift ein, weil ein als Bild
geladenes SVG keine weiteren Dateien nachladen darf.
"""
from __future__ import annotations

import base64
import html
import pathlib
import sys
from dataclasses import dataclass

from buehne import auswahl, regie
from projekte import WURZEL, Gruppe, Liste, Profil, Projekt, icon_fehler, laden, repo_adresse, ungenutzte_icons

VORLAGE = WURZEL / "vorlage.md"
KATALOG = WURZEL / "projekte.md"
README = WURZEL / "readme.md"
KACHELN = WURZEL / "kacheln"
GRAFIK = "grafik"  # Ablage der Rack-Grafiken, relativ zur README

PLATZHALTER = "{{projekte}}"
HINWEIS = "<!-- Erzeugt aus projekte.toml mit werkzeug/profil.py - nicht von Hand bearbeiten. -->"

KACHEL_BREITE = 100
KACHEL_HOEHE = 104
ICON_KANTE = 56
ICON_OBEN = 8
ZEICHEN_JE_ZEILE = 13
SCHRIFTEN = '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif'
MEDIENTYPEN = {".svg": "image/svg+xml", ".png": "image/png"}


@dataclass(frozen=True)
class Farbschema:
    name: str
    schrift: str
    medium: str | None  # None: Rückfall im <img>


HELL = Farbschema("hell", "#1f2328", None)
DUNKEL = Farbschema("dunkel", "#e6edf3", "(prefers-color-scheme: dark)")
FARBSCHEMATA = (HELL, DUNKEL)


def zeilen(name: str) -> list[str]:
    """Bricht lange Namen an der mittigsten Leerstelle oder dem mittigsten Bindestrich um."""
    if len(name) <= ZEICHEN_JE_ZEILE:
        return [name]
    stellen = [i for i, zeichen in enumerate(name) if zeichen in " -"]
    if not stellen:
        return [name]
    i = min(stellen, key=lambda s: abs(s - len(name) / 2))
    erste = name[: i + 1] if name[i] == "-" else name[:i]
    return [erste, name[i + 1 :]]


def eingebettet(icon: pathlib.Path) -> str:
    inhalt = base64.b64encode(icon.read_bytes()).decode("ascii")
    return f"data:{MEDIENTYPEN[icon.suffix]};base64,{inhalt}"


def kachel_svg(projekt: Projekt, schema: Farbschema) -> str:
    beschriftung = zeilen(projekt.name)
    erste_grundlinie = 84 if len(beschriftung) == 1 else 82
    texte = "".join(
        f'<text x="{KACHEL_BREITE / 2:g}" y="{erste_grundlinie + n * 15}">{html.escape(z)}</text>'
        for n, z in enumerate(beschriftung)
    )
    links = (KACHEL_BREITE - ICON_KANTE) / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{KACHEL_BREITE}" height="{KACHEL_HOEHE}" '
        f'viewBox="0 0 {KACHEL_BREITE} {KACHEL_HOEHE}">'
        f"<title>{html.escape(projekt.name)}</title>"
        f"<style>text{{font:600 12px {SCHRIFTEN};fill:{schema.schrift};text-anchor:middle}}</style>"
        f'<image href="{eingebettet(projekt.icon_pfad)}" x="{links:g}" y="{ICON_OBEN}" '
        f'width="{ICON_KANTE}" height="{ICON_KANTE}" preserveAspectRatio="xMidYMid meet"/>'
        f"{texte}</svg>\n"
    )


def kachel_pfad(projekt: Projekt, schema: Farbschema) -> str:
    return f"kacheln/{schema.name}/{projekt.schluessel}.svg"


def kachel_html(projekt: Projekt) -> str:
    titel = html.escape(f"{projekt.name} - {projekt.info}")
    quellen = "".join(
        f'<source media="{s.medium}" srcset="{kachel_pfad(projekt, s)}">' for s in FARBSCHEMATA if s.medium
    )
    return (
        f'<a href="{html.escape(projekt.ziel)}" title="{titel}"><picture>{quellen}'
        f'<img src="{kachel_pfad(projekt, HELL)}" width="{KACHEL_BREITE}" height="{KACHEL_HOEHE}" '
        f'alt="{html.escape(projekt.name)}"></picture></a>'
    )


def gruppe_html(gruppe: Gruppe) -> str:
    kacheln = "\n".join(kachel_html(p) for p in gruppe.projekte)
    return (
        f'<h3 align="center">{html.escape(gruppe.titel)}</h3>\n'
        f'<p align="center">{html.escape(gruppe.text)}</p>\n'
        f'<p align="center">\n{kacheln}\n</p>'
    )


def liste_md(liste: Liste) -> str:
    punkte = "\n".join(f"- [{e.repo}]({repo_adresse(e.repo)}) - {e.info}" for e in liste.eintraege)
    return (
        f"<details>\n<summary><b>{html.escape(liste.titel)}</b> ({len(liste.eintraege)})</summary>\n\n"
        f"{punkte}\n\n</details>"
    )


def projekte_abschnitt(profil: Profil) -> str:
    teile = [gruppe_html(g) for g in profil.gruppen]
    if profil.listen:
        teile.append("<br>\n\n" + "\n\n".join(liste_md(l) for l in profil.listen))
    return "\n\n".join(teile)


def kacheln_schreiben(profil: Profil) -> None:
    for schema in FARBSCHEMATA:
        ordner = KACHELN / schema.name
        ordner.mkdir(parents=True, exist_ok=True)
        for alt in ordner.glob("*.svg"):
            alt.unlink()
        for projekt in profil.projekte:
            (WURZEL / kachel_pfad(projekt, schema)).write_text(kachel_svg(projekt, schema), encoding="utf-8")


def katalog_schreiben(profil: Profil) -> None:
    vorlage = VORLAGE.read_text(encoding="utf-8")
    if vorlage.count(PLATZHALTER) != 1:
        raise SystemExit(f"vorlage.md muss den Platzhalter {PLATZHALTER} genau einmal enthalten")
    KATALOG.write_text(f"{HINWEIS}\n\n{vorlage.replace(PLATZHALTER, projekte_abschnitt(profil))}", encoding="utf-8")


def readme_schreiben(profil: Profil) -> int:
    """Rack als README; alte Grafiken werden ersetzt. Liefert die Zahl der Grafiken."""
    ergebnis = regie.bauen(auswahl.laden(profil), GRAFIK)
    ordner = WURZEL / GRAFIK
    ordner.mkdir(exist_ok=True)
    for alt in ordner.glob("*.svg"):
        alt.unlink()
    for name, inhalt in ergebnis.dateien.items():
        if name.endswith(".svg") and name != "avatar.svg":
            (ordner / name).write_text(inhalt, encoding="utf-8")
    README.write_text(f"{HINWEIS}\n\n{ergebnis.readme}", encoding="utf-8")
    return sum(1 for n in ergebnis.dateien if n != "avatar.svg")


def profilbild_schreiben() -> str:
    from buehne import profilbild  # braucht Pillow und die Schnellansicht von macOS

    ordner = WURZEL / GRAFIK
    profilbild.png_schreiben(ordner / "profilbild.png")
    kante, farben, groesse = profilbild.gif_schreiben(ordner / "profilbild.gif")
    return (f"Profilbild: {GRAFIK}/profilbild.png (still) und {GRAFIK}/profilbild.gif "
            f"({kante} px, {farben} Farben, {groesse // 1024} KB)")


def main() -> int:
    profil = laden()
    fehler = icon_fehler(profil, set(MEDIENTYPEN)) + auswahl.fehler(profil)
    if fehler:
        print("\n".join(fehler), file=sys.stderr)
        return 1
    kacheln_schreiben(profil)
    katalog_schreiben(profil)
    grafiken = readme_schreiben(profil)
    if "--profilbild" in sys.argv[1:]:
        print(profilbild_schreiben())
    for name in ungenutzte_icons(profil):
        print(f"Hinweis: icons/{name} wird von keinem Projekt genutzt", file=sys.stderr)
    eintraege = sum(len(l.eintraege) for l in profil.listen)
    print(f"Profil: {grafiken} Rack-Grafiken unter {GRAFIK}/, Top-Projekte: "
          f"{', '.join(p.name for p in auswahl.laden(profil).projekte)}")
    print(f"Katalog: {len(profil.projekte)} Kacheln in {len(profil.gruppen)} Gruppen, {eintraege} Listeneinträge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
