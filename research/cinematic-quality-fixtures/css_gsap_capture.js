// Round 2: record a CSS / GSAP push-in to numbered PNG frames by STEPPING the animation (not by real-time screen recording).
// Usage:  node css_gsap_capture.js MODE OUTDIR STILL.png GSAP.min.js [FRAMES=96] [FPS=24] [AMOUNT=0.04] [PLAYWRIGHT_CORE_MODULE_DIR] [CHROMIUM_EXE]
// MODE:   css_wc        style.transform = scale(s) set per frame, will-change: transform (compositor layer)
//         css_nowc      same, no will-change
//         gsap_wc       gsap.timeline paused, ease "sine.inOut", tl.time(i/FPS) per frame, will-change: transform
//         gsap_force3d  gsap with force3D:true (translate3d + scale), no will-change
//         gsap_proxy    gsap only supplies the ease: a proxy number is tweened and onUpdate writes style.transform = scale(1+AMT*p) at full float precision
//         css_layout    NEGATIVE CONTROL: animate width/height/left/top (layout) instead of transform
// The still is shown at 1920x1080 CSS px (a 4K still is therefore down-scaled 2:1 at rest), transform-origin centre.
// Cosine in-out (GSAP "sine.inOut" = 0.5-0.5cos(pi u)); the last frame reaches the end value (duration (FRAMES-1)/FPS), as in zoompan_vs_subpixel_prints.py.
// Needs playwright-core (any 1.5x) and a Chromium/headless-shell build; headless, deviceScaleFactor 1, 1920x1080 viewport.
const fs = require('fs'), path = require('path');
const [mode, outdir, still, gsapjs, nS, fS, aS, pwDir, exe] = process.argv.slice(2);
const N = parseInt(nS || '96'), FPS = parseFloat(fS || '24'), AMT = parseFloat(aS || '0.04');
const { chromium } = require(pwDir || '/opt/node-tools/node_modules/playwright-core');
(async () => {
  fs.mkdirSync(outdir, { recursive: true });
  const html = `<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#000;overflow:hidden}
  #stage{position:relative;width:1920px;height:1080px;overflow:hidden}
  #pic{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%;${(mode.endsWith('_wc') || mode === 'gsap_proxy') ? 'will-change:transform;' : ''}}
  </style><div id="stage"><img id="pic" src="file://${path.resolve(still)}"></div><script src="file://${path.resolve(gsapjs)}"></script>`;
  const htmlPath = path.join(outdir, '_page.html'); fs.writeFileSync(htmlPath, html);
  const browser = await chromium.launch({ headless: true, executablePath: exe || undefined, args: ['--force-device-scale-factor=1', '--hide-scrollbars'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(htmlPath));
  await page.evaluate(() => document.getElementById('pic').decode());
  if (mode.startsWith('gsap')) {
    await page.evaluate(({ AMT, N, FPS, mode }) => {
      const vars = { scale: 1 + AMT, duration: (N - 1) / FPS, ease: 'sine.inOut' };
      if (mode === 'gsap_force3d') vars.force3D = true;
      if (mode === 'gsap_proxy') {
        const el = document.getElementById('pic'); window.proxy = { p: 0 };
        window.tl = gsap.timeline({ paused: true }).to(window.proxy, { p: 1, duration: (N - 1) / FPS, ease: 'sine.inOut', onUpdate: () => { el.style.transform = `scale(${1 + AMT * window.proxy.p})`; } });
      } else {
        window.tl = gsap.timeline({ paused: true }).fromTo('#pic', { scale: 1 }, vars);
      }
    }, { AMT, N, FPS, mode });
  }
  const rec = [];
  for (let i = 0; i < N; i++) {
    const u = i / (N - 1), s = 1 + AMT * (0.5 - 0.5 * Math.cos(Math.PI * u));
    const applied = await page.evaluate(({ i, s, mode, FPS }) => {
      const el = document.getElementById('pic');
      if (mode === 'css_wc' || mode === 'css_nowc') el.style.transform = `scale(${s})`;
      else if (mode.startsWith('gsap')) window.tl.time(i / FPS, false);
      else if (mode === 'css_layout') {
        el.style.width = (1920 * s) + 'px'; el.style.height = (1080 * s) + 'px';
        el.style.left = (-(1920 * (s - 1)) / 2) + 'px'; el.style.top = (-(1080 * (s - 1)) / 2) + 'px';
      }
      return el.style.transform || (el.style.width + ' ' + el.style.left);
    }, { i, s, mode, FPS });
    await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    await page.screenshot({ path: path.join(outdir, String(i).padStart(3, '0') + '.png'), type: 'png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    if (i === 0 || i === N >> 1 || i === N - 1) rec.push(applied);
  }
  await browser.close();
  fs.unlinkSync(htmlPath);
  console.log(JSON.stringify({ mode, frames: N, applied_style_samples: rec }));
})().catch(e => { console.error(e); process.exit(1); });
