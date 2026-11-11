#!/usr/bin/env python3
"""Descarga los assets de marca de OneScreen (logos, vectores, manual de marca) desde la carpeta compartida de Drive
a `assets-marca/` (git la ignora: los archivos no se redistribuyen desde el repo).
Uso:  python traer_assets.py            (baja lo que falte)
      python traer_assets.py --forzar   (vuelve a bajar todo)
La carpeta de Drive está compartida como «cualquier persona con el enlace»: no hace falta cuenta de Google."""
import os, shutil, subprocess, sys

DRIVE_ID = "1YnV1UcG8DHPNIGGVmvCY1rkn_gjWvviC"
DRIVE_URL = "https://drive.google.com/drive/folders/" + DRIVE_ID
AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "assets-marca")


def asegurar_gdown():
    try:
        import gdown  # noqa: F401
    except ImportError:
        print("Instalando gdown (para bajar la carpeta de Drive)...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "gdown"])
        if r.returncode != 0:
            sys.exit("No pude instalar gdown. Prueba: pip install gdown")


def indice(archivos):
    l = ["# Assets de marca (bajados de Drive; no se suben a git)", "", "Origen: " + DRIVE_URL, ""]
    for a in sorted(archivos):
        l.append("- `%s`" % os.path.relpath(a, DEST).replace(os.sep, "/"))
    l += ["", "Lo que no esté aquí hay que pedirlo a Cristian al inicio del curso (no se inventa ni se redibuja un logo)."]
    open(os.path.join(DEST, "INDICE.md"), "w", encoding="utf-8").write("\n".join(l) + "\n")


def main():
    forzar = "--forzar" in sys.argv
    if os.path.isdir(DEST) and not forzar and len([f for _, _, fs in os.walk(DEST) for f in fs]) > 5:
        print("assets-marca/ ya existe (usa --forzar para volver a bajar).")
        return 0
    asegurar_gdown()
    import gdown
    if forzar and os.path.isdir(DEST): shutil.rmtree(DEST)
    try:
        r = gdown.download_folder(id=DRIVE_ID, output=DEST, quiet=True, use_cookies=False)
    except Exception as e:
        print("No se pudo bajar la carpeta de Drive: %s" % e)
        print("Bájala a mano desde %s y descomprímela en assets-marca/" % DRIVE_URL)
        return 1
    archivos = [f.path if hasattr(f, "path") else f for f in (r or [])] if r else []
    if not archivos:
        archivos = [os.path.join(d, f) for d, _, fs in os.walk(DEST) for f in fs]
    indice([a for a in archivos if os.path.isfile(a)])
    print("Listo: %d archivos en %s" % (len(archivos), DEST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
