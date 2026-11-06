#!/usr/bin/env python3
"""Builds the static site from src/*.md. No dependencies.
Run: python3 build.py   (writes the HTML files next to this script)."""
import html, re, pathlib

ROOT = pathlib.Path(__file__).parent

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[link:([^|\]]+)\|([^\]]+)\]', r'<a href="\1">\2</a>', t)
    t = t.replace('&amp;middot;', '&middot;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(.+?)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'(https://[^\s<)]+[^\s<).,])', r'<a href="\1">\1</a>', t)
    t = re.sub(r'([\w.+-]+@brainwavelabs\.app)', r'<a href="mailto:\1">\1</a>', t)
    return t

def md(text):
    out, para, items = [], [], []
    def flush():
        if para: out.append('<p>' + '<br>\n'.join(inline(l) for l in para) + '</p>'); para.clear()
        if items: out.append('<ul>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ul>'); items.clear()
    for line in text.splitlines():
        if not line.strip(): flush(); continue
        m = re.match(r'(#{1,3}) (.*)', line)
        if m: flush(); n = len(m.group(1)); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>'); continue
        if line.startswith('- '):
            if para: flush()
            items.append(line[2:]); continue
        if items: flush()
        para.append(line)
    flush()
    return '\n'.join(out)

def page(title, body, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header><a class="brand" href="/">Brainwave Labs</a>
<nav><a href="/pmconsole/">PM Console</a><a href="/pmconsole/support/">Support</a><a href="/pmconsole/privacy/">Privacy</a></nav></header>
<main>
{body}
</main>
<footer>&copy; 2026 Brainwave Labs LLC &middot; <a href="mailto:support@brainwavelabs.app">support@brainwavelabs.app</a></footer>
</body>
</html>
'''

def write(rel, title, body, desc):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(page(title, body, desc))

write('pmconsole/privacy/index.html', 'PM Console Privacy Policy',
      md((ROOT / 'src/pmconsole-privacy.md').read_text()), 'How PM Console handles your information: it collects none.')
write('pmconsole/support/index.html', 'PM Console Support',
      md((ROOT / 'src/pmconsole-support.md').read_text()), 'Help and contact for PM Console, the app for product portfolio planning.')
write('pmconsole/index.html', 'PM Console', md((ROOT / 'src/pmconsole.md').read_text()),
      'PM Console: roadmap, funding requests, finances, and people capacity for product managers, in one app.')
write('index.html', 'Brainwave Labs', md((ROOT / 'src/home.md').read_text()), 'Brainwave Labs makes software for people who plan and run products.')
write('404.html', 'Page not found', '<h1>Page not found</h1>\n<p>That page doesn\'t exist. Try the <a href="/">home page</a>.</p>', 'Page not found')
print('built')
