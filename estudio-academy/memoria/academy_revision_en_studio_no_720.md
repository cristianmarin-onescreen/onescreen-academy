---
name: academy-revision-en-studio-no-720
description: Cris no quiere renders 720p de avance en Academy; se revisa en el Studio de HyperFrames (preview) y el 1080p solo cuando él aprueba.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 165b278a-0e68-4a21-a926-9ae01519abb5
  modified: 2026-11-06T20:55:59.165Z
---

No hacer renders de 720p para que Cris revise los videos de Academy. Se le da un link al Studio de HyperFrames (`npx hyperframes@0.8.112 preview --background --no-open --port=<p> <video>`), que es más rápido y no renderiza. Solo si el video ya está aprobado se lanza el 1080p (`render_final.sh`).

**Why:** 6-nov-2026, tras varios avances 720p de los módulos de estudiantes y admin; los renders tardan 7-9 min y los quiere evitar.
**How to apply:** en P8/P9 del skill academy-onescreen, sustituir "render draft → 720p para Cris" por preview en Studio. Los renders internos de los agentes para autorrevisión pueden seguir (límite 2 vueltas). 1080p solo con aprobación explícita de Cris. Ver [[academy_videos_cursos]].
