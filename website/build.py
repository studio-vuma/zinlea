#!/usr/bin/env python3
"""Build the Zinlea Health static website.

Shared header, footer and form markup live here so every page stays in sync.
Run `python3 website/build.py` after editing; it writes the HTML pages into
website/ (index.html, night/, global/, contact/, clinical-governance/,
privacy/, thank-you/).
"""
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://zinlea.com"
EMAIL = "info@zinlea.com"

ARR = '<svg class="arr" viewBox="0 0 22 9" aria-hidden="true"><path d="M0 4.5h20M16.5 1l3.5 3.5L16.5 8" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'

LOGO = '<span class="logo-word">ZINLEA</span><span class="logo-sub">{sub}</span>'


# --------------------------------------------------------------------------- shell
def head(title, desc, path, schema=None, noindex=False, theme="health"):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in (schema or []))
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#0E1527">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Zinlea Health">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/night-london.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{ld}</head>
<body class="theme-{theme}">
<a class="skip-link" href="#main">Skip to content</a>
"""


NAV = [
    ("night", "/night/", "Zinlea Night", "London"),
    ("global", "/global/", "Zinlea Global", "Africa"),
    ("approach", "/#approach", "Our Approach", ""),
    ("governance", "/clinical-governance/", "Clinical Governance", ""),
    ("contact", "/contact/", "Contact", ""),
]


def header(current="", solid=False, sub="HEALTH", cta=("Enquire", "/contact/")):
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href}"{cur if key == current else ""}>{label}</a></li>'
        for key, href, label, _ in NAV
    )
    drawer = "".join(
        f'<li><a href="{href}">{label}{f"<small>{tag}</small>" if tag else ""}</a></li>'
        for key, href, label, tag in [("home", "/", "Zinlea Health", "Home")] + NAV
    )
    return f"""<div class="utility">
  <div class="container">
    <div class="u-left"><span><span class="dot" aria-hidden="true"></span><span class="u-hide">Zinlea Night &middot; </span>8pm &ndash; 8am</span><span class="u-hide">London &amp; Africa</span></div>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>
<header class="site-header{' solid' if solid else ''}">
  <div class="container">
    <a class="logo" href="/" aria-label="Zinlea Health home">{LOGO.format(sub=sub)}</a>
    <nav class="nav" aria-label="Primary"><ul>{links}</ul></nav>
    <a class="btn btn-line header-cta" href="{cta[1]}">{cta[0]}</a>
    <button class="menu-btn" type="button" aria-controls="drawer" aria-expanded="false">Menu <span class="bars" aria-hidden="true"></span></button>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-label="Menu">
  <div class="drawer-top">
    <a class="logo" href="/" aria-label="Zinlea Health home">{LOGO.format(sub="HEALTH")}</a>
    <button class="drawer-close" type="button">Close &times;</button>
  </div>
  <ul>{drawer}</ul>
  <div class="drawer-foot">
    <a class="btn btn-gold" href="{cta[1]}">{cta[0]} {ARR}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="f-top">
      <div class="f-brand">
        <a class="logo" href="/" aria-label="Zinlea Health home">{LOGO.format(sub="HEALTH")}</a>
        <p>Clinician-led healthcare, quietly available. Overnight clinical support in London through Zinlea Night, and new partnerships across Africa through Zinlea Global.</p>
        <a class="link-arrow" href="mailto:{EMAIL}" >{EMAIL} {ARR}</a>
      </div>
      <div class="f-cols">
        <div><h4>Zinlea Night</h4><ul>
          <li><a href="/night/">Overview</a></li>
          <li><a href="/night/#membership">Membership</a></li>
          <li><a href="/night/#how-it-works">How it works</a></li>
          <li><a href="/night/#partnerships">Partnerships</a></li>
        </ul></div>
        <div><h4>Zinlea Global</h4><ul>
          <li><a href="/global/">Overview</a></li>
          <li><a href="/global/#focus">Our focus</a></li>
          <li><a href="/contact/?type=global">Register interest</a></li>
        </ul></div>
        <div><h4>Company</h4><ul>
          <li><a href="/#approach">Our approach</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul></div>
        <div><h4>Legal</h4><ul>
          <li><a href="/clinical-governance/">Clinical governance</a></li>
          <li><a href="/privacy/">Privacy policy</a></li>
        </ul></div>
      </div>
    </div>
    <p class="f-emergency"><b>Not an emergency service.</b> If you or someone else has chest pain, difficulty breathing, signs of stroke or any life-threatening symptoms, call 999 or go to your nearest A&amp;E.</p>
    <div class="f-bottom">
      <span>&copy; <span data-year>2026</span> Zinlea Health. All rights reserved.</span>
      <span>Registered in England &amp; Wales</span>
    </div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def img(name, alt, cls="", eager=False, sizes=None):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{name}.jpg" alt="{alt}"{c} {loading}>'


ORG = {
    "@context": "https://schema.org",
    "@type": "MedicalOrganization",
    "@id": f"{SITE}/#org",
    "name": "Zinlea Health",
    "url": f"{SITE}/",
    "email": EMAIL,
    "logo": f"{SITE}/assets/favicon.svg",
    "description": "Clinician-led healthcare: overnight clinical support in London through Zinlea Night, and healthcare partnerships across Africa through Zinlea Global.",
    "subOrganization": [{"@id": f"{SITE}/night/#org"}, {"@id": f"{SITE}/global/#org"}],
}
NIGHT_ORG = {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "@id": f"{SITE}/night/#org",
    "name": "Zinlea Night",
    "url": f"{SITE}/night/",
    "email": EMAIL,
    "parentOrganization": {"@id": f"{SITE}/#org"},
    "description": "Private overnight medical advice in London. Experienced Advanced Nurse Practitioners available 8pm–8am for calm reassurance, clinical guidance and escalation support.",
    "areaServed": {"@type": "City", "name": "London"},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "20:00", "closes": "08:00"},
    "makesOffer": [
        {"@type": "Offer", "name": "Individual membership", "priceSpecification": {"@type": "UnitPriceSpecification", "price": 85, "priceCurrency": "GBP", "unitText": "MONTH"}},
        {"@type": "Offer", "name": "Family membership", "priceSpecification": {"@type": "UnitPriceSpecification", "price": 225, "priceCurrency": "GBP", "unitText": "MONTH"}},
    ],
}
GLOBAL_ORG = {
    "@context": "https://schema.org",
    "@type": "MedicalOrganization",
    "@id": f"{SITE}/global/#org",
    "name": "Zinlea Global",
    "url": f"{SITE}/global/",
    "email": EMAIL,
    "parentOrganization": {"@id": f"{SITE}/#org"},
    "areaServed": "Africa",
}


def crumbs(name, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Zinlea Health", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"},
        ],
    }


# --------------------------------------------------------------------------- pages
def home():
    return head(
        "Zinlea Health | Clinician-led care in London and Africa",
        "Zinlea Health is a clinician-led healthcare company. Zinlea Night offers private overnight medical advice in London, 8pm–8am. Zinlea Global brings our standard of care to partners across Africa.",
        "/", [ORG],
    ) + header(solid=True) + f"""
<main id="main">
<section class="hero-panels" aria-label="Zinlea Health and its divisions">
  <div class="hero-intro">
    <span class="kicker rv">Zinlea Health</span>
    <h1 class="display rv d1">Care, <i>quietly</i> exceptional.</h1>
    <p class="lede rv d2">A clinician-led healthcare company. Calm, expert support in London through the night, and a growing commitment to better care across Africa.</p>
    <div class="rv d3"><a class="btn btn-gold" href="/contact/">Make an enquiry {ARR}</a></div>
    <div class="meta rv d3"><span>Clinician-led</span><span>Private &amp; discreet</span><span>London &middot; Africa</span></div>
  </div>
  <a class="panel" href="/night/">
    {img("night-london", "Westminster and Big Ben at dusk, London", eager=True)}
    <span class="p-region">London &middot; 8pm &ndash; 8am</span>
    <h2 class="p-title">Zinlea <i>Night</i></h2>
    <p class="p-desc">Private overnight medical advice from experienced Advanced Nurse Practitioners, for members, families and care providers.</p>
    <span class="p-cta">Discover Zinlea Night {ARR}</span>
  </a>
  <a class="panel global" href="/global/">
    {img("global-acacia", "An acacia tree on the savanna at sunset", eager=True)}
    <span class="p-region">Africa &middot; Partnerships</span>
    <h2 class="p-title">Zinlea <i>Global</i></h2>
    <p class="p-desc">Bringing the Zinlea standard of clinician-led care to partners in Africa&rsquo;s growing healthcare markets.</p>
    <span class="p-cta">Discover Zinlea Global {ARR}</span>
  </a>
</section>

<section class="section-lg" id="about">
  <div class="container intro-statement">
    <div class="side rv">
      <span class="kicker">About Zinlea Health</span>
      <p>One standard of care, delivered through two divisions.</p>
    </div>
    <div>
      <p class="statement rv">We believe good healthcare should feel <em>private, professional and unhurried</em>, whatever the hour and wherever you are.</p>
      <div class="follow">
        <p class="rv d1">Zinlea Health brings together clinicians with backgrounds across urgent care, primary care and acute services. Our first service, Zinlea Night, gives Londoners calm, expert clinical advice during the hours when healthcare can feel hardest to reach.</p>
        <p class="rv d2">Through Zinlea Global, we are now taking that same safety-first, governance-led approach further, working with partners to develop trusted models of care across Africa.</p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-stone">
  <div class="container feature">
    <div class="feature-media rv">
      <div class="frame reveal-img">{img("night-caring-hands", "A clinician gently holding an older patient's hand")}</div>
      <div class="inset">{img("night-bedroom", "A softly lit bedroom at night")}</div>
      <span class="tag">Zinlea Night &middot; London</span>
    </div>
    <div class="feature-body">
      <span class="kicker rv">Overnight clinical support</span>
      <h2 class="h2 rv d1">Overnight medical support, <i>quietly available.</i></h2>
      <p class="lede rv d2">Private overnight medical advice in London through experienced Advanced Nurse Practitioners. Calm reassurance, clear clinical guidance and escalation support, from 8pm to 8am.</p>
      <div class="facts rv d2">
        <div><b>8pm &ndash; 8am</b><span>Every night</span></div>
        <div><b>ANP-led</b><span>Advanced Nurse Practitioners</span></div>
        <div><b>From &pound;85</b><span>Per month</span></div>
      </div>
      <div class="actions rv d3">
        <a class="btn btn-ink" href="/night/">Explore Zinlea Night {ARR}</a>
        <a class="btn btn-line" href="/contact/?type=member">Request membership</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container feature flip">
    <div class="feature-media rv">
      <div class="frame reveal-img">{img("global-clinic", "A clinician reviewing results with a colleague")}</div>
      <div class="inset">{img("global-savanna", "The African savanna at sunset")}</div>
      <span class="tag">Zinlea Global &middot; Africa</span>
    </div>
    <div class="feature-body">
      <span class="kicker rv" style="color:var(--terracotta)">A new chapter</span>
      <h2 class="h2 rv d1">London standards. <i>African ambition.</i></h2>
      <p class="lede rv d2">Zinlea Global is our initiative to bring clinician-led, governance-first care to Africa&rsquo;s growing healthcare markets, in partnership with local providers, clinicians and investors.</p>
      <div class="actions rv d3">
        <a class="btn btn-ink" href="/global/">Explore Zinlea Global {ARR}</a>
        <a class="btn btn-line" href="/contact/?type=global">Register interest</a>
      </div>
    </div>
  </div>
</section>

<section class="section bg-white" id="approach">
  <div class="container">
    <div class="head split-head">
      <div><span class="kicker rv">Our approach</span><h2 class="h2 rv d1" style="margin-top:22px">The principles behind <i>every</i> consultation.</h2></div>
      <p class="lede rv d2">Whether it is a 3am call from a worried parent in Chelsea or a new partnership abroad, the same principles guide how we work.</p>
    </div>
    <div class="principles">
      <article class="principle rv"><span class="n">01</span><h3>Calm expertise</h3><p>Clinical advice delivered thoughtfully and without rush, by experienced clinicians who listen carefully.</p></article>
      <article class="principle rv d1"><span class="n">02</span><h3>Discretion</h3><p>Private care with complete respect for confidentiality and personal boundaries.</p></article>
      <article class="principle rv d2"><span class="n">03</span><h3>Continuity</h3><p>Relationships built over time, so members and partners are supported consistently, night after night.</p></article>
    </div>
  </div>
</section>

<section class="trust" aria-label="Governance">
  <div class="container"><ul>
    <li><b>Clinician-led</b><span>Advanced Nurse Practitioners</span></li>
    <li><b>CQC application</b><span>Registration submitted</span></li>
    <li><b>UK GDPR</b><span>Confidential by design</span></li>
    <li><b>Safety first</b><span>Clear escalation pathways</span></li>
  </ul></div>
</section>

<section class="section">
  <div class="container quote rv">
    <span class="mark" aria-hidden="true">&ldquo;</span>
    <blockquote>Overnight clinical support should feel private, professional and unhurried, with clear guidance and a safety-first approach.</blockquote>
    <cite>The Zinlea philosophy</cite>
  </div>
</section>

<section class="cta-bleed">
  {img("night-london-bus", "London at dusk with Big Ben and a red bus")}
  <div class="container">
    <span class="kicker rv">Speak to us</span>
    <h2 class="h1 rv d1">Peace of mind, <i>through the night.</i></h2>
    <p class="lede rv d2">Founding membership is currently limited while we onboard our first members. We respond to every enquiry within 24 hours.</p>
    <div class="actions rv d3">
      <a class="btn btn-gold" href="/contact/?type=member">Request membership {ARR}</a>
      <a class="btn btn-line-light" href="/contact/?type=partnership">Partnership enquiry</a>
    </div>
  </div>
</section>
</main>
""" + footer()


def night():
    return head(
        "Zinlea Night | Overnight Clinical Support London, 8pm–8am",
        "Private overnight medical advice in London. Experienced Advanced Nurse Practitioners available 8pm–8am for calm reassurance, clinical guidance and escalation support.",
        "/night/", [NIGHT_ORG, crumbs("Zinlea Night", "/night/")], theme="night",
    ) + header("night", sub="NIGHT", cta=("Request Membership", "/contact/?type=member")) + f"""
<main id="main">
<section class="page-hero">
  {img("night-london", "Westminster and Big Ben at dusk, London", eager=True)}
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Zinlea Health</a><span>/</span>Zinlea Night</nav>
    <span class="kicker">Zinlea Night &middot; London</span>
    <h1 class="h1">Overnight medical support, <i>quietly available.</i></h1>
    <p class="lede">Private overnight medical advice in London through experienced Advanced Nurse Practitioners. Calm, expert clinical support from 8pm to 8am.</p>
    <div class="actions">
      <a class="btn btn-gold" href="/contact/?type=member">Request membership {ARR}</a>
      <a class="btn btn-line-light" href="/contact/?type=partnership">Partnership enquiry</a>
    </div>
    <div class="hero-facts">
      <div><b>8pm &ndash; 8am</b><span>Every night</span></div>
      <div><b>ANP-led</b><span>Experienced clinicians</span></div>
      <div><b>24 hours</b><span>Enquiry response</span></div>
    </div>
  </div>
  <span class="scroll-cue">Scroll</span>
</section>

<section class="section-lg">
  <div class="container intro-statement">
    <div class="side rv"><span class="kicker">About Zinlea Night</span><p>Founding membership is currently limited while we onboard our first members.</p></div>
    <div>
      <p class="statement rv">Zinlea Night was created to bring <em>calm, expert</em> overnight medical advice to London during the hours when healthcare access can feel uncertain.</p>
      <div class="follow">
        <p class="rv d1">When you contact Zinlea Night, you speak directly with an experienced Advanced Nurse Practitioner. Consultations are unhurried: we listen carefully, ask the right questions and give clear clinical guidance.</p>
        <p class="rv d2">Unlike a standard out-of-hours GP service, our focus is on continuity and reassurance. When in-person care is needed, we help you understand your options and escalate appropriately.</p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-night">
  <div class="container">
    <div class="head split-head">
      <div><span class="kicker rv" style="color:var(--gold-soft)">Out-of-hours medical support</span><h2 class="h2 rv d1" style="margin-top:22px">What members <i>receive.</i></h2></div>
      <p class="lede rv d2">Private overnight clinical support in London, designed around your comfort and peace of mind.</p>
    </div>
    <ol class="index-list">
      <li class="rv"><span class="n">01</span><h3>Overnight access</h3><p>Access to Advanced Nurse Practitioners throughout the night, 8pm to 8am: reliable out-of-hours medical support in London.</p></li>
      <li class="rv"><span class="n">02</span><h3>Adult &amp; family support</h3><p>Overnight healthcare support for you and the members of your household, when you need it most.</p></li>
      <li class="rv"><span class="n">03</span><h3>Medication guidance</h3><p>Expert advice on medication and treatment options, with remote prescribing where clinically appropriate.</p></li>
      <li class="rv"><span class="n">04</span><h3>Reassurance &amp; escalation</h3><p>Peace of mind, with clear clinical guidance on when further care is needed and where to go.</p></li>
      <li class="rv"><span class="n">05</span><h3>Calm consultations</h3><p>Unhurried, thoughtful clinical conversations by telephone or video, at your pace.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="membership">
  <div class="container">
    <div class="head center">
      <span class="kicker rv">Private membership</span>
      <h2 class="h2 rv d1">Simple, transparent <i>pricing.</i></h2>
      <p class="lede rv d2">Overnight peace of mind in London, for individuals, families and organisations.</p>
    </div>
    <div class="pricing">
      <article class="plan rv">
        <span class="kicker">Individual</span>
        <h3>Personal</h3>
        <p class="for">Personal overnight clinical support.</p>
        <p class="from">From</p>
        <p class="price">&pound;85<small>/ month</small></p>
        <ul><li>Overnight access, 8pm &ndash; 8am</li><li>Advanced Nurse Practitioner consultations</li><li>Medication &amp; treatment guidance</li><li>Reassurance &amp; escalation support</li></ul>
        <a class="btn btn-line" href="/contact/?type=member">Request membership</a>
      </article>
      <article class="plan featured rv d1">
        <span class="kicker" style="color:var(--gold-soft)">Family</span>
        <h3>Household</h3>
        <p class="for">Overnight healthcare support for your household.</p>
        <p class="from">From</p>
        <p class="price">&pound;225<small>/ month</small></p>
        <ul><li>Everything in Individual</li><li>Support for adults &amp; family members</li><li>Continuity with a consistent clinical team</li><li>Unhurried consultations at your pace</li></ul>
        <a class="btn btn-gold" href="/contact/?type=member">Request membership {ARR}</a>
      </article>
      <article class="plan rv d2">
        <span class="kicker">Partnership</span>
        <h3>Organisations</h3>
        <p class="for">Care homes, residences and family offices.</p>
        <p class="from">Monthly</p>
        <p class="price" style="font-size:2.6rem">Tailored</p>
        <ul><li>Overnight clinical decision support</li><li>Triage, remote consultation &amp; prescribing</li><li>Governance-led escalation</li><li>Complements your existing care team</li></ul>
        <a class="btn btn-line" href="/contact/?type=partnership">Enquire</a>
      </article>
    </div>
    <p class="note rv">We are currently onboarding a limited number of founding members.</p>
  </div>
</section>

<section class="section bg-night" id="how-it-works">
  <div class="container">
    <div class="head split-head">
      <div><span class="kicker rv" style="color:var(--gold-soft)">How it works</span><h2 class="h2 rv d1" style="margin-top:22px">From enquiry to <i>consultation.</i></h2></div>
      <p class="lede rv d2">Simple, discreet access to overnight clinical support in London. We keep everything straightforward.</p>
    </div>
    <div class="steps">
      <div class="step rv"><h3>Request membership</h3><p>Complete our short enquiry form. We will respond within 24 hours.</p></div>
      <div class="step rv d1"><h3>Onboarding</h3><p>A brief call to understand your needs and confirm your membership.</p></div>
      <div class="step rv d2"><h3>Overnight access</h3><p>Connect with our Advanced Nurse Practitioners for overnight medical advice, 8pm &ndash; 8am.</p></div>
      <div class="step rv d3"><h3>Ongoing continuity</h3><p>Consistent, reliable overnight clinical support, whenever you need it.</p></div>
    </div>
  </div>
</section>

<section class="section" id="partnerships">
  <div class="container feature">
    <div class="feature-media rv">
      <div class="frame reveal-img">{img("care-home", "A clinician checking an older resident's blood pressure in a care home")}</div>
      <span class="tag">For care providers</span>
    </div>
    <div class="feature-body">
      <span class="kicker rv">Residential &amp; clinical partnerships</span>
      <h2 class="h2 rv d1">Overnight support for <i>care providers.</i></h2>
      <p class="lede rv d2">Zinlea Night works with a small number of carefully selected care homes, residences, family offices and organisations, providing overnight escalation support between 8pm and 8am.</p>
      <ul class="index-list rv d2" style="margin-top:8px">
        <li style="grid-template-columns:40px 1fr;padding:20px 0"><span class="n">&mdash;</span><p>Complements existing care teams with overnight clinical decision support and reassurance.</p></li>
        <li style="grid-template-columns:40px 1fr;padding:20px 0"><span class="n">&mdash;</span><p>Triage, remote consultation and prescribing where clinically appropriate.</p></li>
        <li style="grid-template-columns:40px 1fr;padding:20px 0"><span class="n">&mdash;</span><p>Tailored after an introductory conversation to ensure clinical suitability.</p></li>
      </ul>
      <div class="actions rv d3"><a class="btn btn-ink" href="/contact/?type=partnership">Partnership enquiry {ARR}</a></div>
    </div>
  </div>
</section>

<section class="section bg-stone">
  <div class="container feature flip">
    <div class="feature-media rv">
      <div class="frame reveal-img">{img("nurse", "An Advanced Nurse Practitioner in uniform")}</div>
    </div>
    <div class="feature-body">
      <span class="kicker rv">Our clinicians</span>
      <h2 class="h2 rv d1">Experienced, <i>calm</i> and thorough.</h2>
      <p class="lede rv d2">Zinlea Night is delivered by experienced Advanced Nurse Practitioners with backgrounds across urgent care, primary care and acute services. Our clinicians are trained in remote consultation safety, safeguarding and premium patient experience standards.</p>
      <p class="rv d2" style="color:var(--ink-60)">Zinlea Night is a remote service by design. We do not provide home visits or in-person examinations. When in-person assessment is required, we guide you to the appropriate service.</p>
      <div class="actions rv d3"><a class="link-arrow" href="/clinical-governance/">Clinical governance {ARR}</a></div>
    </div>
  </div>
</section>

<section class="section-tight" style="padding:72px 0">
  <div class="container">
    <div class="notice rv">
      <span class="num">999</span>
      <p><strong>Zinlea Night is not an emergency service.</strong> If you or someone else has chest pain, difficulty breathing, loss of consciousness, severe bleeding or signs of stroke, call 999 immediately or attend your nearest A&amp;E.</p>
      <a class="link-arrow" href="/clinical-governance/">Read more {ARR}</a>
    </div>
  </div>
</section>

<section class="cta-bleed">
  {img("night-bedroom", "A calm, softly lit bedroom at night")}
  <div class="container">
    <span class="kicker rv">Founding membership</span>
    <h2 class="h1 rv d1">Overnight clinical care, <i>quietly available.</i></h2>
    <p class="lede rv d2">Private access to experienced Advanced Nurse Practitioners, 8pm &ndash; 8am.</p>
    <div class="actions rv d3">
      <a class="btn btn-gold" href="/contact/?type=member">Request membership {ARR}</a>
      <a class="btn btn-line-light" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</section>

<section class="xlink" aria-label="Also from Zinlea Health">
  <a href="/">{img("health-hands", "Two people holding hands in reassurance")}<span class="kicker" style="color:var(--gold-soft)">Zinlea Health</span><span class="h3">About the group</span><span class="link-arrow">Discover {ARR}</span></a>
  <a href="/global/">{img("global-acacia", "An acacia tree at sunset")}<span class="kicker" style="color:#E8B48A">Africa</span><span class="h3">Zinlea Global</span><span class="link-arrow">Discover {ARR}</span></a>
</section>
</main>
""" + footer()


def global_page():
    return head(
        "Zinlea Global | Healthcare partnerships across Africa",
        "Zinlea Global brings Zinlea Health's clinician-led, governance-first approach to Africa's growing healthcare markets, in partnership with local providers and investors.",
        "/global/", [GLOBAL_ORG, crumbs("Zinlea Global", "/global/")], theme="global",
    ) + header("global", sub="GLOBAL", cta=("Register Interest", "/contact/?type=global")) + f"""
<main id="main">
<section class="page-hero earth">
  {img("global-acacia", "An acacia tree on the savanna at sunset", eager=True)}
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Zinlea Health</a><span>/</span>Zinlea Global</nav>
    <span class="kicker">Zinlea Global &middot; Africa</span>
    <h1 class="h1">London standards. <i>African ambition.</i></h1>
    <p class="lede">Zinlea Global brings Zinlea Health&rsquo;s clinician-led, governance-first approach to Africa&rsquo;s growing healthcare markets, built in partnership with the people who know them best.</p>
    <div class="actions">
      <a class="btn btn-gold" href="/contact/?type=global">Register interest {ARR}</a>
      <a class="btn btn-line-light" href="#focus">Our focus</a>
    </div>
  </div>
  <span class="scroll-cue">Scroll</span>
</section>

<section class="section-lg">
  <div class="container intro-statement">
    <div class="side rv"><span class="kicker" style="color:var(--terracotta)">The opportunity</span><p>Zinlea Global is in development, and we are speaking with prospective founding partners.</p></div>
    <div>
      <p class="statement rv">Across the continent, demand for private healthcare is growing quickly. We want to help partners meet it with <em>care people can trust.</em></p>
      <div class="follow">
        <p class="rv d1">Our experience in London has shown how much calm expertise, clear escalation and strong clinical governance matter, especially out of hours.</p>
        <p class="rv d2">Zinlea Global will bring those foundations to new markets, shaped with local clinicians and adapted to local needs, culture and regulation.</p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-earth" id="focus">
  <div class="container">
    <div class="head split-head">
      <div><span class="kicker rv">Our focus</span><h2 class="h2 rv d1" style="margin-top:22px">Where we will <i>add value.</i></h2></div>
      <p class="lede rv d2">Three areas where Zinlea&rsquo;s experience can make a practical difference for partners.</p>
    </div>
    <ol class="index-list">
      <li class="rv"><span class="n">01</span><h3>Provider partnerships</h3><p>Working alongside hospital groups and private clinics to strengthen services, including out-of-hours and remote clinical support.</p></li>
      <li class="rv"><span class="n">02</span><h3>Clinical governance &amp; training</h3><p>Sharing protocols, escalation pathways and training, so teams can grow safely and confidently.</p></li>
      <li class="rv"><span class="n">03</span><h3>Models of care</h3><p>Designing sustainable, locally led service models with partners and investors.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container feature">
    <div class="feature-media rv">
      <div class="frame reveal-img">{img("clinician-portrait", "Portrait of a young African woman")}</div>
    </div>
    <div class="feature-body">
      <span class="kicker rv" style="color:var(--terracotta)">How we work</span>
      <h2 class="h2 rv d1">Locally led. <i>Globally informed.</i></h2>
      <p class="lede rv d2">We believe the best care is designed with communities, not for them. Every Zinlea Global partnership starts by listening.</p>
      <div class="facts rv d2">
        <div><b>Listen</b><span>Understand your goals</span></div>
        <div><b>Design</b><span>Co-create the model</span></div>
        <div><b>Grow</b><span>Launch &amp; scale safely</span></div>
      </div>
      <div class="actions rv d3"><a class="btn btn-ink" href="/contact/?type=global">Start a conversation {ARR}</a></div>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="container quote rv">
    <span class="mark" aria-hidden="true" style="color:var(--terracotta)">&ldquo;</span>
    <blockquote>The same calm, safety-first care, wherever our patients and partners are.</blockquote>
    <cite style="color:var(--terracotta)">Zinlea Global</cite>
  </div>
</section>

<section class="cta-bleed earth">
  {img("global-savanna", "The savanna at sunset")}
  <div class="container">
    <span class="kicker rv">Founding partners</span>
    <h2 class="h1 rv d1">Build the future of care <i>with us.</i></h2>
    <p class="lede rv d2">If you are a healthcare provider, clinician or investor in Africa, we would like to hear from you.</p>
    <div class="actions rv d3"><a class="btn btn-gold" href="/contact/?type=global">Register interest {ARR}</a></div>
  </div>
</section>

<section class="xlink" aria-label="Also from Zinlea Health">
  <a href="/">{img("health-hands", "Two people holding hands in reassurance")}<span class="kicker" style="color:var(--gold-soft)">Zinlea Health</span><span class="h3">About the group</span><span class="link-arrow">Discover {ARR}</span></a>
  <a href="/night/">{img("night-london", "London at dusk")}<span class="kicker" style="color:var(--gold-soft)">London</span><span class="h3">Zinlea Night</span><span class="link-arrow">Discover {ARR}</span></a>
</section>
</main>
""" + footer()


def contact():
    return head(
        "Contact | Zinlea Health",
        "Enquire about Zinlea Night membership, partnerships or Zinlea Global. We respond within 24 hours.",
        "/contact/", [ORG, crumbs("Contact", "/contact/")],
    ) + header("contact", solid=True) + f"""
<main id="main">
<section class="section" style="padding-top:calc(var(--header-h) + 38px + 72px)">
  <div class="container contact-grid">
    <div class="contact-aside">
      <span class="kicker rv">Get in touch</span>
      <h1 class="h1 rv d1">Let&rsquo;s talk, <i>privately.</i></h1>
      <p class="lede rv d2">Interested in membership, a partnership or Zinlea Global? Tell us a little about yourself and a member of our team will respond personally.</p>
      <dl class="rv d3">
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Response time</dt><dd>Within 24 hours</dd></div>
        <div><dt>Zinlea Night hours</dt><dd>8pm &ndash; 8am, every night</dd></div>
      </dl>
    </div>
    <form class="form rv d1" name="enquiry" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="website-url" data-enquiry novalidate>
      <input type="hidden" name="form-name" value="enquiry">
      <p class="visually-hidden"><label>Do not fill this in <input name="website-url" tabindex="-1" autocomplete="off"></label></p>
      <div class="fld full">
        <label for="type">Enquiry type</label>
        <select id="type" name="inquiry-type" required>
          <option value="" selected disabled>Select an enquiry type</option>
          <option value="member">Zinlea Night: membership</option>
          <option value="partnership">Zinlea Night: partnership</option>
          <option value="global">Zinlea Global</option>
          <option value="general">General enquiry</option>
        </select>
        <span class="err">Please choose an enquiry type.</span>
      </div>
      <div class="fld">
        <label for="name">Full name</label>
        <input id="name" name="name" type="text" autocomplete="name" required>
        <span class="err">Please tell us your name.</span>
      </div>
      <div class="fld">
        <label for="email">Email address</label>
        <input id="email" name="email" type="email" autocomplete="email" required>
        <span class="err">Please enter a valid email address.</span>
      </div>
      <div class="fld">
        <label for="phone">Phone <span class="opt">(optional)</span></label>
        <input id="phone" name="phone" type="tel" autocomplete="tel">
      </div>
      <div class="fld">
        <label for="org">Organisation <span class="opt">(optional)</span></label>
        <input id="org" name="organisation" type="text" autocomplete="organization">
      </div>
      <div class="fld full">
        <label for="msg">Message</label>
        <textarea id="msg" name="message" required></textarea>
        <span class="err">Please add a short message.</span>
      </div>
      <label class="check full"><input type="checkbox" name="consent" value="yes"> I agree to Zinlea Health contacting me about this enquiry, as described in the <a href="/privacy/">privacy policy</a>.</label>
      <div class="form-foot full">
        <small>Please do not include detailed medical information in this form. For emergencies, call 999.</small>
        <button class="btn btn-ink" type="submit">Send enquiry {ARR}</button>
      </div>
      <p class="form-status full" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
</main>
""" + footer()


def doc_page(slug, title, kicker, heading, intro, body, desc):
    return head(f"{title} | Zinlea Health", desc, f"/{slug}/", [crumbs(title, f"/{slug}/")]) + header(
        "governance" if slug == "clinical-governance" else "", solid=True
    ) + f"""
<main id="main">
<section class="section" style="padding-top:calc(var(--header-h) + 38px + 72px)">
  <div class="container" style="max-width:920px">
    <span class="kicker">{kicker}</span>
    <h1 class="h1" style="margin:22px 0 24px">{heading}</h1>
    <p class="lede" style="margin-bottom:64px">{intro}</p>
    <div class="prose">{body}</div>
  </div>
</section>
</main>
""" + footer()


GOVERNANCE = f"""
<h2>Regulatory status</h2>
<p>Zinlea Night has submitted an application for registration with the Care Quality Commission (CQC), the independent regulator of health and social care services in England.</p>
<p>We are committed to meeting all regulatory requirements and operating in accordance with recognised standards for safe, effective and well-governed healthcare.</p>
<p>While our application is under review, Zinlea Night operates as a clinician-led private healthcare service providing remote consultations, prescribing where appropriate, and personalised overnight care support.</p>
<p>Our service is designed to complement existing NHS and private healthcare provision.</p>
<h2>Scope of service</h2>
<p>Zinlea Night provides private remote consultations and personalised overnight clinical support between 8pm and 8am. Services may include:</p>
<ul><li>Remote video or telephone consultations</li><li>Clinical advice and triage</li><li>Remote prescribing (where clinically appropriate)</li><li>Care planning and follow-up</li><li>Overnight reassurance and guidance</li><li>Coordination with other healthcare providers</li></ul>
<p>All consultations are delivered by appropriately qualified clinicians working within UK clinical guidelines and professional standards.</p>
<h2>Not an emergency service</h2>
<p>Zinlea Night is not an emergency service and does not provide emergency medical response. If you or someone else experiences:</p>
<ul><li>Chest pain</li><li>Difficulty breathing</li><li>Loss of consciousness</li><li>Severe bleeding</li><li>Signs of stroke</li><li>Any life-threatening symptoms</li></ul>
<p><strong>You must call 999 immediately or attend the nearest Accident &amp; Emergency department.</strong> Zinlea Night cannot dispatch ambulances or provide emergency interventions.</p>
<h2>Relationship to your GP &amp; NHS services</h2>
<p>Zinlea Night complements, but does not replace:</p>
<ul><li>Your registered GP</li><li>NHS urgent care</li><li>Hospital services</li><li>Specialist medical care</li></ul>
<p>Patients are encouraged to maintain contact with their GP for ongoing and long-term medical needs. Where appropriate, we may advise you to seek in-person care.</p>
<h2>Clinical governance</h2>
<p>Zinlea Night is establishing a comprehensive clinical governance framework in line with CQC expectations. This includes:</p>
<h3>Clinical leadership</h3>
<p>All clinicians are appropriately qualified, registered with relevant professional bodies, and work within defined clinical protocols.</p>
<h3>Safe prescribing</h3>
<p>Prescribing is undertaken only where clinically appropriate and following proper assessment. Prescribers operate in accordance with UK prescribing guidelines.</p>
<h3>Risk management</h3>
<ul><li>Clear escalation procedures</li><li>Incident reporting</li><li>Clinical audit</li><li>Continuous service review</li></ul>
<h3>Safeguarding</h3>
<p>We maintain safeguarding policies for both adults and children and follow established reporting procedures where concerns arise.</p>
<h3>Quality assurance</h3>
<p>We monitor:</p>
<ul><li>Patient outcomes</li><li>Satisfaction</li><li>Safety incidents</li><li>Service performance</li></ul>
<h2>Prescribing policy</h2>
<p>Zinlea Night offers remote prescribing where clinically appropriate and safe. However:</p>
<ul><li>Not all conditions are suitable for remote prescribing</li><li>Some medications cannot be prescribed remotely</li><li>Clinicians may decline to prescribe if assessment is insufficient</li><li>Controlled drugs and high-risk medications may be restricted</li></ul>
<p>Prescribing decisions remain entirely at the clinician&rsquo;s professional discretion.</p>
<h2>Suitability of remote care</h2>
<p>Remote consultations are not appropriate for all medical situations. Where necessary, we may advise you to:</p>
<ul><li>Seek in-person medical care</li><li>Contact your GP</li><li>Attend urgent care</li><li>Call emergency services</li></ul>
<p>Zinlea Night reserves the right to decline consultation where remote care is not clinically suitable.</p>
<h2>Personalised &amp; concierge care</h2>
<p>Zinlea Night provides a personalised and high-touch service designed for comfort, discretion and continuity. Our concierge-style model may include:</p>
<ul><li>Extended consultation time</li><li>Follow-up guidance</li><li>Coordination with other services</li></ul>
<p>This does not replace clinical judgement or regulatory standards. All care decisions remain based on medical need and safety.</p>
<h2>Data protection &amp; confidentiality</h2>
<p>We are committed to protecting patient privacy and maintaining confidentiality. Zinlea Night operates in accordance with:</p>
<ul><li>UK GDPR</li><li>Data Protection Act 2018</li><li>Medical confidentiality standards</li></ul>
<p>Patient information is:</p>
<ul><li>Stored securely</li><li>Accessed only by authorised clinicians</li><li>Used solely for care provision</li></ul>
<p>Please refer to our <a href="/privacy/">Privacy Policy</a> for full details.</p>
<h2>Patient responsibilities</h2>
<p>By using Zinlea Night, you confirm that:</p>
<ul><li>Information you provide is accurate</li><li>You understand the limits of remote care</li><li>You will seek emergency care when advised</li><li>You will maintain contact with your GP</li></ul>
<h2>Complaints &amp; feedback</h2>
<p>We are committed to continuous improvement and welcome feedback. Complaints can be submitted via <a href="mailto:{EMAIL}">{EMAIL}</a>. All complaints are reviewed through our governance procedures.</p>
"""

PRIVACY = f"""
<p><em>Last updated: April 2026</em></p>
<h2>Introduction</h2>
<p>Zinlea Night (&ldquo;we&rdquo;, &ldquo;us&rdquo;, or &ldquo;our&rdquo;) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our overnight clinical care services.</p>
<p>We are registered in England and Wales and act as the data controller for the personal information we process. We comply with the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018.</p>
<h2>Information we collect</h2>
<h3>Personal information</h3>
<ul><li>Name, email address, phone number</li><li>Membership and account details</li><li>Partnership organisation details (where applicable)</li></ul>
<h3>Health information</h3>
<ul><li>Medical history and symptoms discussed during consultations</li><li>Clinical notes from nurse consultations</li><li>Treatment recommendations and guidance provided</li></ul>
<h3>Technical data</h3>
<ul><li>IP address, browser type, device information</li><li>Pages visited and time spent on our website</li><li>Cookies and similar tracking technologies</li></ul>
<h2>How we use your information</h2>
<ul><li>Provide overnight clinical consultations and services</li><li>Communicate with you about your membership</li><li>Process partnership enquiries</li><li>Improve our services</li><li>Comply with legal and regulatory obligations</li></ul>
<h2>Legal basis for processing</h2>
<ul><li><strong>Consent:</strong> when you explicitly agree to receive communications</li><li><strong>Contract:</strong> when processing is necessary to provide clinical services you&rsquo;ve requested</li><li><strong>Legitimate interests:</strong> for business operations and service improvements</li><li><strong>Legal obligation:</strong> when we must comply with healthcare regulations</li><li><strong>Vital interests:</strong> in emergency situations</li></ul>
<h2>Your rights</h2>
<p>Under UK GDPR, you have the right to:</p>
<ul><li><strong>Access:</strong> request a copy of your personal data</li><li><strong>Rectification:</strong> correct inaccurate or incomplete data</li><li><strong>Erasure:</strong> request deletion of your data</li><li><strong>Restrict processing:</strong> limit how we use your data</li><li><strong>Data portability:</strong> receive your data in a machine-readable format</li><li><strong>Object:</strong> opt out of certain processing activities</li><li><strong>Withdraw consent:</strong> remove previously given consent at any time</li></ul>
<p>To exercise these rights, contact us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Cookies &amp; tracking</h2>
<p>We use cookies and similar technologies on this website. Under UK GDPR and the Privacy and Electronic Communications Regulations (PECR), we only set non-essential cookies (such as analytics) after you have given us your explicit consent. Analytics cookies are blocked by default until you opt in.</p>
<h2>Contact us</h2>
<p>If you have questions about this Privacy Policy, please contact us at <a href="mailto:{EMAIL}">{EMAIL}</a>. You have the right to lodge a complaint with the Information Commissioner&rsquo;s Office (ICO) at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>
"""


def thank_you():
    return head("Thank you | Zinlea Health", "Thank you for your enquiry.", "/thank-you/", noindex=True) + header() + f"""
<main id="main">
<section class="page-hero" style="min-height:100svh;align-items:center">
  {img("night-london", "London at dusk", eager=True)}
  <div class="container">
    <span class="kicker">Enquiry received</span>
    <h1 class="h1">Thank you. <i>We&rsquo;ll be in touch.</i></h1>
    <p class="lede">A member of our team will respond personally within 24 hours.</p>
    <div class="actions"><a class="btn btn-gold" href="/">Return home {ARR}</a></div>
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
        "clinical-governance", "Clinical Governance", "Regulation & service information",
        "Clinical governance, <i>regulation</i> &amp; service information",
        "Transparency, safety and regulatory compliance are at the heart of everything we do.",
        GOVERNANCE,
        "Zinlea Night's regulatory status, scope of service, prescribing policy and clinical governance framework.",
    ),
    "privacy/index.html": lambda: doc_page(
        "privacy", "Privacy Policy", "Legal", "Privacy <i>policy</i>",
        "Your privacy matters. Here&rsquo;s how we collect, use and protect your personal information.",
        PRIVACY,
        "How Zinlea Health and Zinlea Night collect, use and protect your personal information.",
    ),
}

if __name__ == "__main__":
    for path, fn in PAGES.items():
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", path)
