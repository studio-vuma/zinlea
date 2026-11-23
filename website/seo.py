"""SEO metadata for every page: titles, descriptions, social images, breadcrumbs and
structured data (schema.org JSON-LD). build.py reads this; edit copy here.

Title tags stay under ~60 characters and descriptions under ~155 so search engines
show them in full. Each page targets one clear search intent.
"""
SITE = "https://zinlea.com"
EMAIL = "info@zinlea.com"
TODAY = "2026-11-22"

HOME = ("Zinlea Health", "/")
NIGHT = ("Zinlea Night", "/night/")

# path: title, description, social image, page schema type, breadcrumb trail (excluding the page itself)
PAGES = {
    "/": dict(
        title="Zinlea Health | Private Healthcare & Overnight Nurse Advice",
        desc="Expert medical advice when you need it. Zinlea Night: senior nurses overnight in London, 8pm–8am. Zinlea Global: healthcare partnerships across Africa.",
        og="og-health", type="WebPage", trail=[], name="Zinlea Health"),
    "/about/": dict(
        title="About Zinlea Health | Who We Are",
        desc="Zinlea Health is a private healthcare company, home to Zinlea Night (overnight advice from senior nurses, London) and Zinlea Global (Africa).",
        og="og-health", type="AboutPage", trail=[HOME], name="About"),
    "/night/": dict(
        title="Overnight Medical Advice in London, 8pm–8am | Zinlea Night",
        desc="Private overnight medical advice in London. Speak to an experienced Advanced Nurse Practitioner by phone or video, 8pm–8am. Membership from £85 a month.",
        og="og-night", type="WebPage", trail=[HOME], name="Zinlea Night"),
    "/night/membership/": dict(
        title="Membership & Pricing | Zinlea Night, London",
        desc="Zinlea Night membership: overnight medical advice in London from £85 a month for individuals and £225 for families. Private Client by consultation.",
        og="og-night", type="WebPage", trail=[HOME, NIGHT], name="Membership"),
    "/night/private-client/": dict(
        title="Private Client Overnight Care, London | Zinlea Night",
        desc="Private Client: a named lead clinician, specialist coordination and a personal care plan, arranged around you. Fees agreed after a private consultation.",
        og="og-private", type="WebPage", trail=[HOME, NIGHT], name="Private Client"),
    "/night/how-it-works/": dict(
        title="How Overnight Medical Advice Works | Zinlea Night",
        desc="How Zinlea Night works: request membership, hear back within 24 hours, then call an Advanced Nurse Practitioner between 8pm and 8am, by phone or video.",
        og="og-night", type="WebPage", trail=[HOME, NIGHT], name="How it works"),
    "/night/partnerships/": dict(
        title="Overnight Clinical Support for Care Homes | Zinlea Night",
        desc="Overnight clinical support for London care homes, residences and family offices: triage, remote consultation and escalation from 8pm to 8am.",
        og="og-night", type="WebPage", trail=[HOME, NIGHT], name="Partnerships"),
    "/global/": dict(
        title="Healthcare Partnerships in Africa | Zinlea Global",
        desc="Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new healthcare services together, as equal partners.",
        og="og-global", type="WebPage", trail=[HOME], name="Zinlea Global"),
    "/faq/": dict(
        title="FAQ | Overnight Medical Advice & Membership | Zinlea",
        desc="Answers about Zinlea Night: who you speak to, prescribing, emergencies, your GP, membership prices, Private Client, CQC status and Zinlea Global.",
        og="og-health", type="FAQPage", trail=[HOME], name="FAQ"),
    "/contact/": dict(
        title="Contact Zinlea | Membership & Partnership Enquiries",
        desc="Contact Zinlea about Zinlea Night membership, Private Client, care home partnerships or Zinlea Global. Email info@zinlea.com. We reply within 24 hours.",
        og="og-health", type="ContactPage", trail=[HOME], name="Contact"),
    "/clinical-governance/": dict(
        title="Clinical Governance & Regulation | Zinlea Night",
        desc="Zinlea Night's regulatory status, scope of service, prescribing policy, safeguarding and clinical governance framework. Not an emergency service.",
        og="og-health", type="WebPage", trail=[HOME], name="Clinical governance"),
    "/privacy/": dict(
        title="Privacy Policy | Zinlea Health",
        desc="How Zinlea Health and Zinlea Night collect, use and protect your personal and health information under UK GDPR.",
        og="og-health", type="WebPage", trail=[HOME], name="Privacy policy"),
    "/card/": dict(
        title="Zinlea Health | Contact Card",
        desc="Contact Zinlea Health: email info@zinlea.com, visit zinlea.com or save our contact details to your phone.",
        og="og-health", type="ContactPage", trail=[], name="Contact card", noindex=True),
    "/404.html": dict(
        title="Page Not Found | Zinlea Health", desc="This page could not be found.",
        og="og-health", type="WebPage", trail=[], name="Not found", noindex=True),
    "/thank-you/": dict(
        title="Thank You | Zinlea Health", desc="Thank you for your enquiry.",
        og="og-health", type="WebPage", trail=[HOME], name="Thank you", noindex=True),
}

# Social profiles. Add YouTube here once the channel exists, e.g.
# ("YouTube", "https://www.youtube.com/@zinleanight", "youtube")
SOCIAL = [
    ("Instagram", "https://www.instagram.com/zinleanight/", "instagram"),
]
SAME_AS = [url for _, url, _ in SOCIAL]

ORG_ID = f"{SITE}/#org"
NIGHT_ID = f"{SITE}/night/#org"
GLOBAL_ID = f"{SITE}/global/#org"
LOGO = f"{SITE}/assets/brand/logo-512.png"

ORG = {
    "@context": "https://schema.org", "@type": "MedicalOrganization", "@id": ORG_ID,
    "name": "Zinlea Health", "alternateName": "Zinlea", "url": f"{SITE}/", "email": EMAIL,
    "logo": {"@type": "ImageObject", "url": LOGO, "width": 512, "height": 512},
    "image": f"{SITE}/assets/og/og-health.jpg",
    "description": "Zinlea Health is a private healthcare company. Zinlea Night provides overnight medical advice in London; Zinlea Global builds healthcare partnerships across Africa.",
    "address": {"@type": "PostalAddress", "addressCountry": "GB"},
    "areaServed": [{"@type": "City", "name": "London"}, {"@type": "Continent", "name": "Africa"}],
    "knowsAbout": ["Overnight medical advice", "Out-of-hours clinical support", "Remote consultations",
                   "Advanced Nurse Practitioners", "Care home clinical support", "Healthcare partnerships in Africa"],
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "email": EMAIL,
                     "areaServed": "GB", "availableLanguage": "English"},
    "subOrganization": [{"@id": NIGHT_ID}, {"@id": GLOBAL_ID}],
    "sameAs": SAME_AS,
}
WEBSITE = {
    "@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#website",
    "url": f"{SITE}/", "name": "Zinlea Health", "inLanguage": "en-GB", "publisher": {"@id": ORG_ID},
}
NIGHT_ORG = {
    "@context": "https://schema.org", "@type": "MedicalBusiness", "@id": NIGHT_ID,
    "name": "Zinlea Night", "url": f"{SITE}/night/", "email": EMAIL, "parentOrganization": {"@id": ORG_ID},
    "logo": LOGO, "image": f"{SITE}/assets/og/og-night.jpg", "priceRange": "££", "sameAs": SAME_AS,
    "description": "Private overnight medical advice in London. Experienced Advanced Nurse Practitioners available 8pm–8am by phone or video for reassurance, clinical guidance, remote prescribing where appropriate and escalation support.",
    "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
    "areaServed": {"@type": "City", "name": "London"},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                  "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  "opens": "20:00", "closes": "08:00"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Zinlea Night membership", "itemListElement": [
        {"@type": "Offer", "name": "Individual membership", "url": f"{SITE}/night/membership/",
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": 85, "priceCurrency": "GBP", "unitText": "MONTH"}},
        {"@type": "Offer", "name": "Family membership", "url": f"{SITE}/night/membership/",
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": 225, "priceCurrency": "GBP", "unitText": "MONTH"}},
        {"@type": "Offer", "name": "Private Client", "url": f"{SITE}/night/private-client/"},
        {"@type": "Offer", "name": "Care provider partnership", "url": f"{SITE}/night/partnerships/"}]},
}
GLOBAL_ORG = {
    "@context": "https://schema.org", "@type": "Organization", "@id": GLOBAL_ID,
    "name": "Zinlea Global", "url": f"{SITE}/global/", "email": EMAIL, "parentOrganization": {"@id": ORG_ID},
    "logo": LOGO, "image": f"{SITE}/assets/og/og-global.jpg",
    "description": "Zinlea Global works with healthcare providers, clinicians and investors across Africa to develop new healthcare services together.",
    "areaServed": {"@type": "Continent", "name": "Africa"},
}


def service(name, path, desc, audience=None, offers=None):
    s = {"@context": "https://schema.org", "@type": "Service", "name": name, "url": f"{SITE}{path}",
         "serviceType": "Overnight medical advice", "description": desc, "provider": {"@id": NIGHT_ID},
         "areaServed": {"@type": "City", "name": "London"},
         "hoursAvailable": {"@type": "OpeningHoursSpecification", "opens": "20:00", "closes": "08:00"}}
    if audience:
        s["audience"] = {"@type": "Audience", "audienceType": audience}
    if offers:
        s["offers"] = offers
    return s


EXTRA = {
    "/": [ORG, WEBSITE],
    "/about/": [ORG],
    "/night/": [NIGHT_ORG],
    "/night/membership/": [service(
        "Zinlea Night membership", "/night/membership/",
        "Private overnight medical advice in London from Advanced Nurse Practitioners, 8pm–8am, for individuals and families.",
        offers=[{"@type": "Offer", "name": "Individual", "price": 85, "priceCurrency": "GBP"},
                {"@type": "Offer", "name": "Family", "price": 225, "priceCurrency": "GBP"}])],
    "/night/private-client/": [service(
        "Zinlea Night Private Client", "/night/private-client/",
        "A named lead clinician, coordination with specialist consultants and a personal care plan. Fees agreed after a private consultation.")],
    "/night/how-it-works/": [service(
        "Overnight remote consultations", "/night/how-it-works/",
        "Telephone and video consultations with Advanced Nurse Practitioners between 8pm and 8am.")],
    "/night/partnerships/": [service(
        "Overnight clinical support for care providers", "/night/partnerships/",
        "Overnight triage, remote consultation, prescribing where clinically appropriate and escalation support for care homes, residences and family offices in London.",
        audience="Care homes, residences, family offices and organisations")],
    "/global/": [GLOBAL_ORG],
}


def page_schema(path):
    """WebPage (or subtype) + BreadcrumbList + any page-specific entities."""
    p = PAGES[path]
    out = []
    if p["type"] != "FAQPage":  # the FAQ page builds its own FAQPage entity
        out.append({"@context": "https://schema.org", "@type": p["type"], "@id": f"{SITE}{path}#webpage",
                    "url": f"{SITE}{path}", "name": p["title"], "description": p["desc"], "inLanguage": "en-GB",
                    "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": NIGHT_ID if path.startswith("/night/") else (GLOBAL_ID if path.startswith("/global/") else ORG_ID)},
                    "primaryImageOfPage": f"{SITE}/assets/og/{p['og']}.jpg", "dateModified": TODAY})
    if p["trail"]:
        items = p["trail"] + [(p["name"], path)]
        out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{u}"} for i, (n, u) in enumerate(items)]})
    return out + EXTRA.get(path, [])
