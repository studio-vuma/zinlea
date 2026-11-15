# zinzilevuma.com

Static HTML and CSS. No build step. The live site is everything in `site/`.

## Pages
- `site/index.html`: home (hero, approach, services, how it works, work preview, about, contact)
- `site/services.html`: services and who each one suits
- `site/work.html`: three concept studies (clearly labelled, not client projects)
- `site/questions.html`: questions and answers (with FAQ schema)
- `site/contact.html`: Netlify form (name, email, brand, message), redirects to `site/thanks.html`
- `site/404.html`

## Portrait
Add the portrait as `site/portrait.jpeg` (portrait orientation, roughly 4:5, at least 704 x 880 px,
compressed to under 200 KB). Until it exists, the home page hides the image space automatically.

## Deploying on Netlify
1. Add new site, import this repository.
2. Base directory: `zinzilevuma`. Publish directory: `zinzilevuma/site`. Leave the build command empty.
3. Add the custom domain zinzilevuma.com.
4. Forms: Netlify detects the `contact` form on deploy. Under Forms, turn on email notifications
   to enquiries@zinzilevuma.com.

`directions/` holds the early design options and is not published.
