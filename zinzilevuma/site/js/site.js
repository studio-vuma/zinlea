(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  // Header hairline once the page scrolls
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var menu = document.getElementById('mobile-nav');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Close' : 'Menu';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); btn.textContent = 'Menu'; btn.focus(); }
    });
  }

  // Quiet reveal as sections enter the screen
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Enquiry form
  var form = document.getElementById('enquiry');
  if (!form) return;

  var params = new URLSearchParams(window.location.search);
  var area = params.get('area');
  if (area && form.area) {
    Array.prototype.forEach.call(form.area.options, function (o) { if (o.value === area) o.selected = true; });
  }

  var rules = {
    name: function (v) { return v ? '' : 'Please give your name.'; },
    organisation: function (v) { return v ? '' : 'Please give the name of your organisation.'; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Please enter an email address I can reply to.'; },
    message: function (v) { return v.length >= 10 ? '' : 'Please share a few words about your enquiry.'; }
  };
  function check(id) {
    var field = form.elements[id];
    var msg = rules[id](field.value.trim());
    field.setAttribute('aria-invalid', msg ? 'true' : 'false');
    document.getElementById('e-' + id).textContent = msg;
    return !msg;
  }
  Object.keys(rules).forEach(function (id) {
    var f = form.elements[id];
    f.addEventListener('blur', function () { if (f.value) check(id); });
    f.addEventListener('input', function () { if (f.getAttribute('aria-invalid') === 'true') check(id); });
  });

  form.addEventListener('submit', function (e) {
    var firstBad = null;
    Object.keys(rules).forEach(function (id) { if (!check(id) && !firstBad) firstBad = form.elements[id]; });
    if (firstBad) { e.preventDefault(); firstBad.focus(); return; }
    if (!window.fetch) return; // fall back to a normal form post
    e.preventDefault();
    var submit = form.querySelector('[type="submit"]');
    submit.disabled = true; submit.textContent = 'Sending';
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
      .then(function (r) {
        if (!r.ok) throw new Error('Request failed');
        form.hidden = true;
        var done = document.getElementById('sent');
        done.style.display = 'block'; done.focus();
      })
      .catch(function () {
        submit.disabled = false; submit.textContent = 'Request a consultation';
        document.getElementById('e-submit').textContent = 'Your enquiry could not be sent just now. Please try again, or write to enquiries@zinzilevuma.com.';
      });
  });
})();

// Advisory portfolio: reading progress, stations, from-to shift and the balance
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var case_ = document.querySelector('article.case');
  if (!case_) return;
  var bar = document.querySelector('.case-progress');
  var stations = document.querySelector('.stations');
  var items = stations ? stations.querySelectorAll('li') : [];
  var shift = document.querySelector('.shift');

  function tick() {
    var r = case_.getBoundingClientRect(), vh = window.innerHeight;
    var read = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - vh)));
    if (bar) bar.style.setProperty('--read', read.toFixed(4));
    if (stations) {
      var s = stations.getBoundingClientRect();
      var p = reduce ? 1 : Math.min(1, Math.max(0, (vh * 0.75 - s.top) / (s.height + vh * 0.25)));
      stations.style.setProperty('--p', p.toFixed(3));
      items.forEach(function (li, i) { li.classList.toggle('lit', p >= (i / (items.length - 1)) - 0.02 || (p > 0 && i === 0)); });
    }
  }
  window.addEventListener('scroll', tick, { passive: true });
  window.addEventListener('resize', tick);
  tick();

  if (shift && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en, o) { if (en[0].isIntersecting) { shift.classList.add('in'); o.disconnect(); } }, { threshold: 0.35 }).observe(shift);
  } else if (shift) { shift.classList.add('in'); }

  var range = document.getElementById('balance');
  var out = document.getElementById('balance-out');
  if (range && out) {
    var say = function () {
      var v = +range.value, msg;
      if (v <= 20) msg = 'All visibility: found by many, remembered by few. The brand begins to sound like everyone else.';
      else if (v < 40) msg = 'Leaning towards visibility: more traffic, but the story is starting to thin.';
      else if (v <= 60) msg = 'Held at the centre: keywords that serve the storytelling, not replace it.';
      else if (v < 80) msg = 'Leaning towards identity: the story is intact, but fewer people find it.';
      else msg = 'All identity: true to itself, but hard to find. The story stays in the room.';
      out.textContent = msg;
      range.setAttribute('aria-valuetext', msg.split(':')[0]);
      range.style.setProperty('--fill', v + '%');
    };
    range.addEventListener('input', say);
    say();
  }
})();
