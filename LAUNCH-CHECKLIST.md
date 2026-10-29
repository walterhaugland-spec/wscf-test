# Launch checklist

Everything still needed before launch. Butter-highlighted [brackets] must all be gone before launch. Facts marked **config** go in `site-config.json`; the rest are in `src/pages/`.

## Must have for launch
- [ ] Confirm main email (linda@warmspringscarefarm.org) and that texting the phone to book is OK — **config** + Visits
- [ ] Donate link (Givebutter) — **config** `donate_url`
- [ ] Adult, child, and volunteer waiver links (current Google Form?) — **config**
- [ ] Barn Club timing and suggested donation — Programs
- [ ] Drop-off policy for Barn Club — Programs FAQ
- [ ] Parking, restroom, accessibility — Visits
- [ ] Weather cancellation policy — Visits FAQ
- [x] Teen volunteer quote permission — Home, Volunteer (confirmed Oct 29)
- [ ] EIN — **config** `ein`
- [ ] Current team titles and board list — About

## Partner programs
- [ ] Mind and Body Medicine: partner name, format, ages, registration link — Programs, About partners
- [ ] Self Defense: partner name, format, ages, registration link — Programs, About partners
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
- [ ] Newsletter form, calendar embed, Instagram/Facebook links — **config**
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
