"""Arma index.html (video completo) con las escenas de compositions/, o una prueba de una sola escena/inserto.
Fondos POR ESCENA (Cris, 5-nov: «todo es azul, es monotono»): cada escena tiene su propio color y textura; el corte es directo.
Uso:  python armar_maestro.py          -> video completo
      python armar_maestro.py s05      -> solo esa escena (con su tramo de audio)
      python armar_maestro.py s05a-resumen -> solo ese inserto"""
import glob, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_J = json.load(open(os.path.join(AQUI, "escenas.json"), encoding="utf-8"))
ESC, INS = _J["escenas"], _J["insertos"]
TOTAL = ESC[-1]["fin"]
solo = sys.argv[1] if len(sys.argv) > 1 else None

DOTS = lambda px, a: "radial-gradient(rgba(255,255,255,%s) 1.4px, transparent 1.7px) 0 0/%dpx %dpx" % (a, px, px)
LINES = "repeating-linear-gradient(135deg, rgba(255,255,255,.055) 0 1.5px, transparent 1.5px 20px)"
CROSS = "repeating-linear-gradient(45deg, rgba(255,255,255,.04) 0 1px, transparent 1px 22px), repeating-linear-gradient(135deg, rgba(255,255,255,.04) 0 1px, transparent 1px 22px)"
RINGS = "repeating-radial-gradient(circle at 50% 50%, rgba(255,255,255,.07) 0 1.5px, transparent 1.5px 96px)"
SCAN = "repeating-linear-gradient(0deg, rgba(255,255,255,.045) 0 1px, transparent 1px 7px)"
GRID = "linear-gradient(rgba(255,255,255,.05) 1.5px, transparent 1.5px) 0 0/48px 48px, linear-gradient(90deg, rgba(255,255,255,.05) 1.5px, transparent 1.5px) 0 0/48px 48px"
TEX = {"dots44": DOTS(44, .17), "dots60": DOTS(60, .15), "dots26": DOTS(26, .10), "lines": LINES, "cross": CROSS, "rings": RINGS, "scan": SCAN, "grid": GRID}
THEMES = {e["id"]: (e["tema"][0], e["tema"][1], e["tema"][2], TEX[e["tema"][3]]) for e in ESC}

archivos = {os.path.basename(p).split("-")[0]: os.path.basename(p)[:-5] for p in glob.glob(os.path.join(AQUI, "compositions", "s[0-9][0-9]*-*.html"))}
archivos_i = {os.path.basename(p)[:-5]: 1 for p in glob.glob(os.path.join(AQUI, "compositions", "s[0-9][0-9][a-z]-*.html"))}
solo_ins = next((e for e in INS if e["id"] == solo), None) if solo else None

hosts, escenas_vis = [], []
for e in ESC:
    if solo_ins: break
    if e["id"] not in archivos or (solo and e["id"] != solo): continue
    cid = archivos[e["id"]]
    ini = 0.0 if solo else e["inicio"]
    escenas_vis.append((e["id"], ini, ini + e["dur"]))
    hosts.append('  <div id="host-%s" class="scene-host clip" data-composition-id="%s" data-composition-src="compositions/%s.html" data-start="%.3f" data-duration="%.3f" data-track-index="1" data-width="1920" data-height="1080"></div>' % (e["id"], cid, cid, ini, e["dur"]))
for e in INS:
    if solo_ins and e is not solo_ins: continue
    if e["id"] not in archivos_i: continue
    esc_id = e["id"][:3]
    if solo and not solo_ins and esc_id != solo: continue
    base = next(x for x in ESC if x["id"] == esc_id)
    ini = 0.0 if solo_ins else ((e["inicio"] - base["inicio"]) if solo else e["inicio"])
    hosts.append('  <div id="host-%s" class="scene-host clip" data-composition-id="%s" data-composition-src="compositions/%s.html" data-start="%.3f" data-duration="%.3f" data-track-index="2" data-width="1920" data-height="1080"></div>' % (e["id"], e["id"], e["id"], ini, e["dur"]))

if solo_ins:
    dur, audio_media = solo_ins["dur"], solo_ins["inicio"]
    escenas_vis = [(solo_ins["id"][:3], 0.0, dur)]
elif solo:
    e = next(x for x in ESC if x["id"] == solo)
    dur, audio_media = e["dur"], e["inicio"]
else:
    dur, audio_media = TOTAL, 0.0

bgdivs, bgcss, bgjs = [], [], []
for k, (sid, ini, fin) in enumerate(escenas_vis):
    c0, c1, c2, tex = THEMES[sid]
    bgcss.append('  #bg-%s { background: radial-gradient(ellipse 80%% 70%% at 50%% 48%%, %s 0%%, %s 44%%, %s 100%%); opacity: %d; }\n  #bg-%s .tx { position: absolute; inset: -60px; background: %s; opacity: .55; }' % (sid, c0, c1, c2, 1 if k == 0 else 0, sid, tex))
    bgdivs.append('<div class="bgs" id="bg-%s"><div class="tx"></div></div>' % sid)
    if k > 0:
        bgjs.append('  tl.set("#bg-%s", { opacity: 0 }, %.3f); tl.set("#bg-%s", { opacity: 1 }, %.3f);' % (escenas_vis[k - 1][0], ini, sid, ini))
    bgjs.append('  tl.fromTo("#bg-%s .tx", { x: 0, y: 0 }, { x: 40, y: 30, duration: %.3f, ease: "none" }, %.3f);' % (sid, fin - ini, ini))

html = """<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>@TITULO@ · OneScreen Academy</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="stylesheet" href="assets/academy.css" />
<script src="assets/tiempos.js"></script>
<script src="assets/academy.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1920px; height: 1080px; overflow: hidden; background: #020a2e; }
  #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #020a2e; }
  .scene-host { position: absolute; inset: 0; }
  .bgs { position: absolute; inset: 0; overflow: hidden; }
@BGCSS@
  .bg-vig { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse 72% 66% at 50% 50%, rgba(0,0,0,0) 40%, rgba(1,4,22,.46) 80%, rgba(0,2,14,.8) 100%); }
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="@DUR@" data-fps="30">
  @BGDIVS@<div class="bg-vig"></div>
@HOSTS@
  <audio id="narr" src="assets/narracion.wav" data-start="0" data-duration="@DUR@" data-media-start="@AM@" data-track-index="10" data-volume="1"></audio>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
@BGJS@
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
html = (html.replace("@BGCSS@", "\n".join(bgcss)).replace("@BGDIVS@", "".join(bgdivs)).replace("@BGJS@", "\n".join(bgjs))
        .replace("@TITULO@", _J.get("titulo", "SuprNotes")).replace("@DUR@", "%.3f" % dur).replace("@HOSTS@", "\n".join(hosts)).replace("@AM@", "%.3f" % audio_media))
open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8").write(html)
print("escrito index.html con", len(hosts), "escena(s), %.1f s" % dur)
