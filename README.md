# zinlea.com

The public Zinlea Night marketing site, plus a private, password-gated partnership CRM at `/portal`.

## Site structure

- **`public/`** — the public marketing site (zinlea.com). Static build output; not edited by hand here — replace it wholesale when the marketing site is rebuilt elsewhere.
- **`public/portal/`** — the private partnership CRM: pipeline stats, filters, and a record editor.
- **`netlify/functions/records.mts`** — a serverless function backed by [Netlify Blobs](https://docs.netlify.com/blobs/overview/) for real, persistent storage. `GET` loads all records, `PUT` saves the full set.
- **`netlify/edge-functions/gate.ts`** — an edge function scoped to `/portal`, `/portal/*`, and `/.netlify/functions/records`. It checks for a signed session cookie and redirects anyone without one to `/portal/login.html`. The rest of the site (the marketing pages) is not gated.
- **`public/portal/login.html` + `netlify/functions/auth.mts`** — the passcode form posts to the auth function, which checks it against the `PORTAL_PASSWORD` environment variable and, on success, issues an HMAC-signed `HttpOnly` cookie (signed with `SESSION_SECRET`).
- **`netlify/functions/logout.mts`** — clears the session cookie.

## Required environment variables

Set these in Netlify (Site configuration → Environment variables), scoped to Functions/Runtime:

| Variable          | Purpose                                      |
|-------------------|-----------------------------------------------|
| `PORTAL_PASSWORD` | The shared passcode for the private portal.   |
| `SESSION_SECRET`  | Random secret used to sign session cookies.   |

## Local development

```bash
npm install
npx netlify dev
```

## Deployment

This site auto-deploys from the linked GitHub repository on every push to this branch. Build settings live in `netlify.toml` (publish directory `public`, functions directory `netlify/functions`); edge functions are auto-discovered from `netlify/edge-functions`.

To update the marketing site, replace the contents of `public/` (everything except `public/portal/`) with a fresh build and push — the portal is untouched by that.
