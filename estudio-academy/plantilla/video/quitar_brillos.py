import re, glob, os
SOFT = "rgba(255,255,255,.07)"
def split_top(s):
    out, d, cur = [], 0, ""
    for ch in s:
        if ch == "(": d += 1
        if ch == ")": d -= 1
        if ch == "," and d == 0: out.append(cur); cur = ""
        else: cur += ch
    out.append(cur); return out
def glow(layer):
    l = layer.strip()
    if l.startswith("inset"): return layer
    m = re.match(r"^(-?0|0px)\s+(-?0|0px)\s+(\d+)px(\s+\d+px)?\s+(.+)$", l)
    if not m: return layer
    blur = min(int(m.group(3)), 60); spread = m.group(4) or ""
    if spread: spread = " " + str(min(int(spread.strip()[:-2]), 6)) + "px"
    return " 0 0 %dpx%s %s" % (blur, spread, SOFT)
def fix_value(v): return ",".join(glow(x) for x in split_top(v))
n = 0
for p in glob.glob("compositions/*.html"):
    s = open(p, encoding="utf-8").read(); o = s
    # box-shadow / text-shadow en CSS
    s = re.sub(r"((?:box|text)-shadow:\s*)([^;}\"]+)", lambda m: m.group(1) + fix_value(m.group(2)), s)
    # boxShadow / textShadow en JS (cadena entre comillas)
    s = re.sub(r"((?:box|text)Shadow\s*[:=]\s*[\"'])([^\"']+)", lambda m: m.group(1) + fix_value(m.group(2)), s)
    # drop-shadow(...) con 0 0
    s = re.sub(r"drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+(\d+)px\s+[^)]*(?:\([^)]*\))?[^)]*\)",
               lambda m: "drop-shadow(0 0 %dpx %s)" % (min(int(m.group(1)), 24), SOFT), s)
    if s != o: n += 1; open(p, "w", encoding="utf-8").write(s)
# borde cian resaltado -> blanco suave
for p in ["compositions/s02-problema.html"]:
    s = open(p, encoding="utf-8").read()
    s = s.replace('borderColor: "rgba(125,240,255,.9)"', 'borderColor: "rgba(255,255,255,.8)"').replace("border: 3px solid #7df0ff", "border: 3px solid rgba(255,255,255,.8)")
    open(p, "w", encoding="utf-8").write(s)
print("archivos cambiados:", n)
