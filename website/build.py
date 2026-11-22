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
def head(title, desc, path, theme="health", schema=None, noindex=False):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in (schema or []))
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    colour = {"health": "#FFFFFF", "night": "#070B17", "global": "#08101F"}[theme]
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="{colour}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Zinlea Health">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/night-caring-hands.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{ld}</head>
<body class="theme-{theme}">
<a class="skip-link" href="#main">Skip to content</a>
"""


NAV = [
    ("night", "/night/", "Zinlea Night", "n-night"),
    ("global", "/global/", "Zinlea Global", "n-global"),
    ("membership", "/night/#membership", "Membership", ""),
    ("governance", "/clinical-governance/", "Clinical governance", ""),
    ("contact", "/contact/", "Contact", ""),
]


def header(current="", sub="health", cta=("Enquire", "/contact/"), status=True):
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
            ("/global/", "Zinlea Global", "Partnerships"), ("/night/#membership", "Membership", ""),
            ("/clinical-governance/", "Clinical governance", ""), ("/contact/", "Contact", ""),
        ]
    )
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
          <li><a href="/night/">Overview</a></li><li><a href="/night/#membership">Membership</a></li>
          <li><a href="/night/#how-it-works">How it works</a></li><li><a href="/night/#partnerships">Partnerships</a></li></ul></div>
        <div><h4>Zinlea Global</h4><ul>
          <li><a href="/global/">Overview</a></li><li><a href="/global/#focus">What we build</a></li>
          <li><a href="/contact/?type=global">Register interest</a></li></ul></div>
        <div><h4>Zinlea Health</h4><ul>
          <li><a href="/">Home</a></li><li><a href="/contact/">Contact</a></li></ul></div>
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


def img(name, alt, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="/assets/img/{name}.jpg" alt="{alt}" {load}>'


def label(text, pip=True):
    dot = '<span class="pip" aria-hidden="true"></span>' if pip else ""
    return f'<span class="label">{dot}{text}</span>'


# --------------------------------------------------------------------------- schema
ORG = {"@context": "https://schema.org", "@type": "MedicalOrganization", "@id": f"{SITE}/#org", "name": "Zinlea Health",
       "url": f"{SITE}/", "email": EMAIL, "logo": f"{SITE}/assets/favicon.svg",
       "description": "Private, clinician-led healthcare: overnight clinical advice in London through Zinlea Night, and healthcare partnerships across Africa through Zinlea Global.",
       "subOrganization": [{"@id": f"{SITE}/night/#org"}, {"@id": f"{SITE}/global/#org"}]}
NIGHT_ORG = {"@context": "https://schema.org", "@type": "MedicalBusiness", "@id": f"{SITE}/night/#org", "name": "Zinlea Night",
             "url": f"{SITE}/night/", "email": EMAIL, "parentOrganization": {"@id": f"{SITE}/#org"},
             "description": "Private overnight medical advice in London from experienced Advanced Nurse Practitioners, 8pm to 8am.",
             "areaServed": {"@type": "City", "name": "London"},
             "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                           "opens": "20:00", "closes": "08:00"},
             "makesOffer": [
                 {"@type": "Offer", "name": "Individual membership", "priceSpecification": {"@type": "UnitPriceSpecification", "price": 85, "priceCurrency": "GBP", "unitText": "MONTH"}},
                 {"@type": "Offer", "name": "Family membership", "priceSpecification": {"@type": "UnitPriceSpecification", "price": 225, "priceCurrency": "GBP", "unitText": "MONTH"}}]}
GLOBAL_ORG = {"@context": "https://schema.org", "@type": "MedicalOrganization", "@id": f"{SITE}/global/#org", "name": "Zinlea Global",
              "url": f"{SITE}/global/", "email": EMAIL, "parentOrganization": {"@id": f"{SITE}/#org"}, "areaServed": "Africa"}


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

<section class="sec" style="padding-top:24px">
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
      <div class="actions"><a class="btn btn-primary" href="/night/">How Zinlea Night works {ARR}</a></div>
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


def night():
    return head("Zinlea Night | Overnight clinical advice in London, 8pm to 8am",
                "Private overnight medical advice in London. Experienced Advanced Nurse Practitioners available 8pm to 8am for calm reassurance, clinical guidance and escalation support.",
                "/night/", theme="night", schema=[NIGHT_ORG, crumbs("Zinlea Night", "/night/")]) + \
        header("night", sub="night", cta=("Request membership", "/contact/?type=member")) + f"""
<main id="main">
<section class="d-hero">
  <div class="wrap d-hero-grid">
    <div>
      {label("Zinlea Night &middot; London")}
      <h1 class="t-hero">Clinical advice, 8pm to 8am.</h1>
      <p class="lede">Private overnight medical advice in London through experienced Advanced Nurse Practitioners. Calm reassurance, clear guidance and escalation support while the rest of London sleeps.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/contact/?type=member">Request membership {ARR}</a>
        <a class="btn btn-quiet" href="#partnerships">For care providers</a>
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

<section class="sec-lg">
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
      <article class="tile feature"><span class="t-tag mono">20:00 &ndash; 08:00</span><h3>Overnight access</h3><p>Advanced Nurse Practitioners available throughout the night, every night.</p></article>
      <article class="tile"><span class="t-tag">You and your household</span><h3>Adult &amp; family support</h3><p>Overnight healthcare support for adults and family members when you need it most.</p></article>
      <article class="tile"><span class="t-tag">Treatment options</span><h3>Medication guidance</h3><p>Expert advice on medication, treatment and what to do next.</p></article>
      <article class="tile"><span class="t-tag">Where clinically appropriate</span><h3>Remote prescribing</h3><p>Prescribing decisions are made only after proper assessment, within UK guidelines.</p></article>
      <article class="tile"><span class="t-tag">Clear next steps</span><h3>Reassurance &amp; escalation</h3><p>Clear guidance on when further care is needed, and where to go.</p></article>
      <article class="tile"><span class="t-tag">At your pace</span><h3>Calm consultations</h3><p>Unhurried, thoughtful conversations by telephone or video.</p></article>
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
    </div>
  </div>
</section>

<section class="sec" id="membership">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">Membership.</h2>
      <p class="lede">Simple, transparent pricing. We are currently onboarding a limited number of founding members.</p>
    </div>
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
        <a class="btn btn-quiet" href="/contact/?type=partnership">Enquire</a>
      </article>
    </div>
  </div>
</section>

<section class="sec" id="how-it-works" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head split">
      <h2 class="t-2">From enquiry to your first call.</h2>
      <p class="lede">Simple, discreet access to overnight clinical support.</p>
    </div>
    <div class="timeline">
      <div class="tl"><span class="when">Today</span><div><h3>Request membership</h3><p>Complete our short enquiry form.</p></div></div>
      <div class="tl"><span class="when">Within 24 hours</span><div><h3>We reply</h3><p>A member of our team responds personally.</p></div></div>
      <div class="tl"><span class="when">Onboarding call</span><div><h3>Get to know you</h3><p>A brief call to understand your needs and confirm your membership.</p></div></div>
      <div class="tl"><span class="when">Every night, 20:00</span><div><h3>Call when you need us</h3><p>Overnight advice from our Advanced Nurse Practitioners until 08:00.</p></div></div>
    </div>
  </div>
</section>

<section class="sec alt" id="partnerships">
  <div class="wrap split">
    <div class="media">{img("care-home", "A clinician checking an older resident's blood pressure")}</div>
    <div>
      {label("For care providers")}
      <h2 class="t-2">Overnight support for care homes and residences.</h2>
      <p class="lede">Zinlea Night works with a small number of carefully selected care homes, residences, family offices and organisations, providing overnight escalation support between 8pm and 8am.</p>
      <ul class="checks">
        <li><span>Complements existing care teams with overnight clinical decision support</span></li>
        <li><span>Triage, remote consultation and prescribing where clinically appropriate</span></li>
        <li><span>Tailored after an introductory conversation to ensure clinical suitability</span></li>
      </ul>
      <div class="actions"><a class="btn btn-primary" href="/contact/?type=partnership">Partnership enquiry {ARR}</a></div>
    </div>
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

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="notice">
      <span class="n-num">999</span>
      <p><strong>Zinlea Night is not an emergency service.</strong> If you or someone else has chest pain, difficulty breathing, loss of consciousness, severe bleeding or signs of stroke, call 999 immediately or go to your nearest A&amp;E.</p>
      <a class="arrow-link" href="/clinical-governance/">Read more {ARR}</a>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-panel">
      <span class="label">Founding membership</span>
      <h2 class="t-1">Overnight clinical care, quietly available.</h2>
      <p class="lede">Private access to experienced Advanced Nurse Practitioners, 8pm to 8am.</p>
      <div class="actions"><a class="btn btn-light" href="/contact/?type=member">Request membership {ARR}</a></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap xlinks">
    <a class="xlink" href="/"><span><small>Zinlea Health</small><b>About Zinlea</b></span><span class="circ">{ARR}</span></a>
    <a class="xlink" href="/global/"><span><small>Partnerships across Africa</small><b>Zinlea Global</b></span><span class="circ">{ARR}</span></a>
  </div>
</section>
</main>
""" + footer("night")


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
        for v, t in [("member", "Night membership"), ("partnership", "Night partnership"), ("global", "Zinlea Global"), ("general", "Something else")]
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

if __name__ == "__main__":
    for path, fn in PAGES.items():
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", path)
