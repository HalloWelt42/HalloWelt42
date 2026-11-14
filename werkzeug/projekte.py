"""Datenmodell der Projektübersicht: liest projekte.toml, die einzige Wahrheit für Profil, Katalog und Portfolio."""
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
    ausblenden: bool = False  # nicht im Katalog zeigen
    # Nur für die Projekte im Rack der Profilseite (siehe Kopf von projekte.toml)
    top: int | None = None
    akzent: str | None = None
    technik: tuple[str, ...] = ()
    fokus: bool = False
    punkte: tuple[str, ...] = ()
    bild: str | None = None

    @property
    def ziel(self) -> str:
        return self.link or repo_adresse(self.repo)

    @property
    def schluessel(self) -> str:
        return pathlib.Path(self.icon).stem

    @property
    def icon_pfad(self) -> pathlib.Path:
        return ICONS / self.icon

    @property
    def bild_pfad(self) -> pathlib.Path | None:
        return WURZEL / self.bild if self.bild else None


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
class Musik:
    """Eigene Musik im Kopf der Seiten. Eine Grafik kann keinen Ton abspielen; der Link führt zur MP3 auf GitHub
    Pages, die der Browser direkt abspielt."""
    datei: str
    titel: str
    dauer: str
    orte: tuple[str, ...]
    seiten: str

    @property
    def link(self) -> str:
        return self.seiten.rstrip("/") + "/" + self.datei

    def an(self, ort: str) -> bool:
        return ort in self.orte


@dataclass(frozen=True)
class Angaben:
    """Angaben der Profilseite, die keinem einzelnen Projekt gehören."""
    technik: tuple[str, ...]
    katalog: str
    unterstuetzen: str
    musik: Musik | None = None


@dataclass(frozen=True)
class Profil:
    angaben: Angaben
    gruppen: tuple[Gruppe, ...]
    listen: tuple[Liste, ...]

    @property
    def projekte(self) -> tuple[Projekt, ...]:
        return tuple(p for g in self.gruppen for p in g.projekte)

    @property
    def katalog_gruppen(self) -> tuple[Gruppe, ...]:
        """Gruppen für den Katalog: ohne ausgeblendete Projekte, leere Gruppen fallen weg."""
        gruppen = (Gruppe(g.titel, g.text, g.begleittext, tuple(p for p in g.projekte if not p.ausblenden))
                   for g in self.gruppen)
        return tuple(g for g in gruppen if g.projekte)


def _projekt(roh: dict) -> Projekt:
    werte = dict(roh)
    for feld in ("technik", "punkte"):
        if feld in werte:
            werte[feld] = tuple(werte[feld])
    return Projekt(**werte)


def laden(pfad: pathlib.Path = DATEN) -> Profil:
    daten = tomllib.loads(pfad.read_text(encoding="utf-8"))
    angaben = daten["profil"]
    gruppen = tuple(
        Gruppe(g["titel"], g["text"], g["begleittext"], tuple(_projekt(p) for p in g["projekt"]))
        for g in daten["gruppe"]
    )
    listen = tuple(
        Liste(l["titel"], tuple(Eintrag(**e) for e in l["eintrag"]))
        for l in daten.get("liste", [])
    )
    musik = angaben.get("musik")
    musik_angabe = (Musik(musik["datei"], musik["titel"], musik["dauer"], tuple(musik["orte"]), angaben["seiten"])
                    if musik else None)
    return Profil(Angaben(tuple(angaben["technik"]), angaben["katalog"], angaben["unterstuetzen"], musik_angabe),
                  gruppen, listen)


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
