/* Zinlea Health — public site interactions (no dependencies). */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  // Header: solid background once the page is scrolled.
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 24); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu.
  var toggle = document.querySelector('.menu-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    header.querySelectorAll('.mobile-menu a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('menu-open')) {
        header.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Reveal-on-scroll.
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year.
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Enquiry form: inline validation + Netlify Forms submission.
  var form = document.querySelector('form[data-enquiry]');
  if (!form) return;

  // Pre-select the division when arriving from a division page link (?interest=night|global).
  var interest = new URLSearchParams(window.location.search).get('interest');
  var select = form.querySelector('select[name="interest"]');
  if (interest && select) {
    var opt = select.querySelector('option[value="' + interest.replace(/[^a-z-]/g, '') + '"]');
    if (opt) select.value = opt.value;
  }

  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validateField(field) {
    var input = field.querySelector('input,select,textarea');
    if (!input) return true;
    var v = (input.value || '').trim();
    var ok = true;
    if (input.required && !v) ok = false;
    if (ok && input.type === 'email' && v && !emailRe.test(v)) ok = false;
    field.classList.toggle('invalid', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    return ok;
  }
  form.querySelectorAll('.field').forEach(function (field) {
    var input = field.querySelector('input,select,textarea');
    if (!input) return;
    input.addEventListener('blur', function () { validateField(field); });
    input.addEventListener('input', function () { if (field.classList.contains('invalid')) validateField(field); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var fields = Array.prototype.slice.call(form.querySelectorAll('.field'));
    var firstBad = null;
    fields.forEach(function (f) { if (!validateField(f) && !firstBad) firstBad = f; });
    var consent = form.querySelector('input[name="consent"]');
    if (consent && !consent.checked) {
      consent.focus();
      consent.closest('.consent').style.color = 'var(--earth-600)';
      return;
    }
    if (firstBad) { firstBad.querySelector('input,select,textarea').focus(); return; }

    var btn = form.querySelector('button[type="submit"]');
    var label = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = 'Sending…';
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(form)).toString()
    }).then(function (res) {
      if (!res.ok) throw new Error('Request failed');
      window.location.href = '/thank-you/';
    }).catch(function () {
      btn.disabled = false;
      btn.innerHTML = label;
      var note = form.querySelector('.form-status');
      if (note) note.textContent = 'Sorry — your message could not be sent. Please try again in a moment.';
    });
  });
})();
