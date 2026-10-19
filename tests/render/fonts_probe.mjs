// fonts_probe.mjs: the Chromium half of test A7 (build plan WP-04). Renders probe items twice, with the fonts served ("loaded") and with
// every /vendor/fonts request aborted ("blocked"), and screenshots each item box. Python (run_checks.py) does the ink comparison.
//
//   node tests/render/fonts_probe.mjs --plan plan.json --out DIR [--dir pipeline] [--mount /vendor=vendor] [--page scenes/testcard/fonts.html]
//   plan.json: {"items":[{"id","text","family","px","weight","lang"}], "extra_mounts":[{"prefix":"/x","dir":"..."}], "query":"&lock=/x/libs.lock.json"}
// Prints one JSON object {chromium, loaded:[...], blocked:[...]} to stdout. Network is off exactly as in render.mjs (only 127.0.0.1:port).
import fs from 'node:fs';
import path from 'node:path';
import { buildRoots, startServer, CHROMIUM_FLAGS, loadPlaywright, chromiumExecutable } from '../../pipeline/bin/render.mjs';

const arg = (n, d) => { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; };
const mounts = []; process.argv.forEach((a, i) => { if (a === '--mount') { const m = /^(\/[^=]*)=(.+)$/.exec(process.argv[i + 1]); if (m) mounts.push({ prefix: m[1], dir: m[2] }); } });
const plan = JSON.parse(fs.readFileSync(arg('plan'), 'utf8'));
const out = arg('out');
const page0 = arg('page', 'scenes/testcard/fonts.html');
const roots = buildRoots({ dir: arg('dir', 'pipeline'), mounts: [...(mounts.length ? mounts : [{ prefix: '/vendor', dir: 'vendor' }]), ...(plan.extra_mounts || [])] });
const srv = await startServer({ roots });
const pw = loadPlaywright();
const browser = await pw.chromium.launch({ executablePath: chromiumExecutable(), args: CHROMIUM_FLAGS, headless: true });
const result = { chromium: browser.version(), loaded: null, blocked: null };
try {
  for (const mode of ['loaded', 'blocked']) {
    const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1, locale: 'en-US', timezoneId: 'UTC', serviceWorkers: 'block' });
    const outside = [];
    await ctx.route('**/*', (route) => {
      const u = new URL(route.request().url());
      if (u.hostname !== '127.0.0.1' || u.port !== String(srv.port)) { outside.push(u.href); return route.abort(); }
      if (mode === 'blocked' && u.pathname.includes('/fonts/')) return route.abort('blockedbyclient');
      return route.continue();
    });
    const page = await ctx.newPage();
    const errors = []; page.on('pageerror', (e) => errors.push(String(e.message)));
    await page.goto(`http://127.0.0.1:${srv.port}/${page0}?probe=1${plan.query || ''}`, { waitUntil: 'load' });
    await page.waitForFunction(() => window.ready === true || window.readyError, null, { timeout: 30000 });
    const readyError = await page.evaluate(() => window.readyError || null);
    if (readyError) throw new Error(`fonts page not ready (${mode}): ${readyError}`);
    const rep = await page.evaluate((items) => window.probe(items), plan.items);
    fs.mkdirSync(path.join(out, mode), { recursive: true });
    for (const r of rep) {
      await page.screenshot({ path: path.join(out, mode, `${r.id}.png`), type: 'png', fullPage: true, clip: { x: r.rect.x, y: r.rect.y, width: r.rect.width, height: r.rect.height } });
    }
    result[mode] = { items: rep, outside_requests: outside, page_errors: errors };
    await ctx.close();
  }
} finally {
  await browser.close(); await srv.close();
}
console.log(JSON.stringify(result));
process.exit(0);
