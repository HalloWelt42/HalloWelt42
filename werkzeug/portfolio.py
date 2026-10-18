#!/usr/bin/env python3
"""Erzeugt das Portfolio zum Durchblättern: quadratisches PDF und je Seite ein PNG.

Aufruf: python3 werkzeug/portfolio.py
Vorher einmalig: npm install (im Ordner portfolio/, holt die Schriften)

Seite 1 ist das Deckblatt (Jahresbilanz, Banner, Mosaik, Banner), danach folgt je Gruppe
aus projekte.toml eine Seite mit Begleittext und Icons. Die HTML-Datei ist eigenständig:
Schriften und Bilder sind eingebettet, damit Chrome ohne Server und ohne Netz rendert.
"""
from __future__ import annotations

import base64
import html
import pathlib
import subprocess
import sys
import tomllib
from dataclasses import dataclass

from projekte import WURZEL, Gruppe, Profil, Projekt, icon_fehler, laden

ORDNER = WURZEL / "portfolio"
DATEN = ORDNER / "portfolio.toml"
AUSGABE = ORDNER / "ausgabe"
SCHRIFTEN = ORDNER / "node_modules" / "@fontsource"
DRUCKEN = pathlib.Path(__file__).resolve().parent / "drucken.mjs"

KANTE = 1080
MEDIENTYPEN = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".woff2": "font/woff2"}
SCHRIFTSCHNITTE = (
    ("Barlow", "barlow/files/barlow-latin-400-normal.woff2", 400),
    ("Barlow", "barlow/files/barlow-latin-600-normal.woff2", 600),
    ("Barlow", "barlow/files/barlow-latin-700-normal.woff2", 700),
    ("Chakra Petch", "chakra-petch/files/chakra-petch-latin-600-normal.woff2", 600),
)
ZAEHLT_PROJEKTE = "projekte"


@dataclass(frozen=True)
class Kennzahl:
    wert: str
    text: str
    quelle: str


@dataclass(frozen=True)
class Banner:
    name: str
    zeile: str
    punkte: tuple[str, ...]
    icon: pathlib.Path
    bild: pathlib.Path


@dataclass(frozen=True)
class Portfolio:
    marke: str
    titel: str
    leitsatz: str
    seitenkopf: str
    datei: str
    kennzahlen: tuple[Kennzahl, ...]
    banner_oben: Banner
    banner_unten: Banner


def banner_laden(daten: dict) -> Banner:
    return Banner(
        name=daten["name"],
        zeile=daten["zeile"],
        punkte=tuple(daten["punkte"]),
        icon=(ORDNER / daten["icon"]).resolve(),
        bild=(ORDNER / daten["bild"]).resolve(),
    )


def portfolio_laden(pfad: pathlib.Path = DATEN) -> Portfolio:
    daten = tomllib.loads(pfad.read_text(encoding="utf-8"))
    return Portfolio(
        marke=daten["marke"],
        titel=daten["titel"],
        leitsatz=daten["leitsatz"],
        seitenkopf=daten["seitenkopf"],
        datei=daten["datei"],
        kennzahlen=tuple(Kennzahl(**k) for k in daten["kennzahl"]),
        banner_oben=banner_laden(daten["banner_oben"]),
        banner_unten=banner_laden(daten["banner_unten"]),
    )


def pruefen(portfolio: Portfolio, profil: Profil) -> list[str]:
    fehler = icon_fehler(profil, set(MEDIENTYPEN))
    for banner in (portfolio.banner_oben, portfolio.banner_unten):
        for datei in (banner.icon, banner.bild):
            if not datei.is_file():
                fehler.append(f"Banner {banner.name}: Datei fehlt: {datei}")
    for _, pfad, _ in SCHRIFTSCHNITTE:
        if not (SCHRIFTEN / pfad).is_file():
            fehler.append(f"Schrift fehlt: {pfad} (im Ordner portfolio/ einmal npm install ausführen)")
    return fehler


def daten_url(datei: pathlib.Path) -> str:
    inhalt = base64.b64encode(datei.read_bytes()).decode("ascii")
    return f"data:{MEDIENTYPEN[datei.suffix]};base64,{inhalt}"


def e(text: str) -> str:
    return html.escape(text)


# ---------------------------------------------------------------- Bausteine


def kennzahl_wert(kennzahl: Kennzahl, profil: Profil) -> str:
    return str(len(profil.projekte)) if kennzahl.wert == ZAEHLT_PROJEKTE else kennzahl.wert


def kennzahlen_html(portfolio: Portfolio, profil: Profil) -> str:
    karten = "".join(
        f'<div class="kennzahl"><b>{e(kennzahl_wert(k, profil))}</b><span>{e(k.text)}</span></div>'
        for k in portfolio.kennzahlen
    )
    return f'<div class="kennzahlen">{karten}</div>'


def banner_html(banner: Banner) -> str:
    punkte = "".join(f"<li>{e(p)}</li>" for p in banner.punkte)
    return (
        f'<section class="banner">'
        f'<img class="banner-bild" src="{daten_url(banner.bild)}" alt="">'
        f'<div class="banner-text">'
        f'<div class="banner-name"><img src="{daten_url(banner.icon)}" alt="">{e(banner.name)}</div>'
        f'<p class="banner-zeile">{e(banner.zeile)}</p>'
        f'<ul class="banner-punkte">{punkte}</ul>'
        f"</div></section>"
    )


def mosaik_html(profil: Profil) -> str:
    icons = "".join(
        f'<img src="{daten_url(p.icon_pfad)}" alt="{e(p.name)}">' for p in profil.projekte
    )
    return f'<section class="mosaik">{icons}</section>'


def seitenkopf_html(portfolio: Portfolio, nummer: int, gesamt: int) -> str:
    return (
        f'<header class="seitenkopf"><span>{e(portfolio.marke)} · {e(portfolio.seitenkopf)}</span>'
        f'<span class="zahl">{nummer} / {gesamt}</span></header>'
    )


def deckblatt_html(portfolio: Portfolio, profil: Profil, gesamt: int) -> str:
    return (
        f'<article class="seite deckblatt">'
        f'{seitenkopf_html(portfolio, 1, gesamt)}'
        f'<h1>{e(portfolio.titel)}</h1>'
        f'<p class="leitsatz">{e(portfolio.leitsatz)}</p>'
        f"{kennzahlen_html(portfolio, profil)}"
        f"{banner_html(portfolio.banner_oben)}"
        f"{mosaik_html(profil)}"
        f"{banner_html(portfolio.banner_unten)}"
        f"</article>"
    )


def raster_klasse(anzahl: int) -> str:
    """Wenige Projekte bekommen größere Icons."""
    if anzahl <= 4:
        return "raster gross"
    if anzahl <= 8:
        return "raster mittel"
    return "raster klein"


def name_html(name: str) -> str:
    """Umbruch nur zwischen Wörtern, nie am Bindestrich."""
    return " ".join(f'<span class="wort">{e(wort)}</span>' for wort in name.split())


def kachel_html(projekt: Projekt) -> str:
    return f'<figure><img src="{daten_url(projekt.icon_pfad)}" alt=""><figcaption>{name_html(projekt.name)}</figcaption></figure>'


def gruppenseite_html(portfolio: Portfolio, gruppe: Gruppe, nummer: int, gesamt: int) -> str:
    anzahl = len(gruppe.projekte)
    kacheln = "".join(kachel_html(p) for p in gruppe.projekte)
    return (
        f'<article class="seite gruppe">'
        f'{seitenkopf_html(portfolio, nummer, gesamt)}'
        f'<p class="anzahl zahl">{anzahl} {"Projekt" if anzahl == 1 else "Projekte"}</p>'
        f"<h2>{e(gruppe.titel)}</h2>"
        f'<p class="begleittext">{e(gruppe.begleittext)}</p>'
        f'<section class="{raster_klasse(anzahl)}">{kacheln}</section>'
        f"</article>"
    )


# ---------------------------------------------------------------- Seite


def schriften_css() -> str:
    return "".join(
        f'@font-face{{font-family:"{familie}";font-weight:{gewicht};font-style:normal;'
        f'src:url({daten_url(SCHRIFTEN / pfad)}) format("woff2")}}'
        for familie, pfad, gewicht in SCHRIFTSCHNITTE
    )


STIL = """
@page{size:1080px 1080px;margin:0}
:root{--grund:#0a0f15;--flaeche:#111a23;--flaeche-hoch:#16212c;--text:#e8eef4;--leise:#a3b4c4;--minze:#4dffd2}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--grund)}
body{font-family:"Barlow",system-ui,sans-serif;color:var(--text);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.zahl{font-family:"Chakra Petch","Barlow",sans-serif;font-weight:600}
.seite{width:1080px;height:1080px;overflow:hidden;position:relative;break-after:page;display:flex;flex-direction:column;
  padding:52px 60px;background:radial-gradient(120% 70% at 0% 0%,#12303a 0%,rgba(10,15,21,0) 55%),var(--grund)}
.seitenkopf{display:flex;justify-content:space-between;font-size:22px;color:var(--leise);letter-spacing:.02em}
.seitenkopf span:first-child{color:var(--minze);font-weight:600}

/* Deckblatt */
.deckblatt{gap:18px}
.deckblatt h1{font-size:68px;font-weight:700;line-height:1;margin-top:6px}
.leitsatz{font-size:26px;color:var(--leise);margin-top:-6px}
.kennzahlen{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.kennzahl{background:var(--flaeche);border-radius:4px;padding:14px 18px 16px;display:flex;flex-direction:column;gap:4px}
.kennzahl b{font-family:"Chakra Petch",sans-serif;font-weight:600;font-size:46px;line-height:1.05;color:var(--minze)}
.kennzahl span{font-size:20px;line-height:1.2;color:var(--leise)}
.banner{position:relative;height:178px;border-radius:4px;overflow:hidden;background:var(--flaeche)}
.banner-bild{position:absolute;right:0;top:50%;transform:translateY(-50%);width:58%;height:auto;min-height:100%;object-fit:cover}
.banner::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--flaeche) 34%,rgba(17,26,35,.75) 52%,rgba(17,26,35,0) 78%)}
.banner-text{position:relative;z-index:1;height:100%;max-width:66%;display:flex;flex-direction:column;justify-content:center;padding:0 30px;gap:6px}
.banner-name{display:flex;align-items:center;gap:16px;font-size:46px;font-weight:700;line-height:1}
.banner-name img{width:52px;height:52px;object-fit:contain}
.banner-zeile{font-size:24px;color:var(--text)}
.banner-punkte{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.banner-punkte li{font-size:19px;color:var(--leise);background:rgba(10,15,21,.7);border-radius:3px;padding:3px 10px}
.mosaik{flex:1;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));align-content:center;justify-items:center;gap:12px 0}
.mosaik img{width:54px;height:54px;object-fit:contain}

/* Gruppenseite */
.gruppe .anzahl{margin-top:70px;font-size:24px;color:var(--minze)}
.gruppe h2{font-size:84px;font-weight:700;line-height:1;margin-top:8px}
.begleittext{font-size:33px;line-height:1.38;color:var(--leise);margin-top:26px;max-width:930px}
.raster{flex:1;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:30px 0}
.raster figure{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center}
.raster figcaption{font-size:27px;font-weight:600;line-height:1.15}
.wort{white-space:nowrap}
.raster.gross figure{width:240px}
.raster.gross img{width:150px;height:150px;object-fit:contain}
.raster.mittel figure{width:240px}
.raster.mittel img{width:118px;height:118px;object-fit:contain}
.raster.klein figure{width:192px}
.raster.klein img{width:92px;height:92px;object-fit:contain}
.raster.klein figcaption{font-size:24px}
"""


def dokument_html(portfolio: Portfolio, profil: Profil) -> str:
    gesamt = 1 + len(profil.gruppen)
    seiten = [deckblatt_html(portfolio, profil, gesamt)] + [
        gruppenseite_html(portfolio, g, n, gesamt) for n, g in enumerate(profil.gruppen, start=2)
    ]
    return (
        f'<!doctype html><html lang="de"><head><meta charset="utf-8">'
        f"<title>{e(portfolio.marke)} {e(portfolio.titel)}</title>"
        f"<style>{schriften_css()}{STIL}</style></head><body>{''.join(seiten)}</body></html>\n"
    )


def main() -> int:
    profil = laden()
    portfolio = portfolio_laden()
    fehler = pruefen(portfolio, profil)
    if fehler:
        print("\n".join(fehler), file=sys.stderr)
        return 1
    AUSGABE.mkdir(exist_ok=True)
    for alt in AUSGABE.glob("seite-*.png"):
        alt.unlink()
    seite = AUSGABE / f"{portfolio.datei}.html"
    seite.write_text(dokument_html(portfolio, profil), encoding="utf-8")
    ergebnis = subprocess.run(
        ["node", str(DRUCKEN), str(seite), str(AUSGABE / f"{portfolio.datei}.pdf"), str(AUSGABE), str(KANTE)]
    )
    return ergebnis.returncode


if __name__ == "__main__":
    sys.exit(main())
