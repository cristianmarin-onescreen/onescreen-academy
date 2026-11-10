#!/bin/sh
# Prepara el proyecto de video de un módulo de Academy (cualquier curso).
# uso: preparar_video.sh "<carpeta_modulo>"
#   ej.: preparar_video.sh "cursos/AcademyAdmin-M1"
# Copia el sistema compartido (academy.css/js, fuentes, logo OneScreen) SIN pisar los assets de marca del curso que ya
# estén en video/assets (logo oficial del software, íconos: ver video/assets/INVENTARIO.md), pone la narración con ritmo
# y genera tiempos.js + escenas.json + index.html. Después se ejecuta mezclar_audio.py (pisa narracion.wav).
mod=$(echo "$1" | sed 's#\\#/#g; s#/*$##')
V="$mod/video"; A="$V/assets"; mkdir -p "$A"
P="$(cd "$mod/../.." && pwd)/estudio-academy/plantilla/video"
cp -rn "$P/assets/." "$A/"            # -n: no pisa lo que ya exista (assets de marca del curso)
cp -f "$P/assets/academy.css" "$P/assets/academy.js" "$A/"   # el sistema compartido siempre al día
cp "$mod/voz/ritmo/narracion_v2.wav" "$A/narracion.wav"
cp "$P/hacer_tiempos.py" "$P/armar_maestro.py" "$P/arreglar_fuentes.py" "$P/quitar_brillos.py" "$P/sombras_neutras.py" "$V/"
cd "$V" && python hacer_tiempos.py && python armar_maestro.py | tail -1
