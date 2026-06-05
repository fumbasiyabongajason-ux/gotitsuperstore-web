# Got It Superstore — Canonical Stores Spec

> **Read this before editing the mall on `shop.html`.**
> This file is the source of truth for the 50-store U-shape mall.
> Multiple agents collaborate on this repo across sessions. Do not silently
> regress the mall to an earlier 13-store emoji version.

---

## Layout (locked May 2026)

- **Shape:** Single U-shape walkway on `shop.html`, one long-scroll page
- **Total stores:** 50
  - **Left aisle:** 24 stores (top → bottom)
  - **Centre walkway:** 64px-wide thin corridor with a vertical-rl `WALKWAY` pill label
  - **Right aisle:** 24 stores (top → bottom)
  - **Bottom row:** 2 featured stores closing the U
- **Floor:** Tiled mall-floor centre corridor — warm cream `#f0e4cc` base + diamond/argyle tile `#ddc6a0`, 32px tiles
- **Store icons:** Real merchant favicons via Google's CDN: `https://www.google.com/s2/favicons?domain=DOMAIN&sz=128`
  - **No emoji icons in the mall.** Emoji are used elsewhere on the site (ribbons, badges, etc.) — keep those untouched.

## Bottom row (closes the U)

| Position | Store | Ribbon |
|---|---|---|
| Left | Takealot | Featured · Local pick |
| Centre | (invisible spacer matching walkway) | — |
| Right | Amazon | Featured · Global pick |

## The 50 stores

### Left aisle (24, top → bottom)

| # | Store | Domain |
|---|---|---|
| 1 | ASOS | asos.com |
| 2 | Rakuten | rakuten.com |
| 3 | Zalando | zalando.com |
| 4 | Sephora | sephora.com |
| 5 | Wayfair | wayfair.com |
| 6 | Apple | apple.com |
| 7 | Booking.com | booking.com |
| 8 | Newegg | newegg.com |
| 9 | Decathlon | decathlon.com |
| 10 | Etsy | etsy.com |
| 11 | eBay | ebay.com |
| 12 | Shein | shein.com |
| 13 | AliExpress | aliexpress.com |
| 14 | JD.com | jd.com |
| 15 | Trendyol | trendyol.com |
| 16 | Farfetch | farfetch.com |
| 17 | SSENSE | ssense.com |
| 18 | END. | endclothing.com |
| 19 | Revolve | revolve.com |
| 20 | Uniqlo | uniqlo.com |
| 21 | Mr Porter | mrporter.com |
| 22 | Mytheresa | mytheresa.com |
| 23 | H&M | hm.com |
| 24 | Zara | zara.com |

### Right aisle (24, top → bottom)

| # | Store | Domain |
|---|---|---|
| 25 | COS | cos.com |
| 26 | Mango | mango.com |
| 27 | Nike | nike.com |
| 28 | & Other Stories | stories.com |
| 29 | Selfridges | selfridges.com |
| 30 | Cult Beauty | cultbeauty.com |
| 31 | Lookfantastic | lookfantastic.com |
| 32 | Space NK | spacenk.com |
| 33 | The Body Shop | thebodyshop.com |
| 34 | iHerb | iherb.com |
| 35 | MyProtein | myprotein.com |
| 36 | Gymshark | gymshark.com |
| 37 | On Running | on.com |
| 38 | Columbia | columbia.com |
| 39 | B&H Photo | bhphotovideo.com |
| 40 | LEGO | lego.com |
| 41 | Muji | muji.com |
| 42 | IKEA | ikea.com |
| 43 | Lululemon | lululemon.com |
| 44 | Net-a-Porter | net-a-porter.com |
| 45 | Lush | lush.com |
| 46 | Boots | boots.com |
| 47 | The Outnet | theoutnet.com |
| 48 | Costco | costco.com |

### Bottom row (2, featured)

| # | Store | Domain | Ribbon |
|---|---|---|---|
| 49 | Takealot | takealot.com | Featured · Local pick |
| 50 | Amazon | amazon.com | Featured · Global pick |

## Banned retailers (do NOT add)

These were previously in a 13-store version of the mall and have been intentionally removed. They overlap with Amazon's catalogue and/or are not Skimlinks-monetizable; the user has explicitly excluded them.

- Walmart
- Target
- REI Co-op
- Chewy
- Best Buy

Also intentionally absent: Audible, Goodreads, Kindle, Ring, Twitch, IMDb, Whole Foods, Zappos.

> **Note:** Nike (slot 27) was added at the owner's explicit request (2026-06-05), replacing Massimo Dutti, even though Nike overlaps Amazon's catalogue — the same explicit-override basis on which Amazon and Takealot are included.

## Inquiry Reception modal

The Inquiry Reception modal on `shop.html`, `index.html`, `categories.html`, and `deals.html` carries an `INQUIRY_STORES` JS array that mirrors all 50 stores with brand favicons and per-store search URLs. Keep that array in sync when stores change here.

## Safety attributes (every outbound store link)

Every `<a href>` to a store must carry:

```
target="_blank" rel="noopener noreferrer" referrerpolicy="strict-origin-when-cross-origin"
```

And the URL must be `https://`.

## Sanity check before committing

```bash
grep -cE '<a [^>]*class="store-card"' shop.html   # must equal 50
grep -E 'Walmart|Target|REI Co-op|Chewy|Best Buy' shop.html  # must return nothing
grep -c 's2/favicons' shop.html                # ≥ 50 (mall + modal)
```

## Daily deals rotation (`deals.html`)

The curated deals page now uses a **deterministic daily-rotation picker**:

- A **61-deal pool** is embedded inside `deals.html` as `<script id="deal-pool" type="application/json">…</script>`. The pool covers all 50 mall stores (some stores get multiple picks).
- On page load, a small JS picker reads `Math.floor(Date.now() / 86400000)` (today's day number) and uses it as a seed for a Mulberry32-style PRNG to shuffle the pool deterministically. The first 20 are rendered into `#products-grid`.
- All users visiting on the same UTC day see the **same 20 deals** (good for word-of-mouth + caching). The next day rotates ~14 of 20 to fresh picks.
- The status pill reads `Refreshes daily · 20 of 61 picks` and the `Last refreshed` label is stamped with today's date.
- Static HTML fallback: the FIRST 20 deals of the pool are rendered server-side in `#products-grid` so no-JS clients and search-engine crawlers see content.

**Editing the deal pool**: add or remove objects in the `#deal-pool` JSON block in `deals.html`. Keep schema: `{ url, cat, icon, badgeCls, badge, retailer, name, price }`. Category slugs in `cat` must match the categories used in `categories.html` (electronics, home-kitchen, beauty, clothes, outdoor, medicine-health, travel, toys).

## Change log

- **2026-06-05** — Swapped **Massimo Dutti → Nike** (slot 27, right aisle), at the owner's explicit request. Massimo Dutti had no public affiliate program and was redundant with Zara/Mango/COS; Nike adds athletic variety. Total stays **50**. Updated 3 spots on `shop.html`: the store card, the `ItemList` JSON-LD (position 27), and the `INQUIRY_STORES` modal array. ⚠️ The `INQUIRY_STORES` arrays on `index.html`, `categories.html`, `deals.html` (and any Massimo Dutti entry in the `deals.html` deal pool) still reference Massimo Dutti — sync those when next editing those pages.

- **2026-05-28** — Replaced 3 stores that shut down/were absorbed in 2024 with live retailers across the mall and the Inquiry modal on all 4 pages: Wiggle->Columbia, MatchesFashion->Mytheresa, Feelunique->Space NK. Also: curated deals + the 6 search-404 modal stores (SSENSE, END., Selfridges, The Body Shop, Lush, Boots) now link to store HOMEPAGES, never deep search URLs, so they cannot 404. RULE: deal/modal links must use verified homepages or known-good search endpoints — never unverified deep search paths.

- **2026-05-27 (this commit)** — Daily-rotation deal picker installed on `deals.html`. 61-deal pool across all 50 stores, deterministic per-day shuffle, true "refreshes daily" behaviour.
- **2026-05-27 (3626f207)** — Fixed `categories.html` → `deals.html?cat=<slug>` click flow (was preventDefault'ing into nothing). Expanded deals from 12 to 20. Switched grid to auto-fit + 5-col desktop lock. Made meta descriptions unique across index/categories/deals.
- **2026-05-27** — Sentinel guards added: top-of-file comment in `shop.html`, mall-section sentinel, and this `STORES.md` spec to prevent silent regression by another agent session.
- **2026-05-26 (54b94f6d)** — Walkway label switched to `writing-mode: vertical-rl`; bottom row reverted to `1fr 64px 1fr` matching walkway above; 50-store Inquiry Reception modal pushed to all 4 pages.
- **2026-05-26 (1081f239)** — Amazon promoted to bottom row as Featured · Global pick next to Takealot Featured · Local pick; Costco moved into right aisle slot 48; walkway widened 48px → 64px; walkway label tried `rotate(90deg)` (later replaced with vertical-rl).
- **2026-05-26 (a5aed20d)** — On Running URL canonicalized: `on-running.com` → `on.com`.
- **2026-05-26 (b9220073)** — Initial restoration: rebuilt 50-store U-shape mall after an earlier agent session reverted it to a 13-store emoji version. Banned retailers purged from mall, footer quick-links, modal JS, and disclosure copy.
