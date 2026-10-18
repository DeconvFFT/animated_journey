// Round 2: the SHORTCUT to avoid. Record a running CSS animation to video with Playwright's real-time recorder (recordVideo), then conform to 24 fps.
// Usage: node css_record_video.js OUTDIR STILL.png [PLAYWRIGHT_CORE_MODULE_DIR] [CHROMIUM_EXE]   -> OUTDIR/raw.webm (and prints the file name)
// The page runs a 4% push over 3.958 s with the Web Animations API and CSS easeInOutSine (cubic-bezier(0.37, 0, 0.63, 1)), starting after a 0.5 s hold.
// Then: ffmpeg -i raw.webm -vf fps=24 -c:v libx264 -crf 14 out.mp4  and  python3 -I mo8_audit.py out.mp4  (the audit sees the lead-in hold and any dropped frames).
const fs = require('fs'), path = require('path');
const [outdir, still, pwDir, exe] = process.argv.slice(2);
const { chromium } = require(pwDir || '/opt/node-tools/node_modules/playwright-core');
(async () => {
  fs.mkdirSync(outdir, { recursive: true });
  const html = `<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#000;overflow:hidden}#s{width:1920px;height:1080px;overflow:hidden}
  #p{width:1920px;height:1080px;transform-origin:50% 50%;will-change:transform}</style><div id="s"><img id="p" src="file://${path.resolve(still)}"></div>`;
  const hp = path.join(outdir, '_page.html'); fs.writeFileSync(hp, html);
  const browser = await chromium.launch({ headless: true, executablePath: exe || undefined, args: ['--force-device-scale-factor=1'] });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1, recordVideo: { dir: outdir, size: { width: 1920, height: 1080 } } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(hp));
  await page.evaluate(() => document.getElementById('p').decode());
  await page.waitForTimeout(500);
  await page.evaluate(() => { document.getElementById('p').animate([{ transform: 'scale(1)' }, { transform: 'scale(1.04)' }], { duration: 3958, easing: 'cubic-bezier(0.37, 0, 0.63, 1)', fill: 'forwards' }); });
  await page.waitForTimeout(4600);
  const v = page.video();
  await ctx.close(); await browser.close();
  const p = await v.path(); fs.renameSync(p, path.join(outdir, 'raw.webm')); fs.unlinkSync(hp);
  console.log(path.join(outdir, 'raw.webm'));
})().catch(e => { console.error(e); process.exit(1); });
