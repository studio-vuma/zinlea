# Zinzile Vuma: repositioning, brand elevation and digital experience

Prepared November 2026. This document records the audit, the decisions behind the rebuild, and what still needs your input. The draft copy for every principal page is live on the site itself (source: `src/content.py` and `src/build.py`).

---

## 1. Candid assessment of the previous website

**What worked**
- Black and white photography with colour revealed on hover was a distinctive, ownable detail. It is kept on the perspectives links.
- A genuine, high-quality editorial portrait already existed.
- The booking form worked with Netlify Forms, and pages were fast to load as static HTML.

**What did not**
- **The founder was hidden.** On the homepage the portrait appeared after a moodboard, four pain-point quotes and a section break. On the services page it sat in a mid-page box. For a personal practice, that removed the main reason to choose it.
- **The positioning was narrower than the practice.** "Private Luxury Brand Advisory" for "African luxury brands expanding internationally" excluded institutions, investors, destination authorities and international organisations considering Africa. Strategic research and foresight, which you consider central, appeared as a small add-on called "Market Intelligence".
- **It read as a sales funnel, not senior counsel.** "Complimentary" appeared more than a dozen times. A six-stage journey from "The Consultation" to "Delivery & Launch" implied an agency process and market-entry execution, not strategic advice.
- **The voice was inconsistent.** "African luxury, carried to the world", then "I help brands become known for something specific", then "Looked after from the first conversation to the finish": three propositions, each speaking to a different buyer.
- **Invented client quotes in quotation marks** ("Our product is world-class...") could be read as testimonials. That is a credibility risk with a sophisticated buyer.
- **The imagery relied on shorthand:** Kente cloth, Victoria Falls, a woven basket, elephants and a "Provenance" tile. This is exactly the visual cliché the brief asks to avoid.
- **The visual system signalled "luxury template":** Playfair Display, letter-spaced capitals everywhere, a boxed "ZV" monogram, black and white only. It was handsome, but closer to a fashion label than a private advisory practice.
- **Evidence was thin and uneven.** An SEO blog template sat beside a Forbes Africa partnership conversation, and there was no independent thinking that demonstrated the quality of your judgement.
- **Technical:**
  - The site used a personal Gmail address in the footer and in the form fallback.
  - It ran on the temporary netlify.app address.
  - It had no canonical URLs, sitemap, robots file or social share image, and the favicon was a data URI.
  - Images were uncompressed (200 to 580 KB each, no WebP).
  - Fonts loaded from Google in a way that blocked rendering, and the URLs ended in `.html`.
  - A wall of photo credits sat in the footer, and there was no privacy notice even though the form collects personal data.

## 2. Diagnosis

The practice was being presented as a **service provider to small luxury brands**. The brief describes **an independent strategic advisor** whose distinctive value lies in combining three things:

1. **Luxury expertise:** how perception, scarcity, craft, price and access create value.
2. **Strategic intelligence:** research, interpretation and foresight.
3. **African market knowledge:** the relationship between African enterprise and international markets, in both directions.

None of these alone is distinctive. The combination, delivered personally, is. The previous site expressed only the first, and only for one buyer.

## 3. Brand positioning statement

> Zinzile Vuma is an independent luxury and strategic advisory practice for founders, executives and institutions building value across African and international markets. Working directly with each client, I combine luxury brand strategy, commercial intelligence and strategic foresight to help organisations understand where their markets are, anticipate where they are going, and position themselves for what comes next.

**Proposition line:** *Understanding where markets are. Anticipating where they are going. Positioning businesses for what comes next.*

**Supporting idea:** senior counsel, given personally. You get institutional-quality thinking with direct access to the person doing it.

### Where I have challenged the brief

- **Job title.** "Founder & Principal Luxury Brand Advisor" is implemented as you specified. My recommendation is **"Founder & Principal Advisor"**, keeping luxury in the description rather than the title. "Luxury Brand Advisor" sits awkwardly beside destination advisory for ministries, or market intelligence for investors, and narrows the practice at the point of first contact. It is a one-line change in `src/content.py` (`TITLE`).
- **Breadth versus proof.** Six disciplines, from brand positioning to government advisory, is a broad offer for an independent practice with limited published work. Breadth without evidence reads as overreach to exactly the senior buyers you want. I have handled this by leading with the intellectual proposition, publishing perspectives that demonstrate judgement, and labelling every piece of work precisely. The real fix is time: commissioned work you can describe, and testimonials you can attribute.
- **Gold.** The palette uses antique gold only for hairlines, small labels and markers, never as a fill or headline colour. More would undermine the restraint you asked for.
- **"Critical materials and strategic value chains."** I have not written content on this. It is far from the luxury core and would need a substantiated point of view to be credible. I suggest adding it only once you have one.
- **The client quotes.** These are removed. Each service now lists "the questions it addresses", which keeps the empathy without implying testimonials.

## 4. Sitemap

```
/                               Home
/advisory/                      Advisory overview, how I work, who I advise
/advisory/brand-strategy/       I   Luxury Brand Strategy & Positioning
/advisory/market-entry/         II  International Market Entry & Expansion
/advisory/provenance/           III Provenance, Heritage & Value Creation
/advisory/commercial-development/ IV Commercial Development & Market Access
/advisory/institutions-destinations/ V Institutional & Destination Advisory
/advisory/research-intelligence/ VI Strategic Research & Market Intelligence
/about/                         Founder narrative and background
/perspectives/                  Strategic perspectives and selected work
/perspectives/provenance-is-an-asset/
/perspectives/known-for-something/
/perspectives/beyond-the-market-as-it-stands/
/enquire/                       Request a private consultation (Netlify form "enquiry")
/enquire/thank-you/             Fallback confirmation (no JavaScript)
/privacy/  /credits/  /404
```

Old addresses (`/services`, `/service-*.html`, `/book.html`, `/about.html`) redirect permanently to their new equivalents.

## 5. Homepage structure

1. **Hero:** name and title, the three-line proposition, supporting sentence, "Explore the advisory" and "Meet Zinzile". The portrait is in the hero on desktop, and on mobile it comes first, above the headline.
2. **The practice:** "Senior counsel, given personally", then the three-part proposition (where markets are, where they are going, what comes next).
3. **Areas of advisory:** the six disciplines as an editorial index (numeral, title, positioning line). No cards.
4. **The principal advisor:** a navy section with a substantial portrait, a short introduction and a statement of direct access.
5. **Strategic perspectives:** three essays, with black and white images that reveal colour on hover.
6. **Geographic and sector perspective:** London base and a pan-African and global view, with sectors of focus and who I advise. There is no map graphic.
7. **Private enquiry:** a single, discreet invitation.

## 6. Service architecture

Each discipline page follows the same editorial structure:
1. Title.
2. Positioning statement.
3. The strategic challenge.
4. The questions it addresses.
5. My advisory contribution.
6. Areas of advisory.
7. Relevant to.
8. The value of the engagement.
9. Private enquiry, which opens the form with that discipline preselected.

The overview states plainly that these are **disciplines, not packages**: scope is agreed around the client's circumstances and set out in a written proposal.

The pages describe *what* I advise on and *why it matters*. They do not describe frameworks, tools, research instruments or workflow.

| | Discipline | Positioning |
|---|---|---|
| I | Luxury Brand Strategy & Positioning | Building distinctive brands and strengthening their position in competitive markets. |
| II | International Market Entry & Expansion | Supporting businesses navigating new markets and identifying opportunities for international growth. |
| III | Provenance, Heritage & Value Creation | Transforming origin, heritage and production excellence into recognised commercial value. |
| IV | Commercial Development & Market Access | Identifying and strengthening the commercial pathways through which businesses access markets and create value. |
| V | Institutional & Destination Advisory | Strengthening the strategic positioning of destinations, institutions and sector ecosystems. |
| VI | Strategic Research & Market Intelligence | Understanding what exists. Anticipating what comes next. |

The collaborative model replaces the six-stage journey. It is set out as what you bring, what I bring and what we do together, followed by seven commitments: direct engagement, understanding, collaborative perspectives, independent research, commercial implications, recommendations and ongoing support.

## 7. Draft copy

All copy is live on the site and lives in `src/content.py` (services, perspectives, work) and `src/build.py` (page text). The rules it follows:
- British English and the first person.
- No em dashes, no "bespoke", no "unlock", "transform" or "our team".
- No invented clients, statistics, testimonials or credentials.

**The three perspectives are drafts in your voice.** They are built from beliefs you have stated:
- luxury is ease
- provenance must be defined first
- become known for something specific
- build in your own right
- look beyond the market as it stands

They contain no statistics. Please read and approve them before the custom domain goes live.

## 8. Visual design direction

- **Palette:** midnight navy `#0F1B2D`, warm ivory `#F6F1E7`, a deeper ivory `#EEE7D9`, charcoal `#2B2E34`, and antique gold `#A88A55` (hairlines and markers only) with a darker gold `#775C30` for small text. All text meets WCAG AA contrast.
- **Typography:**
  - Newsreader, a variable editorial serif with optical sizes, for display and reading.
  - Instrument Sans, used sparingly, for navigation, labels and buttons.
  - Both are self-hosted, with no third-party font requests.
  - This replaces Playfair Display, which is heavily associated with templates.
- **Wordmark:** the name set in Newsreader, with "Private Advisory · London" beneath. The boxed monogram is gone. The favicon is a single serif "Z" on navy with a gold rule.
- **Photography:**
  - The portrait is used in three crops (4:5 hero, 3:4 feature, 1:1 note).
  - Contemporary African architecture, craft, production, hospitality and commercial infrastructure (Djenné, Fez, Kericho, Durban, Marrakech, Kigali, Nairobi) replaces safari and textile imagery.
  - All of it is shown in black and white for one consistent tone, under open licences with credits on a dedicated page.
- **Layout:** generous space, hairline rules instead of boxes, a consistent 1240px grid, and no rounded cards, shadows or gradients.
- **Motion:** a quiet fade as sections enter the screen, cross-page view transitions in supporting browsers, and colour revealed on hover for perspectives. All of it is switched off for visitors who prefer reduced motion.

## 9. Technical and UX improvements made

- Clean URLs (`/advisory/provenance/`), with redirects from every old address.
- Canonical URLs on `zinzilevuma.com`, plus a sitemap, robots file, Open Graph and Twitter metadata, and a share image built from the portrait.
- Structured data:
  - `Person`
  - `ProfessionalService` with an offer catalogue of the six disciplines
  - `Service` on each discipline page
  - `Article` on each perspective
  - `ProfilePage`
  - `BreadcrumbList`
- Images resized and compressed, with responsive `srcset`, WebP and explicit dimensions so layouts don't jump. The hero portrait loads first and everything else is lazy-loaded.
- Self-hosted variable fonts with preload and `font-display: swap`, and long-term caching for fonts and images.
- Accessibility:
  - skip link, visible focus states, semantic landmarks and one `h1` per page
  - labelled form fields with inline, announced error messages
  - keyboard-operable menu (Escape closes it)
  - reduced-motion support
- Enquiry form:
  - Netlify form `enquiry` with a spam honeypot.
  - Fields for role, organisation, area of advisory (preselected from each discipline page) and markets of interest.
  - Sends in place with confirmation, and falls back to a thank-you page without JavaScript.
  - A privacy notice is linked from the form.
- The footer is branded and clean: the practice description, all six disciplines, a branded email address, and privacy and credits links.

## Open questions (not invented, please confirm)

1. **Email:** the site now uses `enquiries@zinzilevuma.com`. That mailbox must exist and be monitored before launch, and Netlify form notifications should be sent to it.
2. **Domain:** `zinzilevuma.com` needs to be added to the Netlify project and set as the primary domain. Netlify will then redirect the netlify.app address automatically.
3. **Education:** the exact qualification and year for Regent's University London (for example, BA or MA in Luxury Brand Management).
4. **Professional history:** any employers or roles you are happy to name, which would strengthen the About page considerably.
5. **The caviar study:** is it academic research (for example, a dissertation) or independent research? It is labelled "Research in progress" until you confirm.
6. **The Forbes Africa work:** confirm the description is accurate and acceptable to publish.
7. **In-person meetings:** confirm "in person in London" is still offered.
8. **LinkedIn or other profiles** to link from the footer and the `Person` schema (`sameAs`).
9. **Photography:** commission three to four further editorial portraits, for example seated in conversation, at work with documents, an environmental portrait in an architectural interior, and a close portrait. One portrait used in three crops is the main visual weakness that remains.
10. **Image permissions:** five photographs were supplied by you and are credited to where they were published: the Bosjes Chapel (Parametric Architecture; architecture by Steyn Studio), the Cape Town EDITION (Hotel Designs), diamond polishing (Stephen Hughes Fine Diamonds), basket weaving (54kibo) and a safari lodge (source unknown). A credit is not a licence. Written permission from each rights holder, or the original photographer's credit and licence, is needed before the site launches on zinzilevuma.com. The safari lodge image also needs a source, and at 900 pixels wide it looks soft when shown large. Confirm, too, that it is a real photograph rather than a computer-generated image.
11. **Perspectives:** approve the three drafts, and add perspectives over time. One substantive piece a month would quickly build the evidence the breadth of the offer needs.
