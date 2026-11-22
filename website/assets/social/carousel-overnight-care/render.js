// Zinlea Night educational carousel: "Overnight care" (7 slides, 1080x1350).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const D = __dirname;
const photo = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, f)).toString('base64');

const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;
const W = 1080, H = 1350, PAD = 84;
const MOON = '#CCD9EF', INK = '#EEF1F7';

function word(size, ink = INK, dot = MOON, halo = 'rgba(204,217,239,.22)') {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${ink}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${dot};box-shadow:0 0 0 ${h}px ${halo}"></span></span>nlea</span>`;
}
const brand = (ink = INK, sub = 'rgba(238,241,247,.7)', dot = MOON, halo) =>
  `<div style="display:flex;align-items:baseline;gap:10px">${word(34, ink, dot, halo)}<span style="font:300 25px 'Albert Sans';color:${sub}">night</span></div>`;
const arrow = c => `<svg width="64" height="18" viewBox="0 0 64 18" style="display:block"><path d="M0 9h60M53 2l7 7-7 7" fill="none" stroke="${c}" stroke-width="2"/></svg>`;
const pill = (t, c = INK, b = 'rgba(238,241,247,.55)') => `<span style="display:inline-block;padding:14px 26px;border-radius:999px;border:1.5px solid ${b};color:${c};font:400 29px 'Albert Sans';letter-spacing:-.01em">${t}</span>`;

function dial(w, ink, accent, pos = 6.2) {
  const cx = 260, cy = 270, r = 220; let t = '';
  for (let h = 0; h <= 12; h++) {
    const a = Math.PI - (h / 12) * Math.PI, major = h % 2 === 0, r1 = r + 8, r2 = r + (major ? 20 : 14);
    t += `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy - r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy - r2 * Math.sin(a)}" stroke="${ink}" stroke-opacity="${major ? .55 : .28}" stroke-width="2"/>`;
    if (major) t += `<text x="${cx + (r + 46) * Math.cos(a)}" y="${cy - (r + 46) * Math.sin(a) + 7}" text-anchor="middle" font-family="DM Mono" font-size="21" fill="${ink}" fill-opacity=".6">${String((20 + h) % 24).padStart(2, '0')}</text>`;
  }
  const at = Math.PI - (pos / 12) * Math.PI, mx = cx + r * Math.cos(at), my = cy - r * Math.sin(at);
  return `<svg viewBox="-24 0 568 300" width="${w}" style="display:block;overflow:visible">
    <path d="M 40 270 A 220 220 0 0 1 480 270" fill="none" stroke="${ink}" stroke-opacity=".16" stroke-width="2"/>
    <path d="M 40 270 A 220 220 0 0 1 ${mx} ${my}" fill="none" stroke="${accent}" stroke-width="3" stroke-linecap="round"/>${t}
    <circle cx="${mx}" cy="${my}" r="24" fill="${accent}" opacity=".18"/><circle cx="${mx}" cy="${my}" r="10" fill="${accent}"/></svg>`;
}

// Full-bleed photo with a dark gradient so text sits on calm ground.
const photoBg = (img, pos = '50% 50%', tint = 'rgba(7,11,23,.0)', grad = 'linear-gradient(180deg,rgba(7,11,23,.7) 0%,rgba(7,11,23,.25) 14%,rgba(7,11,23,0) 26%,rgba(7,11,23,.15) 45%,rgba(7,11,23,.88) 78%,rgba(7,11,23,.96) 100%)') =>
  `<img src="${img}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${pos};filter:saturate(.85)">
   <div style="position:absolute;inset:0;background:${tint}"></div><div style="position:absolute;inset:0;background:${grad}"></div>`;

const frame = (inner, bg = '#070B17', color = INK) =>
  `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${bg};color:${color};font-family:'Albert Sans'">${inner}</div></body>`;
const top = (b, right = '') => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:72px;display:flex;justify-content:space-between;align-items:center;z-index:2">${b}${right}</div>`;
const mono = (t, c) => `<span style="font:400 22px 'DM Mono';color:${c}">${t}</span>`;

const SLIDES = [
  // 1. Cover
  frame(`${photoBg(photo('london.jpg'), '50% 40%')}
    ${top(brand(), mono('02:00', 'rgba(238,241,247,.75)'))}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:96px">
      <h1 style="margin:0;font:400 88px/1.02 'Albert Sans';letter-spacing:-.04em">What happens when someone feels unwell <span style="color:${MOON}">at 2am?</span></h1>
      <p style="margin:30px 0 36px;font:300 34px/1.4 'Albert Sans';color:rgba(238,241,247,.85);max-width:820px">Most healthcare runs on office hours. Worry doesn&rsquo;t.</p>
      ${arrow(INK)}
    </div>`),

  // 2. Why nights are harder
  frame(`${photoBg(photo('bedroom.jpg'), '30% 50%', 'rgba(10,18,44,.55)')}
    ${top(brand())}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:110px">
      <h2 style="margin:0;font:400 76px/1.05 'Albert Sans';letter-spacing:-.035em">The night is when uncertainty feels loudest.</h2>
      <p style="margin:32px 0 0;font:300 34px/1.45 'Albert Sans';color:rgba(238,241,247,.85)">GP surgeries are closed, fewer services are available, and it can be hard to know whether something can safely wait until morning.</p>
    </div>`),

  // 3. Common worries (pills)
  frame(`${photoBg(photo('hands.jpg'), '55% 50%')}
    ${top(brand())}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:110px;text-align:center">
      <h2 style="margin:0 auto;font:400 66px/1.08 'Albert Sans';letter-spacing:-.035em;max-width:860px">The worries that tend to arrive after dark</h2>
      <p style="margin:26px 0 38px;font:300 32px 'Albert Sans';color:rgba(238,241,247,.85)">Families often call about:</p>
      <div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center">
        ${pill('A rising temperature')}${pill('A new or changing symptom')}${pill('Medication questions')}${pill('An older relative who seems different')}${pill('Whether it can wait')}
      </div>
    </div>`),

  // 4. Light slide with the dial
  frame(`${top(brand('#0E1116', '#5A606B', '#2D4A8A', 'rgba(45,74,138,.16)'), mono('20:00 &mdash; 08:00', '#5A606B'))}
    <div style="position:absolute;left:0;right:0;top:400px;display:flex;justify-content:center">${dial(760, '#0E1116', '#2D4A8A', 6.2)}</div>
    <div style="position:absolute;left:${PAD + 20}px;right:${PAD + 20}px;top:900px;text-align:center">
      <p style="margin:0;font:300 50px/1.25 'Albert Sans';letter-spacing:-.025em;color:#0E1116">Twelve hours, every night, when the right advice can mean <b style="font-weight:500">a calmer night and the right care at the right time.</b></p>
    </div>`, '#F3F4F6', '#0E1116'),

  // 5. What overnight clinical advice looks like
  frame(`${photoBg(photo('nurse.jpg'), '50% 30%')}
    ${top(brand())}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:110px">
      <h2 style="margin:0;font:400 70px/1.05 'Albert Sans';letter-spacing:-.035em">What good overnight clinical advice looks like</h2>
      <p style="margin:28px 0 36px;font:300 32px/1.45 'Albert Sans';color:rgba(238,241,247,.85)">A conversation with an experienced Advanced Nurse Practitioner, by phone or video, that ends with a clear next step.</p>
      <div style="display:flex;flex-wrap:wrap;gap:14px">${pill('Listen')}${pill('Assess')}${pill('Advise')}${pill('Prescribe where appropriate')}${pill('Escalate when needed')}</div>
    </div>`),

  // 6. Safety: know when it's 999
  frame(`${top(brand('#0E1116', '#5A606B', '#2D4A8A', 'rgba(45,74,138,.16)'))}
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:300px">
      <div style="font:400 200px/1 'DM Mono';color:#C0452F;letter-spacing:-.04em">999</div>
      <h2 style="margin:30px 0 0;font:400 70px/1.05 'Albert Sans';letter-spacing:-.035em;color:#0E1116">Some nights can&rsquo;t wait for advice.</h2>
      <p style="margin:26px 0 34px;font:300 33px/1.45 'Albert Sans';color:#5A606B">Call 999 or go to A&amp;E straight away for:</p>
      <div style="display:flex;flex-wrap:wrap;gap:14px">
        ${['Chest pain', 'Difficulty breathing', 'Signs of stroke', 'Severe bleeding', 'Loss of consciousness'].map(t => pill(t, '#0E1116', 'rgba(14,17,22,.35)')).join('')}
      </div>
    </div>
    <p style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:90px;margin:0;font:400 24px/1.4 'Albert Sans';color:#5A606B">Overnight clinical advice complements emergency services. It never replaces them.</p>`, '#FFFFFF', '#0E1116'),

  // 7. Zinlea Night
  frame(`<div style="position:absolute;inset:0;background:radial-gradient(110% 70% at 50% 108%,#1F2D52 0%,#070B17 62%)"></div>
    ${top(brand(), mono('zinlea.com', 'rgba(238,241,247,.7)'))}
    <div style="position:absolute;left:0;right:0;top:230px;display:flex;justify-content:center">${dial(700, INK, MOON, 6.2)}</div>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:100px;text-align:center">
      <h2 style="margin:0;font:400 76px/1.04 'Albert Sans';letter-spacing:-.04em">Overnight medical advice, <span style="color:${MOON}">8pm to 8am.</span></h2>
      <p style="margin:28px auto 40px;font:300 32px/1.45 'Albert Sans';color:rgba(238,241,247,.82);max-width:860px">Zinlea Night gives members in London direct access to experienced Advanced Nurse Practitioners, through the night.</p>
      <span style="display:inline-flex;align-items:center;gap:14px;padding:20px 34px;border-radius:999px;background:${MOON};color:#070B17;font:500 30px 'Albert Sans'">Founding membership at zinlea.com</span>
    </div>`),
];

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (let i = 0; i < SLIDES.length; i++) {
    await pg.setContent(SLIDES[i]);
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(350);
    await (await pg.$('#c')).screenshot({ path: path.join(D, `zinlea-night-carousel-${i + 1}.png`) });
  }
  await b.close();
})();
