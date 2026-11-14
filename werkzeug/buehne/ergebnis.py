"""Schnittstelle eines Entwurfs: erzeugte Bilder plus der README-Ausschnitt, der sie einbindet.

Der Ausschnitt nutzt nur, was GitHub in einer README zulässt: <p align>, <a>, <br>, <img width>. Jede Grafik
ist ein eigenes Bild mit eigenem Link. Breiten stehen in Prozent der README-Spalte: Teile einer Zeile bleiben so
bei jeder Fensterbreite nebeneinander und skalieren gemeinsam.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from buehne.material import esc

VOLL = 840
HALB = 412
DRITTEL = 272
VIERTEL = 206
FUENFTEL = 164


def anteil(breite: int) -> str:
    """Breite als Anteil der README-Spalte; Zwischenräume zwischen Bildern einer Zeile bleiben frei."""
    return "100%" if breite >= VOLL else f"{breite / VOLL * 100:.1f}%"


@dataclass
class Ergebnis:
    kennung: str
    stapeln: bool = False  # True: aufeinanderfolgende Bildzeilen in einem Absatz, nur durch <br> getrennt (dicht)
    dateien: dict[str, str] = field(default_factory=dict)
    zeilen: list[tuple[str, str]] = field(default_factory=list)  # (art, inhalt): "bild" oder "text"

    def bild(self, datei: str, inhalt: str) -> str:
        self.dateien[datei] = inhalt
        return f"{self.kennung}/{datei}"

    def zeile(self, *eintraege: tuple[str, int, str, str | None]) -> None:
        """Eine zentrierte Zeile aus (pfad, breite, alt, link)."""
        teile = []
        for pfad, breite, alt, link in eintraege:
            img = f'<img src="{pfad}" width="{anteil(breite)}" alt="{esc(alt)}">'
            teile.append(f'<a href="{esc(link)}" title="{esc(alt)}">{img}</a>' if link else img)
        self.zeilen.append(("bild", "\n".join(teile)))

    def text(self, markdown: str) -> None:
        """Ein Block Markdown zwischen den Bildern, etwa eine aufklappbare Liste."""
        self.zeilen.append(("text", markdown.strip()))

    @property
    def readme(self) -> str:
        bloecke: list[str] = []
        bilder: list[str] = []

        def bilder_abschliessen() -> None:
            if not bilder:
                return
            if self.stapeln:
                bloecke.append('<p align="center">\n' + "<br>\n".join(bilder) + "\n</p>")
            else:
                bloecke.extend(f'<p align="center">\n{z}\n</p>' for z in bilder)
            bilder.clear()

        for art, inhalt in self.zeilen:
            if art == "bild":
                bilder.append(inhalt)
            else:
                bilder_abschliessen()
                bloecke.append(inhalt)
        bilder_abschliessen()
        return "\n\n".join(bloecke) + "\n"
