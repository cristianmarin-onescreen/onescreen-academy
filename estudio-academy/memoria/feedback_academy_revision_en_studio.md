---
name: feedback-academy-revision-en-studio
description: Cris revisa los videos de Academy en el timeline del Studio de HyperFrames, no en MP4 de 720p; al aprobar se exporta directo en 1080p.
metadata:
  type: feedback
---

Regla de Cris (6-nov-2026, QuizWiz): no hacer renders/previews MP4 de 720p para revisión («es perder el tiempo»). Se le muestran los módulos en el **timeline de HyperFrames Studio** (`hyperframes preview --background --no-open --port N` en `QuizWiz-M<n>\video`, URL `http://localhost:N/#project/video`) y, tras su OK, se exporta **directo en 1080p** (`render -q standard`).

**Why:** el render borrador + conversión a 720p tarda ~15 min por ronda y él ve lo mismo en el Studio al instante, con voz y música.
**How to apply:** tras cada ronda de correcciones, solo `armar_maestro` + `check` y abrir el Studio; mis hojas de contacto con renders `-q draft` son internas (no entregables). Si el puerto pedido está ocupado, HyperFrames elige otro: leer `preview --list`. Ver [[academy_quizwiz]] y [[academy_videos_cursos]].
