# Wallace Office Site Localization Roadmap

**Model site:** Wallace Twin Lakes — https://twinlakesoffice.agent.wallacetn.com/ (Lenoir City / Loudon County)
**Applies to:** the other 10 Wallace office agent sites cloned from the Nelson (Maryville) site.
**Owner:** Howard (Wallace Real Estate marketing). **Executor:** Devin.

The goal for every office site: rank for **its own town, county and nearby communities**, link only to **its own pages**, carry **its own office details**, and **not** reproduce all of East Tennessee (that competes with wallacetn.com). Keep the Wallace design exactly as it is; change copy, links and local scope only.

---

## 0. Ground rules (Howard's, do not break)

1. **Right site first.** Moxi → MY SITES → "Wallace (TN) <Office> Office" → Dashboard. Confirm the admin URL is `<office>office.agent.wallacetn.com` before touching anything.
2. **HTML blocks, not module-by-module edits.** Replace cloned Beaver Builder copy rows with one self-contained, scoped HTML block per page. "KEEP THE DESIGN PRINCIPALS in place - do NOT modify them too much."
3. **Never delete.** Pages stay published; irrelevant ones are **hidden from the menu only**. Old layouts are kept as hidden "Copy" pages before any page is rebuilt.
4. **Local, not regional.** Office town + its counties + nearby towns only. No 22-county grid, no 40-town community list, no "Knoxville & East Tennessee" headings. Point anything broader to wallacetn.com with a single link.
5. **Every link stays on the office site** (`/contact`, `/directory`, `/search#…`, `/our-office`, etc.). Zero links to nelson-realtors.com or any other office site.
6. **Fonts are forced.** Moxi theme CSS overrides headings; every block forces Semplicita Pro with `!important`. Headings are thin (weight 100), two-tone by colour only — never bold/700.
7. **Fix one problem at a time and carry the fix to every similar page/section.**
8. **Verify with cache-busted URLs** (`?v=NN`); Varnish serves stale pages for a few minutes.

---

## 1. Discovery (before editing) — ~30 min

Collect for the office:

| Item | Where |
|---|---|
| Street address, phone, email, managing broker | Moxi office record; wallacetn.com/directory/offices/<slug>; Google Business Profile ("<office> wallace") |
| Office UUID (for Property List checks) | Moxi office record / Featured Properties widget settings |
| Agent roster + directory profile URLs | Moxi roster / `/directory` on the office site |
| Existing About-the-office page (if the broker has one, e.g. tylerletner.com/about-twin-lakes-office) | Ask Howard / search broker's site |
| Primary town, county, 6–8 nearby towns, the lakes/landmarks, interstates, school systems, hospital | Local knowledge + maps |
| Which **county pages** on the site are relevant (Twin Lakes: Loudon, Anderson, Knox, Blount, Monroe, Roane) | Counties dropdown |
| Which **community pages** are viable (Twin Lakes: 16 of 40) | Communities dropdown; map each to its county, drop Knoxville neighbourhoods |
| Office hours (GBP vs. other listings often disagree — confirm with Howard before publishing) | GBP |
| Office-specific Zoho market-report form, Buyer Guide / Seller Guide MoxiPresent links (if any) | Ask Howard. Nelson's must never remain. |

Then audit the live site (curl + grep): count `nelson`, `maryville`, `nelson-realtors`, `Foothills Mall`, `982-0500` on every top-menu page. Twin Lakes started with 79 Nelson links on the home page alone.

---

## 2. Change list, in the order it was done on Twin Lakes

### 2.1 Home page (post 4 on Twin Lakes; check the ID per site)
- Back up: Site Pages → row action **Duplicate** → "Copy of Home" (hide it in the menu).
- Delete the cloned copy rows; keep Moxi's hero/search, CTA strip, listings, journal, consent rows (`scripts/bbapply.py` lists what was kept/removed).
- Insert one HTML module with `templates/block.html` (wrapper `#tlh`). Sections, in order, matching the original design:
  1. Explore <Town> & <County> — 8 local area tiles (image, hover blurb, label) → `/search#location_search_field=<Town>%2C%20TN&status=active`
  2. Search Homes By Lifestyle (Lake & Waterfront, Golf/Mountain, Suburban & Downtown, Country & Land, Investment) → local searches
  3. <County> Market Snapshot cards + "Request a <County> Market Report" button → `/contact` (replaces Nelson's Zoho form unless the office has its own form)
  4. Why Wallace — three local story sections with framed photos + Real Reviews in the same frame
  5. Plan Your Next Move cards (Buying, Selling, Relocation, Investment Opportunities, Luxury) — width 1320px so titles stay on one line
  6. Visit Our <Town> Office — address, phone, email, broker, embedded Google map, directions
  7. Local FAQ (6–8 Qs)
  8. Communities list (local towns only) + Journal heading
- Yoast title/meta: `"<Town> TN Real Estate | Wallace <Office> Office"` + description with the office phone.
- Verify: `#tlh` present, Nelson count 0, all tiles show labels, desktop + mobile screenshots.

### 2.2 About → Our Office (new page, slug `/our-office`)
- Duplicate Home, rename to "Our Office", slug `our-office`, remove the duplicated rows except the HTML row (`scripts/bbapply2.py`).
- Content (`templates/office.html`): office logo + intro, NAP + broker + map, broker's three local stories/photos, agent roster linking to `/directory/...` profiles, "areas we serve" search links, call/message/search CTA. **Leave out any East-TN-wide "Areas of Expertise" list.**
- Yoast: `"Wallace <Office> | <Town> TN Real Estate Office"`.
- Site Pages: nest under **About** as the first child (replaces the brokerage "Our Offices" idea with "Our Office").

### 2.3 Custom footer (site-wide)
- The 8-office block is the brokerage **Default Footer** (saved row 7197, read-only).
- Build the site's own footer template (`/fl-builder-template/footer?fl_builder&fl_builder_ui`, Twin Lakes post 162) as one HTML module with `templates/footer.html` (wrapper `#tlf`) via `scripts/footer_apply.py`.
- Then **Appearance → Footer → Custom Footer → Update**.
- Structure copied from wallacetn.com but office-only: office intro/NAP column · Buyers & Sellers links · Our Office links (Our Office, Meet Our Agents, Reviews, Blog, Contact) · Social · "Request An Evaluation" CTA · single office strip with one "See all Wallace offices" link to wallacetn.com · two buttons (Find A <Office> Agent, Search <County> Homes) · logo row · legal text with auto year · Moxi Terms/Privacy.
- X/Twitter icon is an inline SVG (FA 4.7 has no X logo).

### 2.4 Buyers page (post 6)
- Area of Expertise tiles are heading modules: `save_settings {heading, link}` → 8 local towns + "<County>" in the 9th slot; subtitle → "Browse homes for sale in the <Town> and <County> communities we serve."
- Then the SEO rebuild (`templates/buyers.html`, applied with `scripts/bbapply3.py 6 buyers.html <intro_row> <aoe_row> buyers publish`): replace the intro row + Area of Expertise row with one block — intro with framed photo, 6 "Why buyers choose <County>" cards, 8 area tiles, 6-step buying process, 8-question buyer FAQ (taxes, HOA/POA, dock/TVA rules, schools, commute, down payment, timing, out-of-state).
- Keep Moxi rows: Search Properties, Market Trends, Featured Properties ("My Office's Active Listings" — already office-scoped), Our Partners, Mortgage calculator, contact form.
- The Nelson **BUYER GUIDE** button goes away with the old row; add it back only with an office-specific MoxiPresent link.
- Yoast: `"Buying a Home in <Town> TN | Wallace <Office>"`.

### 2.5 Sellers page (post 7)
- Same pattern (`templates/sellers.html`): intro, 3 "Who is buying" cards + market-report/call CTAs, 6-step selling process (price, prep, photo/video, marketing incl. Luxury Portfolio, negotiate, close), 8-question seller FAQ, valuation CTA.
- Removed the generic "Marketing Services" tabs row (covered by the process section); kept Luxury Services + form. Nelson **SELLER GUIDE** link removed.
- Yoast: `"Sell Your Home in <Town> TN | Wallace <Office>"`.

### 2.6 Relocation page (post 9)
- Replace the 6 East-TN lifestyle-guide tiles row with `templates/relocation.html`: intro (Plan My Move → `/contact`, Relocation Guide PDF), 6 "Why people move to <County>" cards, 4 lifestyle tiles → local searches, 6-step long-distance move process, 8-question moving FAQ. Keep the Moxi search widget row.
- Yoast: `"Relocating to <Town> TN | Wallace <Office>"`.

### 2.7 Luxury page (post 8)
- Brand-wide Wallace Luxury content stays. Fix the **Search Properties** button (Nelson clone pointed at a Murfreesboro drive-time search) → `/search#location_search_field=<County>%2C%20TN&status=active&pricemin=650000`. Heading → "Sophisticated guidance for lakefront & luxury homes in <Town>" (adapt to the office's luxury angle). Yoast title/meta.

### 2.8 Contact page (post 16)
- Insert `templates/contact.html` (office card: NAP, broker, Get Directions, Meet Our Agents + Google map) above the Moxi form; row bg none, padding 0. Yoast title/meta.

### 2.9 Navigation (Moxi Site Pages, no deletions)
- **Counties** dropdown: keep only the office's counties, in Howard's order (`scripts/nav_hide.py "Counties" "Loudon,Anderson,Knox,Blount,Monroe,Roane"`). If a wanted county has no page, ask — don't invent (Twin Lakes: "ignore mcminn").
- **Communities** dropdown: map all 40 to counties, propose a tight list (Twin Lakes: 16), get Howard's pick, then `scripts/nav_hide.py "Communities" "<list>"`.
- Hide the backup "Copy" pages (Duplicate makes them visible).
- Verify: dropdown order live, three hidden pages still open by direct URL.

### 2.10 Still open on Twin Lakes (ask per office)
- Office hours (GBP 9–4 Mon–Thu / 9–3 Fri vs. MapQuest 9–5 — unconfirmed).
- Office-specific Buyer Guide / Seller Guide links; office Zoho market-report form.
- Moxi-global items we can't fix per site: blank company name in the email consent text, old UA Google Analytics (no GA4).

---

## 3. Design system (copy exactly)

- Font: `'Semplicita Pro', Helvetica, Arial, sans-serif`, forced: `#tlh,#tlh *:not(.fa){font-family:… !important}`; `i.fa{font-family:FontAwesome !important}`.
- Headings: weight **100**, uppercase, two-tone (`#2c3e56` + `<span>` in `#93a2b5`), h2 ≈ 40px, section h3 ≈ 24–32px. Body 16/24 `#333`, bold 700.
- Colours: navy `#0a1a2d` / `#0a2240`, slate `#2c3e56`, light slate `#93a2b5`, sage `#c9d4d1`, light blue-gray `#cfd8e1`, light bg `#e8edf2`.
- Buttons: square (`border-radius:0`), navy fill white text; `.tl-soft` light-slate fill; `.tl-ghost` outline. FA 4.7 icons.
- Sections alternate light / dark / sage; inner width 1180px (`.tl-in`), wide 1320px (`.tl-wide`, `.tl-plan`).
- Images in a row are the same size; framed photos use the two-tone frame (`.tl-frame`/`.tl-ph` or Tyler's pre-framed 768×684 images). Tile labels `position:relative;z-index:2` above the photo.
- Row + column: width full, padding 0, bg none, so the block controls its own spacing.

Images available on brokerage.agent.wallacetn.com/files/2026/01/ (shared across sites): Lakes-and-Waterfront.jpg, Mountain-Homes-02.jpg, Suburban-and-Downtown.jpg, Country-and-Land-02.jpg, Walace-Real-Estate-Listing-a-Home02.jpg, Walace-Real-Estate-Relocation.jpg, Wallace-Real-Estate-Investment-Opportunities.jpg, Wallace-Real-Estate-Google-Reviews.png, <County>-County-Tennessee.jpg (Blount, Knox, Loudon, Monroe, Roane…), partner logos (*-Logo-Homepage.png). Office-specific photos (broker's story images, office logo) must be sourced per office.

---

## 4. Mechanics (how the scripts work)

All scripts drive the already-logged-in Chrome over CDP (`http://localhost:29229`) with Playwright. Nothing touches WordPress files.

| Script | Purpose |
|---|---|
| `scripts/bbapply.py` | Home page: delete cloned rows, set HTML module, zero row/col padding, publish, verify `#tlh` + Nelson count |
| `scripts/bbapply2.py <post> <html> draft\|publish` | Duplicated page (Our Office): delete every row except the kept one, set HTML, save |
| `scripts/bbapply3.py <post> <html> <target_row> <rows_to_delete,csv> <slug> publish\|draft` | Generic: add an HTML module to the first column of `<target_row>`, delete that row's old modules/extra columns and the listed rows, zero padding, publish, verify live. Used for Buyers, Sellers, Relocation |
| `scripts/footer_apply.py` | Rebuild the site's footer template (post 162 on Twin Lakes) as one HTML module |
| `scripts/nav_hide.py "<Parent>" "<a,b,c>"` | Reorder + hide dropdown children in Site Pages (no deletions) |
| `scripts/set_yoast.py <post> "<title>" "<desc>" "<kw>"` | Yoast title/meta via the classic edit screen |
| `scripts/backup.py`, `scripts/allpages.js` | Page duplication helper; Moxi Site Pages JS (reference for `setShowHideValues`) |

Beaver Builder facts: open `?page_id=N&preview=true&fl_builder&fl_builder_ui`; builder DOM lives in frame `fl_builder_ui_iframe`; call `FLBuilder.ajax({action:'render_new_module'|'save_settings'|'delete_node'|'render_layout'|'save_layout', …})` from the top frame; node settings in `FLBuilderSettingsConfig.nodes[id]`; reload after deletes (stale ids hang). `save_layout {publish:true}` publishes.

Moxi Site Pages facts: standard WP menus are unsupported by the theme. Rows are `div.mxMoveableRow#nav<ID>` in nested `<ol><li>`; move `<li>`s to reorder/nest; `jQuery(div).setShowHideValues('Show'|'Hide')`; `jQuery('input#publish').click()`. Remove the Zendesk launcher iframe first — it intercepts clicks. Duplicate = row action; the copy is visible in the menu until hidden.

---

## 5. Per-office checklist (copy for each site)

```
Office: ______  Site: ______office.agent.wallacetn.com  Town/County: ______
[ ] 1  Right site confirmed (MY SITES → office → Dashboard)
[ ] 2  Discovery sheet filled (NAP, broker, roster, counties, towns, photos, guides/forms)
[ ] 3  Audit: Nelson/Maryville counts per page recorded
[ ] 4  Home: duplicated (hidden), HTML block applied, Yoast, verified desktop/mobile, 0 Nelson
[ ] 5  Our Office: created, nested under About, Yoast
[ ] 6  Footer: site template rebuilt, Appearance → Footer = Custom Footer, checked on 2 pages
[ ] 7  Buyers: AoE tiles local, HTML block, Yoast, Moxi rows intact, backup hidden
[ ] 8  Sellers: HTML block, Yoast, backup hidden
[ ] 9  Relocation: HTML block, Yoast
[ ] 10 Luxury: search button + heading + Yoast
[ ] 11 Contact: office card + map + Yoast
[ ] 12 Counties dropdown trimmed (list approved by Howard)
[ ] 13 Communities dropdown trimmed (list approved by Howard)
[ ] 14 Backups hidden; 3 hidden pages open by direct URL
[ ] 15 Open items sent to Howard: hours, guide links, market-report form
```

## 6. Find-and-replace map when cloning the Twin Lakes templates

`Twin Lakes` → office name · `Lenoir City` → town · `Loudon County` → county · `105 N. A Street, Lenoir City, TN 37771` → address · `(865) 328-1111` / `+18653281111` → phone · `TwinLakes@Wallacetn.com` → email · `Tyler Letner` → broker · lake/landmark/interstate/school/hospital facts in the FAQs and "why" cards (rewrite, don't just swap names) · the 8 tile towns and their search URLs · Twin-Lakes-2.png logo · story photos 01–03.jpg · Google map `q=` address.
