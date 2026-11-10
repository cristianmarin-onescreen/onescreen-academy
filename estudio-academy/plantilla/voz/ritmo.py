"""Version con ritmo: recorta los silencios de las tomas APROBADAS (sin regenerar nada) y rearma la narracion.
Fuente: aprobada/tomas/*.wav (intactas). Salida: ritmo/tomas, ritmo/narracion_v2.wav, ritmo/tiempos.json."""
import json, os, re, subprocess, sys, time
import urllib.request
from bloques import BLOQUES

from clave import get_key
KEY = get_key()
AQUI = os.path.dirname(os.path.abspath(__file__))
SRC_APR = os.path.join(AQUI, "aprobada", "tomas")
if not os.path.isdir(SRC_APR): SRC_APR = os.path.join(AQUI, "tomas")   # voz aun sin congelar (Cris no la ha aprobado)
SRC_COR = os.path.join(AQUI, "correcciones", "tomas")
OUT = os.path.join(AQUI, "ritmo")
TOM = os.path.join(OUT, "tomas")
os.makedirs(TOM, exist_ok=True)

# silencios >= MIN_D s (a -34 dB) se acortan a PAUSA s (mitad a cada lado); inicio/fin de toma a 0,04 s
UMBRAL_DB, MIN_D, PAUSA = -40, 0.22, 0.20
AIRE_MISMA, AIRE_OTRA = 0.16, 0.80     # entre tomas de una misma idea / entre secciones
# Aire EXTRA tras ciertas tomas (la voz no cambia: solo se alarga la pausa para que el motion respire; Cris 5-nov: se sentia apresurado)
EXTRA = {}   # aire extra tras ciertas tomas (insertos largos): {'b05a': 2.4}


def cortar(src, dst):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=%ddB:d=%s" % (UMBRAL_DB, MIN_D), "-f", "null", "-"], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode().strip())
    if len(ini) > len(fin): fin.append(total)
    quitar = []
    for a0, b0 in zip(ini, fin):
        a0 = max(a0, 0.0)
        if a0 <= 0.01:                       # silencio inicial: dejar 0,04 s
            if b0 - 0.04 > 0: quitar.append((0.0, b0 - 0.04))
        elif b0 >= total - 0.01:             # silencio final: dejar 0,04 s
            quitar.append((a0 + 0.04, total))
        elif b0 - a0 > PAUSA + 0.02:         # pausa interna: queda PAUSA
            quitar.append((a0 + PAUSA / 2, b0 - PAUSA / 2))
    expr = "+".join("between(t,%.4f,%.4f)" % q for q in quitar) or "0"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "aselect='not(%s)',asetpts=N/SR/TB" % expr, "-ac", "1", "-ar", "48000", dst], check=True)
    return len(quitar)


def post(url, headers, data):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def scribe_api(wav):
    b = "----hf%d" % int(time.time() * 1000)
    partes = []
    for k, v in (("model_id", "scribe_v1"), ("language_code", "spa"), ("timestamps_granularity", "word")):
        partes.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (b, k, v)).encode())
    partes.append(("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n" % b).encode() + open(wav, "rb").read() + b"\r\n")
    partes.append(("--%s--\r\n" % b).encode())
    return json.loads(post("https://api.elevenlabs.io/v1/speech-to-text", {"xi-api-key": KEY, "Content-Type": "multipart/form-data; boundary=" + b}, b"".join(partes)))


def scribe(wav):
    try: return scribe_api(wav)
    except Exception as e:
        print('  Scribe no disponible (%s): transcripcion local' % getattr(e,'code',e), flush=True)
        from stt_local import scribe_local
        return scribe_local(wav)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())


ids = [i for i, _ in BLOQUES]
sec = lambda i: re.match(r"b(\d+)", i).group(1)
antes = despues = 0.0
for i in ids:
    s = os.path.join(SRC_COR, i + ".wav") if os.path.exists(os.path.join(SRC_COR, i + ".wav")) else os.path.join(SRC_APR, i + ".wav")
    d = os.path.join(TOM, i + ".wav")
    n = cortar(s, d)
    a, b = dur(s), dur(d); antes += a; despues += b
    sc = scribe(d)
    pal = [{"w": w["text"], "t0": w["start"], "t1": w["end"]} for w in sc.get("words", []) if w.get("type") == "word"]
    json.dump({"id": i, "dur": b, "texto": sc.get("text", ""), "palabras": pal}, open(os.path.join(TOM, i + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("%s %.2f -> %.2f s (%d cortes)" % (i, a, b, n), flush=True)


def silencio(d):
    p = os.path.join(TOM, "sil_%d.wav" % int(d * 1000))
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(d), p], check=True)
    return p


lista, t, bloques, palabras = [], 0.0, [], []
for k, i in enumerate(ids):
    d = json.load(open(os.path.join(TOM, i + ".json"), encoding="utf-8"))
    if k:
        g = (AIRE_MISMA if sec(i) == sec(ids[k - 1]) else AIRE_OTRA) + EXTRA.get(ids[k - 1], 0.0)
        lista.append(silencio(g)); t += g
    lista.append(os.path.join(TOM, i + ".wav"))
    bloques.append({"id": i, "inicio": round(t, 3), "fin": round(t + d["dur"], 3)})
    for w in d["palabras"]:
        palabras.append({"b": i, "w": w["w"], "t0": round(t + w["t0"], 3), "t1": round(t + w["t1"], 3)})
    t += d["dur"]
txt = os.path.join(TOM, "lista.txt")
open(txt, "w").write("".join("file '%s'\n" % p.replace("\\", "/") for p in lista))
out = os.path.join(OUT, "narracion_v2.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", out], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-b:a", "192k", os.path.join(OUT, "narracion_v2.mp3")], check=True)
json.dump({"duracion": round(t, 3), "bloques": bloques, "palabras": palabras}, open(os.path.join(OUT, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tomas: %.1f -> %.1f s | narracion final %.1f s (%d:%02d) (antes 413.6 s)" % (antes, despues, t, t // 60, t % 60))
