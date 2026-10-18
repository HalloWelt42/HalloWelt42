"""Datenmodell der Projektübersicht: liest projekte.toml, die einzige Wahrheit für Profil und Portfolio."""
from __future__ import annotations

import pathlib
import tomllib
from dataclasses import dataclass

WURZEL = pathlib.Path(__file__).resolve().parent.parent
DATEN = WURZEL / "projekte.toml"
ICONS = WURZEL / "icons"
KONTO = "HalloWelt42"


def repo_adresse(repo: str) -> str:
    return f"https://github.com/{KONTO}/{repo}"


@dataclass(frozen=True)
class Projekt:
    name: str
    info: str
    icon: str
    repo: str
    link: str | None = None

    @property
    def ziel(self) -> str:
        return self.link or repo_adresse(self.repo)

    @property
    def schluessel(self) -> str:
        return pathlib.Path(self.icon).stem

    @property
    def icon_pfad(self) -> pathlib.Path:
        return ICONS / self.icon


@dataclass(frozen=True)
class Gruppe:
    titel: str
    text: str
    begleittext: str
    projekte: tuple[Projekt, ...]


@dataclass(frozen=True)
class Eintrag:
    repo: str
    info: str


@dataclass(frozen=True)
class Liste:
    titel: str
    eintraege: tuple[Eintrag, ...]


@dataclass(frozen=True)
class Profil:
    gruppen: tuple[Gruppe, ...]
    listen: tuple[Liste, ...]

    @property
    def projekte(self) -> tuple[Projekt, ...]:
        return tuple(p for g in self.gruppen for p in g.projekte)


def laden(pfad: pathlib.Path = DATEN) -> Profil:
    daten = tomllib.loads(pfad.read_text(encoding="utf-8"))
    gruppen = tuple(
        Gruppe(g["titel"], g["text"], g["begleittext"], tuple(Projekt(**p) for p in g["projekt"]))
        for g in daten["gruppe"]
    )
    listen = tuple(
        Liste(l["titel"], tuple(Eintrag(**e) for e in l["eintrag"]))
        for l in daten.get("liste", [])
    )
    return Profil(gruppen, listen)


def icon_fehler(profil: Profil, formate: set[str]) -> list[str]:
    """Fehlende, doppelt genutzte oder nicht unterstützte Icons."""
    fehler = []
    gesehen: set[str] = set()
    for projekt in profil.projekte:
        if not projekt.icon_pfad.is_file():
            fehler.append(f"{projekt.name}: Icon fehlt: icons/{projekt.icon}")
        if projekt.icon_pfad.suffix not in formate:
            fehler.append(f"{projekt.name}: Icon-Format nicht unterstützt: {projekt.icon}")
        if projekt.schluessel in gesehen:
            fehler.append(f"{projekt.name}: Icon wird schon von einem anderen Projekt genutzt: {projekt.icon}")
        gesehen.add(projekt.schluessel)
    return fehler


def ungenutzte_icons(profil: Profil) -> list[str]:
    genutzt = {p.icon for p in profil.projekte}
    return sorted(d.name for d in ICONS.iterdir() if d.is_file() and d.name not in genutzt)
