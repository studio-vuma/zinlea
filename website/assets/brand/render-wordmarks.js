// Render the Zinlea wordmark set: square profile pictures and transparent logo files.
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = 'wordmarks';
fs.mkdirSync(OUT, { recursive: true });

const DAWN = 'radial-gradient(120% 120% at 50% 115%,#F3B78C 0%,#7A5664 22%,#1A2448 48%,#08101F 75%)';
const BGS = {
  dawn:     { bg: DAWN, ink: '#F4F0EB', sub: 'rgba(244,240,235,.72)', dot: '#F3B78C', halo: 'rgba(243,183,140,.28)' },
  health:   { bg: '#FFFFFF', ink: '#0E1116', sub: '#5A606B', dot: '#2D4A8A', halo: 'rgba(45,74,138,.16)' },
  midnight: { bg: 'radial-gradient(120% 120% at 50% 110%,#1B2747 0%,#070B17 62%)', ink: '#EEF1F7', sub: 'rgba(238,241,247,.7)', dot: '#CCD9EF', halo: 'rgba(204,217,239,.22)' },
};
const BRAND_DOT = { '': BGS.dawn, night: BGS.midnight, global: BGS.dawn };

// The wordmark: "z ı nlea" with the moon dot over the i. size = font size in px.
function word(size, ink, dot, halo) {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${ink};white-space:nowrap">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${dot};box-shadow:0 0 0 ${h}px ${halo}"></span></span>nlea</span>`;
}

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 1 });
  const fontLink = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&display=block">`;
  const made = [];

  // 1. Square profile pictures (stacked: wordmark, sub-brand underneath).
  const subs = ['', 'night', 'global'];
  for (const [bgName, t] of Object.entries(BGS)) {
    for (const sub of subs) {
      const size = sub ? 230 : 250;
      const html = `${fontLink}<body style="margin:0"><div id="c" style="width:1080px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:${sub ? 6 : 0}px;background:${t.bg}">
        ${word(size, t.ink, t.dot, t.halo)}
        ${sub ? `<span style="font:300 ${Math.round(size * 0.42)}px/1 'Albert Sans';letter-spacing:-.02em;color:${t.sub}">${sub}</span>` : ''}
      </div></body>`;
      await pg.setContent(html);
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(250);
      const f = `${OUT}/profile-${bgName}-zinlea${sub ? '-' + sub : ''}.png`;
      await (await pg.$('#c')).screenshot({ path: f });
      made.push(f);
    }
  }

  // 2. Transparent horizontal logos, matching the website lock-up (sub-brand beside the word).
  for (const [inkName, ink, subInk] of [['dark', '#0E1116', '#5A606B'], ['white', '#FFFFFF', 'rgba(255,255,255,.72)']]) {
    for (const sub of subs) {
      const t = sub === 'night' ? BGS.midnight : (inkName === 'dark' ? BGS.health : BGS.dawn);
      const dot = sub === 'global' ? '#F3B78C' : sub === 'night' ? (inkName === 'dark' ? '#2D4A8A' : '#CCD9EF') : t.dot;
      const halo = sub === 'global' ? 'rgba(243,183,140,.28)' : t.halo;
      const html = `${fontLink}<body style="margin:0;background:transparent"><div id="c" style="display:inline-flex;align-items:baseline;gap:34px;padding:60px 70px">
        ${word(240, ink, dot, halo)}
        ${sub ? `<span style="font:300 150px/1 'Albert Sans';letter-spacing:-.02em;color:${subInk}">${sub}</span>` : ''}
      </div></body>`;
      await pg.setContent(html);
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(250);
      const f = `${OUT}/logo-${inkName}-zinlea${sub ? '-' + sub : ''}.png`;
      await (await pg.$('#c')).screenshot({ path: f, omitBackground: true });
      made.push(f);
    }
  }

  // 3. Preview sheet.
  const img = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
  const prof = bg => made.filter(f => f.includes(`profile-${bg}-`)).map(f => `
    <figure style="margin:0;display:flex;flex-direction:column;align-items:center;gap:14px">
      <div style="display:flex;align-items:flex-end;gap:18px">
        <img src="${img(f)}" style="width:230px;border-radius:50%;box-shadow:0 0 0 1px #E3E5E9">
        <img src="${img(f)}" style="width:110px;border-radius:50%;box-shadow:0 0 0 1px #E3E5E9">
      </div>
      <figcaption style="font:400 16px 'Albert Sans';color:#5A606B">${f.split('/')[1]}</figcaption></figure>`).join('');
  const logos = ink => made.filter(f => f.includes(`logo-${ink}-`)).map(f => `
    <figure style="margin:0;padding:28px 34px;border-radius:20px;background:${ink === 'dark' ? '#fff' : '#08101F'};display:flex;flex-direction:column;gap:12px">
      <img src="${img(f)}" style="height:90px;width:auto;align-self:flex-start">
      <figcaption style="font:400 14px 'Albert Sans';color:${ink === 'dark' ? '#5A606B' : '#98A1B4'}">${f.split('/')[1]}</figcaption></figure>`).join('');
  const h = t => `<h2 style="font:500 24px 'Albert Sans';letter-spacing:-.02em;margin:48px 0 20px;color:#0E1116">${t}</h2>`;
  await pg.setViewportSize({ width: 2000, height: 1200 });
  await pg.setContent(`${fontLink}<body style="margin:0;padding:56px;background:#F3F4F6">
    ${h('Profile pictures: dawn (your pick)')}<div style="display:flex;gap:48px;flex-wrap:wrap">${prof('dawn')}</div>
    ${h('Profile pictures: each brand in its own colours')}<div style="display:flex;gap:48px;flex-wrap:wrap">${prof('health')}</div>
    <div style="display:flex;gap:48px;flex-wrap:wrap;margin-top:28px">${prof('midnight')}</div>
    ${h('Transparent logos')}<div style="display:flex;gap:20px;flex-wrap:wrap">${logos('dark')}</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:20px">${logos('white')}</div>
  </body>`);
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(400);
  await pg.screenshot({ path: `${OUT}/_preview.png`, fullPage: true });
  await b.close();
  console.log(made.join('\n'));
})();
