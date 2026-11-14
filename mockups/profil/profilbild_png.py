#!/usr/bin/env python3
"""Macht aus dem Profilbild-SVG eines Entwurfs ein PNG zum Hochladen auf GitHub: rund, außen transparent.

Aufruf (nach bauen.py, nur auf dem Mac): python3 mockups/profil/profilbild_png.py [entwurf] [kante]
Gerendert wird mit der Schnellansicht von macOS (qlmanage), danach schneidet Pillow den Kreis aus.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

from daten import ORDNER

UEBERABTASTUNG = 4  # Kreisrand weich: Maske in vierfacher Größe zeichnen, dann verkleinern


def runde_maske(kante: int) -> Image.Image:
    gross = Image.new("L", (kante * UEBERABTASTUNG,) * 2, 0)
    ImageDraw.Draw(gross).ellipse((0, 0, kante * UEBERABTASTUNG - 1, kante * UEBERABTASTUNG - 1), fill=255)
    return gross.resize((kante, kante), Image.LANCZOS)


def main() -> None:
    entwurf = sys.argv[1] if len(sys.argv) > 1 else "d"
    kante = int(sys.argv[2]) if len(sys.argv) > 2 else 920
    quelle = ORDNER / "ausgabe" / entwurf / "avatar.svg"
    ziel = ORDNER / "ausgabe" / entwurf / "profilbild.png"
    with tempfile.TemporaryDirectory() as ordner:
        subprocess.run(["qlmanage", "-t", "-s", str(kante), "-o", ordner, str(quelle)], check=True,
                       capture_output=True)
        roh = Image.open(pathlib.Path(ordner) / f"{quelle.name}.png").convert("RGBA").resize((kante, kante),
                                                                                             Image.LANCZOS)
    roh.putalpha(runde_maske(kante))
    roh.save(ziel, optimize=True)
    print(f"Profilbild: {ziel} ({kante} x {kante}, außen transparent)")


if __name__ == "__main__":
    main()
