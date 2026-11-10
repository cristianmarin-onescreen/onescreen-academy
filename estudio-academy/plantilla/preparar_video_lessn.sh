n=$1
V="cursos/Lessn-M$n/video"; A="$V/assets"; mkdir -p "$A"
P="estudio-academy/plantilla/video"
cp -r "$P/assets/." "$A/"
cp "cursos/Lessn-assets/"* "$A/" 2>/dev/null
cp "cursos/Lessn-M$n/voz/ritmo/narracion_v2.wav" "$A/narracion.wav"
cp "$P/hacer_tiempos.py" "$P/armar_maestro.py" "$P/arreglar_fuentes.py" "$V/"
cd "$V" && python hacer_tiempos.py && python armar_maestro.py | tail -1
