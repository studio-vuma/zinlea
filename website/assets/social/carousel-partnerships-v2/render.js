// Zinlea Night B2B carousel: overnight clinical support for healthcare organisations (8 slides, 1080x1350).
// Same system as the 2am carousel: Albert Sans + DM Mono, midnight/white alternation, full-bleed photos, pills, the night dial.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const D = __dirname;
const photo = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, f)).toString('base64');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const W = 1080, H = 1350, PAD = 84;
const DARK = { ink: '#EEF1F7', muted: 'rgba(238,241,247,.78)', line: 'rgba(238,241,247,.16)', dot: '#CCD9EF', halo: 'rgba(204,217,239,.22)', sub: 'rgba(238,241,247,.7)' };
const LIGHT = { ink: '#0E1116', muted: '#5A606B', line: 'rgba(14,17,22,.12)', dot: '#2D4A8A', halo: 'rgba(45,74,138,.16)', sub: '#5A606B' };

function word(size, t) {
  const d = Math.round(size * .21), h = Math.round(size * .08), top = Math.round(size * .1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${t.ink}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${t.dot};box-shadow:0 0 0 ${h}px ${t.halo}"></span></span>nlea</span>`;
}
const brand = t => `<div style="display:flex;align-items:baseline;gap:10px">${word(34, t)}<span style="font:300 25px 'Albert Sans';color:${t.sub}">night</span></div>`;
const top = (t, right) => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:72px;display:flex;justify-content:space-between;align-items:center;z-index:2">${brand(t)}<span style="font:400 22px 'DM Mono';color:${t.sub}">${right}</span></div>`;
const label = (t, s) => `<div style="display:inline-flex;align-items:center;gap:12px;font:500 25px 'Albert Sans';color:${t.muted};margin-bottom:28px"><span style="width:10px;height:10px;border-radius:50%;background:${t.dot};box-shadow:0 0 0 7px ${t.halo}"></span>${s}</div>`;
const pill = (t, s) => `<span style="display:inline-block;padding:14px 26px;border-radius:999px;border:1.5px solid ${t === DARK ? 'rgba(238,241,247,.5)' : 'rgba(14,17,22,.3)'};color:${t.ink};font:400 29px 'Albert Sans'">${s}</span>`;
const row = (t, k, title, sub) => `<div style="display:grid;grid-template-columns:118px 1fr;gap:12px;padding:26px 0;border-top:1px solid ${t.line}">
  <span style="font:400 24px 'DM Mono';color:${t.dot};padding-top:6px">${k}</span>
  <div><div style="font:400 36px/1.15 'Albert Sans';letter-spacing:-.02em;color:${t.ink}">${title}</div>${sub ? `<div style="margin-top:6px;font:300 27px/1.4 'Albert Sans';color:${t.muted}">${sub}</div>` : ''}</div></div>`;
const page = n => `<div style="position:absolute;right:${PAD}px;bottom:64px;font:400 20px 'DM Mono';color:inherit;opacity:.55">${String(n).padStart(2, '0')} / 07</div>`;
const frame = (bg, color, inner, n) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${bg};color:${color};font-family:'Albert Sans'">${inner}${page(n)}</div></body>`;
const MID = 'radial-gradient(110% 70% at 50% 108%,#1F2D52 0%,#070B17 62%)';
const WHITE = 'radial-gradient(70% 45% at 90% 6%,rgba(45,74,138,.10),transparent 70%),#FFFFFF';
const photoBg = (img, pos) => `<img src="${img}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${pos};filter:saturate(.85)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,11,23,.7) 0%,rgba(7,11,23,.2) 16%,rgba(7,11,23,.1) 36%,rgba(7,11,23,.88) 70%,rgba(7,11,23,.97) 100%)"></div>`;
function dial(w, ink, accent, pos = 6.2) {
  const cx = 260, cy = 270, r = 220; let t = '';
  for (let h = 0; h <= 12; h++) {
    const a = Math.PI - (h / 12) * Math.PI, major = h % 2 === 0, r1 = r + 8, r2 = r + (major ? 20 : 14);
    t += `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy - r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy - r2 * Math.sin(a)}" stroke="${ink}" stroke-opacity="${major ? .55 : .28}" stroke-width="2"/>`;
    if (major) t += `<text x="${cx + (r + 46) * Math.cos(a)}" y="${cy - (r + 46) * Math.sin(a) + 7}" text-anchor="middle" font-family="DM Mono" font-size="21" fill="${ink}" fill-opacity=".6">${String((20 + h) % 24).padStart(2, '0')}</text>`;
  }
  const at = Math.PI - (pos / 12) * Math.PI, mx = cx + r * Math.cos(at), my = cy - r * Math.sin(at);
  return `<svg viewBox="-24 0 568 300" width="${w}" style="display:block;overflow:visible"><path d="M 40 270 A 220 220 0 0 1 480 270" fill="none" stroke="${ink}" stroke-opacity=".16" stroke-width="2"/><path d="M 40 270 A 220 220 0 0 1 ${mx} ${my}" fill="none" stroke="${accent}" stroke-width="3" stroke-linecap="round"/>${t}<circle cx="${mx}" cy="${my}" r="24" fill="${accent}" opacity=".18"/><circle cx="${mx}" cy="${my}" r="10" fill="${accent}"/></svg>`;
}
const mid = inner => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:150px;bottom:120px;display:flex;flex-direction:column;justify-content:center">${inner}</div>`;
const at = (pos, inner) => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;${pos}">${inner}</div>`;
const H1 = (t, s, size = 80) => `<h1 style="margin:0;font:400 ${size}px/1.04 'Albert Sans';letter-spacing:-.038em;color:${t.ink}">${s}</h1>`;
const P = (t, s, m = 30, size = 33) => `<p style="margin:${m}px 0 0;font:300 ${size}px/1.45 'Albert Sans';color:${t.muted}">${s}</p>`;

const SLIDES = [
  // 1 Cover: her corridor photograph
  frame('#070B17', DARK.ink, `${photoBg(photo('corridor.jpg'), '46% 50%')}${top(DARK, 'For healthcare providers')}
    ${at('bottom:130px', `${label(DARK, 'Zinlea Night &middot; Partnerships')}${H1(DARK, 'When the day ends, clinical responsibility <span style="color:#CCD9EF">doesn&rsquo;t.</span>', 84)}
      ${P(DARK, 'Who supports your care team when a resident&rsquo;s condition changes overnight?', 30, 34)}`)}`, 1),

  // 2 The operational challenge
  frame(MID, DARK.ink, `${top(DARK, '20:00 &mdash; 08:00')}
    ${mid(`${label(DARK, 'The night shift')}${H1(DARK, 'The night shift carries its own pressures.', 84)}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:50px">${['Staffing constraints', 'Changing patient needs', 'Clinical uncertainty', 'Escalation decisions'].map(x => pill(DARK, x)).join('')}</div>
      ${P(DARK, 'The responsibility does not diminish after hours.', 50, 36)}`)}`, 2),

  // 3 The evidence (white, two verified figures)
  frame(WHITE, LIGHT.ink, `${top(LIGHT, 'The evidence')}
    ${mid(`${label(LIGHT, 'Adult social care in England')}${H1(LIGHT, 'The pressure is documented.', 84)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:60px">
        <div style="border-top:2px solid #0E1116;padding-top:26px"><div style="font:300 150px/1 'Albert Sans';letter-spacing:-.05em;color:#2D4A8A">71%</div>
          <div style="margin-top:18px;font:400 30px/1.35 'Albert Sans'">of care locations surveyed found recruiting staff challenging.</div></div>
        <div style="border-top:2px solid #0E1116;padding-top:26px"><div style="font:300 150px/1 'Albert Sans';letter-spacing:-.05em;color:#2D4A8A">23%</div>
          <div style="margin-top:18px;font:400 30px/1.35 'Albert Sans'">staff turnover in care homes in 2025/26.</div></div>
      </div>
      <div style="margin-top:54px;font:400 21px/1.5 'DM Mono';color:#5A606B">Sources: DHSC Adult Social Care Workforce Survey, April 2025.<br>CQC, The State of Health Care and Adult Social Care in England 2025/26.</div>`)}`, 3),

  // 4 The human dimension
  frame('#070B17', DARK.ink, `${photoBg(photo('family.jpg'), '38% 40%')}${top(DARK, 'Families')}
    ${at('bottom:130px', `${H1(DARK, 'And what about the families?', 84)}
      ${P(DARK, 'A late-night telephone call. A sudden change in condition. Questions about what happens next.', 30, 34)}
      ${P(DARK, '<span style="color:#CCD9EF">For families, uncertainty can be as difficult as the wait itself.</span>', 22, 34)}`)}`, 4),

  // 5 The 2am question, with the dial
  frame(MID, DARK.ink, `${top(DARK, '02:00')}
    <div style="position:absolute;left:0;right:0;top:200px;display:flex;justify-content:center">${dial(600, '#EEF1F7', '#CCD9EF', 6)}</div>
    ${at('top:620px', `${H1(DARK, 'What happens when a clinical concern arises at 2am?', 76)}
      <div style="margin-top:40px">
        ${row(DARK, '?', 'Are escalation pathways clear?')}
        ${row(DARK, '?', 'Is the right clinical expertise accessible?')}
        ${row(DARK, '?', 'Can staff get timely professional guidance?')}
      </div>`)}`, 5),

  // 6 Introducing Zinlea Night
  frame('#070B17', DARK.ink, `${photoBg(photo('phonedoc.jpg'), '30% 35%')}${top(DARK, 'Introducing')}
    ${at('bottom:130px', `${label(DARK, 'Zinlea Night')}${H1(DARK, 'Clinical support beyond conventional hours.', 80)}
      ${P(DARK, 'Overnight clinical assessment, guidance and escalation from experienced Advanced Nurse Practitioners, 8pm to 8am.', 28, 32)}
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px">${['Supporting care teams', 'Strengthening clinical access', 'Keeping families in mind'].map(x => pill(DARK, x)).join('')}</div>`)}`, 6),

  // 7 Partnership invitation
  frame(MID, DARK.ink, `${top(DARK, 'zinlea.com')}
    <div style="position:absolute;left:0;right:0;top:200px;display:flex;justify-content:center">${dial(600, '#EEF1F7', '#CCD9EF')}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:150px;text-align:center">
      ${H1(DARK, 'Let&rsquo;s rethink overnight clinical support.', 80)}
      ${P(DARK, 'We welcome conversations with care providers, private hospitals and healthcare organisations in London.', 26, 31)}
      <div style="margin-top:22px;font:400 26px 'Albert Sans';color:#CCD9EF">Advanced clinical care. Overnight. Quietly available.</div>
      <div style="margin-top:38px;display:inline-flex;padding:20px 34px;border-radius:999px;background:#CCD9EF;color:#070B17;font:500 29px 'Albert Sans'">zinlea.com/night/partnerships</div>
      <div style="margin-top:20px;font:400 24px 'DM Mono';color:rgba(238,241,247,.7)">info@zinlea.com</div>
    </div>`, 7),
];

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  for (let i = 0; i < SLIDES.length; i++) {
    await pg.setContent(SLIDES[i]); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `zinlea-partners-v2-${i + 1}.png`) });
  }
  await b.close();
})();
