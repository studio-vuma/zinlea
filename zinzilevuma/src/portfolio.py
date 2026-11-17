"""Advisory portfolio: the portfolio index and each case study."""
import html

e = html.escape

CASE_01 = dict(
    slug="carrying-a-heritage-forward",
    num="01",
    status="Academic placement",
    title="Carrying a heritage forward, online.",
    short_title="Carrying a heritage forward, online",
    teaser="A curated multi-brand platform for independent British designers had built its following through pop-up spaces. Working directly with the founders, I helped them take that following online without losing the craft and storytelling that set them apart.",
    meta="Case study: SEO and digital discovery for a curated multi-brand platform of independent British designers, moving from pop-up spaces to online discovery.",
    glance=[("Client", "Curated multi-brand platform for independent British designers"),
            ("Sector", "Contemporary womenswear: curated, no-waste, organic British fashion"),
            ("My role", "SEO and digital discovery strategy"), ("Worked with", "Directly with the founders"),
            ("Focus", "Editorial, search visibility and trend mapping")],
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
    <p class="lede">A curated multi-brand platform for independent British designers had built its following through pop-up spaces. Each location drew a different crowd and a different set of supporters. The next part of their story was taking that heritage, and the following the pop-ups had built, online without losing the craft and storytelling that set them apart.</p>
    <dl class="glance reveal">{glance}</dl>
    <nav class="chapters reveal" aria-label="Chapters"><p class="label">In this case study</p><ol>{chapters}</ol></nav>
  </div>
</header>

<section class="chapter" id="ch-1">
  <div class="wrap ch-grid">
    {chapter_head(0, "Between editorial and retail.")}
    <div class="ch-body reveal">
      <p class="lede">The platform brings together independent British designers, with a focus on curated, no-waste, organic fashion, much of it made to order.</p>
      <ul class="chips">
        <li>Curated</li><li>No-waste</li><li>Organic</li><li>Made to order</li>
      </ul>
      <p>Its designers came to the platform because of its pop-ups. Many of them already sold online through their own channels, but the pop-ups gave them a physical space and a following in each location.</p>
      <p>Until then, most of the selling happened in person. Customers could touch the garments and understand how they were made, and that physical experience was what everyone leaned towards, the designers included.</p>
      <p>I worked directly with the founders throughout.</p>
    </div>
  </div>
</section>

<section class="chapter on-paper" id="ch-2">
  <div class="wrap ch-grid">
    {chapter_head(1, "From the room to the screen.")}
    <div class="ch-body reveal">
      <p class="lede">The brief was to move from physical to digital discovery.</p>
      <p>One goal mattered more than most. The designers had joined for the pop-ups, and many were already online on their own. The move had to give them a reason to want to be featured online through the platform too, as something that added to their presence rather than competed with it.</p>
    </div>
  </div>
  <div class="wrap">
    <div class="shift reveal" aria-label="The shift the client was making">
      <div class="from"><span class="label">From</span><h3>Physical presence</h3><ul><li>Pop-ups in different locations, each with its own crowd</li><li>Customers touching the garments to understand them</li><li>Designers drawn in by the physical space</li></ul></div>
      <div class="via" aria-hidden="true"><span>&rarr;</span></div>
      <div class="to"><span class="label">To</span><h3>Digital discovery</h3><ul><li>An online home for curated British fashion</li><li>The craft and the story, explained so customers can find it</li><li>Designers who see being featured online as a plus</li></ul></div>
    </div>
  </div>
</section>

<section class="chapter" id="ch-3">
  <div class="wrap ch-grid">
    {chapter_head(2, "Built around the brand, not a template.")}
    <div class="ch-body reveal">
      <p class="lede">I didn't use a standard marketing playbook. I started with the founders' goals and the brand's identity, and shaped every recommendation around them.</p>
      <p>The work had four stages.</p>
    </div>
  </div>
  <div class="wrap">
    <ol class="stations" style="--p:0">
      <li><span class="dot">1</span><h3>Listen</h3><p>I sat down with the founders to understand their goals, the culture they had built and the many designer identities living under one roof.</p></li>
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
      <p class="lede">Search visibility mattered a great deal, but chasing it too hard would flatten a no-waste, story-led brand. The strategy had to balance both.</p>
      <div class="balance">
        <label for="balance" class="label">Move the slider to see the trade-off</label>
        <div class="balance-ends" aria-hidden="true"><span>Search visibility</span><span>Brand identity</span></div>
        <input id="balance" type="range" min="0" max="100" value="50" aria-describedby="balance-out" aria-valuetext="Balanced">
        <p class="balance-out" id="balance-out" aria-live="polite">Balanced: keywords that support the storytelling rather than replace it.</p>
      </div>
    </div>
  </div>
</section>

<section class="chapter on-paper" id="ch-6">
  <div class="wrap ch-grid">
    {chapter_head(5, "Value created.")}
    <div class="ch-body reveal"><p class="lede">The work strengthened the client in four areas.</p></div>
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

{invite(title="Request a private consultation", text="An initial conversation to explore your objectives, understand the nature of the challenge and establish whether there is a basis for working together.", navy=True)}

<section class="section" style="padding-top:0">
  <div class="wrap"><nav class="pager" aria-label="Portfolio"><a href="/portfolio/"><span class="label">&larr; Back to</span><span class="t">The advisory portfolio</span></a><a href="/advisory/"><span class="label">Explore &rarr;</span><span class="t">The advisory disciplines</span></a></nav></div>
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
    <span class="btn">Read the case study {arrow()}</span>
  </div>
  {journey_motif()}
</a>"""
