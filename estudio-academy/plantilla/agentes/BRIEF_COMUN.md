# Brief común · insertos de motion del video «SuprNotes · Módulo 1» (OneScreen Academy)

## Qué es esto
Un video de curso (1920×1080, 30 fps) explica SuprNotes con una voz en off ya grabada y aprobada. La escena 5 muestra cinco tarjetas («salidas»): Resumen, Tarjetas, Cuestionario, Guía de repaso, Chat con IA. Cuando la voz explica cada una, el video **corta** a un **inserto** de motion graphics (tu trabajo) que ilustra esa salida, y al terminar **corta de vuelta** a la escena de tarjetas. Tú construyes UN inserto.

## Lo que Cris pidió (no negociable)
- Motion **bien imaginativo**, nada genérico. Es una escena de curso: debe **explicar** (que se entienda qué es y para qué sirve la salida) y verse increíble.
- Lenguaje visual del módulo: fondo azul muy oscuro con viñeta, **tarjetas de vidrio muy desenfocadas** (`backdrop-filter: blur(34px)`), luz cian/azul, paquetes de luz, tipografía Rubik (títulos) y Manrope (cuerpo). Ya está en `assets/academy.css` (clases `.ac-glass`, `.ac-title`, `.ac-lbl`, `.ac-sub`, `.ac-em`, `.ac-core`, `.ac-pk`, `.ac-links`). Cada inserto lleva además el **color de acento de su salida** (te lo da tu encargo) para distinguirse del resto.
- **Márgenes de seguridad: nada a menos de 160 px de los lados ni de 120 px arriba/abajo** (texto, tarjetas, íconos; incluye zooms y acercamientos de cámara: el contenido no puede llegar al borde en ningún cuadro, salvo fondos decorativos).
- Sin barridos/telón de transición: el inserto entra y sale por **corte directo** (sin fade de salida; el último cuadro debe verse limpio y completo).
- Todo texto en español, la marca se escribe «SuprNotes». Sin cajas «píldora» baratas ni capturas falsas de software ajeno. Datos de ejemplo inventados e inocuos (el ejemplo del módulo: una clase de biología sobre depredadores; términos como ecosistema, especie en peligro, conservación, depredador).
- Cada gráfico arranca **en la palabra que lo nombra** (la voz manda). Nada aparece antes de decirse ni se queda vacío esperando.
- Animación con intención: eases `power3/power4/back.out/expo` y `power2.inOut`; sin parpadeos ni «idle wobble» sin causa en la voz. Se vale 3D (perspective, rotateX/Y), máscaras, trazos que se dibujan, conteos numéricos, partículas con semilla, desenfoque de foco, zoom con ease.

## Dónde trabajar (IMPORTANTE: no pisar a los demás)
1. Copia la carpeta del proyecto SIN `renders` a la tuya: `cursos\SuprNotes-M1\agentes\<tu-id>\` (copia `assets`, `compositions`, `armar_maestro.py`, `escenas.json`, `hyperframes.json`, `package.json`). Trabaja SOLO ahí.
2. Tu archivo: `compositions/<tu-id>.html` (ej. `s05a-resumen.html`).
3. Al terminar copia **únicamente** ese archivo a `cursos\SuprNotes-M1\video\compositions\`. No toques ningún otro archivo del proyecto original.
4. C: está casi lleno: todo en D:.

## Contrato técnico (HyperFrames 0.8.112)
- Plantilla funcional: `compositions/s05-cinco-salidas.html` (léela completa). Lee también las referencias `sub-compositions.md` y `determinism-rules.md` del skill `hyperframes-core`, y la skill `hyperframes-animation` si necesitas ideas de movimiento.
- Es una **sub-composición**: todo (style, markup, script) va dentro de `<template>`. Raíz: `<div id="<tu-id-sin-guiones>" class="ac-root" data-composition-id="<tu-id>" data-width="1920" data-height="1080">`; estila la raíz por id. Registra `window.__timelines["<tu-id>"] = tl` (timeline `paused:true`) al final.
- **Prefija todos los ids/clases propios** con tu id (p. ej. `s05a-`) para no chocar con otras escenas.
- **El inserto debe ser OPACO**: su primera capa es un fondo de cuadro completo (usa el degradado oscuro del módulo, p. ej. `radial-gradient(ellipse 78% 70% at 50% 46%, #1a47d0 0%, #0c2a96 34%, #061a66 62%, #020a2e 100%)` más una viñeta, y opcionalmente tu acento) que cubra por completo la escena que hay debajo.
- Determinismo: sin `Date.now`, `performance.now`, `Math.random` sin semilla (usa `AC.seeded(n)`), sin `repeat:-1`. Estados iniciales ocultos por **CSS**, no con `tl.set(...,0)`. No animes `display`/`visibility`/`autoAlpha` del propio clip.
- Sincronía: `AC.icue(tuId, bloque, palabra, nth)` devuelve el tiempo LOCAL (0 = inicio de tu inserto) en que se dice una palabra; `AC.insDur(tuId)` = duración total. Las palabras de cada bloque están en `assets/tiempos.js` (`AC_T.palabras`, con `b`, `w`, `t0`, `t1`, tiempos absolutos de la narración). Puedes leerlas con Python para planear. Otras ayudas en `assets/academy.js`: `AC.svg(icono, tam)`, `AC.ICON` (28 íconos de línea), `AC.link`, `AC.packet`, `AC.bez`, `AC.line`/`showLn`/`hideLn`, `AC.seeded`.
- Prueba: `python armar_maestro.py <tu-id>` (escribe `index.html` con solo tu inserto y su tramo de audio) → `npx --yes hyperframes@0.8.112 check` (debe quedar sin errores; arregla advertencias de layout/contraste razonables) → `npx --yes hyperframes@0.8.112 render -q draft -o renders/<tu-id>.mp4 --quiet`.
- **Revisa con los ojos**: saca al menos 6 fotogramas con ffmpeg (inicio, en cada palabra clave, final), júntalos en una hoja de contacto y míralos con la herramienta Read (imagen). Itera hasta que explique bien, se vea pulido, respete márgenes y no haya solapes ni texto cortado. Verifica también que el último cuadro sea limpio.

## Entrega (tu respuesta final, corta)
Ruta del archivo copiado, 3–5 líneas de qué ilustra y con qué recursos de motion, cómo quedó la sincronía (qué ocurre en qué palabra), qué verificaste (check + fotogramas) y cualquier duda pendiente. No pegues código.
