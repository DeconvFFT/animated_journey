/* common.js: helpers shared by the test-card scenes (scene.html, fonts.html, flat.html, smoke3d.html).
 * Style-neutral: geometry, digits, grids, gradients. No deity, symbol or devotional text anywhere (D-28, build plan 4.10).
 * A scene built on this file obeys the Route A contract: window.seekTo(t) is a PURE function of t,
 * window.ready = true when fonts are loaded, window.readyError = "why" if it cannot be.
 * Nothing here uses Math.random or Date.now; the two variants that need them say so (?random=1).
 * Everything is fetched from the same local server (/lib/libs.lock.json, /phone/test_strings.json, /vendor/...):
 * run with  --dir pipeline --mount /vendor=vendor, or point ?lock= and ?strings= at other URL paths. */
(function () {
  'use strict';
  var LJ = (window.LJ = {});
  LJ.q = new URLSearchParams(location.search);
  LJ.FPS = 24;
  LJ.vendor = LJ.q.get('vendor') || '/vendor';
  LJ.lockUrl = LJ.q.get('lock') || '/lib/libs.lock.json';
  LJ.stringsUrl = LJ.q.get('strings') || '/phone/test_strings.json';
  LJ.LANG = { latin: 'en', devanagari: 'hi', tamil: 'ta', telugu: 'te', kannada: 'kn', malayalam: 'ml', bengali: 'bn', gujarati: 'gu' };

  /* cosine in-out ease: 0 -> 1, zero slope at both ends (the same curve as GSAP "sine.inOut") */
  LJ.ease = function (u) { u = u < 0 ? 0 : (u > 1 ? 1 : u); return 0.5 - 0.5 * Math.cos(Math.PI * u); };

  /* seeded 32-bit linear congruential generator (Numerical Recipes constants); returns floats in [0, 1) */
  LJ.lcg = function (seed) {
    var s = seed >>> 0;
    return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  };

  LJ.pad = function (n, w) { var s = String(n); while (s.length < w) { s = '0' + s; } return s; };

  LJ.json = function (url) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) { throw new Error(url + ' answered ' + r.status); }
      return r.json();
    });
  };

  LJ.script = function (url) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = url; s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error('script failed to load: ' + url)); };
      document.head.appendChild(s);
    });
  };

  /* an error the harness can see: readyError stops the wait at once, the async throw is a page error */
  LJ.fail = function (err) {
    window.readyError = String(err && err.message ? err.message : err);
    setTimeout(function () { throw err instanceof Error ? err : new Error(window.readyError); }, 0);
  };

  /* @font-face rules for every fetched font in libs.lock.json (faces[] with woff2 files and the package's unicode-range) */
  LJ.fontFaceCss = function (lock) {
    var css = [];
    (lock.fonts || []).forEach(function (f) {
      (f.faces || []).forEach(function (face) {
        if (!face.files || !face.files.woff2) { return; }
        css.push("@font-face{font-family:'" + f.family + "';font-style:" + face.style + ';font-weight:' + face.weight +
          ';font-display:block;src:url(' + LJ.vendor + '/' + face.files.woff2.to + ") format('woff2');" +
          (face.unicode_range ? 'unicode-range:' + face.unicode_range + ';' : '') + '}');
      });
    });
    return css.join('\n');
  };
  LJ.installFonts = function (lock) {
    var st = document.createElement('style');
    st.id = 'lj-fonts'; st.textContent = LJ.fontFaceCss(lock);
    document.head.appendChild(st);
  };

  /* the family that carries a script's glyphs: the fetched libs.lock.json font with role script_family for that script */
  LJ.scriptFamily = function (lock, script) {
    var hit = null;
    (lock.fonts || []).forEach(function (f) {
      if (!hit && f.role === 'script_family' && f.faces && f.scripts.indexOf(script) >= 0) { hit = f.family; }
    });
    return hit;
  };

  /* wait for the faces a list of {family, weight, px, text} needs; never rejects (a blocked font must not hang the page) */
  LJ.loadFonts = function (list) {
    return Promise.allSettled(list.map(function (it) {
      return document.fonts.load((it.weight || 400) + ' ' + (it.px || 32) + 'px "' + it.family + '"', it.text || '');
    })).then(function (res) { return res.map(function (r) { return r.status; }); });
  };

  /* Fine-detail texture drawn from a seeded LCG ("16-bit look"): smooth value noise in three octaves, posterised to 10 levels per channel
   * and expanded the way 5-6-5 bit video hardware did, then 600 crisp hairlines and dots and a 2-unit frame. The smooth contours give an
   * image-motion estimator something to lock on to (a fully random speckle, or fine converging lines near the pixel grid, measure noisy
   * even when the push is perfect: tried and dropped); the crisp detail checks downscale sharpness. Positions use normalised units and
   * sizes scale with the canvas, so the 960x540 card panel and the full-frame ?view=detail panel show the same picture at 1x and 2x. */
  LJ.drawTexture = function (cv, rand) {
    var W = cv.width, H = cv.height, k = W / 1920, g = cv.getContext('2d', { alpha: false });
    var N = 256, tab = new Float32Array(N * N * 3), i, j, c, L = 10, scales = [240, 90, 36], wts = [0.6, 0.3, 0.1], off = [0, 37, 71];
    for (i = 0; i < tab.length; i++) { tab[i] = rand(); }
    function lat(ix, iy, ch) { return tab[(((iy & 255) * N) + (ix & 255)) * 3 + ch]; }
    function noise(x, y, ch) {
      var ix = Math.floor(x), iy = Math.floor(y), fx = x - ix, fy = y - iy;
      fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy);
      var a = lat(ix, iy, ch), b = lat(ix + 1, iy, ch), e = lat(ix, iy + 1, ch), d = lat(ix + 1, iy + 1, ch);
      return a + (b - a) * fx + (e - a) * fy + (a - b - e + d) * fx * fy;
    }
    var img = g.createImageData(W, H), data = img.data;
    var r8 = [], g8 = [];                                           /* level -> 8-bit value through a 5-bit (r, b) and 6-bit (g) grid */
    for (i = 0; i < L; i++) {
      var r5 = 3 + Math.round(i * (24 / (L - 1))), g6 = 6 + Math.round(i * (50 / (L - 1)));
      r8.push((r5 << 3) | (r5 >> 2)); g8.push((g6 << 2) | (g6 >> 4));
    }
    for (var y = 0; y < H; y++) {
      for (var x = 0; x < W; x++) {
        var o = (y * W + x) * 4;
        for (c = 0; c < 3; c++) {
          var v = 0;
          for (j = 0; j < scales.length; j++) { v += wts[j] * noise((x / k + off[c] * 7) / scales[j], (y / k + off[c] * 3) / scales[j], c); }
          var q = Math.min(L - 1, Math.floor(v * L));
          data[o + c] = c === 1 ? g8[q] : r8[q];
        }
        data[o + 3] = 255;
      }
    }
    g.putImageData(img, 0, 0);
    var pal = ['rgb(240,240,240)', 'rgb(18,18,18)', 'rgb(227,179,65)', 'rgb(74,163,162)', 'rgb(200,85,61)'];
    for (i = 0; i < 600; i++) {                                     /* crisp hairlines and dots */
      var x0 = rand() * W, y0 = rand() * H, kind = rand(), col = pal[Math.floor(rand() * pal.length)];
      if (kind < 0.5) {
        var a = rand() * Math.PI, len = (10 + rand() * 40) * k;
        g.strokeStyle = col; g.lineWidth = k; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x0 + Math.cos(a) * len, y0 + Math.sin(a) * len); g.stroke();
      } else { var d = (2 + Math.floor(rand() * 3)) * k; g.fillStyle = col; g.fillRect(x0, y0, d, d); }
    }
    g.strokeStyle = 'rgb(235,235,235)'; g.lineWidth = 2 * k; g.strokeRect(k, k, W - 2 * k, H - 2 * k);
  };
})();
