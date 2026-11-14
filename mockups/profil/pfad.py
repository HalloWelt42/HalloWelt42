"""Macht werkzeug/ importierbar: die Entwürfe nutzen dieselben Bausteine und Daten wie die echte Profilseite."""
import pathlib
import sys

WERKZEUG = pathlib.Path(__file__).resolve().parents[2] / "werkzeug"
if str(WERKZEUG) not in sys.path:
    sys.path.insert(0, str(WERKZEUG))
