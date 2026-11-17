"""Build the Zinzile Vuma website.

All copy lives in this file and in content.py. Run:  python3 src/build.py
Pages are written to ../site as folder/index.html so URLs stay clean.
"""
import html, json, pathlib, shutil, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import (SITE, EMAIL, NAME, TITLE, SERVICES, ARTICLES, WORK, IMAGES, CLIENTS, SECTORS)

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
YEAR = 2026
e = html.escape
TITLE_H = html.escape(TITLE)


# ---------------------------------------------------------------- helpers
def pic(name, alt, sizes="100vw", lazy=True, cls=""):
    """Responsive photograph (3:2 source, 800 and 1600 wide)."""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return (f'<picture><source type="image/webp" srcset="/img/{name}-800.webp 800w, /img/{name}-1600.webp 1600w" sizes="{sizes}">'
            f'<img{(" class=" + chr(34) + cls + chr(34)) if cls else ""} src="/img/{name}-1600.jpg" srcset="/img/{name}-800.jpg 800w, /img/{name}-1600.jpg 1600w" sizes="{sizes}" alt="{e(alt)}" width="1600" height="1067"{load}></picture>')


def portrait(kind, sizes, lazy=True, alt=f"Portrait of {NAME}"):
    small, large, w, h = {"4x5": (640, 1040, 1040, 1300), "1x1": (480, 740, 740, 740), "3x4": (640, 990, 990, 1320)}[kind]
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    base = f"/img/zv-portrait-{kind}"
    return (f'<picture><source type="image/webp" srcset="{base}-{small}.webp {small}w, {base}-{large}.webp {large}w" sizes="{sizes}">'
            f'<img src="{base}-{large}.jpg" srcset="{base}-{small}.jpg {small}w, {base}-{large}.jpg {large}w" sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}"{load}></picture>')


def credit(name):
    i = IMAGES[name]
    if i["licence"]:
        return f'{e(i["caption"])}. Photograph: {e(i["artist"])}, {e(i["licence"])}.'
    return f'{e(i["caption"])}.' + (f' Image: {e(i["via"])}.' if i["via"] else "")


def arrow():
    return '<span class="arr" aria-hidden="true">&rarr;</span>'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


NAV = [("/advisory/", "Advisory"), ("/perspectives/", "Perspectives"), ("/about/", "About")]


def page(path, title, desc, body, section=None, schema=None, noindex=False, og_type="website"):
    url = SITE + path
    nav = "".join(f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if section == h else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if section == h else ""}>{t}</a>' for h, t in [("/", "Home")] + NAV)
    adv = "".join(f'<li><a href="/advisory/{s["slug"]}/">{e(s["short"])}</a></li>' for s in SERVICES)
    schemas = "".join(jsonld(s) for s in (schema or []))
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F1B2D">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/newsreader-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
{schemas}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="wordmark" href="/" aria-label="{NAME}, home"><span class="n">{NAME}</span><span class="t">Private Advisory &middot; London</span></a>
    <nav class="nav" aria-label="Main">{nav}<a class="btn" href="/enquire/">Request a consultation</a></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">{mnav}<a class="btn" href="/enquire/">Request a consultation</a></nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="wordmark" href="/"><span class="n">{NAME}</span><span class="t">{TITLE_H}</span></a>
        <p>An independent advisory practice for founders, executives and institutions building value across African and international markets.</p>
      </div>
      <div><h2>Advisory</h2><ul>{adv}</ul></div>
      <div><h2>Practice</h2><ul><li><a href="/about/">About</a></li><li><a href="/perspectives/">Perspectives</a></li><li><a href="/enquire/">Request a consultation</a></li></ul></div>
      <div><h2>Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li style="color:var(--on-navy-muted)">London, working internationally</li></ul></div>
    </div>
    <div class="foot-base"><span>&copy; {YEAR} {NAME}</span><a href="/privacy/">Privacy</a><a href="/credits/">Photography credits</a></div>
  </div>
</footer>
<script src="/js/site.js" defer></script>
</body>
</html>
"""


def write(path, content):
    target = ROOT / (path.strip("/") + "/index.html" if path not in ("/404",) else "404.html")
    if path == "/":
        target = ROOT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print("built", path)


def invite(title="Request a private consultation", text=None, area=None, navy=False):
    text = text or "An initial conversation to explore your objectives, understand the nature of the strategic challenge and establish whether there is a basis for working together."
    href = "/enquire/" + (f"?area={area}" if area else "")
    return f"""<section class="section{' on-navy' if navy else ' on-paper'}">
  <div class="wrap invite reveal">
    <span class="label">Private enquiry</span>
    <h2>{title}</h2>
    <p class="lede">{text}</p>
    <div class="actions"><a class="btn" href="{href}">Request a consultation {arrow()}</a></div>
  </div>
</section>"""


# ---------------------------------------------------------------- schema
PERSON = {"@type": "Person", "@id": SITE + "/#person", "name": NAME, "jobTitle": TITLE,
          "image": SITE + "/img/zv-portrait-4x5-1040.jpg", "url": SITE + "/about/", "email": "mailto:" + EMAIL,
          "workLocation": {"@type": "Place", "name": "London, United Kingdom"},
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Regent's University London"},
          "knowsAbout": ["Luxury brand strategy", "International market entry", "Provenance and origin-led value creation",
                         "Strategic foresight", "Market intelligence", "Destination positioning", "African markets"]}
ORG = {"@type": "ProfessionalService", "@id": SITE + "/#practice", "name": NAME, "url": SITE + "/",
       "description": "Independent luxury and strategic advisory practice for founders, executives and institutions building value across African and international markets.",
       "email": EMAIL, "image": SITE + "/img/og.jpg", "founder": {"@id": SITE + "/#person"},
       "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
       "areaServed": ["Africa", "Europe", "Middle East", "North America"],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Advisory", "itemListElement": [
           {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"], "description": s["positioning"],
                                               "url": f'{SITE}/advisory/{s["slug"]}/'}} for s in SERVICES]}}


def crumbs(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- home
def home():
    idx = "".join(f'''<a href="/advisory/{s["slug"]}/"><span class="num">{s["num"]}</span><h3>{e(s["title"])}</h3><p>{e(s["positioning"])}</p><span class="go" aria-hidden="true">&rarr;</span></a>''' for s in SERVICES)
    teasers = "".join(f'''<a class="teaser reveal" href="/perspectives/{a["slug"]}/"><div class="img">{pic(a["image"], "", "(min-width: 900px) 30vw, 100vw")}</div><span class="label">{e(a["kind"])}</span><h3>{e(a["title"])}</h3><p>{e(a["standfirst"])}</p></a>''' for a in ARTICLES)
    sectors = "".join(f"<li>{e(x)}</li>" for x in SECTORS)
    clients = "".join(f"<li>{e(x)}</li>" for x in CLIENTS)
    body = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="who">{NAME} &middot; {TITLE_H}</p>
      <h1><span>Understanding where markets are.</span> <span>Anticipating where they are going.</span> <span>Positioning businesses for what comes next.</span></h1>
      <p class="lede">I work directly with founders, executives and institutions to navigate complex markets, develop distinctive positioning and identify opportunities for long-term commercial value.</p>
      <div class="actions"><a class="btn" href="/advisory/">Explore the advisory {arrow()}</a><a class="link" href="/about/">Meet Zinzile {arrow()}</a></div>
    </div>
    <figure class="portrait">{portrait("4x5", "(min-width: 900px) 34vw, 90vw", lazy=False)}<figcaption><strong>{NAME}</strong>{TITLE_H}, London</figcaption></figure>
  </div>
</section>

<section class="section ruled" style="border-top:1px solid var(--line)">
  <div class="wrap">
    <div class="split reveal">
      <div><span class="label">The practice</span><h2>Senior counsel, given personally.</h2></div>
      <div class="body">
        <p class="lede">My advisory practice sits where luxury brand strategy, commercial intelligence and African market knowledge meet.</p>
        <p>I advise founders, executives, investors and public institutions on how brands, businesses and places are positioned, valued and developed in international markets. Every engagement is led by me. Clients work directly with the person developing the thinking, from the first conversation to the final recommendation.</p>
      </div>
    </div>
    <div class="triad reveal">
      <div><h3>Where markets are</h3><p>A grounded understanding of buyers, competitors, commercial conditions and institutions as they stand today.</p></div>
      <div><h3>Where they are going</h3><p>Disciplined attention to emerging behaviours, structural change and opportunities others have not yet recognised.</p></div>
      <div><h3>What comes next</h3><p>Positioning and strategic choices made early enough to create lasting advantage.</p></div>
    </div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap">
    <div class="section-head reveal"><span class="label">Areas of advisory</span><h2>Six disciplines, shaped around each engagement.</h2><p class="muted">Clients engage me in one discipline or across several. The scope is developed around the circumstances, not chosen from a menu.</p></div>
    <nav class="index reveal" aria-label="Advisory disciplines">{idx}</nav>
    <div class="actions"><a class="link" href="/advisory/">How I work with clients {arrow()}</a></div>
  </div>
</section>

<section class="section on-navy">
  <div class="wrap advisor">
    <figure class="reveal">{portrait("3x4", "(min-width: 900px) 34vw, 90vw")}</figure>
    <div class="reveal">
      <span class="label">The principal advisor</span>
      <h2>{NAME}</h2>
      <p class="role">{TITLE_H}</p>
      <div class="body">
        <p>I am an independent advisor working where luxury, strategy and African enterprise meet. My background is in luxury brand management, and my perspective spans the United Kingdom and Southern Africa.</p>
        <p>I take on a limited number of engagements at a time. You deal with me directly: I lead the thinking, direct the research and remain your point of contact throughout.</p>
      </div>
      <div class="actions"><a class="btn" href="/about/">About Zinzile {arrow()}</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="label">Strategic perspectives</span><h2>Independent thinking on markets, origin and value.</h2></div>
    <div class="teasers">{teasers}</div>
    <div class="actions"><a class="link" href="/perspectives/">All perspectives and selected work {arrow()}</a></div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap">
    <div class="split reveal">
      <div><span class="label">Perspective</span><h2>From London, with a pan-African and international view.</h2></div>
      <div class="body">
        <p class="lede">London is the base of the practice. Its perspective is pan-African and global.</p>
        <p>I am interested in the relationship between African commercial opportunity and international markets, in both directions: African producers, brands and destinations building positions in Europe, the Gulf and North America, and international brands, investors and organisations considering African markets.</p>
      </div>
    </div>
    <div class="cols reveal">
      <div><h3>Sectors of focus</h3><ul class="ruled-list">{sectors}</ul></div>
      <div><h3>Who I advise</h3><ul class="ruled-list">{clients}</ul></div>
    </div>
  </div>
</section>

{invite(navy=True)}"""
    desc = "Independent luxury and strategic advisory. Zinzile Vuma works directly with founders, executives and institutions on positioning, international markets, provenance and strategic foresight."
    write("/", page("/", f"{NAME} | Luxury and Strategic Advisory, London", desc, body,
                    schema=[{"@context": "https://schema.org", "@graph": [PERSON, ORG,
                             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "inLanguage": "en-GB"}]}]))


# ---------------------------------------------------------------- advisory overview
def advisory():
    discs = ""
    for s in SERVICES:
        areas = "".join(f"<li>{e(a)}</li>" for a in s["areas"][:6])
        discs += f"""<article class="disc reveal" id="{s['slug']}">
      <div><span class="label">{s['num']}</span><h2>{e(s['title'])}</h2></div>
      <div><p class="pos">{e(s['positioning'])}</p><p style="margin-top:14px">{e(s['summary'])}</p><ul class="areas">{areas}</ul><a class="link" href="/advisory/{s['slug']}/">Explore {e(s['short'])} {arrow()}</a></div>
    </article>"""
    clients = "".join(f"<li>{e(x)}</li>" for x in CLIENTS)
    sectors = "".join(f"<li>{e(x)}</li>" for x in SECTORS)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="label">Advisory</span>
    <h1>Strategic counsel across brand, market and origin.</h1>
    <p class="lede">I advise founders, executives and institutions on how brands, businesses and places are positioned, valued and developed in international markets, with particular depth in African markets and their relationship to global ones.</p>
    <div class="principal">{portrait("1x1", "88px", lazy=False)}<div><p><strong>{NAME}</strong> <span class="role">&middot; {TITLE_H}</span></p><p class="muted">Every engagement is led by me. You work with me directly, from the first conversation to the final recommendation. <a href="/about/">About Zinzile</a></p></div></div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">{discs}</div>
</section>

<section class="section on-paper">
  <div class="wrap split reveal">
    <div><span class="label">Scope</span><h2>Disciplines, not packages.</h2></div>
    <div class="body">
      <p class="lede">These disciplines describe the areas in which I advise. They are not fixed products.</p>
      <p>Many engagements draw on two or three. A decision about entering a market may depend on positioning and provenance; a destination strategy may need research before anything else. We agree the scope together, once I understand the question you are trying to answer, and it is set out in a written proposal before any work begins.</p>
    </div>
  </div>
</section>

<section class="section on-navy" id="approach">
  <div class="wrap">
    <div class="section-head reveal"><span class="label">How I work</span><h2>We work on the problem together.</h2><p class="lede">Clients do not hand me a brief and wait for a report. The most useful strategy comes from combining what you know about your business with an independent view from outside it.</p></div>
    <div class="bring reveal">
      <div><h3>What you bring</h3><p>Knowledge of the business, its ambitions and its operating realities, and the commercial objectives and constraints any recommendation must respect.</p></div>
      <div><h3>What I bring</h3><p>Independent research and market intelligence, critical analysis, an external perspective, and an understanding of how luxury and international markets work.</p></div>
      <div><h3>What we do together</h3><p>Examine the problem, challenge assumptions, weigh the alternatives and arrive at a strategic direction you can act on with confidence.</p></div>
    </div>
    <ul class="together reveal">
      <li>Direct engagement with me throughout</li>
      <li>A clear understanding of your objectives and circumstances</li>
      <li>Perspectives developed together, with assumptions tested openly</li>
      <li>Independent research and critical analysis</li>
      <li>Careful consideration of commercial implications</li>
      <li>Clear strategic recommendations and direction</li>
      <li>Continued advisory support where it is useful</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="label">Who I advise</span><h2>Private enterprise and public institutions alike.</h2></div>
    <div class="cols reveal"><div><h3>Clients</h3><ul class="ruled-list">{clients}</ul></div><div><h3>Sectors of focus</h3><ul class="ruled-list">{sectors}</ul></div></div>
  </div>
</section>

{invite()}"""
    desc = "Six advisory disciplines: luxury brand strategy, international market entry, provenance and value creation, commercial development, institutional and destination advisory, and strategic research."
    write("/advisory/", page("/advisory/", f"Advisory | {NAME}", desc, body, section="/advisory/",
                             schema=[{"@context": "https://schema.org", **ORG}, crumbs(("Home", "/"), ("Advisory", "/advisory/"))]))


# ---------------------------------------------------------------- service pages
def service(i, s):
    areas = "".join(f"<li>{e(a)}</li>" for a in s["areas"])
    rel = "".join(f"<li>{e(r)}</li>" for r in s["relevant"])
    qs = "".join(f"<li>{e(q)}</li>" for q in s["questions"])
    contrib = "".join(f"<p>{e(p)}</p>" for p in s["contribution"])
    chall = "".join(f"<p>{e(p)}</p>" for p in s["challenge"])
    prev_s, next_s = SERVICES[i - 1], SERVICES[(i + 1) % len(SERVICES)]
    others = "".join(f'<li><a href="/advisory/{o["slug"]}/">{e(o["title"])}</a></li>' for o in SERVICES if o is not s)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <p class="crumb"><a href="/advisory/">Advisory</a> &nbsp;/&nbsp; {s['num']}</p>
    <h1>{e(s['title'])}</h1>
    <p class="lede">{e(s['positioning'])}</p>
    <div class="actions"><a class="btn" href="/enquire/?area={s['slug']}">Request a consultation {arrow()}</a></div>
  </div>
</section>

<div class="wrap"><figure class="svc-figure">{pic(s['image'], IMAGES[s['image']]['caption'], "(min-width: 1240px) 1128px, 100vw", lazy=False)}<figcaption>{credit(s['image'])}</figcaption></figure></div>

<section class="section">
  <div class="wrap svc-body">
    <div>
      <div class="block reveal"><span class="label">The strategic challenge</span><h2>{e(s['challenge_head'])}</h2>{chall}</div>
      <div class="block reveal"><span class="label">The questions it addresses</span><ul class="questions" style="margin-top:18px">{qs}</ul></div>
      <div class="block reveal"><span class="label">My advisory contribution</span><h2>How I work on it.</h2>{contrib}</div>
      <div class="block reveal"><span class="label">Areas of advisory</span><ul class="areas-list" style="margin-top:18px">{areas}</ul></div>
    </div>
    <aside class="svc-aside">
      <div class="aside-box"><h2>Relevant to</h2><ul>{rel}</ul></div>
      <div class="aside-box"><h2>Led personally</h2><p style="font-size:17.5px">Every engagement is led by {NAME}. Scope is agreed around your circumstances and may draw on more than one discipline.</p><p style="margin-top:14px"><a class="link" href="/advisory/#approach">How I work {arrow()}</a></p></div>
    </aside>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap reveal"><span class="label">The value of the engagement</span><p class="value">{e(s['value'])}</p></div>
</section>

{invite(text="An initial conversation to explore your objectives, understand the nature of the challenge and establish whether there is a basis for working together.", area=s['slug'], navy=True)}

<section class="section">
  <div class="wrap">
    <nav class="pager" aria-label="Other disciplines">
      <a href="/advisory/{prev_s['slug']}/"><span class="label">&larr; Previous discipline</span><span class="t">{e(prev_s['title'])}</span></a>
      <a href="/advisory/{next_s['slug']}/"><span class="label">Next discipline &rarr;</span><span class="t">{e(next_s['title'])}</span></a>
    </nav>
  </div>
</section>"""
    path = f"/advisory/{s['slug']}/"
    svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "description": s["positioning"],
                  "serviceType": s["title"], "url": SITE + path, "provider": {"@type": "ProfessionalService", "name": NAME, "url": SITE + "/"},
                  "areaServed": ["Africa", "Europe", "Middle East", "North America"]}
    write(path, page(path, f"{s['title']} | {NAME}", s["meta"], body, section="/advisory/",
                     schema=[svc_schema, crumbs(("Home", "/"), ("Advisory", "/advisory/"), (s["title"], path))]))


# ---------------------------------------------------------------- about
def about():
    body = f"""<section class="page-hero">
  <div class="wrap about-hero">
    <div>
      <span class="label">About</span>
      <h1>{NAME}</h1>
      <p class="lede" style="font-family:var(--sans);font-size:16px;color:var(--gold-text);margin-top:14px">{TITLE_H}</p>
      <p class="lede">I am an independent advisor working where luxury, strategy and African enterprise meet. Based in London, I work directly with founders, executives and institutions on how brands, businesses and places are positioned, valued and developed in international markets.</p>
      <div class="actions"><a class="btn" href="/enquire/">Request a consultation {arrow()}</a><a class="link" href="/advisory/">The advisory {arrow()}</a></div>
    </div>
    <figure>{portrait("3x4", "(min-width: 900px) 40vw, 90vw", lazy=False)}</figure>
  </div>
</section>

<section class="section" style="border-top:1px solid var(--line)">
  <div class="wrap split">
    <div><span class="label">Perspective</span><h2>What I believe, and why it shapes the work.</h2></div>
    <div class="essay measure">
      <h2>Luxury as commercial architecture</h2>
      <p>My interest in luxury has never been confined to its surface. What draws me is its architecture: how perception, scarcity, craft, price and access are arranged so that something is understood as exceptional and valued accordingly. To a client, luxury is ease, the feeling that every detail has been considered. Behind that ease sits a series of deliberate commercial decisions. That is where my work begins.</p>
      <h2>Origin and value</h2>
      <p>I am particularly concerned with the relationship between origin and value. African raw materials, techniques and cultural ideas underpin some of the world's most valued goods and experiences, yet much of that value is realised elsewhere. Provenance is now a popular word, but few businesses know how to express it, and fewer still how to own it. It has to be defined first, then shown consistently and protected.</p>
      <h2>African enterprise, in its own right</h2>
      <p>I believe African businesses, destinations and institutions can build distinctive positions in international markets on their own terms, rather than following someone else's rule book. A brand and its region can become known for something specific, the way some destinations are known around the world for a single experience. They can go further than they expect.</p>
      <h2>Beyond conventional metrics</h2>
      <p>Markets are not fully described by their size. I look at the competitive landscape, the behaviour of buyers, the commercial and institutional conditions, and above all at what is beginning to change. The aim is to help clients understand where markets are, anticipate where they are going and position themselves for what comes next.</p>
      <h2>An independent practice</h2>
      <p>My practice is deliberately personal. Clients work with me directly, from the first conversation onwards. I take on a limited number of engagements at a time so that each receives senior attention. Every client is treated as a luxury client, and receives the same care I help them give their own customers.</p>
    </div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap split">
    <div><span class="label">Background</span><h2>Training and experience.</h2></div>
    <div class="measure">
      <p>I studied Luxury Brand Management at Regent's University London, and my professional background is in luxury brand management. My approach to clients has been shaped by years of looking after premium clients in London: understanding what they choose, what they return for and what they recommend. My background spans the United Kingdom and Southern Africa.</p>
      <dl class="facts">
        <div><dt>Education</dt><dd>Luxury Brand Management, Regent's University London</dd></div>
        <div><dt>Base</dt><dd>London, working internationally</dd></div>
        <div><dt>Focus</dt><dd>Luxury brand strategy, provenance and international markets, with particular depth in Africa</dd></div>
        <div><dt>Practice</dt><dd>Independent. Every engagement is led personally.</dd></div>
      </dl>
      <div class="actions"><a class="link" href="/perspectives/">Perspectives and selected work {arrow()}</a></div>
    </div>
  </div>
</section>

{invite(navy=True)}"""
    desc = f"{NAME} is an independent advisor in luxury brand strategy, international markets and provenance, based in London and working directly with founders, executives and institutions."
    write("/about/", page("/about/", f"About {NAME} | {TITLE}", desc, body, section="/about/",
                          schema=[{"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": PERSON}, crumbs(("Home", "/"), ("About", "/about/"))]))


# ---------------------------------------------------------------- perspectives
def perspectives():
    teasers = "".join(f'''<a class="teaser reveal" href="/perspectives/{a["slug"]}/"><div class="img">{pic(a["image"], "", "(min-width: 900px) 30vw, 100vw")}</div><span class="label">{e(a["kind"])}</span><h3>{e(a["title"])}</h3><p>{e(a["standfirst"])}</p></a>''' for a in ARTICLES)
    work = "".join(f'''<article class="work-item reveal"><div><span class="tag">{e(w["status"])}</span><h3 style="margin-top:14px">{e(w["title"])}</h3></div><div><p>{e(w["summary"])}</p><p class="muted" style="margin-top:12px;font-size:17px">{e(w["shows"])}</p></div></article>''' for w in WORK)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="label">Perspectives</span>
    <h1>Independent thinking on markets, origin and value.</h1>
    <p class="lede">Short essays on the questions I find most consequential for luxury, African enterprise and international markets, followed by a selection of professional experience and independent research. Each piece is labelled for exactly what it is.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap"><div class="teasers" style="margin-top:0">{teasers}</div></div>
</section>
<section class="section on-paper" id="work">
  <div class="wrap">
    <div class="section-head reveal"><span class="label">Selected work</span><h2>Professional experience and independent research.</h2><p class="muted">Client confidentiality applies to commissioned work. What follows is described accurately: professional experience, research in progress and independent study are marked as such.</p></div>
    <div class="work-list">{work}</div>
  </div>
</section>
{invite()}"""
    desc = "Strategic perspectives on provenance, destination positioning and strategic foresight, with selected professional experience and independent research."
    write("/perspectives/", page("/perspectives/", f"Perspectives | {NAME}", desc, body, section="/perspectives/",
                                 schema=[crumbs(("Home", "/"), ("Perspectives", "/perspectives/"))]))
    for a in ARTICLES:
        paras = ""
        for block in a["body"]:
            paras += f"<h2>{e(block[1:])}</h2>" if block.startswith("#") else f"<p>{e(block)}</p>"
        others = [o for o in ARTICLES if o is not a]
        more = "".join(f'''<a class="teaser" href="/perspectives/{o["slug"]}/"><div class="img">{pic(o["image"], "", "(min-width: 900px) 45vw, 100vw")}</div><span class="label">{e(o["kind"])}</span><h3>{e(o["title"])}</h3></a>''' for o in others)
        path = f"/perspectives/{a['slug']}/"
        body = f"""<article>
  <header class="wrap article-head">
    <p class="crumb"><a href="/perspectives/">Perspectives</a> &nbsp;/&nbsp; {e(a['kind'])}</p>
    <h1>{e(a['title'])}</h1>
    <p class="standfirst">{e(a['standfirst'])}</p>
    <p class="meta">By {NAME} &middot; {a['date_label']} &middot; {a['minutes']} minute read</p>
  </header>
  <div class="wrap"><figure class="article-figure">{pic(a['image'], IMAGES[a['image']]['caption'], "(min-width: 1240px) 1128px, 100vw", lazy=False)}<figcaption>{credit(a['image'])}</figcaption></figure></div>
  <div class="wrap"><div class="prose">{paras}<p class="note">This is an independent perspective by {NAME}. It does not describe or draw on any client engagement.</p></div></div>
</article>
<section class="section">
  <div class="wrap"><div class="section-head"><span class="label">Further perspectives</span></div><div class="teasers" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">{more}</div></div>
</section>
{invite()}"""
        art = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["standfirst"],
               "datePublished": a["date"], "author": {"@type": "Person", "name": NAME, "url": SITE + "/about/"},
               "image": f"{SITE}/img/{a['image']}-1600.jpg", "mainEntityOfPage": SITE + path, "inLanguage": "en-GB"}
        write(path, page(path, f"{a['title']} | {NAME}", a["standfirst"], body, section="/perspectives/", og_type="article",
                         schema=[art, crumbs(("Home", "/"), ("Perspectives", "/perspectives/"), (a["title"], path))]))


# ---------------------------------------------------------------- enquire
def enquire():
    opts = '<option value="">Select an area, if known</option>' + "".join(f'<option value="{s["slug"]}">{e(s["title"])}</option>' for s in SERVICES) + '<option value="several">More than one, or not yet defined</option>'
    body = f"""<section class="page-hero">
  <div class="wrap enquire">
    <div>
      <span class="label">Private enquiry</span>
      <h1 style="font-size:clamp(36px,4.6vw,58px)">Request a private consultation.</h1>
      <p class="lede">An initial conversation to explore your objectives, understand the nature of the strategic challenge and establish whether there is a basis for working together.</p>
      <ul class="expect">
        <li>A conversation with me directly, not an assistant or a sales team</li>
        <li>By video call, or in person in London</li>
        <li>No charge and no obligation</li>
        <li>Everything you share is held in confidence</li>
      </ul>
      <div class="principal" style="margin-top:36px">{portrait("1x1", "88px")}<div><p><strong>{NAME}</strong></p><p class="role">{TITLE_H}</p></div></div>
    </div>
    <div>
      <form id="enquiry" class="form" name="enquiry" method="POST" action="/enquire/thank-you/" data-netlify="true" netlify-honeypot="website" novalidate>
        <input type="hidden" name="form-name" value="enquiry">
        <p class="hp" aria-hidden="true"><label>Leave this field empty <input name="website" tabindex="-1" autocomplete="off"></label></p>
        <div class="row2">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><p class="err" id="e-name" aria-live="polite"></p></div>
          <div class="field"><label for="f-role">Role <span class="opt">(optional)</span></label><input id="f-role" name="role" autocomplete="organization-title"></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-org">Organisation</label><input id="f-org" name="organisation" autocomplete="organization" required aria-describedby="e-organisation"><p class="err" id="e-organisation" aria-live="polite"></p></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email"><p class="err" id="e-email" aria-live="polite"></p></div>
        </div>
        <div class="field"><label for="f-area">Area of advisory <span class="opt">(optional)</span></label><select id="f-area" name="area">{opts}</select></div>
        <div class="field"><label for="f-markets">Markets or regions of interest <span class="opt">(optional)</span></label><input id="f-markets" name="markets"></div>
        <div class="field"><label for="f-message">The nature of your enquiry</label><textarea id="f-message" name="message" required aria-describedby="e-message"></textarea><p class="err" id="e-message" aria-live="polite"></p></div>
        <p class="form-note">Your details are used only to respond to your enquiry. See the <a href="/privacy/">privacy notice</a>.</p>
        <div><button class="btn" type="submit">Request a consultation</button><p class="err" id="e-submit" aria-live="polite"></p></div>
        <p class="form-note">Or write to <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </form>
      <div class="sent" id="sent" tabindex="-1" role="status"><h2>Thank you.</h2><p>Your enquiry has reached me. I read every enquiry personally and will reply to arrange a time to speak.</p></div>
    </div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap measure" style="max-width:860px">
    <span class="label">Before we speak</span>
    <div class="faq">
      <details><summary>What happens after I send an enquiry?</summary><p>I read every enquiry personally and reply to arrange an initial conversation, by video call or in person in London.</p></details>
      <details><summary>Is there a charge for the initial conversation?</summary><p>No. It is an opportunity to understand your objectives and decide together whether there is a basis for working together.</p></details>
      <details><summary>How are engagements structured?</summary><p>Scope, timing and fees are agreed in a written proposal once I understand the question you are trying to answer. An engagement may focus on a single discipline or draw on several.</p></details>
      <details><summary>Do you work with public institutions?</summary><p>Yes. The practice is open to government bodies, tourism and destination authorities and sector organisations, as well as private businesses and investors.</p></details>
      <details><summary>Will what I share be kept confidential?</summary><p>Yes. Everything you share about your organisation, plans and markets is held in confidence.</p></details>
    </div>
  </div>
</section>"""
    write("/enquire/", page("/enquire/", f"Request a Private Consultation | {NAME}",
                            f"Request a private consultation with {NAME}: an initial conversation to explore your objectives and whether there is a basis for working together.",
                            body, section="/enquire/", schema=[crumbs(("Home", "/"), ("Enquire", "/enquire/"))]))
    write("/enquire/thank-you/", page("/enquire/thank-you/", f"Thank you | {NAME}", "Your enquiry has been received.",
                                      f'<section class="plain-page"><div class="wrap measure"><span class="label">Private enquiry</span><h1 style="margin-top:14px">Thank you.</h1><div class="prose"><p>Your enquiry has reached me. I read every enquiry personally and will reply to arrange a time to speak.</p><p><a class="link" href="/">Return to the home page</a></p></div></div></section>',
                                      noindex=True))


# ---------------------------------------------------------------- small pages
def small_pages():
    def credit_line(i):
        if i["licence"]:
            return f'{e(i["caption"])}. Photograph by {e(i["artist"])}, <a href="{i["licence_url"]}">{e(i["licence"])}</a>, via <a href="{i["source"]}">Wikimedia Commons</a>. Shown in black and white and cropped.'
        return f'{e(i["caption"])}.' + (f' Image: {e(i["via"])}.' if i["via"] else "") + ' Shown in black and white and cropped.'
    used = {s["image"] for s in SERVICES} | {a["image"] for a in ARTICLES}
    credits = "".join(f'<li>{credit_line(IMAGES[k])}</li>' for k in IMAGES if k in used)
    write("/credits/", page("/credits/", f"Photography credits | {NAME}", "Credits for photography used on this website.",
                            f'<section class="plain-page"><div class="wrap measure"><h1>Photography credits</h1><div class="prose"><p>Portraits of {NAME} are used with permission. Other photographs are credited below.</p></div><ul class="credits" style="margin-top:28px">{credits}</ul></div></section>', noindex=False))
    write("/privacy/", page("/privacy/", f"Privacy notice | {NAME}", "How personal information submitted through this website is used.",
                            f"""<section class="plain-page"><div class="wrap measure"><h1>Privacy notice</h1><div class="prose">
<p>This notice explains how {NAME} uses the personal information you share through this website.</p>
<h2>What is collected</h2><p>When you send an enquiry, the details you enter are collected: your name, role, organisation, email address, area of interest, markets of interest and message. The website does not use advertising or tracking cookies.</p>
<h2>How it is used</h2><p>Your details are used only to respond to your enquiry and, if we go on to work together, to correspond with you about that work. They are not added to marketing lists and are never sold or shared for marketing.</p>
<h2>Where it is stored</h2><p>Enquiries are received through the website's hosting provider, Netlify, and by email. Information is kept only for as long as it is needed for these purposes.</p>
<h2>Your rights</h2><p>You may ask to see, correct or delete the information held about you at any time by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div></section>"""))
    write("/404", page("/404", f"Page not found | {NAME}", "This page could not be found.",
                       f'<section class="plain-page"><div class="wrap measure"><span class="label">Page not found</span><h1 style="margin-top:14px">This page could not be found.</h1><div class="prose"><p>It may have moved when the site was reorganised. The <a href="/advisory/">advisory</a> and <a href="/perspectives/">perspectives</a> pages are good places to begin, or you can <a href="/enquire/">get in touch</a>.</p></div></div></section>', noindex=True))
    urls = ["/", "/advisory/"] + [f"/advisory/{s['slug']}/" for s in SERVICES] + ["/about/", "/perspectives/"] + [f"/perspectives/{a['slug']}/" for a in ARTICLES] + ["/enquire/", "/privacy/", "/credits/"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0F1B2D"/><text x="32" y="44" font-family="Georgia, \'Times New Roman\', serif" font-size="36" fill="#F6F1E7" text-anchor="middle">Z</text><rect x="20" y="51" width="24" height="1.5" fill="#CDB27C"/></svg>\n')


if __name__ == "__main__":
    home(); advisory()
    for i, s in enumerate(SERVICES):
        service(i, s)
    about(); perspectives(); enquire(); small_pages()
