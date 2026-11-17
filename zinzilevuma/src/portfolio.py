"""Advisory portfolio: the portfolio index and each case, told as a journey."""
import html

e = html.escape

CASE_01 = dict(
    slug="carrying-a-heritage-forward",
    num="01",
    status="Academic placement",
    title="Carrying a heritage forward, online.",
    short_title="Carrying a heritage forward, online",
    teaser="A curated platform for independent British designers had built its following in pop-up rooms. The question was how to carry that heritage online without losing the craft and storytelling that set it apart.",
    meta="Case study: digital discovery and editorial strategy for a curated platform of independent British designers, moving from pop-up retail to online discovery.",
    glance=[("Client", "Curated British designer platform"), ("Sector", "Contemporary womenswear & jewellery"),
            ("My role", "Brand & digital discovery strategy"), ("Focus", "Editorial, search visibility, trend mapping")],
)

CHAPTERS = [("ch-1", "Where it began"), ("ch-2", "The crossroads"), ("ch-3", "Finding the way"),
            ("ch-4", "The customer's path"), ("ch-5", "The tension"), ("ch-6", "What changed"), ("ch-7", "The road ahead")]
WORDS = ["one", "two", "three", "four", "five", "six", "seven"]


def chapter_head(i, heading):
    cid, name = CHAPTERS[i]
    return (f'<div class="ch-head reveal"><span class="ch-num" aria-hidden="true">{i + 1}</span>'
            f'<span class="label">Chapter {WORDS[i]} &middot; {e(name)}</span><h2>{heading}</h2></div>')


def case_01_body(arrow, invite):
    c = CASE_01
    glance = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c["glance"])
    chapters = "".join(f'<li><a href="#{cid}"><span>{i + 1}</span>{e(n)}</a></li>' for i, (cid, n) in enumerate(CHAPTERS))
    return f"""<div class="case-progress" aria-hidden="true"><span></span></div>
<article class="case">
<header class="page-hero case-hero">
  <div class="wrap">
    <p class="crumb"><a href="/portfolio/">Portfolio</a> &nbsp;/&nbsp; Case {c['num']}</p>
    <span class="label" style="display:block;margin-top:26px">Advisory portfolio &middot; Case {c['num']} &middot; {e(c['status'])}</span>
    <h1>Carrying a heritage forward, <span class="ink-swap">online</span>.</h1>
    <p class="lede">A curated platform for independent British designers had built its following in pop-up rooms, one conversation at a time. The question was how to carry that heritage online without losing the craft and storytelling that set it apart. This is the journey of how we found the way.</p>
    <dl class="glance reveal">{glance}</dl>
    <nav class="chapters reveal" aria-label="Chapters"><p class="label">The journey</p><ol>{chapters}</ol></nav>
  </div>
</header>

<section class="chapter" id="ch-1">
  <div class="wrap ch-grid">
    {chapter_head(0, "Between editorial and retail.")}
    <div class="ch-body reveal">
      <p class="lede">The client curates collections from a network of independent studios across the British Isles.</p>
      <ul class="chips">
        <li>Sustainability-led production</li><li>Heritage textiles</li><li>Limited runs</li><li>Made to order</li>
      </ul>
      <p>It is not a volume retailer. It sits somewhere between an editorial discovery space and a selective boutique, serving a considered customer who wants to know who made something, and why.</p>
      <p>Until now, that story had mostly been told in person: in the room, with the garment in hand.</p>
    </div>
  </div>
</section>

<section class="chapter on-paper" id="ch-2">
  <div class="wrap ch-grid">
    {chapter_head(1, "From the room to the screen.")}
    <div class="ch-body reveal">
      <p class="lede">The brief: connect an audience spread across the country, and design a marketing structure that could grow with it, while the business moved from physical retail towards online discovery.</p>
    </div>
  </div>
  <div class="wrap">
    <div class="shift reveal" aria-label="The shift the client was making">
      <div class="from"><span class="label">From</span><h3>Physical presence</h3><ul><li>Reliance on pop-ups and in-person retail</li><li>Stories told in the room, not online</li><li>Discovery limited by geography</li></ul></div>
      <div class="via" aria-hidden="true"><span>&rarr;</span></div>
      <div class="to"><span class="label">To</span><h3>Digital discovery</h3><ul><li>An online destination for British design</li><li>Storytelling customers can find and read</li><li>A framework that works for years, not one campaign</li></ul></div>
    </div>
  </div>
</section>

<section class="chapter" id="ch-3">
  <div class="wrap ch-grid">
    {chapter_head(2, "Built around the brand, not a template.")}
    <div class="ch-body reveal">
      <p class="lede">I did not reach for a standard marketing playbook. I started with the client's goals and identity, and shaped every recommendation to fit them.</p>
      <p>The work moved through four stations.</p>
    </div>
  </div>
  <div class="wrap">
    <ol class="stations" style="--p:0">
      <li><span class="dot">1</span><h3>Listen</h3><p>I began with the goals, the leadership culture and the many designer identities living under one roof.</p></li>
      <li><span class="dot">2</span><h3>Map</h3><p>I read seasonal runway and industry trend signals, and matched them to stories the brand was already telling: craft, texture, layering and material heritage.</p></li>
      <li><span class="dot">3</span><h3>Structure</h3><p>I built a keyword and editorial framework covering blog themes, styling guidance and tone of voice.</p></li>
      <li><span class="dot">4</span><h3>Hand over</h3><p>I left a repeatable system the team can keep using, so nobody starts from a blank page each season.</p></li>
    </ol>
  </div>
</section>

<section class="chapter on-paper" id="ch-4">
  <div class="wrap ch-grid">
    {chapter_head(3, "From inspiration to purchase.")}
    <div class="ch-body reveal"><p class="lede">The framework gives a customer a clear path through the site, without turning a discovery platform into a hard-sell shop.</p></div>
  </div>
  <div class="wrap">
    <ol class="path">
      <li class="reveal"><span class="label">Search</span><h3>Found through considered keywords</h3></li>
      <li class="reveal"><span class="label">Read</span><h3>Editorial and designer stories</h3></li>
      <li class="reveal"><span class="label">Style</span><h3>Guidance on how to wear it</h3></li>
      <li class="reveal"><span class="label">Buy</span><h3>A considered purchase</h3></li>
    </ol>
  </div>
</section>

<section class="chapter" id="ch-5">
  <div class="wrap ch-grid">
    {chapter_head(4, "Visibility without dilution.")}
    <div class="ch-body reveal">
      <p class="lede">Here was the real tension. Search visibility mattered a great deal, but chasing it too hard would flatten a sustainability-led, story-first brand. The strategy had to hold both.</p>
      <div class="balance">
        <label for="balance" class="label">Drag to feel the trade-off</label>
        <div class="balance-ends" aria-hidden="true"><span>Search visibility</span><span>Brand identity</span></div>
        <input id="balance" type="range" min="0" max="100" value="50" aria-describedby="balance-out" aria-valuetext="Held at the centre">
        <p class="balance-out" id="balance-out" aria-live="polite">Held at the centre: keywords that serve the storytelling, not replace it.</p>
      </div>
    </div>
  </div>
</section>

<section class="chapter on-paper" id="ch-6">
  <div class="wrap ch-grid">
    {chapter_head(5, "Value created.")}
    <div class="ch-body reveal"><p class="lede">By the end of the journey, the work had strengthened the client on four fronts.</p></div>
  </div>
  <div class="wrap">
    <div class="fronts">
      <div class="reveal"><span class="label">Strategic</span><h3>A real move online</h3><p>Supported the shift away from reliance on pop-ups towards a stronger digital discovery platform.</p></div>
      <div class="reveal"><span class="label">Brand</span><h3>Positioning reinforced</h3><p>Strengthened the client's place as a curated destination for contemporary British design.</p></div>
      <div class="reveal"><span class="label">Digital</span><h3>Clearer navigation</h3><p>The keyword and editorial structure created clear routes across styling guidance and blog pages.</p></div>
      <div class="reveal"><span class="label">Commercial</span><h3>Browsing to buying</h3><p>Moved visitors from inspiration-led browsing to structured engagement, with the identity intact.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <figure class="case-quote reveal">
      <blockquote>A multi-brand platform carries many identities at once. The work was to carry all of them forward, together.</blockquote>
      <figcaption>Zinzile Vuma</figcaption>
    </figure>
  </div>
</section>

<section class="chapter" id="ch-7">
  <div class="wrap ch-grid">
    {chapter_head(6, "Where I would take it next.")}
    <ol class="ahead reveal">
      <li><span>i</span>Competitor keyword benchmarking, to see where the client can own search ground.</li>
      <li><span>ii</span>Clear performance measures showing how editorial content turns into engagement and sales over time.</li>
      <li><span>iii</span>A plan to reassure partner designers that moving online adds to their presence rather than taking from it.</li>
    </ol>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="case-note reveal">
      <span class="tag">Academic placement &middot; Assessed at 80%, publishable standard</span>
      <p>Undertaken during a placement as part of my BA (Hons) Luxury Brand Management at Regent's University London. The client's name and proprietary materials are withheld to protect confidentiality.</p>
    </div>
  </div>
</section>
</article>

{invite(title="Begin your own journey", text="An initial conversation to explore your objectives, understand the nature of the challenge and establish whether there is a basis for working together.", navy=True)}

<section class="section" style="padding-top:0">
  <div class="wrap"><nav class="pager" aria-label="Portfolio"><a href="/portfolio/"><span class="label">&larr; Back to</span><span class="t">The advisory portfolio</span></a><a href="/advisory/"><span class="label">Explore &rarr;</span><span class="t">The six advisory disciplines</span></a></nav></div>
</section>"""


def journey_motif():
    steps = ["Listen", "Map", "Structure", "Hand over"]
    return '<ol class="motif" aria-hidden="true">' + "".join(f'<li><span></span>{s}</li>' for s in steps) + "</ol>"


def feature_card(arrow, heading_tag="h2"):
    c = CASE_01
    return f"""<a class="case-feature reveal" href="/portfolio/{c['slug']}/">
  <div>
    <span class="label">Case {c['num']} &middot; {e(c['status'])}</span>
    <{heading_tag}>{e(c['title'])}</{heading_tag}>
    <p>{e(c['teaser'])}</p>
    <span class="btn">Follow the journey {arrow()}</span>
  </div>
  {journey_motif()}
</a>"""
