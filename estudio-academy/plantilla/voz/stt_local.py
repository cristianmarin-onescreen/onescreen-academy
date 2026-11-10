"""Transcripcion local con tiempos por palabra (faster-whisper) con la misma forma que devuelve Scribe.
Se usa cuando se agotan los creditos de ElevenLabs. pip install faster-whisper"""
_M = None
def scribe_local(wav):
    global _M
    from faster_whisper import WhisperModel
    if _M is None: _M = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = _M.transcribe(wav, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
    words, texto = [], []
    for s in segs:
        texto.append(s.text.strip())
        for w in s.words or []:
            words.append({"type": "word", "text": w.word.strip(), "start": float(w.start), "end": float(w.end)})
    return {"text": " ".join(texto), "words": words}
