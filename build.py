#!/usr/bin/env python3
"""Builds the static site. No dependencies.
Run: python3 build.py   (writes the HTML files next to this script).

Text pages (privacy, support questions) come from src/*.md. The product page,
the home page, and the support page's top section are laid out here, since
they mix text with images and cards.

Markdown handled: # headings, - bullets, **bold**, *italics*, [link:/path|text],
https:// autolinks, @brainwavelabs.app emails, "> " lines (a highlighted box),
and, in the support questions, a **question?** line followed by its answer,
which becomes a click-to-open question.

No analytics, trackers, cookies, or outside fonts: the site practices what the
privacy policy says.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = 'https://brainwavelabs.app'
YEAR = 2026


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[link:([^|\]]+)\|([^\]]+)\]', r'<a href="\1">\2</a>', t)
    t = t.replace('&amp;middot;', '&middot;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(.+?)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'(https://[^\s<)]+[^\s<).,])', r'<a href="\1">\1</a>', t)
    t = re.sub(r'([\w.+-]+@brainwavelabs\.app)', r'<a href="mailto:\1">\1</a>', t)
    return t


def md(text, faq=False):
    """faq=True turns '**Question?**' + answer lines into <details> blocks."""
    out, para, items, quote = [], [], [], []
    def flush():
        if quote:
            out.append('<div class="glance">' + ''.join(f'<p>{inline(q)}</p>' for q in quote) + '</div>'); quote.clear()
        if para:
            first = para[0]
            if faq and re.fullmatch(r'\*\*[^*]+\?\*\*', first) and len(para) > 1:
                q = first.strip('*')
                out.append(f'<details><summary>{inline(q)}</summary><p>' + '<br>\n'.join(inline(l) for l in para[1:]) + '</p></details>')
            else:
                out.append('<p>' + '<br>\n'.join(inline(l) for l in para) + '</p>')
            para.clear()
        if items:
            out.append('<ul>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ul>'); items.clear()
    for line in text.splitlines():
        if not line.strip(): flush(); continue
        if line.startswith('> '):
            if para or items: flush()
            quote.append(line[2:]); continue
        if quote: flush()
        m = re.match(r'(#{1,3}) (.*)', line)
        if m: flush(); n = len(m.group(1)); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>'); continue
        if line.startswith('- '):
            if para: flush()
            items.append(line[2:]); continue
        if items: flush()
        para.append(line)
    flush()
    return '\n'.join(out)


def page(title, body, desc, path, product=False, image='/img/og-pmconsole.jpg', wide=False, mid=False):
    t = html.escape(title); d = html.escape(desc)
    def here(p): return ' aria-current="page"' if path == p else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/pm-icon.svg" type="image/svg+xml">
<link rel="icon" href="/img/pm-icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/img/pm-icon-180.png">
<link rel="stylesheet" href="/style.css">
</head>
<body{' class="product"' if product else ''}>
<header class="site">
  <div class="bar">
    <a class="brand" href="/">Brainwave Labs</a>
    <nav>
      <a class="nav-app" href="/pmconsole/"{here('/pmconsole/')}><img src="/img/pm-icon.svg" alt="" width="22" height="22">PM Console</a>
      <a href="/pmconsole/support/"{here('/pmconsole/support/')}>Support</a>
      <a href="/pmconsole/privacy/"{here('/pmconsole/privacy/')}>Privacy</a>
    </nav>
  </div>
</header>
<main{' class="wide"' if wide else ' class="mid"' if mid else ''}>
{body}
</main>
<footer class="site">
  <div class="foot">
    <div class="foot-brand"><img src="/img/pm-icon.svg" alt="" width="20" height="20"> &copy; {YEAR} Brainwave Labs LLC</div>
    <div><a href="/pmconsole/support/">Support</a> &middot; <a href="/pmconsole/privacy/">Privacy</a> &middot; <a href="mailto:support@brainwavelabs.app">support@brainwavelabs.app</a></div>
  </div>
</footer>
</body>
</html>
'''


def write(rel, *args, **kw):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(page(*args, **kw))


def shot(name, alt, eager=False):
    lazy = '' if eager else ' loading="lazy"'
    return f'<img class="shot" src="/img/{name}.jpg" alt="{html.escape(alt)}" width="1600" height="1000"{lazy} decoding="async">'


def icon(paths):
    return ('<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


# Shown in the hero until the app is on sale. When it is, replace this with
# Apple's official "Download on the Mac App Store" badge linking to the app,
# following Apple's marketing guidelines (badge artwork from Apple only).
AVAILABILITY = '<span class="pill">Coming soon to the Mac App Store</span><span class="req">For Mac, macOS 13 or newer</span>'

FEATURES = [
    ('02-timeline', 'Roadmap', 'See the whole roadmap at a glance',
     'Lay out initiatives by quarter, break them into features with their own dates, and track milestones and risks. '
     'A dashed line shows where today falls. Export the timeline to Excel, ready to paste into a slide.',
     'The Timeline: initiatives as colored bars by quarter, with milestones above'),
    ('05-car', 'Funding requests', 'Make a stronger case for the money',
     'A guided questionnaire walks you through the problem, the options, and the costs. PM Console estimates payback, IRR, and NPV '
     'as you type, then builds a memo and a financial workbook. AI drafting is there if you want it, never required.',
     'A funding request: spending by year, a cost breakdown, and estimated returns'),
    ('03-finances', 'Finances', 'Know where every dollar stands',
     'Budget, forecast, and actual spending for every project, month by month. Burn charts show where you are headed, '
     'and you can paste actuals straight from a spreadsheet or import a template.',
     "A project's finances: budget, actual to date, projected total, and a burn chart"),
    ('04-capacity', 'People and capacity', 'Spot overload before it happens',
     "See who is working on what, month by month. Click any month to rebalance someone's time on the spot, "
     'and see what each person and department costs.',
     "The Capacity Planner: each person's allocation by month, with over-allocation in red"),
    ('06-backlog', 'Backlog', 'Keep day-to-day work moving',
     'A flexible board for the smaller tasks: your own columns, groups, and statuses, in a table or as cards you drag between lanes.',
     'The Backlog as a Kanban board with cards in status lanes'),
]

PROMISES = [
    ('No account', 'Open the app and start. There is nothing to sign up for.',
     '<circle cx="12" cy="8" r="4" /><path d="M5 20a7 7 0 0 1 14 0" />'),
    ('No tracking', "No analytics, ads, or crash reports. We can't see what you do in the app.",
     '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" /><circle cx="12" cy="12" r="2.5" /><path d="M4 4l16 16" />'),
    ('Stays on your device', 'Your plans, budgets, and people are saved on your own computer, with backups you control.',
     '<rect x="3" y="4" width="18" height="12" rx="2" /><path d="M8 20h8M12 16v4" />'),
]


def product_page():
    rows = []
    for i, (img, kicker, title, text, alt) in enumerate(FEATURES):
        rows.append(f'''<section class="feature{' flip' if i % 2 else ''}">
  <div class="copy"><p class="kicker">{kicker}</p><h2>{title}</h2><p>{text}</p></div>
  <div class="frame">{shot(img, alt)}</div>
</section>''')
    promises = ''.join(f'<div class="promise">{icon(p)}<h3>{t}</h3><p>{d}</p></div>' for t, d, p in PROMISES)
    return f'''<section class="hero">
  <img class="app-icon" src="/img/pm-icon.svg" alt="PM Console app icon" width="128" height="128">
  <h1>PM Console</h1>
  <p class="tagline">Your roadmap, budget, and team in one app.</p>
  <p class="lead">Plan initiatives, ask for funding, track every dollar, and see who is working on what, without juggling a stack of spreadsheets.</p>
  <div class="cta">{AVAILABILITY}</div>
</section>
<div class="hero-shot frame">{shot('01-dashboard', 'The PM Console Dashboard: budget, spending, alerts, and the funding pipeline across every project', eager=True)}</div>
{''.join(rows)}
<section class="privacy-band">
  <h2>Private by design</h2>
  <div class="promises">{promises}</div>
  <p class="fine">Two optional features, AI drafting and Jira, send data only when you set them up and use them, straight to those services under your own account. <a href="/pmconsole/privacy/">Read the privacy policy</a>.</p>
</section>
<section class="closing">
  <h2>Questions? We're glad to help.</h2>
  <p>Browse the <a href="/pmconsole/support/">support page</a>, or email <a href="mailto:support@brainwavelabs.app">support@brainwavelabs.app</a>. A real person reads every message.</p>
</section>'''


def support_page():
    text = (ROOT / 'src/pmconsole-support.md').read_text()
    _, _, rest = text.partition('## Common questions')
    questions, _, _ = rest.partition('## Privacy')
    cards = f'''<div class="cards">
  <div class="card">{icon('<path d="M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2V5Z" /><path d="M8 7h6M8 11h6" />')}
    <h3>Read the built-in guide</h3><p>Click <strong>Help</strong> in the sidebar, or the <strong>?</strong> on any screen for help with that screen. New? The <strong>Getting started</strong> checklist on the Dashboard walks you through setup.</p></div>
  <div class="card">{icon('<rect x="3" y="5" width="18" height="14" rx="2" /><path d="m3 7 9 6 9-6" />')}
    <h3>Email us</h3><p><a href="mailto:support@brainwavelabs.app">support@brainwavelabs.app</a><br>A real person reads every message. We aim to reply within two business days.</p></div>
  <div class="card">{icon('<path d="M12 3v12m0 0-4-4m4 4 4-4" /><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />')}
    <h3>Back up your data</h3><p>In <strong>Settings &gt; Backups</strong>, click <strong>Back up now</strong> and save the file. The app also makes an automatic backup every day.</p></div>
</div>'''
    return f'''<section class="page-head">
  <img class="app-icon small" src="/img/pm-icon.svg" alt="" width="72" height="72">
  <h1>How can we help?</h1>
  <p class="lead">PM Console brings your roadmap, the money, and the people doing the work together in one place. Here's how to get unstuck.</p>
</section>
{cards}
<div class="prose">
<h2>When you email us</h2>
<p>Please include:</p>
<ul>
  <li>What you were trying to do, and what happened instead.</li>
  <li>Your PM Console version and your device and its system version (on a Mac: <strong>PM Console &gt; About PM Console</strong> in the menu bar, and <strong>Apple menu &gt; About This Mac</strong>).</li>
  <li>A screenshot, if it helps.</li>
</ul>
<h2>Common questions</h2>
<div class="faq">
{md(questions, faq=True)}
</div>
<h2>Privacy</h2>
<p>See the <a href="/pmconsole/privacy/">PM Console Privacy Policy</a>. In short: we collect nothing, and your data stays on your device.</p>
</div>'''


def home_page():
    return f'''<section class="hero home">
  <h1>Brainwave Labs</h1>
  <p class="tagline">Thoughtful software for people who plan and run products.</p>
  <p class="lead">We're a small studio. We build the tools we wish we'd had, and we keep your data where it belongs: on your device.</p>
</section>
<a class="product-card" href="/pmconsole/">
  <div class="pc-copy">
    <img src="/img/pm-icon.svg" alt="" width="72" height="72">
    <h2>PM Console</h2>
    <p>Your roadmap, funding requests, finances, and team capacity together in one app.</p>
    <span class="more">Learn more &rarr;</span>
  </div>
  <div class="frame">{shot('01-dashboard', 'The PM Console Dashboard', eager=True)}</div>
</a>'''


write('pmconsole/index.html', 'PM Console: your roadmap, budget, and team in one app', product_page(),
      'PM Console brings your roadmap, funding requests, finances, and team capacity together in one app. No account, no tracking; your data stays on your device.',
      '/pmconsole/', product=True, wide=True)
write('pmconsole/support/index.html', 'PM Console Support', support_page(),
      'Help and contact for PM Console: the built-in guide, email support, and answers to common questions.', '/pmconsole/support/', mid=True)
write('pmconsole/privacy/index.html', 'PM Console Privacy Policy', '<div class="prose">' + md((ROOT / 'src/pmconsole-privacy.md').read_text()) + '</div>',
      'How PM Console handles your information: it collects none. Your data stays on your device.', '/pmconsole/privacy/')
write('index.html', 'Brainwave Labs', home_page(),
      'Brainwave Labs makes thoughtful software for people who plan and run products.', '/', wide=True)
write('404.html', 'Page not found', '<section class="page-head"><h1>Page not found</h1><p class="lead">That page doesn\'t exist. Try the <a href="/">home page</a> or <a href="/pmconsole/">PM Console</a>.</p></section>',
      'Page not found', '/404.html')
print('built')
