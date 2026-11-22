# Zinlea Health — website & Partnership Portal

zinlea.com is organised around one parent brand and two divisions:

| Brand | URL | What it is |
|---|---|---|
| **Zinlea Health** | `/` | Parent brand / group homepage |
| **Zinlea Night** | `/night/` | Overnight clinical provision across London |
| **Zinlea Global** | `/global/` | Healthcare partnerships across Africa |
| Partnership Portal | `/portal/` | Private, password-gated CRM (both divisions) |

## Public site

Plain static HTML, no build step: `public/index.html`, `public/night/`, `public/global/`, `public/thank-you/`, sharing `public/assets/site.css` and `public/assets/site.js`. The enquiry form uses [Netlify Forms](https://docs.netlify.com/forms/setup/) (form name `enquiry`) — turn on form detection in Netlify and add an email notification so enquiries reach the inbox.

These public paths are listed in `excludedPath` in `netlify/edge-functions/gate.ts`. Any **new** public page must be added there too, otherwise it will redirect to the login.

## Partnership Portal (private)

Each record has a `division` (`night`, `global` or `health`); records saved before divisions existed are treated as Zinlea Night.

## How it works

- **Static app** (`public/portal/index.html`) — the CRM itself: pipeline stats, filters, and a record editor. Shows who's signed in and auto-attributes "Logged by" and engagement-log entries to the authenticated user — these aren't free-text, so one person can't type another's name.
- **Data** (`netlify/functions/records.mts`) — a serverless function backed by [Netlify Blobs](https://docs.netlify.com/blobs/overview/) for real, persistent storage. `GET` loads all records, `PUT` saves the full set.
- **Private entrance** (`netlify/edge-functions/gate.ts`) — an edge function that runs on every request. It checks for a signed session cookie and redirects anyone without one to `/login.html`.
- **Login** (`public/login.html` + `netlify/functions/auth.mts`) — the visitor picks their name and enters their own passcode. The auth function checks both against the `PORTAL_USERS` list and, on success, issues an HMAC-signed `HttpOnly` cookie that embeds the username (signed with `SESSION_SECRET`, so it can't be tampered with client-side).
- **Identity** (`netlify/functions/whoami.mts`) — validates the session cookie and returns the signed-in user's name; the CRM calls this on load to know who's using it.
- **Sign out** (`netlify/functions/logout.mts`) — clears the session cookie.

## Required environment variables

Set these in Netlify (Site configuration → Environment variables), scoped to Functions/Runtime, as **regular** variables (not "secret"/sensitive-flagged — flagging them secret was observed to keep them from reaching Functions at runtime on this project):

| Variable         | Purpose                                                        |
|------------------|------------------------------------------------------------------|
| `PORTAL_USERS`   | JSON array of `{username, name, password}` — one entry per person who can log in. |
| `SESSION_SECRET` | Random secret used to sign session cookies.                    |

To add or remove a person, edit the `PORTAL_USERS` JSON and add a matching `<option>` to the "Who are you?" select in `public/login.html`.

## Local development

```bash
npm install
npx netlify dev
```

## Deployment

This site auto-deploys from the linked GitHub repository on every push to this branch. Build settings live in `netlify.toml` (publish directory `public`, functions directory `netlify/functions`); edge functions are auto-discovered from `netlify/edge-functions`.
