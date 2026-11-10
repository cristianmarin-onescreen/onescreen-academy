# Ronda v3 · logotipo oficial de SuprNotes + fondos por escena

Contexto: Cris vio el preview azul y pidió dos cambios: (1) **«todo es azul, es monótono»**: ahora cada escena tiene su propio fondo (color y textura distintos) y los acentos de las salidas vuelven a variar (azul, cian, verde azulado, coral, rosa); (2) **usar el logotipo oficial de SuprNotes** donde SuprNotes se muestra como marca.

## Proyecto y flujo (cambia la carpeta de trabajo)
- Proyecto vigente: `cursos\SuprNotes-M1\video_v3\` (ya trae fondos por escena y acentos recoloreados). **Copia** esa carpeta SIN `snapshots`/`renders` a `cursos\SuprNotes-M1\agentes_v3\<tu-id>\` y trabaja ahí. Prueba con `python armar_maestro.py <tu-escena>` (p. ej. `s01`), `npx --yes hyperframes@0.8.112 check`, render `-q draft`, y **revisa fotogramas** (inicio, palabras clave, final). Al terminar copia SOLO tus archivos modificados a `video_v3\compositions\` (y los assets nuevos que hayas creado a `video_v3\assets\`; avísalo).
- Lee de nuevo `agentes\BRIEF_COMUN.md` y `BRIEF_ESCENAS.md` (márgenes 160/120, ritmo calmado, corte directo, determinismo).

## Fondos por escena (tu escena es transparente sobre el fondo del maestro)
s01 azul de marca · s02 grafito cálido (rayado diagonal) · s03 verde azulado (anillos concéntricos) · s04 pizarra (cruces finas) · s05 índigo azulado · s06 océano (líneas de barrido) · s07 tinta casi negra · s08 terracota cálida · s09 vino · s10 acero (retícula) · s11 azul noche · s12 azul de marca. Revisa que tu escena se lea bien sobre el fondo que le tocó y, si algún acento se pelea con él, ajústalo (sin perder el lenguaje de vidrio del módulo).

## Logotipo oficial (assets ya en `assets/`)
- `assets/sn-app-icon.png` — ícono de app oficial: cuadrado redondeado morado con libro abierto blanco + triángulo de «play» + trazo de lápiz (180×180). Úsalo entero (no lo recolorees) a **≤ 200 px** de ancho mostrado (más grande se pixela).
- `assets/sn-mark.png` — la marca sola (libro con play y lápiz) como máscara de 142×124 con transparencia; úsala con `mask-image` + `background-color` si necesitas la marca en un solo color (blanco/cian) a ≤ 150 px de ancho.
- **Lockup oficial**: ícono de app + la palabra «SuprNotes» a su derecha (altura del texto ≈ 0,42 × alto del ícono, separación ≈ 0,3 × alto del ícono). La palabra va en una sans humanista de peso medio (usa **Poppins 500**, tracking normal; blanca sobre los fondos oscuros del módulo). Nunca estires ni cambies proporciones del ícono; deja aire alrededor.
- Íconos reales de la app (SVG) en `assets/sn/`: `youtube.svg`, `pdf.svg`, `google-slides.svg`, `google-docs.svg`, `drive.svg`, `rec-ring.svg`, `rec-icon.svg`, `rec-mic.svg` (de `/assets/ds/dashboard/` de suprnotes.ai).
- «OneScreen» sigue con `assets/logo-white.png` (logo oficial de OneScreen).
- Dónde reemplazar/añadir (tu encargo concreto viene en tu mensaje): donde SuprNotes aparezca como MARCA (wordmark, núcleo, firma, favicon), sustituye la versión escrita/aproximada por el lockup o el ícono oficial. Donde solo se nombra el producto dentro de una frase, déjalo como texto.
