#!/usr/bin/env python3
"""Entwurf HELF-241: wo die eigene Musik ins Rack käme. Baut beide Köpfe ohne und mit Abspielfeld.

Aufruf: python3 mockups/musik/bauen.py   (Ausgabe in mockups/musik/ausgabe/)
"""
from __future__ import annotations

import pathlib
import sys

ORDNER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ORDNER.parents[1] / "werkzeug"))

import projekte  # noqa: E402
from buehne import auswahl, katalog, regie  # noqa: E402

TITEL = "EIGENE KI-MUSIK"  # Platzhalter, bis die MP3 und ihr Titel feststehen


def main() -> None:
    profil = projekte.laden()
    ausgabe = ORDNER / "ausgabe"
    ausgabe.mkdir(exist_ok=True)
    bilder = {
        "katalog-kopf-heute.svg": katalog.kopf(profil),
        "katalog-kopf-musik.svg": katalog.kopf(profil, TITEL),
        "profil-kopf-heute.svg": regie.kopf(auswahl.laden(profil)),
        "profil-kopf-musik.svg": regie.kopf(auswahl.laden(profil), TITEL),
    }
    for name, inhalt in bilder.items():
        (ausgabe / name).write_text(inhalt, encoding="utf-8")
    print(f"{len(bilder)} Köpfe unter {ausgabe}")


if __name__ == "__main__":
    main()
