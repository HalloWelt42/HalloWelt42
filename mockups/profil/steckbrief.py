"""Was die Vorschauseite über einen Entwurf erzählt, und die Reihenaufteilung, die nur Entwürfe brauchen."""
from __future__ import annotations

from dataclasses import dataclass


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
