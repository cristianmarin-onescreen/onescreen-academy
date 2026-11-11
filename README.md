# OneScreen Academy · videos de curso con IA

Proceso abierto de OneScreen para producir **videos de cursos de software** a partir de un video crudo de captura de pantalla: Claude transcribe, escribe un guion mejor, lo voza (ElevenLabs), recrea la interfaz con fidelidad y la anima como motion graphics con [HyperFrames](https://github.com/heygen-com/hyperframes). Entrega MP4 1080p. Sin cámara, sin Premiere.

## Empezar (3 pasos)

```bash
git clone https://github.com/cristianmarin-onescreen/onescreen-academy.git
cd onescreen-academy
python setup.py
```

`setup.py` revisa Python, Node.js y ffmpeg; instala HyperFrames 0.8.112 y su Chrome de render; opcionalmente instala los skills de HyperFrames para Claude Code; y **te pide la API key de ElevenLabs** (entrada oculta) y la guarda solo en `.env`, que git ignora. Después abre la carpeta en [Claude Code](https://claude.com/claude-code) y pide, por ejemplo:

> Hazme el video de OneScreen Academy del módulo 1 del curso «Mi software». El crudo está en `C:\ruta\crudo.mp4`.

Claude sigue `CLAUDE.md` y el skill `academy-onescreen`.

## Qué necesitas
- Python 3.9+, Node.js 20+, ffmpeg (en la ruta del sistema).
- Una cuenta de ElevenLabs con API key (voz `eleven_v4` y transcripción Scribe). La clave te la comparte quien administra el proyecto por un canal seguro; **no la pegues en el chat de Claude**.
- Claude Code. Para medir la interfaz viva del software, la extensión Claude in Chrome (con tu sesión).

## Qué hay en el repo
| Ruta | Contenido |
|---|---|
| `CLAUDE.md` | Instrucciones de entrada para Claude (instalación, reglas) |
| `estudio-academy/CLAUDE.md` | Flujo completo y reglas de estilo (fuente única) |
| `.claude/skills/academy-onescreen/` | Skill con las puertas P0–P10 y los prompts de subagentes |
| `estudio-academy/plantilla/` | Plantilla de módulo: voz, ritmo, video, mezcla, briefs |
| `estudio-academy/ejemplos/suprnotes-m1/` | Módulo aprobado: las 17 escenas, guion y escenas.json |
| `estudio-academy/memoria/` | Lecciones de los cursos hechos (SuprNotes, Lessn, QuizWiz, LearningHub) |
| `docs/PROCESO_ACADEMY_MOTION.md` | Documento del proceso de motion |

Tus cursos viven en `cursos/` (ignorado por git).

## Notas
- Los logos y el manual de marca NO están en el repo: `setup.py` / `python traer_assets.py` los baja de la carpeta compartida de Drive a `assets-marca/`. La fuente **Nevis** falta (licencia). Ver `CLAUDE.md`.
- Hecho para el flujo de Cristian Marín y el equipo de OneScreen LATAM; los textos están en español.
