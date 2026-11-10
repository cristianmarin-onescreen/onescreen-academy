# Proceso Academy de motion graphics — para integrarlo al sistema de videos

Documento de traspaso. Describe **cómo funciona hoy** el proceso de OneScreen Academy (100 % motion graphics, sin planos grabados) y **qué partes se pueden reutilizar** en los videos comerciales. Fuente de reglas completas: `estudio-academy/CLAUDE.md` y skill `.claude/skills/academy-onescreen/SKILL.md`. Caso de referencia aprobado por Cris: **SuprNotes M1** (5-nov-2026, «me encanta»).

---

## 1. La idea en una frase

Cris pasa una fuente (un crudo de pantalla, o nada: solo la plataforma viva) → Claude escribe un **guion mejor**, lo voza **una sola vez**, mide la **interfaz real**, y **un subagente por escena** construye cada escena como motion graphics sincronizado a la voz por palabra → un **revisor distinto** exige la calidad de la vara aprobada → render MP4. Cris solo interviene al final (y en el guion si él lo pide).

Lo que hace que funcione no es el estilo visual: es **la estructura** (puertas en orden, sincronía por palabra, un agente por escena, revisor independiente, voz congelada). Eso es lo transferible.

---

## 2. Las 11 puertas (P0–P10)

| Puerta | Qué se hace | Salida |
|---|---|---|
| **P0 Preparar** | Leer reglas; mirar fotogramas de la vara aprobada para calibrar | — |
| **P0b Assets** | Inventario al INICIO: logo oficial, íconos, fuentes, colores, capturas. Lo que no se puede sacar se le pide a Cris **en un solo mensaje, con la lista exacta**. Nunca se redibuja un logo | `video/assets/INVENTARIO.md` |
| **P1 Crudo → texto** | ffmpeg saca audio + fotogramas + hojas de contacto; Scribe da transcripción con tiempos por palabra | `crudo/transcripcion.txt` |
| **P2 Medir lo vivo** | Subagente con Chrome (sesión de Cris, solo lectura) mide textos exactos, coordenadas, colores, íconos. **Lo vivo manda sobre el crudo** | capturas + mapa de diferencias crudo vs vivo |
| **P3 Guion** | Subagente guionista + **segundo agente revisor de guion** con lista de autocrítica; se repite hasta que pase | `bloques.py` + `escenas_def.json` |
| **P4 Voz** | Una generación por módulo; aprobada = **congelada** | `voz/aprobada/` |
| **P5 Ritmo** | Recorta silencios, genera tiempos por palabra | `narracion_v2.wav` + `tiempos.json` |
| **P6 Proyecto** | Copia el sistema, pone la narración, genera tiempos y maestro, mezcla música/SFX | proyecto HyperFrames |
| **P7 Escenas** | **UN agente por escena**, todos en paralelo | `compositions/sNN.html` |
| **P8 Puerta de calidad** | check + render draft + **revisor de motion distinto a los constructores**; REHACER vuelve al agente; máx. 3 vueltas | todas `APROBADA` |
| **P9 Entrega** | Cris revisa → render final 1080p | MP4 en `_entregas` |
| **P10 Registro** | Memoria del módulo; correcciones nuevas de Cris al CLAUDE.md | — |

---

## 3. Las piezas que lo hacen excelente (lo que hay que copiar)

### 3.1 Sincronía por palabra, nunca por segundos
Todas las animaciones se disparan con `AC.cue(escena, bloque, palabra)`, que devuelve el tiempo local de una palabra tomado de `tiempos.json` (transcripción con timestamps por palabra).
- **Ninguna escena lleva segundos escritos a mano.** Si cambia la voz, no se toca ninguna animación.
- `AC.cue` tolera transcripciones distintas (distancia de edición ≤ 2), busca en el guion del bloque y, si no encuentra la palabra, cae a un punto estimado. En el log del render, `AC.cue: no se encontro` debe quedar en ≈ 0.
- Las tarjetas, íconos e interruptores se encienden **solo cuando la voz los nombra**: ni antes, ni todos juntos.

### 3.2 Guion por bloques con marcas de voz
`voz/bloques.py`: el guion es una lista de bloques con marcas inline:
- `[tag]` = dirección de actuación
- `*palabra*` = énfasis (se pasa a MAYÚSCULA)
- `{Marca}` = pronunciación (diccionario `PRON`: SuprNotes → «Supr Nouts», Lessn → «Leson», Learning Hub en inglés)

`escenas_def.json` define cada escena: bloques, **tipo** (`motion` | `ui`), **idea** (metáfora visual) y **tema de fondo**. De ahí sale todo (`hacer_tiempos.py` → `tiempos.js` + `escenas.json`; `generar_modulo_md_generico.py` → `MODULO.md` con el encargo por escena).

### 3.3 Un agente por escena + brief con vara de calidad
Cada escena es su propio subagente, en su carpeta `agentes/<id>/`, copiando solo su `compositions/<id>.html`. El prompt incluye:
1. el encargo pegado del `MODULO.md` (narración + tipo + metáfora),
2. `BRIEF_COMUN` + `BRIEF_ESCENAS` (reglas de estilo y de motor),
3. rutas a escenas aprobadas como **vara** (s01 apertura, s05 hub con insertos, s11 interfaz recreada, s12 cierre),
4. autorrevisión obligatoria (≥2 iteraciones, máx. 2 salvo defecto duro).

**Lección medida:** con 2–3 escenas por agente la calidad bajó; con uno por escena se mantuvo. Los cambios de guion a mitad se mandan por `SendMessage` al agente (texto + `tiempos.js` nuevos). Si un agente se atasca (`stream watchdog`), relanzar con otro id/carpeta, no reutilizar.

### 3.4 Revisor independiente (la puerta que no se salta)
Un agente **distinto** a los constructores: calibra contra la vara, mira ≥3 fotogramas por escena, puntúa 1–5 y lista defectos duros. Cada escena sale `APROBADA` o `REHACER` con instrucciones concretas. Después, yo miro una hoja de ≥24 fotogramas del video completo. Tras cualquier arreglo en lote (regex), **re-renderizar y mirar de nuevo**: un arreglo parcial deja residuos.

### 3.5 Voz: una receta, una toma, congelada
- ElevenLabs `eleven_v4`, voz `ACADEMY_VOZ_ID`, stability .4 / similarity .75 / style .5, `language_code` es, clave en `ELEVENLABS_API_KEY` (nunca en código).
- **Voz aprobada = congelada** en `voz/aprobada/`. Correcciones solo `gen_voz.py --correccion ids` y con permiso de Cris.
- Si faltan créditos: voz provisional (`gen_provisional.py`, edge-tts) + tiempos con `stt_local.py` (faster-whisper), y se avisa con `PROVISIONAL.txt`.
- Si una pronunciación falla: 4–5 muestras cortas de **una** frase, Cris elige, se regeneran solo los bloques afectados.

### 3.6 Ritmo de audio
`ritmo.py`: silencios ≥ 0,22 s a −40 dB → pausa de **0,20 s (no bajar: se comen inicios de palabra suaves)**; aire 0,16 s misma idea / 0,80 s entre secciones; `EXTRA` alarga pausas donde hay insertos.

### 3.7 Mezcla
`mezclar_audio.py`: voz + música de curso (bucle con fundido cruzado, ~13 LU bajo la voz, ducking) + «swish» suave (~19 LU bajo la voz) al empezar cada escena. Medido: voz −18 LUFS, mezcla −17 LUFS, pico −2,7 dBFS. **Mezclar siempre después de `preparar_video`** (pisa `narracion.wav`).

### 3.8 Interfaz recreada con fidelidad
Medida en vivo, no inventada: se recrea a tamaño de viewport real, escalada dentro de una ventana de navegador de vidrio (3 puntos + dirección que se escribe). Animación: zoom suave, resto atenuado con blur, cursor con pulso de clic, campos que se llenan al decir su palabra, insignias de paso. Datos ficticios fijos por curso (Camila Rojas, camila.rojas@ejemplo.com). Resaltados medidos sobre el elemento real recreado.

---

## 4. Reglas de motion (el «look»)

- **Vidrio:** `backdrop-filter: blur(34px) saturate(1.5)`, borde blanco fino. Fondo **oscuro con viñeta**.
- **Fondo distinto por escena** (color + textura: puntos, diagonales, anillos, cruces, barrido, retícula); nunca casi negro. Corte **directo** entre escenas; el último cuadro queda completo y limpio.
- **Cero neón.** Brillo máximo: halo blanco al 7 %. Sombras solo negras, cortas y suaves (`0 8px 22px rgba(0,0,0,.2)`). Sin extrusión 3D en logos/texto.
- **Acentos variados** (azul, cian, verde azulado, coral, rosa), nunca un solo color.
- **Márgenes de seguridad** (1920×1080): ≥160 px lados, ≥120 px arriba/abajo, también con zoom final.
- **Ritmo calmado:** movimientos 1,0–1,6 s, eases suaves (`power2.inOut`, `expo.out`), un evento principal por ~1 s, textos clave quietos ≥ 1,2 s, respiro tras cada beat.
- **Motion que explica:** diagramas que representan lo que dice la voz, 3D de vidrio, trazos que se dibujan, conteos, partículas con semilla, máscaras. Explicar > decorar. Sin píldoras baratas ni MAYÚSCULAS tipo diapositiva.
- Tipografía: Rubik títulos, Manrope cuerpo; «OneScreen» con logo oficial o Nevis Bold; nunca «One Screen».
- Texto e íconos de una fila alineados en un eje; **cero desbordes** en ninguna fase; etiquetas flotantes ancladas a algo.

## 5. Reglas técnicas del motor (HyperFrames 0.8.112, GSAP 3.14.2)

- Una timeline GSAP **pausada** por composición; sub-composiciones en `<template>` con `window.__timelines[id]`.
- Sin `Math.random` (PRNG con semilla), sin `repeat:-1`.
- **Nunca** `tl.set(el,{visibility:"visible"})` (el elemento se fuga a escenas siguientes). En `fromTo` con opacidad inicial > 0 usar `immediateRender:false`.
- `pathLength` no se respeta en el render: para trazos que se dibujan usar `getTotalLength()`.
- `arreglar_fuentes.py` mete `@font-face` en cada composición (el lint lo exige).
- `npx --yes hyperframes@0.8.112 check .` recibe **solo la carpeta** (un `prueba_*.html` suelto da `multiple_root_compositions`). Los avisos `content_overlap`/contraste a mitad de animación suelen ser falsos positivos: se juzga por fotogramas.
- En CSS, `%` rompe `str %` en el ensamblado: usar reemplazo por tokens.
- Scripts de lote correctivos: `sombras_neutras.py`, `quitar_brillos.py`.

---

## 6. Cómo revisa Cris (cambio importante, 6-nov)

**No se hacen renders 720p ni «previews» MP4 para que él revise.** Cris revisa en el **timeline del Studio de HyperFrames**:

```bash
npx hyperframes@0.8.112 preview --background --no-open --port <p>
```
en la carpeta `video` del módulo → `http://localhost:<puerto>/#project/video`. Cuando aprueba, se exporta **directo en 1080p** (`render -q standard`). Los renders `-q draft` solo sirven para mis hojas de contacto internas.

---

## 7. Qué es específico de Academy y qué se puede llevar a videos comerciales

| Elemento | ¿Se lleva a los videos comerciales? |
|---|---|
| Sincronía por palabra (`AC.cue` + `tiempos.json`) | **Sí, es lo más valioso.** Reemplaza animar por segundos |
| Guion por bloques con `[tag]`, `*énfasis*`, `{pronunciación}` | **Sí** (ya hay receta de voz Hale en comerciales; adaptar `PRON`) |
| Un agente por escena + brief + vara de calidad | **Sí** para las escenas de motion/gráficos de un video comercial |
| Revisor independiente con puntaje 1–5 y máx. 3 vueltas | **Sí** |
| Voz congelada tras aprobar + `--correccion ids` | **Ya es regla en comerciales** (`voz_aprobada_no_se_regenera`) |
| Revisión en Studio de HyperFrames en vez de MP4 de avance | A decidir: en comerciales hoy hay preview 720p y .prproj |
| Inventario de assets al inicio y pedirlos en un solo mensaje | **Sí** |
| Vidrio, fondos por escena, interfaz recreada, Camila Rojas | Solo para piezas de interfaz/tutorial; no para video de producto |
| Sin Premiere, sin planos, sin S-Log3 | **No**: los comerciales sí usan planos, color y .prproj |
| Paleta/estilo «Apple» (`estilo_motion_apple`) | Los comerciales siguen su propia paleta; Academy explícitamente **ignora `05_MOTION.md`** |

**Conflictos a resolver al integrar** (decisión de Cris, no mía):
1. **Voz:** Academy usa `ACADEMY_VOZ_ID` + `eleven_v4` con TTS; comerciales usan receta Hale (`voz_exp_d.py`, v4 + STS). Son recetas distintas a propósito: no mezclarlas.
2. **Pronunciaciones:** `PRON` de Academy (Leson, Supr Nouts) vs. la lista de marcas de comerciales (`pronunciacion_marcas_voz`): unificar en un solo diccionario.
3. **Música/SFX:** Academy usa música de curso a −13 LU; comerciales piden drumming ≥160 BPM y ~6 LU bajo la voz. Parametrizar `mezclar_audio.py`.
4. **Revisión:** Studio (Academy) vs. preview 720p (comerciales, pasos 3–5 del flujo de 16).

---

## 8. Cómo montarlo como módulo del sistema de videos (propuesta mínima)

1. Copiar a `estudio-video/herramientas/motion_por_palabra/`: `ritmo.py`, `hacer_tiempos.py`, `academy.js` (solo `AC.cue`/`AC.icue`), `armar_maestro.py`, `arreglar_fuentes.py`, `mezclar_audio.py` (con parámetros de LU y música).
2. Añadir en `estudio-video/CLAUDE.md` una puerta «Escenas de motion» que use el patrón P7+P8 (un agente por escena + revisor).
3. Crear `prompts/escena.md` y `prompts/revisor.md` genéricos (los de Academy están en `.claude/skills/academy-onescreen/prompts/`).
4. Mantener `estudio-academy/` como está: es el caso de referencia y la vara de calidad.

---

## 9. Reglas de gasto y seguridad (siguen aplicando)

- **Gastar poco:** una sola generación de voz por módulo, una sola ronda de revisor por video, máx. 2 iteraciones por escena salvo defecto duro, sin agentes de exploración repetidos.
- Medir la app viva: sesión de Cris, **nunca** contraseñas, cerrar sesión, pagar, borrar ni pulsar «generar/crear» (gasta créditos del cliente o crea datos).
- Claves solo en variables de entorno; Odoo y datos de clientes no entran al proyecto.
- **No mencionar «Odoo» al cliente** en voz, texto en pantalla ni logos (grep «odoo|odú» en guion, `bloques.py` y compositions antes de entregar).
- Sin cifras de precios en el guion («consulta con tu asesor comercial»); nunca dirigirse al usuario en femenino; no explicar dos veces lo mismo; todo ajuste que se nombre se explica (qué hace y para qué).
- Entregar con **link clicable**, no con ruta.

---

## 10. Estado de los cursos (9-nov-2026)

SuprNotes M1 (vara aprobada, entregado) · Lessn M1–M5 (entregados) · QuizWiz M1–M3 (crudos, guiones pendientes) · LearningHub M1–M5 (entregados, sin crudo: fuente única = app viva).
