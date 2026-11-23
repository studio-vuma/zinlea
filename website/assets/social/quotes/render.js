// Zinlea quote posts on white (1080x1350, rendered at 2x). Six layouts so they don't repeat on the grid.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const D = __dirname, W = 1080, H = 1350, PAD = 90;
const INK = '#0E1116', MUTED = '#5A606B', BLUE = '#2D4A8A', LINE = 'rgba(14,17,22,.12)';
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const word = (s, sub = 'health') => { const d = Math.round(s * .21), h = Math.round(s * .08), t = Math.round(s * .1);
  return `<span style="display:inline-flex;align-items:baseline;gap:9px"><span style="font:600 ${s}px/1 'Albert Sans';letter-spacing:-.045em;color:${INK}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${t}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${BLUE};box-shadow:0 0 0 ${h}px rgba(45,74,138,.16)"></span></span>nlea</span><span style="font:300 ${Math.round(s * .74)}px 'Albert Sans';color:${MUTED}">${sub}</span></span>`; };
const frame = (inner, bg = '#FFFFFF') => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${bg};color:${INK};font-family:'Albert Sans'">${inner}</div></body>`;
const foot = (left, right = 'zinlea.com') => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:84px;display:flex;justify-content:space-between;align-items:center">${left}<span style="font:400 22px 'DM Mono';color:${MUTED}">${right}</span></div>`;
const hl = s => `<span style="color:${BLUE}">${s}</span>`;
function arc(w, pos = 6.2, op = 1) {
  const cx = 260, cy = 270, r = 220; let t = '';
  for (let h = 0; h <= 12; h++) { const a = Math.PI - (h / 12) * Math.PI, m = h % 2 === 0, r1 = r + 8, r2 = r + (m ? 20 : 14);
    t += `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy - r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy - r2 * Math.sin(a)}" stroke="${INK}" stroke-opacity="${m ? .5 : .25}" stroke-width="2"/>`;
    if (m) t += `<text x="${cx + (r + 46) * Math.cos(a)}" y="${cy - (r + 46) * Math.sin(a) + 7}" text-anchor="middle" font-family="DM Mono" font-size="21" fill="${INK}" fill-opacity=".55">${String((20 + h) % 24).padStart(2, '0')}</text>`; }
  const at = Math.PI - (pos / 12) * Math.PI, mx = cx + r * Math.cos(at), my = cy - r * Math.sin(at);
  return `<svg viewBox="-24 0 568 300" width="${w}" style="display:block;overflow:visible;opacity:${op}"><path d="M 40 270 A 220 220 0 0 1 480 270" fill="none" stroke="${INK}" stroke-opacity=".14" stroke-width="2"/><path d="M 40 270 A 220 220 0 0 1 ${mx} ${my}" fill="none" stroke="${BLUE}" stroke-width="3" stroke-linecap="round"/>${t}<circle cx="${mx}" cy="${my}" r="24" fill="${BLUE}" opacity=".15"/><circle cx="${mx}" cy="${my}" r="10" fill="${BLUE}"/></svg>`;
}

const Q = [
  // 1. Big quotation mark, left aligned
  frame(`<div style="position:absolute;left:${PAD}px;top:96px">${word(36)}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:200px;bottom:200px;display:flex;flex-direction:column;justify-content:center">
      <div style="width:26px;height:26px;border-radius:50%;background:${BLUE};box-shadow:0 0 0 14px rgba(45,74,138,.14);margin:0 0 70px 14px"></div>
      <div style="font:300 96px/1.06 'Albert Sans';letter-spacing:-.04em">Good care shouldn&rsquo;t depend on ${hl('what time it is.')}</div></div>
    ${foot(`<span style="font:400 22px 'DM Mono';color:${MUTED}">20:00 &mdash; 08:00</span>`)}`),

  // 2. Huge time stamp, line beneath
  frame(`<div style="position:absolute;left:${PAD}px;top:96px">${word(36, 'night')}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:200px;bottom:200px;display:flex;flex-direction:column;justify-content:center">
      <div style="font:300 250px/1 'DM Mono';letter-spacing:-.05em;color:${BLUE}">03:00</div>
      <div style="margin-top:56px;padding-top:40px;border-top:1px solid ${LINE};font:300 80px/1.08 'Albert Sans';letter-spacing:-.035em">Worry doesn&rsquo;t keep office hours.</div></div>
    ${foot('')}`),

  // 3. Centred, soft grey panel
  frame(`<div style="position:absolute;inset:60px;border-radius:44px;background:#F3F4F6"></div>
    <div style="position:absolute;left:0;right:0;top:140px;text-align:center">${word(36)}</div>
    <div style="position:absolute;left:130px;right:130px;top:240px;bottom:240px;display:flex;align-items:center;justify-content:center;text-align:center;font:300 88px/1.1 'Albert Sans';letter-spacing:-.035em"><div>The quietest hours can be ${hl('the hardest ones.')}</div></div>
    <div style="position:absolute;left:0;right:0;bottom:150px;text-align:center;font:400 22px 'DM Mono';color:${MUTED}">zinlea.com</div>`),

  // 4. Dial on top, statement beneath
  frame(`<div style="position:absolute;left:${PAD}px;top:96px">${word(36, 'night')}</div>
    <div style="position:absolute;left:0;right:0;top:230px;display:flex;justify-content:center">${arc(640, 6.2)}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:690px;text-align:center;font:300 84px/1.08 'Albert Sans';letter-spacing:-.035em">Calm, expert advice. ${hl('Whatever the hour.')}</div>
    ${foot(`<span style="font:400 22px 'DM Mono';color:${MUTED}">Senior nurses &middot; 8pm&ndash;8am</span>`)}`),

  // 5. Two-tone, bottom-anchored
  frame(`<div style="position:absolute;left:${PAD}px;top:96px">${word(36)}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:200px;font:300 84px/1.1 'Albert Sans';letter-spacing:-.035em">Good healthcare should feel private, professional and unhurried. <span style="color:#9AA0AA">Whatever the hour, wherever you are.</span></div>
    ${foot('')}`),

  // 6. Question & answer style
  frame(`<div style="position:absolute;left:${PAD}px;top:96px">${word(36, 'night')}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:200px;bottom:200px;display:flex;flex-direction:column;justify-content:center">
      <div style="font:400 26px 'DM Mono';color:${BLUE};margin-bottom:30px">Not every night needs 999.</div>
      <div style="font:300 92px/1.06 'Albert Sans';letter-spacing:-.04em">But every worry deserves ${hl('a calm answer.')}</div>
      <div style="margin-top:60px;padding-top:34px;border-top:1px solid ${LINE};font:300 32px/1.45 'Albert Sans';color:${MUTED}">Overnight medical advice from senior nurses, by phone or video. In an emergency, always call 999.</div></div>
    ${foot('')}`),
];

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  for (let i = 0; i < Q.length; i++) {
    await pg.setContent(Q[i]); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(250);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `zinlea-quote-${i + 1}.png`) });
  }
  await b.close();
})();
