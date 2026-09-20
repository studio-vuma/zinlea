# Zinlea Night — Private Partnership CRM

A private, password-gated portal for tracking Zinlea Night's strategic partnership pipeline (care homes, private healthcare groups, concierge services, corporate clients, and more).

## How it works

- **Static app** (`public/index.html`) — the CRM itself: pipeline stats, filters, and a record editor.
- **Data** (`netlify/functions/records.mts`) — a serverless function backed by [Netlify Blobs](https://docs.netlify.com/blobs/overview/) for real, persistent storage. `GET` loads all records, `PUT` saves the full set.
- **Private entrance** (`netlify/edge-functions/gate.ts`) — an edge function that runs on every request. It checks for a signed session cookie and redirects anyone without one to `/login.html`.
- **Login** (`public/login.html` + `netlify/functions/auth.mts`) — the passcode form posts to the auth function, which checks it against the `PORTAL_PASSWORD` environment variable and, on success, issues an HMAC-signed `HttpOnly` cookie (signed with `SESSION_SECRET`).
- **Sign out** (`netlify/functions/logout.mts`) — clears the session cookie.

## Required environment variables

Set these in Netlify (Site configuration → Environment variables):

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
