#!/usr/bin/env python3
"""
Warm Springs Care Farm: static site builder.

    python3 build.py

Reads page bodies from src/pages/, wraps each in the shared header and footer,
fills {{placeholders}} from site-config.json, and writes the finished site to docs/
(the folder GitHub Pages publishes). No packages to install; Python 3.8+ only.
"""
import json, re, shutil, sys
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

# (source file, output folder, <title>, meta description, nav key, in sitemap)
PAGES = [
    ("home.html", "", "A Care Farm for Kids in Boise | Warm Springs Care Farm",
     "A working care farm in Boise's East End where kids ages 7 to 12 build calm and confidence through real chores and animals with names.",
     "home", True),
    ("programs.html", "programs", "Farm Programs for Kids in Boise | Warm Springs Care Farm",
     "Barn Club, Pre-4-H Club, school field trips, partner classes, and farm-based therapy for kids 7 to 12 on a working care farm in Boise's East End.",
     "programs", True),
    ("volunteer.html", "volunteer", "Volunteer at a Care Farm in Boise | Warm Springs Care Farm",
     "Volunteer with animals and gardens at Warm Springs Care Farm in Boise. Teen Leadership Crew, weekly shifts, group work days, and service hours.",
     "volunteer", True),
    ("visits.html", "visits", "Plan Your Visit | Warm Springs Care Farm, Boise",
     "Plan a visit to Warm Springs Care Farm in Boise's East End. Every visit is by appointment. Sign your waiver, then book your first visit with Linda.",
     "visits", True),
    ("about.html", "about", "About Us | Warm Springs Care Farm, Boise",
     "A century-old horse farm in Boise's East End, now a care farm for children's mental health. Meet founder Linda Haley, our team, and our supporters.",
     "about", True),
    ("linda-haley.html", "about/linda-haley", "Linda Haley, Founder of Warm Springs Care Farm | Boise",
     "Linda Haley founded Warm Springs Care Farm in Boise and helps other communities start care farms for kids ages 7 to 12.",
     "about", True),
    ("volunteer-guide.html", "volunteer-guide", "Volunteer Guide | Warm Springs Care Farm",
     "Before you volunteer at Warm Springs Care Farm in Boise: what to wear, how to work with kids and animals, and how we keep everyone safe.",
     "volunteer", True),
]


def todo(text):
    return f'<span class="tbd">[{text}]</span>'


def derived(cfg):
    """Values computed from the config, so empty fields degrade gracefully."""
    email = cfg["email"]
    mail = lambda subj: f"mailto:{email}?subject={quote(subj)}"
    d = {
        "barn_club_href": cfg.get("barn_club_form_url") or mail("Barn Club"),
        "teen_crew_href": cfg.get("teen_crew_form_url") or mail("Teen Leadership Crew"),
        "volunteer_href": cfg.get("volunteer_form_url") or mail("Volunteering at the farm"),
        "ein_text": cfg.get("ein") or todo("EIN: XX-XXXXXXX"),
        "mailing_address_text": cfg.get("mailing_address") or todo("mailing address"),
        "year": "2026",
    }
    if cfg.get("newsletter_form_action"):
        d["newsletter_block"] = (
            f'<form class="signup" action="{cfg["newsletter_form_action"]}" method="post">'
            '<label>Email address<input type="email" name="email" required autocomplete="email"></label>'
            '<button class="btn" type="submit">Get farm news</button></form>')
    else:
        d["newsletter_block"] = (
            f'<div class="btns"><a class="btn" href="{mail("Add me to farm news")}">Get farm news by email</a></div>')
    if cfg.get("calendar_embed_url"):
        d["calendar_block"] = (f'<div class="embed"><iframe src="{cfg["calendar_embed_url"]}" '
                               'title="Warm Springs Care Farm calendar" loading="lazy"></iframe></div>')
    else:
        d["calendar_block"] = ('<div class="embed empty">The farm calendar will appear here. '
                               + todo("Add the Google Calendar embed link to site-config.json") + '</div>')
    social = []
    if cfg.get("instagram_url"):
        social.append(f'<li><a href="{cfg["instagram_url"]}" rel="noopener">Instagram</a></li>')
    if cfg.get("facebook_url"):
        social.append(f'<li><a href="{cfg["facebook_url"]}" rel="noopener">Facebook</a></li>')
    d["social_links"] = "".join(social)
    return d


def fill(text, values):
    def rep(m):
        key = m.group(1)
        if key not in values:
            sys.exit(f"Unknown placeholder {{{{{key}}}}}")
        return str(values[key])
    # Two passes so derived blocks can contain config placeholders.
    for _ in range(2):
        text = re.sub(r"\{\{\s*([a-z0-9_]+)\s*\}\}", rep, text)
    return text


def relativize(html, depth):
    """Turn root links (/programs/) into relative ones (../programs/) so the site
    works on a custom domain, a github.io project URL, or a local preview."""
    prefix = "../" * depth if depth else "./"
    return re.sub(r'(href|src|action)="/(?!/)', lambda m: f'{m.group(1)}="{prefix}', html)


def new_tab(html, site_url):
    """Outside sites (Givebutter, partner registration, Children's Home) open in a new tab."""
    def fix(m):
        tag = m.group(0)
        if site_url in tag or "target=" in tag:
            return tag
        tag = tag.replace(' rel="noopener"', "")
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r'<a [^>]*href="https?://[^"]*"[^>]*>', fix, html)


def page(layout_head, layout_foot, body, title, desc, nav, url_path, cfg, jsonld=""):
    canonical = cfg["site_url"].rstrip("/") + "/" + (url_path + "/" if url_path else "")
    head = layout_head.replace("%%TITLE%%", title).replace("%%DESC%%", desc) \
                      .replace("%%CANONICAL%%", canonical).replace("%%JSONLD%%", jsonld)
    head = head.replace(f'data-nav="{nav}"', f'data-nav="{nav}" aria-current="page"')
    if cfg.get("test_mode"):  # test domain: keep it out of search results
        head = head.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    return head + body + layout_foot


def main():
    cfg = json.loads((ROOT / "site-config.json").read_text())
    values = {k: v for k, v in cfg.items() if not k.startswith("_")}
    values.update(derived(cfg))

    head = (SRC / "layout-head.html").read_text()
    foot = (SRC / "layout-foot.html").read_text()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(SRC / "assets", OUT / "assets")
    for f in (SRC / "root").iterdir():          # favicons, app icons, web manifest
        shutil.copy(f, OUT / f.name)

    org_ld = json.dumps({
        "@context": "https://schema.org", "@type": "NGO",
        "name": cfg["site_name"], "url": cfg["site_url"],
        "email": cfg["email"], "telephone": cfg["phone"],
        "description": "A working care farm in Boise's East End that supports children's mental health through hands-on, nature-based experiences.",
        "address": {"@type": "PostalAddress", "streetAddress": "Warm Springs Avenue",
                    "addressLocality": "Boise", "addressRegion": "ID", "addressCountry": "US"},
        "founder": {"@type": "Person", "name": "Linda Haley"},
    }, indent=1)

    report = []
    for src, out_dir, title, desc, nav, _ in PAGES:
        body = (SRC / "pages" / src).read_text()
        jsonld = f'<script type="application/ld+json">{org_ld}</script>' if src == "home.html" else ""
        html = page(head, foot, body, title, desc, nav, out_dir, cfg, jsonld)
        html = fill(html, values)
        depth = len([p for p in out_dir.split("/") if p])
        html = new_tab(html, cfg["site_url"])
        html = relativize(html, depth)
        for label, text, cap in (("title", title, 60), ("description", desc, 155)):
            if len(text) > cap:
                print(f"  note: {src} {label} is {len(text)} characters (guide: under {cap})")
        dest = OUT / out_dir / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        report.append((("/" + out_dir + "/") if out_dir else "/", html.count('class="tbd"'), html.count('href="#"')))

    # 404 page keeps root-absolute links (GitHub serves it at any depth).
    body = (SRC / "pages" / "404.html").read_text()
    html = fill(page(head, foot, body, "Page not found | Warm Springs Care Farm",
                     "This page could not be found.", "", "404", cfg), values)
    if not cfg.get("test_mode"):
        html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    (OUT / "404.html").write_text(html)

    # GitHub Pages extras
    host = urlparse(cfg["site_url"]).hostname
    (OUT / "CNAME").write_text(host + "\n")
    (OUT / ".nojekyll").write_text("")
    base = cfg["site_url"].rstrip("/")
    urls = "".join(f"  <url><loc>{base}/{d + '/' if d else ''}</loc></url>\n" for _, d, *_r, inc in PAGES if inc)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    if cfg.get("test_mode"):
        (OUT / "robots.txt").write_text("# Test site: not for search engines\nUser-agent: *\nDisallow: /\n")
    else:
        (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

    print(f"Built {len(PAGES)} pages + 404 into {OUT.relative_to(ROOT)}/ for {host}"
          + (" (TEST MODE: hidden from search engines)" if cfg.get("test_mode") else "") + "\n")
    print(f"{'Page':28} {'Open items':>10} {'Empty links':>12}")
    for path, t, h in report:
        print(f"{path:28} {t:>10} {h:>12}")
    print("\nOpen items show as butter-highlighted [brackets] on the page. See LAUNCH-CHECKLIST.md.")


if __name__ == "__main__":
    main()
