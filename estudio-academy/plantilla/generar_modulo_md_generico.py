"""Genera MODULO_<nombre>.md (encargo por escena para los agentes) de CUALQUIER módulo de Academy.
Uso: python generar_modulo_md_generico.py "cursos/<Curso>-M<N>"
Lee video/escenas_def.json (cada escena con id, nombre, bloques, tema y los campos «tipo» = motion|ui e «idea» = metáfora visual)
y voz/bloques.py (BLOQUES). Escribe <modulo>/MODULO.md. Un agente por escena: cada escena sale como su propio encargo."""
import json, os, re, sys, importlib.util

mod = sys.argv[1].replace("\\", "/").rstrip("/")
d = json.load(open(mod + "/video/escenas_def.json", encoding="utf-8"))
sp = importlib.util.spec_from_file_location("bl", mod + "/voz/bloques.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
txt = dict(m.BLOQUES)
nombre = os.path.basename(mod)
out = ["# %s · %s\n" % (nombre, d.get("titulo", "")),
       "Proyecto: `%s/video`. Narración: `%s/voz/ritmo/narracion_v2.wav`. Referencias de interfaz viva: `%s/agentes/ref_ui/` (documentos UI_*.md y capturas). Inventario de assets/logos: `%s/video/assets/INVENTARIO.md`. **Toda la sincronía sale de `AC.cue`/`AC.cueEnd`/`AC.blockStart`, nunca de segundos escritos a mano.** UN agente por escena.\n" % (mod, mod, mod, mod),
       "## Escenas\n"]
for e in d["escenas"]:
    cid = "%s-%s" % (e["id"], e["nombre"])
    out.append("### %s  (tipo: %s)\nArchivo: `compositions/%s.html`, composition-id `%s`. Bloques de voz: %s. Fondo del maestro (tu escena es transparente sobre él): centro %s, medio %s, borde %s, textura %s.\n\n**Narración (limpia):**\n" % (cid, e.get("tipo", "motion"), cid, cid, ", ".join(e["bloques"]), *e["tema"]))
    for b in e["bloques"]:
        lim = re.sub(r"\[[^\]]*\]\s*", "", txt[b]); lim = re.sub(r"\{([^}]*)\}", r"\1", lim); lim = re.sub(r"\*([^*]+)\*", r"\1", lim)
        out.append("- `%s`: %s\n" % (b, lim))
    out.append("\n**Concepto / metáfora visual:** %s\n" % e.get("idea", "(definir antes de lanzar el agente)"))
open(mod + "/MODULO.md", "w", encoding="utf-8").write("\n".join(out))
print("ok", mod + "/MODULO.md", len(d["escenas"]), "escenas")
