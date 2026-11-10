/* Ayudantes compartidos de Academy. Todo es determinista (sin reloj, sin azar sin semilla). */
window.AC = (function () {
  const T = window.AC_T;
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");
  const scene = {}; T.escenas.forEach((e) => (scene[e.id] = e));
  const block = {}; T.bloques.forEach((b) => (block[b.id] = b));
  const ins = {}; (T.insertos || []).forEach((e) => (ins[e.id] = e));

  // distancia de edicion (para tolerar que el transcriptor escriba distinto: Supernotes/SuprNotes, vídeo/video...)
  function lev(a, b) {
    const m = a.length, n = b.length; if (!m || !n) return Math.max(m, n);
    let prev = Array.from({ length: n + 1 }, (_, j) => j);
    for (let i = 1; i <= m; i++) { const cur = [i]; for (let j = 1; j <= n; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); prev = cur; }
    return prev[n];
  }
  // Palabra del bloque: exacta, o la mas parecida (distancia <= 2 para palabras de 5+ letras); null si no hay
  function findWord(blockId, word, nth) {
    nth = nth || 0; const q = norm(word); let c = 0;
    for (const w of T.palabras) if (w.b === blockId && norm(w.w) === q) { if (c === nth) return w; c++; }
    if (q.length >= 5) {
      const cand = T.palabras.filter((w) => w.b === blockId && lev(norm(w.w), q) <= 2);
      if (cand[nth]) return cand[nth];
    }
    return null;
  }
  // Estimacion cuando el transcriptor no trae la palabra: se ubica en el GUION del bloque (b.g = palabras del texto) y se mapea
  // proporcionalmente a las palabras transcritas. Tambien resuelve marcas habladas distinto (Supr Nouts, One Screen...).
  function estimate(blockId, word, nth) {
    nth = nth || 0; const q = norm(word), b = block[blockId], pal = T.palabras.filter((w) => w.b === blockId);
    if (!pal.length) return null;
    const g = b.g || [];
    if (q.startsWith("su")) { const c = pal.filter((w) => norm(w.w).startsWith("su")); if (c[nth]) return c[nth]; }
    if (q === "onescreen") { const i = pal.findIndex((w, k) => norm(w.w) === "one" || norm(w.w) === "juan" || norm(w.w) === "onescreen"); if (i >= 0) return pal[i]; }
    if (g.length) {
      let c = 0, idx = -1;
      for (let i = 0; i < g.length; i++) { if (g[i] === q || (q.length >= 5 && lev(g[i], q) <= 2)) { if (c === nth) { idx = i; break; } c++; } }
      if (idx >= 0) return pal[Math.min(pal.length - 1, Math.round(idx * (pal.length - 1) / Math.max(1, g.length - 1)))];
    }
    if (q.startsWith("su") || q.startsWith("sup")) { const c = pal.filter((w) => norm(w.w).startsWith("su")); if (c[nth]) return c[nth]; }
    return null;
  }
  // Tiempo LOCAL de la escena (0 = inicio de la escena) en que se dice una palabra (la n-esima ocurrencia, 0 = primera).
  // Si la palabra no existe (otra voz/transcripcion) cae a un punto estimado dentro del bloque en vez de al inicio.
  function cue(sceneId, blockId, word, nth) {
    const w = findWord(blockId, word, nth) || estimate(blockId, word, nth);
    if (w) return +(w.t0 - scene[sceneId].inicio).toFixed(3);
    console.warn("AC.cue: no se encontro '" + word + "' (" + (nth || 0) + ") en " + blockId);
    const b = block[blockId];
    return +(b.inicio + 0.35 * (b.fin - b.inicio) - scene[sceneId].inicio).toFixed(3);
  }
  // Fin local de la palabra
  function cueEnd(sceneId, blockId, word, nth) {
    const w = findWord(blockId, word, nth) || estimate(blockId, word, nth);
    if (w) return +(w.t1 - scene[sceneId].inicio).toFixed(3);
    return cue(sceneId, blockId, word, nth);
  }
  // Igual que cue pero relativo al inicio de un INSERTO (animacion a la que se corta desde la escena)
  function icue(insId, blockId, word, nth) {
    const w = findWord(blockId, word, nth) || estimate(blockId, word, nth);
    if (w) return +(w.t0 - ins[insId].inicio).toFixed(3);
    console.warn("AC.icue: no se encontro '" + word + "' en " + blockId);
    return 0;
  }
  const insDur = (insId) => ins[insId].dur;
  const blockStart = (sceneId, blockId) => +(block[blockId].inicio - scene[sceneId].inicio).toFixed(3);
  const blockEnd = (sceneId, blockId) => +(block[blockId].fin - scene[sceneId].inicio).toFixed(3);
  const sceneDur = (sceneId) => scene[sceneId].dur;

  const ICON = {
    doc: '<rect x="10" y="6" width="28" height="36" rx="4"/><path d="M16 16h16M16 24h16M16 32h10"/>',
    audio: '<path d="M8 24v0M14 16v16M20 8v32M26 14v20M32 18v12M38 22v4"/>',
    video: '<rect x="6" y="10" width="36" height="28" rx="5"/><path d="M20 18l12 6-12 6z"/>',
    texto: '<path d="M10 12h28M24 12v26M17 38h14"/>',
    imagen: '<rect x="6" y="8" width="36" height="32" rx="5"/><circle cx="17" cy="19" r="4"/><path d="M8 36l11-10 8 7 6-5 9 8"/>',
    resumen: '<path d="M10 12h28M10 20h28M10 28h18M10 36h12"/>',
    tarjetas: '<rect x="6" y="16" width="30" height="22" rx="4"/><path d="M12 9h30v22"/>',
    cuest: '<circle cx="24" cy="24" r="16"/><path d="M16 24l6 6 11-12"/>',
    guia: '<path d="M8 10c6-3 11-3 16 1v28c-5-4-10-4-16-1zM40 10c-6-3-11-3-16 1v28c5-4 10-4 16-1z"/>',
    chat: '<path d="M8 12h32v20H22l-8 7v-7H8z"/>',
    reloj: '<circle cx="24" cy="24" r="17"/><path d="M24 13v11l8 5"/>',
    escudo: '<path d="M24 6l15 5v12c0 10-7 16-15 19C16 39 9 33 9 23V11z"/><path d="M17 24l5 5 9-10"/>',
    candado: '<rect x="10" y="21" width="28" height="20" rx="5"/><path d="M16 21v-6a8 8 0 0116 0v6"/>',
    globo: '<circle cx="24" cy="24" r="17"/><path d="M7 24h34M24 7c-8 9-8 25 0 34M24 7c8 9 8 25 0 34"/>',
    gorro: '<path d="M4 18l20-9 20 9-20 9z"/><path d="M12 22v10c4 4 20 4 24 0V22"/>',
    persona: '<circle cx="24" cy="15" r="8"/><path d="M8 41c1-9 8-14 16-14s15 5 16 14"/>',
    edificio: '<rect x="10" y="6" width="28" height="36" rx="3"/><path d="M17 14h4M27 14h4M17 22h4M27 22h4M17 30h4M27 30h4M21 42v-6h6v6"/>',
    calendario: '<rect x="7" y="10" width="34" height="31" rx="5"/><path d="M7 20h34M16 6v8M32 6v8"/>',
    ojo: '<path d="M4 24c5-9 12-14 20-14s15 5 20 14c-5 9-12 14-20 14S9 33 4 24z"/><circle cx="24" cy="24" r="6"/>',
    cerebro: '<path d="M18 8a7 7 0 00-7 7 6 6 0 00-3 10 6 6 0 004 9 7 7 0 0013 2V10a5 5 0 00-7-2zM30 8a7 7 0 017 7 6 6 0 013 10 6 6 0 01-4 9 7 7 0 01-13 2"/>',
    check: '<path d="M10 25l9 9 19-20"/>',
    equis: '<path d="M12 12l24 24M36 12L12 36"/>',
    enlace: '<path d="M20 28a7 7 0 0010 0l6-6a7 7 0 00-10-10l-2 2M28 20a7 7 0 00-10 0l-6 6a7 7 0 0010 10l2-2"/>',
    youtube: '<rect x="4" y="10" width="40" height="28" rx="9"/><path d="M20 18l11 6-11 6z"/>',
    rayo: '<path d="M26 4L10 27h12l-2 17 18-25H26z"/>',
    carpeta: '<path d="M6 12h13l4 5h19v23H6z"/>'
  };
  const svg = (key, size, extra) => '<svg class="ac-ico" viewBox="0 0 48 48" width="' + size + '" height="' + size + '" ' + (extra || "") + '>' + ICON[key] + '</svg>';

  const bez = (p, t) => { const u = 1 - t; return { x: u*u*u*p[0] + 3*u*u*t*p[2] + 3*u*t*t*p[4] + t*t*t*p[6], y: u*u*u*p[1] + 3*u*u*t*p[3] + 3*u*t*t*p[5] + t*t*t*p[7] }; };
  const pathD = (p) => "M" + p[0] + " " + p[1] + " C" + p[2] + " " + p[3] + " " + p[4] + " " + p[5] + " " + p[6] + " " + p[7];

  // Dibuja un trayecto (en un <svg class="ac-links">) y lo revela con trazo progresivo en el tiempo t
  function link(tl, svgEl, p, t, dur, color, id) {
    const e = document.createElementNS("http://www.w3.org/2000/svg", "path");
    e.setAttribute("d", pathD(p)); e.setAttribute("fill", "none"); e.setAttribute("stroke", color || "#bcd6ff");
    e.setAttribute("stroke-width", "3"); e.setAttribute("stroke-linecap", "round"); e.setAttribute("pathLength", "1");
    e.setAttribute("stroke-dasharray", "1"); e.setAttribute("stroke-dashoffset", "1"); e.setAttribute("opacity", ".6");
    if (id) e.id = id; svgEl.appendChild(e);
    tl.to(e, { strokeDashoffset: 0, duration: dur || .9, ease: "power2.inOut" }, t);
    return e;
  }
  // Paquete de luz que recorre el trayecto p entre start y start+dur (sale del DOM de 'parent')
  function packet(tl, parent, p, start, dur, ease) {
    const d = document.createElement("div"); d.className = "ac-pk"; parent.appendChild(d);
    const pr = { t: 0 };
    tl.set(d, { opacity: 1 }, start);
    tl.to(pr, { t: 1, duration: dur, ease: ease || "power1.inOut", onUpdate: () => { const b = bez(p, pr.t); d.style.left = b.x + "px"; d.style.top = b.y + "px"; } }, start);
    tl.set(d, { opacity: 0 }, start + dur);
    return d;
  }
  // Titulo: lineas con palabras que suben desde una mascara
  const showLn = (tl, sel, t) => tl.fromTo(sel + " .w", { yPercent: 115 }, { yPercent: 0, duration: .7, ease: "power4.out", stagger: .09 }, t);
  const hideLn = (tl, sel, t) => tl.to(sel + " .w", { yPercent: -115, duration: .45, ease: "power3.in", stagger: .04 }, t);
  // Aparece la linea (contenedor) y despues sus palabras; la oculta al terminar
  function line(tl, sel, tIn, tOut) {
    tl.set(sel, { opacity: 1 }, tIn - 0.001); showLn(tl, sel, tIn);
    if (tOut != null) { hideLn(tl, sel, tOut); tl.set(sel, { opacity: 0 }, tOut + .7); }
  }
  // Generador pseudoaleatorio con semilla
  const seeded = (a) => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

  return { T, scene, block, ins, icue, insDur, cue, cueEnd, blockStart, blockEnd, sceneDur, ICON, svg, bez, pathD, link, packet, showLn, hideLn, line, seeded, norm };
})();
