/* Zinlea Health — website interactions (no dependencies). */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');

  /* Sticky header: transparent over the hero, solid ivory once scrolled past it. */
  var header = document.querySelector('.site-header');
  if (header && !header.classList.contains('solid')) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 520); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  } else if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('is-stuck', window.scrollY > 120);
    }, { passive: true });
  }

  /* Full-screen menu drawer. */
  var drawer = document.getElementById('drawer');
  var openBtn = document.querySelector('.menu-btn');
  var closeBtn = drawer && drawer.querySelector('.drawer-close');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open && closeBtn) closeBtn.focus();
    if (!open && openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', function () { setDrawer(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setDrawer(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) setDrawer(false);
  });
  if (drawer) drawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { setDrawer(false); });
  });

  /* Reveal on scroll. */
  var els = document.querySelectorAll('.rv, .reveal-img');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Enquiry form: inline validation, then submit to Netlify Forms. */
  var form = document.querySelector('form[data-enquiry]');
  if (!form) return;

  var type = new URLSearchParams(window.location.search).get('type');
  var sel = form.querySelector('select[name="inquiry-type"]');
  if (type && sel && sel.querySelector('option[value="' + type.replace(/[^a-z-]/g, '') + '"]')) sel.value = type;

  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function check(fld) {
    var input = fld.querySelector('input, select, textarea');
    if (!input) return true;
    var v = (input.value || '').trim();
    var ok = !(input.required && !v) && !(input.type === 'email' && v && !emailRe.test(v));
    fld.classList.toggle('invalid', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    return ok;
  }
  form.querySelectorAll('.fld').forEach(function (fld) {
    var input = fld.querySelector('input, select, textarea');
    if (!input) return;
    input.addEventListener('blur', function () { check(fld); });
    input.addEventListener('input', function () { if (fld.classList.contains('invalid')) check(fld); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = null;
    form.querySelectorAll('.fld').forEach(function (f) { if (!check(f) && !bad) bad = f; });
    var consent = form.querySelector('input[name="consent"]');
    var consentWrap = consent && consent.closest('.check');
    if (consent && !consent.checked) { consentWrap.classList.add('invalid'); if (!bad) consent.focus(); }
    else if (consentWrap) consentWrap.classList.remove('invalid');
    if (bad) { bad.querySelector('input, select, textarea').focus(); return; }
    if (consent && !consent.checked) return;

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
      if (status) status.textContent = 'Sorry, your message could not be sent. Please email info@zinlea.com.';
    });
  });
})();
