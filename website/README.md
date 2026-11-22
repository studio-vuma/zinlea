# Zinlea Health — public website (redesign)

A redesign of zinlea.com with **Zinlea Health** as the parent brand and two divisions:

| Page | Path | Purpose |
|---|---|---|
| Zinlea Health | `/` | Main page; calls to action for both divisions |
| Zinlea Night | `/night/` | London overnight clinical support (8pm–8am), membership, partnerships |
| Zinlea Global | `/global/` | The Africa initiative; register interest |
| Contact | `/contact/` | Enquiry form (Netlify Forms, `enquiry`) — supports `?type=member\|partnership\|global` |
| Clinical governance | `/clinical-governance/` | Carried over verbatim from the live site |
| Privacy | `/privacy/` | Carried over from the live site |

This folder is separate from the private partnership portal (`/public`, deployed by this repo's Netlify site) and is **not deployed by it**.

## Editing

Pages are generated from `build.py` so the header, footer and form stay consistent:

```bash
python3 website/build.py
```

Styles: `assets/site.css`. Behaviour (sticky header, menu, scroll reveals, form validation): `assets/site.js`.

## Preview locally

```bash
cd website && python3 -m http.server 8000
# open http://localhost:8000
```

## Going live

The current zinlea.com is a separate React app. To launch, either deploy this folder as the zinlea.com site on Netlify (publish directory `website`), or port the design into the existing app. Enable form detection in Netlify so enquiries reach info@zinlea.com.

Photography is from Unsplash (free licence); `assets/img/night-caring-hands.jpg` is the existing hero image from the live site.

## SEO

All page titles, descriptions, social images and structured data live in `seo.py`; `build.py` applies them to every page and also writes `sitemap.xml`, `robots.txt`, `_redirects` (old zinlea.com URLs → new pages, 301), `_headers` and `site.webmanifest`.

What is in place:
- Static HTML pages with real text (the previous site rendered in JavaScript, which search engines read poorly)
- Unique title (≤60 chars) and description (≤155 chars) per page, one `<h1>` per page, canonical URLs, `en-GB` hreflang
- schema.org JSON-LD: MedicalOrganization (Zinlea Health), MedicalBusiness with opening hours and offers (Zinlea Night), Organization (Zinlea Global), Service, WebSite, WebPage/AboutPage/ContactPage, FAQPage and BreadcrumbList
- 1200×630 share images per brand (`assets/og/`), icons and manifest
- Responsive WebP images with explicit sizes, lazy loading and a preloaded hero image
- Sitemap with image entries; 404 page; long-cache headers for assets

Launch checklist:
1. Deploy, then add zinlea.com to Google Search Console and Bing Webmaster Tools and submit `https://zinlea.com/sitemap.xml`.
2. Create or update a Google Business Profile for Zinlea Night (service-area business, London, 8pm–8am).
3. Add social profile URLs (e.g. Instagram) to `sameAs` in `seo.py` so search engines connect them to the brand.
4. Re-run `python3 build.py` after any copy change. To refresh share images: `node tools/render-brand-assets.js`.
