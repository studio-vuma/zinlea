/* Zinlea — site behaviour: header, menu, live London night clock, enquiry form. */
(function () {
  'use strict';

  /* Header hairline once the page scrolls. */
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Menu drawer. */
  var drawer = document.getElementById('drawer');
  var openBtn = document.querySelector('.menu-btn');
  var closeBtn = drawer && drawer.querySelector('.drawer-close');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    (open ? closeBtn : openBtn) && (open ? closeBtn : openBtn).focus();
  }
  if (openBtn) openBtn.addEventListener('click', function () { setDrawer(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setDrawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) setDrawer(false); });
  if (drawer) drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setDrawer(false); }); });

  /* Live London clock: Zinlea Night runs 20:00–08:00. */
  var fmt;
  try { fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }); }
  catch (e) { fmt = null; }

  function londonNow() {
    var d = new Date();
    if (!fmt) return { h: d.getHours(), m: d.getMinutes() };
    var parts = fmt.formatToParts(d);
    var h = 0, m = 0;
    parts.forEach(function (p) { if (p.type === 'hour') h = +p.value; if (p.type === 'minute') m = +p.value; });
    return { h: h % 24, m: m };
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  // Dial geometry must match build.py: centre (260,270), radius 220, 20:00 at left, 08:00 at right.
  var CX = 260, CY = 270, R = 220;
  function point(t) { // t = minutes since 20:00, 0..720
    var a = Math.PI - (t / 720) * Math.PI;
    return { x: CX + R * Math.cos(a), y: CY - R * Math.sin(a) };
  }

  function tick() {
    var now = londonNow();
    var mins = now.h * 60 + now.m;
    var t = (mins - 1200 + 1440) % 1440;
    var open = t < 720;
    var clock = pad(now.h) + ':' + pad(now.m);
    var pos = open ? t : (t < 1080 ? 720 : 0); // after 08:00 rest at the end, later in the day wait at the start

    document.querySelectorAll('[data-dial]').forEach(function (svg) {
      var p = point(pos);
      var marker = svg.querySelector('.marker');
      var halo = svg.querySelector('.marker-halo');
      var elapsed = svg.querySelector('.elapsed');
      if (marker) { marker.setAttribute('cx', p.x.toFixed(1)); marker.setAttribute('cy', p.y.toFixed(1)); }
      if (halo) { halo.setAttribute('cx', p.x.toFixed(1)); halo.setAttribute('cy', p.y.toFixed(1)); }
      if (elapsed) elapsed.setAttribute('d', open && t > 0 ? 'M 40 270 A 220 220 0 0 1 ' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) : '');
      svg.classList.toggle('closed', !open);
      svg.setAttribute('aria-label', open
        ? 'Zinlea Night is open. It is ' + clock + ' in London; members can call until 08:00.'
        : 'Zinlea Night is closed. It is ' + clock + ' in London; the service opens at 20:00.');
    });
    document.querySelectorAll('[data-clock]').forEach(function (el) { el.textContent = clock; });
    document.querySelectorAll('[data-open-state]').forEach(function (el) {
      el.classList.toggle('open', open);
      var title = el.querySelector('[data-state-title]');
      var sub = el.querySelector('[data-state-sub]');
      if (title) title.textContent = open ? 'Zinlea Night is open' : 'Zinlea Night opens at 20:00';
      if (sub) sub.textContent = open ? 'Clinicians available until 08:00, London' : 'Overnight clinical advice, 8pm to 8am';
    });
    document.querySelectorAll('[data-status-short]').forEach(function (el) {
      el.innerHTML = (open ? '<b>Open now</b>' : '<b>Opens 20:00</b>') + ' &middot; ' + clock + ' London';
    });
  }
  tick();
  setInterval(tick, 30000);

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Enquiry form. */
  var form = document.querySelector('form[data-enquiry]');
  if (!form) return;
  var type = new URLSearchParams(window.location.search).get('type');
  if (type) {
    var r = form.querySelector('input[name="inquiry-type"][value="' + type.replace(/[^a-z-]/g, '') + '"]');
    if (r) r.checked = true;
  }
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function check(fld) {
    var radios = fld.querySelectorAll('input[type="radio"]');
    var ok;
    if (radios.length) {
      ok = Array.prototype.some.call(radios, function (x) { return x.checked; });
    } else {
      var input = fld.querySelector('input, textarea');
      if (!input) return true;
      var v = (input.value || '').trim();
      ok = !(input.required && !v) && !(input.type === 'email' && v && !emailRe.test(v));
      input.setAttribute('aria-invalid', String(!ok));
    }
    fld.classList.toggle('invalid', !ok);
    return ok;
  }
  form.querySelectorAll('.fld').forEach(function (fld) {
    fld.querySelectorAll('input, textarea').forEach(function (input) {
      input.addEventListener(input.type === 'radio' ? 'change' : 'blur', function () { check(fld); });
      input.addEventListener('input', function () { if (fld.classList.contains('invalid')) check(fld); });
    });
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = null;
    form.querySelectorAll('.fld').forEach(function (f) { if (!check(f) && !bad) bad = f; });
    var consent = form.querySelector('input[name="consent"]');
    var wrapC = consent && consent.closest('.check');
    if (wrapC) wrapC.classList.toggle('invalid', !consent.checked);
    if (bad) { var first = bad.querySelector('input, textarea'); if (first) first.focus(); return; }
    if (consent && !consent.checked) { consent.focus(); return; }
    var btn = form.querySelector('button[type="submit"]');
    var label = btn.innerHTML;
    var status = form.querySelector('.form-status');
    btn.disabled = true;
    btn.textContent = 'Sending…';
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(form)).toString()
    }).then(function (res) {
      if (!res.ok) throw new Error('failed');
      window.location.href = '/thank-you/';
    }).catch(function () {
      btn.disabled = false;
      btn.innerHTML = label;
      if (status) status.textContent = 'Your message could not be sent. Please email info@zinlea.com instead.';
    });
  });
})();
