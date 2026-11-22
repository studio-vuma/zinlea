// Render Instagram profile picture options (1080x1080) and a preview sheet.
const { chromium } = require('playwright');
const fs = require('fs');
fs.mkdirSync('insta', { recursive: true });

const THEMES = {
  health: { bg: '#FFFFFF', ink: '#0E1116', dot: '#2D4A8A', halo: 'rgba(45,74,138,.16)' },
  night:  { bg: 'radial-gradient(120% 120% at 50% 110%,#1B2747 0%,#070B17 62%)', ink: '#EEF1F7', dot: '#CCD9EF', halo: 'rgba(204,217,239,.22)' },
  global: { bg: 'radial-gradient(120% 120% at 50% 115%,#F3B78C 0%,#7A5664 22%,#1A2448 48%,#08101F 75%)', ink: '#F4F0EB', dot: '#F3B78C', halo: 'rgba(243,183,140,.28)' },
};

// Three marks. Glyphs are the brand face (Albert Sans 600), the dot is the moon.
function mark(kind, t) {
  if (kind === 'z') return `
    <div style="position:relative;font:600 720px/1 'Albert Sans';letter-spacing:-.04em;color:${t.ink};transform:translate(-40px,-44px)">z
      <span style="position:absolute;right:-136px;top:30px;width:136px;height:136px;border-radius:50%;background:${t.dot};box-shadow:0 0 0 50px ${t.halo}"></span>
    </div>`;
  if (kind === 'i') return `
    <div style="position:relative;font:600 640px/1 'Albert Sans';color:${t.ink};transform:translateY(40px)">&#305;
      <span style="position:absolute;left:50%;top:-12px;width:150px;height:150px;border-radius:50%;transform:translateX(-50%);background:${t.dot};box-shadow:0 0 0 52px ${t.halo}"></span>
    </div>`;
  return `
    <div style="position:relative;font:600 250px/1 'Albert Sans';letter-spacing:-.045em;color:${t.ink}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:26px;width:52px;height:52px;border-radius:50%;transform:translateX(-50%);background:${t.dot};box-shadow:0 0 0 20px ${t.halo}"></span></span>nlea</div>`;
}

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  const files = [];
  for (const kind of ['z', 'i', 'word']) {
    for (const [name, t] of Object.entries(THEMES)) {
      await pg.setContent(`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@600&display=block">
        <body style="margin:0"><div id="c" style="width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;background:${t.bg}">${mark(kind, t)}</div></body>`);
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(300);
      const f = `insta/zinlea-${kind}-${name}.png`;
      await (await pg.$('#c')).screenshot({ path: f });
      files.push([kind, name, f]);
    }
  }

  // Preview sheet: each option as Instagram shows it (circle crop) at profile size and at feed/story size.
  const img = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
  const titles = { z: 'Recommended: z + moon dot', i: 'Your idea: the ı with the dot', word: 'Full wordmark' };
  const rows = ['z', 'i', 'word'].map(kind => `
    <section style="margin-bottom:56px">
      <h2 style="font:500 26px 'Albert Sans';letter-spacing:-.02em;margin:0 0 22px;color:#0E1116">${titles[kind]}</h2>
      <div style="display:flex;gap:56px;align-items:flex-end;flex-wrap:wrap">
        ${files.filter(x => x[0] === kind).map(([, name, f]) => `
          <figure style="margin:0;display:flex;flex-direction:column;align-items:center;gap:16px">
            <div style="display:flex;align-items:flex-end;gap:22px">
              <img src="${img(f)}" style="width:220px;height:220px;border-radius:50%;box-shadow:0 0 0 1px #E3E5E9">
              <img src="${img(f)}" style="width:110px;height:110px;border-radius:50%;box-shadow:0 0 0 1px #E3E5E9">
              <img src="${img(f)}" style="width:40px;height:40px;border-radius:50%;box-shadow:0 0 0 1px #E3E5E9">
            </div>
            <figcaption style="font:400 17px 'Albert Sans';color:#5A606B">${{ health: 'Zinlea Health', night: 'Zinlea Night', global: 'Zinlea Global' }[name]}</figcaption>
          </figure>`).join('')}
      </div>
    </section>`).join('');
  await pg.setViewportSize({ width: 2100, height: 1200 });
  await pg.setContent(`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500&display=block">
    <body style="margin:0;padding:64px;background:#F3F4F6;font-family:'Albert Sans'">
    <p style="font:400 18px 'Albert Sans';color:#5A606B;margin:0 0 40px">Each shown at three sizes: large, the actual Instagram profile size on a phone (110px), and the tiny size beside comments and stories (40px).</p>
    ${rows}</body>`);
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(400);
  await pg.screenshot({ path: 'insta/preview-sheet.png', fullPage: true });
  await b.close();
})();
