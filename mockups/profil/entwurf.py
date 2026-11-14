"""Schnittstelle eines Entwurfs: erzeugte Bilder plus der README-Ausschnitt, der sie einbindet.

Der Ausschnitt nutzt nur, was GitHub in einer README zulässt: <p align>, <a>, <br>, <img width>. Jede Grafik
ist ein eigenes Bild mit eigenem Link. Breiten stehen in Prozent der README-Spalte: Teile einer Zeile bleiben so
bei jeder Fensterbreite nebeneinander und skalieren gemeinsam.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from material import esc

VOLL = 840
HALB = 412
DRITTEL = 272


def anteil(breite: int) -> str:
    """Breite als Anteil der README-Spalte; Zwischenräume zwischen Bildern einer Zeile bleiben frei."""
    return "100%" if breite >= VOLL else f"{breite / VOLL * 100:.1f}%"


@dataclass
class Ergebnis:
    kennung: str
    stapeln: bool = False  # True: alle Zeilen in einem Absatz, nur durch <br> getrennt (dicht wie ein Rack)
    dateien: dict[str, str] = field(default_factory=dict)
    zeilen: list[str] = field(default_factory=list)

    def bild(self, datei: str, inhalt: str) -> str:
        self.dateien[datei] = inhalt
        return f"{self.kennung}/{datei}"

    def zeile(self, *eintraege: tuple[str, int, str, str | None]) -> None:
        """Eine zentrierte Zeile aus (pfad, breite, alt, link)."""
        teile = []
        for pfad, breite, alt, link in eintraege:
            img = f'<img src="{pfad}" width="{anteil(breite)}" alt="{esc(alt)}">'
            teile.append(f'<a href="{esc(link)}">{img}</a>' if link else img)
        self.zeilen.append("\n".join(teile))

    @property
    def readme(self) -> str:
        if self.stapeln:
            return '<p align="center">\n' + "<br>\n".join(self.zeilen) + "\n</p>\n"
        return "\n\n".join(f'<p align="center">\n{z}\n</p>' for z in self.zeilen) + "\n"


@dataclass(frozen=True)
class Steckbrief:
    kennung: str
    titel: str
    idee: str
    merkmale: tuple[str, ...]


def reihen_teilen(eintraege: tuple) -> list[tuple]:
    """Teilt Karten in Reihen ohne Lücke: Dreier schmal, Zweier breit, nie eine allein, wenn es sich vermeiden lässt."""
    anzahl = len(eintraege)
    groessen = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [2, 3]}.get(anzahl) or [3] * (anzahl // 3) + (
        [anzahl % 3] if anzahl % 3 else [])
    reihen, start = [], 0
    for groesse in groessen:
        reihen.append(eintraege[start:start + groesse])
        start += groesse
    return reihen
