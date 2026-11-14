"""Glas-Bausteine im Cyber-Stil: gefräster Rahmen mit Glasfläche, Kantenlicht, Abtastlinie, Eckwinkel, Chips."""
from __future__ import annotations

from buehne.material import CYAN, fase, mulde, platte, text, textbreite

GLAS_TINTE = "#eef6f8"
GLAS_LEISE = "#93a8b6"
GLAS_STUMM = "#6f8594"


def defs_glas() -> str:
    """Glas- und Rahmenverläufe (ohne den Grundbestand aus material.defs_grund)."""
    return (
        '<linearGradient id="rahmen" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#50565e"/><stop offset=".18" stop-color="#30353b"/>'
        '<stop offset=".8" stop-color="#1f2226"/><stop offset="1" stop-color="#121417"/></linearGradient>'
        '<linearGradient id="tiefglas" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0b141b"/><stop offset="1" stop-color="#04080b"/></linearGradient>'
        '<pattern id="gitter" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M24,0V24M0,24H24" fill="none" stroke="{CYAN}" stroke-opacity=".05"/></pattern>'
        '<radialGradient id="vignette" cx=".5" cy=".45" r=".75">'
        '<stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/>'
        '</radialGradient>'
        '<linearGradient id="lauflicht" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="abtastung" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".85" stop-color="{CYAN}" stop-opacity=".06"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".18"/></linearGradient>'
        '<linearGradient id="strahl" x1="0" y1="1" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/>'
        '</linearGradient>'
    )


BEWEGUNG_GLAS = (
    ".lauf{animation:lauf 6s linear infinite}"
    "@keyframes lauf{from{transform:translateX(0)}to{transform:translateX(1100px)}}"
    ".abtasten{animation:abtasten 7s linear infinite}"
    "@keyframes abtasten{from{transform:translateY(-60px)}to{transform:translateY(320px)}}"
)


def rahmen(b: float, h: float, gross: float, klein: float) -> tuple[str, str]:
    """Gefräster Rahmen mit Glasfläche; liefert Grafik und den Pfad der Glasfläche."""
    aussen = fase(0, 0, b, h, (gross, klein, gross, klein))
    glas = fase(6, 6, b - 12, h - 12, (gross - 4, max(klein - 2, 1), gross - 4, max(klein - 2, 1)))
    teile = [
        f'<path d="{aussen}" fill="#050607"/>',
        platte(fase(1, 1, b - 2, h - 2, (gross, klein, gross, klein)), "url(#rahmen)"),
        mulde(glas, "url(#tiefglas)"),
        f'<path d="{glas}" fill="url(#gitter)"/>',
        f'<path d="{glas}" fill="url(#vignette)"/>',
    ]
    return "".join(teile), glas


def kantenlicht(b: float, glas: str, nummer: int = 0, farbe: str = CYAN) -> str:
    return (
        f'<clipPath id="kante{nummer}"><rect x="0" y="5" width="{b:g}" height="3"/></clipPath>'
        f'<path d="M30,6.6H{b - 20:g}" stroke="{farbe}" stroke-opacity=".28"/>'
        f'<g clip-path="url(#kante{nummer})"><rect class="lauf" x="-220" y="5" width="220" height="3" '
        f'fill="url(#lauflicht)" filter="url(#leuchten)"/></g>'
    )


def abtastung(glas: str, h: float, nummer: int = 0) -> str:
    return (
        f'<clipPath id="glas{nummer}"><path d="{glas}"/></clipPath>'
        f'<g clip-path="url(#glas{nummer})"><rect class="abtasten" x="0" y="0" width="100%" height="60" '
        f'fill="url(#abtastung)"/></g>'
    )


def klammern(x: float, y: float, b: float, h: float, farbe: str, laenge: float = 16) -> str:
    """Eckwinkel oben rechts und unten links, wie Markierungen auf einer Anzeige."""
    return (
        f'<path d="M{x + b - laenge:g},{y:g}H{x + b:g}V{y + laenge:g}M{x:g},{y + h - laenge:g}V{y + h:g}H{x + laenge:g}" '
        f'fill="none" stroke="{farbe}" stroke-width="1.6" stroke-opacity=".75" filter="url(#leuchten)"/>'
    )


def chip(x: float, y: float, inhalt: str, farbe: str) -> tuple[str, float]:
    breite = textbreite(inhalt.upper(), 10, 1) + 22
    h = 21
    d = f"M{x + 6:g},{y:g}H{x + breite - 6:g}L{x + breite:g},{y + h / 2:g}L{x + breite - 6:g},{y + h:g}H{x + 6:g}L{x:g},{y + h / 2:g}Z"
    return (
        f'<path d="{d}" fill="{farbe}" fill-opacity=".09" stroke="{farbe}" stroke-opacity=".5"/>'
        + text(x + breite / 2, y + 14.5, inhalt.upper(), 10, "#d6e8ee", 700, 1, "middle")
    ), breite
