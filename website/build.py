#!/usr/bin/env python3
"""Build the Zinlea website (static HTML).

Identity: Zinlea is measured in hours. Zinlea Health is the day (white),
Zinlea Night is midnight (ink blue + moonlight), Zinlea Global is first light
(midnight warming to dawn). Shared header, footer, dial and form markup live
here so every page stays consistent.

    python3 website/build.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_legal import GOVERNANCE, PRIVACY  # noqa: E402
import seo  # noqa: E402
from PIL import Image  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://zinlea.com"
EMAIL = "info@zinlea.com"

ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def wordmark(sub="health"):
    return (f'<span class="wm-word" aria-hidden="true">z<span class="wm-i">&#305;</span>nlea</span>'
            f'<span class="wm-sub" aria-hidden="true">{sub}</span>')


# --------------------------------------------------------------------------- dial
def dial(extra_class=""):
    """12-hour arc from 20:00 (left) to 08:00 (right). site.js moves the marker to London time."""
    cx, cy, r = 260, 270, 220
    parts = []
    for h in range(13):
        a = math.pi - (h / 12) * math.pi
        major = h % 2 == 0
        r1, r2 = r + 8, r + (20 if major else 14)
        x1, y1 = cx + r1 * math.cos(a), cy - r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy - r2 * math.sin(a)
        parts.append(f'<line class="tick{" major" if major else ""}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        if major:
            label = f"{(20 + h) % 24:02d}"
            lx, ly = cx + (r + 38) * math.cos(a), cy - (r + 38) * math.sin(a) + 4
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle">{label}</text>')
    return f"""<svg class="dial {extra_class}" data-dial viewBox="-10 0 540 300" role="img" aria-label="Zinlea Night runs from 20:00 to 08:00, London time.">
  <path class="track" d="M 40 270 A 220 220 0 0 1 480 270"/>
  <path class="elapsed" d=""/>
  {''.join(parts)}
  <circle class="marker-halo" cx="40" cy="270" r="18"/>
  <circle class="marker" cx="40" cy="270" r="7"/>
</svg>"""


# --------------------------------------------------------------------------- shell
PRELOAD = {"/": "night-caring-hands", "/night/partnerships/": "care-home", "/about/": "consult-elderly"}


def head(title, desc, path, theme="health", schema=None, noindex=False):
    """Document head. Title, description, social card and structured data come from seo.py."""
    meta = seo.PAGES[path]
    title, desc = meta["title"], meta["desc"]
    noindex = noindex or meta.get("noindex", False)
    own = [x for x in (schema or []) if x.get("@type") == "FAQPage"]
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in own + seo.page_schema(path))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    colour = {"health": "#FFFFFF", "night": "#070B17", "global": "#08101F"}[theme]
    og = f"{SITE}/assets/og/{meta['og']}.jpg"
    pre = ""
    if path in PRELOAD:
        n = PRELOAD[path]
        pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(n)}" imagesizes="(min-width: 1000px) 40vw, 100vw" fetchpriority="high">\n'
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="en-GB" href="{SITE}{path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{path}">
<meta name="author" content="Zinlea Health">
<meta name="theme-color" content="{colour}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Zinlea Health">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/icon-32.png">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{pre}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{ld}</head>
<body class="theme-{theme}">
<a class="skip-link" href="#main">Skip to content</a>
"""


NAV = [
    ("night", "/night/", "Zinlea Night", "n-night"),
    ("global", "/global/", "Zinlea Global", "n-global"),
    ("about", "/about/", "About", ""),
    ("faq", "/faq/", "FAQ", ""),
    ("contact", "/contact/", "Contact", ""),
]


def header(current="", sub="health", cta=("Enquire", "/contact/"), status=True, subnav=None):
    cur = ' aria-current="page"'
    def dot(d):
        return f'<span class="n-dot {d}" aria-hidden="true"></span>' if d else ""
    links = "".join(
        f'<li><a href="{h}"{cur if k == current else ""}>{dot(d)}{text}</a></li>'
        for k, h, text, d in NAV
    )
    drawer = "".join(
        f'<li><a href="{h}">{label}<small>{tag}</small></a></li>'
        for h, label, tag in [
            ("/", "Zinlea Health", "Home"), ("/night/", "Zinlea Night", "London, 8pm to 8am"),
            ("/night/membership/", "Membership", "Zinlea Night"), ("/night/private-client/", "Private Client", "Zinlea Night"),
            ("/global/", "Zinlea Global", "Partnerships"), ("/about/", "About", ""), ("/faq/", "FAQ", ""),
            ("/contact/", "Contact", ""),
        ]
    )
    sub_html = ""
    if subnav:
        items, now = subnav
        sub_html = '<nav class="subnav" aria-label="Zinlea Night"><div class="wrap"><ul>' + "".join(
            f'<li><a href="{h}"{cur if k == now else ""}>{t}</a></li>' for k, h, t in items) + '</ul></div></nav>'
    chip = '<span class="status" data-open-state><span class="s-dot" aria-hidden="true"></span><span data-status-short>8pm &ndash; 8am &middot; London</span></span>' if status else ""
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="wm" href="/" aria-label="Zinlea {sub.title()}, home">{wordmark(sub)}</a>
    <nav class="nav" aria-label="Primary"><ul>{links}</ul></nav>
    <div class="head-right">
      {chip}
      <a class="btn btn-primary btn-sm head-cta" href="{cta[1]}">{cta[0]}</a>
      <button class="menu-btn" type="button" aria-controls="drawer" aria-expanded="false" aria-label="Open menu"><span></span></button>
    </div>
  </div>
  {sub_html}
</header>
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-label="Menu">
  <div class="drawer-top">
    <a class="wm" href="/" aria-label="Zinlea Health, home">{wordmark(sub)}</a>
    <button class="drawer-close" type="button" aria-label="Close menu">&times;</button>
  </div>
  <nav aria-label="Menu"><ul>{drawer}</ul></nav>
  <div class="drawer-foot">
    <a class="btn btn-primary" href="{cta[1]}">{cta[0]} {ARR}</a>
    <span class="label">{EMAIL}</span>
  </div>
</div>
"""


def footer(sub="health"):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand">
        <a class="wm" href="/" aria-label="Zinlea Health, home">{wordmark(sub)}</a>
        <p>Private, clinician-led healthcare. Zinlea Night provides overnight clinical advice in London. Zinlea Global builds healthcare partnerships across Africa.</p>
        <a class="arrow-link" href="mailto:{EMAIL}">{EMAIL} {ARR}</a>
      </div>
      <div class="f-cols">
        <div><h4>Zinlea Night</h4><ul>
          <li><a href="/night/">Overview</a></li><li><a href="/night/membership/">Membership</a></li>
          <li><a href="/night/private-client/">Private Client</a></li><li><a href="/night/how-it-works/">How it works</a></li>
          <li><a href="/night/partnerships/">Partnerships</a></li></ul></div>
        <div><h4>Zinlea Global</h4><ul>
          <li><a href="/global/">Overview</a></li><li><a href="/global/#focus">What we build</a></li>
          <li><a href="/contact/?type=global">Register interest</a></li></ul></div>
        <div><h4>Zinlea Health</h4><ul>
          <li><a href="/">Home</a></li><li><a href="/about/">About</a></li>
          <li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li></ul></div>
        <div><h4>Legal</h4><ul>
          <li><a href="/clinical-governance/">Clinical governance</a></li><li><a href="/privacy/">Privacy policy</a></li></ul></div>
      </div>
    </div>
    <div class="f-big" aria-hidden="true">zinlea</div>
    <div class="f-base">
      <span><b>Not an emergency service.</b> For chest pain, difficulty breathing, signs of stroke or any life-threatening symptoms, call 999.</span>
      <span>&copy; <span data-year>2026</span> Zinlea Health &middot; Registered in England &amp; Wales</span>
    </div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


IMG_DIR = os.path.join(OUT, "assets", "img")
WIDTHS = (800, 1600)
_dims = {}


def make_variants(name):
    """Create WebP versions at 800px and 1600px wide (never upscaled); remember the source size."""
    if name in _dims:
        return _dims[name]
    src = os.path.join(IMG_DIR, f"{name}.jpg")
    im = Image.open(src).convert("RGB")
    _dims[name] = im.size
    for w in WIDTHS:
        out = os.path.join(IMG_DIR, f"{name}-{w}.webp")
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
            ww = min(w, im.size[0])
            im.resize((ww, round(im.size[1] * ww / im.size[0])), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)
    return _dims[name]


def srcset(name):
    w0, _ = make_variants(name)
    return ", ".join(f"/assets/img/{name}-{w}.webp {min(w, w0)}w" for w in WIDTHS)


def img(name, alt, eager=False, sizes="(min-width: 1000px) 50vw, 100vw"):
    w, h = make_variants(name)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{srcset(name)}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load}></picture>')


def label(text, pip=True):
    dot = '<span class="pip" aria-hidden="true"></span>' if pip else ""
    return f'<span class="label">{dot}{text}</span>'


# --------------------------------------------------------------------------- schema (see seo.py)
ORG, NIGHT_ORG, GLOBAL_ORG = seo.ORG, seo.NIGHT_ORG, seo.GLOBAL_ORG

def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Zinlea Health", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"}]}


# --------------------------------------------------------------------------- HOME (Zinlea Health, day)
def home():
    return head("Zinlea Health | Private clinical care, whatever the hour",
                "Zinlea Health is a private, clinician-led healthcare company. Zinlea Night offers overnight clinical advice in London, 8pm to 8am. Zinlea Global builds healthcare partnerships across Africa.",
                "/", schema=[ORG]) + header() + f"""
<main id="main">
<section class="h-hero">
  <div class="wrap h-hero-grid">
    <div>
      {label("Zinlea Health")}
      <h1 class="t-hero">Private clinical care, whatever the hour.</h1>
      <p class="lede">A clinician-led healthcare company. Zinlea Night gives London members calm, expert clinical advice from 8pm to 8am. Zinlea Global builds healthcare partnerships across Africa.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/night/">Discover Zinlea Night {ARR}</a>
        <a class="btn btn-quiet" href="/global/">Zinlea Global</a>
      </div>
    </div>
    <div class="h-hero-media">
      {img("night-caring-hands", "A clinician gently holding an older patient's hand", eager=True)}
      <div class="glass" data-open-state>
        <span class="g-dot" aria-hidden="true"></span>
        <div><b data-state-title>Zinlea Night</b><span data-state-sub>Overnight clinical advice, 8pm to 8am</span></div>
        <span class="mono" data-clock>20:00</span>
      </div>
    </div>
  </div>
</section>

<section class="sec who">
  <div class="wrap who-grid">
    <div>
      {label("Who we are")}
      <h2 class="t-2">A private healthcare company, led by clinicians.</h2>
    </div>
    <div>
      <p class="lede">Zinlea Health is led by experienced clinicians who want to make expert healthcare easier to reach at the moments it matters most. We design services around the people who use them: calm, private and unhurried, with clinical safety at the centre of every decision.</p>
      <p class="lede">Our first service, <a href="/night/">Zinlea Night</a>, gives members in London direct access to experienced Advanced Nurse Practitioners between 8pm and 8am. Through <a href="/global/">Zinlea Global</a>, we are building healthcare partnerships with providers, clinicians and investors across Africa.</p>
      <dl class="who-facts">
        <div><dt>Led by</dt><dd>Experienced clinicians</dd></div>
        <div><dt>Based in</dt><dd>The United Kingdom</dd></div>
        <div><dt>Services</dt><dd>Zinlea Night &amp; Zinlea Global</dd></div>
      </dl>
      <a class="arrow-link" href="/about/">More about Zinlea Health {ARR}</a>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">Two services, one way of caring.</h2>
      <p class="lede">Each Zinlea service is led by experienced clinicians and built on the same principles: calm expertise, discretion and continuity.</p>
    </div>
    <div class="doors">
      <a class="door door-night" href="/night/">
        <div class="door-dial">{dial()}</div>
        <div class="d-top"><span>London</span><span class="mono">20:00 &ndash; 08:00</span></div>
        <h3>Zinlea Night</h3>
        <p>Private overnight medical advice from experienced Advanced Nurse Practitioners, for members, families and care providers.</p>
        <span class="d-cta"><span class="circ">{ARR}</span>Discover Zinlea Night</span>
      </a>
      <a class="door door-global" href="/global/">
        <span class="sun" aria-hidden="true"></span><span class="horizon" aria-hidden="true"></span>
        <div class="d-top"><span>Partnerships</span><span>Across Africa</span></div>
        <h3>Zinlea Global</h3>
        <p>Working with healthcare providers, clinicians and investors across Africa to build new services together.</p>
        <span class="d-cta"><span class="circ">{ARR}</span>Discover Zinlea Global</span>
      </a>
    </div>
  </div>
</section>

<section class="sec-lg alt">
  <div class="wrap">
    <p class="two-tone">Good healthcare should feel private, professional and unhurried. <span>Whatever the hour, wherever you are.</span></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="tiles c3">
      <article class="tile"><span class="t-tag">How we speak to you</span><h3>Calm expertise</h3><p>Clinical advice delivered thoughtfully and without rush, by experienced clinicians who listen carefully.</p></article>
      <article class="tile"><span class="t-tag">How we treat your information</span><h3>Discretion</h3><p>Private care with complete respect for confidentiality and personal boundaries.</p></article>
      <article class="tile"><span class="t-tag">How we stay with you</span><h3>Continuity</h3><p>A membership built over time, so you are supported consistently, night after night.</p></article>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap split">
    <div class="media">{img("consult-elderly", "A clinician speaking warmly with an older woman")}</div>
    <div>
      {label("Zinlea Night")}
      <h2 class="t-2">A senior nurse, at the end of the phone.</h2>
      <p class="lede">When you contact Zinlea Night, you speak directly with an experienced Advanced Nurse Practitioner. Consultations are unhurried: we listen carefully, ask the right questions and give clear clinical guidance.</p>
      <ul class="checks">
        <li><span><b>Overnight access</b>, 8pm to 8am, by phone or video</span></li>
        <li><span><b>Medication guidance</b> and remote prescribing where clinically appropriate</span></li>
        <li><span><b>Clear escalation</b> when you need in-person care</span></li>
      </ul>
      <div class="actions"><a class="btn btn-primary" href="/night/how-it-works/">How Zinlea Night works {ARR}</a></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="trust">
      <div><b>Clinician-led</b><span>Advanced Nurse Practitioners</span></div>
      <div><b>CQC application submitted</b><span>Registration under review</span></div>
      <div><b>UK GDPR</b><span>Confidential by design</span></div>
      <div><b>Safety first</b><span>Clear escalation pathways</span></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel">
      <span class="label">Founding membership</span>
      <h2 class="t-1">Peace of mind, from 8pm to 8am.</h2>
      <p class="lede">Founding membership is currently limited while we onboard our first members. We reply to every enquiry within 24 hours.</p>
      <div class="actions">
        <a class="btn btn-light" href="/contact/?type=member">Request membership {ARR}</a>
        <a class="btn btn-quiet" href="/contact/?type=partnership">Partnership enquiry</a>
      </div>
    </div>
  </div>
</section>
</main>
""" + footer()


# --------------------------------------------------------------------------- NIGHT (midnight)
def mcard(kind, tier):
    return f"""<div class="mcard {kind}" aria-hidden="true">
  <div class="mc-top"><span class="mc-wm">zinlea night</span><span class="mc-tier">{tier}</span></div>
  <div class="mc-bottom"><span class="mc-hours">20:00 &mdash; 08:00</span><span class="mc-chip"></span></div>
</div>"""


NIGHT_SUB = [
    ("overview", "/night/", "Overview"),
    ("membership", "/night/membership/", "Membership"),
    ("private-client", "/night/private-client/", "Private Client"),
    ("how", "/night/how-it-works/", "How it works"),
    ("partnerships", "/night/partnerships/", "Partnerships"),
    ("faq", "/faq/#night", "FAQ"),
]


def night_head(title, desc, path, sub_current, cta=("Request membership", "/contact/?type=member")):
    schema = [NIGHT_ORG] if path == "/night/" else [crumbs(title.split(" | ")[0], path)]
    return head(title, desc, path, theme="night", schema=schema) + header("night", sub="night", cta=cta, subnav=(NIGHT_SUB, sub_current))


def page_intro(lbl, h1, lede, actions=""):
    return f"""<section class="p-intro">
  <div class="wrap">
    {label(lbl)}
    <h1 class="t-1">{h1}</h1>
    <p class="lede">{lede}</p>
    {f'<div class="actions">{actions}</div>' if actions else ''}
  </div>
</section>"""


NIGHT_CTA = f"""<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel">
      <span class="label">Founding membership</span>
      <h2 class="t-1">Overnight clinical care, quietly available.</h2>
      <p class="lede">Private access to experienced Advanced Nurse Practitioners, 8pm to 8am. We reply to every enquiry within 24 hours.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/?type=member">Request membership {ARR}</a><a class="btn btn-quiet" href="/night/private-client/">Private Client</a></div>
    </div>
  </div>
</section>"""

NOTICE = f"""<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="notice">
      <span class="n-num">999</span>
      <p><strong>Zinlea Night is not an emergency service.</strong> If you or someone else has chest pain, difficulty breathing, loss of consciousness, severe bleeding or signs of stroke, call 999 immediately or go to your nearest A&amp;E.</p>
      <a class="arrow-link" href="/clinical-governance/">Read more {ARR}</a>
    </div>
  </div>
</section>"""


def night():
    teasers = "".join(
        f'<a class="teaser" href="{h}"><span class="t-k">{k}</span><b>{t}</b><span class="t-d">{d}</span><span class="circ">{ARR}</span></a>'
        for k, h, t, d in [
            ("From &pound;85 a month", "/night/membership/", "Membership", "Individual and family membership, with simple monthly pricing."),
            ("By private consultation", "/night/private-client/", "Private Client", "A named lead clinician and specialist care arranged entirely around you."),
            ("Enquiry to first call", "/night/how-it-works/", "How it works", "What happens after you get in touch, and what a call is like."),
            ("For organisations", "/night/partnerships/", "Partnerships", "Overnight support for care homes, residences and family offices."),
        ]
    )
    return night_head("Zinlea Night | Overnight clinical advice in London, 8pm to 8am",
                      "Private overnight medical advice in London. Experienced Advanced Nurse Practitioners available 8pm to 8am for calm reassurance, clinical guidance and escalation support.",
                      "/night/", "overview") + f"""
<main id="main">
<section class="d-hero">
  <div class="wrap d-hero-grid">
    <div>
      {label("Zinlea Night &middot; London")}
      <h1 class="t-hero">Overnight medical advice, 8pm to 8am.</h1>
      <p class="lede">Private overnight medical advice in London through experienced Advanced Nurse Practitioners. Calm reassurance, clear guidance and escalation support while the rest of London sleeps.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/contact/?type=member">Request membership {ARR}</a>
        <a class="btn btn-quiet" href="/night/membership/">See membership</a>
      </div>
      <div class="facts">
        <span class="chip"><b>Advanced Nurse Practitioners</b></span>
        <span class="chip">Phone &amp; video</span>
        <span class="chip">From <b>&pound;85</b> a month</span>
      </div>
    </div>
    <div class="hero-dial" data-open-state>
      {dial()}
      <div class="readout"><span class="mono" data-clock>20:00</span><span data-state-title>Zinlea Night opens at 20:00</span></div>
    </div>
  </div>
</section>

<div class="wrap">
  <figure class="band-img" style="margin:0">{img("night-london", "Westminster at dusk, London")}<figcaption>Remote by design &middot; members across London</figcaption></figure>
</div>

<section class="sec explain" id="what-is-zinlea-night">
  <div class="wrap">
    <div class="sec-head split">
      <div>{label("In plain terms")}<h2 class="t-2" style="margin-top:18px">What is Zinlea Night?</h2></div>
      <p class="lede">Zinlea Night is a private membership that gives you direct access to an experienced nurse practitioner overnight, by phone or video. If something worries you between 8pm and 8am, you can speak to a senior clinician who will listen, assess and tell you clearly what to do next.</p>
    </div>
    <div class="timeline">
      <div class="tl"><span class="when">Step 1</span><div><h3>You become a member</h3><p>Choose individual or family membership. We reply to every enquiry within 24 hours.</p></div></div>
      <div class="tl"><span class="when">Step 2</span><div><h3>You call when you need us</h3><p>Any time between 8pm and 8am, by telephone or video.</p></div></div>
      <div class="tl"><span class="when">Step 3</span><div><h3>A senior nurse guides you</h3><p>Clear advice, remote prescribing where clinically appropriate, or help getting the right in-person care.</p></div></div>
      <div class="tl"><span class="when">Next day</span><div><h3>Continuity</h3><p>Your membership means you are supported consistently, night after night.</p></div></div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap explain-grid">
    <div>
      {label("When members call")}
      <h2 class="t-2" style="margin-top:18px">For the moments that can&rsquo;t wait until morning, but aren&rsquo;t a 999 call.</h2>
    </div>
    <ul class="checks">
      <li><span>Someone at home feels unwell during the night and you are not sure whether it can wait until morning.</span></li>
      <li><span>You have a question about medication after your pharmacy and GP surgery have closed.</span></li>
      <li><span>You are caring for an older relative and something has changed.</span></li>
      <li><span>A symptom is worrying you and you want calm, expert reassurance.</span></li>
      <li><span>You want help deciding which service is right for you, from self-care to urgent care.</span></li>
    </ul>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">What Zinlea Night is not.</h2>
      <p class="lede">Being clear about our limits is part of keeping you safe.</p>
    </div>
    <div class="tiles c3">
      <article class="tile"><span class="t-tag mono">999</span><h3>Not an emergency service</h3><p>For chest pain, difficulty breathing, signs of stroke or any life-threatening symptoms, call 999 or go to A&amp;E.</p></article>
      <article class="tile"><span class="t-tag">Remote by design</span><h3>Not home visits</h3><p>We advise by phone or video and guide you to in-person care when you need it.</p></article>
      <article class="tile"><span class="t-tag">Works alongside</span><h3>Not a replacement for your GP</h3><p>Zinlea Night complements your GP and NHS services, which remain your home for long-term care.</p></article>
    </div>
  </div>
</section>

<section class="sec-lg alt">
  <div class="wrap">
    <p class="two-tone">Zinlea Night was created for the hours when healthcare can feel hardest to reach. <span>Private, professional and unhurried, with a safety-first approach.</span></p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">What members receive.</h2>
      <p class="lede">Out-of-hours medical support designed around your comfort and peace of mind.</p>
    </div>
    <div class="tiles c3">
      <article class="tile feature"><span class="t-tag mono">20:00 &ndash; 08:00</span><h3>Overnight access</h3><p>Advanced Nurse Practitioners available throughout the night.</p></article>
      <article class="tile"><span class="t-tag">You and your household</span><h3>Adult &amp; family support</h3><p>Overnight healthcare support for adults and family members when you need it most.</p></article>
      <article class="tile"><span class="t-tag">Treatment options</span><h3>Medication guidance</h3><p>Expert advice on medication, treatment and what to do next.</p></article>
      <article class="tile"><span class="t-tag">Where clinically appropriate</span><h3>Remote prescribing</h3><p>Prescribing decisions are made only after proper assessment, within UK guidelines.</p></article>
      <article class="tile"><span class="t-tag">Clear next steps</span><h3>Reassurance &amp; escalation</h3><p>Clear guidance on when further care is needed, and where to go.</p></article>
      <article class="tile"><span class="t-tag">At your pace</span><h3>Calm consultations</h3><p>Unhurried, thoughtful conversations by telephone or video.</p></article>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">Explore Zinlea Night.</h2>
      <p class="lede">Membership for individuals and families, a fully personal Private Client service, and partnerships for organisations.</p>
    </div>
    <div class="teasers">{teasers}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap split flip">
    <div class="media">{img("nurse", "An Advanced Nurse Practitioner in uniform")}</div>
    <div>
      {label("Our clinicians")}
      <h2 class="t-2">Experienced, calm and thorough.</h2>
      <p class="lede">Zinlea Night is delivered by experienced Advanced Nurse Practitioners with backgrounds across urgent care, primary care and acute services, trained in remote consultation safety and safeguarding.</p>
      <p class="lede">Zinlea Night is a remote service. We do not provide home visits or in-person examinations, and we guide you to the right service when you need one.</p>
      <div class="actions"><a class="arrow-link" href="/clinical-governance/">Clinical governance {ARR}</a></div>
    </div>
  </div>
</section>

{NOTICE}
{NIGHT_CTA}
</main>
""" + footer("night")


def night_membership():
    return night_head("Membership | Zinlea Night",
                      "Zinlea Night membership: Individual from £85 a month, Family from £225 a month, and the Private Client service by consultation.",
                      "/night/membership/", "membership") + f"""
<main id="main">
{page_intro("Zinlea Night &middot; Membership", "Membership.", "Simple, transparent pricing for overnight peace of mind in London. We are currently onboarding a limited number of founding members.")}

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <div class="plans">
      <article class="plan">
        {mcard("silver", "Individual")}
        <div class="plan-body"><h3>Individual</h3><p class="for">Personal overnight clinical support.</p>
          <div class="price"><span class="from">From</span><b>&pound;85</b><small>a month</small></div>
          <ul><li>Overnight access, 8pm to 8am</li><li>Advanced Nurse Practitioner consultations</li><li>Medication and treatment guidance</li><li>Reassurance and escalation support</li></ul></div>
        <a class="btn btn-quiet" href="/contact/?type=member">Request membership</a>
      </article>
      <article class="plan">
        {mcard("midnight", "Family")}
        <div class="plan-body"><h3>Family</h3><p class="for">Overnight healthcare support for your household.</p>
          <div class="price"><span class="from">From</span><b>&pound;225</b><small>a month</small></div>
          <ul><li>Everything in Individual</li><li>Support for adults and family members</li><li>Continuity with a consistent clinical team</li><li>Unhurried consultations at your pace</li></ul></div>
        <a class="btn btn-primary" href="/contact/?type=member">Request membership {ARR}</a>
      </article>
      <article class="plan">
        {mcard("glass-card", "Partner")}
        <div class="plan-body"><h3>Partnership</h3><p class="for">Care homes, residences, family offices and organisations.</p>
          <div class="price"><b style="font-size:2.2rem">Tailored</b><small>monthly</small></div>
          <ul><li>Overnight clinical decision support</li><li>Triage, remote consultation and prescribing</li><li>Governance-led escalation</li><li>Complements your existing care team</li></ul></div>
        <a class="btn btn-quiet" href="/night/partnerships/">About partnerships</a>
      </article>
    </div>

    <a class="pc-panel" href="/night/private-client/">
      <div class="pc-card">{mcard("obsidian", "Private Client")}</div>
      <div class="pc-body">
        {label("By private consultation")}
        <h2 class="t-2">Private Client.</h2>
        <p class="lede">For individuals and families who want care arranged entirely around them: a named lead clinician, coordination with specialist consultants, and a care plan that knows your history. Fees are agreed after a private consultation.</p>
        <span class="arrow-link">Discover Private Client {ARR}</span>
      </div>
    </a>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">Every membership includes.</h2>
      <p class="lede">The same clinical standards, whichever membership you choose.</p>
    </div>
    <div class="tiles c3">
      <article class="tile"><span class="t-tag mono">20:00 &ndash; 08:00</span><h3>Overnight access</h3><p>Speak to an Advanced Nurse Practitioner through the night, by phone or video.</p></article>
      <article class="tile"><span class="t-tag">Safety first</span><h3>Clear escalation</h3><p>Guidance on when you need in-person care, and help finding the right service.</p></article>
      <article class="tile"><span class="t-tag">UK GDPR</span><h3>Confidentiality</h3><p>Your information is stored securely and used only to provide your care.</p></article>
    </div>
    <p class="note-line">Questions about membership? <a href="/faq/#night">Read the FAQ</a> or <a href="/contact/?type=member">get in touch</a>.</p>
  </div>
</section>

{NOTICE.replace('style="padding-top:0"', '')}
</main>
""" + footer("night")


def night_private_client():
    return night_head("Private Client | Zinlea Night",
                      "Zinlea Night Private Client: a named lead clinician, coordination with specialist consultants and care arranged entirely around you. By private consultation.",
                      "/night/private-client/", "private-client", cta=("Arrange a consultation", "/contact/?type=private-client")) + f"""
<main id="main">
<section class="pc-hero">
  <div class="wrap pc-hero-grid">
    <div>
      {label("Zinlea Night &middot; Private Client")}
      <h1 class="t-hero">Care that knows you.</h1>
      <p class="lede">Private Client is our most personal service. One lead clinician who knows you and your family, specialist input arranged on your behalf, and care that is planned around your life rather than a schedule.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/contact/?type=private-client">Arrange a private consultation {ARR}</a>
      </div>
      <p class="pc-note">Fees are agreed individually, after a private consultation.</p>
    </div>
    <div class="pc-hero-card">{mcard("obsidian", "Private Client")}</div>
  </div>
</section>

<section class="sec-lg alt">
  <div class="wrap">
    <p class="two-tone">Some families want more than access to a clinician. <span>They want a clinician who already knows the history, the medication and the people involved.</span></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">What Private Client includes.</h2>
      <p class="lede">Everything in Zinlea Night membership, with care arranged personally around you. The details are agreed with you during your consultation.</p>
    </div>
    <div class="tiles c3">
      <article class="tile feature"><span class="t-tag">One point of contact</span><h3>A named lead clinician</h3><p>A senior clinician who knows you, your household and your medical history, and leads your care.</p></article>
      <article class="tile"><span class="t-tag">Specialist input</span><h3>Specialist coordination</h3><p>Referrals and liaison with specialist consultants and your own doctors, arranged on your behalf.</p></article>
      <article class="tile"><span class="t-tag">Written for you</span><h3>A personal care plan</h3><p>A plan that reflects your history and preferences, so every overnight call starts from what we already know.</p></article>
      <article class="tile"><span class="t-tag">No rush</span><h3>Extended consultations</h3><p>Longer, unhurried conversations and follow-up guidance after every call.</p></article>
      <article class="tile"><span class="t-tag">Your household</span><h3>Family and staff</h3><p>Care that can extend to family members and, where appropriate, household staff.</p></article>
      <article class="tile"><span class="t-tag">Complete discretion</span><h3>Quiet by design</h3><p>Strict confidentiality and personal boundaries, whoever you are.</p></article>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">How it begins.</h2>
      <p class="lede">Private Client is arranged individually. There is no sign-up form and no published price.</p>
    </div>
    <div class="timeline">
      <div class="tl"><span class="when">First</span><div><h3>Get in touch</h3><p>Tell us a little about yourself, in confidence.</p></div></div>
      <div class="tl"><span class="when">Within 24 hours</span><div><h3>We arrange a time</h3><p>A member of our clinical leadership contacts you personally.</p></div></div>
      <div class="tl"><span class="when">Consultation</span><div><h3>A private conversation</h3><p>We understand your needs, your family and what good care looks like for you.</p></div></div>
      <div class="tl"><span class="when">Your proposal</span><div><h3>Care, designed for you</h3><p>A written proposal with your lead clinician, care plan and fees.</p></div></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel obsidian">
      <span class="label">Private Client</span>
      <h2 class="t-1">Begin with a conversation.</h2>
      <p class="lede">Every Private Client relationship starts with a private consultation. There is no obligation.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/?type=private-client">Arrange a private consultation {ARR}</a></div>
    </div>
  </div>
</section>
{NOTICE}
</main>
""" + footer("night")


def night_how():
    return night_head("How it works | Zinlea Night",
                      "How Zinlea Night works: from your enquiry to your first overnight call with an Advanced Nurse Practitioner.",
                      "/night/how-it-works/", "how") + f"""
<main id="main">
{page_intro("Zinlea Night &middot; How it works", "From enquiry to your first call.", "Simple, discreet access to overnight clinical support in London. We keep everything straightforward.")}

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <div class="timeline">
      <div class="tl"><span class="when">Today</span><div><h3>Request membership</h3><p>Complete our short enquiry form.</p></div></div>
      <div class="tl"><span class="when">Within 24 hours</span><div><h3>We reply</h3><p>A member of our team responds personally.</p></div></div>
      <div class="tl"><span class="when">Onboarding call</span><div><h3>Get to know you</h3><p>A brief call to understand your needs and confirm your membership.</p></div></div>
      <div class="tl"><span class="when">From 20:00</span><div><h3>Call when you need us</h3><p>Overnight advice from our Advanced Nurse Practitioners until 08:00.</p></div></div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap split">
    <div>
      <div class="phone" aria-hidden="true">
        <div class="phone-screen">
          <div class="phone-time"><span class="mono">02:14</span><span>&#9679;&#9679;&#9679;</span></div>
          <div class="phone-notch"></div>
          <div class="p-wm">zinlea night</div>
          <div class="p-avatar">ANP</div>
          <div class="p-name">Your nurse practitioner</div>
          <div class="p-role">Advanced Nurse Practitioner</div>
          <div class="p-timer">On call &middot; 06:41</div>
          <div class="p-note">Calm, unhurried advice. If you need in-person care, we will guide you to the right service.</div>
          <div class="p-actions">
            <span class="p-btn"><svg viewBox="0 0 24 24" fill="none" stroke="#EEF1F7" stroke-width="1.8"><path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3Z"/><path d="M19 10a7 7 0 0 1-14 0M12 17v5"/></svg></span>
            <span class="p-btn"><svg viewBox="0 0 24 24" fill="none" stroke="#EEF1F7" stroke-width="1.8"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3"/></svg></span>
            <span class="p-btn end"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M3 15c5-5 13-5 18 0l-2 3-4-1v-3c-2-.6-4-.6-6 0v3l-4 1Z"/></svg></span>
          </div>
        </div>
      </div>
    </div>
    <div>
      {label("What to expect")}
      <h2 class="t-2">You speak directly to a senior nurse.</h2>
      <p class="lede">When you contact Zinlea Night, you speak with an experienced Advanced Nurse Practitioner. We listen carefully, ask the right questions and give clear clinical guidance.</p>
      <p class="lede">Unlike a standard out-of-hours service, our focus is continuity and reassurance. When in-person care is needed, we help you understand your options and escalate appropriately. Everything is confidential.</p>
      <ul class="checks">
        <li><span><b>By phone or video</b>, whichever you prefer</span></li>
        <li><span><b>Remote prescribing</b> where clinically appropriate</span></li>
        <li><span><b>Clear next steps</b> if you need in-person care</span></li>
      </ul>
    </div>
  </div>
</section>

{NOTICE.replace('style="padding-top:0"', '')}
{NIGHT_CTA}
</main>
""" + footer("night")


def night_partnerships():
    return night_head("Partnerships | Zinlea Night",
                      "Zinlea Night partners with care homes, residences, family offices and organisations to provide overnight clinical support in London, 8pm to 8am.",
                      "/night/partnerships/", "partnerships", cta=("Partnership enquiry", "/contact/?type=partnership")) + f"""
<main id="main">
{page_intro("Zinlea Night &middot; Partnerships", "Overnight support for care providers.", "Zinlea Night partners with a limited number of organisations and private residences seeking discreet overnight clinical support in London.", f'<a class="btn btn-primary" href="/contact/?type=partnership">Partnership enquiry {ARR}</a>')}

<section class="sec" style="padding-top:8px">
  <div class="wrap split">
    <div class="media">{img("care-home", "A clinician checking an older resident's blood pressure")}</div>
    <div>
      {label("Residential &amp; clinical partnerships")}
      <h2 class="t-2">For care homes and residences.</h2>
      <p class="lede">We work with a small number of carefully selected residential and clinical partners, providing overnight escalation support between 8pm and 8am.</p>
      <ul class="checks">
        <li><span>Complements existing care teams with overnight clinical decision support and reassurance</span></li>
        <li><span>Triage, remote consultation and prescribing where clinically appropriate</span></li>
        <li><span>Governance-led escalation aligned with your existing care model</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap split flip">
    <div class="media wide">{img("consult-elderly", "A clinician speaking warmly with an older woman")}</div>
    <div>
      {label("Organisational partnerships")}
      <h2 class="t-2">For family offices and organisations.</h2>
      <p class="lede">We partner with family offices, leadership teams and small organisations seeking private overnight support for their people and the communities they look after.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">How partnership fees work.</h2>
      <p class="lede">Partnership fees are monthly and tailored to your requirements, following an introductory conversation to ensure clinical suitability.</p>
    </div>
    <div class="tiles c3">
      <article class="tile"><span class="t-tag">First</span><h3>Introductory conversation</h3><p>We learn about your setting, your residents or people, and where nights feel stretched.</p></article>
      <article class="tile"><span class="t-tag">Then</span><h3>Clinical suitability</h3><p>We confirm that our remote overnight model is right for your setting.</p></article>
      <article class="tile"><span class="t-tag">Monthly</span><h3>Tailored partnership</h3><p>A clear monthly arrangement, reviewed with you over time.</p></article>
    </div>
    <p class="note-line">We are currently onboarding a limited number of London partners while our CQC registration is under review.</p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel">
      <span class="label">Partnerships</span>
      <h2 class="t-1">Let&rsquo;s talk about your nights.</h2>
      <p class="lede">Tell us about your organisation and we will arrange an introductory conversation.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/?type=partnership">Partnership enquiry {ARR}</a></div>
    </div>
  </div>
</section>
</main>
""" + footer("night")


def about():
    return head("", "", "/about/", schema=[]) + header("about") + f"""
<main id="main">
{page_intro("About Zinlea Health", "Who we are.", "Zinlea Health is a private, clinician-led healthcare company. We create services for the moments when expert care is hardest to reach, and we build them around calm expertise, discretion and continuity.")}

<section class="sec" style="padding-top:8px">
  <div class="wrap split">
    <div class="media">{img("consult-elderly", "A clinician speaking warmly with an older woman", eager=True)}</div>
    <div>
      {label("Our purpose")}
      <h2 class="t-2">Expert care, without the wait or the worry.</h2>
      <p class="lede">Most healthcare is designed around opening hours. Worry isn&rsquo;t. Zinlea exists so that people can speak to an experienced clinician when they need one, and come away with a clear answer about what to do next.</p>
      <p class="lede">We are a private company, led by clinicians, and we work alongside the NHS and your own GP rather than replacing them.</p>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">What we do.</h2>
      <p class="lede">Zinlea Health is the parent company of two services, each with its own focus.</p>
    </div>
    <div class="teasers">
      <a class="teaser" href="/night/"><span class="t-k">London &middot; 20:00 &ndash; 08:00</span><b>Zinlea Night</b><span class="t-d">Private overnight medical advice. Members speak directly to experienced Advanced Nurse Practitioners by phone or video, with remote prescribing where clinically appropriate and clear escalation when in-person care is needed. Zinlea Night also supports care homes, residences and family offices.</span><span class="circ">{ARR}</span></a>
      <a class="teaser" href="/global/"><span class="t-k">Across Africa &middot; In development</span><b>Zinlea Global</b><span class="t-d">Healthcare partnerships with providers, clinicians and investors across Africa, developing new services together as equal partners, with knowledge flowing in both directions.</span><span class="circ">{ARR}</span></a>
    </div>
  </div>
</section>

<section class="sec-lg">
  <div class="wrap">
    <p class="two-tone">Good healthcare should feel private, professional and unhurried. <span>Whatever the hour, wherever you are.</span></p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">How we work.</h2>
      <p class="lede">The same principles guide every Zinlea service, from a single overnight call to a new partnership.</p>
    </div>
    <div class="tiles c3">
      <article class="tile"><span class="t-tag">How we speak to you</span><h3>Calm expertise</h3><p>Clinical advice delivered thoughtfully and without rush, by experienced clinicians who listen carefully.</p></article>
      <article class="tile"><span class="t-tag">How we treat your information</span><h3>Discretion</h3><p>Private care with complete respect for confidentiality and personal boundaries.</p></article>
      <article class="tile"><span class="t-tag">How we stay with you</span><h3>Continuity</h3><p>Relationships built over time, so you are supported consistently.</p></article>
      <article class="tile"><span class="t-tag">How we keep you safe</span><h3>Safety first</h3><p>Clear escalation pathways, and honesty about what remote care can and cannot do.</p></article>
      <article class="tile"><span class="t-tag">How we are governed</span><h3>Accountability</h3><p>Clinical protocols, incident reporting, clinical audit and continuous service review.</p></article>
      <article class="tile"><span class="t-tag">How we work with others</span><h3>Partnership</h3><p>We complement the NHS, your GP and our partners, and we coordinate with them when needed.</p></article>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap split flip">
    <div class="media">{img("nurse", "An Advanced Nurse Practitioner in uniform")}</div>
    <div>
      {label("Our clinicians")}
      <h2 class="t-2">Experienced, calm and thorough.</h2>
      <p class="lede">Our clinicians are experienced Advanced Nurse Practitioners with backgrounds across urgent care, primary care and acute services. They are registered with their professional bodies, work within defined clinical protocols, and are trained in remote consultation safety, safeguarding and patient experience standards.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      {label("Regulation and safety")}
      <h2 class="t-2">Transparent about where we are.</h2>
      <p class="lede">Zinlea Night has submitted an application for registration with the Care Quality Commission (CQC), the independent regulator of health and social care in England. While our application is under review, we operate as a clinician-led private healthcare service, in line with UK clinical guidelines and professional standards.</p>
      <div class="actions"><a class="btn btn-quiet" href="/clinical-governance/">Read our clinical governance {ARR}</a></div>
    </div>
    <div class="trust two">
      <div><b>Clinician-led</b><span>Advanced Nurse Practitioners</span></div>
      <div><b>CQC application</b><span>Submitted, under review</span></div>
      <div><b>UK GDPR</b><span>Data Protection Act 2018</span></div>
      <div><b>Safeguarding</b><span>Adults and children</span></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel">
      <span class="label">Get in touch</span>
      <h2 class="t-1">We would like to hear from you.</h2>
      <p class="lede">Whether you are interested in membership, a partnership or Zinlea Global, we reply to every enquiry within 24 hours.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/">Contact us {ARR}</a><a class="btn btn-quiet" href="/faq/">Read the FAQ</a></div>
    </div>
  </div>
</section>
</main>
""" + footer()


FAQ = [
    ("general", "About Zinlea", [
        ("What is Zinlea Health?", "Zinlea Health is a private, clinician-led healthcare company. It is home to Zinlea Night, which provides overnight clinical advice in London, and Zinlea Global, which builds healthcare partnerships across Africa."),
        ("How do I get in touch?", f'Use our <a href="/contact/">contact form</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. We reply to every enquiry within 24 hours.'),
        ("Is Zinlea regulated?", 'Zinlea Night has submitted an application for registration with the Care Quality Commission (CQC), the independent regulator of health and social care in England. While the application is under review, Zinlea Night operates as a clinician-led private healthcare service. Read more on our <a href="/clinical-governance/">clinical governance</a> page.'),
        ("How do you look after my information?", 'We operate in accordance with UK GDPR, the Data Protection Act 2018 and medical confidentiality standards. Patient information is stored securely, accessed only by authorised clinicians and used solely for care. See our <a href="/privacy/">privacy policy</a>.'),
    ]),
    ("night", "Zinlea Night", [
        ("What is Zinlea Night?", "A private membership providing overnight medical advice in London through experienced Advanced Nurse Practitioners, from 8pm to 8am."),
        ("Who will I speak to?", "You speak directly with an experienced Advanced Nurse Practitioner, with a background across urgent care, primary care or acute services."),
        ("How do consultations take place?", "By telephone or video. Zinlea Night is a remote service by design: we do not provide home visits or in-person examinations. When you need in-person care, we guide you to the right service."),
        ("Can you prescribe medication?", "Yes, where it is clinically appropriate and safe, after proper assessment. Some medications cannot be prescribed remotely, and controlled drugs and high-risk medicines may be restricted. Prescribing decisions remain at the clinician's professional discretion."),
        ("Is Zinlea Night an emergency service?", "No. If you or someone else has chest pain, difficulty breathing, loss of consciousness, severe bleeding, signs of stroke or any life-threatening symptoms, call 999 immediately or go to your nearest A&amp;E. Zinlea Night cannot dispatch ambulances."),
        ("Does Zinlea Night replace my GP?", "No. Zinlea Night complements your registered GP, NHS urgent care and hospital services. We encourage members to stay in touch with their GP for ongoing and long-term needs."),
        ("How much does membership cost?", 'Individual membership starts from &pound;85 a month and Family membership from &pound;225 a month. Partnerships are tailored, and Private Client fees are agreed after a private consultation. See <a href="/night/membership/">membership</a>.'),
        ("How do I become a member?", 'Request membership through our <a href="/contact/?type=member">enquiry form</a>. We reply within 24 hours, then arrange a brief onboarding call to understand your needs and confirm your membership.'),
        ("What is Private Client?", 'Our most personal service: a named lead clinician, coordination with specialist consultants and your own doctors, and a care plan built around you. It is arranged individually after a private consultation. <a href="/night/private-client/">Learn more</a>.'),
        ("Do you work with care homes and organisations?", 'Yes. We partner with a small number of care homes, residences, family offices and organisations to provide overnight escalation support. <a href="/night/partnerships/">About partnerships</a>.'),
    ]),
    ("global", "Zinlea Global", [
        ("What is Zinlea Global?", "Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new healthcare services together, as equal partners."),
        ("Is Zinlea Global operating yet?", "Zinlea Global is in development. We are currently speaking with prospective founding partners."),
        ("Who can partner with Zinlea Global?", 'Hospital groups, private clinics, clinicians and investors. <a href="/contact/?type=global">Register your interest</a> and we will be in touch.'),
    ]),
]


def faq():
    def strip(t):
        return re.sub(r"<[^>]+>", "", t).replace("&amp;", "&").replace("&pound;", "£")
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
        for _, _, items in FAQ for q, a in items]}
    jump = "".join(f'<a class="chip" href="#{gid}">{title}</a>' for gid, title, _ in FAQ)
    groups = "".join(
        f'<section class="faq-group" id="{gid}"><h2 class="t-3">{title}</h2>'
        + "".join(f'<details class="faq"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in items)
        + "</section>"
        for gid, title, items in FAQ
    )
    return head("FAQ | Zinlea Health", "Answers to common questions about Zinlea Night membership, prescribing, emergencies, Private Client and Zinlea Global.",
                "/faq/", schema=[schema, crumbs("FAQ", "/faq/")]) + header("faq") + f"""
<main id="main">
{page_intro("Questions &amp; answers", "Frequently asked questions.", "Everything you might want to know before getting in touch. If your question isn&rsquo;t here, we are happy to help.", f'<div class="faq-jump">{jump}</div>')}
<section class="sec" style="padding-top:8px">
  <div class="wrap faq-wrap">{groups}</div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap xlinks">
    <a class="xlink" href="/contact/"><span><small>We reply within 24 hours</small><b>Ask us a question</b></span><span class="circ">{ARR}</span></a>
    <a class="xlink" href="/clinical-governance/"><span><small>Regulation and safety</small><b>Clinical governance</b></span><span class="circ">{ARR}</span></a>
  </div>
</section>
</main>
""" + footer()


# --------------------------------------------------------------------------- GLOBAL (first light)
def global_page():
    return head("Zinlea Global | Healthcare partnerships across Africa",
                "Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new healthcare services together.",
                "/global/", theme="global", schema=[GLOBAL_ORG, crumbs("Zinlea Global", "/global/")]) + \
        header("global", sub="global", cta=("Register interest", "/contact/?type=global"), status=False) + f"""
<main id="main">
<section class="dawn-hero">
  <span class="sunrise" aria-hidden="true"></span>
  <div class="wrap">
    {label("Zinlea Global &middot; Now speaking with founding partners")}
    <h1 class="t-hero">Healthcare partnerships, built together.</h1>
    <p class="lede">Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new services, as equal partners from the very first conversation.</p>
    <div class="actions" style="margin-top:36px">
      <a class="btn btn-primary" href="/contact/?type=global">Register interest {ARR}</a>
      <a class="btn btn-quiet" href="#focus" style="color:#F4F0EB;border-color:rgba(244,240,235,.3)">What we build</a>
    </div>
  </div>
</section>

<section class="sec-lg">
  <div class="wrap">
    <p class="two-tone">Africa&rsquo;s healthcare sector is home to outstanding clinicians, entrepreneurs and innovators. <span>We want to build alongside them.</span></p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap split">
    <div class="media wide">{img("global-clinic", "A clinician reviewing results with a colleague")}</div>
    <div>
      {label("Why partnership")}
      <h2 class="t-2">Each side brings what it knows best.</h2>
      <p class="lede">We bring our experience of running a private, clinician-led overnight service. Our partners bring their own expertise, relationships and deep understanding of their markets.</p>
      <p class="lede">Together, we can develop services that neither of us could build alone, and learn from each other along the way.</p>
    </div>
  </div>
</section>

<section class="sec alt" id="focus">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">What we can build together.</h2>
      <p class="lede">Three areas where we are looking to collaborate.</p>
    </div>
    <div class="tiles c3">
      <article class="tile"><span class="t-tag">Hospitals &amp; clinics</span><h3>Provider partnerships</h3><p>Working with hospital groups and private clinics to develop new services, including out-of-hours and remote clinical support.</p></article>
      <article class="tile"><span class="t-tag">Both directions</span><h3>Shared learning</h3><p>Exchanging clinical protocols, escalation pathways and training, with knowledge flowing in both directions.</p></article>
      <article class="tile"><span class="t-tag">Built to last</span><h3>Models of care</h3><p>Co-designing sustainable service models with partners and investors.</p></article>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split flip">
    <div class="media">{img("global-partnership", "Two professionals shaking hands across a meeting table")}</div>
    <div>
      {label("How we work")}
      <h2 class="t-2">Partnership, from the first conversation.</h2>
      <p class="lede">Every Zinlea Global partnership starts by listening, and every decision is made together.</p>
      <div class="timeline" style="margin-top:32px;grid-template-columns:1fr">
        <div class="tl" style="grid-template-columns:150px 1fr;background:none;border-radius:0;border-bottom:1px solid var(--line);padding:22px 0"><span class="when" style="padding:6px 0 0">First</span><div><h3>Listen</h3><p>Understand your organisation, goals and community.</p></div></div>
        <div class="tl" style="grid-template-columns:150px 1fr;background:none;border-radius:0;border-bottom:1px solid var(--line);padding:22px 0"><span class="when" style="padding:6px 0 0">Then</span><div><h3>Design</h3><p>Shape the service model, governance and plan together.</p></div></div>
        <div class="tl" style="grid-template-columns:150px 1fr;background:none;border-radius:0;border-bottom:1px solid var(--line);padding:22px 0"><span class="when" style="padding:6px 0 0">Over time</span><div><h3>Grow</h3><p>Launch, review and scale what works.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap explain-grid">
    <div>
      {label("Who we work with")}
      <h2 class="t-2" style="margin-top:18px">Partners across Africa&rsquo;s healthcare sector.</h2>
      <p class="lede" style="margin-top:22px">Zinlea Global is in development. We are speaking with prospective founding partners who share our commitment to safe, clinician-led and sustainable care.</p>
    </div>
    <ul class="checks">
      <li><span><b>Hospital groups and private clinics</b> developing new services, including out-of-hours and remote clinical support</span></li>
      <li><span><b>Clinicians and clinical leaders</b> interested in shared protocols, training and knowledge exchange</span></li>
      <li><span><b>Investors and development partners</b> backing sustainable models of care</span></li>
      <li><span><b>Organisations</b> looking for a clinician-led partner with experience of running a private remote service</span></li>
    </ul>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel dawn">
      <span class="label">Founding partners</span>
      <h2 class="t-1">Build the future of care with us.</h2>
      <p class="lede">If you are a healthcare provider, clinician or investor in Africa, we would like to hear from you.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/?type=global">Register interest {ARR}</a></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap xlinks">
    <a class="xlink" href="/"><span><small>Zinlea Health</small><b>About Zinlea</b></span><span class="circ">{ARR}</span></a>
    <a class="xlink" href="/night/"><span><small>London, 8pm to 8am</small><b>Zinlea Night</b></span><span class="circ">{ARR}</span></a>
  </div>
</section>
</main>
""" + footer("global")


# --------------------------------------------------------------------------- CONTACT
def contact():
    pills = "".join(
        f'<span><input type="radio" id="t-{v}" name="inquiry-type" value="{v}" required><label for="t-{v}">{t}</label></span>'
        for v, t in [("member", "Night membership"), ("private-client", "Private Client"), ("partnership", "Night partnership"), ("global", "Zinlea Global"), ("general", "Something else")]
    )
    return head("Contact | Zinlea Health", "Enquire about Zinlea Night membership, partnerships or Zinlea Global. We reply within 24 hours.",
                "/contact/", schema=[ORG, crumbs("Contact", "/contact/")]) + header("contact") + f"""
<main id="main">
<section class="sec" style="padding-top:56px">
  <div class="wrap contact">
    <div>
      {label("Contact")}
      <h1 class="t-1">Let&rsquo;s talk, privately.</h1>
      <p class="lede">Tell us a little about yourself and a member of our team will reply personally.</p>
      <ul class="c-list">
        <li><span>Email</span><b>{EMAIL}</b></li>
        <li><span>Response time</span><b>Within 24 hours</b></li>
        <li><span>Zinlea Night hours</span><b class="mono">20:00 &ndash; 08:00</b></li>
      </ul>
    </div>
    <div class="form-card">
      <form class="form" name="enquiry" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="website-url" data-enquiry novalidate>
        <input type="hidden" name="form-name" value="enquiry">
        <p class="vh"><label>Leave this empty <input name="website-url" tabindex="-1" autocomplete="off"></label></p>
        <fieldset class="fld full"><legend>What can we help with?</legend><div class="pills">{pills}</div><span class="err">Please choose one.</span></fieldset>
        <div class="fld"><label for="name">Full name</label><input id="name" name="name" type="text" autocomplete="name" required><span class="err">Please tell us your name.</span></div>
        <div class="fld"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required><span class="err">Please enter a valid email address.</span></div>
        <div class="fld"><label for="phone">Phone <span class="opt">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="fld"><label for="org">Organisation <span class="opt">(optional)</span></label><input id="org" name="organisation" type="text" autocomplete="organization"></div>
        <div class="fld full"><label for="msg">Message</label><textarea id="msg" name="message" required></textarea><span class="err">Please add a short message.</span></div>
        <label class="check full"><input type="checkbox" name="consent" value="yes"> I agree to Zinlea Health contacting me about this enquiry, as set out in the <a href="/privacy/">privacy policy</a>.</label>
        <div class="form-foot full"><small>Please don&rsquo;t include detailed medical information here. In an emergency, call 999.</small><button class="btn btn-primary" type="submit">Send enquiry {ARR}</button></div>
        <p class="form-status full" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
</section>
</main>
""" + footer()


# --------------------------------------------------------------------------- DOCUMENTS
def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"&[a-z]+;", "", t.lower())).strip("-")


def doc_page(slug, title, heading, intro, body, desc, current=""):
    toc = []

    def add_id(m):
        text = m.group(1)
        sid = slugify(text)
        toc.append((sid, text))
        return f'<h2 id="{sid}">{text}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", add_id, body)
    toc_html = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc)
    return head(f"{title} | Zinlea Health", desc, f"/{slug}/", schema=[crumbs(title, f"/{slug}/")]) + header(current) + f"""
<main id="main">
<section class="sec" style="padding-top:56px">
  <div class="wrap">
    {label(title)}
    <h1 class="t-1" style="margin:22px 0 20px;max-width:18ch">{heading}</h1>
    <p class="lede" style="margin-bottom:72px">{intro}</p>
    <div class="doc">
      <nav class="toc" aria-label="On this page"><ul>{toc_html}</ul></nav>
      <div class="prose">{body}</div>
    </div>
  </div>
</section>
</main>
""" + footer()


def thank_you():
    return head("Thank you | Zinlea Health", "Thank you for your enquiry.", "/thank-you/", noindex=True) + header() + f"""
<main id="main">
<section class="sec-lg">
  <div class="wrap" style="max-width:900px;text-align:center">
    {label("Enquiry received")}
    <h1 class="t-1" style="margin:22px 0 20px">Thank you. We&rsquo;ll be in touch.</h1>
    <p class="lede" style="margin:0 auto 36px">A member of our team will reply personally within 24 hours.</p>
    <a class="btn btn-primary" href="/">Return home {ARR}</a>
  </div>
</section>
</main>
""" + footer()


PAGES = {
    "index.html": home,
    "night/index.html": night,
    "night/membership/index.html": night_membership,
    "night/private-client/index.html": night_private_client,
    "night/how-it-works/index.html": night_how,
    "night/partnerships/index.html": night_partnerships,
    "about/index.html": about,
    "faq/index.html": faq,
    "global/index.html": global_page,
    "contact/index.html": contact,
    "thank-you/index.html": thank_you,
    "clinical-governance/index.html": lambda: doc_page(
        "clinical-governance", "Clinical governance", "Clinical governance, regulation and service information",
        "Transparency, safety and regulatory compliance are at the heart of everything we do.", GOVERNANCE,
        "Zinlea Night's regulatory status, scope of service, prescribing policy and clinical governance framework.", "governance"),
    "privacy/index.html": lambda: doc_page(
        "privacy", "Privacy policy", "Privacy policy",
        "How we collect, use and protect your personal information.", PRIVACY,
        "How Zinlea Health and Zinlea Night collect, use and protect your personal information."),
}

def not_found():
    return head("", "", "/404.html") + header() + f"""
<main id="main">
<section class="sec-lg">
  <div class="wrap" style="max-width:900px">
    {label("Page not found")}
    <h1 class="t-1" style="margin:22px 0 20px">We couldn&rsquo;t find that page.</h1>
    <p class="lede" style="margin-bottom:36px">The page may have moved. These are the most visited parts of the site.</p>
    <div class="xlinks">
      <a class="xlink" href="/night/"><span><small>London, 8pm to 8am</small><b>Zinlea Night</b></span><span class="circ">{ARR}</span></a>
      <a class="xlink" href="/night/membership/"><span><small>From &pound;85 a month</small><b>Membership</b></span><span class="circ">{ARR}</span></a>
      <a class="xlink" href="/about/"><span><small>Who we are</small><b>About Zinlea</b></span><span class="circ">{ARR}</span></a>
      <a class="xlink" href="/contact/"><span><small>We reply within 24 hours</small><b>Contact</b></span><span class="circ">{ARR}</span></a>
    </div>
  </div>
</section>
</main>
""" + footer()


PAGES["404.html"] = not_found

# Old zinlea.com addresses -> new pages (301), so existing search rankings and links carry over.
REDIRECTS = [
    # Only pages that moved. Same-path trailing-slash rules (e.g. /about -> /about/) are left out:
    # Netlify matches both forms to one rule, so they would loop. Netlify adds the slash itself.
    ("/membership", "/night/membership/"),
    ("/how-it-works", "/night/how-it-works/"),
    ("/partnerships", "/night/partnerships/"),
    ("/private-client", "/night/private-client/"),
]

SITEMAP_PRIORITY = {"/": "1.0", "/night/": "0.9", "/night/membership/": "0.9", "/about/": "0.8", "/global/": "0.8",
                    "/night/private-client/": "0.8", "/night/how-it-works/": "0.7", "/night/partnerships/": "0.8",
                    "/faq/": "0.7", "/contact/": "0.6", "/clinical-governance/": "0.5", "/privacy/": "0.3"}


def write(rel, text):
    with open(os.path.join(OUT, rel), "w", encoding="utf-8") as f:
        f.write(text)


def site_files():
    urls = "".join(
        f"""  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{seo.TODAY}</lastmod>\n    <priority>{pr}</priority>\n"""
        f"""    <image:image><image:loc>{SITE}/assets/og/{seo.PAGES[p]['og']}.jpg</image:loc></image:image>\n  </url>\n"""
        for p, pr in SITEMAP_PRIORITY.items())
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")
    write("_redirects", "# Netlify redirects: old zinlea.com pages -> new structure\n" +
          "".join(f"{a}  {b}  301!\n" for a, b in REDIRECTS))
    write("_headers", """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
/assets/*
  Cache-Control: public, max-age=31536000, immutable
/assets/site.css
  Cache-Control: public, max-age=86400
/assets/site.js
  Cache-Control: public, max-age=86400
""")
    write("site.webmanifest", json.dumps({
        "name": "Zinlea Health", "short_name": "Zinlea", "start_url": "/", "display": "standalone",
        "background_color": "#FFFFFF", "theme_color": "#070B17",
        "icons": [{"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/brand/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))


if __name__ == "__main__":
    for path, fn in PAGES.items():
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", path)
    site_files()
    print("wrote sitemap.xml, robots.txt, _redirects, _headers, site.webmanifest")
