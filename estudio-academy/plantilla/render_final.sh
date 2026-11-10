#!/bin/sh
# Render final de un módulo de Academy (cualquier curso).
# uso: render_final.sh "<carpeta_modulo>" [carpeta_video=video]
#   ej.: render_final.sh "cursos/AcademyAdmin-M1"
# Deja renders/<Nombre>_1080p.mp4, renders/<Nombre>_preview_720p.mp4 y copia el 1080p a cursos/_entregas/
mod=$(echo "$1" | sed 's#\\#/#g; s#/*$##'); v=${2:-video}
mod=$(cd "$mod" && pwd)
nombre=$(basename "$mod" | sed 's/-M/_M/')
cd "$mod/$v" || exit 1
mkdir -p renders "$mod/../_entregas"
npx --yes hyperframes@0.8.112 render -q standard -o "renders/${nombre}_1080p.mp4" > renders/final.log 2>&1
ffmpeg -y -i "renders/${nombre}_1080p.mp4" -vf scale=1280:720 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 160k "renders/${nombre}_preview_720p.mp4" >> renders/final.log 2>&1
cp "renders/${nombre}_1080p.mp4" "$mod/../_entregas/${nombre}_1080p.mp4"
grep -c "AC.cue: no se encontro" renders/final.log | sed 's/^/avisos AC.cue sin palabra: /' >> renders/final.log
echo LISTO >> renders/final.log
