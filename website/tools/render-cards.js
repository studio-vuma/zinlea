// Business card front/back (85x55mm ratio) and a phone-shareable card, using the tested QR code.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const R = path.join(__dirname, '..');
const qr = 'data:image/png;base64,' + fs.readFileSync(path.join(R, 'assets/brand/qr/zinlea-qr.png')).toString('base64');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const word = (size, ink, dot, halo) => { const d = Math.round(size * .21), h = Math.round(size * .08), t = Math.round(size * .1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${ink}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${t}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${dot};box-shadow:0 0 0 ${h}px ${halo}"></span></span>nlea</span>`; };
const W = 1004, H = 650; // 85x55mm at 300dpi
const MID = 'radial-gradient(120% 120% at 100% 0%,#24345E 0%,#0B1124 58%)';
const front = `<div id="c" style="width:${W}px;height:${H}px;box-sizing:border-box;padding:64px 70px;background:${MID};color:#EEF1F7;display:flex;flex-direction:column;justify-content:space-between;font-family:'Albert Sans'">
  <div style="display:flex;justify-content:space-between;align-items:center"><div style="display:flex;align-items:baseline;gap:12px">${word(64, '#EEF1F7', '#CCD9EF', 'rgba(204,217,239,.22)')}<span style="font:300 44px 'Albert Sans';color:rgba(238,241,247,.7)">health</span></div>
  <span style="font:400 24px 'DM Mono';color:rgba(238,241,247,.6)">20:00 &mdash; 08:00</span></div>
  <div style="font:300 58px/1.08 'Albert Sans';letter-spacing:-.03em;max-width:13ch">Expert medical advice, <span style="color:#CCD9EF">when you need it.</span></div>
  <div style="display:flex;gap:34px;font:400 24px 'Albert Sans';color:rgba(238,241,247,.72)"><span>Zinlea Night &middot; London</span><span>Zinlea Global &middot; Africa</span></div></div>`;
const back = `<div id="c" style="width:${W}px;height:${H}px;box-sizing:border-box;padding:60px 64px;background:#FFFFFF;color:#0E1116;display:flex;gap:56px;align-items:center;font-family:'Albert Sans'">
  <div style="flex:1;display:flex;flex-direction:column;gap:26px">
    <div style="display:flex;align-items:baseline;gap:10px">${word(46, '#0E1116', '#2D4A8A', 'rgba(45,74,138,.16)')}<span style="font:300 32px 'Albert Sans';color:#5A606B">health</span></div>
    <div style="display:grid;gap:14px;font:400 30px 'Albert Sans'">
      <span>info@zinlea.com</span><span>zinlea.com</span><span>@zinleanight</span></div>
    <div style="font:400 20px 'DM Mono';color:#5A606B">Scan to email or save our contact</div></div>
  <div style="width:400px;height:400px;flex-shrink:0;border-radius:28px;padding:18px;box-sizing:border-box;box-shadow:inset 0 0 0 2px #E3E5E9"><img src="${qr}" style="width:100%;height:100%;display:block"></div></div>`;
// Phone-friendly card to send by WhatsApp/text or show on screen.
const share = `<div id="c" style="width:1080px;height:1350px;box-sizing:border-box;padding:90px 84px;background:${MID};color:#EEF1F7;display:flex;flex-direction:column;align-items:center;text-align:center;font-family:'Albert Sans'">
  <div style="display:flex;align-items:baseline;gap:12px">${word(64, '#EEF1F7', '#CCD9EF', 'rgba(204,217,239,.22)')}<span style="font:300 44px 'Albert Sans';color:rgba(238,241,247,.7)">health</span></div>
  <div style="margin-top:56px;font:300 64px/1.08 'Albert Sans';letter-spacing:-.03em">Expert medical advice, <span style="color:#CCD9EF">when you need it.</span></div>
  <div style="margin-top:60px;width:520px;height:520px;border-radius:40px;background:#fff;padding:26px;box-sizing:border-box"><img src="${qr}" style="width:100%;height:100%;display:block"></div>
  <div style="margin-top:34px;font:400 28px 'DM Mono';color:rgba(238,241,247,.7)">Scan to email us or save our contact</div>
  <div style="margin-top:auto;display:flex;gap:40px;font:400 30px 'Albert Sans'"><span>info@zinlea.com</span><span style="color:rgba(238,241,247,.5)">&middot;</span><span>zinlea.com</span></div></div>`;
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ deviceScaleFactor: 1 });
  fs.mkdirSync(path.join(R, 'assets/brand/cards'), { recursive: true });
  for (const [n, html, w, h] of [['business-card-front', front, W, H], ['business-card-back', back, W, H], ['digital-card-share', share, 1080, 1350]]) {
    await pg.setViewportSize({ width: w, height: h });
    await pg.setContent(`${FONT}<body style="margin:0">${html}</body>`); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(250);
    await (await pg.$('#c')).screenshot({ path: path.join(R, 'assets/brand/cards', n + '.png') });
  }
  await b.close();
})();
