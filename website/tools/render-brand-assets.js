// Renders social share images (assets/og/*.jpg, 1200x630) and icons (assets/brand/*.png)
// in the Zinlea identity. Run from the website folder: node tools/render-brand-assets.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600&family=DM+Mono&display=block">`;

function word(size, ink, dot, halo) {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${ink};white-space:nowrap">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${dot};box-shadow:0 0 0 ${h}px ${halo}"></span></span>nlea</span>`;
}

const OG = {
  'og-health':  { bg: '#FFFFFF', ink: '#0E1116', sub: '#5A606B', dot: '#2D4A8A', halo: 'rgba(45,74,138,.16)', subname: 'health', line: 'Private clinical care, whatever the hour.', meta: 'Zinlea Night · Zinlea Global' },
  'og-night':   { bg: 'radial-gradient(120% 140% at 80% 120%,#1B2747 0%,#070B17 60%)', ink: '#EEF1F7', sub: 'rgba(238,241,247,.7)', dot: '#CCD9EF', halo: 'rgba(204,217,239,.22)', subname: 'night', line: 'Overnight medical advice in London.', meta: '20:00 — 08:00 · Advanced Nurse Practitioners' },
  'og-global':  { bg: 'radial-gradient(130% 120% at 50% 125%,#F3B78C 0%,#7A5664 24%,#1A2448 50%,#08101F 78%)', ink: '#F4F0EB', sub: 'rgba(244,240,235,.72)', dot: '#F3B78C', halo: 'rgba(243,183,140,.28)', subname: 'global', line: 'Healthcare partnerships, built together.', meta: 'Across Africa' },
  'og-private': { bg: 'radial-gradient(130% 120% at 100% 0%,#2A2F3D 0%,#0A0B0F 55%)', ink: '#E9E4DA', sub: 'rgba(233,228,218,.7)', dot: '#E9E4DA', halo: 'rgba(233,228,218,.16)', subname: 'night', line: 'Private Client. Care that knows you.', meta: 'By private consultation' },
};

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const [name, t] of Object.entries(OG)) {
    await pg.setContent(`${FONT}<body style="margin:0"><div id="c" style="width:1200px;height:630px;box-sizing:border-box;padding:72px 84px;display:flex;flex-direction:column;justify-content:space-between;background:${t.bg}">
      <div style="display:flex;align-items:baseline;gap:16px">${word(64, t.ink, t.dot, t.halo)}<span style="font:300 44px 'Albert Sans';letter-spacing:-.02em;color:${t.sub}">${t.subname}</span></div>
      <div style="font:300 78px/1.04 'Albert Sans';letter-spacing:-.035em;color:${t.ink};max-width:16ch">${t.line}</div>
      <div style="display:flex;justify-content:space-between;font:400 22px 'DM Mono';color:${t.sub}"><span>${t.meta}</span><span>zinlea.com</span></div>
    </div></body>`);
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(250);
    await (await pg.$('#c')).screenshot({ path: path.join(ROOT, 'assets/og', name + '.jpg'), type: 'jpeg', quality: 88 });
  }
  // Square icon: the "z" with the moon dot on night blue.
  for (const [file, size] of [['logo-512.png', 512], ['apple-touch-icon.png', 180], ['icon-192.png', 192], ['icon-32.png', 32]]) {
    await pg.setViewportSize({ width: size, height: size });
    const f = Math.round(size * 0.66), d = Math.round(size * 0.125);
    await pg.setContent(`${FONT}<body style="margin:0"><div id="c" style="width:${size}px;height:${size}px;display:flex;align-items:center;justify-content:center;background:radial-gradient(120% 120% at 50% 110%,#1B2747 0%,#070B17 62%)">
      <div style="position:relative;font:600 ${f}px/1 'Albert Sans';color:#EEF1F7;transform:translate(-${Math.round(size*.04)}px,-${Math.round(size*.04)}px)">z<span style="position:absolute;right:-${d}px;top:${Math.round(size*.03)}px;width:${d}px;height:${d}px;border-radius:50%;background:#CCD9EF;box-shadow:0 0 0 ${Math.round(d*.35)}px rgba(204,217,239,.22)"></span></div></div></body>`);
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(200);
    await (await pg.$('#c')).screenshot({ path: path.join(ROOT, 'assets/brand', file) });
  }
  await b.close();
})();
