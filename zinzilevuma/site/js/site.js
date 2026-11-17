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
