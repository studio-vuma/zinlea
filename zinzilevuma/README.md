# zinzilevuma.com

Static website for Zinzile Vuma's advisory practice. See `STRATEGY.md` for the positioning, audit and open questions.

## Structure

```
src/content.py          Copy and data: disciplines, perspectives, work, image credits
src/build.py            Page templates; writes every page into site/
src/prepare_images.py   One-off image resizing (JPEG + WebP)
src/assets/             Original portrait and photo credit records
site/                   The published website (generated HTML, css, js, fonts, img)
netlify.toml            Publish settings, headers and redirects
```

## Editing

1. Change copy in `src/content.py` or `src/build.py`.
2. Run `python3 src/build.py` from this folder.
3. Commit the changes in `site/` and deploy.

Keep to the house style: British English, first person, no em dashes, no invented clients, results or credentials.

## Deployment

The Netlify project is `zinzile-vuma`. The base directory is `zinzilevuma`, the publish directory is `site`, and there is no build command.

The enquiry form is the Netlify form `enquiry`. Under Forms, turn on email notifications to enquiries@zinzilevuma.com.

Add `zinzilevuma.com` under Domain management and set it as the primary domain.
