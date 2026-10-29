#!/usr/bin/env python3
"""
Builds review.html: the whole site in one self-contained page, for review and
comments as a claude.ai artifact. Run after build.py:  python3 review.py
"""
import base64, re
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
PAGES = [  # key, built path, switcher label
    ("home", "", "Home"),
    ("programs", "programs/", "Programs"),
    ("volunteer", "volunteer/", "Volunteer"),
    ("visits", "visits/", "Visits"),
    ("about", "about/", "About"),
    ("linda", "about/linda-haley/", "Linda Haley"),
    ("guide", "volunteer-guide/", "Volunteer Guide"),
]
KEY_BY_PATH = {"/" + p: k for k, p, _ in PAGES}
BASE = "https://site.local/"


def data_uri(path):
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def rewrite(html, page_path, key):
    """Point every internal link at the review page's hash routes; inline images."""
    base = urljoin(BASE, page_path)

    def href(m):
        attr, url = m.group(1), m.group(2)
        if attr == "src" and not url.startswith(("http", "data:")):
            return f'src="{data_uri(DOCS / urlparse(urljoin(base, url)).path.lstrip("/"))}"'
        if attr != "href" or url.startswith(("mailto:", "tel:", "http")) or url == "#":
            return m.group(0)
        if url.startswith("#"):
            return f'href="#{key}--{url[1:]}"'
        u = urlparse(urljoin(base, url))
        target = KEY_BY_PATH.get(u.path)
        if not target:
            return m.group(0)
        return f'href="#{target}--{u.fragment}"' if u.fragment else f'href="#{target}"'

    html = re.sub(r'(href|src)="([^"]*)"', href, html)
    if key:
        html = re.sub(r'\b(id|aria-labelledby)="([^"]+)"', lambda m: f'{m.group(1)}="{key}--{m.group(2)}"', html)
    return html


def between(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i) + len(end)]


home = (DOCS / "index.html").read_text()
header = rewrite(between(home, '<header class="site-header">', "</header>"), "", "")
footer = rewrite(between(home, '<footer class="site-footer">', "</footer>"), "", "")
css = (DOCS / "assets/css/site.css").read_text()
js = (DOCS / "assets/js/site.js").read_text()

sections, switcher = [], []
for key, path, label in PAGES:
    src = (DOCS / path / "index.html").read_text()
    main = src[src.index('<main id="main">') + len('<main id="main">'):src.index("</main>")]
    hidden = "" if key == "home" else " hidden"
    sections.append(f'<div class="page" data-page="{key}" aria-label="{label} page"{hidden}>{rewrite(main, path, key)}</div>')
    switcher.append(f'<a href="#{key}" data-key="{key}">{label}</a>')

review_css = """
:root { color-scheme: light; }
body { background: var(--cream); }
.wrap { padding-left: max(var(--gutter), env(safe-area-inset-left, 0px)); padding-right: max(var(--gutter), env(safe-area-inset-right, 0px)); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 60; background: var(--forest); }
.review { background: var(--forest); color: var(--cream); font: 600 14px/1.4 var(--font-sans); }
.review .wrap { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; padding-block: 10px; }
.review strong { color: var(--butter); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }
.review nav { display: flex; flex-wrap: wrap; gap: 6px; }
.review a { color: var(--cream); text-decoration: none; padding: 6px 12px; border-radius: 999px; min-height: 32px; display: inline-flex; align-items: center; }
.review a:hover { background: var(--forest-raised); }
.review a[aria-current="page"] { background: var(--cream); color: var(--forest); }
.review span { opacity: .85; font-weight: 400; margin-left: auto; }
.site-header { top: env(safe-area-inset-top, 0px); }
"""

router = """
(function () {
  var pages = document.querySelectorAll('.page');
  function route() {
    var h = (location.hash || '#home').slice(1), key = h.split('--')[0];
    var found = document.querySelector('.page[data-page="' + key + '"]');
    if (!found) { key = 'home'; found = document.querySelector('.page[data-page="home"]'); }
    pages.forEach(function (p) { p.hidden = p !== found; });
    document.querySelectorAll('.review a').forEach(function (a) {
      if (a.dataset.key === key) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    var navKey = { linda: 'about', guide: 'volunteer' }[key] || key;
    document.querySelectorAll('.nav-list > li > a').forEach(function (a) {
      var k = (a.getAttribute('href') || '').slice(1).split('--')[0];
      if (k === navKey) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    var target = h.indexOf('--') > 0 ? document.getElementById(h) : null;
    if (target) target.scrollIntoView(); else window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', route);
  route();
})();
"""

page = f"""<title>Warm Springs Care Farm Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&amp;family=Mulish:wght@400;600;700&amp;display=swap">
<style>{css}{review_css}</style>
<div class="review"><div class="wrap">
<strong>Review copy</strong>
<nav aria-label="Site pages">{''.join(switcher)}</nav>
<span>Butter highlights are facts still to confirm.</span>
</div></div>
{header}
<main id="main">{''.join(sections)}</main>
{footer}
<script>{js}{router}</script>
"""
(ROOT / "review.html").write_text(page)
print(f"review.html: {len(page) // 1024} KB, {len(PAGES)} pages")
