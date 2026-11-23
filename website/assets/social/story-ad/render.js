// Zinlea Night Instagram Story ad (1080x1920). All text sits inside Meta's ad safe zone:
// top 14% (~270px) and bottom 35% (~670px) kept clear for Instagram's profile bar and the CTA button; 6% sides.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const D = __dirname;
const photo = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, f)).toString('base64');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const W = 1080, H = 1920, SIDE = 72, TOP = 280, BOTTOM = 1240;
const word = s => { const d = Math.round(s * .21), h = Math.round(s * .08), t = Math.round(s * .1);
  return `<span style="font:600 ${s}px/1 'Albert Sans';letter-spacing:-.045em;color:#EEF1F7">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${t}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:#CCD9EF;box-shadow:0 0 0 ${h}px rgba(204,217,239,.22)"></span></span>nlea</span>`; };
const check = t => `<div style="display:flex;gap:18px;align-items:flex-start;font:400 33px/1.3 'Albert Sans';color:#EEF1F7"><span style="flex-shrink:0;margin-top:9px;width:22px;height:22px;border-radius:50%;background:#CCD9EF;box-shadow:0 0 0 6px rgba(204,217,239,.18)"></span>${t}</div>`;

function ad(v) {
  return `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#070B17;font-family:'Albert Sans';color:#EEF1F7">
    <img src="${photo('bedside.jpg')}" style="position:absolute;left:0;top:0;width:100%;height:1180px;object-fit:cover;object-position:62% 38%;filter:saturate(.9)">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,11,23,.72) 0%,rgba(7,11,23,.12) 14%,rgba(7,11,23,.05) 24%,rgba(7,11,23,.82) 38%,rgba(7,11,23,.96) 52%,#070B17 62%,#0B1428 100%)"></div>
    <svg style="position:absolute;inset:0" width="${W}" height="${H}">${[0,1,2,3].map(i => `<circle cx="${W}" cy="${H - 120}" r="${260 + i * 95}" fill="none" stroke="#CCD9EF" stroke-opacity="${.2 - i * .04}" stroke-width="${i === 0 ? 10 : 3}" ${i === 1 ? 'stroke-dasharray="2 16"' : ''} stroke-linecap="round"/>`).join('')}</svg>
    <div style="position:absolute;left:${SIDE}px;right:${SIDE}px;top:${TOP}px;display:flex;justify-content:space-between;align-items:center">
      <div style="display:flex;align-items:baseline;gap:10px">${word(40)}<span style="font:300 30px 'Albert Sans';color:rgba(238,241,247,.75)">night</span></div>
      <span style="padding:10px 18px;border-radius:999px;background:rgba(7,11,23,.55);backdrop-filter:blur(10px);font:400 24px 'DM Mono'">20:00 &mdash; 08:00</span>
    </div>
    <div style="position:absolute;left:${SIDE}px;right:${SIDE}px;top:${v.textTop}px">
      <h1 style="margin:0;font:400 88px/1.02 'Albert Sans';letter-spacing:-.04em">${v.headline}</h1>
      <p style="margin:24px 0 34px;font:300 36px/1.4 'Albert Sans';color:rgba(238,241,247,.85)">${v.sub}</p>
      <div style="display:grid;gap:18px">${v.points.map(check).join('')}</div>
    </div>
    <div style="position:absolute;left:${SIDE}px;right:${SIDE}px;top:${BOTTOM - 70}px;display:flex;justify-content:space-between;align-items:center">
      <span style="font:500 32px 'Albert Sans'">From &pound;85 a month</span>
      <span style="display:flex;align-items:center;gap:12px;font:400 26px 'DM Mono';color:#CCD9EF">Learn more
        <svg width="26" height="40" viewBox="0 0 26 40"><path d="M13 0v36M2 25l11 11 11-11" fill="none" stroke="#CCD9EF" stroke-width="2.5"/></svg></span>
    </div>
    ${v.guides ? `<div style="position:absolute;left:0;right:0;top:0;height:269px;background:rgba(255,0,80,.18);border-bottom:2px dashed #ff2d6f"></div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:672px;background:rgba(255,0,80,.18);border-top:2px dashed #ff2d6f;display:flex;align-items:center;justify-content:center;font:500 30px 'Albert Sans'">Instagram's button and caption sit here</div>` : ''}
  </div></body>`;
}

const A = { headline: 'Worried at 2am?<br><span style="color:#CCD9EF">Speak to a senior nurse.</span>', sub: 'Private overnight medical advice for London families.', textTop: 690,
  points: ['Phone or video, 8pm to 8am', 'Experienced Advanced Nurse Practitioners', 'Advice, prescribing and clear next steps'] };
const B = { headline: 'Medical advice,<br><span style="color:#CCD9EF">after your GP closes.</span>', sub: 'Private overnight support from senior nurses in London.', textTop: 690,
  points: ['Phone or video, 8pm to 8am', 'Experienced Advanced Nurse Practitioners', 'Advice, prescribing and clear next steps'] };

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const [n, v] of [['story-ad-A', A], ['story-ad-B', B], ['_safezone-check', { ...A, guides: true }]]) {
    await pg.setContent(ad(v)); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', n + '.png') });
  }
  await b.close();
})();
