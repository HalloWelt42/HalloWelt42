"""Entwurf D "Regie": gebaut vom echten Werkzeug (werkzeug/buehne/regie.py), hier nur beschrieben."""
from __future__ import annotations

import pfad  # noqa: F401  (macht werkzeug/ importierbar)
from buehne import regie
from buehne.auswahl import Auswahl
from buehne.ergebnis import Ergebnis
from steckbrief import Steckbrief

STECKBRIEF = Steckbrief(
    kennung="d",
    titel="Regie",
    idee="Das Studio-Rack aus A als Grundlage, ergänzt um das Beste der anderen: der Ortungsschirm aus B im "
         "Kopf, die TubeVault-Präsentation aus C als Fokus-Einschub, alle Teile dicht gestapelt wie in einem "
         "Gestell. Das Profilbild ist der Kern: Drahtkugel, Ringe und die 42 in der Mitte.",
    merkmale=(
        "Kopf mit Ortungsschirm in Rack-Fassung neben der Bernstein-Anzeige",
        "Signalmonitor: Zielliste mit Peilung passend zum Schirm, ein VU-Meter",
        "TubeVault im Fokus-Einschub mit Bildschirmfoto im Rack-Fenster",
        "Weitere Projekte als flache Einschübe über die volle Breite, Steckfeld und Tasten wie in A",
        "Breiten in Prozent: Tasten bleiben bei jeder Fensterbreite nebeneinander",
        "Profilbild: der Kern rund, außen transparent, still (GitHub zeigt keine bewegten Profilbilder)",
    ),
)


def bauen(auswahl: Auswahl) -> Ergebnis:
    return regie.bauen(auswahl, STECKBRIEF.kennung)
