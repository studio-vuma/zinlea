"""Wrap each page's content in the shared header and footer."""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [("index", "Home"), ("services", "Services & Experience"), ("about", "About & Work"), ("book", "Book a Consultation")]
NAV = [p for p in PAGES if p[0] != "index"]

FAVICON = ("data:image/svg+xml," +
  "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230B0B0B'/%3E"
  "%3Crect x='6' y='6' width='52' height='52' fill='none' stroke='%23fff' stroke-width='2'/%3E"
  "%3Ctext x='32' y='42' font-family='Georgia,serif' font-size='26' fill='%23fff' text-anchor='middle'%3EZV%3C/text%3E%3C/svg%3E")

SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Zinzile Vuma Luxury Brand Advisory",
 "description":"Private luxury brand advisory for African luxury brands and platforms expanding into international markets.",
 "areaServed":"Worldwide","email":"mailto:vzinzile@gmail.com",
 "founder":{"@type":"Person","name":"Zinzile Vuma","jobTitle":"Luxury Brand Advisor"},
 "makesOffer":[{"@type":"Offer","price":"0","priceCurrency":"GBP","itemOffered":{"@type":"Service","name":"Complimentary 30-minute consultation"}}]}
</script>"""

CREDITS = ("Photography via Wikimedia Commons: Kente cloth by Warmglow (CC0); Victoria Falls by Diego Delso (CC BY-SA 4.0); "
           "Mosi-oa-Tunya by Matti Blume (CC BY-SA 4.0); basket weaving by Rogerirakoze (CC BY-SA 4.0); "
           "Lower Zambezi by Joachim Huber (CC BY-SA 2.0).")

def page(slug, label, body, title, desc):
    nav = "".join(f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{html.escape(l)}</a></li>' for s, l in NAV if s != "book")
    mnav = "".join(f'<a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{html.escape(l)}</a>' for s, l in PAGES)
    fnav = "".join(f'<a href="{s}.html">{html.escape(l)}</a>' for s, l in PAGES)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Playfair+Display:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{SCHEMA if slug == "index" else ""}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <nav aria-label="Main"><ul class="nav-links">{nav}</ul></nav>
    <a class="brand" href="index.html" aria-label="Zinzile Vuma, home"><span class="mono" aria-hidden="true"><span>Z</span><span>V</span></span><span class="name">ZINZILE VUMA</span></a>
    <a class="head-cta" href="book.html"{' aria-current="page"' if slug == "book" else ""}>Book a consultation</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">{mnav}</nav>
</header>
<main id="main">
{body}
{"" if slug == "book" else BAND}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <a class="brand" href="index.html"><span class="mono" aria-hidden="true"><span>Z</span><span>V</span></span><span class="name" style="margin-top:12px">ZINZILE VUMA · PRIVATE LUXURY BRAND ADVISORY</span></a>
      <nav aria-label="Footer">{fnav}</nav>
    </div>
    <div class="credits">© 2026 Zinzile Vuma · London · <a href="mailto:vzinzile@gmail.com">vzinzile@gmail.com</a><br>{CREDITS}</div>
  </div>
</footer>
<script src="script.js"></script>
</body>
</html>
"""

BAND = """<section class="dark band">
  <div class="wrap">
    <div class="eyebrow reveal">Where we begin</div>
    <h2 class="reveal">Thirty minutes, entirely about your brand.</h2>
    <p class="reveal">A complimentary consultation to understand your brand, your ambitions and what stands in the way.</p>
    <a class="btn reveal" href="book.html">Book your complimentary consultation</a>
  </div>
</section>"""

for slug, label in PAGES:
    src = (ROOT / "src" / f"{slug}.part.html").read_text()
    title = re.search(r"<!--TITLE:(.*?)-->", src).group(1)
    desc = re.search(r"<!--DESC:(.*?)-->", src).group(1)
    body = re.sub(r"<!--(TITLE|DESC):.*?-->\n?", "", src)
    (ROOT / f"{slug}.html").write_text(page(slug, label, body, title, desc))
    print("built", slug + ".html")
