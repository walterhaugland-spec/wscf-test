# Launch checklist

Everything still needed before launch. Butter-highlighted [brackets] must all be gone before launch. Facts marked **config** go in `site-config.json`; the rest are in `src/pages/`.

## Must have for launch
- [ ] Confirm main email (linda@warmspringscarefarm.org) and that texting the phone to book is OK — **config** + Visits
- [x] Donate link (Givebutter) — **config** `donate_url` (givebutter.com/eju5dV, Nov 2)
- [ ] Adult, child, and volunteer waiver links (current Google Form?) — **config**
- [x] Barn Club suggested donation ($25/week, Nov 12)
- [ ] Barn Club timing — Programs
- [ ] Drop-off policy for Barn Club — Programs FAQ
- [x] Parking, restroom, accessibility — removed from Visits (Nov 12)
- [x] Weather cancellation policy — Visits FAQ (snow, lightning within 5 miles; Nov 12)
- [x] Teen volunteer quote permission — Home, Volunteer (confirmed Oct 29)
- [x] EIN — **config** `ein` (87-1279392, Nov 2)
- [ ] Current team titles and board list — About

## Partner programs
- [x] Mind and Body Medicine: Rhythms of Connection, registration link — Programs (Nov 12)
- [ ] Mind and Body Medicine: add to About partners list
- [ ] Self Defense: partner name, format, registration link (ages: junior high, Nov 12) — Programs, About partners
- [ ] Animal-assisted therapy: who delivers sessions (Carbon's Hoofprints?) — Programs
- [ ] Fox & Kids Studio registration link — **config** `fox_kids_url`
- [ ] School or college service-hour partner — Volunteer

## Giving
- [ ] Venmo, Zelle, PayPal handles; mailing address — About (address in **config**)
- [ ] Sponsorship levels approved and packet PDF — About, **config** `sponsorship_packet_url`
- [ ] Amazon wish list link — **config**
- [ ] Business supporter logos — About

## Linda's page (needs her sign-off)
- [ ] Years and roles as an educator
- [ ] Credentials, awards, board seats, education
- [ ] Her own account of why she started the farm (current bracket is a placeholder, not her story)
- [ ] Approve or replace the pull quote
- [ ] What she's ready to share with other farms; whether workshops are offered
- [ ] Recent speaking appearances
- [ ] Parent quote for Notice, Get, Go (with permission)

## Volunteer Guide
- [ ] Where volunteers park; who they check in with and text if they can't come
- [ ] First aid kit location
- [ ] Child-safety reporting steps

## Nice to have
- [x] Calendar embed — **config** (Nov 2)
- [ ] Newsletter form, Instagram/Facebook links — **config**
- [ ] Blog address (Ghost subdomain) — **config** `blog_url`; header Blog link points to "#" until set
- [ ] Event link for "Help at farm events" — Volunteer
- [ ] Photos for each placeholder (see README)
- [ ] Choose the tagline (logo: "A place to gather and grow"; brand guidelines: "A place to heal, connect, and grow"). The site uses the logo's line.
- [ ] Confirm nav labels and order (Programs, Volunteer, Visits, About, Give)
- [ ] Signed media release on file for every photo with an identifiable child; none in therapy settings

## Cutover
- [ ] Review on wscf-test.com (test mode: hidden from search)
- [ ] Switch site-config.json to warmspringscarefarm.org with test_mode false, rebuild, push
- [ ] Point DNS (README step 4), enforce HTTPS
- [ ] Submit `https://warmspringscarefarm.org/sitemap.xml` in Google Search Console
- [ ] Cancel the Wix plan once live
