---
name: academy-quizwiz
description: "Curso QuizWiz de OneScreen Academy (6-nov-2026): 6 módulos, 63 escenas, voz Francisco, previews 720p listos; pendiente aprobación de Cris y render final."
metadata:
  node_type: memory
  type: project
  originSessionId: ab7eb158-9205-4741-a690-b582e73ddc06
  modified: 2026-11-06T18:04:06.572Z
---

Tercer curso de Academy (tras SuprNotes y Lessn). Fuentes: 3 crudos de Drive 1NE1NPFB… (narra Cris; Scribe escribió «Quizizz» por error), plataforma https://quizwiz.onescreensolutions.com/ (v1.6.0, morado #4E0F89→#7D00BA + verde #7DC243, DM Sans/Open Sans) y ficha D:\Archivos de computador\Descargas\OneScreen_QuizWiz_Spec_Sheet.pdf.

**Estructura FINAL (decidida por Cris tras dos rondas: «muy pocos módulos» → 10 → «ya mucho: 1-3 uno solo, 4, 5, 6 bien, 7+8 uno, 9+10 uno»):** 6 módulos: M1 Qué es QuizWiz, cómo entrar y tu cuenta (7:30) · M2 Primer examen desde texto (2:41) · M3 Editar y afinar (2:34) · M4 Tema/archivo/URL (2:29) · M5 Exportar, guardar y publicar (4:39) · M6 Compartir, resultados y certificación (3:53). Guiones `guion_v2.md` aprobados por Cris en `cursos\QuizWiz-M1…M6`; índice `QuizWiz_INDICE_MODULOS.md`; historial en `QuizWiz-crudos\` (crudos, transcripciones, versión de 10 módulos). Lección: agrupar por tema afín pero sin pasarse; al fusionar usar puentes cortos y renumerar «módulo N» en textos y tablas.

**ENTREGADO 6-nov (noche): los 6 módulos exportados a 1080p en `cursos\_entregas\QuizWiz_M1…M6_1080p.mp4`, aprobados por Cris tras revisar en el Studio (guion neutro, «Camila Rojas» siempre, «Learning Hub»→«lernin jób» elegida por Cris entre 5 muestras). Pendiente de Cris: borrar el quiz «PRUEBA Academy - borrar» de su cuenta; decidir si rehacer SuprNotes/Lessn con la voz nueva. Los puertos del Studio (3013–3018) quedan vivos hasta `preview --stop`.**
**Estado previo 6-nov (noche):** voz hecha con la clave V2 y la voz oficial del curso ( las tomas de la voz anterior quedaron en `voz\tomas_voz_anterior`), ritmo, tiempos, mezcla (música+swish, −17 LUFS), 63 escenas construidas por agentes (briefs `BRIEF_ESCENAS_QUIZWIZ.md`, `MODULO_QUIZWIZ_N.md`) y revisadas con hojas de contacto. **Previews 720p en `cursos\_previews_quizwiz\`** (de renders borrador + audio mezclado). Falta: aprobación de Cris, correcciones y render final con `_render_final_quizwiz.sh <N>` → `_entregas`.

**Pendientes / avisos para Cris:** (1) borrar de su cuenta QuizWiz el quiz «PRUEBA Academy - borrar» (código MBYVH8; se publicó con autorización «máxima»; respuesta de «camila.rojas» 3/3; se gastó 1 de 10 quizzes gratis); (2) `hyperframes snapshot` corre Gemini por defecto si hay GEMINI_API_KEY: SIEMPRE `--describe false` (algunos snapshots de la primera oleada corrieron sin la opción, ya dicho); (3) aproximado/no visto en vivo: registro, PDF/TXT/Forms/Guardar/Combinar, Ayuda/Acerca de, «Unirse quiz» con código, Finalizar/Publicar resultados, regenerar pregunta con 2 alternativas, selección de párrafo, desplegable Correcto/Incorrecto; (4) examen de certificación «15 preguntas, 20 min» viene del crudo; (5) los datos del perfil, estudiantes, medias y varias preguntas son ficticios; (6) M2 s06 «A tus estudiantes» tapa algo de texto; M1 s10 (registro) es pantalla inventada.
**How to apply:** no pulsar acciones destructivas ni «Enviar invitación» en la plataforma de Cris; no regenerar voz sin autorización; el estilo de motion es el de SuprNotes M1/M2/M5/M6 (metáfora real), no el de Lessn M2–M4.
