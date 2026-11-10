"""Clave y voz de ElevenLabs para Academy.
Lee ELEVENLABS_API_KEY (y ACADEMY_VOZ_ID) del entorno o del archivo .env en la raíz del repo (lo crea `python setup.py`).
La clave nunca se escribe en código ni se sube a git."""
import os


def _cargar_env():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        p = os.path.join(d, ".env")
        if os.path.isfile(p):
            for linea in open(p, encoding="utf-8"):
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    k, v = linea.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return
        d = os.path.dirname(d)


_cargar_env()


def get_key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        raise SystemExit("Falta la clave de ElevenLabs. Corre `python setup.py` en la raiz del repo.")
    return k
