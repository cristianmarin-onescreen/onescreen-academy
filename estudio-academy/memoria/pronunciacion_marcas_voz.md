---
name: pronunciacion-marcas-voz
description: "Cómo escribir en el guion dirigido las marcas y siglas para que ElevenLabs las pronuncie bien (IA, QuizWiz, SuprNotes, Lessn, Scrybe…)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 467d22e0-0422-4874-87ab-33c830efe075
  modified: 2026-11-09T20:46:26.267Z
---

En `guion_dirigido_v3.txt` (lo que se manda a ElevenLabs) las marcas se escriben como suenan; el `guion_limpio.txt` y los textos en pantalla llevan el nombre real.

- IA → `i-a` (con "IA" la voz decía "AI" en inglés)
- QuizWiz → `Cuis Wis`
- SuprNotes → `Supr Nouts`
- Lessn → `leson`
- Gurú → `Gurú` (como suena en español)
- Scrybe → `escraib`
- LearningHub / Learning Hub → **`Learning Hub` tal cual (en inglés)** desde 9-nov (curso LearningHub M3–M5). «lernin jób» (QuizWiz, LearningHub M1–M2) a veces sale «lernin yob»; «lernin jab» y «lerning job» Cris las rechazó en muestras.
- Sage → `seich`

**Why:** Cris (28-oct, INTA23) oyó la voz decir "AI" en inglés y nombres mal dichos; pidió cuidado con eso.
**How to apply:** al escribir cualquier guion dirigido, reemplazar con este glosario antes de generar; tras Scribe confirmar que la transcripción coincide. Ver [[voz_una_sola_receta]].

**Corrección 9-nov-2026 (LearningHub M3):** los botones/términos de interfaz en inglés van TAL CUAL en inglés (Home Room, Download, Create a Room…); las escrituras fonéticas tipo «criéit a rum», «otomáticali yoin» sonaban a francés. Y nunca poner *énfasis* en siglas o términos en inglés: la dirigida los pasa a MAYÚSCULAS y la voz los deletrea («CÓDIGO CU ERRE» → «C U R»). Solo se respelean QR→cu erre, PDF→pe de efe, IA→i-a, QuizWiz, Google→Gúgol.

**Corrección 6-nov-2026 (QuizWiz):** «Learning Hub» → «lernin job» (no «lernin jab»). Respeling con «job» en el PRON de `bloques.py`.
