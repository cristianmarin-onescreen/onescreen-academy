import json, re, importlib.util

IDEAS = {
2: {
 "s01": ("motion", "Apertura del módulo 2 (misma familia que la apertura del M1: ver cursos/SuprNotes-M1/video_v3/compositions/s01-apertura.html): wordmark/logo oficial, chip «Módulo 2», título «Importar contenido», tres tarjetas-índice que anuncian lo que viene (Grabar, Subir, Combinar fuentes). Termina con la promesa «darle a SuprNotes el material»."),
 "s02": ("motion", "Dos caminos: de un punto (la clase) salen dos rutas que se bifurcan hacia SuprNotes: ruta 1 GRABAR (micrófono + pantalla que se dibuja), ruta 2 SUBIR (YouTube, archivo, nube). Al decir cada palabra se enciende su ruta; al final convergen en un núcleo."),
 "s03": ("ui", "Opciones de grabación: recrear con fidelidad el diálogo/pantalla real de grabación de SuprNotes (ver UI_M2.md) y animar cada opción al nombrarla (pantalla + audio del sistema, pantalla + micrófono, solo audio con micrófono). Valor agregado: íconos animados (onda de audio, ventana), cursor con pulso, zoom, resto atenuado. Cierra con docente y estudiante."),
 "s04": ("ui", "Subir contenido: recrear el diálogo real de subir (YouTube, computador, Google Drive, OneDrive) y los formatos compatibles MP4, MKV, MOV, WebM, AVI como fichas que entran una a una (una por palabra); al final una ficha «¿otro formato? → YouTube»."),
 "s05": ("ui", "Video de YouTube paso a paso con la interfaz real: copiar enlace (botón Compartir en una ventana de navegador de vidrio; no imites la marca de YouTube, usa un ícono de play genérico), pegar en SuprNotes, reconocimiento del video, selector de minutos (rango arrastrable) y botón agregar."),
 "s06": ("ui", "Varias fuentes: la lista de fuentes de la clase (video + documento convertido a PDF) con la interfaz real; animación de fuentes que se suman y se combinan en una sola clase; ejemplos: docente (video, presentación, escritos) y estudiante (foto de apuntes)."),
 "s07": ("ui", "Nombre de la clase («El sistema solar»), materia/etiqueta («ciencias»), idioma (español/inglés/árabe) y el botón de generar, con la interfaz real; se escribe el nombre, se elige idioma; el botón se resalta al final (no se pulsa)."),
 "s08": ("motion", "Tres consejos para mejores resultados, tres motions distintos: (1) hasta 3 horas (reloj/barra que llena 3:00 con tope), (2) audio de buena calidad (onda ruidosa que se limpia), (3) material bien iluminado y legible (diapositiva borrosa que se enfoca). Cada uno con su propio color de acento."),
 "s09": ("motion", "Limpieza automática: una transcripción fluye por un filtro de vidrio; las palabras ofensivas y el dato personal (un número de cédula ficticio tipo 1.***.***) se tachan/difuminan y quedan fuera; sale texto limpio y profesional. Sello de protección de menores. Todo automático: nadie toca nada."),
 "s10": ("motion", "Cierre: tres ideas del módulo (grabar o subir; varias fuentes; limpieza automática) como tarjetas de vidrio, y una tarjeta «Módulo 3 · Recorrido por la interfaz» con el lockup SuprNotes y la firma OneScreen (como el cierre del M1: ver s12-cierre.html del M1)."),
},
3: {
 "s01": ("motion", "Apertura del módulo 3: logo oficial, chip «Módulo 3», título «Recorrido por la interfaz», un mapa de la plataforma con cuatro zonas que se iluminan (Perfil, Inicio, Biblioteca, Soporte)."),
 "s02": ("ui", "Perfil: nombre, correo, uso mensual (resúmenes de IA y materiales con barras de uso) y planes; recomendación de consultar al asesor comercial de OneScreen o en suprnotes.ai (ver UI_M3.md)."),
 "s03": ("ui", "Menú de opciones: perfil, cerrar sesión (solo mostrar), tema oscuro/claro (alternar la vista con una transición suave), idioma español/inglés."),
 "s04": ("ui", "Inicio: dos opciones para importar (subir/grabar), resúmenes recientes y el asistente de estudio de IA (chat entrenado solo con tus clases): animar que solo responde sobre «tus tres clases»."),
 "s05": ("ui", "Biblioteca: tarjetas de las tres clases con su antigüedad (hace 70 días, hace unos minutos, la recién creada) y las estadísticas de estudio (resúmenes de IA, cuestionarios, tarjetas, guías de revisión) con conteos que suben."),
 "s06": ("ui", "Filtros (completadas, favoritas, recientes, compartidas), etiquetas (organizar por materia o día de la semana: se asignan y se filtran), buscador (se escribe y filtra) y filtros por tipo."),
 "s07": ("ui", "Soporte: el botón, el ticket (asunto, mensaje, adjuntar pantallazo) y el correo supernotes@onescreensolutions.com; sin enviar nada. Un reloj de «menor tiempo posible»."),
 "s08": ("motion", "Cierre del módulo 3: cuatro tarjetas-resumen (inicio, biblioteca, asistente, soporte), y «Siguiente: tu clase ya creada» con lockup y firma OneScreen."),
},
4: {
 "s01": ("motion", "Apertura del módulo 4: logo, chip «Módulo 4», título «Tu clase creada»; una tarjeta de clase «El sistema solar» con dos fuentes (video + documento) que se abre."),
 "s02": ("ui", "Resumen de IA de la clase con la interfaz real: se condensan dos fuentes (video + paper) en un solo resumen, incluye capturas del video; animar la condensación y resaltar las capturas."),
 "s03": ("ui", "Modo lectura vs modo edición: alternar, aparece la barra de herramientas de texto, se escribe «Marte es un planeta genial» y se muestra que el cambio viaja a tarjetas, cuestionario y guía (flechas hacia esas tres tarjetas)."),
 "s04": ("ui", "Tabla de contenidos automática: el resumen largo hace scroll, la tabla aparece y al tocar un punto la vista salta a ese tema."),
 "s05": ("ui", "Pantalla completa y exportar: menú con las cuatro opciones (correo, enlace, PDF, Google Drive); cada una anima su destino."),
 "s06": ("ui", "Chat de IA con el material de la clase: preguntas sugeridas, la pregunta «¿qué puedes hacer con esta nota?» y la respuesta (preguntar, investigar lo que no sepamos, elaborar ejemplos, fórmulas, acrónimos, resúmenes, guías); concepto «minidocente» y sello «solo tu clase»."),
 "s07": ("ui", "Tarjetas didácticas: selector de temas, generar, tarjeta 1 de 25 «¿qué papel jugaron los quarks en el universo temprano?», pistas, voltear para revelar la respuesta con giro 3D."),
 "s08": ("ui", "Cuestionario: elegir temas, duración (corta/media/larga) y dificultad (fácil/media/difícil) con selectores animados, y generar desde el resumen (sin pulsar generar)."),
 "s09": ("motion", "Cierre del módulo 4: de una sola clase salen resumen, chat, tarjetas y cuestionarios; y «Siguiente: cuestionarios y taxonomía de Bloom» con lockup y firma."),
},
5: {
 "s01": ("motion", "Apertura del módulo 5: logo, chip «Módulo 5», título «Cuestionarios y taxonomía de Bloom»; una pirámide de cuatro niveles que se levanta."),
 "s02": ("motion", "¿Qué es la taxonomía de Bloom?: marco de referencia para objetivos y evaluaciones educativas; SuprNotes la aplica para clasificar y generar preguntas de distinta complejidad cognitiva. Visual: una pirámide/escalera de cristal que se construye, preguntas que se ubican en ella y se clasifican."),
 "s03": ("motion", "Los cuatro niveles, uno por frase: 1 Conocimiento y comprensión (recordar, entender conceptos básicos), 2 Aplicación (usar lo aprendido en situaciones concretas), 3 Análisis (descomponer información e identificar relaciones), 4 Evaluación y síntesis (habilidades de mayor orden). Cada nivel con su propio motion explicativo, ejemplo de biología (depredadores) y color."),
 "s04": ("motion", "Alineación con el nivel de dominio: un cuestionario cuyas preguntas se alinean con el contenido de la clase Y con el nivel esperado; estadísticas para el estudiante (de su propio estudio) y para el docente (cómo entienden su clase): dos paneles de datos que se llenan; mejoras a trabajar con cada uno."),
 "s05": ("ui", "Reporte de un examen: puntuación general (0 de 20), recomendaciones generales por desempeño; recrear con la interfaz real (ver UI_M5.md) y animar los datos en cero con claridad."),
 "s06": ("ui", "Desempeño por taxonomía de Bloom: recordar, entender, aplicar, evaluar (los cuatro pilares del reporte real) con su gráfico/barras; qué funciona en mis clases y qué aprendo mejor."),
 "s07": ("ui", "Dominio por tema: cada tema con su nivel de dominio y recomendaciones («Este tema necesita revisión significativa. Enfócate en comprender los conceptos centrales primero.»), botón de volver a practicar."),
 "s08": ("motion", "Objetivo de SuprNotes: que los estudiantes realmente aprendan, no solo tener un resumen; «estudiar no debería ser difícil»; acompañar durante la clase, después y antes de los exámenes (tres momentos en una línea de tiempo)."),
 "s09": ("motion", "Cierre del módulo 5: a largo plazo estudiantes mejor preparados, instituciones con mejores resultados, mayor progreso académico (tres tarjetas/gráficos que suben); y «Siguiente: la biblioteca y el cierre del curso» con lockup y firma."),
},
6: {
 "s01": ("motion", "Apertura del módulo 6, el último: logo, chip «Módulo 6», título «Biblioteca y examen»; recorrido en tres hitos (Biblioteca, Repaso, Examen) que se iluminan."),
 "s02": ("ui", "Biblioteca: botón de acceso, tarjetas didácticas del sistema solar, cuestionarios, guías de revisión (pestañas/secciones reales, ver UI_M6.md)."),
 "s03": ("ui", "Guía de revisión abierta: temas, glosario, fórmulas y ecuaciones; énfasis en que sirve para matemáticas y física (fórmulas resaltadas)."),
 "s04": ("ui", "Favoritos: la estrellita se marca, la clase se guarda, el filtro muestra solo favoritas/resúmenes de IA/recientes."),
 "s05": ("motion", "Transición al repaso: «lo que sigue es el examen de certificación; antes, un repaso»: una línea de tiempo/tablero que reúne los pasos del curso en tarjetas pequeñas, listo para repasar."),
 "s06": ("motion", "Repaso 1 · crear una clase: subir (YouTube, PC, Drive/OneDrive) o grabar (solo audio, pantalla, celular grabando): dos ramas con íconos que se encienden en cada palabra."),
 "s07": ("motion", "Repaso 2 · el resumen: chat de IA, tabla de contenidos, editar, exportar (correo, enlace, PDF, Drive); miniaturas fieles (usa componentes de las escenas del M4 si ya existen en cursos/SuprNotes-M4/video/compositions) o dibújalas tú."),
 "s08": ("motion", "Repaso 3 · estudiar y medir: tarjetas didácticas, cuestionario en modo práctica o examen (cronómetro, asistente de chat, aleatorizar), reportes con la taxonomía de Bloom (recordar, entender, aplicar, evaluar) y recomendaciones."),
 "s09": ("motion", "Repaso 4 · guía de revisión y entorno de estudio inteligente: la guía extrae puntos clave (fórmulas, conceptos, palabras); de una clase normal sale un entorno completo (resumen, tarjetas, cuestionario, guía) para prepararte o preparar a tus estudiantes."),
 "s10": ("motion", "Examen de certificación: 15 preguntas y 25 minutos; un reloj de 25:00 y un contador 0/15 que se llena; al aprobar, sello «Certificado por OneScreen en SuprNotes». Sin imitar un examen real: solo tarjetas de vidrio con números."),
 "s11": ("motion", "Mensaje de cierre: SuprNotes transforma la forma en que docentes y estudiantes gestionan el conocimiento; a partir de hoy tienes todo para implementarla con confianza y criterio; úsala y familiarízate: tres frases clave que aparecen quietas y legibles."),
 "s12": ("motion", "Cierre del curso: «Gracias» con el lockup SuprNotes + firma OneScreen Academy (como el cierre del M1), sin nombres de personas; «mucho éxito en tu examen»."),
},
}

OVER = {
2: {
 "s03": ("ui", "Grabación (interfaz VIVA, ver UI_M2.md §2): modal «Iniciar grabación» con las dos opciones «Grabación de pantalla» (con subtítulos en vivo) y «Grabación de audio» (micrófono), botón Continuar; luego «Elige la vista de grabación»: «Modo flotante / pantalla completa» y «Modo editor lado a lado». Anima cada opción en su palabra; cursor con pulso, zoom, resto atenuado; cierra con docente y estudiante."),
 "s04": ("ui", "Subir (VIVA, UI_M2.md §3): modal «Crear resumen inteligente» con el menú «Añadir archivo»: Desde tu dispositivo, Google Drive, OneDrive, Dropbox, YouTube, Teams, Zoom (se encienden al nombrarse); formatos MP4, MKV, MOV, WebM, AVI como fichas que entran una a una; al final ficha «¿otro formato? → YouTube»."),
 "s05": ("ui", "YouTube (VIVA, UI_M2.md §4): sub-modal «Añadir un video de YouTube»: pegar el enlace, el video reconocido con su duración, línea de tiempo con asas moradas para elegir segmentos a conservar, casilla de permiso azul y botón «Añadir video». No imites la marca de YouTube (usa el ícono genérico de assets_ui)."),
 "s06": ("ui", "Varias fuentes (VIVA, UI_M2.md §5): selector con pestañas Archivos / Notas / Resúmenes inteligentes, filas de fuentes con checkbox, chips de fuentes elegidas con ✕ en el pie y botón «Siguiente»; animación de fuentes (video, documento, audio, notas) que se suman en el pie; ejemplos docente (video, presentación, escritos) y estudiante (notas)."),
 "s07": ("ui", "Suri (VIVA, UI_M2.md §6/7): modal «Suri está preparando tu resumen inteligente…»: «Leyendo tus fuentes…» fila por fuente con estado Leyendo→Documento/Video, «¡He leído tus fuentes! Esto es lo que encontré:», y la tarjeta «Una pregunta rápida de Suri / Tu respuesta da forma al plan» con opciones radio (la sugerida) y «Enviar». Nada se envía realmente."),
},
3: {
 "s02": ("ui", "Perfil (VIVA, UI_M3.md): `/dashboard/profile` con menú lateral Perfil / Uso / Facturación; «Información del perfil» (nombre, correo, «Nombre del asistente: Suri»), pestaña Uso con dos tarjetas de anillo («Créditos de resumen inteligente», «Créditos de material de estudio» con fecha de reinicio) y Facturación con los planes; recomendación de consultar al asesor comercial o suprnotes.ai."),
 "s03": ("ui", "Idioma y accesibilidad (VIVA): selector «ESP ⌄» (English/Español) en la cabecera; modal «Ajustes de accesibilidad» con Tema Claro/Oscuro/Sistema (alternar con transición suave) y ajustes de lectura/color; y el avatar con «Perfil» y «Cerrar sesión» (solo mostrar, nunca pulsar)."),
 "s04": ("ui", "Inicio y asistente (VIVA): dashboard con las dos tarjetas (Crear resumen inteligente / Iniciar grabación), chips (Crear una nota, tarjetas, cuestionario, guía) y Recientes; y la página del asistente de estudio con Suri (saludo, caja «Hola, ¿en qué puedo ayudarte?», «Añadir desde la biblioteca»)."),
 "s05": ("ui", "Biblioteca (VIVA): carpetas «Files» (con Audio, Documents, Video) y «Recordings», y debajo tres kits de estudio con fecha; cada kit con sus pestañas (Resumen inteligente, Cuestionario, Tarjetas, Guía de repaso). NO hay panel de estadísticas ni pestañas de biblioteca."),
 "s06": ("ui", "Buscar, ordenar, filtrar (VIVA): buscador «Buscar en la biblioteca», orden Recientes/Más antiguos/A-Z/Z-A, «Filtro» (tipo, etiquetas), «Filtrar por: Favoritos / Compartido conmigo», vista cuadrícula/lista con columnas Nombre·Etiquetas·Creado·Compartido con; etiquetas de materia (ej. Science)."),
 "s07": ("ui", "Ayuda y soporte (VIVA): es una PÁGINA `/dashboard/support` «Contactar con soporte» con Asunto, Mensaje, Adjuntos y correo supernotes@onescreensolutions.com; no envíes nada; un reloj de «menor tiempo posible»."),
},
4: {
 "s03": ("ui", "Edición (VIVA, UI_M4.md): no hay modos lectura/edición; al hacer clic en el documento aparece la barra de herramientas (deshacer, títulos, listas, alinear, B I S, enlace…), se escribe «Marte es un planeta genial», el indicador «Guardado ✓» y flechas hacia Tarjetas, Cuestionario y Guía."),
 "s04": ("ui", "Tabla de contenido (VIVA): botón de TOC en la esquina del documento que abre el árbol «Tabla de contenido»; al elegir un punto el documento salta a ese tema."),
 "s05": ("ui", "Exportar y compartir (VIVA): «Exportar ⌄» → modal «Exportar resumen de IA» con Formato PDF/Word/Más y «Guardar en» Descargar/Google Drive/OneDrive/Dropbox/Teams; y «Compartir kit de estudio» con pestañas Correo / Grupo / Enlace."),
 "s06": ("ui", "Suri en el resumen (VIVA): panel derecho «¡Suri está aquí para ayudarte!», orbe, entrada «Haz preguntas o pide cambios»; pregunta «¿qué puedes hacer con esta nota?» y respuesta (contestar dudas, investigar, elaborar ejemplos, fórmulas, acrónimos, resúmenes, guías); concepto «minidocente» y sello «solo tu clase». No hay preguntas sugeridas."),
 "s07": ("ui", "Tarjetas (VIVA): mazo de 25 tarjetas, cajas Dominadas/Por repasar/Sin estudiar, tarjeta morada «¿Qué papel jugaron los quarks en el universo temprano?» con «Toca o pulsa Espacio para girarla» (giro 3D al reverso blanco con la respuesta) y botones 1 Dominada / 2 Mostrar de nuevo / 3 Repasar después. No hay pistas."),
 "s08": ("ui", "Cuestionario (VIVA): lista con tarjeta «Quiz on El sistema solar» (Fácil, 20 preguntas), «Crear más cuestionarios», selector «Elige tus temas» (casillas), y modo Práctica|Examen con «Con tiempo». Duración/dificultad NO aparecen en el paso de crear."),
},
5: {
 "s05": ("ui", "Informe (VIVA, UI_M5.md): anillo «2/20 · 10% de puntuación», «¡Sigue practicando!», tiempo medio y total; consejo de Suri en caja lila. Sin radar ni recomendaciones generales."),
 "s06": ("ui", "Rendimiento por tema con Bloom (VIVA): barras por tema coloreadas por nivel (leyenda Recordar, Comprender, Aplicar, Evaluar) con porcentajes; qué funciona en mis clases y qué aprendo mejor."),
 "s07": ("ui", "Dominio por tema + consejo de Suri («Te cuestan las preguntas de evaluación, pero dominas las definiciones. Suri te recomienda comparar argumentos y justificar tus respuestas.») y volver a practicar (modos Práctica/Examen, Con tiempo)."),
},
6: {
 "s02": ("ui", "Biblioteca (VIVA, UI_M3/UI_M6): carpetas y kits; cada kit con pestañas Resumen inteligente · Cuestionario · Tarjetas · Guía de repaso; «Filtro > Tipo» para ver solo tarjetas, cuestionarios o guías."),
 "s03": ("ui", "Guía de repaso abierta (VIVA, UI_M4/UI_M6): TOC con Definitions / Formulas & Equations / Key Concepts; definiciones en negrita; fórmula centrada E = mc² con «Where: …»; chat Suri a la derecha."),
 "s04": ("ui", "Favoritos (VIVA): estrella amarilla en la tarjeta del kit (se marca), «Filtrar por: Favoritos / Compartido conmigo» y orden Recientes."),
 "s06": ("motion", "Repaso 1 · crear una clase: «Crear resumen inteligente» con «Añadir archivo» (dispositivo, Drive, OneDrive, Dropbox, YouTube, Teams, Zoom) o «Iniciar grabación» (solo audio o pantalla): dos ramas con íconos que se encienden en cada palabra. (Sin celular.)"),
 "s07": ("motion", "Repaso 2 · el resumen: Suri lee fuentes y arma el resumen; tabla de contenido, editar el texto, exportar (PDF/Word; Drive, OneDrive, Dropbox, Teams) y compartir (correo, grupo, enlace); Suri responde con base en lo explicado."),
 "s08": ("motion", "Repaso 3 · estudiar y medir: tarjetas didácticas, cuestionario en modo práctica o examen (con tiempo o sin tiempo), informe con puntuación y rendimiento por tema coloreado por Bloom (recordar, comprender, aplicar, evaluar) y recomendación de Suri."),
 "s09": ("motion", "Repaso 4 · guía de repaso (definiciones, fórmulas y ecuaciones, conceptos clave) y entorno de estudio inteligente: de una clase sale resumen, tarjetas, cuestionario y guía."),
},
}
for _n, _d in OVER.items(): IDEAS[_n].update(_d)
for n in (2, 3, 4, 5, 6):
    base = "cursos/SuprNotes-M%d" % n
    d = json.load(open(base + "/video/escenas_def.json", encoding="utf-8"))
    sp = importlib.util.spec_from_file_location("bl%d" % n, base + "/voz/bloques.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    txt = dict(m.BLOQUES)
    out = ["# Módulo %d · %s\n" % (n, d["titulo"]),
           "Proyecto: `%s/video`. Narración: `%s/voz/ritmo/narracion_v2.wav` (voz PROVISIONAL, cambiará por la real: **toda la sincronía debe salir de `AC.cue`/`AC.cueEnd`/`AC.blockStart`, nunca de segundos escritos a mano**). Referencias de la interfaz real: `%s/agentes/ref_ui/UI_M%d.md` y `cursos/UI_COMUN.md` (si no existen todavía, no inventes la interfaz: avisa en tu reporte). Crudo original (hojas de contacto `%s/crudo/hoja_*.jpg` muestran cómo se ve cada pantalla y cuándo): `%s/crudo/`.\n" % (base, base, base, n, base, base)]
    out.append("## Escenas\n")
    for e in d["escenas"]:
        tipo, idea = IDEAS[n][e["id"]]
        out.append("### %s · %s  (tipo: %s)\nArchivo: `compositions/%s-%s.html`, composition-id `%s-%s`. Bloques de voz: %s. Fondo del maestro (tu escena es transparente sobre él): centro %s, medio %s, borde %s, textura %s.\n\n**Narración (limpia):**\n" % (e["id"], e["nombre"], tipo, e["id"], e["nombre"], e["id"], e["nombre"], ", ".join(e["bloques"]), *e["tema"]))
        for b in e["bloques"]:
            lim = re.sub(r"\[[^\]]*\]\s*", "", txt[b]).replace("{SuprNotes}", "SuprNotes"); lim = re.sub(r"\*([^*]+)\*", r"\1", lim)
            out.append("- `%s`: %s\n" % (b, lim))
        out.append("\n**Concepto:** %s\n" % idea)
    open("cursos/MODULO_%d.md" % n, "w", encoding="utf-8").write("\n".join(out))
print("ok")
