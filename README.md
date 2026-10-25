# easyelm.com

Static site for Easy Elm, hosted on Render (static site `srv-dbc5pd5g1s2s7395fg30`). No build step on Render: the generated HTML files are committed.

## How pages are made

Shared header, footer, contact line and the (hidden) sign-up box live in `_build/build.py`.
Page content lives in `_build/content/`. After editing, run:

    python3 _build/build.py

and commit the regenerated `*.html` files. Do not hand-edit generated pages.

Top menu is always just Home, Support, Privacy. The footer lists every app plus Support and Privacy.

## Adding a future app

1. **Icon:** put a square icon at `/<slug>/icon.png`.
2. **One card on the home page:** copy an `app-card` section in `_build/content/home.html`: icon, name, status badge (`badge` = Testing, `badge badge-soon` = Coming soon), one-line description, one button to `/<slug>/`.
3. **One page from the template:** copy `_app-template.html` to `_build/content/<slug>.html` and fill it in. Keep the section order: what it does, how it works in 3 steps, who it's for, get it, help and privacy links.
4. **One privacy section:** write `_build/content/privacy-<slug>.html` (starts with an `<h1>`). It appears on `/privacy/` under `#<slug>` and as its own page at `/privacy/<slug>/` for Google Play.
5. **Support:** add a button to `#<slug>` in the "Which app?" choice and a `<section id="<slug>">` in `_build/content/support.html`.
6. **Register it** in `_build/build.py`: add `("<slug>", "App Name")` to `APPS` and a `page(...)` line for the app page with `app="<slug>"`.
7. Run the build, check the pages, commit, push, then trigger a Render deploy.

## Email sign-up (not live yet)

Every page has a hidden "Be the first to know" box (`<form id="signup-form">`, with a hidden `app` input: `remote`, `reminders`, `intercom` or `general`). It is hidden with `hidden` + `display:none` and has no action. To go live, wire it to Brevo in `signup()` in `_build/build.py` and remove the hiding.
