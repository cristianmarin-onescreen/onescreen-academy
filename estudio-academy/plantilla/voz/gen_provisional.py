"""VOZ PROVISIONAL (solo cuando se agotan los creditos de ElevenLabs). Genera las tomas con edge-tts (es-CO) en aprobada/tomas
para poder construir y sincronizar todo el video; luego se cambia por la voz real (ver PROVISIONAL.txt).
Uso: python gen_provisional.py     (clave ELEVENLABS_API_KEY solo para los tiempos por palabra con Scribe)"""
import asyncio, json, os, subprocess, sys, time
import urllib.request
import edge_tts
from bloques import BLOQUES, limpio

from clave import get_key
KEY = get_key()
AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "aprobada", "tomas"); os.makedirs(DEST, exist_ok=True)
VOZ = os.environ.get("ACADEMY_VOZ_ID", "")
open(os.path.join(AQUI, "aprobada", "PROVISIONAL.txt"), "w", encoding="utf-8").write(
    "Voz provisional (edge-tts %s) por falta de creditos de ElevenLabs. Para poner la real: mover esta carpeta a aprobada_provisional, "
    "python gen_voz.py (solo genera lo que falta), copiar tomas/ a aprobada/tomas/, python ritmo.py, hacer_tiempos.py y re-renderizar.\n" % VOZ)


def scribe_api(wav):
    b = "----hf%d" % int(time.time() * 1000); partes = []
    for k, v in (("model_id", "scribe_v1"), ("language_code", "spa"), ("timestamps_granularity", "word")):
        partes.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (b, k, v)).encode())
    partes.append(("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\nContent-Type: audio/wav\r\n\r\n" % b).encode() + open(wav, "rb").read() + b"\r\n")
    partes.append(("--%s--\r\n" % b).encode())
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=b"".join(partes), headers={"xi-api-key": KEY, "Content-Type": "multipart/form-data; boundary=" + b})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())


def scribe(wav):
    try: return scribe_api(wav)
    except Exception as e:
        print('  Scribe no disponible (%s): transcripcion local' % getattr(e,'code',e), flush=True)
        from stt_local import scribe_local
        return scribe_local(wav)


async def main():
    for bid, t in BLOQUES:
        wav = os.path.join(DEST, bid + ".wav")
        if os.path.exists(wav): print(bid, "ya existe"); continue
        txt = limpio(t).replace("suprnotes punto ai", "Supr Nouts punto a i").replace("supernotes arroba", "Supr Nouts arroba").replace("SuprNotes", "Supr Nouts").replace("MP4", "eme pe cuatro").replace("MKV", "eme ka ve").replace("WebM", "web eme").replace("AVI", "a ve i").replace("PDF", "pe de efe")
        mp3 = os.path.join(DEST, bid + ".mp3")
        await edge_tts.Communicate(txt, VOZ, rate="-4%").save(mp3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", "48000", wav], check=True)
        sc = scribe(wav)
        pal = [{"w": w["text"], "t0": w["start"], "t1": w["end"]} for w in sc.get("words", []) if w.get("type") == "word"]
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode().strip())
        json.dump({"id": bid, "dur": dur, "texto": sc.get("text", ""), "palabras": pal}, open(os.path.join(DEST, bid + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
        print(bid, "%.1f s" % dur, flush=True)
asyncio.run(main())
