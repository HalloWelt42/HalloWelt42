#!/usr/bin/env python3
"""Baut die Katalog-Entwürfe nach ausgabe/: je Entwurf die SVGs und README.md, dazu die Vorschauseite.

Aufruf: python3 mockups/katalog/bauen.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ORDNER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ORDNER.parents[1] / "werkzeug"))  # Bausteine und Daten der echten Seite

import projekte  # noqa: E402
from entwuerfe import ENTWUERFE, bauen  # noqa: E402
from seite import als_artefakt, seite  # noqa: E402

AUSGABE = ORDNER / "ausgabe"


def main() -> None:
    profil = projekte.laden()
    AUSGABE.mkdir(exist_ok=True)
    for alt in AUSGABE.iterdir():  # Inhalt leeren, Ordner behalten
        shutil.rmtree(alt) if alt.is_dir() else alt.unlink()
    fertig = []
    for entwurf in ENTWUERFE:
        ergebnis = bauen(entwurf, profil)
        ordner = AUSGABE / ergebnis.kennung
        ordner.mkdir()
        for name, inhalt in ergebnis.dateien.items():
            (ordner / name).write_text(inhalt, encoding="utf-8")
        (ordner / "README.md").write_text(ergebnis.readme, encoding="utf-8")
        groesse = sum(len(i) for i in ergebnis.dateien.values()) // 1024
        print(f"Entwurf {entwurf.kennung.upper()} {entwurf.titel}: {len(ergebnis.dateien)} Dateien, {groesse} KB")
        fertig.append((entwurf, ergebnis))
    (AUSGABE / "index.html").write_text(seite(fertig), encoding="utf-8")
    (AUSGABE / "artefakt.html").write_text(als_artefakt(seite(fertig, einbetten=False)), encoding="utf-8")
    print(f"Vorschau: {AUSGABE / 'index.html'}")


if __name__ == "__main__":
    main()
