# OneScreen Academy — instrucciones para Claude

Este repo es el proceso completo para hacer **videos de curso de OneScreen Academy** (cursos de software, 100 % motion graphics con HyperFrames) a partir de un video crudo de captura de pantalla.

## Antes de cualquier tarea (primera vez en esta máquina)

1. Mira si existe el archivo `.env` en la raíz **y** si `npx --no-install hyperframes@0.8.112 --version` responde. Si falta alguno: **dile a la persona que corra `python setup.py` en su propia terminal** (en Claude Code, escribiendo `! python setup.py`). El instalador:
   - verifica Python, Node.js y ffmpeg y dice cómo instalar lo que falte,
   - instala HyperFrames 0.8.112 y su Chrome de render, y (si la persona acepta) los skills de HyperFrames,
   - pide la API key de ElevenLabs con la entrada oculta, la prueba, deja elegir la voz de la cuenta y guarda todo en `.env`.
2. **Nunca pidas la API key en el chat, ni la leas, imprimas o pegues en un archivo versionado.** Si la persona te la escribe en el chat, no la uses: pídele que corra `python setup.py` (y que la considere expuesta si el chat no es privado). `.env` está en `.gitignore`; no lo agregues a git.
3. `python setup.py --check` verifica sin tocar nada.

## Cómo se trabaja

- Reglas, flujo y estilo (fuente única): **`estudio-academy/CLAUDE.md`**.
- Puertas obligatorias en orden: skill **`academy-onescreen`** (`.claude/skills/academy-onescreen/SKILL.md`, prompts para subagentes en su carpeta `prompts/`).
- Módulo nuevo: `python estudio-academy/nuevo_modulo.py "<Curso>-M<N>"` → crea `cursos/<Curso>-M<N>/` (carpeta local, git la ignora; ahí van crudos, audio y renders). Entregas en `cursos/_entregas/`.
- Ejemplo aprobado (la vara de calidad): `estudio-academy/ejemplos/suprnotes-m1/`. Historial y lecciones de cada curso: `estudio-academy/memoria/`.
- Contexto adicional del proceso: `docs/PROCESO_ACADEMY_MOTION.md`.

## Siempre

- Claves solo en `.env` o variables de entorno. Jamás en código, briefs o commits.
- No subas crudos, audio, renders ni datos de clientes: `cursos/` está ignorado a propósito.
- La voz aprobada se congela y no se regenera sin permiso (cuesta caracteres de ElevenLabs).
- **Assets de marca:** `python traer_assets.py` (lo corre `setup.py`) baja de Drive a `assets-marca/` los logos de OneScreen (azul, blanco, negro, púrpura), los de los softwares (SuprNotes, Lessn, QuizWiz, Scrybe, Gurú, Orbit Blue), los vectores SVG (`Vectorizados/`) y el manual de marca PDF. Esa carpeta es la fuente de logos: úsala en P0b antes de pedir nada a nadie; `assets-marca/INDICE.md` lista lo disponible. Nunca inventes ni redibujes un logo. Git la ignora.
- Falta la fuente **Nevis** (licencia): sin ella «OneScreen» en texto cae a otra fuente; si la persona tiene `Nevis.ttf`, va en `estudio-academy/plantilla/video/assets/fonts/`.

## Voz (resumen; detalle en `estudio-academy/CLAUDE.md`, sección «Voz»)
Siempre ElevenLabs `eleven_v4` con la voz «Francisco - Estudio» (`ACADEMY_VOZ_ID` en `.env`), guion dirigido con etiquetas (`[warm]`, `[short pause]`…), marcas respeleadas en español y **términos en inglés escritos `{en:...}` para que se digan en inglés**, sin respelling ni énfasis.
