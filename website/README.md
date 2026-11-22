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
