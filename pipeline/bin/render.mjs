#!/usr/bin/env node
// render.mjs: the Route A seek-capture harness (build plan WP-04, research/agent-pipeline.md R7, spike SP2).
//
//   node pipeline/bin/render.mjs --dir pipeline --page scenes/testcard/scene.html --mount /vendor=vendor \
//        --out renders/wp04/a --seconds 2 --json renders/wp04/a.json
//   node pipeline/bin/render.mjs --dir pipeline --page scenes/testcard/scene.html --seconds 2 --chain h264 --ffmpeg renders/wp04/a.mp4
//   node pipeline/bin/render.mjs --help        (full option list; see also pipeline/bin/README-render.md)
//
// THE CONTRACT WITH A SCENE. The page defines window.seekTo(t_seconds): a PURE function of t that sets the picture
// for time t and does nothing else (no Date.now, no Math.random, no animation that runs by itself). It may return a
// promise. The page sets window.ready = true once its fonts and images are loaded (or window.readyError = "why"
// if it cannot). Optional: window.ljReport() returns a JSON-able object that is copied into the --json report.
//
// WHAT IT DOES. Serves --dir (plus every --mount /urlpath=dir) on 127.0.0.1 only; starts headless Chromium with a
// fixed flag set; opens the page; for each frame f of the shard it calls seekTo(f/fps), waits two animation frames,
// takes a PNG screenshot and either writes it as f_000000.png (through .tmp and rename, so a kill never leaves a
// half frame) or pipes it into ffmpeg using a chain from pipeline/lib/chains.json (built-in H.264 default).
// Frames that already exist are skipped (resume); --shard i/n takes every n-th frame (shards never overlap).
//
// WHAT IT NEVER DOES. It never touches a path outside --dir and the --mount folders (a request that tries gets 404),
// never listens on anything but 127.0.0.1, never lets the page reach any other host (every other request is aborted
// and the run exits 2 naming the URL), and never writes outside --out, the --ffmpeg/--video file and the --json file.
//
// EXIT CODES. 0 done (also: --max-seconds soft cap reached, with a resume hint). 1 a check failed (the encoded
// file does not match the chain's expected tags). 2 bad usage, or the scene is broken (network request, scene error,
// missing local asset, or an uncaught page error). 3 environment problem (no Playwright, no Chromium, no ffmpeg, time cap in
// video mode). 130/143 stopped by SIGINT/SIGTERM (finished frames are kept). On exit 2 or 3 the output of THIS run
// is removed (frames it wrote, .tmp files, a partial video) so a broken scene never leaves frames that resume would trust.

import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(HERE, '..', '..');
export const HARNESS_VERSION = '1';

// ---------------------------------------------------------------------------------------------- constants
// Experiments only: PW_EXTRA_FLAGS="--a --b" appends Chromium flags and PW_DROP_FLAGS="--a --b" removes default ones (the report lists the flags
// actually used, so a run is never silently different). The history-independence test uses PW_DROP_FLAGS as its negative control.
const EXTRA_FLAGS = (process.env.PW_EXTRA_FLAGS || '').split(/\s+/).filter(Boolean);
const DROP_FLAGS = (process.env.PW_DROP_FLAGS || '').split(/\s+/).filter(Boolean);
// Deterministic Chromium: fixed scale, no scrollbars, grayscale text with no hinting, sRGB output, software GL for WebGL (SwiftShader, as in R7),
// no throttling of hidden pages, no proxy, and no name resolution except loopback. Two flags remove HISTORY from the pixels (SP2 finding, tested):
//   --disable-partial-raster   Chromium otherwise re-rasterises only the damaged rectangle, so edge pixels of anti-aliased shapes depend on the
//                              previous frame: a flat SVG scene rendered by 1 page and by 4 pages differed in 62 of 96 frames, and a killed
//                              and resumed run did not equal an uninterrupted one;
//   --disable-gpu-compositing  software compositing: the same pixels whatever the frame order, and about 50% faster here than compositing
//                              through SwiftShader Vulkan (the readback was the cost). WebGL still runs on SwiftShader.
export const CHROMIUM_FLAGS = [
  '--force-device-scale-factor=1', '--hide-scrollbars', '--disable-lcd-text', '--font-render-hinting=none',
  '--force-color-profile=srgb',
  '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
  '--disable-partial-raster', '--disable-gpu-compositing',
  '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows',
  '--no-proxy-server', '--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1 , EXCLUDE localhost',
].filter((f) => !DROP_FLAGS.includes(f)).concat(EXTRA_FLAGS);


const H264_VF = 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv';
// Built-in chain: used only when pipeline/lib/chains.json (WP-05) is absent. It mirrors that file's h264_venue entry (the Q-F1 colour line, W-17 venue
// settings); tests/render asserts the two are equal, so the file stays the single source of truth and a drift is caught.
export const BUILTIN_CHAINS = {
  h264: {
    container: 'mp4', ext: '.mp4', vf: H264_VF, alpha: false,
    video_args: ['-c:v', 'libx264', '-profile:v', 'high', '-level', '4.1', '-crf', '18', '-maxrate', '20M', '-bufsize', '40M',
      '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', '-map_metadata', '-1'],
    audio_args: [],
    expect: { codec: 'h264', profile: null, pix_fmt: 'yuv420p', color_range: 'tv', color_space: 'bt709', color_primaries: 'bt709', color_transfer: 'bt709' },
    expect_extra: { profile: 'High' },
    notes: 'built-in default (scale first, then format, then setparams); mirrors h264_venue in chains.json', source: 'built-in',
  },
};
const CHAIN_ALIASES = { h264_venue: 'h264' };   // used only when chains.json is absent or lacks the name

const MIME = {
  '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.ttf': 'font/ttf', '.otf': 'font/otf', '.txt': 'text/plain; charset=utf-8', '.wasm': 'application/wasm', '.glsl': 'text/plain; charset=utf-8',
};

const OPTIONS = {
  page: 'v', dir: 'v', mount: 'vr', out: 'v', fps: 'v', w: 'v', h: 'v', seconds: 'v', frames: 'v', shard: 'v', chain: 'v', ffmpeg: 'v', video: 'v',
  json: 'v', concurrency: 'v', 'max-seconds': 'v', 'ready-timeout': 'v', 'frame-timeout': 'v', 'serve-seconds': 'v', 'chains-file': 'v', 'ffmpeg-bin': 'v',
  alpha: 'f', 'fail-on-pageerror': 'f', serve: 'f', overwrite: 'f', encode: 'f', quiet: 'f', help: 'f', version: 'f', 'list-chains': 'f',
};

const USAGE = `render.mjs ${HARNESS_VERSION}: Route A seek-capture harness (headless Chromium, frames stepped through window.seekTo(t))

  node pipeline/bin/render.mjs --page SCENE.html[?query] [--dir DIR] [--mount /urlpath=dir ...] --out FRAMES_DIR (--seconds S | --frames A:B)
  node pipeline/bin/render.mjs --page SCENE.html --seconds S --chain h264 --ffmpeg OUT.mp4        (frames piped into ffmpeg, no PNGs)

  --page P            scene page, relative to --dir or a mount, query allowed (required)
  --dir DIR           folder served at / (default .)
  --mount /u=DIR      also serve DIR at /u (repeatable); the page can only read --dir and the mounts
  --out DIR           PNG frames f_000000.png, resumable (default frames)
  --fps N             frames per second (default 24)        --w N --h N   viewport (default 1920 1080)
  --seconds S         frames 0..round(S*fps)-1               --frames A:B  frame range [A,B)  (default --seconds 1)
  --shard i/n         render frames with (frame mod n) == i (default 0/1)
  --concurrency N     pages used in parallel, 1 to 8 (default 1)
  --alpha             transparent page background, RGBA frames (the scene must not paint its own background)
  --chain NAME        encode with a chain from pipeline/lib/chains.json, else built-in "h264" (needs --ffmpeg or --video, or writes OUT/video.EXT)
  --ffmpeg OUT / --video OUT   the video file to write (frames are piped; whole shot in one process; no --shard)
  --encode            do not render: pipe the existing PNG frames of --out for the range into the chain (after a sharded run)
  --json FILE         write a report (frames, seconds, fps, peak RSS, Chromium version, chain, frame hashes, errors)
  --max-seconds S     soft cap: stop after the current frame once S seconds have passed, print a resume hint, exit 0 (PNG mode)
  --fail-on-pageerror stop at the first uncaught page error: exit 2 and remove this run's output (default: finish, then exit 2)
  --overwrite         ignore existing frames and a changed-scene fingerprint, render everything again
  --ready-timeout S   wait for window.ready (default 60)      --frame-timeout S   per-frame limit (default 120)
  --serve [--serve-seconds S]   only serve the folders on 127.0.0.1 and print the URL (preview, tests)
  --chains-file F     chain file (default pipeline/lib/chains.json)     --list-chains   print the chains and exit
  --ffmpeg-bin F      ffmpeg program (default env FFMPEG, else ffmpeg)  --quiet   no progress lines
Environment: PW_PATH (playwright module folder), PW_CHROMIUM (browser executable; default /opt/pw-browsers/chromium).
`;

// ---------------------------------------------------------------------------------------------- small helpers
class Exit extends Error { constructor(code, message) { super(message); this.exitCode = code; } }
const fail = (code, message) => { throw new Exit(code, message); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const pad6 = (n) => String(n).padStart(6, '0');

function displayPath(p) {
  if (!p) return null;
  const rel = path.relative(process.cwd(), path.resolve(p));
  return (rel.startsWith('..') || path.isAbsolute(rel)) ? `<outside-cwd>/${path.basename(p)}` : (rel || '.');
}

export function parseArgs(argv) {
  const o = { mount: [] };
  for (let i = 0; i < argv.length; i++) {
    let a = argv[i];
    if (!a.startsWith('--')) fail(2, `unexpected argument "${a}" (options start with --; try --help)`);
    let name = a.slice(2), val;
    const eq = name.indexOf('=');
    if (eq >= 0) { val = name.slice(eq + 1); name = name.slice(0, eq); }
    const kind = OPTIONS[name];
    if (!kind) fail(2, `unknown option --${name} (try --help)`);
    if (kind === 'f') {
      if (val !== undefined) fail(2, `--${name} takes no value`);
      o[name] = true;
    } else {
      if (val === undefined) { if (i + 1 >= argv.length) fail(2, `--${name} needs a value`); val = argv[++i]; }
      if (kind === 'vr') o[name].push(val); else o[name] = val;
    }
  }
  return o;
}

function num(o, name, def, { min = -Infinity, max = Infinity, int = false } = {}) {
  if (o[name] === undefined) return def;
  const s = String(o[name]);
  if (!/^-?\d+(\.\d+)?$/.test(s)) fail(2, `--${name} must be a number, got "${s}"`);
  const v = Number(s);
  if (int && !Number.isInteger(v)) fail(2, `--${name} must be a whole number, got "${s}"`);
  if (v < min || v > max) fail(2, `--${name} must be between ${min} and ${max}, got ${s}`);
  return v;
}

export function normaliseOptions(o) {
  const cfg = {};
  cfg.fps = num(o, 'fps', 24, { min: 0.001, max: 240 });
  cfg.w = num(o, 'w', 1920, { min: 16, max: 8192, int: true });
  cfg.h = num(o, 'h', 1080, { min: 16, max: 8192, int: true });
  cfg.concurrency = num(o, 'concurrency', 1, { min: 1, max: 8, int: true });
  cfg.maxSeconds = num(o, 'max-seconds', 0, { min: 0 });
  cfg.readyTimeout = num(o, 'ready-timeout', 60, { min: 1 }) * 1000;
  cfg.frameTimeout = num(o, 'frame-timeout', 120, { min: 1 }) * 1000;
  cfg.serveSeconds = num(o, 'serve-seconds', 0, { min: 0 });
  if (o.seconds !== undefined && o.frames !== undefined) fail(2, 'give --seconds or --frames, not both');
  if (o.frames !== undefined) {
    const m = /^(\d+):(\d+)$/.exec(String(o.frames));
    if (!m) fail(2, `--frames must look like A:B (frames A up to but not including B), got "${o.frames}"`);
    cfg.range = [Number(m[1]), Number(m[2])];
    if (cfg.range[0] >= cfg.range[1]) fail(2, `--frames ${o.frames}: A must be less than B`);
  } else {
    const secs = num(o, 'seconds', 1, { min: 0.001 });
    cfg.range = [0, Math.max(1, Math.round(secs * cfg.fps))];
  }
  const sm = /^(\d+)\/(\d+)$/.exec(String(o.shard ?? '0/1'));
  if (!sm || Number(sm[2]) < 1 || Number(sm[2]) > 1000 || Number(sm[1]) >= Number(sm[2])) fail(2, `--shard must look like i/n with 0 <= i < n <= 1000, got "${o.shard}"`);
  cfg.shard = [Number(sm[1]), Number(sm[2])];
  cfg.out = o.out ?? 'frames';
  cfg.dir = o.dir ?? '.';
  cfg.alpha = !!o.alpha; cfg.failOnPageError = !!o['fail-on-pageerror']; cfg.overwrite = !!o.overwrite; cfg.quiet = !!o.quiet;
  cfg.encode = !!o.encode; cfg.serve = !!o.serve; cfg.json = o.json; cfg.chain = o.chain;
  cfg.video = o.ffmpeg ?? o.video;
  if (o.ffmpeg !== undefined && o.video !== undefined) fail(2, 'give --ffmpeg or --video, not both');
  cfg.ffmpegBin = o['ffmpeg-bin'] ?? process.env.FFMPEG ?? 'ffmpeg';
  cfg.chainsFile = o['chains-file'] ?? path.join(REPO_ROOT, 'pipeline', 'lib', 'chains.json');
  cfg.page = o.page;
  cfg.mounts = o.mount.map((m) => {
    const mm = /^(\/[^=]*)=(.+)$/.exec(m);
    if (!mm) fail(2, `--mount must look like /urlpath=folder, got "${m}"`);
    return { prefix: mm[1].replace(/\/+$/, ''), dir: mm[2] };
  });
  cfg.videoMode = !!(cfg.chain || cfg.video) && !cfg.serve;
  if (cfg.videoMode && cfg.shard[1] > 1) fail(2, 'video mode needs the whole shot in one process: do not combine --chain/--ffmpeg with --shard (render PNG shards, then run --encode)');
  if (cfg.encode && !cfg.videoMode) cfg.videoMode = true;     // --encode implies the default chain
  return cfg;
}

// ---------------------------------------------------------------------------------------------- static server (fix for F-09)
export function buildRoots({ dir, mounts }) {
  const roots = [];
  const add = (prefix, folder, what) => {
    let real;
    try { real = fs.realpathSync(folder); } catch { fail(2, `${what} folder not found: ${displayPath(folder)}`); }
    if (!fs.statSync(real).isDirectory()) fail(2, `${what} is not a folder: ${displayPath(folder)}`);
    roots.push({ prefix, dir: real });
  };
  add('', dir, '--dir');
  for (const m of mounts) {
    if (m.prefix === '' || m.prefix.split('/').some((s, i) => i > 0 && (s === '' || s === '.' || s === '..'))) fail(2, `--mount path "${m.prefix}" is not a plain /name or /a/b path`);
    add(m.prefix, m.dir, `--mount ${m.prefix}`);
  }
  roots.sort((a, b) => b.prefix.length - a.prefix.length);   // longest prefix wins
  return roots;
}

/** Map a request URL (the raw request line target) to a file inside an allowed root, or a status code. */
export function resolveRequest(roots, rawUrl) {
  const raw = String(rawUrl).split('#')[0].split('?')[0];
  if (!raw.startsWith('/')) return { status: 400 };
  let decoded;
  try { decoded = decodeURIComponent(raw); } catch { return { status: 400 }; }
  if (decoded.includes('\0') || decoded.includes('\\')) return { status: 404 };
  if (decoded.split('/').includes('..')) return { status: 404 };           // /../x and /%2e%2e/x never reach the filesystem
  for (const r of roots) {
    if (r.prefix !== '' && decoded !== r.prefix && !decoded.startsWith(r.prefix + '/')) continue;
    const rel = decoded.slice(r.prefix.length);
    let target = path.resolve(r.dir, '.' + rel);
    if (target !== r.dir && !target.startsWith(r.dir + path.sep)) continue;   // outside this root: try the next, else 404
    let st;
    try { st = fs.statSync(target); } catch { continue; }
    if (st.isDirectory()) { target = path.join(target, 'index.html'); try { st = fs.statSync(target); } catch { continue; } }
    if (!st.isFile()) continue;
    let real;
    try { real = fs.realpathSync(target); } catch { continue; }
    if (real !== r.dir && !real.startsWith(r.dir + path.sep)) continue;       // a symlink must not lead out of the root
    return { status: 200, file: real, url: decoded };
  }
  return { status: 404 };
}

export function startServer({ roots }) {
  const served = new Map();                 // url path -> sha256 of the bytes served (200 only), for the resume fingerprint
  const cache = new Map();                  // file -> {key, hash}
  let port = 0;
  const server = http.createServer((req, res) => {
    const send = (status, body, type) => {
      res.writeHead(status, { 'content-type': type || 'text/plain; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', 'content-length': Buffer.byteLength(body) });
      res.end(req.method === 'HEAD' ? undefined : body);
    };
    try {
      if (req.method !== 'GET' && req.method !== 'HEAD') return send(405, 'method not allowed');
      const host = req.headers.host;
      if (host !== `127.0.0.1:${port}` && host !== `localhost:${port}`) return send(403, 'forbidden host');
      const r = resolveRequest(roots, req.url || '/');
      if (r.status !== 200) return send(r.status, r.status === 400 ? 'bad request' : 'not found');
      fs.readFile(r.file, (e, buf) => {
        if (e) return send(404, 'not found');
        const ext = path.extname(r.file).toLowerCase();
        const st = fs.statSync(r.file);
        const key = `${st.size}:${st.mtimeMs}`;
        let c = cache.get(r.file);
        if (!c || c.key !== key) { c = { key, hash: sha256(buf) }; cache.set(r.file, c); }
        served.set(r.url, c.hash);
        res.writeHead(200, { 'content-type': MIME[ext] || 'application/octet-stream', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff', 'content-length': buf.length });
        res.end(req.method === 'HEAD' ? undefined : buf);
      });
    } catch { try { send(500, 'server error'); } catch { /* socket gone */ } }
  });
  server.on('clientError', (err, sock) => { try { sock.end('HTTP/1.1 400 Bad Request\r\n\r\n'); } catch { /* ignore */ } });
  return new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      port = server.address().port;
      resolve({ server, port, served, close: () => new Promise((r) => { server.close(() => r()); server.closeAllConnections?.(); }) });
    });
  });
}

// ---------------------------------------------------------------------------------------------- chains
export function loadChain(cfg) {
  const name = cfg.chain || 'h264';
  let fromFile = null, fileKey = name;
  if (fs.existsSync(cfg.chainsFile)) {
    let d;
    try { d = JSON.parse(fs.readFileSync(cfg.chainsFile, 'utf8')); } catch (e) { fail(2, `chain file ${displayPath(cfg.chainsFile)} is not valid JSON: ${e.message}`); }
    if (d.schema !== 'lj-chains/1' || typeof d.chains !== 'object' || d.chains === null) fail(2, `chain file ${displayPath(cfg.chainsFile)}: schema must be "lj-chains/1" with a "chains" object`);
    if (!d.chains[name] && name === 'h264' && d.chains.h264_venue) fileKey = 'h264_venue';   // "h264" is the venue chain when the file defines it
    fromFile = d.chains[fileKey];
    if (fromFile) {
      if (typeof fromFile.vf !== 'string' || !Array.isArray(fromFile.video_args) || fromFile.video_args.some((x) => typeof x !== 'string')) fail(2, `chain "${name}" in ${displayPath(cfg.chainsFile)} needs a string "vf" and a "video_args" array of strings`);
    }
  }
  let ch = fromFile ? { ...fromFile, source: fileKey === name ? 'chains.json' : `chains.json:${fileKey}` } : null;
  if (!ch) {
    const b = BUILTIN_CHAINS[name] || BUILTIN_CHAINS[CHAIN_ALIASES[name]];
    if (!b) fail(2, `unknown chain "${name}" (built-in: ${Object.keys(BUILTIN_CHAINS).join(', ')}; chain file: ${fs.existsSync(cfg.chainsFile) ? displayPath(cfg.chainsFile) : 'not present'})`);
    ch = { ...b };
  }
  ch.name = name;
  ch.container = ch.container || 'mp4';
  ch.ext = ch.ext || ({ mp4: '.mp4', mov: '.mov', mkv: '.mkv', matroska: '.mkv' }[ch.container] || `.${ch.container}`);
  ch.audio_args = ch.audio_args || [];
  ch.expect = { ...(ch.expect || {}), ...(ch.expect_extra || {}) };   // expect_extra holds the keys the colour test does not need (for example the H.264 profile name)
  return ch;
}
const MUXER = { mp4: 'mp4', mov: 'mov', mkv: 'matroska', matroska: 'matroska' };

function ffprobeBin(ffmpegBin) {
  if (process.env.FFPROBE) return process.env.FFPROBE;
  const base = path.basename(ffmpegBin);
  return base.startsWith('ffmpeg') ? path.join(path.dirname(ffmpegBin), base.replace('ffmpeg', 'ffprobe')) : 'ffprobe';
}

function probeVideo(file, cfg) {
  const r = spawnSync(ffprobeBin(cfg.ffmpegBin), ['-v', 'error', '-select_streams', 'v:0', '-show_entries',
    'stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,color_range,color_space,color_primaries,color_transfer', '-of', 'json', file], { encoding: 'utf8' });
  if (r.error || r.status !== 0) return { error: (r.error && r.error.message) || r.stderr.trim() || 'ffprobe failed' };
  try { return JSON.parse(r.stdout).streams[0]; } catch { return { error: 'ffprobe output not JSON' }; }
}

// ---------------------------------------------------------------------------------------------- Playwright and Chromium
export function loadPlaywright() {
  const req = createRequire(import.meta.url);
  const cands = [];
  if (process.env.PW_PATH) cands.push(process.env.PW_PATH);
  cands.push('playwright', 'playwright-core', '/opt/node-tools/node_modules/playwright', '/opt/node22/lib/node_modules/playwright');
  for (const c of cands) {
    try {
      const m = req(c);
      if (!m || !m.chromium) continue;
      let version = null;
      try { let d = path.dirname(req.resolve(c)); for (let i = 0; i < 4 && !version; i++, d = path.dirname(d)) { const pj = path.join(d, 'package.json'); if (fs.existsSync(pj)) { const j = JSON.parse(fs.readFileSync(pj, 'utf8')); if (/^playwright/.test(j.name || '')) version = j.version; } } } catch { /* version stays null */ }
      return { chromium: m.chromium, version };
    } catch { /* try the next candidate */ }
  }
  return fail(3, 'Playwright was not found. Set PW_PATH to the playwright module folder (the container has it at /opt/node-tools/node_modules/playwright). Do not run "playwright install".');
}
export function chromiumExecutable() {
  const env = process.env.PW_CHROMIUM;
  if (env) { if (!fs.existsSync(env)) fail(3, `PW_CHROMIUM points to a file that does not exist: ${env}`); return env; }
  return fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
}

// ---------------------------------------------------------------------------------------------- peak RSS sampler (Linux)
function startRssSampler(intervalMs = 400) {
  const peak = { browser_tree: 0, ffmpeg: 0, sum: 0 };
  if (process.platform !== 'linux') return { stop: () => ({ node_mb: Math.round(process.resourceUsage().maxRSS / 1024), browser_tree_mb: null, ffmpeg_mb: null, sum_mb: null, note: 'RSS tree sampling is Linux only' }) };
  const pageKb = 4;
  const kids = (pid) => { try { return fs.readFileSync(`/proc/${pid}/task/${pid}/children`, 'utf8').trim().split(/\s+/).filter(Boolean).map(Number); } catch { return []; } };
  const rssKb = (pid) => { try { const s = fs.readFileSync(`/proc/${pid}/stat`, 'utf8'); const f = s.slice(s.lastIndexOf(')') + 2).split(' '); return { kb: Number(f[21]) * pageKb, comm: s.slice(s.indexOf('(') + 1, s.lastIndexOf(')')) }; } catch { return null; } };
  const tick = () => {
    let br = 0, ff = 0; const stack = kids(process.pid);
    while (stack.length) { const p = stack.pop(); const r = rssKb(p); if (r) { if (/ffmpeg/.test(r.comm)) ff += r.kb; else br += r.kb; } stack.push(...kids(p)); }
    const me = (rssKb(process.pid) || { kb: 0 }).kb;
    peak.browser_tree = Math.max(peak.browser_tree, br); peak.ffmpeg = Math.max(peak.ffmpeg, ff); peak.sum = Math.max(peak.sum, br + ff + me);
  };
  tick();
  const t = setInterval(tick, intervalMs); t.unref();
  return { stop: () => { clearInterval(t); tick(); return { node_mb: Math.round(process.resourceUsage().maxRSS / 1024), browser_tree_mb: Math.round(peak.browser_tree / 1024), ffmpeg_mb: Math.round(peak.ffmpeg / 1024), sum_mb: Math.round(peak.sum / 1024), note: 'RSS counts shared pages in every process, so the sum over-counts' }; } };
}

// ---------------------------------------------------------------------------------------------- PNG validity (resume only trusts whole files)
function validPng(file) {
  try {
    const fd = fs.openSync(file, 'r');
    try {
      const size = fs.fstatSync(fd).size;
      if (size < 67) return false;
      const head = Buffer.alloc(8), tail = Buffer.alloc(12);
      fs.readSync(fd, head, 0, 8, 0); fs.readSync(fd, tail, 0, 12, size - 12);
      return head.equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) && tail.subarray(4, 8).toString('latin1') === 'IEND';
    } finally { fs.closeSync(fd); }
  } catch { return false; }
}

// ---------------------------------------------------------------------------------------------- main
async function main(argv) {
  const o = parseArgs(argv);
  if (o.help) { process.stdout.write(USAGE); return 0; }
  if (o.version) { console.log(`render.mjs ${HARNESS_VERSION}`); return 0; }
  const cfg = normaliseOptions(o);
  const log = (...a) => { if (!cfg.quiet) console.error(...a); };

  if (o['list-chains']) {
    const names = new Set(Object.keys(BUILTIN_CHAINS));
    if (fs.existsSync(cfg.chainsFile)) { try { Object.keys(JSON.parse(fs.readFileSync(cfg.chainsFile, 'utf8')).chains || {}).forEach((n) => names.add(n)); } catch { /* reported by loadChain */ } }
    for (const n of names) { const c = loadChain({ ...cfg, chain: n }); console.log(`${n}\t${c.source}\t${c.container}`); }
    return 0;
  }

  const roots = buildRoots({ dir: cfg.dir, mounts: cfg.mounts });
  const srv = await startServer({ roots });
  const base = `http://127.0.0.1:${srv.port}`;
  try {
    if (cfg.serve) {
      console.log(JSON.stringify({ serving: `${base}/`, roots: roots.map((r) => ({ url: r.prefix || '/', folder: displayPath(r.dir) })) }));
      await new Promise((resolve) => {
        const stop = () => resolve();
        process.once('SIGINT', stop); process.once('SIGTERM', stop);
        if (cfg.serveSeconds > 0) setTimeout(stop, cfg.serveSeconds * 1000).unref?.();
      });
      return 0;
    }
    return await render(cfg, roots, srv, base, log);
  } finally {
    await srv.close();
  }
}

async function render(cfg, roots, srv, base, log) {
  if (!cfg.page) fail(2, '--page is required (try --help)');
  const qi = cfg.page.search(/[?#]/);
  const pagePath = '/' + (qi >= 0 ? cfg.page.slice(0, qi) : cfg.page).replace(/^\/+/, '');
  const pageQuery = qi >= 0 ? cfg.page.slice(qi) : '';
  const rr = resolveRequest(roots, pagePath);
  if (rr.status !== 200) fail(2, `page not found under --dir or a --mount: ${pagePath}`);
  const pageUrl = `${base}${pagePath}${pageQuery}`;

  const [A, B] = cfg.range, [si, sn] = cfg.shard;
  const inShard = []; for (let f = A; f < B; f++) if (f % sn === si) inShard.push(f);
  if (inShard.length === 0) fail(2, `shard ${si}/${sn} has no frames in range ${A}:${B}`);

  // output targets
  const video = cfg.videoMode;
  let chain = null, videoFile = null, videoPartial = null;
  if (video) {
    chain = loadChain(cfg);
    videoFile = cfg.video ?? path.join(cfg.out, `video${chain.ext}`);
    videoPartial = `${videoFile}.partial`;
    if (!cfg.encode && !cfg.alpha && (chain.alpha === true || /^(yuva|gbra|rgba|bgra|argb|abgr)/.test(String(chain.expect && chain.expect.pix_fmt)))) { cfg.alpha = true; log(`render.mjs: chain ${chain.name} expects an alpha pixel format, so --alpha is on`); }
  }
  const framePath = (f) => path.join(cfg.out, `f_${pad6(f)}.png`);

  // report skeleton
  const t0 = Date.now(), tStart = process.hrtime.bigint();
  const bench = process.env.LJ_BENCH_NPROC ? { nproc: Number(process.env.LJ_BENCH_NPROC), load1_start: Number(process.env.LJ_BENCH_LOAD1_START), contaminated: process.env.LJ_BENCH_CONTAMINATED === 'yes' } : null;
  const report = {
    schema: 'lj-render-report/1', harness: HARNESS_VERSION, ok: false, complete: false,
    page: cfg.page, fps: cfg.fps, w: cfg.w, h: cfg.h, alpha: cfg.alpha, range: [A, B], shard: `${si}/${sn}`, concurrency: cfg.concurrency,
    mode: video ? (cfg.encode ? 'encode-existing-frames' : 'video') : 'png',
    out: video ? null : displayPath(cfg.out), video: video ? displayPath(videoFile) : null, chain: chain ? { name: chain.name, source: chain.source, container: chain.container, vf: chain.vf, video_args: chain.video_args } : null,
    frames_in_shard: inShard.length, frames_rendered: 0, frames_skipped_existing: 0, remaining: 0, seconds: 0, seconds_render: 0, throughput_fps: 0,
    peak_rss: null, chromium: null, playwright: null, node: process.version, platform: `${process.platform}-${process.arch}`, cpus: os.cpus().length,
    loadavg_start: os.loadavg().map((x) => Math.round(x * 100) / 100), loadavg_end: null, bench,
    chromium_flags: CHROMIUM_FLAGS, page_errors: [], asset_errors: [], blocked_requests: [], fingerprint: null, scene_report: null,
    frame_sha256: {}, frame_sha256_digest: null, resume_hint: null, error: null, chain_check: null,
  };
  const finishReport = (extra = {}) => {
    Object.assign(report, extra);
    report.seconds = Math.round((Date.now() - t0)) / 1000;
    report.loadavg_end = os.loadavg().map((x) => Math.round(x * 100) / 100);
    const keys = Object.keys(report.frame_sha256).sort((a, b) => a - b);
    report.frame_sha256_digest = keys.length ? sha256(Buffer.from(keys.map((k) => `${k}:${report.frame_sha256[k]}`).join('\n'))) : null;
    if (cfg.json) {
      fs.mkdirSync(path.dirname(path.resolve(cfg.json)), { recursive: true });
      const tmp = `${cfg.json}.tmp`; fs.writeFileSync(tmp, JSON.stringify(report, null, 1) + '\n'); fs.renameSync(tmp, cfg.json);
    }
  };

  // ---- --encode: no browser; existing PNG frames of the range into the chain
  if (cfg.encode) {
    for (let f = A; f < B; f++) if (!validPng(framePath(f))) fail(2, `--encode: frame ${f} is missing or incomplete in ${displayPath(cfg.out)} (render it first; resume skips finished frames)`);
    return await encodeOnly(cfg, chain, videoFile, videoPartial, A, B, framePath, report, finishReport, log);
  }

  if (!video) {
    fs.mkdirSync(cfg.out, { recursive: true });
    for (const f of inShard) { try { fs.unlinkSync(framePath(f) + '.tmp'); } catch { /* none */ } }   // a SIGKILL may have left these (own frames only)
  } else {
    fs.mkdirSync(path.dirname(path.resolve(videoFile)), { recursive: true });
  }

  const pw = loadPlaywright();
  report.playwright = pw.version;
  const exe = chromiumExecutable();

  // ---- run state
  const state = { fatal: null, stop: null, closing: false, written: new Set(), pageErrors: 0 };
  const setFatal = (kind, message, code = 2, extra = {}) => { if (!state.fatal) state.fatal = { kind, message, code, ...extra }; };
  let browser = null, ff = null, ffErr = '', rssSampler = null;
  const pages = [];

  const discardOutput = () => {
    if (video) { try { fs.unlinkSync(videoPartial); } catch { /* none */ } return; }
    for (const f of state.written) { try { fs.unlinkSync(framePath(f)); } catch { /* none */ } }
    for (const f of inShard) { try { fs.unlinkSync(framePath(f) + '.tmp'); } catch { /* none */ } }
  };
  const closeAll = async () => {
    state.closing = true;
    if (ff && ff.exitCode === null) { try { ff.stdin.destroy(); ff.kill('SIGKILL'); } catch { /* gone */ } }
    if (browser) { await Promise.race([browser.close().catch(() => {}), sleep(8000)]); }
  };
  const onSignal = (sig) => { if (!state.fatal) { state.fatal = { kind: 'signal', message: `stopped by ${sig}`, code: sig === 'SIGINT' ? 130 : 143, keep: true }; } };
  process.on('SIGINT', onSignal); process.on('SIGTERM', onSignal);

  try {
    rssSampler = startRssSampler();
    try {
      browser = await pw.chromium.launch({ executablePath: exe, args: CHROMIUM_FLAGS, headless: true, handleSIGINT: false, handleSIGTERM: false, handleSIGHUP: false });
    } catch (e) {
      fail(3, `could not start Chromium (${exe || 'Playwright default'}): ${String(e.message).split('\n')[0]}. Set PW_CHROMIUM to a Chromium executable.`);
    }
    report.chromium = browser.version();
    browser.on('disconnected', () => { if (!state.closing) setFatal('crash', 'the browser process exited unexpectedly'); });
    const context = await browser.newContext({ viewport: { width: cfg.w, height: cfg.h }, deviceScaleFactor: 1, locale: 'en-US', timezoneId: 'UTC', colorScheme: 'light', reducedMotion: 'no-preference', serviceWorkers: 'block', acceptDownloads: false });
    context.setDefaultTimeout(cfg.frameTimeout);

    // network off: only the local server may be reached
    await context.route('**/*', async (route) => {
      const url = route.request().url();
      let local = false;
      try { const u = new URL(url); local = (u.protocol === 'http:' && u.hostname === '127.0.0.1' && u.port === String(srv.port)) || ['data:', 'blob:', 'about:'].includes(u.protocol); } catch { /* not a URL: block */ }
      if (local) { try { await route.continue(); } catch { /* page closed */ } return; }
      report.blocked_requests.push(url);
      setFatal('network', `network access is off: the scene requested ${url} (blocked). A scene must be self-contained: put the file under --dir or a --mount.`);
      try { await route.abort('blockedbyclient'); } catch { /* page closed */ }
    });
    try { await context.routeWebSocket(/.*/, (ws) => { report.blocked_requests.push(ws.url()); setFatal('network', `network access is off: the scene opened a WebSocket to ${ws.url()} (blocked).`); ws.close(); }); } catch { /* older Playwright */ }

    const attach = (page) => {
      page.on('pageerror', (e) => {
        const msg = String(e && e.message || e).split('\n')[0];
        report.page_errors.push(msg); state.pageErrors++;
        log(`[page error] ${msg}`);
        if (cfg.failOnPageError) setFatal('pageerror', `uncaught page error: ${msg}`);
      });
      page.on('console', (m) => { if (m.type() === 'error') log(`[console.error] ${m.text().split('\n')[0]}`); });
      page.on('crash', () => setFatal('crash', 'the page crashed'));
      page.on('response', (r) => {
        const u = r.url();
        if (u.startsWith(base) && r.status() >= 400 && !u.endsWith('/favicon.ico')) {
          const p = new URL(u).pathname; report.asset_errors.push({ url: p, status: r.status() });
          const hint = p.startsWith('/vendor/') ? ' (run bash pipeline/lib/fetch_libs.sh)' : '';
          setFatal('asset', `the scene requested ${p} and got ${r.status()}${hint}`);
        }
      });
    };

    // open the pages, wait for ready
    for (let i = 0; i < cfg.concurrency; i++) { const p = await context.newPage(); attach(p); pages.push(p); }
    await Promise.all(pages.map(async (p) => {
      await p.goto(pageUrl, { waitUntil: 'load', timeout: cfg.readyTimeout });
      const deadline = Date.now() + cfg.readyTimeout;
      for (;;) {
        if (state.fatal) return;
        const st = await p.evaluate(() => ({ ready: window.ready === true, err: window.readyError || null, seek: typeof window.seekTo === 'function' }));
        if (st.err) { setFatal('scene', `the scene could not get ready: ${st.err}`); return; }
        if (st.ready) { if (!st.seek) setFatal('scene', 'the page set window.ready but does not define window.seekTo(t)'); break; }
        if (Date.now() > deadline) { setFatal('scene', `window.ready did not become true within ${cfg.readyTimeout / 1000} s`); return; }
        await sleep(25);
      }
      await p.evaluate(() => document.fonts.ready);
    }));
    if (state.fatal) throw new Error('fatal-before-render');

    // fingerprint of the scene: everything the server delivered up to ready, plus the settings that change pixels
    const files = [...srv.served.entries()].sort(([a], [b]) => (a < b ? -1 : 1));
    report.fingerprint = sha256(Buffer.from(JSON.stringify({ v: 1, page: cfg.page, fps: cfg.fps, w: cfg.w, h: cfg.h, alpha: cfg.alpha, files })));

    // resume bookkeeping (PNG mode)
    let todo;
    if (video) {
      todo = inShard.slice();
    } else {
      const metaFile = path.join(cfg.out, '.render-meta.json');
      const meta = { schema: 'lj-render-meta/1', fingerprint: report.fingerprint, page: cfg.page, fps: cfg.fps, w: cfg.w, h: cfg.h, alpha: cfg.alpha };
      let existing = null;
      try { existing = JSON.parse(fs.readFileSync(metaFile, 'utf8')); } catch { existing = null; }
      if (existing && existing.fingerprint !== report.fingerprint && !cfg.overwrite) {
        fail(2, `${displayPath(cfg.out)} holds frames from a different scene or settings (page ${existing.page}, ${existing.w}x${existing.h} at ${existing.fps} fps). Use a new --out, or --overwrite to render everything again.`);
      }
      if (!existing || cfg.overwrite || existing.fingerprint !== report.fingerprint) {
        try { fs.writeFileSync(metaFile, JSON.stringify(meta) + '\n', { flag: cfg.overwrite ? 'w' : 'wx' }); }
        catch (e) {
          if (e.code === 'EEXIST') { let again = null; try { again = JSON.parse(fs.readFileSync(metaFile, 'utf8')); } catch { /* being written by a sibling shard */ } if (again && again.fingerprint !== report.fingerprint) fail(2, `${displayPath(cfg.out)} was started by a different scene while this run was starting; use a new --out.`); if (!again) fs.writeFileSync(metaFile, JSON.stringify(meta) + '\n'); }
          else throw e;
        }
      }
      todo = [];
      for (const f of inShard) { if (!cfg.overwrite && validPng(framePath(f))) report.frames_skipped_existing++; else todo.push(f); }
    }

    // ffmpeg for video mode
    if (video) {
      const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(cfg.fps), '-c:v', 'png', '-i', '-', '-vf', chain.vf, ...chain.video_args, '-an', '-f', MUXER[chain.container] || chain.container, videoPartial];
      ff = spawn(cfg.ffmpegBin, args, { stdio: ['pipe', 'ignore', 'pipe'] });
      ff.stderr.on('data', (d) => { ffErr = (ffErr + d.toString()).slice(-4000); });
      ff.on('error', (e) => setFatal('ffmpeg', e.code === 'ENOENT' ? `ffmpeg not found (${cfg.ffmpegBin}); set FFMPEG or --ffmpeg-bin` : `ffmpeg failed to start: ${e.message}`, e.code === 'ENOENT' ? 3 : 2));
      ff.stdin.on('error', () => { if (!state.closing) setFatal('ffmpeg', `ffmpeg stopped early: ${ffErr.trim().split('\n').slice(-3).join(' | ') || 'no message'}`); });
    }

    // ---- the frame loop
    const tRender0 = Date.now();
    let cursor = 0, nextPos = 0, lastProgress = Date.now();
    const pending = new Map();
    const WINDOW = Math.max(4, cfg.concurrency * 3);
    const writeFf = (buf) => new Promise((resolve) => {
      if (ff.stdin.destroyed || ff.stdin.writableEnded) return resolve();
      if (ff.stdin.write(buf)) return resolve();
      ff.stdin.once('drain', resolve); ff.stdin.once('close', resolve); ff.stdin.once('error', resolve);
    });
    // frames reach ffmpeg in frame order; each call queues one pass behind the previous, so the last await sees everything written
    let drainChain = Promise.resolve();
    const drain = () => {
      drainChain = drainChain.then(async () => { while (pending.has(nextPos) && !state.fatal) { const b = pending.get(nextPos); pending.delete(nextPos); nextPos++; await writeFf(b); } });
      return drainChain;
    };
    const capture = async (page, f) => {
      const t = f / cfg.fps;
      await page.evaluate(async (tt) => {
        const r = window.seekTo(tt);
        if (r && typeof r.then === 'function') await r;
        await new Promise((res) => requestAnimationFrame(() => requestAnimationFrame(res)));
      }, t);
      return page.screenshot({ type: 'png', omitBackground: cfg.alpha, clip: { x: 0, y: 0, width: cfg.w, height: cfg.h }, caret: 'hide' });
    };
    const worker = async (page) => {
      for (;;) {
        if (state.fatal || state.stop) return;
        if (cfg.maxSeconds > 0 && (Date.now() - t0) / 1000 > cfg.maxSeconds) {
          if (video) { setFatal('timecap', `--max-seconds ${cfg.maxSeconds} reached in video mode, which cannot resume: render PNG shards and use --encode, or run it in the background`, 3); return; }
          state.stop = 'max-seconds'; return;
        }
        const pos = cursor++; if (pos >= todo.length) return;
        const f = todo[pos];
        if (video) { while (pos - nextPos >= WINDOW && !state.fatal) await sleep(2); if (state.fatal) return; }
        let buf;
        try { buf = await capture(page, f); }
        catch (e) { setFatal('scene', `frame ${f}: ${String(e.message || e).split('\n')[0]}`); return; }
        if (state.fatal) return;
        report.frame_sha256[f] = sha256(buf);
        if (video) { pending.set(pos, buf); await drain(); }
        else {
          const file = framePath(f);
          await fsp.writeFile(`${file}.tmp`, buf); await fsp.rename(`${file}.tmp`, file); state.written.add(f);
        }
        report.frames_rendered++;
        if (!cfg.quiet && Date.now() - lastProgress > 5000) { lastProgress = Date.now(); log(`[render] ${report.frames_rendered}/${todo.length} frames, ${(report.frames_rendered / ((Date.now() - tRender0) / 1000)).toFixed(2)} fps`); }
      }
    };
    await Promise.all(pages.map((p) => worker(p)));
    if (video && !state.fatal) { await drain(); }
    report.seconds_render = Math.round(Date.now() - tRender0) / 1000;
    report.throughput_fps = report.seconds_render > 0 ? Math.round((report.frames_rendered / report.seconds_render) * 100) / 100 : 0;

    if (!state.fatal) {
      try { report.scene_report = await pages[0].evaluate(() => (typeof window.ljReport === 'function' ? window.ljReport() : null)); } catch { report.scene_report = null; }
    }
    if (!state.fatal && video) {
      ff.stdin.end();
      const code = await new Promise((resolve) => ff.on('close', resolve));
      if (code !== 0) setFatal('ffmpeg', `ffmpeg exited with ${code}: ${ffErr.trim().split('\n').slice(-3).join(' | ')}`);
    }
    if (!state.fatal && !video && state.pageErrors > 0) { /* default: finish, then exit 2 below */ }

    // ---- outcome
    report.peak_rss = rssSampler.stop(); rssSampler = null;
    if (state.fatal) throw new Error('fatal-during-render');
    if (video) {
      fs.renameSync(videoPartial, videoFile);
      const probe = probeVideo(videoFile, cfg);
      const want = { ...(chain.expect || {}), width: cfg.w, height: cfg.h };
      const got = probe.error ? probe : { codec: probe.codec_name, profile: probe.profile, pix_fmt: probe.pix_fmt, width: probe.width, height: probe.height, color_range: probe.color_range, color_space: probe.color_space, color_primaries: probe.color_primaries, color_transfer: probe.color_transfer, r_frame_rate: probe.r_frame_rate, nb_frames: probe.nb_frames };
      const mismatches = [];
      if (probe.error) mismatches.push(`ffprobe: ${probe.error}`);
      else {
        for (const [k, v] of Object.entries(want)) if (v !== undefined && v !== null && String(got[k]) !== String(v)) mismatches.push(`${k}: expected ${v}, got ${got[k]}`);
        const wantFrames = B - A; if (String(got.nb_frames) !== String(wantFrames)) mismatches.push(`nb_frames: expected ${wantFrames}, got ${got.nb_frames}`);
      }
      report.chain_check = { ok: mismatches.length === 0, got, mismatches };
      report.complete = true;
      report.ok = mismatches.length === 0;
      finishReport();
      console.log(JSON.stringify({ mode: 'video', frames: report.frames_rendered, seconds: report.seconds, throughput_fps: report.throughput_fps, video: report.video, chain: chain.name, chain_ok: report.ok }));
      if (mismatches.length) { console.error(`render.mjs: encoded file does not match chain "${chain.name}": ${mismatches.join('; ')}`); return 1; }
      return 0;
    }
    const remaining = todo.length - report.frames_rendered;
    report.remaining = remaining;
    report.complete = remaining === 0;
    report.ok = state.pageErrors === 0;
    if (state.stop === 'max-seconds') { report.resume_hint = 'soft cap reached: run the same command again to resume (finished frames are skipped)'; log(`render.mjs: ${report.resume_hint}; ${remaining} frame(s) left`); }
    if (state.pageErrors > 0) { report.error = { kind: 'pageerror', message: `${state.pageErrors} uncaught page error(s); frames were kept (use --fail-on-pageerror to stop at the first one)` }; log(`render.mjs: ${report.error.message}`); }
    finishReport();
    console.log(JSON.stringify({ shard: `${si}/${sn}`, frames: report.frames_rendered, skipped: report.frames_skipped_existing, remaining, seconds: report.seconds, throughput_fps: report.throughput_fps, complete: report.complete }));
    return state.pageErrors > 0 ? 2 : 0;
  } catch (e) {
    // fatal paths: remove this run's output, write the report, exit with the recorded code
    if (e instanceof Exit) { await closeAll(); discardOutput(); throw e; }
    const fatalInfo = state.fatal || { kind: 'internal', message: String(e && e.message || e), code: 1 };
    if (rssSampler) { report.peak_rss = rssSampler.stop(); rssSampler = null; }
    await closeAll();
    if (!fatalInfo.keep) discardOutput();
    report.error = { kind: fatalInfo.kind, message: fatalInfo.message };
    report.output_removed = !fatalInfo.keep;
    finishReport();
    console.error(`render.mjs: ${fatalInfo.message}`);
    if (!fatalInfo.keep) console.error('render.mjs: the output of this run was removed' + (cfg.out && !video ? ' (frames written by earlier runs are untouched)' : ''));
    else console.error('render.mjs: finished frames are kept; run the same command again to continue');
    return fatalInfo.code;
  } finally {
    process.removeListener('SIGINT', onSignal); process.removeListener('SIGTERM', onSignal);
    if (rssSampler) rssSampler.stop();
    await closeAll();
  }
}

async function encodeOnly(cfg, chain, videoFile, videoPartial, A, B, framePath, report, finishReport, log) {
  const t0 = Date.now();
  const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(cfg.fps), '-c:v', 'png', '-i', '-', '-vf', chain.vf, ...chain.video_args, '-an', '-f', MUXER[chain.container] || chain.container, videoPartial];
  fs.mkdirSync(path.dirname(path.resolve(videoFile)), { recursive: true });
  const ff = spawn(cfg.ffmpegBin, args, { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = '', spawnErr = null;
  ff.stderr.on('data', (d) => { err = (err + d.toString()).slice(-4000); });
  ff.on('error', (e) => { spawnErr = e; });
  ff.stdin.on('error', () => {});
  for (let f = A; f < B && !spawnErr; f++) {
    const buf = await fsp.readFile(framePath(f));
    report.frame_sha256[f] = sha256(buf);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    report.frames_rendered++;
  }
  ff.stdin.end();
  const code = await new Promise((r) => ff.on('close', r));
  if (spawnErr || code !== 0) {
    try { fs.unlinkSync(videoPartial); } catch { /* none */ }
    report.error = { kind: 'ffmpeg', message: spawnErr ? spawnErr.message : `ffmpeg exited with ${code}: ${err.trim().split('\n').slice(-3).join(' | ')}` };
    finishReport(); console.error(`render.mjs: ${report.error.message}`);
    return spawnErr && spawnErr.code === 'ENOENT' ? 3 : 2;
  }
  fs.renameSync(videoPartial, videoFile);
  const probe = probeVideo(videoFile, cfg);
  const mismatches = [];
  if (probe.error) mismatches.push(`ffprobe: ${probe.error}`);
  else {
    const got = { codec: probe.codec_name, profile: probe.profile, pix_fmt: probe.pix_fmt, width: probe.width, height: probe.height, color_range: probe.color_range, color_space: probe.color_space, color_primaries: probe.color_primaries, color_transfer: probe.color_transfer, nb_frames: probe.nb_frames };
    for (const [k, v] of Object.entries({ ...(chain.expect || {}), width: cfg.w, height: cfg.h })) if (v != null && String(got[k]) !== String(v)) mismatches.push(`${k}: expected ${v}, got ${got[k]}`);
    if (String(got.nb_frames) !== String(B - A)) mismatches.push(`nb_frames: expected ${B - A}, got ${got.nb_frames}`);
    report.chain_check = { ok: mismatches.length === 0, got, mismatches };
  }
  report.complete = true; report.ok = mismatches.length === 0;
  report.seconds_render = Math.round(Date.now() - t0) / 1000;
  finishReport();
  console.log(JSON.stringify({ mode: 'encode', frames: report.frames_rendered, video: report.video, chain: chain.name, chain_ok: report.ok }));
  if (mismatches.length) { console.error(`render.mjs: encoded file does not match chain "${chain.name}": ${mismatches.join('; ')}`); return 1; }
  return 0;
}

// run only when started as a program, so tests can import parseArgs/resolveRequest/startServer
const isMain = process.argv[1] && (() => { try { return pathToFileURL(fs.realpathSync(process.argv[1])).href === import.meta.url; } catch { return false; } })();
if (isMain) {
  main(process.argv.slice(2)).then(
    (code) => { process.exitCode = code; setTimeout(() => process.exit(code), 50).unref(); },
    (e) => {
      if (e instanceof Exit) { console.error(`render.mjs: ${e.message}`); process.exit(e.exitCode); }
      console.error(`render.mjs: internal error: ${e && e.stack || e}`); process.exit(1);
    },
  );
}
