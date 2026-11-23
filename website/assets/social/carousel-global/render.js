// Zinlea Global carousel (5 slides, 1080x1350 @2x): midnight warming to dawn, apricot accents.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = __dirname, W = 1080, H = 1350, PAD = 84;
const INK = '#F4F0EB', MUTED = 'rgba(244,240,235,.78)', LINE = 'rgba(244,240,235,.16)', AP = '#F3B78C';
const photo = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, f)).toString('base64');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const word = `<span style="display:inline-flex;align-items:baseline;gap:10px"><span style="font:600 34px/1 'Albert Sans';letter-spacing:-.045em;color:${INK}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:3px;width:7px;height:7px;border-radius:50%;transform:translateX(-50%);background:${AP};box-shadow:0 0 0 3px rgba(243,183,140,.28)"></span></span>nlea</span><span style="font:300 25px 'Albert Sans';color:${MUTED}">global</span></span>`;
const top = r => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:72px;display:flex;justify-content:space-between;align-items:center;z-index:2">${word}<span style="font:400 22px 'DM Mono';color:${MUTED}">${r}</span></div>`;
const page = n => `<div style="position:absolute;right:${PAD}px;bottom:64px;font:400 20px 'DM Mono';color:${MUTED};opacity:.7">0${n} / 05</div>`;
const DAWN = `linear-gradient(180deg,#08101F 0%,#0E1A35 42%,#2A2C50 72%,#5A4A64 100%)`;
const SUN = `<div style="position:absolute;left:50%;bottom:-520px;width:1300px;height:1300px;margin-left:-650px;border-radius:50%;background:radial-gradient(circle,rgba(255,206,160,.8) 0%,rgba(243,183,140,.4) 22%,rgba(122,86,100,.2) 42%,transparent 62%)"></div>`;
const photoBg = (f, pos) => `<img src="${photo(f)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${pos};filter:saturate(.9)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,16,31,.72) 0%,rgba(8,16,31,.15) 16%,rgba(8,16,31,.1) 38%,rgba(8,16,31,.88) 70%,rgba(8,16,31,.97) 100%)"></div>`;
const frame = (bg, inner, n) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${bg};color:${INK};font-family:'Albert Sans'">${inner}${page(n)}</div></body>`;
const label = s => `<div style="display:inline-flex;align-items:center;gap:12px;font:500 25px 'Albert Sans';color:${MUTED};margin-bottom:28px"><span style="width:10px;height:10px;border-radius:50%;background:${AP};box-shadow:0 0 0 7px rgba(243,183,140,.25)"></span>${s}</div>`;
const H1 = (s, z = 80) => `<h1 style="margin:0;font:400 ${z}px/1.04 'Albert Sans';letter-spacing:-.038em">${s}</h1>`;
const P = (s, m = 30) => `<p style="margin:${m}px 0 0;font:300 33px/1.45 'Albert Sans';color:${MUTED}">${s}</p>`;
const pill = s => `<span style="display:inline-block;padding:14px 26px;border-radius:999px;border:1.5px solid rgba(244,240,235,.5);font:400 29px 'Albert Sans'">${s}</span>`;
const row = (k, t, s) => `<div style="display:grid;grid-template-columns:96px 1fr;gap:12px;padding:26px 0;border-top:1px solid ${LINE}"><span style="font:400 24px 'DM Mono';color:${AP};padding-top:6px">${k}</span><div><div style="font:400 36px/1.15 'Albert Sans';letter-spacing:-.02em">${t}</div><div style="margin-top:6px;font:300 27px/1.4 'Albert Sans';color:${MUTED}">${s}</div></div></div>`;
const at = (pos, inner) => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;${pos}">${inner}</div>`;
const A = s => `<span style="color:${AP}">${s}</span>`;
const SLIDES = [
  frame('#08101F', `${photoBg('doctor.jpg', '50% 20%')}${top('Across Africa')}
    ${at('bottom:130px', `${label('Zinlea Global')}${H1('Healthcare partnerships, ' + A('built together.'), 90)}${P('How Zinlea Global works with healthcare organisations across Africa.')}`)}`, 1),
  frame('#08101F', `${photoBg('board.jpg', '50% 40%')}${top('Who we work with')}
    ${at('bottom:130px', `${H1('Built with the people who know their markets best.', 74)}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:40px">${['Hospital groups', 'Private clinics', 'Clinicians', 'Investors', 'Development partners'].map(pill).join('')}</div>`)}`, 2),
  frame(DAWN, `${SUN}${top('How we support partners')}
    ${at('top:200px', `${label('What we bring')}${H1('Practical support, ' + A('shaped with you.'), 78)}
      <div style="margin-top:44px">
        ${row('01', 'Out-of-hours and remote clinical support', 'Models for overnight advice, triage and escalation')}
        ${row('02', 'Clinical governance', 'Protocols, escalation pathways and safety frameworks')}
        ${row('03', 'Shared learning and training', 'Knowledge flowing in both directions')}
        ${row('04', 'Sustainable models of care', 'Co-designed with partners and investors')}
      </div>`)}`, 3),
  frame('#08101F', `${photoBg('phone.jpg', '40% 35%')}${top('Partnership')}
    ${at('bottom:130px', `${H1('Each side brings ' + A('what it knows best.'), 80)}
      ${P('We bring our experience of running a private overnight advice service in London. Our partners bring their expertise, relationships and understanding of their communities.')}`)}`, 4),
  frame(DAWN, `${SUN}${top('zinlea.com')}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:330px;text-align:center">
      ${label('Now speaking with founding partners')}
      ${H1('Build the future of care ' + A('with us.'), 88)}
      ${P('If you are a healthcare provider, clinician or investor in Africa, we would like to hear from you.', 30)}
      <div style="margin-top:44px;display:inline-flex;padding:20px 34px;border-radius:999px;background:${AP};color:#1B0F07;font:500 30px 'Albert Sans'">zinlea.com/global</div>
      <div style="margin-top:22px;font:400 24px 'DM Mono';color:${MUTED}">info@zinlea.com</div></div>`, 5),
];
(async () => { fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  for (let i = 0; i < SLIDES.length; i++) { await pg.setContent(SLIDES[i]); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `zinlea-global-${i + 1}.png`) }); }
  await b.close(); })();
