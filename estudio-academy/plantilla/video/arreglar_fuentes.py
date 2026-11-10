"""Asegura que cada sub-composicion declare sus @font-face dentro del <template> (lo exige el lint de HyperFrames)."""
import glob, re, os
FF = ('  @font-face { font-family: "Rubik"; src: url("assets/fonts/Rubik-Variable.ttf") format("truetype"); font-weight: 300 900; font-display: block; }\n'
      '  @font-face { font-family: "Manrope"; src: url("assets/fonts/Manrope-variable-latin.woff2") format("woff2"); font-weight: 200 800; font-display: block; }\n'
      '  @font-face { font-family: "Nevis"; src: url("assets/fonts/Nevis.ttf") format("truetype"); font-weight: 700; font-display: block; }\n')
for p in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "compositions", "s[0-9][0-9]*.html")):
    s = open(p, encoding="utf-8").read()
    if "@font-face" in s:
        print("ya tiene", os.path.basename(p)); continue
    s2 = re.sub(r"(<template>\s*<style>\n?)", lambda m: m.group(1) + FF, s, count=1)
    if s2 == s: print("sin <style> tras template:", os.path.basename(p)); continue
    open(p, "w", encoding="utf-8").write(s2); print("arreglado", os.path.basename(p))
