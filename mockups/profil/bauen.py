#!/usr/bin/env python3
"""Baut alle Profil-Entwürfe nach ausgabe/: je Entwurf die SVGs und README.md, dazu die Vorschauseite.

Aufruf: python3 mockups/profil/bauen.py
"""
from __future__ import annotations

import pathlib
import shutil

import entwurf_leitwarte
import entwurf_rack
import entwurf_regie
import entwurf_signatur
import pfad  # noqa: F401  (macht werkzeug/ importierbar)
from buehne.auswahl import laden

ORDNER = pathlib.Path(__file__).resolve().parent
from seite import als_artefakt, seite

ENTWUERFE = (entwurf_regie, entwurf_rack, entwurf_leitwarte, entwurf_signatur)  # erster = Vorgabe der Vorschau
AUSGABE = ORDNER / "ausgabe"


def main() -> None:
    auswahl = laden()
    AUSGABE.mkdir(exist_ok=True)
    for alt in AUSGABE.iterdir():  # Inhalt leeren, Ordner behalten: die Vorschau liefert ihn weiter aus
        shutil.rmtree(alt) if alt.is_dir() else alt.unlink()
    fertig = []
    for modul in ENTWUERFE:
        ergebnis = modul.bauen(auswahl)
        ordner = AUSGABE / ergebnis.kennung
        ordner.mkdir()
        for name, inhalt in ergebnis.dateien.items():
            (ordner / name).write_text(inhalt, encoding="utf-8")
        (ordner / "README.md").write_text(ergebnis.readme, encoding="utf-8")
        groesse = sum(len(i) for i in ergebnis.dateien.values()) // 1024
        print(f"Entwurf {ergebnis.kennung.upper()} {modul.STECKBRIEF.titel}: {len(ergebnis.dateien)} Dateien, {groesse} KB")
        fertig.append((modul.STECKBRIEF, ergebnis))
    dokument = seite(auswahl, fertig)
    (AUSGABE / "index.html").write_text(dokument, encoding="utf-8")
    (AUSGABE / "artefakt.html").write_text(als_artefakt(dokument), encoding="utf-8")
    print(f"Vorschau: {AUSGABE / 'index.html'}")


if __name__ == "__main__":
    main()
