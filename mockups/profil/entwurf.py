"""Schnittstelle eines Entwurfs: erzeugte Bilder plus der README-Ausschnitt, der sie einbindet.

Der Ausschnitt nutzt nur, was GitHub in einer README zulässt: <p align>, <a>, <img width>. Jede Grafik
ist ein eigenes Bild mit eigenem Link; zwei Kacheln je Zeile brechen auf schmalen Schirmen von selbst um.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from material import esc

VOLL = 840
HALB = 412
DRITTEL = 272


@dataclass
class Ergebnis:
    kennung: str
    dateien: dict[str, str] = field(default_factory=dict)
    zeilen: list[str] = field(default_factory=list)

    def bild(self, datei: str, inhalt: str) -> str:
        self.dateien[datei] = inhalt
        return f"{self.kennung}/{datei}"

    def zeile(self, *eintraege: tuple[str, int, str, str | None]) -> None:
        """Eine zentrierte Zeile aus (pfad, breite, alt, link)."""
        teile = []
        for pfad, breite, alt, link in eintraege:
            img = f'<img src="{pfad}" width="{breite}" alt="{esc(alt)}">'
            teile.append(f'<a href="{esc(link)}">{img}</a>' if link else img)
        self.zeilen.append('<p align="center">\n' + "\n".join(teile) + "\n</p>")

    @property
    def readme(self) -> str:
        return "\n\n".join(self.zeilen) + "\n"


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
