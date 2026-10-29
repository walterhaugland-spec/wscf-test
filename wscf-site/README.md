# Warm Springs Care Farm website

A plain static site: HTML, one stylesheet, one tiny script. No Wix, no hosting fees, nothing to install. GitHub Pages serves it for free.

## What's here

```
docs/               The finished site. This is what GitHub Pages publishes.
src/pages/          Page content (one file per page). Edit copy here.
src/layout-*.html   Shared header and footer.
src/assets/         Stylesheet, script, favicon, and photos.
site-config.json    Email, phone, waiver links, donate link, EIN, etc.
build.py            Rebuilds docs/ from src/ and site-config.json.
LAUNCH-CHECKLIST.md Every fact still needed before launch.
```

Pages: Home, Programs, Volunteer, Visits, About Us, Linda Haley (/about/linda-haley/), Volunteer Guide (/volunteer-guide/, linked from Volunteer and the footer, not the main nav), and a 404 page.

## Launch on GitHub Pages (about 15 minutes)

1. **Create the repo.** On github.com, click New repository. Name it `warmspringscarefarm.org` (any name works). Public.
2. **Upload the files.** On the empty repo page, click "uploading an existing file," drag in everything inside this folder (including `docs/`), and commit.
   Or from a terminal: `git remote add origin <repo URL>` then `git push -u origin main`.
3. **Turn on Pages.** Repo → Settings → Pages → Source: *Deploy from a branch* → Branch: `main`, folder: `/docs` → Save.
4. **Point the domain.** `docs/CNAME` already contains `warmspringscarefarm.org`. At the domain registrar, add:
   - Four `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One `CNAME` record for `www` → `<your-github-username>.github.io`
   Then in Settings → Pages, enter the domain and tick **Enforce HTTPS** once it's available (can take up to a day).
5. **Before cutting over:** the domain currently points at Wix. Switching the DNS records moves it. Cancel the Wix plan only after the new site is live.

The site also works at `https://<username>.github.io/<repo>/` before the domain is pointed, so you can review it there first. (Only the 404 page needs the custom domain to look right.)

## Test domain (current setting)

The build is set to **wscf-test.com** with `test_mode` on:

- `docs/CNAME` reads `wscf-test.com`, so GitHub Pages serves the site there.
- Every page carries `noindex, nofollow`, and `robots.txt` blocks all crawlers. Google won't list the test site, and it won't compete with warmspringscarefarm.org later.
- Canonical links and the share image point at wscf-test.com.

At the registrar for wscf-test.com, add the four GitHub `A` records for `@` (step 4 above) and a `CNAME` for `www` pointing to `<your-github-username>.github.io`. Then enter `wscf-test.com` under Settings, then Pages, and tick Enforce HTTPS once it's offered.

**Moving to the real domain:** in `site-config.json`, set `site_url` to `https://warmspringscarefarm.org` and `test_mode` to `false`, run `python3 build.py`, and push. The CNAME, canonical links, sitemap and robots.txt all switch over. Then update DNS for warmspringscarefarm.org and remove the custom domain from the test setup.

## Making changes

1. Edit copy in `src/pages/…html`, or facts in `site-config.json`.
2. Run `python3 build.py`. It rebuilds `docs/` and prints how many open items remain per page.
3. Commit and push (or upload the changed `docs/` files). GitHub republishes in about a minute.

Preview locally: `cd docs && python3 -m http.server 8000`, then open http://localhost:8000.

## Open items and placeholders

- **Yellow [brackets]** on the pages are facts still needed. They're visible on purpose so nothing ships unconfirmed. The full list is in LAUNCH-CHECKLIST.md.
- **Links set to `#`** in `site-config.json` (donate, waivers, sponsorship packet, Fox & Kids, wish list) do nothing until filled.
- **Empty optional fields degrade gracefully:** with no form URL, the Barn Club, Teen Crew, and volunteer buttons open an email to Linda; with no newsletter form, "Sign up" opens an email; with no calendar link, a placeholder box shows; social links appear in the footer only once added.

## Photos

The brand guide rules out stock photography, so every image spot is a labeled placeholder describing the shot it needs. To add a photo:

1. Save it to `src/assets/images/` (JPG, about 1600px wide, under 400 KB).
2. In the page file, replace the placeholder, for example
   `<figure class="photo placeholder"><figcaption>…</figcaption></figure>`
   with
   `<figure class="photo"><img src="/assets/images/barn-club.jpg" alt="Two kids brushing a horse in the barn"></figure>`
3. Rebuild. Only publish identifiable photos of minors with written guardian permission.

## Newsletter, forms, and calendar

- **Newsletter:** create a free list in Mailchimp, Buttondown, or Givebutter, copy its form "action" URL into `newsletter_form_action`.
- **Interest forms:** a Google Form link in `barn_club_form_url`, `teen_crew_form_url`, or `volunteer_form_url` replaces the email buttons.
- **Calendar:** Google Calendar → Settings → Integrate calendar → copy the "Public URL to this calendar" embed `src` into `calendar_embed_url`. The calendar must be public.

## Brand

The site follows the WSCF Web Style Guide (Draft 1, October 2026), which builds on Brand Guidelines v1.0:

- **Color:** cream leads, forest carries emphasis, wheat gold appears only on giving buttons (the header Give button and Give online). Section grounds alternate cream, warm white, and oat, with one forest emphasis band per page and a forest footer. All tokens sit at the top of `src/assets/css/site.css`.
- **Type:** Newsreader 500 for headings, quotes, and gift amounts; Mulish for everything else. Both load from Google Fonts.
- **Logo:** official kit files only, in `src/assets/images/logo/`: horizontal full color in the header (200px), reversed in the footer (220px), the hero badge on the home page, and the forest goat mark on the 404 page. Favicons, app icons, and the web manifest are in `src/root/` and land at the top of the site. The cream OG image is the link preview everywhere.
- **Components:** feature rows, three-up and two-up cards, ruled lists, step cards (01, 02, 03), FAQ (heading left, questions right), pull-quote bands, oat jump-link chips, a wheat-gold safety flag in the Volunteer Guide, eucalyptus photo slots with a written brief, and butter `[to confirm]` highlights.
- **Links:** outside sites (Givebutter, partner registration, Children's Home) open in a new tab automatically; internal links do not.
- **SEO:** titles under 60 characters, descriptions under 155. `build.py` prints a note if a page goes over.
