"""Vorschauseite: zeigt jeden Entwurf im Rahmen einer GitHub-Profilseite, dunkel und hell, Rechner und Telefon.

Der README-Ausschnitt jedes Entwurfs wird unverändert eingesetzt, so wie GitHub ihn darstellen würde.
Der Anker merkt sich den Entwurf: #studio-rack, #leitwarte, #signatur
"""
from __future__ import annotations

import base64
import json

from daten import Auswahl
from entwurf import Ergebnis, Steckbrief
from material import esc, schriften

SPRACHFARBEN = {"Python": "#3572A5", "Svelte": "#ff3e00", "HTML": "#e34c26", "JavaScript": "#f1e05a",
                "TypeScript": "#3178c6", "Swift": "#F05138"}

UMSETZUNG = (
    "Alles sind SVG-Dateien im Profil-Repo, eingebunden mit <img>; nur das lässt GitHub in einer README zu.",
    "Schrift (Chakra Petch), Icons und Bildschirmfotos stecken eingebettet im SVG, so wie heute schon bei den Kacheln.",
    "Bewegung (Nadeln, LEDs, Lichtlauf) per CSS im SVG; sie ruht, wenn der Betrachter Bewegung abgeschaltet hat.",
    "Jede Grafik ist ein eigener Link; zwei Kacheln je Zeile brechen auf schmalen Schirmen von selbst um.",
    "Die Platten bleiben auch im hellen GitHub dunkel, wie ein Gerät auf hellem Tisch.",
    "Erzeugt aus projekte.toml mit dem vorhandenen Werkzeug; die volle Liste wandert nach projekte.md.",
)


def _beitragsraster() -> str:
    zellen = []
    for woche in range(53):
        for tag in range(7):
            wert = (woche * 37 + tag * 11 + woche * tag) % 23
            stufe = 0 if wert < 9 else 1 if wert < 15 else 2 if wert < 19 else 3 if wert < 22 else 4
            zellen.append(f'<i class="b{stufe}" style="grid-column:{woche + 1};grid-row:{tag + 1}"></i>')
    return "".join(zellen)


def _angeheftet(auswahl: Auswahl) -> str:
    karten = []
    for p in auswahl.projekte:
        sprache = p.technik[0]
        karten.append(
            '<div class="pin"><div class="pin-kopf"><svg viewBox="0 0 16 16" width="16" height="16">'
            '<path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 '
            '0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 '
            '1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8Z" fill="currentColor"/></svg>'
            f'<a>{esc(p.repo)}</a><span class="oeffentlich">Public</span></div>'
            f'<p>{esc(p.info)}</p><div class="sprache"><span style="background:{SPRACHFARBEN.get(sprache, "#888")}">'
            f'</span>{esc(sprache)}</div></div>'
        )
    return "".join(karten)


def _svg_url(inhalt: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(inhalt.encode("utf-8")).decode("ascii")


def _eingebettet(ergebnis: Ergebnis) -> str:
    """README-Ausschnitt mit eingebetteten Bildern: die Vorschau braucht so keinen Server."""
    readme = ergebnis.readme
    for datei, inhalt in ergebnis.dateien.items():
        readme = readme.replace(f'src="{ergebnis.kennung}/{datei}"', f'src="{_svg_url(inhalt)}"')
    return readme


def als_artefakt(dokument: str) -> str:
    """Fassung für eine geteilte Seite: ohne Dokumenthülle, die setzt der Gastgeber."""
    kopf_ende = dokument.index("<title>")
    rumpf = dokument[kopf_ende:].replace("</head>\n<body>\n", "").replace("</body>\n</html>\n", "")
    return rumpf


def seite(auswahl: Auswahl, entwuerfe: list[tuple[Steckbrief, Ergebnis]]) -> str:
    steckbriefe = {s.kennung: {"titel": s.titel, "idee": s.idee, "merkmale": list(s.merkmale),
                               "avatar": _svg_url(e.dateien["avatar.svg"])} for s, e in entwuerfe}
    vorlagen = "".join(f'<template id="readme-{s.kennung}">{_eingebettet(e)}</template>' for s, e in entwuerfe)
    knoepfe = "".join(
        f'<button data-wert="{s.kennung}"><b>{s.kennung.upper()}</b> {esc(s.titel)}</button>' for s, _ in entwuerfe
    )
    umsetzung = "".join(f"<li>{esc(z)}</li>" for z in UMSETZUNG)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Profil-Entwürfe</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
{schriften(400, 600, 700)}
:root{{--grund:#121417;--leiste:#1b1e22;--schiene:#0b0c0e;--tinte:#e6eaee;--leise:#9aa3ad;--akzent:#ffae1a;
  --rollfeld-oben:0px;color-scheme:dark}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--grund);color:var(--tinte);font:17px/1.5 'Chakra Petch',sans-serif}}
.steuerung{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:linear-gradient(#24282d,#1a1d21);
  border-bottom:1px solid #000;box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 6px 18px rgba(0,0,0,.5);
  padding-block:12px;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:#24282d}}
.steuerung h1{{margin:0;font-size:20px;font-weight:700;letter-spacing:.06em;margin-right:auto}}
.steuerung h1 small{{display:block;font-size:13px;font-weight:600;color:var(--leise);letter-spacing:.12em}}
.gruppe{{display:flex;align-items:center;gap:8px}}
.gruppe>span{{font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--leise)}}
.schiene{{display:flex;padding:3px;gap:3px;background:var(--schiene);border-radius:8px;
  box-shadow:inset 0 2px 4px rgba(0,0,0,.8),0 1px 0 rgba(255,255,255,.07)}}
.schiene button{{font:600 15px 'Chakra Petch',sans-serif;color:var(--leise);background:transparent;border:0;
  padding:6px 12px;border-radius:6px;cursor:pointer;white-space:nowrap}}
.schiene button b{{color:#c8ced5}}
.schiene button:hover{{color:var(--tinte)}}
.schiene button[aria-pressed=true]{{color:#ffcf6b;background:linear-gradient(#3a3f45,#2a2e33);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 2px 4px rgba(0,0,0,.6);text-shadow:0 0 8px rgba(255,174,26,.45)}}
.schiene button[aria-pressed=true] b{{color:#ffcf6b}}
.steckbrief{{max-width:1280px;margin:20px auto 0;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:20px}}
.tafel{{background:linear-gradient(#24272b,#1c1f22);border-radius:10px;padding:16px 20px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 0 0 1px #000,0 6px 16px rgba(0,0,0,.4)}}
.tafel h2{{margin:0 0 6px;font-size:15px;letter-spacing:.16em;color:var(--akzent)}}
.tafel p{{margin:0 0 8px}}
.tafel ul{{margin:0;padding-left:18px;color:#c9d0d7;font-size:15px}}
.buehne{{max-width:1320px;margin:20px auto 40px;padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px))}}
.schiene button:focus-visible{{outline:2px solid var(--akzent);outline-offset:1px}}
.telefon-huelle{{display:contents}}

/* ---------- Nachbildung der GitHub-Profilseite ---------- */
.gh{{--g-grund:#0d1117;--g-kopf:#010409;--g-rand:#30363d;--g-tinte:#e6edf3;--g-leise:#9198a1;--g-knopf:#212830;
  --g-b0:#151b23;--g-b1:#033a16;--g-b2:#196c2e;--g-b3:#2ea043;--g-b4:#56d364;
  background:var(--g-grund);color:var(--g-tinte);border-radius:10px;overflow:hidden;
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
  box-shadow:0 0 0 1px #000,0 10px 30px rgba(0,0,0,.5)}}
.gh.hell{{--g-grund:#ffffff;--g-kopf:#f6f8fa;--g-rand:#d1d9e0;--g-tinte:#1f2328;--g-leise:#59636e;--g-knopf:#f6f8fa;
  --g-b0:#eff2f5;--g-b1:#aceebb;--g-b2:#4ac26b;--g-b3:#2da44e;--g-b4:#116329}}
.gh-kopf{{background:var(--g-kopf);height:64px;display:flex;align-items:center;gap:14px;padding:0 16px;
  border-bottom:1px solid var(--g-rand)}}
.gh-kopf .marke{{width:32px;height:32px;border-radius:50%;background:var(--g-tinte);opacity:.9}}
.gh-kopf b{{font-size:14px}}
.gh-kopf .suche{{margin-left:auto;width:260px;height:32px;border:1px solid var(--g-rand);border-radius:6px;
  color:var(--g-leise);font-size:13px;display:flex;align-items:center;padding:0 10px}}
.gh-kopf .mini{{width:32px;height:32px;border-radius:50%;overflow:hidden}}
.gh-kopf .mini img{{width:100%;height:100%}}
.gh-reiter{{background:var(--g-kopf);display:flex;gap:4px;padding:0 16px;border-bottom:1px solid var(--g-rand);
  overflow:hidden}}
.gh-reiter span{{padding:10px 8px;font-size:14px;white-space:nowrap}}
.gh-reiter span.an{{box-shadow:inset 0 -2px 0 #fd8c73;font-weight:600}}
.gh-reiter em{{font-style:normal;background:var(--g-knopf);border-radius:2em;padding:0 6px;font-size:12px;margin-left:4px}}
.gh-rumpf{{display:grid;grid-template-columns:296px minmax(0,1fr);gap:24px;padding:24px 32px;max-width:1280px;margin:0 auto}}
.gh-seite .avatar{{width:100%;aspect-ratio:1;border-radius:50%;box-shadow:0 0 0 1px var(--g-rand)}}
.gh-seite .avatar img{{width:100%;height:100%;border-radius:50%;display:block}}
.gh-seite h3{{margin:16px 0 0;font-size:24px;line-height:1.25}}
.gh-seite .login{{font-size:20px;font-weight:300;color:var(--g-leise)}}
.gh-seite .knopf{{margin:16px 0;border:1px solid var(--g-rand);background:var(--g-knopf);border-radius:6px;
  text-align:center;padding:5px;font-weight:500}}
.gh-seite .leise{{color:var(--g-leise);margin:6px 0}}
.gh-seite .leise b{{color:var(--g-tinte)}}
.gh-haupt{{min-width:0}}
.readme{{border:1px solid var(--g-rand);border-radius:6px;padding:24px}}
.readme .pfad{{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;margin-bottom:16px}}
.readme .inhalt p{{margin:0 0 16px}}
.readme .inhalt p:last-child{{margin-bottom:0}}
.readme .inhalt img{{max-width:100%;height:auto;box-sizing:content-box;background-color:var(--g-grund)}}
.readme .inhalt a{{color:#4493f8}}
.gh h4{{font-size:16px;font-weight:400;margin:24px 0 8px}}
.pins{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}
.pin{{border:1px solid var(--g-rand);border-radius:6px;padding:16px;font-size:12px;color:var(--g-leise)}}
.pin-kopf{{display:flex;align-items:center;gap:8px;color:var(--g-leise)}}
.pin-kopf a{{color:#4493f8;font-weight:600;font-size:14px}}
.gh.hell .pin-kopf a,.gh.hell .readme .inhalt a{{color:#0969da}}
.oeffentlich{{border:1px solid var(--g-rand);border-radius:2em;padding:0 7px;font-size:12px;margin-left:auto}}
.pin p{{margin:8px 0 16px}}
.sprache{{display:flex;align-items:center;gap:6px}}
.sprache span{{width:12px;height:12px;border-radius:50%}}
.beitraege{{border:1px solid var(--g-rand);border-radius:6px;padding:16px;overflow:hidden}}
.raster{{display:grid;grid-template-columns:repeat(53,10px);grid-template-rows:repeat(7,10px);gap:3px}}
.raster i{{border-radius:2px;background:var(--g-b0)}}
.raster .b1{{background:var(--g-b1)}}.raster .b2{{background:var(--g-b2)}}
.raster .b3{{background:var(--g-b3)}}.raster .b4{{background:var(--g-b4)}}

/* Schmaler: GitHub bei etwa 1012 px Fensterbreite, schmalere Seitenleiste und README-Spalte */
.mittel .gh{{max-width:1012px;margin:0 auto}}
.mittel .gh-rumpf{{grid-template-columns:256px minmax(0,1fr);padding:24px}}
/* Telefon: GitHub stapelt die Spalten, Profilbild klein neben dem Namen */
.telefon .telefon-huelle{{display:block;width:390px;margin:0 auto;border-radius:44px;padding:14px;
  background:linear-gradient(#2c3035,#15171a);box-shadow:inset 0 1px 0 rgba(255,255,255,.15),0 0 0 1px #000,0 20px 40px rgba(0,0,0,.6)}}
.telefon .gh{{border-radius:32px;max-height:780px;overflow:auto}}
.telefon .gh-kopf .suche,.telefon .gh-kopf b{{display:none}}
.telefon .gh-rumpf{{grid-template-columns:minmax(0,1fr);padding:16px;gap:16px}}
.telefon .gh-seite{{display:grid;grid-template-columns:72px minmax(0,1fr);gap:0 14px;align-items:center}}
.telefon .gh-seite .avatar{{grid-row:span 2}}
.telefon .gh-seite h3{{margin:0;font-size:20px}}
.telefon .gh-seite .login{{font-size:16px}}
.telefon .gh-seite .knopf,.telefon .gh-seite .leise{{grid-column:1/-1}}
.telefon .readme{{padding:16px}}
.telefon .pins{{grid-template-columns:minmax(0,1fr)}}
@media (max-width:1100px){{.steckbrief{{grid-template-columns:minmax(0,1fr)}}
  .gh-rumpf{{grid-template-columns:minmax(0,1fr)}} .gh-seite{{max-width:296px}}}}
@media (max-width:700px){{.telefon .telefon-huelle{{width:100%;padding:8px;border-radius:30px}}
  .gh-kopf .suche{{display:none}}}}
</style>
</head>
<body>
<header class="steuerung">
  <h1>Profil-Entwürfe<small>GITHUB-STARTSEITE HALLOWELT42</small></h1>
  <div class="gruppe"><span>ENTWURF</span><div class="schiene" data-wahl="entwurf">{knoepfe}</div></div>
  <div class="gruppe"><span>GITHUB</span><div class="schiene" data-wahl="github">
    <button data-wert="dunkel">Dunkel</button><button data-wert="hell">Hell</button></div></div>
  <div class="gruppe"><span>BREITE</span><div class="schiene" data-wahl="breite">
    <button data-wert="rechner">Rechner</button><button data-wert="mittel">Schmaler</button>
    <button data-wert="telefon">Telefon</button></div></div>
</header>
<section class="steckbrief">
  <div class="tafel"><h2 id="sb-titel"></h2><p id="sb-idee"></p><ul id="sb-merkmale"></ul></div>
  <div class="tafel"><h2>SO WIRD ES UMGESETZT</h2><ul>{umsetzung}</ul></div>
</section>
<main class="buehne" id="buehne">
 <div class="telefon-huelle">
  <div class="gh" id="gh">
    <div class="gh-kopf"><span class="marke"></span><b>HalloWelt42</b><span class="suche">Type / to search</span>
      <span class="mini"><img id="avatar-klein" alt=""></span></div>
    <nav class="gh-reiter"><span class="an">Overview</span><span>Repositories<em>215</em></span><span>Projects</span>
      <span>Packages</span><span>Stars<em>221</em></span></nav>
    <div class="gh-rumpf">
      <aside class="gh-seite">
        <div class="avatar"><img id="avatar" alt="Profilbild-Vorschlag"></div>
        <div><h3>HalloWelt42</h3><div class="login">HalloWelt42</div></div>
        <div class="knopf">Edit profile</div>
        <div class="leise"><b>27</b> followers · <b>68</b> following</div>
        <div class="leise">Sachsen-Anhalt (Deutschland)</div>
      </aside>
      <div class="gh-haupt">
        <article class="readme"><div class="pfad">HalloWelt42 / README.md</div><div class="inhalt" id="inhalt"></div></article>
        <h4>Pinned</h4><div class="pins">{_angeheftet(auswahl)}</div>
        <h4>Beiträge im letzten Jahr</h4><div class="beitraege"><div class="raster">{_beitragsraster()}</div></div>
      </div>
    </div>
  </div>
 </div>
</main>
{vorlagen}
<script>
const STECKBRIEFE = {json.dumps(steckbriefe, ensure_ascii=False)};
const VORGABE = {{entwurf: Object.keys(STECKBRIEFE)[0], github: "dunkel", breite: "rechner"}};
// Direktlink je Entwurf über den Anker (#studio-rack, #leitwarte, #signatur)
const ANKER = Object.fromEntries(Object.entries(STECKBRIEFE).map(([k, sb]) => [k, sb.titel.toLowerCase().replace(/[^a-z0-9]+/g, "-")]));
const zustand = Object.assign({{}}, VORGABE);
function ankerLesen() {{
  const name = location.hash.slice(1);
  const treffer = Object.keys(ANKER).find(k => ANKER[k] === name);
  if (treffer) zustand.entwurf = treffer;
}}
ankerLesen();
window.addEventListener("hashchange", () => {{ ankerLesen(); zeigen(); }});
function zeigen() {{
  for (const schiene of document.querySelectorAll("[data-wahl]")) {{
    for (const knopf of schiene.querySelectorAll("button"))
      knopf.setAttribute("aria-pressed", String(knopf.dataset.wert === zustand[schiene.dataset.wahl]));
  }}
  const vorlage = document.getElementById("readme-" + zustand.entwurf);
  document.getElementById("inhalt").replaceChildren(vorlage.content.cloneNode(true));
  const sb = STECKBRIEFE[zustand.entwurf];
  document.getElementById("sb-titel").textContent = `ENTWURF ${{zustand.entwurf.toUpperCase()}}: ${{sb.titel.toUpperCase()}}`;
  document.getElementById("sb-idee").textContent = sb.idee;
  document.getElementById("sb-merkmale").replaceChildren(...sb.merkmale.map(m => Object.assign(document.createElement("li"), {{textContent: m}})));
  for (const id of ["avatar", "avatar-klein"]) document.getElementById(id).src = sb.avatar;
  document.getElementById("gh").classList.toggle("hell", zustand.github === "hell");
  document.getElementById("buehne").classList.toggle("telefon", zustand.breite === "telefon");
  document.getElementById("buehne").classList.toggle("mittel", zustand.breite === "mittel");
  try {{ history.replaceState(null, "", "#" + ANKER[zustand.entwurf]); }} catch (fehler) {{ /* Rahmen ohne Verlauf */ }}
}}
for (const schiene of document.querySelectorAll("[data-wahl]")) {{
  schiene.addEventListener("click", ereignis => {{
    const knopf = ereignis.target.closest("button");
    if (!knopf) return;
    zustand[schiene.dataset.wahl] = knopf.dataset.wert;
    zeigen();
  }});
}}
zeigen();
</script>
</body>
</html>
"""
