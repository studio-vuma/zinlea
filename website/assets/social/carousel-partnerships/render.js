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
const page = n => `<div style="position:absolute;right:${PAD}px;bottom:64px;font:400 20px 'DM Mono';color:inherit;opacity:.55">${String(n).padStart(2, '0')} / 08</div>`;
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
  // 1 Cover: white, to contrast with the dark 2am post beside it on the grid
  frame(WHITE, LIGHT.ink, `${top(LIGHT, 'For care providers')}
    ${at('top:230px', `${label(LIGHT, 'Zinlea Night &middot; Partnerships')}${H1(LIGHT, 'Clinical support beyond <span style="color:#2D4A8A">conventional hours.</span>', 96)}
      ${P(LIGHT, 'Overnight clinical support for care homes and healthcare organisations in London.', 34, 36)}`)}
    <div style="position:absolute;left:0;right:0;bottom:120px;display:flex;justify-content:center">${dial(640, '#0E1116', '#2D4A8A')}</div>`, 1),

  // 2 The problem
  frame('#070B17', DARK.ink, `${photoBg(photo('carehome.jpg'), '50% 35%')}${top(DARK, '20:00 &mdash; 08:00')}
    ${at('bottom:130px', `${H1(DARK, 'The day team goes home. Responsibility doesn&rsquo;t.', 78)}
      ${P(DARK, 'Overnight, care teams make difficult decisions with the least clinical support available. That is when expert advice matters most.')}`)}`, 2),

  // 3 Who we partner with
  frame(WHITE, LIGHT.ink, `${top(LIGHT, 'zinlea.com')}
    ${mid(`${label(LIGHT, 'Who we work with')}${H1(LIGHT, 'Built for organisations that care through the night.', 76)}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:56px">${['Care homes', 'Residential care', 'Private hospitals', 'Private GP practices', 'Family offices', 'Corporate healthcare providers'].map(x => pill(LIGHT, x)).join('')}</div>
      ${P(LIGHT, 'We partner with a small number of carefully selected organisations, so every partnership gets our full attention.', 56, 31)}`)}`, 3),

  // 4 What partners receive
  frame(MID, DARK.ink, `${top(DARK, '20:00 &mdash; 08:00')}
    ${mid(`${label(DARK, 'What partners receive')}${H1(DARK, 'An extension of your team, overnight.', 76)}
      <div style="margin-top:44px">
        ${row(DARK, '01', 'Overnight clinical decision support', 'Expert advice for your staff, 8pm to 8am')}
        ${row(DARK, '02', 'Triage and remote consultation', 'By phone or video, with clear next steps')}
        ${row(DARK, '03', 'Prescribing', 'Where clinically appropriate, after proper assessment')}
        ${row(DARK, '04', 'Governance-led escalation', 'Aligned with your existing care model')}
      </div>`)}`, 4),

  // 5 Clinicians
  frame('#070B17', DARK.ink, `${photoBg(photo('nursephone.jpg'), '58% 30%')}${top(DARK, 'Our clinicians')}
    ${at('bottom:130px', `${H1(DARK, 'Delivered by Advanced Nurse Practitioners.', 78)}
      ${P(DARK, 'Experienced senior nurses with backgrounds across urgent care, primary care and acute services, trained in remote consultation safety and safeguarding.')}`)}`, 5),

  // 6 Governance
  frame(WHITE, LIGHT.ink, `${top(LIGHT, 'Clinical governance')}
    ${mid(`${label(LIGHT, 'Safety and accountability')}${H1(LIGHT, 'Governance first, by design.', 80)}
      <div style="margin-top:44px">
        ${row(LIGHT, 'CQC', 'Registration application submitted', 'Currently under review')}
        ${row(LIGHT, '&mdash;', 'Clear clinical protocols and escalation')}
        ${row(LIGHT, '&mdash;', 'Incident reporting and clinical audit')}
        ${row(LIGHT, '&mdash;', 'Adult and child safeguarding')}
        ${row(LIGHT, '&mdash;', 'UK GDPR and medical confidentiality')}
      </div>`)}`, 6),

  // 7 How partnership works
  frame(MID, DARK.ink, `${top(DARK, 'Partnerships')}
    ${mid(`${label(DARK, 'How partnership works')}${H1(DARK, 'Tailored to your setting.', 80)}
      <div style="margin-top:44px">
        ${row(DARK, 'Step 1', 'An introductory conversation', 'About your setting, people and overnight pressures')}
        ${row(DARK, 'Step 2', 'Clinical suitability', 'We confirm our remote model is right for you')}
        ${row(DARK, 'Step 3', 'A tailored monthly partnership', 'Clear scope, clinical model and terms')}
        ${row(DARK, 'Step 4', 'Ongoing review', 'So the partnership keeps improving')}
      </div>`)}`, 7),

  // 8 CTA
  frame(MID, DARK.ink, `${top(DARK, 'zinlea.com')}
    <div style="position:absolute;left:0;right:0;top:210px;display:flex;justify-content:center">${dial(640, '#EEF1F7', '#CCD9EF')}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:150px;text-align:center">
      ${H1(DARK, 'Advanced clinical care. <span style="color:#CCD9EF">Overnight.</span>', 80)}
      ${P(DARK, 'We are onboarding a limited number of London partners. Start with a conversation.', 26, 31)}
      <div style="margin-top:40px;display:inline-flex;padding:20px 34px;border-radius:999px;background:#CCD9EF;color:#070B17;font:500 29px 'Albert Sans'">zinlea.com/night/partnerships</div>
      <div style="margin-top:22px;font:400 24px 'DM Mono';color:rgba(238,241,247,.7)">info@zinlea.com</div>
    </div>`, 8),
];

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  for (let i = 0; i < SLIDES.length; i++) {
    await pg.setContent(SLIDES[i]); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `zinlea-partners-${i + 1}.png`) });
  }
  await b.close();
})();
