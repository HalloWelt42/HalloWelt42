"""Profilbild zum Hochladen auf GitHub: der Kern als PNG (still, außen transparent) und als GIF (bewegt, außen
schwarz, weil GIF nur harte Transparenz kennt und der Kreisrand sonst ausfranst).

Gerendert wird mit der Schnellansicht von macOS (qlmanage), danach setzt Pillow zusammen. Läuft daher nur auf
dem Mac. GitHub nimmt für Profilbilder höchstens 1 MB an; das GIF wird so lange verkleinert, bis es passt.
"""
from __future__ import annotations

import pathlib
import subprocess
import tempfile

from PIL import Image, ImageDraw

from buehne.kern import SCHLEIFE, profilbild_kern

UEBERABTASTUNG = 4  # Kreisrand weich: Maske größer zeichnen, dann verkleinern
GRENZE = 1_000_000  # Byte, Obergrenze für Profilbilder bei GitHub


def _runde_maske(kante: int) -> Image.Image:
    gross = Image.new("L", (kante * UEBERABTASTUNG,) * 2, 0)
    ImageDraw.Draw(gross).ellipse((0, 0, kante * UEBERABTASTUNG - 1, kante * UEBERABTASTUNG - 1), fill=255)
    return gross.resize((kante, kante), Image.LANCZOS)


def _rendern(svgs: list[str], kante: int) -> list[Image.Image]:
    """Rendert SVG-Texte in einem Aufruf der Schnellansicht; Reihenfolge bleibt erhalten."""
    with tempfile.TemporaryDirectory() as ordner:
        pfade = []
        for n, inhalt in enumerate(svgs):
            pfad = pathlib.Path(ordner) / f"bild{n:03d}.svg"
            pfad.write_text(inhalt, encoding="utf-8")
            pfade.append(pfad)
        subprocess.run(["qlmanage", "-t", "-s", str(kante), "-o", ordner, *map(str, pfade)], check=True,
                       capture_output=True)
        return [Image.open(f"{p}.png").convert("RGBA").resize((kante, kante), Image.LANCZOS) for p in pfade]


def png_schreiben(ziel: pathlib.Path, kante: int = 920) -> None:
    bild = _rendern([profilbild_kern(0.0)], kante)[0]
    bild.putalpha(_runde_maske(kante))
    bild.save(ziel, optimize=True)


def _gif(einzelbilder: list[Image.Image], kante: int, farben: int, dauer_ms: int) -> bytes:
    maske = _runde_maske(kante)
    bilder = []
    for roh in einzelbilder:
        schwarz = Image.new("RGBA", (kante, kante), (0, 0, 0, 255))
        schwarz.paste(roh.resize((kante, kante), Image.LANCZOS), (0, 0), maske)
        bilder.append(schwarz.convert("RGB").quantize(colors=farben, method=Image.Quantize.MEDIANCUT,
                                                       dither=Image.Dither.NONE))
    with tempfile.TemporaryFile() as datei:
        bilder[0].save(datei, format="GIF", save_all=True, append_images=bilder[1:], duration=dauer_ms, loop=0,
                       optimize=True, disposal=1)
        datei.seek(0)
        return datei.read()


# Stufen von gut nach sparsam: (Kante in px, Farben). GitHub zeigt das Profilbild höchstens 296 px groß.
# Gemessen am 14.11.2026 bei 36 Bildern je Schleife: 300 px mit 64 Farben rund 0,95 MB, 260/32 rund 0,7 MB.
STUFEN = ((300, 64), (280, 64), (260, 64), (300, 32), (260, 32), (220, 32))


def gif_schreiben(ziel: pathlib.Path, bilder_je_schleife: int = 36) -> tuple[int, int, int]:
    """Bewegtes Profilbild; nimmt die beste Stufe unter der Grenze. Liefert (Kante, Farben, Byte)."""
    zeiten = [n * SCHLEIFE / bilder_je_schleife for n in range(bilder_je_schleife)]
    roh = _rendern([profilbild_kern(t, grund="#000000") for t in zeiten], max(k for k, _ in STUFEN))
    dauer = round(SCHLEIFE * 1000 / bilder_je_schleife)
    for kante, farben in STUFEN:
        daten = _gif(roh, kante, farben, dauer)
        if len(daten) <= GRENZE:
            ziel.write_bytes(daten)
            return kante, farben, len(daten)
    raise SystemExit(f"Profilbild-GIF bleibt über {GRENZE} Byte, auch in der sparsamsten Stufe")
