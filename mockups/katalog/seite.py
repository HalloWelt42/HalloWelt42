"""Vorschau der Katalog-Entwürfe im Rahmen der GitHub-Dateiansicht von projekte.md.

Der README-Ausschnitt jedes Entwurfs wird unverändert eingesetzt, die Bilder eingebettet (kein Server nötig).
Der Anker merkt sich den Entwurf: #instrumente, #konsole, #matrix.
"""
from __future__ import annotations

import base64
import json

from buehne.ergebnis import Ergebnis
from buehne.material import esc, schriften
from entwuerfe import Entwurf


def _svg_url(inhalt: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(inhalt.encode("utf-8")).decode("ascii")


def _eingebettet(ergebnis: Ergebnis) -> str:
    readme = ergebnis.readme
    for datei, inhalt in ergebnis.dateien.items():
        readme = readme.replace(f'src="{ergebnis.kennung}/{datei}"', f'src="{_svg_url(inhalt)}"')
    return readme


DATEIEN = ("bilder", "grafik", "icons", "kacheln", "mockups", "portfolio", "werkzeug", ".gitignore", "projekte.md",
           "projekte.toml", "readme.md", "vorlage.md")


def seite(entwuerfe: list[tuple[Entwurf, Ergebnis]]) -> str:
    steckbriefe = {e.kennung: {"titel": e.titel, "idee": e.idee, "merkmale": list(e.merkmale)} for e, _ in entwuerfe}
    vorlagen = "".join(f'<template id="readme-{e.kennung}">{_eingebettet(r)}</template>' for e, r in entwuerfe)
    knoepfe = "".join(f'<button data-wert="{e.kennung}"><b>{e.kennung.upper()}</b> {esc(e.titel)}</button>'
                      for e, _ in entwuerfe)
    baum = "".join(f'<li class="{"an" if d == "projekte.md" else ""}">{esc(d)}</li>' for d in DATEIEN)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Katalog-Entwürfe</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
{schriften(400, 600, 700)}
:root{{--grund:#121417;--tinte:#e6eaee;--leise:#9aa3ad;--akzent:#5ff2ff;color-scheme:dark}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--grund);color:var(--tinte);font:17px/1.5 'Chakra Petch',sans-serif}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:#1b2128}}
.steuerung{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:linear-gradient(#1f262d,#151a1f);
  border-bottom:1px solid #000;box-shadow:0 1px 0 rgba(95,242,255,.12) inset,0 6px 18px rgba(0,0,0,.5);
  padding-block:12px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));
  display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center}}
.steuerung h1{{margin:0;font-size:20px;font-weight:700;letter-spacing:.06em;margin-right:auto}}
.steuerung h1 small{{display:block;font-size:13px;font-weight:600;color:var(--leise);letter-spacing:.12em}}
.gruppe{{display:flex;align-items:center;gap:8px}}
.gruppe>span{{font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--leise)}}
.schiene{{display:flex;padding:3px;gap:3px;background:#06090b;border-radius:8px;
  box-shadow:inset 0 2px 4px rgba(0,0,0,.8),0 1px 0 rgba(255,255,255,.07)}}
.schiene button{{font:600 15px 'Chakra Petch',sans-serif;color:var(--leise);background:transparent;border:0;
  padding:6px 12px;border-radius:6px;cursor:pointer;white-space:nowrap}}
.schiene button:hover{{color:var(--tinte)}}
.schiene button:focus-visible{{outline:2px solid var(--akzent);outline-offset:1px}}
.schiene button[aria-pressed=true]{{color:#bffaff;background:linear-gradient(#2c3740,#1d252c);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 2px 4px rgba(0,0,0,.6);text-shadow:0 0 8px rgba(95,242,255,.5)}}
.steckbrief{{max-width:1280px;margin:20px auto 0;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px))}}
.tafel{{background:linear-gradient(#1d2329,#161b20);border-radius:10px;padding:16px 20px;
  box-shadow:inset 0 1px 0 rgba(95,242,255,.1),0 0 0 1px #000}}
.tafel h2{{margin:0 0 6px;font-size:15px;letter-spacing:.16em;color:var(--akzent)}}
.tafel p{{margin:0 0 8px}}
.tafel ul{{margin:0;padding-left:18px;color:#c9d0d7;font-size:15px}}
.buehne{{max-width:1320px;margin:20px auto 40px;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px))}}
.huelle{{display:contents}}

/* ---------- Nachbildung der GitHub-Dateiansicht ---------- */
.gh{{--g-grund:#0d1117;--g-kopf:#010409;--g-rand:#30363d;--g-tinte:#e6edf3;--g-leise:#9198a1;--g-knopf:#212830;
  --g-link:#4493f8;background:var(--g-grund);color:var(--g-tinte);border-radius:10px;overflow:hidden;
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
  box-shadow:0 0 0 1px #000,0 10px 30px rgba(0,0,0,.5)}}
.gh.hell{{--g-grund:#ffffff;--g-kopf:#f6f8fa;--g-rand:#d1d9e0;--g-tinte:#1f2328;--g-leise:#59636e;--g-knopf:#f6f8fa;
  --g-link:#0969da}}
.gh-kopf{{background:var(--g-kopf);height:56px;display:flex;align-items:center;gap:12px;padding:0 16px}}
.gh-kopf .marke{{width:32px;height:32px;border-radius:50%;background:var(--g-tinte);opacity:.9}}
.gh-reiter{{background:var(--g-kopf);display:flex;gap:4px;padding:0 16px;border-bottom:1px solid var(--g-rand);overflow:hidden}}
.gh-reiter span{{padding:8px;white-space:nowrap}}
.gh-reiter span.an{{box-shadow:inset 0 -2px 0 #fd8c73;font-weight:600}}
.gh-rumpf{{display:grid;grid-template-columns:280px minmax(0,1fr);gap:24px;padding:16px 24px;max-width:1280px;margin:0 auto}}
.baum{{border-right:1px solid var(--g-rand);padding-right:16px}}
.baum b{{display:block;margin-bottom:8px}}
.baum ul{{list-style:none;margin:0;padding:0;color:var(--g-leise)}}
.baum li{{padding:3px 8px;border-radius:6px}}
.baum li.an{{background:var(--g-knopf);color:var(--g-tinte)}}
.pfad{{font-size:16px;font-weight:600;margin-bottom:12px}}
.pfad a{{color:var(--g-link)}}
.datei{{border:1px solid var(--g-rand);border-radius:6px;overflow:hidden}}
.datei-kopf{{display:flex;gap:8px;align-items:center;padding:8px 12px;background:var(--g-kopf);border-bottom:1px solid var(--g-rand)}}
.datei-kopf span{{padding:3px 10px;border-radius:6px;color:var(--g-leise)}}
.datei-kopf span.an{{background:var(--g-knopf);color:var(--g-tinte);box-shadow:0 0 0 1px var(--g-rand)}}
.inhalt{{padding:32px}}
.inhalt p{{margin:0 0 16px}}
.inhalt img{{max-width:100%;height:auto;box-sizing:content-box;background-color:var(--g-grund)}}
.inhalt a{{color:var(--g-link)}}
.inhalt details{{margin:0 0 16px}}
.inhalt summary{{cursor:pointer}}
.inhalt ul{{margin:8px 0 0;padding-left:2em}}
.inhalt hr{{border:0;border-top:1px solid var(--g-rand);margin:24px 0}}
/* Schmaler: GitHub bei etwa 1012 px Fensterbreite, Dateibaum eingeklappt */
.mittel .gh{{max-width:1012px;margin:0 auto}}
.mittel .gh-rumpf{{grid-template-columns:minmax(0,1fr)}}
.mittel .baum{{display:none}}
/* Telefon */
.telefon .huelle{{display:block;width:390px;margin:0 auto;border-radius:44px;padding:14px;
  background:linear-gradient(#2c3035,#15171a);box-shadow:inset 0 1px 0 rgba(255,255,255,.15),0 0 0 1px #000}}
.telefon .gh{{border-radius:32px;max-height:780px;overflow:auto}}
.telefon .gh-rumpf{{grid-template-columns:minmax(0,1fr);padding:12px}}
.telefon .baum{{display:none}}
.telefon .inhalt{{padding:12px}}
@media (max-width:1100px){{.gh-rumpf{{grid-template-columns:minmax(0,1fr)}} .baum{{display:none}}}}
@media (max-width:700px){{.telefon .huelle{{width:100%;padding:8px;border-radius:30px}}}}
</style>
</head>
<body>
<header class="steuerung">
  <h1>Katalog-Entwürfe<small>SEITE ALLE PROJEKTE (PROJEKTE.MD)</small></h1>
  <div class="gruppe"><span>ENTWURF</span><div class="schiene" data-wahl="entwurf">{knoepfe}</div></div>
  <div class="gruppe"><span>GITHUB</span><div class="schiene" data-wahl="github">
    <button data-wert="dunkel">Dunkel</button><button data-wert="hell">Hell</button></div></div>
  <div class="gruppe"><span>BREITE</span><div class="schiene" data-wahl="breite">
    <button data-wert="rechner">Rechner</button><button data-wert="mittel">Schmaler</button>
    <button data-wert="telefon">Telefon</button></div></div>
</header>
<section class="steckbrief"><div class="tafel"><h2 id="sb-titel"></h2><p id="sb-idee"></p><ul id="sb-merkmale"></ul></div></section>
<main class="buehne" id="buehne"><div class="huelle"><div class="gh" id="gh">
  <div class="gh-kopf"><span class="marke"></span><b>HalloWelt42 / HalloWelt42</b></div>
  <nav class="gh-reiter"><span class="an">Code</span><span>Issues</span><span>Pull requests</span><span>Actions</span>
    <span>Projects</span><span>Security</span><span>Insights</span></nav>
  <div class="gh-rumpf">
    <aside class="baum"><b>Files</b><ul>{baum}</ul></aside>
    <div>
      <div class="pfad"><a>HalloWelt42</a> / projekte.md</div>
      <div class="datei"><div class="datei-kopf"><span class="an">Preview</span><span>Code</span><span>Blame</span></div>
        <article class="inhalt" id="inhalt"></article></div>
    </div>
  </div>
</div></div></main>
{vorlagen}
<script>
const STECKBRIEFE = {json.dumps(steckbriefe, ensure_ascii=False)};
const VORGABE = {{entwurf: Object.keys(STECKBRIEFE)[0], github: "dunkel", breite: "rechner"}};
const ANKER = Object.fromEntries(Object.entries(STECKBRIEFE).map(([k, sb]) => [k, sb.titel.toLowerCase()]));
const zustand = Object.assign({{}}, VORGABE);
function ankerLesen() {{
  const treffer = Object.keys(ANKER).find(k => ANKER[k] === location.hash.slice(1));
  if (treffer) zustand.entwurf = treffer;
}}
ankerLesen();
window.addEventListener("hashchange", () => {{ ankerLesen(); zeigen(); }});
function zeigen() {{
  for (const schiene of document.querySelectorAll("[data-wahl]"))
    for (const knopf of schiene.querySelectorAll("button"))
      knopf.setAttribute("aria-pressed", String(knopf.dataset.wert === zustand[schiene.dataset.wahl]));
  document.getElementById("inhalt").replaceChildren(document.getElementById("readme-" + zustand.entwurf).content.cloneNode(true));
  const sb = STECKBRIEFE[zustand.entwurf];
  document.getElementById("sb-titel").textContent = `ENTWURF ${{zustand.entwurf.toUpperCase()}}: ${{sb.titel.toUpperCase()}}`;
  document.getElementById("sb-idee").textContent = sb.idee;
  document.getElementById("sb-merkmale").replaceChildren(...sb.merkmale.map(m => Object.assign(document.createElement("li"), {{textContent: m}})));
  document.getElementById("gh").classList.toggle("hell", zustand.github === "hell");
  const buehne = document.getElementById("buehne");
  buehne.classList.toggle("telefon", zustand.breite === "telefon");
  buehne.classList.toggle("mittel", zustand.breite === "mittel");
  try {{ history.replaceState(null, "", "#" + ANKER[zustand.entwurf]); }} catch (fehler) {{ /* Rahmen ohne Verlauf */ }}
}}
for (const schiene of document.querySelectorAll("[data-wahl]"))
  schiene.addEventListener("click", ereignis => {{
    const knopf = ereignis.target.closest("button");
    if (!knopf) return;
    zustand[schiene.dataset.wahl] = knopf.dataset.wert;
    zeigen();
  }});
zeigen();
</script>
</body>
</html>
"""


def als_artefakt(dokument: str) -> str:
    """Fassung für eine geteilte Seite: ohne Dokumenthülle, die setzt der Gastgeber."""
    rumpf = dokument[dokument.index("<title>"):]
    return rumpf.replace("</head>\n<body>\n", "").replace("</body>\n</html>\n", "")
