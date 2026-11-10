import re, glob
def split_top(s):
    out,d,cur=[],0,""
    for ch in s:
        if ch=="(": d+=1
        if ch==")": d-=1
        if ch=="," and d==0: out.append(cur); cur=""
        else: cur+=ch
    out.append(cur); return out
LAY=re.compile(r"^(\s*)(-?\d+)(?:px)?\s+(-?\d+)(?:px)?\s+(\d+)px(\s+-?\d+px)?\s+rgba?\(([^)]*)\)\s*$")
def layer(l):
    if l.strip().startswith("inset"): return l
    m=LAY.match(l)
    if not m: return l
    sp,x,y,b,s,col=m.groups(); x,y,b=int(x),int(y),int(b)
    if y==0 and x==0: return l
    parts=[p.strip() for p in col.split(",")]
    a=float(parts[3]) if len(parts)==4 else 1.0
    a=round(min(a,.5)*0.55,2)
    y=min(y,16); b=min(b,34); x=max(min(x,0),0)
    return "%s%dpx %dpx %dpx rgba(0,0,0,%s)"%(sp or " ",x,y,b,a)
def fix(v): return ",".join(layer(x) for x in split_top(v))
for p in glob.glob("compositions/*.html")+["assets/academy.css"]:
    if "s11-registro" in p: continue
    s=open(p,encoding="utf-8").read(); o=s
    s=re.sub(r"((?:box|text)-shadow:\s*)([^;}\"]+)",lambda m:m.group(1)+fix(m.group(2)),s)
    s=re.sub(r"((?:box|text)Shadow\s*[:=]\s*[\"'])([^\"']+)",lambda m:m.group(1)+fix(m.group(2)),s)
    s=re.sub(r"drop-shadow\(\s*(-?\d+)(?:px)?\s+(-?\d+)(?:px)?\s+(\d+)px\s+rgba?\(([^)]*)\)\)",
             lambda m:"drop-shadow(0 %dpx %dpx rgba(0,0,0,.3))"%(min(abs(int(m.group(2))),8),min(int(m.group(3)),14)) if int(m.group(2))!=0 else m.group(0),s)
    if s!=o: open(p,"w",encoding="utf-8").write(s); print("ok",p)
