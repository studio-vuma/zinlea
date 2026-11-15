(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('mobile-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
  } else { els.forEach(function (e) { e.classList.add('in'); }); }

  // Booking form
  var form = document.getElementById('consultForm');
  if (!form) return;
  var EMAIL = 'vzinzile@gmail.com';
  function setErr(id, msg) {
    document.getElementById('e-' + id).textContent = msg;
    document.getElementById('f-' + id).setAttribute('aria-invalid', msg ? 'true' : 'false');
  }
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var name = form.name.value.trim(), brand = form.brand.value.trim(), email = form.email.value.trim();
    var ok = true;
    setErr('name', name ? '' : 'Please share your name.'); if (!name) ok = false;
    setErr('brand', brand ? '' : 'Please share your brand or organisation.'); if (!brand) ok = false;
    var validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    setErr('email', validEmail ? '' : 'Please enter a valid email address.'); if (!validEmail) ok = false;
    if (!ok) { var first = form.querySelector('[aria-invalid="true"]'); if (first) first.focus(); return; }

    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
      .then(function (r) { if (!r.ok) throw new Error(); form.style.display = 'none'; var t = document.getElementById('thanks'); t.style.display = 'block'; t.focus(); })
      .catch(function () {
        // Until the site is hosted with form handling, open an email draft instead
        var body = 'Name: ' + name + '\nBrand: ' + brand + '\nEmail: ' + email + '\nInterest: ' + form.interest.value + '\nMarkets: ' + form.markets.value + '\n\n' + form.message.value;
        window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Complimentary consultation request: ' + brand) + '&body=' + encodeURIComponent(body);
      });
  });
})();
