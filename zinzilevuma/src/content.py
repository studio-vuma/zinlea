"""Website copy and data. British English, first person, no em dashes."""

SITE = "https://zinzilevuma.com"
EMAIL = "enquiries@zinzilevuma.com"
NAME = "Zinzile Vuma"
TITLE = "Founder & Principal Luxury Brand Advisor"

CLIENTS = [
    "Founders and owners",
    "CEOs and executive leadership",
    "Investors and commercial stakeholders",
    "Corporations and international brands",
    "African producers and businesses",
    "Governments and public institutions",
    "Tourism and destination authorities",
]

SECTORS = [
    "Luxury and premium goods",
    "Hospitality, tourism and destinations",
    "Origin-led food and drink",
    "Craft, design and the creative industries",
    "Retail and distribution",
    "Public institutions and sector bodies",
]

SERVICES = [
    dict(
        num="I", slug="brand-strategy", short="Brand Strategy & Positioning",
        title="Luxury Brand Strategy & Positioning",
        positioning="Building distinctive brands and strengthening their position in competitive markets.",
        summary="Luxury brand strategy extends well beyond visual identity. It concerns the commercial, cultural and strategic foundations that determine how a brand is understood, valued and positioned.",
        meta="Luxury brand strategy and positioning: differentiation, brand architecture, perceived value, pricing architecture and long-term brand development.",
        challenge_head="Quality is not the same as position.",
        challenge=[
            "In luxury, how a brand is understood determines what it can charge, where it can be sold and who will choose it. Many brands of genuine quality are positioned by default: priced against the wrong competitors, described in borrowed language and judged by standards that were never theirs.",
            "The gap between what a brand is and how it is perceived is rarely a design problem. It is a strategic one, and it compounds over time.",
        ],
        questions=[
            "Why is the brand not valued at the level of its quality?",
            "Are we competing against the right brands, at the right price?",
            "What should we never compromise as we grow?",
        ],
        contribution=[
            "I work with founders and leadership teams on the foundations of the brand: what it stands for, whom it is for, how it differs, and how that difference is expressed in product, price, place and presence.",
            "Visual identity follows from these decisions. It does not substitute for them. Where creative work is needed, I set the strategic direction and work alongside the designers and agencies who carry it out.",
        ],
        areas=[
            "Luxury positioning and differentiation", "Brand identity and strategic architecture",
            "Brand equity and perceived value", "Portfolio and product positioning",
            "Pricing architecture and value creation", "Brand narrative and cultural relevance",
            "Customer perception and competitive distinction", "Long-term brand development",
        ],
        relevant=[
            "Founders and owners of luxury and premium brands",
            "Established houses repositioning or extending a portfolio",
            "International brands refining their position in new markets",
            "Hospitality and destination brands",
        ],
        value="A position the business can defend: clear about what it is, credible at its price, and difficult to imitate.",
        image="bosjes-chapel",
    ),
    dict(
        num="II", slug="market-entry", short="Market Entry & Expansion",
        title="International Market Entry & Expansion",
        positioning="Supporting businesses navigating new markets and identifying opportunities for international growth.",
        summary="Strategic market development: deciding where to go, when and on what terms, and how the business should be positioned when it arrives.",
        meta="International market entry and expansion advisory: market prioritisation, feasibility, buyers, competition, routes to market and partnerships, including across African markets.",
        challenge_head="The order of markets shapes a brand for years.",
        challenge=[
            "Expansion decisions are often made on the strength of an inbound enquiry, a trade mission or one partner's enthusiasm. Yet each market carries its own buyer expectations, competitive structure, regulation and institutional relationships, and the sequence in which markets are entered can define a brand for a long time.",
            "Across Africa, regional integration under the African Continental Free Trade Area, uneven logistics and differing regulatory environments add further layers to the decision. Entering a neighbouring market can be as complex as entering one on another continent.",
        ],
        questions=[
            "Which market should we enter first, and why?",
            "What will buyers there expect of us?",
            "Is this partner right for the long term, or only for the first order?",
        ],
        contribution=[
            "I help leadership teams decide where to go, when, and on what terms. That means building a grounded view of each market's buyers, competitors and commercial and institutional conditions, testing feasibility honestly, and shaping how the business should be positioned and represented when it arrives.",
            "The aim is strategic market development, not simply finding a distributor. Routes to market and partnerships are considered for what they do to the brand and its margins over time, not only for how quickly they open a door.",
        ],
        areas=[
            "Market prioritisation", "Market entry feasibility", "Consumer and buyer understanding",
            "Competitive landscape assessment", "Commercial and institutional conditions",
            "Distribution and route-to-market considerations", "Partnership and market access opportunities",
            "International positioning", "Strategic growth considerations",
        ],
        relevant=[
            "African businesses entering European, Gulf and North American markets",
            "International brands and investors considering African markets",
            "Businesses expanding across African regional markets",
            "Leadership teams reviewing an existing international footprint",
        ],
        value="A sequenced, evidence-led route into new markets, with the brand's position protected rather than diluted along the way.",
        image="cape-town-edition",
    ),
    dict(
        num="III", slug="provenance", short="Provenance & Value Creation",
        title="Provenance, Heritage & Value Creation",
        positioning="Transforming origin, heritage and production excellence into recognised commercial value.",
        summary="Provenance is not only a story. It is a question of definition, ownership, recognition and who captures the value that origin creates.",
        meta="Provenance and origin-led value creation: country-of-origin positioning, heritage capital, value-chain positioning, intellectual property considerations and value capture.",
        challenge_head="Origin creates value. Others often keep it.",
        challenge=[
            "Origin is among the most valuable assets an African business can hold, and among the least protected. Raw materials, techniques and cultural references frequently leave their place of origin and acquire their value elsewhere, under someone else's name.",
            "Provenance is often treated as a marketing story. In practice it concerns definition, ownership, recognition and the distribution of value along the chain from producer to buyer.",
        ],
        questions=[
            "Why does our origin add so little to our price?",
            "Who benefits from the reputation of where we come from?",
            "How do we protect what makes us distinct?",
        ],
        contribution=[
            "I advise on how origin, heritage and production capability can become a durable source of competitive advantage. That begins with defining what a place, a technique or a community genuinely contributes, and what evidence supports the claim.",
            "From there, I consider how the claim is expressed consistently, how it is protected, how it is recognised in international markets and how value is shared with the producers and communities on whom it depends. Where legal protection is relevant, I work alongside specialist advisers.",
        ],
        areas=[
            "Country-of-origin positioning", "Provenance and authenticity", "Cultural and heritage capital",
            "Origin-led brand differentiation", "Producer and value-chain positioning",
            "Intellectual property considerations", "Artisan and production ecosystems",
            "Commercial value capture", "International recognition and market perception",
        ],
        relevant=[
            "Producers of origin-defined goods such as coffee, tea, cacao, wine and spirits",
            "Craft, textile, leather and jewellery businesses",
            "Cooperatives, producer associations and sector bodies",
            "Public institutions developing national or regional origin strategies",
        ],
        value="Origin that is defined, defended and recognised, so that more of the value it creates is retained where it begins.",
        image="diamond-polishing",
    ),
    dict(
        num="IV", slug="commercial-development", short="Commercial Development & Market Access",
        title="Commercial Development & Market Access",
        positioning="Identifying and strengthening the commercial pathways through which businesses access markets and create value.",
        summary="Commercial substance rather than networking: which channels and partners suit the business, on what terms, and with how much of the value retained.",
        meta="Commercial development and market access advisory: opportunity assessment, channel strategy, retail and hospitality readiness, buyer engagement, partnerships and value capture.",
        challenge_head="Access is earned, and it has a price.",
        challenge=[
            "A strong product and a clear position do not guarantee access. Luxury retail, hospitality and private buyers operate through relationships, standards and expectations that are rarely written down.",
            "Many businesses reach these channels before they are ready, or through intermediaries who capture much of the margin. Others never reach them at all.",
        ],
        questions=[
            "Are we ready for this buyer, and what would they expect?",
            "Which channel suits the brand we want to become?",
            "How much of our margin are we giving away, and to whom?",
        ],
        contribution=[
            "I work with businesses to assess where the real commercial opportunities lie, which channels and partners suit the brand, and what readiness those channels require.",
            "The focus is on commercial substance: the terms on which a business enters a channel, the value it retains, and the relationships that will sustain its growth.",
        ],
        areas=[
            "Commercial opportunity assessment", "Channel and distribution strategy",
            "Retail and hospitality market readiness", "Strategic buyer engagement",
            "Partnership development", "Commercial positioning", "Market access considerations",
            "Growth opportunities", "Revenue and value-capture considerations",
        ],
        relevant=[
            "Brands preparing for luxury retail or hospitality channels",
            "Producers seeking direct relationships with international buyers",
            "Platforms and marketplaces representing African brands",
            "Businesses reviewing distribution and partner arrangements",
        ],
        value="Routes to market chosen deliberately, entered when the business is ready, and structured to retain value.",
        image="riad",
    ),
    dict(
        num="V", slug="institutions-destinations", short="Institutional & Destination Advisory",
        title="Institutional & Destination Advisory",
        positioning="Strengthening the strategic positioning of destinations, institutions and sector ecosystems.",
        summary="Countries, regions and sectors compete for attention, investment and visitors much as brands do. The challenge is as much alignment and architecture as it is message.",
        meta="Institutional and destination advisory: destination positioning, luxury and high-value tourism, institutional brand architecture, investment propositions and international competitiveness.",
        challenge_head="Extraordinary assets, without a clear claim.",
        challenge=[
            "Many destinations and sectors have extraordinary assets but no clear claim. A place becomes known for something specific only when that claim is defined, agreed across many stakeholders and expressed consistently over time.",
            "For institutions, the difficulty is as much about alignment and architecture as it is about message: who decides, how the decision is held, and how many organisations present one coherent proposition.",
        ],
        questions=[
            "What should this destination or sector be known for?",
            "How do we attract the right kind of investment and visitor?",
            "How can many institutions present one coherent proposition?",
        ],
        contribution=[
            "I advise public institutions, tourism and destination bodies and sector organisations on how their assets are positioned internationally: what the destination or sector should be known for, how luxury and high-value tourism can be developed responsibly, and how investment propositions are framed.",
            "I also consider how institutional brands are structured, so that many stakeholders can speak with one voice without losing what makes each of them distinct.",
        ],
        areas=[
            "Destination positioning", "Luxury and high-value tourism development", "Sector development opportunities",
            "Institutional brand architecture", "Investment proposition development",
            "Stakeholder and partnership considerations", "International competitiveness",
            "Strategic positioning of national and regional assets",
        ],
        relevant=[
            "Government ministries and public agencies",
            "Tourism and destination authorities",
            "Investment promotion bodies",
            "Sector associations and development organisations",
            "Hospitality groups working with public partners",
        ],
        value="A distinctive, coordinated international position that stakeholders can align behind and that investors and visitors recognise.",
        image="kigali-convention",
    ),
    dict(
        num="VI", slug="research-intelligence", short="Strategic Research & Intelligence",
        title="Strategic Research & Market Intelligence",
        positioning="Understanding what exists. Anticipating what comes next.",
        summary="Research, commercial interpretation and forward-looking judgement, developed with decision-makers to inform where to compete, how to develop and where to invest.",
        meta="Strategic research and market intelligence: sector assessments, competitive intelligence, buyer behaviour, strategic foresight, scenario development and opportunity assessment.",
        challenge_head="Market size is not a strategy.",
        challenge=[
            "Informed decisions require more than an understanding of market size. They require a considered view of the competitive landscape, consumer behaviour, commercial conditions and the institutional environment.",
            "Most analysis describes the market as it stands. By the time a pattern is clear enough to appear in a market report, the most valuable position has often been taken.",
        ],
        questions=[
            "What is changing in this market that others have not yet recognised?",
            "Where could future value emerge, and under what conditions?",
            "Which decision today creates an advantage tomorrow?",
        ],
        contribution=[
            "I work collaboratively with founders, executives and decision-makers to develop the research and intelligence needed to inform market prioritisation, commercial development and investment decisions.",
            "My approach extends beyond established market patterns. By examining emerging behaviours, shifting market dynamics and underexplored opportunities, I help identify where industries may be heading, what businesses could do differently and where future competitive advantage may emerge.",
            "This is not prediction. It is disciplined foresight: developing plausible scenarios, testing assumptions against them and preparing the business to act before a market becomes crowded.",
        ],
        areas=[
            "Market and sector assessments", "Competitive intelligence", "Consumer and buyer behaviour",
            "Emerging market dynamics", "Strategic foresight", "Scenario development", "Commercial feasibility",
            "Investment and opportunity assessments", "Market whitespace identification", "Future positioning",
        ],
        relevant=[
            "Founders and executives facing a significant market decision",
            "Investors assessing opportunities in luxury, hospitality and origin-led sectors",
            "International organisations considering African markets",
            "Institutions developing sector strategies",
        ],
        value="The objective is not simply to understand the market as it stands, but to anticipate what it could become and to position the business accordingly.",
        image="nairobi",
    ),
]

ARTICLES = [
    dict(
        slug="provenance-is-an-asset", kind="Perspective · Provenance", date="2026-11-17", date_label="November 2026", minutes=4,
        title="Provenance is not a story. It is an asset.",
        standfirst="Origin is one of the most valuable things an African business owns. Too often, it is also the first thing it gives away.",
        image="basket-weaving",
        body=[
            "Provenance has become one of the most used words in African luxury. It appears on labels, in investor presentations and in tourism campaigns. Yet in many cases it is doing very little commercial work. The word is present; the value is not.",
            "#Where the value goes",
            "Many goods leave the continent as raw material or unbranded product and acquire their premium elsewhere. Beans become chocolate in another country. Leaf becomes a blend under another name. Techniques and motifs reappear in collections designed far from the communities that developed them. In each case origin contributes to the value of the final product, but the reputation and the margin are captured by whoever names it, finishes it and sells it.",
            "This is not only a question of manufacturing. It is a question of who defines the origin, who is recognised for it, and who has the standing to charge for it.",
            "#Define before you display",
            "The instinct is to tell the story. The more useful discipline is to define it first. What does this place, this technique or this community contribute that cannot be found elsewhere? What evidence supports the claim? What must remain true for it to stay credible? Only once those questions are answered can provenance be expressed consistently in how a business looks, speaks, presents itself and prices what it makes.",
            "#From story to structure",
            "Treated seriously, provenance becomes a strategic architecture rather than a narrative. It informs which products carry the origin and which do not, how scarcity is managed, which partners may use the name, and what protection is sought, whether through trademarks, collective marks or geographical indications where they are available.",
            "It also informs how value is shared with the producers and communities on whom the claim depends. A provenance claim that does not benefit its source will not stay credible for long.",
            "The businesses and institutions that take this seriously will not simply tell better stories about where they come from. They will own more of what their origin is worth.",
        ],
    ),
    dict(
        slug="known-for-something", kind="Perspective · Positioning", date="2026-11-17", date_label="November 2026", minutes=4,
        title="Known for something.",
        standfirst="The most valuable position a brand, a destination or a sector can hold is a specific one.",
        image="safari-lodge",
        body=[
            "Ask an international traveller what South Africa and Kenya are known for and many will mention the game drive. Ask about the Seychelles and they will describe the beaches. These associations are not accidents of geography alone. They are positions, reinforced over years by experience, investment and consistent communication, and they shape demand long before any single business makes its case.",
            "#The cost of being known for everything",
            "Many destinations and brands describe themselves through a long list of attributes: rich culture, beautiful landscapes, warm hospitality, exceptional craft. Each may be true. Together, they are difficult to distinguish from the claims of many competitors. A position that tries to include everything ends up owning very little.",
            "#Choosing the claim",
            "A specific claim requires choices that can feel uncomfortable. It means deciding what to lead with and what to leave in the background, often in the face of stakeholders who each want their own asset represented. For institutions, this is as much a question of governance as of creativity: who decides, and how is the decision held over time?",
            "The strongest claims tend to share three qualities. They are true, resting on something the place or brand genuinely does well. They are distinctive, in that competitors cannot easily make the same promise. And they are extendable, able to grow into products, experiences and investment opportunities without losing their meaning.",
            "#In their own right",
            "There is a temptation to borrow positions that have worked elsewhere: to present an African lodge as an alternative to a European resort, or an African label as a more accessible version of a European house. Comparison of this kind concedes the frame. African brands and destinations can build their own reference points, and in doing so they can go further than they expect.",
        ],
    ),
    dict(
        slug="beyond-the-market-as-it-stands", kind="Perspective · Foresight", date="2026-11-17", date_label="November 2026", minutes=4,
        title="Looking beyond the market as it stands.",
        standfirst="Market data describes where demand has been. Strategy has to consider where it is going.",
        image="durban-port",
        body=[
            "Most market research answers a reasonable question: how large is this market, who competes in it, and how do customers behave today? These answers are necessary. They are rarely sufficient. By the time a pattern is clear enough to appear in a market report, the businesses best placed to benefit from it have often already moved.",
            "#What the numbers leave out",
            "Conventional analysis tends to underweight what is emerging: behaviours visible in small groups before they spread, changes in trade or regulation that alter the economics of a route to market, and shifts in what a new generation of customers regards as valuable.",
            "Across African markets, the developments worth watching include the gradual implementation of the African Continental Free Trade Area, the development of domestic and intra-African demand for high-value goods and experiences, and growing international interest in origin and traceability. None of these can be reduced to a single forecast. Each could reshape a sector.",
            "#Foresight, not prediction",
            "Strategic foresight does not claim to know the future. It asks disciplined questions about it. What is changing? What might plausibly happen next, and under what conditions? Which assumptions in the current plan would fail if it did? Where are the opportunities that competitors have not yet recognised because they are still reading last year's data?",
            "Developing a small number of plausible scenarios, and testing decisions against each, allows a business to act with more confidence rather than less. It reveals the choices that hold up across several possible futures, and the early signals worth watching.",
            "#Positioning before the market is crowded",
            "The practical value of this thinking is timing. A position established before a category becomes crowded is far less costly to hold than one fought for afterwards. Understanding where markets are is the starting point. Anticipating where they are going, and positioning for what comes next, is where advantage is built.",
        ],
    ),
]

WORK = [
    dict(status="Professional experience", title="Retail strategy: from shopfront to online",
         summary="For a London retailer weighing the future of its physical store, I analysed search demand and competitor activity to understand where customers were really looking. The analysis informed the decision to move the business from its physical store to online retail.",
         shows="Where a business chooses to be present is a decision for evidence rather than instinct."),
    dict(status="Professional experience", title="A partnership conversation with Forbes Africa",
         summary="While building the public profile of a new practice focused on African luxury strategy, I wrote long-form editorial and led media and partnership outreach. Forbes Africa requested a partnership call, for which I prepared the partnership deck.",
         shows="A clear point of view, expressed with care, opens doors that promotion alone does not."),
    dict(status="Research in progress", title="Madagascan caviar and luxury hospitality in Marrakech",
         summary="A mixed-methods study, built around structured interviews with hotel food and beverage managers, examining how Madagascan caviar could be distributed through luxury hotels in Marrakech.",
         shows="How an African luxury product might reach international luxury hospitality on its own terms."),
    dict(status="Independent study, not client work", title="The Zambia Luxury Lodge Collection",
         summary="An independent examination of how four distinct Zambian safari lodges, brought under one owner-led brand in 2026, might become one choice in the minds of international travellers, and of the case for conservation as the collection's unifying idea.",
         shows="Becoming known for something specific is a choice that has to show in every detail."),
]

LIC = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
}

def _img(caption, artist, licence, source):
    return dict(caption=caption, artist=artist, licence=licence, licence_url=LIC[licence], source=source, via=None)

def _via(caption, via, source=None):
    """Image supplied by Zinzile, credited to where it was published. Permission to be confirmed."""
    return dict(caption=caption, via=via, source=source, artist=None, licence=None, licence_url=None)

IMAGES = {
    "bosjes-chapel": _via("Bosjes Chapel, Western Cape, South Africa. Architecture by Steyn Studio", "Parametric Architecture"),
    "cape-town-edition": _via("The Cape Town EDITION, V&A Waterfront, Cape Town", "Hotel Designs"),
    "diamond-polishing": _via("Diamond polishing", "Stephen Hughes Fine Diamonds"),
    "basket-weaving": _via("Basket weaving", "54kibo"),
    "safari-lodge": _via("Safari lodge at dusk", None),
    "durban-port": _img("Container terminal, Port of Durban, South Africa", "Media Club", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:Durban_container_port_(24747434937).jpg"),
    "kigali-convention": _img("Kigali Convention Centre, Rwanda", "Schlawgclart", "CC0", "https://commons.wikimedia.org/wiki/File:Kigali_convention_centre.jpg"),
    "nairobi": _img("Nairobi, Kenya", "Lmwangi", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Nairobi_skyline_P1000020.jpg"),
    "riad": _img("Riad courtyard, Marrakech, Morocco", "calflier001", "CC BY-SA 2.0", "https://commons.wikimedia.org/wiki/File:RIAD_LALLA_KHITI_MARRAKECH_MOROCCO_APRIL_2013_(8713893422).jpg"),
}
