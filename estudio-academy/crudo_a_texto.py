"""Crudo -> audio, transcripcion con timestamps (Scribe) y fotogramas con hojas de contacto.
Uso: python crudo_a_texto.py "<video.mp4>" "cursos/<modulo>"   (clave en ELEVENLABS_API_KEY)"""
import json, os, subprocess, sys, urllib.request, uuid, glob

video, mod = sys.argv[1], sys.argv[2]
crudo = os.path.join(mod, "crudo"); fr = os.path.join(crudo, "frames"); os.makedirs(fr, exist_ok=True)
wav = os.path.join(crudo, "audio.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1/5,scale=640:360", os.path.join(fr, "f_%04d.jpg")], check=True)
lst = sorted(glob.glob(os.path.join(fr, "f_*.jpg")))
for k in range(0, len(lst), 20):  # hojas de 20 fotogramas (cada 5 s)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-start_number", str(k + 1), "-framerate", "1", "-i", os.path.join(fr, "f_%04d.jpg"), "-vf", "tile=4x5", "-frames:v", "1", "-update", "1", os.path.join(crudo, "hoja_%02d.jpg" % (k // 20 + 1))], check=True)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "plantilla", "voz")); from clave import get_key
key = get_key(); b = uuid.uuid4().hex
datos = open(wav, "rb").read()
def campo(n, v): return ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, n, v)).encode()
cuerpo = campo("model_id", "scribe_v1") + campo("language_code", "es") + campo("timestamps_granularity", "word") + \
    ('--%s\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\nContent-Type: audio/wav\r\n\r\n' % b).encode() + datos + ("\r\n--%s--\r\n" % b).encode()
req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=cuerpo, headers={"xi-api-key": key, "Content-Type": "multipart/form-data; boundary=" + b})
out = json.loads(urllib.request.urlopen(req, timeout=600).read())
json.dump(out, open(os.path.join(crudo, "scribe.json"), "w", encoding="utf-8"), ensure_ascii=False)
# texto con marcas de tiempo cada ~frase
txt, cur, t0 = [], [], None
for w in out.get("words", []):
    if w.get("type") != "word": continue
    if t0 is None: t0 = w["start"]
    cur.append(w["text"])
    if w["text"].endswith((".", "?", "!")) or len(cur) > 28:
        txt.append("[%5.1f] %s" % (t0, " ".join(cur))); cur, t0 = [], None
if cur: txt.append("[%5.1f] %s" % (t0, " ".join(cur)))
open(os.path.join(crudo, "transcripcion.txt"), "w", encoding="utf-8").write("\n".join(txt))
print("ok", mod, len(txt), "frases")
