#!/usr/bin/env python3
"""One-off generator for windsports.obx.deals area + guide pages.
Not part of the rental-intel repo (no recurring data dependency to keep live) --
run once to produce the static pages, then edit by hand going forward."""
import json
from pathlib import Path

OUT = Path("/Users/loaner/git/obx-windsports")

NAV = """  <nav class="site-nav" aria-label="OBX Deals network">
    <div class="site-nav-inner">
      <a href="https://obx.deals/" class="nav-brand-obx">OBX</a><a href="/" class="nav-brand-suffix">Wind Sports</a>
      <div class="nav-links">
        <a href="/canadian-hole/"{ch}>Canadian Hole</a>
        <a href="/tri-villages/"{tv}>Tri-Villages</a>
        <a href="/island-creek/"{ic}>Island Creek</a>
        <a href="/guide/"{gd}>Trip Guide</a>
      </div>
      <div class="nav-cta"><a href="https://search.obx.deals/">Search all rentals &rarr;</a></div>
    </div>
  </nav>
"""

CSS = """  <style>
    :root {
      --ink: #0f1d1c; --muted: #4d6663; --rule: #d7e8e6;
      --accent: #0d9488; --accent-dark: #0a6d64; --bg: #f3faf9; --card-bg: #fff;
      --nav-bg: #1A2B3C; --nav-text: #b8d0cc; --nav-active: #ffffff; --nav-gold: #E8B84B;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      background: var(--bg); color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 17px; line-height: 1.6;
    }
    a { color: var(--accent-dark); }
    .site-nav { background: var(--nav-bg); position: sticky; top: 0; z-index: 100; border-bottom: 2px solid var(--nav-gold); }
    .site-nav-inner { max-width: 980px; margin: 0 auto; display: flex; align-items: center; padding: 0 1.25rem; flex-wrap: wrap; }
    .nav-brand-obx, .nav-brand-suffix { font-weight: 800; font-size: 1.1rem; text-decoration: none; padding: 0.75rem 0; white-space: nowrap; }
    .nav-brand-obx { color: var(--nav-gold); margin-right: 0.45rem; }
    .nav-brand-obx:hover { color: var(--nav-active); }
    .nav-brand-suffix { color: var(--nav-active); margin-right: 0.75rem; }
    .nav-brand-suffix:hover { color: var(--nav-gold); }
    .nav-links { display: flex; align-items: stretch; gap: 0; flex: 1; overflow-x: auto; scrollbar-width: none; }
    .nav-links::-webkit-scrollbar { display: none; }
    .nav-links a { color: var(--nav-text); text-decoration: none; font-size: 0.85rem; font-weight: 500; padding: 0.75rem 0.8rem; white-space: nowrap; border-bottom: 2px solid transparent; margin-bottom: -2px; }
    .nav-links a:hover { color: var(--nav-active); }
    .nav-links a.nav-active { color: var(--nav-active); border-bottom-color: #2dd4c4; font-weight: 600; }
    .nav-cta { margin-left: auto; flex-shrink: 0; }
    .nav-cta a { display: inline-block; background: var(--nav-gold); color: #1A2B3C; font-weight: 700; padding: 0.4rem 0.85rem; border-radius: 5px; text-decoration: none; font-size: 0.82rem; margin: 0.6rem 0; }
    .page-hero { background: linear-gradient(160deg, #0a2f2c 0%, #0d4a44 55%, #0d9488 130%); color: #eafff9; padding: 3rem 1.5rem 2.6rem; }
    .page-hero-inner { max-width: 760px; margin: 0 auto; }
    .breadcrumb { font-size: 0.82rem; color: #9fe6da; margin-bottom: 1rem; }
    .breadcrumb a { color: #cdf3ec; text-decoration: none; }
    .page-hero h1 { font-size: clamp(1.7rem, 3.6vw, 2.3rem); letter-spacing: -0.01em; line-height: 1.15; margin-bottom: 0.4rem; }
    .page-hero .stat-line { font-size: 0.92rem; color: #9fe6da; font-weight: 600; }
    main { max-width: 760px; margin: 0 auto; padding: 2.6rem 1.5rem 5rem; }
    main p { margin-bottom: 1.1rem; font-size: 1.02rem; }
    .section-head { font-size: 1.3rem; letter-spacing: -0.01em; margin: 2.4rem 0 0.4rem; }
    .section-sub { color: var(--muted); font-size: 0.92rem; margin-bottom: 1.4rem; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.1rem; margin-bottom: 1rem; }
    .h-card { background: #fff; border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; text-decoration: none; color: inherit; display: block; }
    .h-card:hover { box-shadow: 0 8px 20px rgba(13,148,136,.15); }
    .h-card img { width: 100%; height: 150px; object-fit: cover; display: block; background: #e2f0ee; }
    .h-card-body { padding: 0.85rem 1rem 1rem; }
    .h-card-name { font-size: 0.95rem; font-weight: 700; margin-bottom: 0.2rem; }
    .h-card-meta { font-size: 0.8rem; color: var(--muted); }
    .h-card-badge { display: inline-block; margin-top: 0.5rem; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--accent-dark); background: #d8f4ef; padding: 0.15rem 0.5rem; border-radius: 3px; }
    footer { color: var(--muted); font-size: 0.87rem; margin-top: 3rem; border-top: 1px solid var(--rule); padding-top: 1.4rem; max-width: 760px; margin-left: auto; margin-right: auto; padding-left: 1.5rem; padding-right: 1.5rem; }
    footer a { text-decoration: none; }
  </style>
"""

GTAG = """  <script async src="https://www.googletagmanager.com/gtag/js?id=G-1P2LPD0VMY"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-1P2LPD0VMY');
  </script>
"""


def nav(active):
    return NAV.format(
        ch=' class="nav-active"' if active == "ch" else "",
        tv=' class="nav-active"' if active == "tv" else "",
        ic=' class="nav-active"' if active == "ic" else "",
        gd=' class="nav-active"' if active == "gd" else "",
    )


def house_card(p):
    beds = f"{p['bedrooms']}BR" if p.get("bedrooms") else ""
    pmc_label = p["pmc"].replace("_", " ").title()
    return f"""      <a class="h-card" href="{p['url']}" target="_blank" rel="noopener">
        <img src="{p['image_url']}" alt="{p['property_name']}" loading="lazy">
        <div class="h-card-body">
          <div class="h-card-name">{p['property_name']}</div>
          <div class="h-card-meta">{beds} &middot; {pmc_label} &middot; {int(p['gis_ft_to_sound'])} ft to sound</div>
          <span class="h-card-badge">🪁 Wind Sports Home</span>
        </div>
      </a>"""


# ADR 0216 — real area centroids for Place schema JSON-LD. Tier 1/2 only.
AREA_COORDS = {
    "/canadian-hole/": (35.26354, -75.55444),
    "/tri-villages/": (35.60578, -75.50718),
    "/island-creek/": (35.369, -75.50208),
}


def _json_ld(path, breadcrumb_label, desc):
    import json as _json
    lat, lng = AREA_COORDS[path]
    place = {
        "@context": "https://schema.org",
        "@type": "Place",
        "name": breadcrumb_label,
        "description": desc,
        "address": {"@type": "PostalAddress", "addressRegion": "NC", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        "url": f"https://windsports.obx.deals{path}",
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Wind Sports", "item": "https://windsports.obx.deals/"},
            {"@type": "ListItem", "position": 2, "name": breadcrumb_label, "item": f"https://windsports.obx.deals{path}"},
        ],
    }
    return (f'  <script type="application/ld+json">{_json.dumps(place)}</script>\n'
            f'  <script type="application/ld+json">{_json.dumps(breadcrumb)}</script>\n')


def page(title, desc, path, active, breadcrumb_label, stat_line, body_paragraphs, houses):
    houses_html = "\n".join(house_card(p) for p in houses)
    paras_html = "\n".join(f"      <p>{p}</p>" for p in body_paragraphs)
    json_ld = _json_ld(path, breadcrumb_label, desc)
    # Island Creek's flagship house has a real photo; other areas fall back
    # to the shared hero rather than using a mismatched stock image.
    og_image = ("https://obx.deals/images/hr-avic15.jpg" if path == "/island-creek/"
                else "https://obx.deals/images/hero.png")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{GTAG}  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://windsports.obx.deals{path}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="canonical" href="https://windsports.obx.deals{path}">
  <link rel="icon" href="https://obx.deals/favicon.ico">
{json_ld}{CSS}</head>
<body>
{nav(active)}
  <div class="page-hero">
    <div class="page-hero-inner">
      <nav class="breadcrumb"><a href="/">Wind Sports</a> &middot; {breadcrumb_label}</nav>
      <h1>{breadcrumb_label}</h1>
      <div class="stat-line">{stat_line}</div>
    </div>
  </div>
  <main>
{paras_html}

    <h2 class="section-head">Featured houses</h2>
    <p class="section-sub">Hand-picked for genuine, GIS-verified proximity to real sound-side water access.</p>
    <div class="card-grid">
{houses_html}
    </div>

    <footer>
      <a href="https://obx.deals/">obx.deals</a> &middot;
      <a href="https://search.obx.deals/">Search all rentals</a> &middot;
      <a href="https://obx.deals/wind-sports/">Full ranked wind-sports list</a>
    </footer>
  </main>
</body>
</html>
"""


HOUSES = {
    "hr-avic15": dict(property_id="hr-avic15", property_name="AVIC15 Island Thunder #15-I", pmc="hatteras_realty", bedrooms=4, url="https://www.hatterasrealty.com/hatteras-realty-rentals/avic15-island-thunder-15-i/", image_url="https://gallery.streamlinevrs.com/stl-default-images/3562/home/976925/1760096788_image.jpeg", gis_ft_to_sound=67),
    "hr-avic5": dict(property_id="hr-avic5", property_name="AVIC5 Island Gale #5-I", pmc="hatteras_realty", bedrooms=4, url="https://www.hatterasrealty.com/hatteras-realty-rentals/avic5-island-gale-5-i/", image_url="https://gallery.streamlinevrs.com/stl-default-images/3562/home/976929/1760096847_image.jpeg", gis_ft_to_sound=54),
    "sos-1006": dict(property_id="sos-1006", property_name="Island Blast - #1006", pmc="surf_or_sound", bedrooms=3, url="https://www.surforsound.com/hatteras-vacation-rental/property/1006", image_url="https://www.surforsound.com/media/lgyji3g5/surf-or-sound-realty-1006-island-blast-drone-2.jpg", gis_ft_to_sound=55),
    "bb-hib400-channel-house": dict(property_id="bb-hib400-channel-house", property_name="HIB400, Channel House", pmc="brindley_beach", bedrooms=4, url="https://www.brindleybeach.com/outer-banks-vacation-rentals/hib400-channel-house", image_url="https://images.rezfusion.com?optimize=true&rotate=true&quality=70&width=420&source=https%3A//gallery.streamlinevrs.com/units-gallery/00/08/BB/image_168415163.jpeg&settings=default", gis_ft_to_sound=45),
    "midgett-bsr04": dict(property_id="midgett-bsr04", property_name="BSR04 - Sound Oak Ridge", pmc="midgett", bedrooms=6, url="https://www.midgettrealty.com/rental/sound-oak-ridge", image_url="https://gallery.streamlinevrs.com/stl-default-images/2128/home/402271/1714399196_image.jpeg", gis_ft_to_sound=66),
    "hr-bx470": dict(property_id="hr-bx470", property_name="BX470 Sounds Good", pmc="hatteras_realty", bedrooms=4, url="https://www.hatterasrealty.com/hatteras-realty-rentals/bx470-sounds-good/", image_url="https://gallery.streamlinevrs.com/stl-default-images/3562/home/998470/1765298223_image.png", gis_ft_to_sound=74),
    "resort_realty-7041": dict(property_id="resort_realty-7041", property_name="7041- Duck Dog", pmc="resort_realty", bedrooms=4, url="https://www.resortrealty.com/booking/duck-dog/7041", image_url="https://gallery.streamlinevrs.com/stl-default-images/1538/home/861244/1758657738_image.jpeg", gis_ft_to_sound=1519),
    "resort_realty-7042": dict(property_id="resort_realty-7042", property_name="7042 - Whistling Oyster", pmc="resort_realty", bedrooms=6, url="https://www.resortrealty.com/booking/whistling-oyster/7042", image_url="https://gallery.streamlinevrs.com/stl-default-images/1538/home/777617/1758657638_image.jpeg", gis_ft_to_sound=1586),
    "bb-hir104-pier-house": dict(property_id="bb-hir104-pier-house", property_name="HIR104, Pier House", pmc="brindley_beach", bedrooms=3, url="https://www.brindleybeach.com/outer-banks-vacation-rentals/hir104-pier-house", image_url="https://images.rezfusion.com?optimize=true&rotate=true&quality=70&width=420&source=https%3A//gallery.streamlinevrs.com/units-gallery/00/08/C0/image_163205205.jpeg&settings=default", gis_ft_to_sound=1991),
}

# ── Canadian Hole ────────────────────────────────────────────────────────────
ch_body = [
    "If East Coast wind sports has a capital, it's here: the stretch of soundfront between Avon and Buxton around the Haulover Day Use Area, known to everyone who rides it as Canadian Hole. The name is old and earned &mdash; riders have been driving down from Ontario and Quebec for this spot since the windsurfing era, and on a good forecast weekend the parking lot fills with plates from a dozen states and gear bags with airline tags.",
    "The draw is the same combination that defines the whole island, in its most convenient form: flat, protected Pamlico Sound water, with the launch sitting directly off NC-12. Park, rig on the sand, walk in. No boat, no long carry, no access negotiation. The sound here is shallow a long way out, which is why it's absorbed generations of people learning to jibe and, more recently, learning to foil.",
    "Convenience has a cost: this is the most famous and most crowded spot on Hatteras Island. Big-wind days bring a genuine scene &mdash; which is half the appeal for some riders and exactly what others drive a few more miles to avoid (quieter launches like Island Creek in Avon are a short hop north).",
    "For a home base, Buxton is the largest cluster of wind-sports-eligible rental houses in our data &mdash; 181 properties in the Buxton area alone, from soundfront houses with their own water access to cheaper places a short drive from the Haulover lot. If you want to wake up, check the flag, and be rigged in fifteen minutes, this is the deepest bench of houses on the island.",
]
(OUT / "canadian-hole" / "index.html").write_text(
    page(
        "Canadian Hole / Buxton — OBX Wind Sports",
        "The Outer Banks' most famous kiteboarding and windsurfing spot: Canadian Hole near Buxton, NC. 181 wind-sports-verified rental houses.",
        "/canadian-hole/", "ch", "Canadian Hole / Buxton",
        "181 wind-sports-eligible rental houses &middot; Buxton, NC",
        ch_body,
        [HOUSES[k] for k in ["bb-hib400-channel-house", "midgett-bsr04", "hr-bx470"]],
    ), encoding="utf-8"
)

# ── Tri-villages ─────────────────────────────────────────────────────────────
tv_body = [
    "Cross the Marc Basnight Bridge heading south and the first three villages you hit &mdash; Rodanthe, Waves, and Salvo &mdash; run together into one continuous strip of sandbar, sound on the right, ocean on the left, maybe a half-mile wide in places. This is the tri-village area, and in the wind-sports community it has a specific reputation: everything Canadian Hole offers, with a fraction of the crowd.",
    "The water is the same Pamlico Sound &mdash; flat, protected, shallow far offshore &mdash; and the villages have a long history as a teaching hub, with a strong kiteboarding and windsurfing school presence going back decades. That history shows in the infrastructure: this is a stretch of island that's used to people walking around with kites and boards, and launches are close to where you sleep rather than a drive away.",
    "The rental footprint here is real but small &mdash; 11 wind-sports-eligible houses in our data across the three villages combined, against Buxton's 181. That scarcity cuts both ways. There are fewer houses to choose from, and the good soundfront ones book early. But when you land one, the logistics get very simple: no parking-lot scramble, no waiting for a lane through the crowd, no loading the truck at all if the house sits on the water.",
    "If your ideal trip is sessions from the yard, a quieter lineup, and a shorter drive from the north (these are the first villages on the island), the tri-villages are the play. If you want the scene, Canadian Hole is thirty minutes south.",
]
(OUT / "tri-villages" / "index.html").write_text(
    page(
        "Rodanthe, Waves &amp; Salvo — OBX Wind Sports",
        "A quieter alternative to Canadian Hole on Hatteras Island's northern villages. 11 wind-sports-verified rental houses in Rodanthe, Waves, and Salvo.",
        "/tri-villages/", "tv", "Rodanthe, Waves &amp; Salvo",
        "11 wind-sports-eligible rental houses &middot; The tri-villages, Hatteras Island",
        tv_body,
        [HOUSES[k] for k in ["resort_realty-7041", "resort_realty-7042", "bb-hir104-pier-house"]],
    ), encoding="utf-8"
)

# ── Island Creek (reuse existing Fable copy) ────────────────────────────────
ic_body = [
    "Island Creek is a small soundfront neighborhood in Avon &mdash; fifteen-odd houses on flat Pamlico Sound water, with private community slips, a rigging lawn, and a kite operation running right out of the marina. It's the home venue of OBX Wind, the Outer Banks' premier annual wind-sports event, and the kind of spot regulars keep quiet about: you rig at the house, walk your gear to the water, and launch onto protected sound without ever loading the truck.",
    "The neighborhood has 5&ndash;8 private community slips and a big common area where everyone rigs before launching, and a kite/gear shop sits just across a small footbridge for a downhaul line or a lesson for whoever you dragged along. Most of the houses come set up for this life &mdash; lockable gear storage, outdoor showers &mdash; because they were built for people who show up with quivers, not just beach chairs.",
    "Canadian Hole is about five miles south if you want the bigger scene; Island Creek is the quieter, close-to-home alternative, with the added pull of being where OBX Wind itself is held every year.",
]
(OUT / "island-creek" / "index.html").write_text(
    page(
        "Island Creek — OBX Wind Sports",
        "A small soundfront neighborhood in Avon, NC and home venue of OBX Wind. 16 wind-sports-verified rental houses with private community slips.",
        "/island-creek/", "ic", "Island Creek",
        "16 wind-sports-eligible rental houses &middot; Avon, NC &middot; Home of OBX Wind",
        ic_body,
        [HOUSES[k] for k in ["hr-avic15", "hr-avic5", "sos-1006"]],
    ), encoding="utf-8"
)

print("wrote canadian-hole/, tri-villages/, island-creek/")
