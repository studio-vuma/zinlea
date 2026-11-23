// Instagram highlight story sets for the overall Zinlea account, in each brand's colours:
// About (Health, white), How it works (Night, midnight), FAQ (Health, white), Zinlea Global (midnight + dawn).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const D = __dirname;
const W = 1080, H = 1920, PAD = 96;
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;

const T = {
  health: { bg: 'radial-gradient(70% 45% at 85% 8%,rgba(45,74,138,.10),transparent 70%),radial-gradient(80% 50% at 0% 100%,rgba(45,74,138,.08),transparent 70%),#FFFFFF',
    ink: '#0E1116', muted: '#5A606B', line: 'rgba(14,17,22,.12)', dot: '#2D4A8A', halo: 'rgba(45,74,138,.16)', accent: '#16213C', accentInk: '#FFFFFF', arc: '#2D4A8A', sub: 'health', surface: '#F3F4F6' },
  night: { bg: 'radial-gradient(60% 40% at 80% 12%,rgba(60,86,150,.45),transparent 70%),radial-gradient(120% 60% at 50% 110%,#16213C 0%,#070B17 60%)',
    ink: '#EEF1F7', muted: 'rgba(238,241,247,.74)', line: 'rgba(238,241,247,.14)', dot: '#CCD9EF', halo: 'rgba(204,217,239,.22)', accent: '#CCD9EF', accentInk: '#070B17', arc: '#CCD9EF', sub: 'night', surface: 'rgba(255,255,255,.06)' },
  global: { bg: 'radial-gradient(85% 32% at 50% 100%,rgba(255,206,160,.95) 0%,rgba(243,183,140,.75) 22%,rgba(122,86,100,.55) 50%,transparent 80%),linear-gradient(180deg,#08101F 0%,#0E1A35 45%,#2A2C50 75%,#5A4A64 100%)',
    ink: '#F4F0EB', muted: 'rgba(244,240,235,.76)', line: 'rgba(244,240,235,.14)', dot: '#F3B78C', halo: 'rgba(243,183,140,.28)', accent: '#F3B78C', accentInk: '#1B0F07', arc: '#F3B78C', sub: 'global', surface: 'rgba(255,255,255,.06)' },
};

function word(size, t) {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${t.ink}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${t.dot};box-shadow:0 0 0 ${h}px ${t.halo}"></span></span>nlea</span>`;
}
const brand = (t, sub = t.sub) => `<div style="display:flex;align-items:baseline;gap:10px">${word(38, t)}<span style="font:300 28px 'Albert Sans';color:${t.muted}">${sub}</span></div>`;
const arrow = t => `<svg width="120" height="20" viewBox="0 0 120 20"><path d="M0 10h116M108 2l8 8-8 8" fill="none" stroke="${t.ink}" stroke-width="2"/></svg>`;

function frame(t, inner, opts = {}) {
  const arcs = t === T.global ? '' : [0, 1, 2, 3].map(i => `<circle cx="${opts.flip ? 1080 : 0}" cy="1680" r="${260 + i * 90}" fill="none" stroke="${t.arc}" stroke-opacity="${(t === T.health ? .14 : .16) - i * 0.03}" stroke-width="${i === 0 ? 10 : 3}" ${i === 1 ? 'stroke-dasharray="2 16"' : ''} stroke-linecap="round"/>`).join('');
  const right = opts.right ?? (t === T.night ? '20:00 &mdash; 08:00' : t === T.global ? 'Across Africa' : 'zinlea.com');
  return `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${t.bg};color:${t.ink};font-family:'Albert Sans'">
    <svg style="position:absolute;inset:0" width="${W}" height="${H}">${arcs}</svg>
    <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:270px;display:flex;justify-content:space-between;align-items:center">${brand(t, opts.sub)}<span style="font:400 24px 'DM Mono';color:${t.muted}">${right}</span></div>
    ${inner}</div></body>`;
}
const at = (top, inner, center) => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:${top}px;${center ? 'text-align:center' : ''}">${inner}</div>`;
const h = (t, s, size = 80) => `<h1 style="margin:0;font:400 ${size}px/1.06 'Albert Sans';letter-spacing:-.035em;color:${t.ink}">${s}</h1>`;
const p = (t, s, m = 34, size = 38) => `<p style="margin:${m}px 0 0;font:300 ${size}px/1.45 'Albert Sans';color:${t.muted}">${s}</p>`;
const label = (t, s) => `<div style="display:inline-flex;align-items:center;gap:14px;font:500 28px 'Albert Sans';color:${t.muted};margin-bottom:34px"><span style="width:12px;height:12px;border-radius:50%;background:${t.dot};box-shadow:0 0 0 8px ${t.halo}"></span>${s}</div>`;
const pill = (t, s) => `<span style="display:inline-block;padding:16px 28px;border-radius:999px;border:1.5px solid ${t.line.replace(/[\d.]+\)$/, '.45)')};font:400 31px 'Albert Sans';color:${t.ink}">${s}</span>`;
const row = (t, a, b) => `<div style="display:flex;justify-content:space-between;gap:24px;padding:30px 0;border-top:1px solid ${t.line};font:400 34px 'Albert Sans'"><span style="color:${t.muted}">${a}</span><b style="font-weight:500;text-align:right">${b}</b></div>`;
const sticker = t => `<div style="margin:48px auto 0;width:640px;height:150px;border-radius:28px;border:2px dashed ${t.line.replace(/[\d.]+\)$/, '.5)')};display:flex;align-items:center;justify-content:center;font:400 24px 'DM Mono';color:${t.muted}">place link sticker here</div>`;

// Small brand "doors" used on the About story.
const door = (kind, title, sub, meta) => {
  const bg = kind === 'night' ? 'radial-gradient(120% 90% at 50% 110%,#1F2D52 0%,#070B17 70%)' : 'linear-gradient(180deg,#08101F 0%,#122142 38%,#4A4166 62%,#B97C72 72%,#2A2440 82%,#0B1224 100%)';
  const accent = kind === 'night' ? '#CCD9EF' : '#F3B78C';
  return `<div style="flex:1;height:520px;border-radius:32px;padding:32px;box-sizing:border-box;display:flex;flex-direction:column;background:${bg};color:#EEF1F7">
    <div style="display:flex;justify-content:space-between;font:400 20px 'DM Mono';color:rgba(238,241,247,.7)"><span>${meta[0]}</span><span>${meta[1]}</span></div>
    <div style="margin-top:auto;font:300 52px/1 'Albert Sans';letter-spacing:-.035em">Zinlea <span style="color:${accent}">${title}</span></div>
    <div style="margin-top:16px;font:300 25px/1.4 'Albert Sans';color:rgba(238,241,247,.8)">${sub}</div></div>`;
};

const SETS = {
  about: [
    frame(T.health, at(820, `${h(T.health, 'Meet Zinlea Health', 108)}${p(T.health, 'Who we are, and what we do.', 44, 42)}<div style="margin-top:40px">${arrow(T.health)}</div>`)),
    frame(T.health, at(620, `${label(T.health, 'Who we are')}${h(T.health, 'A private healthcare company, led by clinicians.', 84)}
      ${p(T.health, 'We make expert healthcare easier to reach at the moments it matters most: calm, private and unhurried, with clinical safety at the centre of every decision.')}`)),
    frame(T.health, at(560, `${label(T.health, 'What we do')}${h(T.health, 'Two services, one way of caring.', 80)}
      <div style="display:flex;gap:24px;margin-top:56px">
        ${door('night', 'Night', 'Overnight medical advice from senior nurses, by phone or video.', ['London', '20:00&ndash;08:00'])}
        ${door('global', 'Global', 'Healthcare partnerships, built together with partners across Africa.', ['Partnerships', 'Africa'])}
      </div>`)),
    frame(T.health, at(600, `${label(T.health, 'How we work')}${h(T.health, 'The principles behind every call.', 80)}
      <div style="margin-top:50px">${row(T.health, 'How we speak to you', 'Calm expertise')}${row(T.health, 'How we treat your information', 'Discretion')}${row(T.health, 'How we stay with you', 'Continuity')}${row(T.health, 'How we keep you safe', 'Safety first')}</div>`)),
    frame(T.health, at(660, `${h(T.health, 'Find out more', 92)}
      <div style="margin-top:50px">${row(T.health, 'Website', 'zinlea.com')}${row(T.health, 'Email', 'info@zinlea.com')}${row(T.health, 'Instagram', '@zinleanight')}</div>${sticker(T.health)}`)),
  ],

  'how-it-works': [
    frame(T.night, at(820, `${h(T.night, 'How Zinlea Night works', 108)}${p(T.night, 'From your first message to your first call.', 44, 42)}<div style="margin-top:40px">${arrow(T.night)}</div>`)),
    ...[
      ['Step 1 &middot; Today', 'Request membership', 'Send a short enquiry through zinlea.com. Choose individual or family membership.'],
      ['Step 2 &middot; Within 24 hours', 'We reply personally', 'A member of our team gets back to you, usually the same day.'],
      ['Step 3 &middot; Onboarding call', 'We get to know you', 'A brief call to understand your needs, your household and your history.'],
      ['Step 4 &middot; From 20:00', 'Call when you need us', 'Any time between 8pm and 8am, by phone or video, you speak directly to a senior nurse.'],
    ].map(([k, t1, s], i) => frame(T.night, at(700, `<div style="font:400 30px 'DM Mono';color:#CCD9EF;margin-bottom:40px">${k}</div>${h(T.night, t1, 96)}${p(T.night, s, 40, 40)}
      <div style="display:flex;gap:10px;margin-top:80px">${[0, 1, 2, 3].map(j => `<span style="height:6px;flex:1;border-radius:3px;background:${j <= i ? '#CCD9EF' : 'rgba(238,241,247,.16)'}"></span>`).join('')}</div>`), { flip: i % 2 })),
    frame(T.night, at(560, `${label(T.night, 'On the call')}${h(T.night, 'What happens when you call', 80)}
      ${p(T.night, 'An experienced Advanced Nurse Practitioner will:', 34, 36)}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:40px">${['Listen', 'Assess', 'Advise', 'Prescribe where appropriate', 'Escalate when needed'].map(x => pill(T.night, x)).join('')}</div>
      <div style="margin-top:70px;padding:30px 34px;border-radius:24px;background:rgba(240,138,114,.12);font:400 31px/1.4 'Albert Sans'"><span style="font-family:'DM Mono';color:#F08A72">999</span>&nbsp; In an emergency, always call 999 or go to A&amp;E.</div>`)),
    frame(T.night, at(720, `${h(T.night, 'Ready to join?', 96)}${p(T.night, 'Request membership here', 40, 40)}${sticker(T.night)}
      <p style="margin:56px 0 0;font:400 30px 'DM Mono';color:${T.night.muted}">zinlea.com/night/membership</p>`, true)),
  ],

  faq: [
    frame(T.health, at(820, `${h(T.health, 'Your questions, answered', 108)}${p(T.health, 'The things people ask us most.', 44, 42)}<div style="margin-top:40px">${arrow(T.health)}</div>`)),
    ...[
      ['Who will I speak to?', 'An experienced Advanced Nurse Practitioner, a senior nurse with a background in urgent, primary or acute care.'],
      ['Can you prescribe medication?', 'Yes, where it is clinically appropriate and safe, after a proper assessment. Some medicines cannot be prescribed remotely.'],
      ['Is Zinlea Night an emergency service?', 'No. For chest pain, difficulty breathing, signs of stroke or any life-threatening symptoms, call 999 or go to A&amp;E.'],
      ['Does it replace my GP?', 'No. Zinlea Night works alongside your GP and NHS services, which remain your home for long-term care.'],
      ['How much is membership?', 'Individual from &pound;85 a month. Family from &pound;225 a month. Private Client and partnerships are tailored.'],
      ['Is Zinlea regulated?', 'Zinlea Night has applied for registration with the Care Quality Commission (CQC). Our application is under review.'],
    ].map(([q, a], i) => frame(T.health, at(660, `<div style="font:400 30px 'DM Mono';color:${T.health.dot};margin-bottom:40px">Q${i + 1}</div>${h(T.health, q, 84)}
      <div style="margin-top:48px;padding-top:40px;border-top:1px solid ${T.health.line};font:300 40px/1.45 'Albert Sans';color:${T.health.muted}">${a}</div>`), { flip: i % 2 })),
    frame(T.health, at(720, `${h(T.health, 'Still have a question?', 92)}${p(T.health, 'Read the full FAQ or ask us directly', 40, 40)}${sticker(T.health)}
      <p style="margin:56px 0 0;font:400 30px 'DM Mono';color:${T.health.muted}">zinlea.com/faq</p>`, true)),
  ],

  global: [
    frame(T.global, at(720, `${h(T.global, 'Zinlea Global', 112)}${p(T.global, 'Healthcare partnerships, built together.', 44, 44)}<div style="margin-top:40px">${arrow(T.global)}</div>`)),
    frame(T.global, at(600, `${label(T.global, 'What it is')}${h(T.global, 'Partners across Africa&rsquo;s healthcare sector.', 80)}
      ${p(T.global, 'Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new services together, as equal partners from the very first conversation.')}`)),
    frame(T.global, at(560, `${label(T.global, 'Who we work with')}${h(T.global, 'Building alongside', 84)}
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:50px">${['Hospital groups', 'Private clinics', 'Clinicians', 'Investors', 'Development partners'].map(x => pill(T.global, x)).join('')}</div>
      ${p(T.global, 'Zinlea Global is in development. We are speaking with prospective founding partners now.', 60, 36)}`)),
    frame(T.global, at(700, `${h(T.global, 'Register your interest', 92)}${p(T.global, 'Tell us about your organisation', 40, 40)}${sticker(T.global)}
      <p style="margin:56px 0 0;font:400 30px 'DM Mono';color:${T.global.muted}">zinlea.com/global</p>`, true)),
  ],
};

// Highlight covers in each brand's colours.
const ICON = {
  about: '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v6M12 7.5v.01"/>',
  global: '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5a14 14 0 0 1 0 19M12 2.5a14 14 0 0 0 0 19"/>',
  faq: '<circle cx="12" cy="12" r="9.5"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 1c0 1.8-2.5 2.2-2.5 4M12 17.5v.01"/>',
  steps: '<path d="M4 18h5v-5h5V8h5V4"/>',
};
const cover = (bg, ring, stroke, key) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;background:${bg}">
  <div style="position:absolute;left:50%;top:50%;width:820px;height:820px;transform:translate(-50%,-50%);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 3px ${ring}">
  <svg width="440" height="440" viewBox="0 0 24 24" fill="none" stroke="${stroke}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">${ICON[key]}</svg></div></div></body>`;
const COVERS = {
  'about-health': cover('radial-gradient(70% 40% at 50% 50%,#F3F5F9 0%,#FFFFFF 70%)', 'rgba(45,74,138,.18)', '#16213C', 'about'),
  'faq-health': cover('radial-gradient(70% 40% at 50% 50%,#F3F5F9 0%,#FFFFFF 70%)', 'rgba(45,74,138,.18)', '#16213C', 'faq'),
  'how-it-works-night': cover('radial-gradient(70% 40% at 50% 50%,#1B2747 0%,#070B17 70%)', 'rgba(204,217,239,.2)', '#CCD9EF', 'steps'),
  'global-dawn': cover('radial-gradient(70% 45% at 50% 70%,#7A5664 0%,#1A2448 45%,#08101F 75%)', 'rgba(243,183,140,.3)', '#F3B78C', 'global'),
};

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const [set, slides] of Object.entries(SETS)) {
    for (let i = 0; i < slides.length; i++) {
      await pg.setContent(slides[i]);
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(250);
      await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `${set}-${i + 1}.png`) });
    }
  }
  for (const [k, html] of Object.entries(COVERS)) {
    await pg.setContent(html);
    await pg.waitForTimeout(120);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `highlight-cover-${k}.png`) });
  }
  await b.close();
})();
