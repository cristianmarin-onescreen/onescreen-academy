"""Mezcla de audio de un módulo de Academy: voz + música de curso (bajita, con ducking) + «soniditos» suaves al cambiar de escena.
Uso:  python mezclar_audio.py "cursos/SuprNotes-M2" [carpeta_video=video]
Entrada : voz/ritmo/narracion_v2.wav, <video>/escenas.json, cursos/musica/{musica_curso_a.mp3, sfx_swish.mp3}
Salida  : <video>/assets/narracion.wav (mezcla; la voz sola queda en <video>/assets/narracion_voz.wav)
Reglas de Cris (5-nov-2026): música de curso para que no sea aburrido, soniditos pasito, nada exagerado, que no distraigan."""
import json, os, re, subprocess, sys, shutil

mod = sys.argv[1].rstrip("/\\"); vid = sys.argv[2] if len(sys.argv) > 2 else "video"
MUS = os.path.join(mod, "musica")
V = os.path.join(mod, vid); A = os.path.join(V, "assets")
voz_src = os.path.join(mod, "voz", "ritmo", "narracion_v2.wav")
voz_copy = os.path.join(A, "narracion_voz.wav")
if (not os.path.exists(voz_copy)) or os.path.getmtime(voz_src) > os.path.getmtime(voz_copy): shutil.copy(voz_src, voz_copy)   # la voz sola se refresca si la narración con ritmo es más nueva (bug 6-nov: quedaba la voz provisional)
esc = json.load(open(os.path.join(V, "escenas.json"), encoding="utf-8"))["escenas"]
dur = esc[-1]["fin"]
tmp = os.path.join(A, "_mix"); os.makedirs(tmp, exist_ok=True)


def lufs(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])


v_lufs = lufs(voz_copy)
V_OBJ = -18.0     # nivel de la voz (igual que los videos anteriores); la voz nueva sale mas baja y se sube aqui
g_v = V_OBJ - v_lufs
MUS_REL, SFX_REL = -13.0, -19.0      # LU respecto a la voz (música ~13 LU debajo; soniditos ~19 debajo)
# 1) música en bucle con fundido cruzado hasta cubrir la duración
src = os.path.join(MUS, "musica_curso_a.mp3")
mdur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode().strip())
XF = 4.0
n = 1
while mdur * n - XF * (n - 1) < dur + 6: n += 1
ins = []; fc = ""
for k in range(n): ins += ["-i", src]
chain = "[0:a]"
for k in range(1, n):
    chain += "[%d:a]acrossfade=d=%.1f:c1=tri:c2=tri" % (k, XF) + ("[x%d];[x%d]" % (k, k) if k < n - 1 else "[loop]")
    if k < n - 1: pass
if n == 1: fc = "[0:a]anull[loop]"
else:
    fc = "[0:a][1:a]acrossfade=d=%.1f:c1=tri:c2=tri[x1]" % XF
    for k in range(2, n): fc += ";[x%d][%d:a]acrossfade=d=%.1f:c1=tri:c2=tri[x%d]" % (k - 1, k, XF, k)
    fc += ";[x%d]anull[loop]" % (n - 1)
loop = os.path.join(tmp, "musica_loop.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[loop]", "-t", "%.2f" % (dur + 0.5), "-ac", "2", "-ar", "48000", loop], check=True)
# 2) sonidos suaves al inicio de cada escena (salvo la primera): lista de entradas con retardo
sfx = os.path.join(MUS, "sfx_swish.mp3")
sfx_in = []; sfx_fc = []; labels = []
for k, e in enumerate(esc[1:]):
    sfx_in += ["-i", sfx]
    ms = int(max(0, e["inicio"] - 0.25) * 1000)
    sfx_fc.append("[%d:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=%d|%d[s%d]" % (k, ms, ms, k)); labels.append("[s%d]" % k)
sfx_graph = ";".join(sfx_fc) + ";" + "".join(labels) + "amix=inputs=%d:normalize=0:duration=longest[sfxall]" % len(labels)
sfx_wav = os.path.join(tmp, "sfx_all.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + sfx_in + ["-filter_complex", sfx_graph, "-map", "[sfxall]", "-t", "%.2f" % dur, "-ac", "2", "-ar", "48000", sfx_wav], check=True)
m_l, s_l = lufs(loop), lufs(sfx_wav)
g_m = V_OBJ + MUS_REL - m_l; g_s = V_OBJ + SFX_REL - s_l
# 3) mezcla: voz + música (con ducking por la voz y fundidos) + soniditos; limitador final
filt = (
    "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=%.2fdB,apad=whole_dur=%.2f,asplit=2[v][vk];"
    "[1:a]volume=%.2fdB,afade=t=in:st=0:d=3,afade=t=out:st=%.2f:d=4[m];"
    "[m][vk]sidechaincompress=threshold=0.03:ratio=4:attack=60:release=700:makeup=1[md];"
    "[2:a]volume=%.2fdB[s];"
    "[v][md][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[out]"
) % (g_v, dur, g_m, dur - 4, g_s)
out = os.path.join(A, "narracion.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voz_copy, "-i", loop, "-i", sfx_wav, "-filter_complex", filt, "-map", "[out]", "-t", "%.2f" % dur, "-ar", "48000", out], check=True)
print("voz %.1f LUFS | musica %+.1f dB | sfx %+.1f dB | mezcla %.1f LUFS | %.1f s" % (v_lufs, g_m, g_s, lufs(out), dur))
