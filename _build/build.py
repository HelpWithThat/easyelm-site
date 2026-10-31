#!/usr/bin/env python3
"""Generates every page from shared header/footer. Run: python3 _build/build.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = [("remote","Easy Elm Remote"),("reminders","Proximity Reminders"),("intercom","Easy Elm Intercom")]

def head(title, desc, url, og="og-easyelm.png", ogalt="Easy Elm logo: a green leaf in a white rounded square on green"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Easy Elm">
<meta property="og:url" content="https://www.easyelm.com{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.easyelm.com/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogalt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://www.easyelm.com/{og}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''

def cur(url, here):
    return ' aria-current="page"' if url == here else ''

def header(here):
    items = "".join(f'<li><a href="{u}"{cur(u,here)}>{n}</a></li>' for u,n in [("/","Home"),("/support/","Support"),("/privacy/","Privacy")])
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/"><img src="/assets/company-mark-160.png" width="56" height="56" alt=""><span>Easy Elm</span></a>
    <nav aria-label="Main"><ul>{items}</ul></nav>
  </div>
</header>
<main id="main" class="wrap">
'''

def signup(app):
    # Kept hidden and inactive until the Brevo backend is wired. No action, no submit handler.
    return f'''<section id="signup" class="card signup" aria-labelledby="signup-h" hidden style="display:none">
  <h2 id="signup-h">Be the first to know</h2>
  <p>Get a short email when a new Easy Elm app is ready to try. No spam, and you can leave anytime.</p>
  <!-- TODO(Brevo): wire this form to the Brevo backend, then remove the hidden attribute and style="display:none". -->
  <form id="signup-form" class="signup-form" hidden style="display:none" onsubmit="return false" novalidate>
    <label for="signup-email">Your email</label>
    <input id="signup-email" name="email" type="email" autocomplete="email" inputmode="email" required>
    <input type="hidden" name="app" value="{app}">
    <button class="btn btn-big" type="submit" disabled>Keep me posted</button>
  </form>
</section>
'''

CONTACT = '<p class="contact">Questions? We&rsquo;d love to hear from you. <a href="mailto:support@easyelm.com">support@easyelm.com</a> or <a href="/contact/">talk with us</a>.</p>'

def footer(here, app="general"):
    links = [("/","Home")] + [(f"/{s}/",n) for s,n in APPS] + [("/news/","What&rsquo;s new"),("/contact/","Talk with us"),("/support/","Support"),("/privacy/","Privacy")]
    items = "".join(f'<li><a href="{u}"{cur(u,here)}>{n}</a></li>' for u,n in links)
    return f'''{signup(app)}{CONTACT}
</main>
<footer class="site-footer">
  <div class="wrap">
    <nav aria-label="Footer"><ul>{items}</ul></nav>
    {CONTACT}
    <p class="slogan">Easy Elm. Helpful apps that stay out of your way.</p>
    <p>&copy; 2026 Easy Elm</p>
  </div>
</footer>
</body>
</html>
'''

def page(path, title, desc, url, body, app="general", **kw):
    fp = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(head(title, desc, url, **kw) + header(url) + "\n" + body.strip() + "\n" + footer(url, app))

def read(name):
    return open(os.path.join(ROOT, "_build", "content", name)).read()

C = lambda n: read(n)

# Single source for the home cards and /apps.json.
SITE = "https://www.easyelm.com"
APP_DATA = [
    dict(name="Easy Elm Remote", slug="remote", description="Use your Android phone as a mouse and keyboard for your computer.", status="Testing", icon="/assets/logo-160.png", alt="Easy Elm Remote app icon: a white laptop and keyboard on green"),
    dict(name="Proximity Reminders", slug="reminders", description="Reminders that go off when you arrive at, or drive by, your favorite places.", status="Coming soon", icon="/reminders/icon.png", alt="Proximity Reminders app icon"),
    dict(name="Easy Elm Intercom", slug="intercom", description="A push-to-talk intercom for the phones in your home or workplace.", status="Coming soon", icon="/intercom/icon.png", alt="Easy Elm Intercom app icon: a microphone with a PUSH button"),
]
def card(a):
    cls = "badge" if a["status"] == "Testing" else "badge badge-soon"
    badge = f'<a class="{cls}" href="/{a['slug']}/#test">{a['status']}</a>' if a["status"] == "Testing" else f'<span class="{cls}">{a['status']}</span>'
    return f'''<section class="card app-card">
  <img class="app-icon" src="{a['icon']}" width="96" height="96" alt="{a['alt']}">
  <h2>{a['name']} {badge}</h2>
  <p>{a['description']}</p>
  <a class="btn btn-big" href="/{a['slug']}/">See {a['name']}</a>
</section>'''
import json
json.dump([dict(name=a["name"], slug=a["slug"], description=a["description"], status=a["status"], page=f"{SITE}/{a['slug']}/", icon=SITE + a["icon"]) for a in APP_DATA],
          open(os.path.join(ROOT, "apps.json"), "w"), indent=2, ensure_ascii=False)
page("index.html","Easy Elm. Helpful apps that stay out of your way.","Easy Elm. Helpful apps that stay out of your way.","/",C("home.html").replace("{{APP_CARDS}}", "\n".join(card(a) for a in APP_DATA)))
page("remote/index.html","Easy Elm Remote: your phone as a mouse and keyboard","Easy Elm Remote turns your Android phone or tablet into a wireless Bluetooth mouse, keyboard, mic and volume control for your Windows PC, laptop, or Android tablet.","/remote/",C("remote.html"),app="remote",og="og-remote.png",ogalt="Easy Elm Remote app icon: a white laptop and keyboard on green")
page("reminders/index.html","Proximity Reminders: reminders at the right place","Location reminders that go off when you drive by or arrive at your favorite places.","/reminders/",C("reminders.html"),app="reminders")
page("intercom/index.html","Easy Elm Intercom: hold a name and talk","A push-to-talk intercom for the phones in your home or workplace, over your own Wi-Fi.","/intercom/",C("intercom.html"),app="intercom")
page("support/index.html","Support: Easy Elm","Help for Easy Elm Remote, Proximity Reminders and Easy Elm Intercom.","/support/",C("support.html"))
def demote(h):
    return h.replace("<h2","<h3").replace("</h2>","</h3>").replace("<h1","<h2").replace("</h1>","</h2>")
pr = {s: C(f"privacy-{s}.html") for s,_ in APPS}
page("privacy/index.html","Privacy Policy: Easy Elm","Privacy policies for Easy Elm apps.","/privacy/",
     C("privacy-intro.html") + "".join(f'<section id="{s}" class="policy">\n{demote(pr[s])}\n</section>\n' for s,_ in APPS))
for s,n in APPS:
    page(f"privacy/{s}/index.html",f"Privacy Policy: {n}",f"Privacy policy for the {n} Android app.",f"/privacy/{s}/",f'<article class="policy">\n{pr[s]}\n</article>', app=s)
page("contact/index.html","Talk to us: Easy Elm","Share an idea, report a problem, or work with Easy Elm.","/contact/",C("contact.html"))
page("news/index.html","What's new: Easy Elm","Latest Easy Elm apps and updates, in plain words.","/news/",C("news.html"))
