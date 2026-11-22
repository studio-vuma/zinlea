// Rebuild the "When illness doesn't wait until morning" Instagram post in the new Zinlea identity.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const scene = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname, 'scene-bedside.jpg')).toString('base64');

function word(size) {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:#EEF1F7">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:#CCD9EF;box-shadow:0 0 0 ${h}px rgba(204,217,239,.22)"></span></span>nlea</span>`;
}

// Small night dial (20:00 -> 08:00) with the marker part-way through the night.
function dial(w) {
  const cx = 260, cy = 270, r = 220; let t = '';
  for (let h = 0; h <= 12; h++) {
    const a = Math.PI - (h / 12) * Math.PI, major = h % 2 === 0;
    const r1 = r + 8, r2 = r + (major ? 20 : 14);
    t += `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy - r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy - r2 * Math.sin(a)}" stroke="#EEF1F7" stroke-opacity="${major ? .6 : .3}" stroke-width="2"/>`;
    if (major) t += `<text x="${cx + (r + 44) * Math.cos(a)}" y="${cy - (r + 44) * Math.sin(a) + 7}" text-anchor="middle" font-family="DM Mono" font-size="22" fill="#EEF1F7" fill-opacity=".6">${String((20 + h) % 24).padStart(2, '0')}</text>`;
  }
  const at = Math.PI - (6.4 / 12) * Math.PI, mx = cx + r * Math.cos(at), my = cy - r * Math.sin(at);
  return `<svg viewBox="-20 0 560 300" width="${w}" style="display:block;overflow:visible">
    <path d="M 40 270 A 220 220 0 0 1 480 270" fill="none" stroke="#EEF1F7" stroke-opacity=".18" stroke-width="2"/>
    <path d="M 40 270 A 220 220 0 0 1 ${mx} ${my}" fill="none" stroke="#CCD9EF" stroke-width="3" stroke-linecap="round"/>
    ${t}<circle cx="${mx}" cy="${my}" r="22" fill="#CCD9EF" opacity=".2"/><circle cx="${mx}" cy="${my}" r="9" fill="#CCD9EF"/></svg>`;
}

const BG = 'radial-gradient(120% 70% at 50% 105%,#1B2747 0%,#070B17 62%)';
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;

function post(W, H, story) {
  const pad = 72;
  const photoH = story ? 640 : 430;
  return `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;box-sizing:border-box;padding:${story ? 120 : 64}px ${pad}px ${story ? 110 : 60}px;background:${BG};color:#EEF1F7;font-family:'Albert Sans';display:flex;flex-direction:column;overflow:hidden">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="display:flex;align-items:baseline;gap:12px">${word(44)}<span style="font:300 32px 'Albert Sans';letter-spacing:-.02em;color:rgba(238,241,247,.7)">night</span></div>
      <span style="font:400 22px 'DM Mono';color:rgba(238,241,247,.7)">20:00 &mdash; 08:00</span>
    </div>

    <h1 style="margin:${story ? 96 : 52}px 0 0;font:300 ${story ? 104 : 92}px/1.0 'Albert Sans';letter-spacing:-.04em">When illness doesn&rsquo;t wait <span style="color:#CCD9EF">until morning.</span></h1>

    <div style="position:relative;margin-top:${story ? 64 : 40}px;height:${photoH}px;border-radius:36px;overflow:hidden">
      <img src="${scene}" style="width:100%;height:100%;object-fit:cover;object-position:50% 38%;filter:saturate(.92)">
      <div style="position:absolute;left:20px;bottom:20px;display:flex;align-items:center;gap:12px;padding:14px 20px;border-radius:18px;background:rgba(7,11,23,.5);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.16);font:500 22px 'Albert Sans';letter-spacing:-.01em">
        <span style="width:10px;height:10px;border-radius:50%;background:#5FD39A;box-shadow:0 0 0 5px rgba(95,211,154,.22)"></span>Advanced clinical care, overnight.
      </div>
    </div>

    <p style="margin:${story ? 56 : 34}px 0 0;font:300 ${story ? 32 : 27}px/1.45 'Albert Sans';color:rgba(238,241,247,.78);max-width:${story ? 900 : 880}px">For families, night-time can bring uncertainty, especially when access to clinical support feels limited. <span style="color:#EEF1F7;font-weight:400">Healthcare needs do not follow office hours.</span></p>
    ${`<p style="margin:${story ? 28 : 18}px 0 0;font:300 ${story ? 32 : 27}px/1.45 'Albert Sans';color:rgba(238,241,247,.78)">Zinlea Night is developing a dedicated overnight clinical support service, providing access to professional clinical assessment and support when it is needed.</p>`}

    <div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:32px;padding-top:${story ? 0 : 26}px;border-top:${story ? 0 : 1}px solid rgba(238,241,247,.14)">
      <div>
        <div style="font:400 ${story ? 44 : 36}px/1.15 'Albert Sans';letter-spacing:-.03em;max-width:${story ? 640 : 560}px">Because care should not have a closing time.</div>
        <div style="margin-top:16px;font:400 22px 'DM Mono';color:rgba(238,241,247,.6)">zinlea.com</div>
      </div>
      <div style="flex-shrink:0">${dial(story ? 300 : 230)}</div>
    </div>
  </div></body>`;
}

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const [name, W, H, story] of [['zinlea-night-post-4x5', 1080, 1350, false], ['zinlea-night-story-9x16', 1080, 1920, true]]) {
    await pg.setContent(post(W, H, story));
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(400);
    await (await pg.$('#c')).screenshot({ path: path.join(__dirname, name + '.png') });
  }
  await b.close();
})();
