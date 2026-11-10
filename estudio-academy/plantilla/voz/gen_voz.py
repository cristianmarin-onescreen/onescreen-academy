"""Genera la voz del modulo con ElevenLabs v4. Clave en ELEVENLABS_API_KEY (nunca en el codigo).
Uso: python gen_voz.py [id ...]   (sin ids = todos). No sobrescribe tomas ya generadas salvo --forzar."""
import json, os, subprocess, sys, time
import urllib.request, urllib.error
from bloques import BLOQUES, limpio, dirigido

from clave import get_key
KEY = get_key()
VOZ = os.environ.get("ACADEMY_VOZ_ID") or sys.exit("Falta ACADEMY_VOZ_ID: corre python setup.py (elige la voz de tu cuenta de ElevenLabs)")
FORMATO = os.environ.get("ACADEMY_FORMATO", "wav_48000")        # sin compresion (mejor calidad); mp3_44100_128 si hiciera falta
MODELO = "eleven_v4"
AJUSTES = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True}
AQUI = os.path.dirname(os.path.abspath(__file__))
CORR = "--correccion" in sys.argv
TOMAS = os.path.join(AQUI, "correcciones", "tomas") if CORR else os.path.join(AQUI, "tomas")
os.makedirs(TOMAS, exist_ok=True)

if not CORR: open(os.path.join(AQUI, "guion_limpio.txt"), "w", encoding="utf-8").write("\n\n".join("## %s\n%s" % (i, limpio(t)) for i, t in BLOQUES))
if not CORR: open(os.path.join(AQUI, "guion_dirigido.txt"), "w", encoding="utf-8").write("\n\n".join("## %s\n%s" % (i, dirigido(t)) for i, t in BLOQUES))

if os.path.isdir(os.path.join(AQUI, "aprobada")) and not CORR:
    sys.exit("Voz aprobada y congelada (carpeta aprobada/). No se regenera.")
if CORR and not [a for a in sys.argv[1:] if not a.startswith("--")]:
    sys.exit("--correccion exige ids explicitos (solo las tomas que Cris autorizo corregir).")
forzar = "--forzar" in sys.argv
ids = [a for a in sys.argv[1:] if not a.startswith("--")] or [i for i, _ in BLOQUES]


def post(url, body=None, headers=None, data=None):
    req = urllib.request.Request(url, data=data if data is not None else json.dumps(body).encode(), headers=headers or {}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def tts(texto, prev, nxt):
    body = {"text": texto, "model_id": MODELO, "language_code": "es", "voice_settings": AJUSTES}
    if prev: body["previous_text"] = prev
    if nxt: body["next_text"] = nxt
    h = {"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"}
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=%s" % (VOZ, FORMATO)
    try:
        return post(url, body, h)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")[:600]
        print("  HTTP", e.code, detalle)
        if e.code == 400 and ("previous_text" in detalle or "next_text" in detalle):
            body.pop("previous_text", None); body.pop("next_text", None)
            return post(url, body, h)
        raise


def scribe(wav):
    b = "----hf%d" % int(time.time())
    partes = []
    for k, v in (("model_id", "scribe_v1"), ("language_code", "spa"), ("timestamps_granularity", "word")):
        partes.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (b, k, v)).encode())
    partes.append(("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n" % b).encode() + open(wav, "rb").read() + b"\r\n")
    partes.append(("--%s--\r\n" % b).encode())
    out = post("https://api.elevenlabs.io/v1/speech-to-text", headers={"xi-api-key": KEY, "Content-Type": "multipart/form-data; boundary=" + b}, data=b"".join(partes))
    return json.loads(out)


orden = [i for i, _ in BLOQUES]
mapa = dict(BLOQUES)
for bid in ids:
    wav = os.path.join(TOMAS, bid + ".wav")
    if os.path.exists(wav) and not forzar:
        print(bid, "ya existe, se conserva"); continue
    k = orden.index(bid)
    prev = dirigido(mapa[orden[k - 1]]) if k > 0 else None
    nxt = dirigido(mapa[orden[k + 1]]) if k + 1 < len(orden) else None
    print(bid, "generando...", flush=True)
    audio = tts(dirigido(mapa[bid]), prev, nxt)
    crudo = os.path.join(TOMAS, bid + (".wav.src" if FORMATO.startswith("wav") else ".mp3"))
    open(crudo, "wb").write(audio)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "wav" if FORMATO.startswith("wav") else "mp3", "-i", crudo, "-ac", "1", "-ar", "48000", wav], check=True)
    sc = scribe(wav)
    palabras = [{"w": w["text"], "t0": w["start"], "t1": w["end"]} for w in sc.get("words", []) if w.get("type") == "word"]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode().strip())
    json.dump({"id": bid, "dur": dur, "texto": sc.get("text", ""), "palabras": palabras}, open(os.path.join(TOMAS, bid + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("  %s: %.2f s, %d palabras" % (bid, dur, len(palabras)))
