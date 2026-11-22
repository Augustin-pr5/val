/*
 * ink.js — outils partagés par toutes les scènes de la bande-annonce.
 * Traits d'encre qui se dessinent, karaoké mot à mot, surlignage au marqueur,
 * écriture « à la plume ». Tout est fonction du temps de la timeline (aucune horloge).
 *
 * Formes déclaratives : un <path> porte data-shape et ses paramètres ; INK.shapes(racine)
 * calcule son attribut d. Exemples :
 *   <path data-shape="circle" data-c="400,300" data-r="120,90" data-seed="3" data-a0="-115"> (data-a0 = angle de départ)
 *   <path data-shape="line"   data-p="100,200,800,240" data-bow="30" data-seed="5">
 *   <path data-shape="spiral" data-c="960,540" data-r="20,300" data-turns="3.2">
 *   <path data-shape="strike" data-p="100,200,900,180" data-seed="2">   (rature)
 */
(function () {
  if (window.INK) return;
  var INK = {};
  INK.C = { papier: '#F5F1E8', encre: '#161412', gris: '#B8B2A7', cire: '#B3261E' };

  // ---------- hasard reproductible ----------
  INK.rng = function (seed) {
    var a = (seed >>> 0) || 1;
    return function () {
      a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  function noise1(r, n) {
    var v = [];
    for (var i = 0; i < n; i++) v.push(r() * 2 - 1);
    return function (t) {
      var x = Math.max(0, Math.min(1, t)) * (n - 1), i = Math.floor(x), f = x - i;
      var a = v[i], b = v[Math.min(n - 1, i + 1)], s = f * f * (3 - 2 * f);
      return a + (b - a) * s;
    };
  }
  function nums(s) { return String(s || '').split(',').map(Number); }
  function f1(x) { return Math.round(x * 10) / 10; }

  // Catmull-Rom → courbes de Bézier (tracé lisse passant par les points)
  INK.smooth = function (pts) {
    if (pts.length < 2) return '';
    var d = 'M' + f1(pts[0][0]) + ' ' + f1(pts[0][1]);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
      d += ' C' + f1(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + f1(p1[1] + (p2[1] - p0[1]) / 6) + ' ' +
        f1(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + f1(p2[1] - (p3[1] - p1[1]) / 6) + ' ' + f1(p2[0]) + ' ' + f1(p2[1]);
    }
    return d;
  };

  // Cercle tracé à la main : il ne se referme pas parfaitement (léger dépassement)
  INK.circle = function (cx, cy, rx, ry, o) {
    o = o || {};
    var r = INK.rng(o.seed || 1), nz = noise1(r, 7), N = o.n || 56;
    var a0 = (o.start != null ? o.start : -115) * Math.PI / 180;
    var sw = (o.sweep != null ? o.sweep : 378) * Math.PI / 180;
    var wob = o.wobble != null ? o.wobble : 0.045, drift = o.drift != null ? o.drift : 0.05;
    var pts = [];
    for (var i = 0; i <= N; i++) {
      var t = i / N, a = a0 + sw * t, k = 1 + wob * nz(t) + drift * (t - 0.5);
      pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
    }
    return INK.smooth(pts);
  };

  // Ligne tremblée avec un léger arc (bow) perpendiculaire
  INK.line = function (x1, y1, x2, y2, o) { return INK.smooth(INK.linePts(x1, y1, x2, y2, o)); };
  INK.linePts = function (x1, y1, x2, y2, o) {
    o = o || {};
    var r = INK.rng(o.seed || 1), nz = noise1(r, 6), N = o.n || 16;
    var dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    var bow = o.bow || 0, wob = o.wobble != null ? o.wobble : Math.min(6, L * 0.008), pts = [];
    for (var i = 0; i <= N; i++) {
      var t = i / N, off = bow * Math.sin(Math.PI * t) + wob * nz(t);
      pts.push([x1 + dx * t + nx * off, y1 + dy * t + ny * off]);
    }
    return pts;
  };
  // Fait voyager un élément (le point rouge) le long de points, de t à t+dur
  INK.travel = function (tl, el, pts, t, dur, ease) {
    tl.set(el, { x: pts[0][0], y: pts[0][1] }, 0);
    tl.to(el, { keyframes: { x: pts.map(function (p) { return p[0]; }), y: pts.map(function (p) { return p[1]; }), easeEach: 'none' },
      duration: dur, ease: ease || 'power2.inOut' }, t);
  };

  // Spirale (du centre vers l'extérieur)
  INK.spiral = function (cx, cy, r0, r1, turns, o) {
    o = o || {};
    var r = INK.rng(o.seed || 1), nz = noise1(r, 9), N = Math.max(40, Math.round(turns * 36)), pts = [];
    var a0 = (o.start || 0) * Math.PI / 180, dir = o.ccw ? -1 : 1;
    for (var i = 0; i <= N; i++) {
      var t = i / N, a = a0 + dir * turns * 2 * Math.PI * t, rr = (r0 + (r1 - r0) * t) * (1 + 0.04 * nz(t));
      pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * (o.squash || 1)]);
    }
    return INK.smooth(pts);
  };

  // Rature : un trait vif, un peu courbé, qui déborde des deux côtés
  INK.strike = function (x1, y1, x2, y2, o) {
    o = o || {};
    return INK.line(x1, y1, x2, y2, { seed: o.seed || 7, bow: o.bow != null ? o.bow : -10, wobble: 3, n: 10 });
  };

  INK.shapes = function (root) {
    var els = (root || document).querySelectorAll('[data-shape]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], s = el.dataset, seed = +s.seed || i + 1, d = '';
      if (s.shape === 'circle') { var c = nums(s.c), rr = nums(s.r); d = INK.circle(c[0], c[1], rr[0], rr[1] || rr[0], { seed: seed, start: s.a0 != null ? +s.a0 : null, sweep: s.sweep != null ? +s.sweep : null, wobble: s.wobble != null ? +s.wobble : null }); }
      else if (s.shape === 'line') { var p = nums(s.p); d = INK.line(p[0], p[1], p[2], p[3], { seed: seed, bow: +s.bow || 0, wobble: s.wobble != null ? +s.wobble : null }); }
      else if (s.shape === 'spiral') { var c2 = nums(s.c), r2 = nums(s.r); d = INK.spiral(c2[0], c2[1], r2[0], r2[1], +s.turns || 3, { seed: seed, start: +s.a0 || 0, ccw: s.ccw === '1', squash: +s.squash || 1 }); }
      else if (s.shape === 'strike') { var p2 = nums(s.p); d = INK.strike(p2[0], p2[1], p2[2], p2[3], { seed: seed, bow: s.bow != null ? +s.bow : null }); }
      if (d) el.setAttribute('d', d);
      el.setAttribute('pathLength', '1000');
    }
  };

  // ---------- animation ----------
  // Dessine un tracé (pathLength="1000") de t à t+dur. Invisible avant t.
  // (longueur normalisée à 1000 : GSAP arrondit stroke-dashoffset au pixel entier)
  INK.draw = function (tl, el, t, dur, ease) {
    tl.set(el, { opacity: 0, strokeDasharray: '1000 2000', strokeDashoffset: 1000 }, 0);
    tl.set(el, { opacity: 1 }, t);
    tl.fromTo(el, { strokeDashoffset: 1000 }, { strokeDashoffset: 0, duration: dur, ease: ease || 'power2.inOut' }, t);
  };
  // Efface un tracé dans le sens du dessin
  INK.undraw = function (tl, el, t, dur, ease) {
    tl.fromTo(el, { strokeDashoffset: 0 }, { strokeDashoffset: -1000, duration: dur, ease: ease || 'power2.in', immediateRender: false }, t);
  };

  // Mots de la transcription (words.json → window.WORDS = [[texte, début, fin, scène, phrase], …])
  INK.words = function (scene, phrase) {
    return (window.WORDS || []).filter(function (w) { return w[3] === scene && (phrase == null || w[4] === phrase); });
  };

  // Karaoké : chaque .kw passe du gris à l'encre au moment exact où il est dit.
  // data-w = index du mot dans la phrase (0, 1, 2…). sceneStart = début absolu de la scène.
  INK.karaoke = function (tl, els, words, sceneStart, o) {
    o = o || {};
    var grey = o.grey || INK.C.gris, ink = o.ink || INK.C.encre, lead = o.lead != null ? o.lead : 0.02;
    for (var i = 0; i < els.length; i++) {
      var w = words[+els[i].dataset.w];
      if (!w) continue;
      tl.fromTo(els[i], { color: grey }, { color: ink, duration: 0.1, ease: 'none' }, Math.max(0, w[1] - sceneStart - lead));
    }
  };
  INK.wordTime = function (words, i, sceneStart) { return words[i][1] - sceneStart; };

  // Surlignage au marqueur rouge : l'élément .mk balaie de gauche à droite en 0,3 s
  INK.highlight = function (tl, mk, t, dur) {
    tl.fromTo(mk, { clipPath: 'inset(-10% 100% -10% 0%)' }, { clipPath: 'inset(-10% 0% -10% 0%)', duration: dur || 0.3, ease: 'power1.inOut' }, t);
  };

  // Écriture à la plume : la ligne se révèle de gauche à droite, la plume suit le bord.
  INK.write = function (tl, line, t, dur, nib) {
    tl.fromTo(line, { clipPath: 'inset(-30% 100% -30% -2%)' }, { clipPath: 'inset(-30% 0% -30% -2%)', duration: dur, ease: 'none' }, t);
    if (nib) {
      var w = line.offsetWidth, x0 = line.offsetLeft, y0 = line.offsetTop + line.offsetHeight * 0.62;
      tl.set(nib, { opacity: 1 }, t);
      tl.fromTo(nib, { x: x0, y: y0 }, { x: x0 + w, y: y0, duration: dur, ease: 'none' }, t);
      // petit va-et-vient vertical de la plume (fini, déterministe)
      var steps = Math.max(2, Math.round(dur / 0.09));
      for (var k = 0; k < steps; k++) {
        tl.to(nib, { yPercent: (k % 2 ? -1 : 1) * 60, duration: dur / steps, ease: 'sine.inOut' }, t + k * dur / steps);
      }
      tl.set(nib, { opacity: 0, yPercent: 0 }, t + dur + 0.05);
    }
  };

  // Charge les polices avant toute mesure de mise en page
  INK.fontsReady = function (specs) {
    return Promise.all((specs || []).map(function (s) { return document.fonts.load(s); })).then(function () { return document.fonts.ready; });
  };

  window.INK = INK;
})();
