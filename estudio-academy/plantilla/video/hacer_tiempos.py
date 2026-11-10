"""Genera assets/tiempos.js y escenas.json desde ../voz/ritmo/tiempos.json y escenas_def.json.
escenas_def.json = {"escenas":[{"id":"s01","nombre":"apertura","bloques":["b01"],"tema":["#c0","#c1","#c2","dots44"]}, ...],
                    "insertos":[{"id":"s05a-resumen","bloque":"b05a","palabra":"versión","fin_extra":1.7}]}   (insertos opcional)"""
import json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(AQUI, "..", "voz", "ritmo", "tiempos.json"), encoding="utf-8"))
D = json.load(open(os.path.join(AQUI, "escenas_def.json"), encoding="utf-8"))
import importlib.util
_sp = importlib.util.spec_from_file_location("bloques_guion", os.path.join(AQUI, "..", "voz", "bloques.py")); _bm = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_bm)
_nrm = lambda s: re.sub(r"[^a-z0-9ñ]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())
_g = {i: [x for x in (_nrm(t) for t in _bm.limpio(txt).split()) if x] for i, txt in _bm.BLOQUES}
for b in T["bloques"]: b["g"] = _g.get(b["id"], [])
bl = {b["id"]: b for b in T["bloques"]}
norm = lambda s: re.sub(r"[^a-z0-9ñ]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())
ESC = D["escenas"]
tot = round(T["duracion"] + 0.8, 2)
esc = []
for k, e in enumerate(ESC):
    ini = bl[e["bloques"][0]]["inicio"] if k else 0.0
    fin = bl[ESC[k + 1]["bloques"][0]]["inicio"] if k + 1 < len(ESC) else tot
    esc.append({"id": e["id"], "nombre": e["nombre"], "bloques": e["bloques"], "tema": e.get("tema"), "inicio": round(ini, 3), "fin": round(fin, 3), "dur": round(fin - ini, 3)})
ins = []
for i in D.get("insertos", []):
    b = i["bloque"]
    t0 = next((x["t0"] for x in T["palabras"] if x["b"] == b and norm(x["w"]) == norm(i["palabra"])), bl[b]["inicio"] + 2.0)
    ini = round(t0 - 0.12, 3); fin = round(bl[b]["fin"] + i.get("fin_extra", 1.7), 3)
    ins.append({"id": i["id"], "bloque": b, "palabra": i["palabra"], "inicio": ini, "fin": fin, "dur": round(fin - ini, 3)})
data = {"duracion": tot, "bloques": T["bloques"], "palabras": T["palabras"], "escenas": esc, "insertos": ins}
os.makedirs(os.path.join(AQUI, "assets"), exist_ok=True)
open(os.path.join(AQUI, "assets", "tiempos.js"), "w", encoding="utf-8").write("window.AC_T = " + json.dumps(data, ensure_ascii=False) + ";\n")
json.dump({"titulo": D.get("titulo", "SuprNotes"), "escenas": esc, "insertos": ins}, open(os.path.join(AQUI, "escenas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("duracion %.1f s (%d:%02d)" % (tot, tot // 60, tot % 60))
for e in esc: print(e["id"], e["nombre"], e["inicio"], "->", e["fin"], "(%.1f s)" % e["dur"])
for i in ins: print("inserto", i["id"], "%.2f -> %.2f" % (i["inicio"], i["fin"]), "corta en", i["palabra"])
