"""Crea el esqueleto de un módulo nuevo de OneScreen Academy en cursos/<nombre>/.
Uso:  python estudio-academy/nuevo_modulo.py "Odoo-M1"
Copia plantilla/ (voz, video, agentes), crea crudo/ y deja instrucciones. No sobrescribe nada existente."""
import os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("ACADEMY_CURSOS") or os.path.join(os.path.dirname(AQUI), "cursos")
if len(sys.argv) < 2:
    sys.exit('Uso: python nuevo_modulo.py "<Curso>-M<N>"   (ej. "Odoo-M1")')
destino = os.path.join(BASE, sys.argv[1])
if os.path.exists(destino):
    sys.exit("Ya existe: %s (no se sobrescribe)" % destino)
shutil.copytree(os.path.join(AQUI, "plantilla"), destino)
os.makedirs(os.path.join(destino, "crudo"))
os.makedirs(os.path.join(destino, "video", "compositions"))
os.makedirs(os.path.join(destino, "video", "renders"))
print("Módulo creado en", destino)
print("""Siguiente:
 1. Pon el video crudo en crudo\\ y transcríbelo (Scribe) -> crudo\\scribe.json
 2. Mide el software en vivo con Claude in Chrome (capturas en agentes\\ref_ui\\, logo oficial en video\\assets\\)
 3. Escribe guion_v1.md y pásalo a Cris para aprobar
 4. Edita voz\\bloques.py (marcas y pronunciaciones del software) y genera la voz
 5. Adapta video\\hacer_tiempos.py (lista de escenas) y video\\armar_maestro.py (THEMES por escena)
 Ver estudio-academy\\CLAUDE.md para el flujo completo y las reglas de estilo.""")
