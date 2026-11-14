"""Datenmodell der Profil-Entwürfe: liest auswahl.toml und zählt die Projekte aus projekte.toml."""
from __future__ import annotations

import pathlib
import sys
import tomllib
from dataclasses import dataclass

ORDNER = pathlib.Path(__file__).resolve().parent
REPO = ORDNER.parents[1]
sys.path.insert(0, str(REPO / "werkzeug"))

import projekte  # noqa: E402  (vorhandenes Datenmodell der Projektübersicht)


@dataclass(frozen=True)
class Projekt:
    name: str
    info: str
    repo: str
    icon: pathlib.Path
    akzent: str
    technik: tuple[str, ...]
    link: str | None = None
    fokus: bool = False
    punkte: tuple[str, ...] = ()
    bild: pathlib.Path | None = None

    @property
    def ziel(self) -> str:
        return self.link or projekte.repo_adresse(self.repo)

    @property
    def schluessel(self) -> str:
        return self.repo.lower()


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


def _projekt(roh: dict) -> Projekt:
    return Projekt(
        name=roh["name"],
        info=roh["info"],
        repo=roh["repo"],
        icon=REPO / roh["icon"],
        akzent=roh["akzent"],
        technik=tuple(roh["technik"]),
        link=roh.get("link"),
        fokus=roh.get("fokus", False),
        punkte=tuple(roh.get("punkte", ())),
        bild=REPO / roh["bild"] if "bild" in roh else None,
    )


def laden() -> Auswahl:
    roh = tomllib.loads((ORDNER / "auswahl.toml").read_text(encoding="utf-8"))
    gesamt = projekte.laden()
    return Auswahl(
        projekte=tuple(_projekt(p) for p in roh["projekt"]),
        technik=tuple(roh["technik"]["liste"]),
        link_alle=roh["links"]["alle"],
        link_unterstuetzen=roh["links"]["unterstuetzen"],
        anzahl_gesamt=len(gesamt.projekte),
        anzahl_themen=len(gesamt.gruppen),
    )
