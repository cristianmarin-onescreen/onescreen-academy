# Brief · ESCENAS de motion del video «SuprNotes · Módulo 1» (OneScreen Academy)

Este brief reemplaza al de insertos para escenas completas. **Lee primero `BRIEF_COMUN.md`** (misma carpeta): casi todo aplica (estilo de vidrio, márgenes, contrato de sub-composición, determinismo, dónde trabajar, pruebas, entrega). Aquí solo van las DIFERENCIAS y las reglas nuevas.

## Qué es una escena
Una de las 12 escenas del video. Va sobre el **fondo continuo del módulo** (degradado azul oscuro con cuadrícula, viñeta y luces que el maestro ya pone): **tu escena NO lleva fondo propio** (transparente; puedes añadir luces/elementos propios sobre él). Tiempo local 0 = inicio de la escena (`AC.sceneDur(id)` = duración). Sincroniza con `AC.cue(escenaId, bloque, palabra, nth)` (tiempo local de una palabra de la voz), `AC.cueEnd`, `AC.blockStart/blockEnd`. El texto de cada bloque está en `cursos\SuprNotes-M1\voz\guion_limpio.txt` (secciones `## bNN`) y las palabras con sus tiempos en `assets/tiempos.js` (`AC_T.palabras`). Prueba con `python armar_maestro.py <escenaId>` (p. ej. `s03`); el id de composición y el archivo son `sNN-nombre` (ej. `compositions/s03-que-es.html`, `data-composition-id="s03-que-es"`).

## REGLA NUEVA DE RITMO (Cris, 5-nov: «hermoso, pero el timing se siente apresurado»)
Cris adora el estilo pero siente el motion apresurado. Diseña con **calma**:
- Cada movimiento principal dura **1.0–1.6 s** (eases suaves: power2.inOut, expo.out, power3.out), no 0.4–0.6 s.
- A lo sumo **UN evento principal por ventana de ~1 s**; escalona y **quita lo decorativo** antes que amontonar. Menos cosas, mejor ejecutadas.
- Cada reacción arranca en su palabra pero se despliega sin prisa; los textos clave se leen **≥1.2 s** quietos.
- Cada «beat» explicado termina con un **respiro**: la composición queda completa y quieta ≥1.2 s antes de pasar al siguiente beat (la voz tiene pausas; úsalas, no las llenes).
- Las ráfagas (partículas, destellos) acompañan, nunca compiten con lo que hay que leer.

## Más reglas (de lo que Cris aprobó)
- Entre escenas el corte es directo: tu escena entra sin fundido y su último cuadro debe verse **completo y limpio** (sin fade de salida).
- Nada de píldoras baratas ni texto en MAYÚSCULAS tipo diapositiva; titulares Rubik, cuerpo Manrope; «OneScreen» siempre con el logo oficial `assets/logo-white.png` (o `assets/onescreen-wordmark.svg`) cuando se firme la marca, o escrito «OneScreen» en Nevis (`font-family:"Nevis"`) si va en texto; «SuprNotes» siempre junto.
- Imaginación: motions diferentes en cada escena (diagramas que representan lo que dice la voz, 3D de vidrio, trazos que se dibujan, conteos, partículas con semilla, máscaras). Explicar > decorar. Ya existen escenas hechas como referencia de calidad y de lenguaje: `compositions/s05-cinco-salidas.html` y los insertos `s05a…s05e` (léelos).
- Datos de ejemplo inocuos; ejemplo del módulo: clase de biología sobre depredadores.

## Entrega
Igual que en el brief común: tu copia de trabajo en `agentes\<tu-escena>\` (copia de `video` sin `renders`), prueba/check/render/fotogramas (≥8, incluye cada palabra clave y el final), y copia SOLO `compositions/<tu-escena>.html` al original. Respuesta final corta.
