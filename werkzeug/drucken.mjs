// Rendert eine HTML-Datei mit Chrome ohne Oberfläche: ein PDF mit allen Seiten und je Seite ein PNG.
//
// Aufruf: node werkzeug/drucken.mjs <seite.html> <ziel.pdf> <png-ordner> <seitenkante-px>
// Jede Seite ist ein Element .seite mit der Kante als Breite und Höhe. Chrome-Pfad über CHROME änderbar.
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [seite, pdfZiel, pngOrdner, kanteText] = process.argv.slice(2);
if (!kanteText) {
  console.error('Aufruf: node drucken.mjs <seite.html> <ziel.pdf> <png-ordner> <seitenkante-px>');
  process.exit(2);
}
const KANTE = Number(kanteText);
const PNG_FAKTOR = 2;
const CHROME = process.env.CHROME ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const warten = (ms) => new Promise((fertig) => setTimeout(fertig, ms));

async function chromeStarten() {
  const profil = mkdtempSync(join(tmpdir(), 'portfolio-chrome-'));
  const prozess = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=0', '--remote-allow-origins=*', `--user-data-dir=${profil}`, 'about:blank',
  ], { stdio: 'ignore' });
  const portDatei = join(profil, 'DevToolsActivePort');
  for (let versuch = 0; versuch < 100 && !existsSync(portDatei); versuch++) await warten(100);
  const port = readFileSync(portDatei, 'utf8').split('\n')[0];
  const ziele = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
  const ziel = ziele.find((z) => z.type === 'page');
  return { prozess, profil, adresse: ziel.webSocketDebuggerUrl };
}

function verbinden(adresse) {
  const socket = new WebSocket(adresse);
  const offen = new Map();
  const ereignisse = new Map();
  let naechste = 1;
  socket.addEventListener('message', ({ data }) => {
    const nachricht = JSON.parse(data);
    if (nachricht.id && offen.has(nachricht.id)) {
      const { fertig, fehler } = offen.get(nachricht.id);
      offen.delete(nachricht.id);
      nachricht.error ? fehler(new Error(nachricht.error.message)) : fertig(nachricht.result);
    } else if (nachricht.method && ereignisse.has(nachricht.method)) {
      ereignisse.get(nachricht.method)(nachricht.params);
      ereignisse.delete(nachricht.method);
    }
  });
  const senden = (method, params = {}) => new Promise((fertig, fehler) => {
    const id = naechste++;
    offen.set(id, { fertig, fehler });
    socket.send(JSON.stringify({ id, method, params }));
  });
  const einmal = (method) => new Promise((fertig) => ereignisse.set(method, fertig));
  const bereit = new Promise((fertig) => socket.addEventListener('open', fertig));
  return { bereit, senden, einmal, schliessen: () => socket.close() };
}

const chrome = await chromeStarten();
const cdp = verbinden(chrome.adresse);
try {
  await cdp.bereit;
  await cdp.senden('Page.enable');
  await cdp.senden('Emulation.setDeviceMetricsOverride', {
    width: KANTE, height: KANTE, deviceScaleFactor: PNG_FAKTOR, mobile: false,
  });
  const geladen = cdp.einmal('Page.loadEventFired');
  await cdp.senden('Page.navigate', { url: pathToFileURL(resolve(seite)).href });
  await geladen;
  const { result } = await cdp.senden('Runtime.evaluate', {
    expression: `document.fonts.ready.then(() => Promise.all([...document.images].map((b) => b.decode().catch(() => null))))
      .then(() => document.querySelectorAll('.seite').length)`,
    awaitPromise: true,
    returnByValue: true,
  });
  const seiten = result.value;

  const pdf = await cdp.senden('Page.printToPDF', { printBackground: true, preferCSSPageSize: true });
  writeFileSync(pdfZiel, Buffer.from(pdf.data, 'base64'));

  for (let i = 0; i < seiten; i++) {
    const bild = await cdp.senden('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: true,
      clip: { x: 0, y: i * KANTE, width: KANTE, height: KANTE, scale: 1 },
    });
    writeFileSync(join(pngOrdner, `seite-${String(i + 1).padStart(2, '0')}.png`), Buffer.from(bild.data, 'base64'));
  }
  console.log(`${seiten} Seiten: ${pdfZiel} und PNGs in ${pngOrdner}`);
} finally {
  cdp.schliessen();
  chrome.prozess.kill();
  await warten(300);
  rmSync(chrome.profil, { recursive: true, force: true });
}
