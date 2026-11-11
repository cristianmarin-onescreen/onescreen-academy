---
name: academy-onescreen
description: Hace videos de OneScreen Academy (cursos de software como SuprNotes, Lessn, QuizWiz, Odoo) a partir de un crudo de captura de pantalla - escribe el guion, lo voza, lanza subagentes que construyen cada escena de motion y un revisor que exige la misma calidad de los módulos aprobados (SuprNotes M1) - 100 % motion graphics, sin Premiere. Úsalo siempre que Cris pase un crudo o pida un módulo, curso, video de Academy, una corrección de uno ya hecho o el siguiente módulo de un curso; también si menciona SuprNotes, Lessn, QuizWiz o "el proceso de Academy", aunque no diga la palabra skill. No uses estudio-video ni el flujo de 16 pasos.
---

# Videos OneScreen Academy

Fuente única de reglas: **`estudio-academy/CLAUDE.md`** (en el PC: `estudio-academy`). Plantilla, briefs y ejemplo aprobado (SuprNotes M1) viven ahí. Módulos en `cursos\<Curso>-M<N>\` (nunca C:), creados con `python estudio-academy/nuevo_modulo.py "<Curso>-M<N>"`. Entregable: **MP4 1080p** en `cursos\_entregas\`. Sin Premiere/planos/S-Log3.

Prompts de subagentes listos (pega y rellena `<>`): `prompts/guion.md`, `prompts/escena.md`, `prompts/revisor.md` (en esta misma carpeta del skill).

**Modo de trabajo:** tú orquestas; el trabajo pesado lo hacen subagentes (`Agent`, general-purpose). Lanza en **un solo mensaje** todos los agentes independientes de una ola. No hagas escenas tú mismo salvo arreglos puntuales. Cris pidió que el guion y los motions salgan **siempre** al nivel de SuprNotes M1: eso se garantiza con las puertas, no con confianza.

## Puertas (en orden)

**P0 · Preparar.** Lee `estudio-academy/CLAUDE.md`. Mira un fotograma de s01/s05/s12 del ejemplo (`ejemplos/suprnotes-m1/` o `_entregas/SuprNotes_M1_1080p.mp4`) para calibrar. Si el curso ya tiene módulos, reutiliza su marca/assets/brief de suplemento (Lessn: `BRIEF_ESCENAS_LESSN.md`).

**P0b · Assets: pedirlos AL INICIO, no a mitad de camino.** Primero mira `assets-marca/` (logos de OneScreen y de SuprNotes, Lessn, QuizWiz, Scrybe, Gurú; vectores; manual de marca; se baja con `python traer_assets.py`) y `assets-marca/INDICE.md`. Antes de P3, haz el inventario de lo que el video necesita y consigue lo que puedas de la plataforma web (P2): logo oficial (SVG/PNG del encabezado, favicon/ícono de app, wordmark), íconos reales de la interfaz, fuentes, colores de marca, capturas. Lo que NO logres sacar (logo en alta, manual de marca, ícono sin fondo, cuenta de prueba, acceso a una pantalla, datos de ejemplo, fuente tipográfica propia) lo pides a Cris **en un solo mensaje, al comienzo**, con la lista exacta de qué falta y por qué, y mientras tanto avanzas con lo demás (P1, guion). Nunca inventes ni redibujes un logo «aproximado»: espera el oficial o avisa. Deja el inventario en `video/assets/INVENTARIO.md` (asset, origen, estado).

**P1 · Crudo → texto.** `crudo_a_texto.py`. Mira las hojas de contacto: el crudo puede mostrar una interfaz vieja. **Modo sin crudo** (instructivos de una plataforma propia, p. ej. el Academy de Odoo): no hay P1; la plataforma viva es la única fuente y el guion se construye desde la exploración de P2 y lo que Cris explica en su pedido. En ese modo, la regla de layout de Cris manda sobre lo que la plataforma muestre (p. ej. recrear CENTRADO lo que está alineado a la izquierda).

**P2 · Medir la interfaz VIVA (subagente con Chrome).** Brief `BRIEF_UI_MEDIR_INTERFAZ.md` / `BRIEF_UI_LESSN.md`. Seguro: sesión de Cris, nunca contraseñas/cerrar sesión/pagar/borrar/pulsar «generar»; anota lo que cree en su cuenta. Sale: capturas, medidas, textos exactos, tokens, logo oficial y **mapa de diferencias crudo vs viva**, más la lista de assets que no se pudieron extraer (alimenta P0b). Lo vivo manda. Esto va ANTES del guion.

**P3 · Guion (subagente guionista, `prompts/guion.md`) + revisión.** El guion lo escribe un subagente con el estándar del guion aprobado de M1 (no copia el crudo, describe la app de hoy, ejemplos, narrador sin nombre, marcas de voz, idea de motion por bloque, `bloques.py` + `escenas_def.json`). Luego lanza **un segundo agente revisor de guion** con la lista de autocrítica del prompt (¿suena a persona?, ¿botones exactos?, ¿ejemplos?, ¿palabras distintivas para anclar animaciones?, ¿cierre con «qué viene»?) y devuelve correcciones; aplica y repite hasta que pase. **No esperes aprobación de Cris para seguir** (él pidió que el guion salga bien solo): al presentar el resultado final incluye el guion y los textos en que dudaste. Si Cris quiere aprobarlo antes, lo dice y se respeta.

**P4 · Voz.** `gen_voz.py` (eleven_v4, voz `ACADEMY_VOZ_ID`). Prueba una toma corta primero; si faltan créditos → voz provisional (`gen_provisional.py`) y se avisa. Voz aprobada = congelada en `voz/aprobada/`; correcciones solo con `--correccion ids` y permiso de Cris.

**P5 · Ritmo.** `ritmo.py` (pausa mínima 0,20 s; `EXTRA` donde haya insertos).

**P6 · Proyecto.** `preparar_video.sh "<carpeta_modulo>"` (copia el sistema, pone la narración y corre `hacer_tiempos.py` + `armar_maestro.py`; no pisa los assets de marca del curso en `video/assets`) → `mezclar_audio.py "<carpeta_modulo>"` (después, porque prepara pisa `narracion.wav`) → `armar_maestro.py`. Sincronía solo con `AC.cue`. Los scripts son genéricos (sirven para cualquier curso).

**P7 · Escenas con subagentes, `prompts/escena.md`.** `python generar_modulo_md_generico.py "<carpeta_modulo>"` produce `MODULO.md` con narración, tipo (motion|ui) y metáfora visual por escena (salen de `escenas_def.json`; el guionista debe llenar `tipo` e `idea`). **UN AGENTE POR ESCENA, sin excepciones** (así se hizo SuprNotes M1, la vara aprobada; con 2–3 escenas por agente la calidad baja). También cada inserto/subescena compleja (p. ej. s05a–e) es su propio agente. Todas las escenas se lanzan en paralelo (en lotes de ≤8 por mensaje si son muchas), motion primero y ui después si comparten assets. Cada prompt incluye el encargo pegado de `MODULO_<N>.md`, la **vara de calidad** (rutas a s01/s05/s11/s12 de M1 y a SuprNotes M4) y la autorrevisión obligatoria con ≥2 iteraciones. Cambios de guion a mitad: `SendMessage` al agente con texto y `tiempos.js` nuevos.

**P8 · Puerta de calidad de motion (obligatoria, no se salta).**
1. Ensambla el video completo y haz `npx --yes hyperframes@0.8.112 check .` (0 errores; `AC.cue: no se encontro` ≈ 0).
2. Render draft → 720p.
3. Lanza **revisor(es) de motion** (`prompts/revisor.md`, agente distinto a los constructores): calibra contra SuprNotes M1, mira ≥3 fotogramas por escena, puntúa 1–5 y lista defectos duros.
4. Toda escena `REHACER` vuelve a su subagente (o a uno nuevo) con las instrucciones concretas del revisor; re-renderiza y **vuelve a revisar**. Repite hasta que todas queden `APROBADA`. Máximo 3 vueltas por escena; si sigue fallando, dilo a Cris con el fotograma, no lo entregues como bueno.
5. Mira tú mismo una hoja de ≥24 fotogramas del video completo antes de enviar. Tras cualquier arreglo en lote, re-renderiza y mira de nuevo.

**P9 · Preview 720p a Cris → render final.** `render_final.sh "<carpeta_modulo>"` (1080p + preview 720p + copia a `_entregas`). Formatos extra, 4K o Drive solo si lo pide. Entrega con **link clicable**, no solo ruta.

**P10 · Registro.** Memoria del módulo (rutas, decisiones, pendientes); correcciones nuevas de Cris → sección «Correcciones de Cris» de `estudio-academy/CLAUDE.md`; actualiza la lista de módulos entregados.

## Reglas que nunca se rompen
- **NUNCA mencionar «Odoo» al cliente** (ni en voz, ni en texto en pantalla, ni logos de Odoo): se enseña OneScreen Academy; que esté montada en Odoo no se le dice. Aplica a guion, bloques.py, escenas y capturas. Si una pantalla recreada tiene marca de Odoo, se sustituye por la de OneScreen Academy. Chequeo obligatorio en P3 y P8: grep «odoo|odú» sobre guion, voz y compositions.
- **Gastar poco (cuesta plata):** cero pruebas innecesarias de voz o de agentes. Una sola generación de voz por módulo (la prueba corta solo si hay duda de créditos), una sola ronda de revisor por video con una hoja de contacto, y cada agente de escena hace como máximo 2 iteraciones salvo defecto duro. No lanzar agentes «de exploración» repetidos: reusar lo ya medido. Con voz aprobada no se regenera nada.
- Cris decide solo el preview final (y el guion si él lo pide). No le pidas nada más.
- Vidrio `blur(34px)`, fondo oscuro con viñeta y **distinto por escena**, corte directo, **cero neón**, sombras negras cortas, márgenes 160/120, ritmo calmado (1,0–1,6 s; textos quietos ≥1,2 s), motion que explica la voz.
- Rubik títulos / Manrope cuerpo; «OneScreen» con logo oficial o Nevis; logo del software = el oficial del sitio.
- Interfaz fiel con datos ficticios (Camila Rojas). Nunca crear cuentas reales ni gastar créditos del cliente al medir.
- Clave en `ELEVENLABS_API_KEY`, jamás en código. Odoo y datos de clientes no entran aquí.
