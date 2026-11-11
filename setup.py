#!/usr/bin/env python3
"""Instalador de OneScreen Academy: deja la máquina lista para hacer videos de curso.

Uso (en tu terminal, desde la raíz del repo):   python setup.py
Opciones:  --check        solo verifica, no instala ni pregunta nada
           --sin-skills   no instala los skills de HyperFrames en tus herramientas de IA

Qué hace:
  1. Verifica Python, Node.js y ffmpeg (y te dice cómo instalar lo que falte).
  2. Instala HyperFrames 0.8.112 (el motor de video) y su Chrome de render.
  3. Instala los skills de HyperFrames para Claude Code (te pregunta antes).
  4. Te pide la API key de ElevenLabs (se escribe oculta, no se ve) y la guarda SOLO en `.env`
     de esta carpeta (git la ignora). Prueba que funcione y te deja elegir la voz de tu cuenta.
La clave nunca se imprime, no va en el código y no se sube a ningún lado salvo a api.elevenlabs.io."""
import getpass, json, os, platform, shutil, subprocess, sys, urllib.error, urllib.request

HF = "hyperframes@0.8.112"
VOZ_OFICIAL = "LIeln6cQyrBADSs7jUXR"   # «Francisco - Estudio» (voz clonada de la cuenta de OneScreen; el ID solo sirve con esa cuenta)
AQUI = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(AQUI, ".env")
SOLO_VERIFICAR = "--check" in sys.argv
SIN_SKILLS = "--sin-skills" in sys.argv
SO = platform.system()
problemas = []


def ok(m): print("  [ok] " + m)
def mal(m, ayuda=""):
    print("  [!!] " + m + (("\n       " + ayuda) if ayuda else "")); problemas.append(m)
def titulo(m): print("\n== " + m)


def ejecutar(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pedir_si(pregunta, defecto=True):
    if SOLO_VERIFICAR or not sys.stdin.isatty(): return False
    r = input(pregunta + (" [S/n] " if defecto else " [s/N] ")).strip().lower()
    return defecto if not r else r.startswith(("s", "y"))


def leer_env():
    d = {}
    if os.path.isfile(ENV):
        for l in open(ENV, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#") and "=" in l:
                k, v = l.split("=", 1); d[k.strip()] = v.strip()
    return d


def guardar_env(d):
    with open(ENV, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Creado por setup.py. No lo subas a git ni lo compartas.\n")
        for k, v in d.items(): f.write("%s=%s\n" % (k, v))
    try: os.chmod(ENV, 0o600)
    except OSError: pass


def api(ruta, clave):
    req = urllib.request.Request("https://api.elevenlabs.io" + ruta, headers={"xi-api-key": clave, "User-Agent": "onescreen-academy-setup"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


# ---------------------------------------------------------------- 1. herramientas
titulo("1/4 Herramientas base")
if sys.version_info >= (3, 9): ok("Python %s" % platform.python_version())
else: mal("Python 3.9 o superior", "https://www.python.org/downloads/")

node = shutil.which("node")
npx = shutil.which("npx")
if node and npx:
    v = ejecutar([node, "-v"]).stdout.strip()
    try: mayor = int(v.lstrip("v").split(".")[0])
    except ValueError: mayor = 0
    if mayor >= 20: ok("Node.js " + v)
    else: mal("Node.js %s es muy viejo (se necesita 20 o superior)" % v, "https://nodejs.org (versión LTS)")
else:
    ayuda = {"Windows": "winget install OpenJS.NodeJS.LTS", "Darwin": "brew install node"}.get(SO, "https://nodejs.org (versión LTS)")
    mal("Node.js no está instalado", ayuda)

if shutil.which("ffmpeg") and shutil.which("ffprobe"): ok("ffmpeg y ffprobe")
else:
    ayuda = {"Windows": "winget install Gyan.FFmpeg   (luego abre una terminal nueva)", "Darwin": "brew install ffmpeg"}.get(SO, "sudo apt install ffmpeg")
    mal("ffmpeg no está instalado", ayuda)

if not (node and npx):
    print("\nInstala Node.js, abre una terminal NUEVA y vuelve a correr: python setup.py")
    sys.exit(1)

# ---------------------------------------------------------------- 2. HyperFrames
titulo("2/4 HyperFrames (motor de video)")
if SOLO_VERIFICAR:
    r = ejecutar([npx, "--no-install", HF, "--version"])
    ok("HyperFrames instalado: " + r.stdout.strip()) if r.returncode == 0 else mal("HyperFrames no está en caché (corre setup.py sin --check)")
else:
    print("  Descargando %s (la primera vez tarda un poco)..." % HF)
    r = ejecutar([npx, "--yes", HF, "--version"])
    if r.returncode == 0: ok("HyperFrames " + r.stdout.strip().splitlines()[-1])
    else: mal("No se pudo instalar HyperFrames", (r.stderr or r.stdout).strip()[-300:])
    print("  Verificando el Chrome de render...")
    r = ejecutar([npx, "--yes", HF, "browser", "ensure"])
    if r.returncode == 0: ok("Chrome de render listo")
    else: mal("No se pudo preparar el Chrome de render", (r.stderr or r.stdout).strip()[-300:])

# ---------------------------------------------------------------- 3. skills
titulo("3/4 Skills de HyperFrames para Claude Code")
if SIN_SKILLS or SOLO_VERIFICAR:
    print("  (omitido)")
elif pedir_si("  Instalar los skills de HyperFrames (hyperframes, animación, audio...)? Se agregan a tu configuración de IA (recomendado)"):
    r = subprocess.run([npx, "--yes", HF, "skills"])
    ok("Skills instalados") if r.returncode == 0 else mal("Los skills no se instalaron (puedes reintentar: npx %s skills)" % HF)
else:
    print("  Omitido. Cuando quieras: npx %s skills" % HF)

# ---------------------------------------------------------------- 4. ElevenLabs
titulo("4/4 ElevenLabs (voz y transcripción)")
env = leer_env()
clave = os.environ.get("ELEVENLABS_API_KEY") or env.get("ELEVENLABS_API_KEY", "")
if clave and not SOLO_VERIFICAR and sys.stdin.isatty() and "ELEVENLABS_API_KEY" in env:
    if not pedir_si("  Ya hay una API key guardada en .env. ¿Conservarla?"): clave = ""
if not clave and not SOLO_VERIFICAR:
    if not sys.stdin.isatty():
        mal("Falta la API key de ElevenLabs", "Corre `python setup.py` en tu propia terminal: te la pide oculta. No la pegues en el chat.")
    else:
        print("  Pega la API key de ElevenLabs (no se verá al escribir) y Enter.")
        print("  Si no la tienes, pídesela a quien te compartió este repo, por un canal seguro.")
        clave = getpass.getpass("  API key: ").strip()
if clave:
    try:
        info = api("/v1/user/subscription", clave)
        ok("Clave válida. Plan %s, %s de %s caracteres usados" % (info.get("tier", "?"), info.get("character_count", "?"), info.get("character_limit", "?")))
    except urllib.error.HTTPError as e:
        if e.code == 401 and "missing_permissions" in (e.read().decode("utf-8", "ignore")):
            ok("Clave aceptada (sin permiso para leer el plan; está bien)")
        else:
            mal("ElevenLabs rechazó la clave (HTTP %d). Revisa que esté completa." % e.code); clave = ""
    except Exception as e:
        mal("No se pudo contactar a ElevenLabs: %s" % e)
if clave and not SOLO_VERIFICAR:
    env["ELEVENLABS_API_KEY"] = clave
    voz = env.get("ACADEMY_VOZ_ID", "")
    try:
        voces = api("/v1/voices", clave).get("voices", [])
    except Exception:
        voces = []
    if not voz and any(v["voice_id"] == VOZ_OFICIAL for v in voces):
        voz = VOZ_OFICIAL; print("  Encontré la voz oficial de Academy en tu cuenta: Francisco - Estudio.")
    elif not voz and not voces:
        voz = VOZ_OFICIAL; print("  No pude listar voces; uso la voz oficial de Academy (Francisco - Estudio).")
    elif not voz:
        print("  La voz oficial de Academy (Francisco - Estudio) NO está en esta cuenta: elige otra o pide la cuenta correcta.")
    if voces and not (voz and any(v["voice_id"] == voz for v in voces)) and sys.stdin.isatty():
        propias = [v for v in voces if v.get("category") in ("cloned", "professional", "generated")] or voces
        print("\n  Voces de tu cuenta (elige la del curso; las clonadas van primero):")
        for i, v in enumerate(propias[:20], 1):
            print("   %2d. %s  (%s)" % (i, v["name"], v.get("category", "")))
        n = input("  Número de la voz [1]: ").strip() or "1"
        try: voz = propias[int(n) - 1]["voice_id"]
        except (ValueError, IndexError): voz = propias[0]["voice_id"]
    elif not voces and sys.stdin.isatty() and not voz:
        voz = input("  No pude listar voces. Pega el ID de la voz (o Enter para saltar): ").strip()
    if voz: env["ACADEMY_VOZ_ID"] = voz; ok("Voz elegida: " + voz)
    else: mal("No hay voz elegida (ACADEMY_VOZ_ID); se pedirá antes de generar audio")
    guardar_env(env); ok("Guardado en .env (ignorado por git)")
elif not clave and SOLO_VERIFICAR:
    mal("No hay API key de ElevenLabs (corre python setup.py)")

# ---------------------------------------------------------------- extras
if not SOLO_VERIFICAR:
    titulo("Extras")
    if pedir_si("  Instalar respaldos locales (edge-tts y faster-whisper) por si se acaban los créditos de ElevenLabs? (pesado)", False):
        r = subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts", "faster-whisper"])
        ok("Respaldos instalados") if r.returncode == 0 else mal("No se instalaron los respaldos (opcional)")
    else:
        print("  Omitido (opcional: pip install edge-tts faster-whisper).")
    print("\n  Diagnóstico de HyperFrames (los avisos de Docker, whisper-cpp, Kokoro y MusicGen son opcionales):")
    r = ejecutar([npx, "--yes", HF, "doctor"])
    print("\n".join("   " + l for l in (r.stdout or "").splitlines()))
    print("\n  Manual (una vez): instala la extensión «Claude in Chrome» y entra a tu sesión del software que vas a explicar.")

# ---------------------------------------------------------------- fin
print("\n" + "=" * 60)
if problemas:
    print("Quedaron pendientes:"); [print("  - " + p) for p in problemas]
    print("Arregla lo anterior y vuelve a correr: python setup.py")
    sys.exit(1)
print("Todo listo. Abre esta carpeta en Claude Code y pídele, por ejemplo:")
print('  "Hazme un video de OneScreen Academy para el módulo 1 del curso X; este es el crudo: <ruta>"')
print("Claude seguirá CLAUDE.md y el skill academy-onescreen.")
