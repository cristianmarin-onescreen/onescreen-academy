"""Une las tomas en una sola narracion con pausas y escribe los tiempos por palabra en el eje del video."""
import json, os, re, subprocess
from bloques import BLOQUES

AQUI = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(AQUI, "tomas")
ids = [i for i, _ in BLOQUES]
sec = lambda i: re.match(r"b(\d+)", i).group(1)
AIRE_MISMA, AIRE_OTRA = 0.35, 0.85

silencios = {}
def silencio(d):
    p = os.path.join(T, "sil_%d.wav" % int(d * 1000))
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(d), p], check=True)
    return p

lista, t, bloques, palabras = [], 0.0, [], []
for k, i in enumerate(ids):
    d = json.load(open(os.path.join(T, i + ".json"), encoding="utf-8"))
    if k:
        g = AIRE_MISMA if sec(i) == sec(ids[k - 1]) else AIRE_OTRA
        lista.append(silencio(g)); t += g
    lista.append(os.path.join(T, i + ".wav"))
    bloques.append({"id": i, "inicio": round(t, 3), "fin": round(t + d["dur"], 3)})
    for w in d["palabras"]:
        palabras.append({"b": i, "w": w["w"], "t0": round(t + w["t0"], 3), "t1": round(t + w["t1"], 3)})
    t += d["dur"]

txt = os.path.join(T, "lista.txt")
open(txt, "w").write("".join("file '%s'\n" % p.replace("\\", "/") for p in lista))
out = os.path.join(AQUI, "narracion_v1.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", out], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-b:a", "192k", os.path.join(AQUI, "narracion_v1.mp3")], check=True)
json.dump({"duracion": round(t, 3), "bloques": bloques, "palabras": palabras}, open(os.path.join(AQUI, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("duracion total %.1f s (%d:%02d)" % (t, t // 60, t % 60))
for b in bloques:
    print(b["id"], b["inicio"], b["fin"])
