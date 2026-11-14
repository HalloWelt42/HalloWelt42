"""Auswahl für das Rack der Profilseite: die Top-Projekte aus projekte.toml in ihrer Reihenfolge."""
from __future__ import annotations

from dataclasses import dataclass

import projekte
from projekte import Profil, Projekt


@dataclass(frozen=True)
class Auswahl:
    projekte: tuple[Projekt, ...]
    technik: tuple[str, ...]
    link_alle: str
    link_unterstuetzen: str
    anzahl_gesamt: int
    anzahl_themen: int

    @property
    def fokus(self) -> Projekt:
        return next(p for p in self.projekte if p.fokus)

    @property
    def ohne_fokus(self) -> tuple[Projekt, ...]:
        return tuple(p for p in self.projekte if not p.fokus)


def fehler(profil: Profil) -> list[str]:
    """Was dem Rack fehlt, damit es gebaut werden kann."""
    top = [p for p in profil.projekte if p.top]
    meldungen = []
    if not top:
        meldungen.append("Kein Projekt mit top: das Rack bliebe leer")
    plaetze = [p.top for p in top]
    if len(set(plaetze)) != len(plaetze):
        meldungen.append(f"top doppelt vergeben: {sorted(plaetze)}")
    for p in top:
        if not p.akzent or not p.technik:
            meldungen.append(f"{p.name}: top braucht akzent und technik")
    fokus = [p for p in top if p.fokus]
    if len(fokus) != 1:
        meldungen.append(f"Genau ein Top-Projekt braucht fokus = true, gefunden: {len(fokus)}")
    for p in fokus:
        if not p.punkte or not p.bild_pfad or not p.bild_pfad.is_file():
            meldungen.append(f"{p.name}: fokus braucht punkte und ein vorhandenes bild")
    return meldungen


def laden(profil: Profil | None = None) -> Auswahl:
    profil = profil or projekte.laden()
    top = tuple(sorted((p for p in profil.projekte if p.top), key=lambda p: p.top))
    return Auswahl(
        projekte=top,
        technik=profil.angaben.technik,
        link_alle=profil.angaben.katalog,
        link_unterstuetzen=profil.angaben.unterstuetzen,
        anzahl_gesamt=sum(len(g.projekte) for g in profil.katalog_gruppen),  # so viele zeigt der Katalog
        anzahl_themen=len(profil.katalog_gruppen),
    )
