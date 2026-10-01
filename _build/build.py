"""Static site generator for Dishaa Platinum (brand v2). Run: python build.py  (writes ../*.html)"""
import json, os, re, html
from datetime import date
import time
VER = str(int(time.time()))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = json.load(open(os.path.join(ROOT, "_build", "catalog.json")))
E = html.escape
for _col in CAT:  # PT_Mine pieces ("Diamond Edit") are not shown on the site
    CAT[_col] = [i for i in CAT[_col] if i["cat"] != "Diamond Edit"]

PHONE1, PHONE1_T = "+918169120942", "+91 81691 20942"
PHONE2, PHONE2_T = "+912268956666", "+91 22 6895 6666"
EMAIL = "sales@dishaaplatinum.com"
WA = "918169120942"
ADDRESS = "F7 A&amp;B, 2nd Floor, 61, Chandra Darshan Building,<br>Next to Diamond Plaza, Dhanji Street,<br>Zaveri Bazaar, Mumbai 400 005"
# Deploy config (env overrides). BASE is the URL path prefix (e.g. "/disha_platinum" on GitHub Pages,
# "" on a custom domain). SITE is the public origin + BASE, used for canonical/OG/sitemap URLs.
BASE = os.environ.get("DISHAA_BASE", "").rstrip("/")
SITE = os.environ.get("DISHAA_SITE", "https://www.dishaaplatinum.com").rstrip("/")
OUT = os.environ.get("DISHAA_OUT", "") or None
LASTMOD = date.today().isoformat()

# ------------------------------------------------------------------ collections
COLS = [
  dict(slug="men-of-platinum", name="Men of Platinum", short="Men of Platinum", logo="assets/brand/col-mop.png",
       tag="Bold platinum for today’s achievers.", line="Boost your men’s category with bold platinum pieces, built for today’s achievers.",
       hero="assets/p/men-of-platinum/mop-ch-gcc22371tp.webp", bg="assets/banner/bg-room.webp", photo=None),
  dict(slug="evara", name="Evara", short="Evara", logo="assets/brand/col-evara.png",
       tag="Elegance that sells.", line="Add timeless platinum styles to your women’s counter. Evara is elegance that sells.",
       hero="assets/p/evara/evr-ps-psb8970pla-copy.webp", bg="assets/banner/bg-flowers.webp", photo=None),
  dict(slug="platinum-days-of-love", name="Platinum Days of Love", short="PDOL", logo="assets/brand/col-pdol.png",
       tag="Love bands that last forever.", line="Offer love bands that last forever: the platinum rings every modern couple desires.",
       hero="assets/p/platinum-days-of-love/pdl-cb-pgprn1712-f-1.webp", bg="assets/banner/bg-podium.webp", photo=None),
  dict(slug="bandhan", name="Bandhan", short="Bandhan", logo="assets/brand/col-bandhan.png",
       tag="The new-age bride’s choice.", line="Upgrade tradition with platinum mangalsutras, the new-age bride’s choice.",
       hero="assets/p/bandhan/bdn-ms-pt-1.webp", bg="assets/banner/bg-flowers.webp", photo=None),
  dict(slug="farishtey", name="Farishtey", short="Farishtey", logo="assets/brand/col-farishtey.png",
       tag="Made for little angels.", line="Bring more choice to the kids’ section with platinum jewellery made for little angels.",
       hero="assets/p/farishtey/frs-pd-lp24093tp.webp", bg="assets/banner/bg-room.webp", photo=None),
  dict(slug="pride-n-perfect", name="Pride N Perfect", short="Pride N Perfect", logo="assets/brand/col-pnp.png",
       tag="Couple sets that turn heads.", line="Platinum couple sets that turn heads, perfect for weddings, gifting and festive picks.",
       hero=None, bg=None, photo="assets/props/sha00318.webp"),
]
COLMAP = {c["slug"]: c for c in COLS}

# Shop by: who the jewellery is for (collection -> audience)
AUD = [
  dict(key="men", name="Men", cols=["men-of-platinum"], img="assets/spotlight/p-mop.webp", pos="44% 14%",
       line="Chains, kadas, bracelets, rings, studs &amp; cufflinks.",
       looks=["props/sha00145", "props/13372", "props/sha00183", "props/sha00195", "props/sha00151", "props/sha00153", "props/sha00201"]),
  dict(key="women", name="Women", cols=["evara", "bandhan"], img="assets/spotlight/p-evara.webp", pos="34% 18%",
       line="Necklaces, earrings, kadas, pendant sets &amp; mangalsutras.",
       looks=["studio/st09", "studio/st01", "studio/st16", "props/sha00130", "studio/st19", "studio/st07", "props/sha00119", "studio/st22", "studio/st14", "studio/st10", "studio/st20", "studio/st17"]),
  dict(key="kids", name="Kids", cols=["farishtey"], img="assets/spotlight/p-kids.webp", pos="50% 30%",
       line="Baby tops &amp; pendants, gentle on young skin.",
       looks=["props/sha00115", "props/sha00118"]),
  dict(key="couples", name="Couples", cols=["platinum-days-of-love", "pride-n-perfect"], img="assets/spotlight/p-pdol.webp", pos="50% 20%",
       line="Couple bands &amp; matched sets for weddings and gifting.",
       looks=["props/sha00053", "props/sha00318", "props/sha00050", "props/sha00089", "props/sha00059", "props/sha00046", "props/sha00098", "props/sha00062", "props/new1", "props/sha00081"]),
]
AUDOF = {c: a["key"] for a in AUD for c in a["cols"]}

# ------------------------------------------------------------------ svg bits
ARROW = '<svg width="16" height="10" viewBox="0 0 16 10" class="ar" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'
ARROW_UR = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 13L13 3M5 3h8v8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
CHEV_L = '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M11 3 5 9l6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
CHEV_R = '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="m7 3 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
PLUS = '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.5"/></svg>'
TRAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9h18l-2 11H5L3 9Z M8 9V7a4 4 0 0 1 8 0v2" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'
WA_ICO = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2s.2-1.1.2-1.2-.2-.2-.4-.3Z"/></svg>'

ICONS = {
 "trust": '<path d="M24 4 8 10v12c0 10 7 18 16 22 9-4 16-12 16-22V10L24 4Z"/><path d="m16 24 6 6 11-12"/>',
 "innovation": '<path d="M24 6a12 12 0 0 0-7 21.7V33h14v-5.3A12 12 0 0 0 24 6Z"/><path d="M19 38h10M21 42h6M24 14v8l4 3"/>',
 "quality": '<path d="M12 18 24 6l12 12-12 24L12 18Z"/><path d="M12 18h24M18 18l6-12 6 12-6 24"/>',
 "commitment": '<circle cx="18" cy="26" r="11"/><circle cx="30" cy="26" r="11"/>',
 "support": '<path d="M8 26v-4a16 16 0 0 1 32 0v4"/><rect x="6" y="26" width="7" height="12" rx="2"/><rect x="35" y="26" width="7" height="12" rx="2"/><path d="M40 38c0 4-6 6-12 6"/>',
 "growth": '<path d="M6 40h36"/><path d="M10 34 20 24l6 6 14-16"/><path d="M32 14h8v8"/>',
 "exclusivity": '<path d="M24 5 29 18h14l-11 8 4 14-12-9-12 9 4-14-11-8h14Z"/>',
 "reliability": '<circle cx="24" cy="24" r="17"/><path d="M24 12v12l8 5"/>',
 "range": '<rect x="6" y="6" width="15" height="15" rx="3"/><rect x="27" y="6" width="15" height="15" rx="3"/><rect x="6" y="27" width="15" height="15" rx="3"/><rect x="27" y="27" width="15" height="15" rx="3"/>',
 "tech": '<circle cx="24" cy="24" r="6"/><path d="M24 4v8M24 36v8M4 24h8M36 24h8M10 10l6 6M32 32l6 6M10 38l6-6M32 16l6-6"/>',
 "men": '<circle cx="20" cy="28" r="12"/><path d="M29 19 42 6M32 6h10v10"/>',
 "custom": '<path d="M8 40 30 18M26 14l8 8M34 6l8 8-6 6-8-8Z"/>',
 "chat": '<path d="M6 10h36v22H20l-9 8v-8H6Z"/><path d="M14 19h20M14 25h12"/>',
 "branding": '<path d="M8 8h20l12 12-20 20L8 28Z"/><circle cx="17" cy="17" r="3"/>',
 "display": '<rect x="6" y="8" width="36" height="22" rx="2"/><path d="M4 38h40M14 30v8M34 30v8"/><path d="M16 22l5-6 5 5 6-7"/>',
 "training": '<path d="M4 16 24 8l20 8-20 8Z"/><path d="M12 20v10c0 3 5 6 12 6s12-3 12-6V20M44 16v12"/>',
 "promo": '<path d="M6 20v8h6l14 10V10L12 20Z"/><path d="M32 18c2 2 2 10 0 12M37 14c4 4 4 16 0 20"/>',
 "online": '<circle cx="24" cy="24" r="18"/><path d="M6 24h36M24 6c6 6 6 30 0 36M24 6c-6 6-6 30 0 36"/>',
 "marketing": '<path d="M6 38V22M16 38V14M26 38V26M36 38V8"/>',
 "pgi": '<path d="M16 6v36M16 8h8a9 9 0 0 1 0 18h-8"/><path d="M28 22v16c0 3 2 4 6 4"/>',
 "box": '<path d="M6 16 24 8l18 8v18l-18 8-18-8Z"/><path d="M6 16l18 8 18-8M24 24v18"/>',
 "refill": '<path d="M40 24a16 16 0 1 1-5-11.6"/><path d="M40 6v8h-8"/>',
 "buyback": '<path d="M8 18h26a8 8 0 0 1 0 16H14"/><path d="m14 12-6 6 6 6"/>',
 "logo": '<rect x="8" y="8" width="32" height="32" rx="16"/><path d="M20 16v16M20 16h4a6 6 0 0 1 0 12h-4"/>',
 "cert": '<rect x="6" y="8" width="36" height="26" rx="2"/><circle cx="32" cy="34" r="6"/><path d="m28 39-2 6 6-3 6 3-2-6M12 16h20M12 22h14"/>',
 "fast": '<path d="M26 4 10 28h12l-2 16 16-24H24Z"/>',
 "plan": '<rect x="8" y="6" width="32" height="36" rx="3"/><path d="M16 16h16M16 24h16M16 32h10"/>',
}
def icon(k):
    return f'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">{ICONS[k]}</svg>'

def lines(text):
    return "".join(f'<span class="split-line"><span>{t}</span></span>' for t in text.split("|"))

def sparkle(n=22):
    return f'<div class="sparkle" data-n="{n}" aria-hidden="true"></div>'

HEX = """<div class="hex rv"><svg viewBox="0 0 220 246" aria-hidden="true"><path d="M110 4 214 64v118L110 242 6 182V64Z" fill="#fff"/><path d="M110 16 203 70v106l-93 54-93-54V70Z" fill="none" stroke="#27326d" stroke-width="1.4"/></svg>
<div><i>Aggressive</i><b>Action</b><span class="amp">&amp;</span><b>Expansion</b><i>as never before</i></div></div>"""

# ------------------------------------------------------------------ chrome
NAV = [("index.html", "Home"), ("about.html", "About"), ("collections.html", "Collections"),
       ("why-platinum.html", "Why Platinum"), ("partner.html", "Partner"), ("lookbook.html", "Lookbook"), ("contact.html", "Contact")]

ORG_LD = {
  "@context": "https://schema.org", "@type": ["JewelryStore", "Organization"],
  "@id": "SITE_URL/#org", "name": "Dishaa Platinum", "alternateName": "Dishaa — The Platinum Hub",
  "url": "SITE_URL/", "logo": "SITE_URL/assets/brand/dishaa-lockup.png", "image": "SITE_URL/assets/hero/d01.webp",
  "description": "India’s preferred B2B platinum jewellery partner: PGI-certified collections, display, training and branding support for retail jewellers.",
  "telephone": "+91-81691-20942", "email": "sales@dishaaplatinum.com", "priceRange": "B2B",
  "address": {"@type": "PostalAddress", "streetAddress": "F7 A&B, 2nd Floor, 61, Chandra Darshan Building, Next to Diamond Plaza, Dhanji Street, Zaveri Bazaar",
              "addressLocality": "Mumbai", "addressRegion": "Maharashtra", "postalCode": "400005", "addressCountry": "IN"},
  "areaServed": "IN", "slogan": "Pure · Precious · Progressive",
  "brand": [{"@type": "Brand", "name": n} for n in ["Men of Platinum", "Evara", "Platinum Days of Love", "Bandhan", "Farishtey", "Pride N Perfect"]],
}
CRUMB_NAMES = {"explore": "Shop by", "about": "About", "collections": "Collections", "why-platinum": "Why Platinum", "partner": "Partner With Us",
               "lookbook": "Lookbook", "contact": "Contact"}

def ld_json(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("SITE_URL", SITE) + "</script>"

def head(title, desc, page, img="assets/hero/d01.webp", crumbs=None):
    url = f"{SITE}{page}"
    ogimg = f"{SITE}/{img}"
    lds = [ld_json(ORG_LD)]
    if page == "/":
        lds.append(ld_json({"@context": "https://schema.org", "@type": "WebSite", "name": "Dishaa Platinum", "url": "SITE_URL/",
                            "inLanguage": "en-IN", "publisher": {"@id": "SITE_URL/#org"}}))
    else:
        parts = [p for p in page.strip("/").split("/") if p]
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "SITE_URL/"}]
        path = ""
        for k, p in enumerate(parts):
            path += f"/{p}"
            name = (crumbs or {}).get(p) or CRUMB_NAMES.get(p) or next((c["name"] for c in COLS if c["slug"] == p), p.replace("-", " ").title())
            items.append({"@type": "ListItem", "position": k + 2, "name": name, "item": f"SITE_URL{path}/"})
        lds.append(ld_json({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}))
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Dishaa Platinum">
<meta name="theme-color" content="#2e3490">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dishaa Platinum">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:alt" content="Dishaa Platinum — platinum jewellery">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{ogimg}">
<link rel="icon" href="assets/brand/d-mark.png" type="image/png">
<link rel="apple-touch-icon" href="assets/brand/d-mark.png">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
{'<link rel="preload" as="image" href="assets/hero/x01bg.webp" media="(min-width:761px)"><link rel="preload" as="image" href="assets/hero/m01.webp" media="(max-width:760px)">' if page == "/" else ""}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={VER}">
{chr(10).join(lds)}
</head>"""

def header(active):
    cols = "".join(f'<a href="{c["slug"]}.html"><img src="{c["logo"]}" alt="{c["name"]}"></a>' for c in COLS)
    cols += "".join(f'<a class="txt aud" href="explore.html#{a["key"]}"><b>{a["name"]}</b><span>Shop by</span></a>' for a in AUD)
    cols += '<a class="txt" href="accessories.html"><b>Accessories</b><span>Cufflinks &amp; more</span></a><a class="txt" href="d-the-platinum.html"><b>D — The Platinum</b><span>Bars &amp; coins</span></a><a class="txt" href="collections.html"><b>All collections</b><span>Overview</span></a>'
    items = []
    for href, label in NAV:
        on = ' class="on"' if href == active or (label == "Collections" and active == "collections") else ""
        if label == "Collections":
            items.append(f'<div class="dd"><a href="{href}"{on}>{label}</a><div class="dd-menu">{cols}</div></div>')
        else:
            items.append(f'<a href="{href}"{on}>{label}</a>')
    msub = "".join(f'<a class="txt" href="explore.html#{a["key"]}">{a["name"]}</a>' for a in AUD) + "".join(f'<a href="{c["slug"]}.html"><img src="{c["logo"]}" alt="{c["name"]}"></a>' for c in COLS) + '<a class="txt" href="accessories.html">Accessories</a><a class="txt" href="d-the-platinum.html">D — The Platinum</a>'
    mitems = "".join(f'<a href="{h}">{l}</a>' + (f'<div class="sub-m">{msub}</div>' if l == "Collections" else "") for h, l in NAV)
    return f"""<header class="hdr"><div class="wrap">
<a class="brand" href="index.html" aria-label="Dishaa Platinum — home"><img src="assets/brand/dishaa-horizontal.png" alt="Dishaa Platinum"></a>
<nav class="nav" aria-label="Main">{''.join(items)}</nav>
<div class="hdr-cta"><button class="tray-btn" data-open-tray aria-label="Open selection tray">{TRAY}<i>0</i></button>
<a class="btn btn-royal" href="partner.html">Become a Partner</a>
<button class="burger" aria-label="Menu"><span></span><span></span></button></div>
</div></header>
<nav class="mnav" aria-label="Mobile">{mitems}<div class="mfoot"><a href="tel:{PHONE1}">{PHONE1_T}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></nav>"""

def shells():
    return f"""<div class="scrim"></div>
<aside class="tray" aria-label="Selection tray"><div class="tray-hd"><div><h3>Selection Tray</h3><p class="tray-n">0 designs shortlisted</p></div><button class="x" data-close-tray aria-label="Close">&times;</button></div>
<div class="tray-list"></div>
<div class="tray-ft"><button class="btn btn-royal" data-tray-wa>{WA_ICO} Send on WhatsApp</button><button class="btn btn-line" data-tray-mail>Email this selection</button><button class="link" style="justify-self:center;margin-top:6px" data-tray-clear>Clear tray</button></div></aside>
<div class="toast" role="status" aria-live="polite"></div>"""

def footer():
    cols = "".join(f'<li><a href="{c["slug"]}.html">{c["name"]}</a></li>' for c in COLS)
    return f"""<footer class="ftr">
<div class="wrap">
<div class="ftr-top">
<div><img class="flogo" src="assets/brand/dishaa-lockup-white.png" alt="Dishaa Platinum — The Platinum Hub">
<p class="hinglish" style="font-size:24px;color:#fff;margin-top:24px">Aapke saath hai hum.</p></div>
<div><h4>Collections</h4><ul>{cols}<li><a href="accessories.html">Accessories</a></li><li><a href="d-the-platinum.html">D — The Platinum</a></li></ul></div>
<div><h4>Shop by</h4><ul>{"".join(f'<li><a href="explore.html#{a["key"]}">{a["name"]}</a></li>' for a in AUD)}<li><a href="explore.html">All designs</a></li></ul>
<h4 style="margin-top:26px">Dishaa</h4><ul><li><a href="about.html">About Us</a></li><li><a href="why-platinum.html">Why Platinum</a></li><li><a href="partner.html">Partner With Us</a></li><li><a href="partner.html#display">Display &amp; Counters</a></li><li><a href="lookbook.html">Lookbook</a></li><li><a href="contact.html">Contact</a></li></ul></div>
<div><h4>Visit the Hub</h4><address>{ADDRESS}</address><p style="margin-top:16px"><a href="tel:{PHONE1}">{PHONE1_T}</a><br><a href="tel:{PHONE2}">{PHONE2_T}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<img src="assets/brand/pt-logo-white.png" alt="Platinum" style="height:46px;width:auto;opacity:.8;margin-top:18px"></div>
</div>
<div class="ftr-bot"><span>© {date.today().year} Dishaa Platinum · The Platinum Hub, Mumbai</span><span>Pure · Precious · Progressive · Authorised PGI Dealer · T&amp;Cs apply</span></div>
</div></footer>
<script src="assets/vendor/anime.min.js" defer></script>
<script src="assets/js/site.js?v={VER}" defer></script>
</body></html>"""

ROUTES = {"index.html": "/", "about.html": "/about/", "collections.html": "/collections/", "explore.html": "/explore/",
          "accessories.html": "/collections/accessories/", "d-the-platinum.html": "/collections/d-the-platinum/",
          "why-platinum.html": "/why-platinum/", "partner.html": "/partner/", "lookbook.html": "/lookbook/", "contact.html": "/contact/"}
ROUTES.update({f'{c["slug"]}.html': f'/collections/{c["slug"]}/' for c in COLS})

def route_links(html_text):
    """Rewrite internal links to clean folder URLs and assets to root-absolute paths."""
    def repl(m):
        return f'href="{BASE}{ROUTES[m.group(1)]}{m.group(2) or ""}"'
    html_text = re.sub(r'href="([a-z0-9-]+\.html)([?#][^"]*)?"', repl, html_text)
    html_text = html_text.replace('href="sitemap.xml"', f'href="{BASE}/sitemap.xml"')
    html_text = html_text.replace('"assets/', f'"{BASE}/assets/').replace("'assets/", f"'{BASE}/assets/").replace("(assets/", f"({BASE}/assets/")
    return html_text

OG_IMG = {"index.html": "assets/hero/d01.webp", "about.html": "assets/insta/c18.webp", "collections.html": "assets/insta/c05.webp",
          "why-platinum.html": "assets/insta/c07.webp", "partner.html": "assets/insta/c10.webp", "lookbook.html": "assets/lookbook/ph10.webp",
          "contact.html": "assets/insta/c11.webp", "accessories.html": "assets/props/sha00153.webp", "d-the-platinum.html": "assets/dthe/dthe-5.webp"}

def page(fname, title, desc, body, active=None):
    route = ROUTES[fname]
    hero = "light"  # header is always the solid light bar (readable over dark page heroes)
    img = OG_IMG.get(fname) or next((c["hero"] or c["photo"] for c in COLS if f'{c["slug"]}.html' == fname), "assets/hero/d01.webp")
    out = head(title, desc, route, img) + f'\n<body data-hero="{hero}">\n' + header(active or fname) + "\n<main>" + body + "</main>\n" + shells() + footer()
    out = route_links(out)
    d = os.path.join(OUT or ROOT, route.strip("/").replace("/", os.sep))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", route, f"{len(out)//1024} KB")

def phero(kick, title, sub, art, crumbs, tagline=""):
    tg = f'<div class="tagline">{tagline}</div>' if tagline else ""
    return f"""<section class="phero mistbg"><div class="wrap grid">
<div><div class="crumbs"><a href="index.html">Home</a><span>/</span>{crumbs}</div>
<h1 class="h1 rv in">{lines(title)}</h1><p class="sub">{sub}</p><span class="kick" style="margin-top:22px">{kick}</span></div>
<div class="art rv in"><img src="{art}" alt="" fetchpriority="high">{tg}</div>
</div></section>"""

def cta(title="India’s platinum movement has started.", em="Let’s play.", prod="assets/banner/earring-hoop.webp"):
    return f"""<section class="sec-sm"><div class="wrap"><div class="ctabox royal rv">{sparkle(18)}
<div class="cta-copy"><span class="kick">Partner with Dishaa</span><h2 class="h1" style="margin-top:18px">{title} <em>{em}</em></h2>
<div class="ctas"><a class="btn btn-white" href="contact.html">Start your platinum journey {ARROW}</a><a class="btn btn-ghost" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_ICO} WhatsApp</a></div></div>
<div class="cta-art" aria-hidden="true"><span class="halo"></span><img src="{prod}" alt="" loading="lazy"></div>
</div></div></section>"""

def logos_marquee():
    vs = ["bn", "emerad", "hk", "jewelex", "kama", "novo", "oro", "ppt", "prism", "tankaria"]
    names = {"bn": "B N Jewellers", "emerad": "Emerald", "hk": "HK Jewels", "jewelex": "Jewelex", "kama": "Kama", "novo": "Novo Jewels", "oro": "ORO", "ppt": "Pure Platinum", "prism": "Prism Jewellery", "tankaria": "Tankaria"}
    items = "".join(f'<div class="item"><img src="assets/vendors/{v}.webp" alt="{names[v]}" loading="lazy"></div>' for v in vs)
    return f'<div class="marquee logos"><div class="track">{items}</div><div class="track" aria-hidden="true">{items}</div></div>'

def words(ws):
    it = "".join(f'<div class="item">{w}<span class="dia"></span></div>' for w in ws)
    return f'<div class="marquee words"><div class="track">{it}</div><div class="track" aria-hidden="true">{it}</div></div>'

def insta_wall():
    a = "".join(f'<figure data-full="assets/insta/c{k:02d}.webp"><img src="assets/insta/c{k:02d}.webp" alt="Dishaa Platinum creative" loading="lazy"></figure>' for k in range(1, 13))
    b = "".join(f'<figure data-full="assets/insta/c{k:02d}.webp"><img src="assets/insta/c{k:02d}.webp" alt="Dishaa Platinum creative" loading="lazy"></figure>' for k in range(13, 25))
    a2 = a.replace("<figure data-full", "<figure aria-hidden=\"true\" data-dup data-full")
    b2 = b.replace("<figure data-full", "<figure aria-hidden=\"true\" data-dup data-full")
    return f"""<div class="marquee insta"><div class="track">{a}</div><div class="track">{a2}</div></div>
<div class="marquee insta rev"><div class="track">{b}</div><div class="track">{b2}</div></div>"""

PLB = f'<div class="lb plb photo-only" role="dialog" aria-modal="true" aria-label="Image viewer"><button class="lb-x" aria-label="Close">&times;</button><div class="lb-stage photo"><img src="" alt=""><button class="lb-nav lb-prev" aria-label="Previous">{CHEV_L}</button><button class="lb-nav lb-next" aria-label="Next">{CHEV_R}</button></div></div>'

def count(col):
    return len([i for i in CAT.get(col, []) if not i.get("pgi")])

def films():
    return "".join(f'<div class="film rv d{k%3}"><video data-auto muted loop playsinline preload="none" poster="assets/video/men-{k}.jpg"><source src="assets/video/men-{k}.mp4" type="video/mp4"></video></div>' for k in range(1, 6))


# ------------------------------------------------------------------ hero banners (from Banner_1024 x 512.psd)
# (font, text, ink-left, baseline, font-size, scaleX)  in PSD units; desktop plates are 1024 wide, mobile 512.
JOST = dict(fam="j", base=0.84, inkl=0.08)
BOD = dict(fam="b", base=0.81, inkl=0.035)
BANNERS = [
  dict(n="01", href="collections.html", alt="Dishaa Platinum — Empowering retailers with India’s most trusted platinum collections",
       d=[(JOST, "Empowering Retailers with", 984, 338, 23, 1.0, "r"), (BOD, "India’s Most Trusted", 984, 377, 38, .97, "r"), (BOD, "Platinum Collections", 984, 414, 38, .96, "r")],
       m=[(JOST, "Empowering Retailers with", 22, 44, 18.6, 1.0), (BOD, "India’s Most Trusted", 22, 84, 32, 1.0), (BOD, "Platinum Collections", 22, 118, 32, 1.0)],
       cta=("Explore collections", "collections.html", 984, 430, "royal", "r")),
  dict(n="02", href="about.html", alt="India’s most preferred platinum partner",
       d=[(JOST, "India’s Most", 996, 166, 34.3, 1.03, "r"), (BOD, "Preferred", 996, 218, 51.7, .981, "r"), (BOD, "Platinum Partner", 996, 271, 51.7, .973, "r")],
       m=[(JOST, "India’s Most", 490, 44, 18.6, 1.0, "r"), (BOD, "Preferred", 490, 84, 32, 1.0, "r"), (BOD, "Platinum Partner", 490, 118, 32, 1.0, "r")],
       cta=("Why Dishaa", "about.html", 996, 298, "royal", "r")),
  dict(n="03", href="collections.html", alt="Select from the most famous platinum collections",
       d=[(JOST, "Select from the Most Famous", 621, 164, 30, 1.015, "", "#000"), (BOD, "Platinum", 621, 239, 72.3, .986, "", "#fff"), (BOD, "Collection", 705, 308, 72.3, .974, "", "#fff")],
       m=[(JOST, "Select from the Most Famous", 58, 68, 17, 1.0, "", "#000"), (BOD, "Platinum", 58, 112, 42, 1.0, "", "#fff"), (BOD, "Collection", 118, 156, 42, 1.0, "", "#fff")],
       cta=("View all six", "collections.html", 706, 330, "white"),
       logos_d=(46, 83, 447, 429), logos_m=(18, 196, 318, 455)),
]
LOGO_ORDER = ["evara", "men-of-platinum", "platinum-days-of-love", "bandhan", "farishtey", "pride-n-perfect"]

def banner_lines(lines, W, dy=0):
    u = 100 / W  # 1 PSD unit in cqw
    out = []
    for ln in lines:
        font, text, x, base, fs, sx = ln[:6]
        align = ln[6] if len(ln) > 6 else ""; col = ln[7] if len(ln) > 7 else ""
        top = (base + dy - font["base"] * fs) * u
        style = f"top:{top:.3f}cqw;font-size:{fs*u:.3f}cqw;"
        if align == "r":
            style += f"right:{(W - x) * u:.3f}cqw;transform:scaleX({sx});transform-origin:right;"
        else:
            style += f"left:{(x - font['inkl'] * fs * sx) * u:.3f}cqw;transform:scaleX({sx});"
        if col: style += f"color:{col};"
        out.append(f'<span class="ln {font["fam"]}" style="{style}">{text}</span>')
    return "".join(out)

def banner_logos(box, W):
    u = 100 / W; x0, y0, x1, y1 = box; cw, ch = (x1 - x0) / 2, (y1 - y0) / 3
    return "".join(f'<a class="hot" href="{s}.html" aria-label="{COLMAP[s]["name"]}" style="left:{(x0 + (k % 2) * cw) * u:.3f}cqw;top:{(y0 + (k // 2) * ch) * u:.3f}cqw;width:{cw * u:.3f}cqw;height:{ch * u:.3f}cqw"></a>' for k, s in enumerate(LOGO_ORDER))

def live_layers(n):
    """Animated product cut-outs placed at their exact PSD positions (art units -> cqw)."""
    p = os.path.join(ROOT, "assets", "hero", f"live{n}.json")
    if not os.path.exists(p):
        return ""
    boxes = json.load(open(p)); u = 100 / 1024; out = ""
    for key, (x0, y0, x1, y1) in boxes.items():
        img = f"assets/hero/{n}-{key}.webp"
        out += (f'<span class="pc pc-{key}" style="left:{x0*u:.3f}cqw;top:{y0*u:.3f}cqw;width:{(x1-x0)*u:.3f}cqw;'
                f'height:{(y1-y0)*u:.3f}cqw;--m:url({img})"><img src="{img}" alt="" fetchpriority="high"></span>')
    return f'<div class="live" aria-hidden="true">{out}</div>'

GLASS01 = f"""<div class="glass01">
<span class="g-kick">Dishaa · The Platinum Hub</span>
<p class="g-1">Empowering Retailers with</p>
<p class="g-2">India’s Most Trusted <em>Platinum Collections</em></p>
<p class="g-meta"><span>PGI certified</span><span>1000+ jewellers</span><span>25+ years</span></p>
<div class="g-ctas"><a class="g-btn" href="collections.html">Explore collections {ARROW}</a><a class="g-link" href="partner.html">Become a partner</a></div>
</div>"""

PAUSE_ICO = '<svg class="i-pause" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M4 2v10M10 2v10" stroke="currentColor" stroke-width="2"/></svg><svg class="i-play" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M4 2l8 5-8 5Z" fill="currentColor"/></svg>'
ED_PANELS = [
  ("evara", "assets/spotlight/p-evara.webp", "34% 18%", "Elegance that sells."),
  ("men-of-platinum", "assets/spotlight/p-mop.webp", "44% 14%", "Rare character, rare platinum."),
  ("platinum-days-of-love", "assets/spotlight/p-pdol.webp", "50% 20%", "For a love so rare."),
  ("collections", "assets/lookbook/ph10.webp", "50% 50%", "700+ designs, ready for your counter."),
]
def editorial_slide():
    """Hero slide 1: the collection faces in auto-expanding panels + the photoshoot, with the brand promise."""
    panels = ""
    for k, (slug, img, pos, tag) in enumerate(ED_PANELS):
        if slug == "collections":
            name, logo, href = "The Platinum Hub", "", "collections.html"
            mark = '<b class="ep-name">The Platinum Hub</b>'
        else:
            c = COLMAP[slug]; name, href = c["name"], f"{slug}.html"
            mark = f'<img class="ep-logo" src="{c["logo"]}" alt="{name}">'
        panels += f"""<a class="ep{' on' if k == 0 else ''}" href="{href}" data-i="{k}" style="--op:{pos}"><img class="ep-im" src="{img}" alt="{name}" {'fetchpriority="high"' if k == 0 else ''}>
<span class="ep-bar" aria-hidden="true"></span><span class="ep-v">{name}</span>
<div class="ep-info">{mark}<p>{tag}</p><span class="ep-go">Explore {ARROW}</span></div></a>"""
    return f"""<div class="slide s01 ed on" data-dur="12000">
<div class="ed-bg" aria-hidden="true"></div>{sparkle(26)}
<span class="shine" aria-hidden="true"></span>
<div class="ed-in">
<div class="ed-copy"><span class="g-kick">Dishaa · The Platinum Hub</span>
<p class="ed-1">Empowering Retailers with</p>
<p class="ed-h g-2">India’s Most Trusted <em>Platinum Collections</em></p>
<p class="g-meta"><span>PGI certified</span><span>1000+ jewellers</span><span>25+ years</span></p>
<div class="g-ctas"><a class="g-btn" href="collections.html">Explore collections {ARROW}</a><a class="g-link" href="partner.html">Become a partner</a></div></div>
<div class="ed-panels" data-depth="-6">{panels}</div>
</div></div>"""

# city positions on the India map of plate x02 (art units, 1024 x 512)
CITIES = [("Mumbai", 100, 196, "hq"), ("Delhi", 148, 90, ""), ("Jaipur", 124, 112, ""), ("Ahmedabad", 92, 152, ""),
          ("Lucknow", 186, 110, ""), ("Kolkata", 252, 150, ""), ("Hyderabad", 160, 214, ""), ("Pune", 114, 206, ""),
          ("Bengaluru", 148, 256, ""), ("Chennai", 178, 256, ""), ("Kochi", 138, 286, ""), ("Indore", 130, 156, "")]

def netmap():
    """Slide 2: glowing links from the Mumbai hub to cities across India (drawn on slide entry)."""
    hx, hy = CITIES[0][1], CITIES[0][2]
    paths = ""
    for k, (name, x, y, _) in enumerate(CITIES[1:]):
        mx, my = (hx + x) / 2, (hy + y) / 2 - 26
        paths += f'<path d="M{hx} {hy} Q{mx:.0f} {my:.0f} {x} {y}" style="--d:{0.35 + k * 0.09:.2f}s"/>'
    dots = "".join(f'<g class="city {c}" style="--d:{0.5 + k * 0.09:.2f}s"><circle class="ring" cx="{x}" cy="{y}" r="7"/><circle class="dot" cx="{x}" cy="{y}" r="{4.2 if c else 2.8}"/></g>' for k, (n, x, y, c) in enumerate(CITIES))
    return (f'<div class="tx net" aria-hidden="true"><svg viewBox="0 0 1024 512" preserveAspectRatio="none">'
            f'<g class="links">{paths}</g>{dots}<text x="{hx - 12}" y="{hy + 4}" text-anchor="end">MUMBAI HUB</text></svg></div>')

BSTATS = [(1000, "+", "Jewellers"), (25, "+", "Years"), (200, "+", "Cities")]
def bstats():
    it = "".join(f'<div><b data-n="{n}" data-s="{sfx}">{n}{sfx}</b><span>{t}</span></div>' for n, sfx, t in BSTATS)
    u = 100 / 1024
    return f'<div class="bstats" style="right:{28 * u:.3f}cqw;top:{352 * u:.3f}cqw">{it}</div>'

def collections_slide(active=False):
    """Slide 3: six collections, one signature piece at a time on a halo stage; logos light up in turn."""
    stage, tiles = "", ""
    order = ["evara", "men-of-platinum", "platinum-days-of-love", "bandhan", "farishtey", "pride-n-perfect"]
    for k, slug in enumerate(order):
        c = COLMAP[slug]
        img = c["hero"] or c["photo"]
        cls = "cut" if c["hero"] else "photo"
        stage += f'<a class="cs-item {cls}{" on" if k == 0 else ""}" href="{slug}.html" data-i="{k}"><img src="{img}" alt="{c["name"]}" loading="lazy"></a>'
        tiles += f'<a class="cs-tile{" on" if k == 0 else ""}" href="{slug}.html" data-i="{k}" aria-label="{c["name"]}"><img src="{c["logo"]}" alt="{c["name"]}" loading="lazy"><i></i></a>'
    names = "".join(f'<div class="cs-name{" on" if k == 0 else ""}" data-i="{k}"><b>{COLMAP[s]["name"]}</b><span>{COLMAP[s]["tag"]}</span></div>' for k, s in enumerate(order))
    return f"""<div class="slide s03 cs{' on' if active else ''}" data-dur="13000">
<div class="cs-bg" aria-hidden="true"></div>{sparkle(22)}
<span class="shine" aria-hidden="true"></span>
<div class="cs-in">
<div class="cs-copy"><span class="g-kick">One brand · six collections</span>
<p class="ed-1">Select from the Most Famous</p>
<p class="ed-h g-2">Platinum <em>Collections</em></p>
<div class="g-ctas"><a class="g-btn" href="collections.html">View all collections {ARROW}</a></div></div>
<div class="cs-stage"><span class="cs-halo" aria-hidden="true"></span><span class="cs-orbit" aria-hidden="true"></span>{stage}<div class="cs-names">{names}</div></div>
<div class="cs-tiles">{tiles}</div>
</div></div>"""

def hero_banners():
    slides = ""
    for i, b in enumerate(BANNERS):
        n = b["n"]
        if n == "01":
            slides += editorial_slide(); continue
        if n == "03":
            slides += collections_slide(); continue
        t, href, cx, cy, kind = b["cta"][:5]
        u = 100 / 1024
        pos = f"right:{(1024-cx)*u:.3f}cqw" if len(b["cta"]) > 5 else f"left:{cx*u:.3f}cqw"
        cta = f'<a class="bcta {kind}" href="{href}" style="{pos};top:{cy*u:.3f}cqw">{t} {ARROW}</a>'
        logos = ""
        if "logos_d" in b:
            logos = f'<div class="tx d">{banner_logos(b["logos_d"], 1024)}</div><div class="tx m">{banner_logos(b["logos_m"], 512)}</div>'
        live = live_layers(n) if n == "01" else ""
        plate = f"x{n}bg" if live else f"x{n}"
        dcopy = GLASS01 if n == "01" else f"{banner_lines(b['d'], 1024)}{cta}" + (bstats() if n == "02" else "")
        slides += f"""<div class="slide s{n}{' on' if i == 0 else ''}{' is-live' if live else ''}">
<a class="blink" href="{b['href']}" aria-label="{E(b['alt'])}"><picture><source media="(max-width:760px)" srcset="assets/hero/m{n}.webp"><img class="plate" src="assets/hero/{plate}.webp" alt="{E(b['alt'])}" {'fetchpriority="high"' if i == 0 else 'loading="lazy"'}></picture></a>
{sparkle(30) if live else ""}
<span class="shine" aria-hidden="true"></span>
<div class="art" data-depth="-10">{live}{netmap() if n == "02" else ""}<div class="tx d">{dcopy}</div>
<div class="tx m" aria-hidden="true">{banner_lines(b['m'], 512)}</div>{logos}</div>
</div>"""
    return f"""<section class="bnr" aria-label="Featured">
<div class="bnr-frame">{slides}
<div class="art art-ui"><div class="bnr-ui"><div class="hero-dots"><button aria-label="Banner 1"><i>01</i><span>The Platinum Hub</span></button><button aria-label="Banner 2"><i>02</i><span>Preferred partner</span></button><button aria-label="Banner 3"><i>03</i><span>Six collections</span></button></div>
<div class="hero-arrows"><button data-prev aria-label="Previous banner">{CHEV_L}</button><button data-next aria-label="Next banner">{CHEV_R}</button></div></div></div>
</div></section>"""


# ------------------------------------------------------------------ spotlight banners (PGI BANNERS FOR WEBSITE)
SPOTS = [
  dict(slug="evara", img="evara", tag="New collection", alt="Discover the new collection from Platinum Evara and Dishaa"),
  dict(slug="men-of-platinum", img="mop", tag="Rare character, rare platinum", alt="Men of Platinum: rare character, rare platinum"),
  dict(slug="platinum-days-of-love", img="pdol", tag="For a love so rare", alt="Platinum Love Bands: for a love so rare, a love so platinum"),
]
SPOTMAP = {c["slug"]: c for c in SPOTS}

def camp_pic(c, eager=False):
    ld = "" if eager else ' loading="lazy"'
    return (f'<picture><source media="(max-width:640px)" srcset="assets/spotlight/{c["img"]}-m.webp">'
            f'<img src="assets/spotlight/{c["img"]}-d.webp" alt="{c["alt"]}" width="960" height="540"{ld}></picture>')

def spotlight():
    """Home: stacked deck of the three collection spotlights (animated with anime.js in site.js)."""
    cards = "".join(f"""<a class="dk-card{' on' if k == 0 else ''}" href="{c["slug"]}.html" data-i="{k}">{camp_pic(c)}
<span class="dk-cta">{COLMAP[c["slug"]]["name"]} {ARROW}</span></a>""" for k, c in enumerate(SPOTS))
    tabs = "".join(f'<button class="dk-tab{" on" if k == 0 else ""}" data-i="{k}"><img src="{COLMAP[c["slug"]]["logo"]}" alt="{COLMAP[c["slug"]]["name"]}"><small>{c["tag"]}</small></button>' for k, c in enumerate(SPOTS))
    return f"""<section class="sec spot">{sparkle(16)}<div class="wrap">
<div class="head"><div><span class="kick">In the spotlight</span><h2 class="h2 rv">This season’s <em>platinum stories.</em></h2></div><a class="btn btn-line rv" href="collections.html">All collections {ARROW}</a></div>
<div class="deck rv"><div class="dk-stage">{cards}</div>
<div class="dk-side"><div class="dk-tabs">{tabs}</div>
<div class="dk-ctrl"><button data-dk-prev aria-label="Previous story">{CHEV_L}</button><button class="hp" data-dk-pause aria-label="Pause stories">{PAUSE_ICO}</button><span class="dk-count"><b>01</b> / 0{len(SPOTS)}</span><button data-dk-next aria-label="Next story">{CHEV_R}</button></div></div></div>
</div></section>"""

def pgi_band():
    return f"""<section class="sec-sm pgiband"><div class="wrap"><a class="pgi-strip rv" href="why-platinum.html" aria-label="Platinum is the fastest growing jewellery category today — why platinum">
<img src="assets/spotlight/dishaa-pgi.webp" alt="Platinum is the fastest growing jewellery category today — Platinum and Dishaa, The Platinum Hub" width="1300" height="400" loading="lazy">
<span class="pgi-go">Why platinum {ARROW}</span></a></div></section>"""

def camp_strip(slug):
    c = SPOTMAP.get(slug)
    if not c: return ""
    return f'<section class="sec-sm campstrip"><div class="wrap"><div class="camp-frame rv">{camp_pic(c)}</div></div></section>'


# ------------------------------------------------------------------ v5 showpieces (21st.dev-inspired, native HTML)
SHOW_BG = {"men-of-platinum": "assets/banner/bg-room.webp", "evara": "assets/banner/bg-flowers.webp",
           "platinum-days-of-love": "assets/banner/bg-podium.webp", "bandhan": "assets/banner/bg-flowers.webp",
           "farishtey": "assets/banner/bg-room.webp", "pride-n-perfect": "assets/props/sha00318.webp"}

def showcase():
    """Lumina-style interactive stage: one collection at a time, numbered list navigation."""
    stages, nav = "", ""
    for k, c in enumerate(COLS):
        n = count(c["slug"])
        prod = f'<img class="sc-prod" src="{c["hero"]}" alt="{c["name"]} signature piece" loading="lazy">' if c["hero"] else ""
        photo = " photo" if not c["hero"] else ""
        stages += f"""<a class="sc-stage{photo}{' on' if k == 0 else ''}" href="{c["slug"]}.html" data-i="{k}">
<img class="sc-bg" src="{SHOW_BG[c["slug"]]}" alt="" loading="lazy">{prod}
<div class="sc-copy"><img class="sc-logo" src="{c["logo"]}" alt="{c["name"]}"><p>{c["line"]}</p>
<span class="sc-cta">{f"Explore {n} designs" if n else "Explore the collection"} {ARROW}</span></div></a>"""
        nav += f'<button class="sc-tab{" on" if k == 0 else ""}" data-i="{k}" aria-label="Show {c["name"]}"><i>0{k+1}</i><span>{c["name"]}</span></button>'
    return f"""<section class="sec showcase-sec"><div class="wrap">
<div class="head"><div><span class="kick">Our collections</span><h2 class="h2 rv">Six collections. <em>One hub.</em></h2></div><a class="btn btn-line rv" href="collections.html">View all {ARROW}</a></div>
<div class="showcase rv">{stages}<div class="sc-nav" role="tablist">{nav}</div><div class="sc-bar"><i></i></div></div>
</div></section>"""

def impact_bento(total):
    return f"""<section class="sec lavbg"><div class="wrap">
<div class="center" style="margin-bottom:clamp(24px,3vw,40px)"><span class="kick">Welcome to Dishaa Platinum Hub</span><h2 class="h2 rv" style="margin-top:12px">Not just a supplier. <em>Your platinum partner.</em></h2></div>
<div class="bento">
<div class="bx bx-hero rv"><img src="assets/lookbook/ph10.webp" alt="Platinum necklace on steel-blue paper" loading="lazy">
<div><span class="pill-tag">India’s biggest stockist</span><h3>Certified platinum,<br><em>ready to sell.</em></h3><p>PGI-certified jewellery from India’s top manufacturers, in ready stock for your counter.</p></div></div>
<div class="bx bx-stat royal rv d1">{sparkle(8)}<b data-count="25" data-suffix="+">25+</b><span>Years of collective experience</span></div>
<div class="bx bx-stat sky rv d2"><b data-count="1000" data-suffix="+">1000+</b><span>Jewellers trust Dishaa</span></div>
<div class="bx bx-stat pink rv d1"><b data-count="{total}" data-suffix="+">{total}+</b><span>Designs to browse online</span></div>
<div class="bx bx-stat deep rv d2"><b>100%</b><span>On-time delivery</span></div>
<a class="bx bx-cta rv d3" href="partner.html"><span class="pill-tag light">Partner programme</span><h3>Become a Dishaa partner</h3><span class="go">{ARROW_UR}</span></a>
</div></div></section>"""

def why_bento():
    t = [
      ("b big", "We don’t sell trends.", "We set them", "assets/banner/bracelet-cable.webp"),
      ("l", "Zero delay.", "100% on-time delivery", "assets/banner/pendant-leaf.webp"),
      ("sky", "We know platinum.", "From production to profit", "assets/banner/ring-topaz.webp"),
      ("pink", "From concepts to counter.", "We master the art", "assets/banner/earring-hoop.webp"),
      ("b", "Every gram, every order.", "Crafted with clarity", "assets/banner/ring-sunburst.webp"),
      ("l wide", "Oldest in the game.", "Fastest in the field", "assets/banner/ring-trillion.webp"),
    ]
    tl = "".join(f'<div class="tile {c} rv d{k%3}"><h3>{h}</h3><small>{sub}</small><img src="{im}" alt="" loading="lazy"></div>' for k, (c, h, sub, im) in enumerate(t))
    return f"""<section class="sec"><div class="wrap">
<div class="head"><div><span class="kick">Why jewellers choose Dishaa</span><h2 class="h2 rv">Not just a brand. A <em>platinum powerhouse.</em></h2></div></div>
<div class="tiles bento-tiles">{tl}</div></div></section>"""

# ================================================================== SHOP BY (men / women / kids / couples)
def aud_count(a):
    return sum(count(c) for c in a["cols"])

def shop_by():
    """Home: four doors — Men, Women, Kids, Couples."""
    t = "".join(f"""<a class="door rv d{k}" href="explore.html#{a["key"]}"><img src="{a["img"]}" alt="Platinum jewellery for {a["name"].lower()}" loading="lazy" style="object-position:{a["pos"]}">
<div class="door-tx"><span class="door-n">{aud_count(a)} designs</span><h3>{a["name"]}</h3><p>{a["line"]}</p><span class="door-go">Shop {a["name"].lower()} {ARROW}</span></div></a>""" for k, a in enumerate(AUD))
    return f"""<section class="sec shopby"><div class="wrap">
<div class="head"><div><span class="kick">Shop by</span><h2 class="h2 rv">For him, for her, <em>for the little ones.</em></h2></div><a class="btn btn-line rv" href="explore.html">Browse all designs {ARROW}</a></div>
<div class="doors">{t}</div></div></section>"""

def explore():
    items = []
    for c in COLS:
        for it in CAT.get(c["slug"], []):
            if not it.get("pgi"): items.append((it, c))
    cats = []
    for it, _ in items:
        if it["cat"] not in cats: cats.append(it["cat"])
    chips = f'<button class="chip on" data-cat="all">All<i>{len(items)}</i></button>' + "".join(
        f'<button class="chip" data-cat="{E(k)}">{E(k)}<i>{sum(1 for x, _ in items if x["cat"] == k)}</i></button>' for k in cats)
    allline = "Every Dishaa design in one place: men, women, kids and couples."
    btns = f'<button class="audb on" data-aud-btn="all" data-line="{E(allline)}" aria-pressed="true"><span class="ai all">{icon("range")}</span><b>All</b><i>{len(items)}</i></button>'
    btns += "".join(f'<button class="audb" data-aud-btn="{a["key"]}" data-line="{E(a["line"])}" aria-pressed="false"><span class="ai"><img src="{a["img"]}" alt="" style="object-position:{a["pos"]}"></span><b>{a["name"]}</b><i>{aud_count(a)}</i></button>' for a in AUD)
    cards = ""
    for it, c in items:
        code = re.sub(r"-{2,}", " / ", it["code"]).replace("_", "-"); views = it["views"]
        alt = f'<img class="alt" src="{views[1]}" alt="" loading="lazy">' if len(views) > 1 else ""
        vtag = f'<span class="views">{len(views)} views</span>' if len(views) > 1 else ""
        cards += f"""<article class="pcard" tabindex="0" data-aud="{AUDOF[c['slug']]}" data-code="{E(code)}" data-cat="{E(it['cat'])}" data-catlabel="{E(it['cat'])}" data-col="{E(c['name'])}" data-views='{json.dumps(views)}'>
<div class="im">{alt}<img class="main{' hasalt' if alt else ''}" src="{views[0]}" alt="{E(c['name'])} {E(it['cat'])} {E(code)}" loading="lazy"></div>{vtag}
<button class="add" aria-label="Add {E(code)} to selection tray">{PLUS}</button>
<div class="info"><b>{E(code)}</b><span>{E(it['cat'])}</span></div></article>"""
    looks = ""
    mix = {"men": [0, 1, 2], "women": [0, 1, 2], "kids": [0], "couples": [0, 1]}
    for a in AUD:
        for k, l in enumerate(a["looks"]):
            all_ = " data-look-all" if k in mix[a["key"]] else ""
            looks += f'<figure data-look="{a["key"]}"{all_} data-full="assets/{l}.webp"><img src="assets/{l}.webp" alt="Platinum jewellery for {a["name"].lower()}" loading="lazy"></figure>'
    body = phero("Men · Women · Kids · Couples", "Find the right|<em>platinum look.</em>",
                 "Browse every design by who it’s for, then by category. Shortlist and send the list in one go.",
                 "assets/studio/st09.webp", "<span>Shop by</span>") + f"""
<div class="filters explore-f" id="designs"><div class="wrap audbar" role="group" aria-label="Shop by">{btns}</div><div class="wrap">{chips}</div></div>
<section class="sec-sm" style="padding-top:26px"><div class="wrap">
<div class="looks-head"><span class="kick">Get the look</span><p class="aud-line">{allline}</p></div>
<div class="looks">{looks}</div>
<div class="pgrid" style="margin-top:clamp(24px,3vw,40px)">{cards}</div>
<div class="more-wrap"><button class="btn btn-line" data-more>Load more designs</button></div>
<p class="center" style="color:var(--muted);font-size:14px;margin-top:26px">Tap <b>+</b> to shortlist designs and send the list in one go.</p>
</div></section>
{LB}{PLB}
{cta("Something for every", "customer who walks in.", "assets/banner/ring-sunburst.webp")}"""
    page("explore.html", "Shop Platinum Jewellery for Men, Women, Kids & Couples | Dishaa Platinum",
         "Browse Dishaa platinum jewellery by who it is for: men, women, kids and couples, then by category.", body, active="collections")

# ================================================================== HOME
def home():
    total = sum(count(c) for c in CAT)
    logos6 = "".join(f'<a href="{c["slug"]}.html" style="--i:{k}"><img src="{c["logo"]}" alt="{c["name"]}"></a>' for k, c in enumerate(COLS))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3"><animate attributeName="opacity" values=".2;1;.2" dur="{d}s" repeatCount="indefinite"/></circle>' for x, y, d in [(300, 90, 2.4), (330, 170, 3), (260, 330, 2.8), (60, 330, 3.4), (120, 60, 2.2), (172, 158, 2.6), (210, 220, 3.1)])
    hero = hero_banners()

    ribbon = "".join(f'<a class="rv d{k%4}" href="{c["slug"]}.html"><img src="{c["logo"]}" alt="{c["name"]}" loading="lazy"></a>' for k, c in enumerate(COLS))
    cls = {"men-of-platinum": "blue", "platinum-days-of-love": "", "evara": "", "bandhan": "", "farishtey": "blue", "pride-n-perfect": "photo"}
    cards = ""
    for k, c in enumerate(COLS):
        n = count(c["slug"])
        cnt = f'<span class="cnt">{n} designs</span>' if n else '<span class="cnt">Couple sets</span>'
        if c["hero"]:
            art = f'<div class="plinth"><img src="{c["hero"]}" alt="{c["name"]} platinum jewellery" loading="lazy"></div>'
        else:
            art = f'<img class="bgp" src="{c["photo"]}" alt="{c["name"]} couple set" loading="lazy"><div class="plinth"></div>'
        cards += f"""<a class="ccard {cls[c['slug']]} rv d{k%3}" href="{c["slug"]}.html">{cnt}<div class="lg"><img src="{c["logo"]}" alt="{c["name"]}" loading="lazy"></div>{art}
<div class="meta"><p>{c["tag"]}</p><span class="go">{ARROW_UR}</span></div></a>"""
    tiles = [
      ("b", "We don’t sell trends.", "We set them", "assets/banner/bracelet-cable.webp"),
      ("l", "Zero delay.", "100% on-time delivery", "assets/banner/pendant-leaf.webp"),
      ("b", "We know platinum.", "From production to profit", "assets/banner/ring-topaz.webp"),
      ("l", "From concepts to counter.", "We master the art", "assets/banner/earring-hoop.webp"),
      ("b", "Every gram, every order.", "Crafted with clarity", "assets/banner/ring-sunburst.webp"),
      ("l", "Oldest in the game.", "Fastest in the field", "assets/banner/ring-trillion.webp"),
    ]
    tl = "".join(f'<div class="tile {t} rv d{k%3}"><h3>{h}</h3><small>{s}</small><img src="{im}" alt="" loading="lazy"></div>' for k, (t, h, s, im) in enumerate(tiles))
    support = [("pgi", "PGI partner plan"), ("training", "Staff training"), ("branding", "360° branding"), ("display", "Display &amp; counters"), ("fast", "Ready stock"), ("buyback", "Best buyback")]
    ch = "".join(f'<div class="chipc rv d{k%4}">{icon(i)}<span>{t}</span></div>' for k, (i, t) in enumerate(support))
    compass_ticks = "".join(f'<line x1="100" y1="6" x2="100" y2="{16 if k%2==0 else 11}" stroke="rgba(255,255,255,.6)" transform="rotate({k*22.5} 100 100)"/>' for k in range(16))
    body = '<h1 class="sr">Dishaa Platinum — India’s most trusted platinum jewellery wholesaler for retail jewellers</h1>' + hero + f"""
{words(["Couple Bands", "Chains", "Kadas", "Bracelets", "Pendants", "Mangalsutras", "Earrings", "Cufflinks", "Watch Straps"])}
{shop_by()}

{impact_bento(total)}

{showcase()}

{why_bento()}
<section class="sec mistbg"><div class="wrap">
<div class="head"><div><span class="kick">Turning potential into performance</span><h2 class="h2 rv">Everything you need to <em>grow platinum.</em></h2></div><a class="btn btn-royal rv" href="partner.html">Partner benefits {ARROW}</a></div>
<div class="chips">{ch}</div></div></section>

<section class="sec" style="overflow:hidden"><div class="wrap">
<div class="head"><div><span class="kick">Men of Platinum</span><h2 class="h2 rv">Serious about platinum? <em>Talk to the pros.</em></h2></div><a class="link rv" href="men-of-platinum.html">Shop the men’s edit {ARROW}</a></div>
<div class="films">{films()}</div></div></section>

<section class="sec-sm lavbg" style="overflow:hidden"><div class="wrap head" style="margin-bottom:34px"><div><span class="kick">From our feed</span><h2 class="h2 rv">Zaveri Bazaar just got a <em>platinum upgrade.</em></h2></div></div>
{insta_wall()}</section>

<section class="sec-sm"><div class="wrap center" style="margin-bottom:26px"><span class="kick">Partnered with India’s top manufacturers</span></div>{logos_marquee()}</section>

{cta()}
{PLB}"""
    page("index.html", "Dishaa Platinum — India’s Most Trusted Platinum Jewellery Partner",
         "Dishaa Platinum, The Platinum Hub: India’s biggest stockist of PGI-certified platinum jewellery. Men of Platinum, Evara, PDOL, Bandhan, Farishtey & Pride N Perfect for retail jewellers.", body)

# ================================================================== ABOUT
def about():
    values = [("Trust", "trust"), ("Innovation", "innovation"), ("Quality", "quality"), ("Commitment", "commitment"),
              ("Support", "support"), ("Growth", "growth"), ("Exclusivity", "exclusivity"), ("Reliability", "reliability")]
    vals = "".join(f'<div class="val rv d{k%4}">{icon(ic)}<b>{t}</b></div>' for k, (t, ic) in enumerate(values))
    usps = [("range", "Widest range &amp; huge inventory"), ("innovation", "Innovative designs"), ("reliability", "25 years of collective experience"),
            ("chat", "Systematic · smooth · straightforward"), ("quality", "No-compromise QC"), ("box", "Every category"),
            ("tech", "Latest technology"), ("trust", "Trusted by 1000+ jewellers"), ("exclusivity", "Creative craftsmanship"),
            ("pgi", "Top manufacturers, partnered"), ("men", "Men’s specialists"), ("custom", "Customised for every occasion")]
    usp = "".join(f'<div class="chipc rv d{k%4}">{icon(ic)}<span>{t}</span></div>' for k, (ic, t) in enumerate(usps))
    pillars = [
      ("Widest range", "range", ["Couple bands, chains, bracelets, kadas", "Cufflinks, belts, brooches, watch straps", "Customised for every occasion"]),
      ("Years of excellence", "reliability", ["25+ years of collective experience", "Authorised PGI dealer", "Advanced manufacturing technology"]),
      ("Quality products", "quality", ["Platinum Guild certified", "India’s top manufacturers", "Rigorous QC on every piece"]),
      ("Trusted by 1000+", "trust", ["Consistent product quality", "Transparent business practices", "Unparalleled service"]),
    ]
    pl = "".join(f'<div class="card rv d{k}">{icon(ic)}<h3>{t}</h3><ul class="bullets" style="font-size:15px;color:var(--muted)">{"".join(f"<li>{b}</li>" for b in bl)}</ul></div>' for k, (t, ic, bl) in enumerate(pillars))
    body = phero("Mumbai · India · International", "Built on legacy.|<em>Driven by platinum.</em>",
                 "A renowned platinum jewellery wholesaler and manufacturer in Mumbai, trusted by 1000+ retail jewellers across India and abroad.",
                 "assets/insta/c18.webp", "<span>About</span>") + f"""
<section class="sec"><div class="wrap split">
<div class="frame d ar45 rv"><img src="assets/props/sha00313.webp" alt="Two-tone platinum couple bands" loading="lazy"></div>
<div><span class="kick">About us</span><h2 class="h2 rv" style="margin:16px 0 22px">Innovation and quality are <em>our roots.</em></h2>
<p class="sub rv">We create and craft exclusive platinum jewellery for jewellers across India and internationally. We see platinum as a pure and precious partner in growth, rare and eternal.</p>
<p class="quote rv" style="font-size:clamp(20px,1.8vw,25px);margin-top:26px">“Platinum is the perfect and precious metal for life. We go above and beyond every day to take it to every corner of the country.”</p></div>
</div></section>

<section class="sec-sm"><div class="wrap vm">
<div class="rv"><img src="assets/lookbook/phe3.webp" alt="" loading="lazy"><span class="kick">Our vision</span><h3>India’s biggest &amp; most trusted platinum jewellery partner.</h3></div>
<div class="rv d1"><img src="assets/lookbook/ph14.webp" alt="" loading="lazy"><span class="kick">Our mission</span><h3>A benchmark for classic platinum creations, and the best service to jewellers worldwide.</h3></div>
</div></section>

<section class="sec mistbg"><div class="wrap center"><span class="kick">What we stand for</span><h2 class="h2 rv" style="margin:14px auto 44px">Innovation is routine. <em>Excellence is standard.</em></h2>
<div class="values">{vals}</div></div></section>

<section class="sec royal">{sparkle(24)}<div class="wrap split">
<div class="rv"><span class="kick">Director’s message</span>
<p class="quote" style="margin-top:22px">“The next-generation metal is in demand across every state of India. We serve jewellers anything to everything they need in platinum, and train their teams to grow it.”</p>
<p class="hinglish" style="margin-top:24px">Team Dishaa is at your service — <span class="rosegold">aapke saath hai hum.</span></p>
<p style="margin-top:20px;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#cfd0f0">— Director, Dishaa Platinum</p></div>
<div class="frame d ar45 rv d1" style="background:#fff;display:grid;place-items:center"><img src="assets/brand/dishaa-lockup.png" alt="Dishaa Platinum" style="width:56%;height:auto;object-fit:contain"></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="head"><div><span class="kick">The Dishaa difference</span><h2 class="h2 rv">Your preferred <em>platinum partner.</em></h2></div></div>
<div class="cards">{pl}</div></div></section>

<section class="sec-sm lavbg"><div class="wrap">
<div class="head"><div><span class="kick">Our USPs</span><h2 class="h2 rv">Twelve reasons to <em>choose Dishaa.</em></h2></div></div>
<div class="chips">{usp}</div></div></section>

<section class="sec"><div class="wrap">
<div class="head"><div><span class="kick">Making it happen</span><h2 class="h2 rv">Branding. Display. <em>Training.</em></h2></div></div>
<div class="acc-grid">
<div class="acc rv"><img src="assets/support/creatives.webp" alt="Platinum brand creatives" loading="lazy"><div><h3>Branding</h3><p>A distinct identity, premium marketing, strong digital presence.</p></div></div>
<div class="acc rv d1"><img src="assets/display/fixture-1.webp" alt="Platinum display counter" loading="lazy"><div><h3>Display</h3><p>Visual merchandising that shows platinum at its best.</p></div></div>
<div class="acc rv d2"><img src="assets/support/training.webp" alt="Sales staff training" loading="lazy"><div><h3>Training</h3><p>Product expertise and selling skills for your team.</p></div></div>
</div></div></section>
{cta("Your growth is our", "platinum mission.", "assets/banner/ring-leaf.webp")}"""
    page("about.html", "About Dishaa Platinum — The Platinum Hub, Mumbai",
         "Dishaa Platinum, The Platinum Hub: a Mumbai platinum jewellery wholesaler and manufacturer with 25+ years of collective experience, trusted by 1000+ jewellers.", body)

# ================================================================== COLLECTIONS OVERVIEW
def collections():
    rows = ""
    for i, c in enumerate(COLS):
        n = count(c["slug"])
        cats = sorted({x["cat"] for x in CAT.get(c["slug"], []) if not x.get("pgi")})
        tags = "".join(f"<span>{t}</span>" for t in cats) or "<span>Couple sets</span><span>Wedding</span><span>Gifting</span>"
        if c["hero"]:
            art = f'<div class="frame d ar43" style="background:var(--grad-mist)"><img src="{c["bg"]}" alt="" loading="lazy" style="position:absolute;inset:0"><img src="{c["hero"]}" alt="{c["name"]}" loading="lazy" style="position:absolute;left:50%;bottom:14%;width:42%;height:auto;translate:-50% 0;object-fit:contain;filter:drop-shadow(0 26px 24px rgba(34,40,110,.3))"></div>'
        else:
            art = f'<div class="frame d ar43"><img src="{c["photo"]}" alt="{c["name"]}" loading="lazy"></div>'
        order = 'style="order:2"' if i % 2 else ""
        rows += f"""<div class="split rv" style="padding:clamp(34px,5vw,70px) 0">
<div {order}>{art}</div>
<div><img src="{c["logo"]}" alt="{c["name"]}" style="height:clamp(70px,7vw,100px);width:auto;max-width:80%;object-fit:contain" loading="lazy">
<p class="quote" style="margin:22px 0 18px">{c["tag"]}</p>
<div class="tagrow" style="margin-bottom:26px">{tags}</div>
<a class="btn btn-royal" href="{c["slug"]}.html">{f"Explore {n} designs" if n else "Explore"} {ARROW}</a></div></div>"""
    body = phero("Men · Women · Couples · Brides · Kids", "One brand.|Six collections.|<em>The best selection.</em>",
                 "Plus platinum accessories and bars &amp; coins, all from one hub.", "assets/insta/c05.webp", "<span>Collections</span>") + f"""
{showcase()}
<section class="sec" style="padding-top:0"><div class="wrap">{rows}</div></section>
<section class="sec-sm lavbg"><div class="wrap"><div class="acc-grid">
<a class="acc rv" href="accessories.html"><img src="assets/props/sha00151.webp" alt="Platinum cufflinks" loading="lazy"><div><h3>Accessories</h3><p>Cufflinks, watch straps, specks &amp; more</p></div></a>
<a class="acc rv d1" href="d-the-platinum.html"><img src="assets/dthe/dthe-5.webp" alt="D The Platinum bars" loading="lazy"><div><h3>D — The Platinum</h3><p>Platinum bars &amp; coins</p></div></a>
<a class="acc rv d2" href="lookbook.html"><img src="assets/lookbook/phe1.webp" alt="Platinum earrings" loading="lazy"><div><h3>Lookbook</h3><p>Our jewellery, photographed</p></div></a>
</div></div></section>
{cta()}"""
    page("collections.html", "Platinum Jewellery Collections — Dishaa Platinum",
         "Men of Platinum, Evara, Platinum Days of Love, Bandhan, Farishtey and Pride N Perfect: India’s most famous platinum collections.", body, active="collections")

# ================================================================== COLLECTION PAGES
def product_cards(slug):
    items = CAT.get(slug, [])
    order = [i for i in items if not i.get("pgi")] + [i for i in items if i.get("pgi")]
    c = COLMAP[slug]
    out = []
    for it in order:
        code = re.sub(r"-{2,}", " / ", it["code"]).replace("_", "-")
        views = it["views"]
        alt = f'<img class="alt" src="{views[1]}" alt="" loading="lazy">' if len(views) > 1 and not it.get("pgi") else ""
        cls = "pcard pgi" if it.get("pgi") else "pcard"
        vtag = f'<span class="views">{len(views)} views</span>' if len(views) > 1 else ""
        out.append(f"""<article class="{cls}" tabindex="0" data-aud="{AUDOF.get(slug, '')}" data-code="{E(code)}" data-cat="{E(it['cat'])}" data-catlabel="{E(it['cat'])}" data-col="{E(c['name'])}" data-views='{json.dumps(views)}'>
<div class="im">{alt}<img class="main{' hasalt' if alt else ''}" src="{views[0]}" alt="{E(c['name'])} {E(it['cat'])} {E(code)}" loading="lazy"></div>{vtag}
<button class="add" aria-label="Add {E(code)} to selection tray">{PLUS}</button>
<div class="info"><b>{E(code)}</b><span>{E(it['cat'])}</span></div></article>""")
    cats = []
    for it in order:
        if it["cat"] not in cats: cats.append(it["cat"])
    chips = f'<button class="chip on" data-cat="all">All<i>{len(order)}</i></button>' + "".join(
        f'<button class="chip" data-cat="{E(k)}">{E(k)}<i>{sum(1 for x in order if x["cat"]==k)}</i></button>' for k in cats)
    return chips, "".join(out), len(order), cats

LB = f"""<div class="lb pdlb" role="dialog" aria-modal="true" aria-label="Design viewer">
<button class="lb-x" aria-label="Close">&times;</button>
<div class="lb-stage"><div style="display:flex;flex-direction:column;align-items:center;width:100%"><img src="" alt=""><div class="lb-thumbs"></div></div>
<button class="lb-nav lb-prev" aria-label="Previous">{CHEV_L}</button><button class="lb-nav lb-next" aria-label="Next">{CHEV_R}</button></div>
<div class="lb-side"><span class="kick lb-col"></span><h3 class="lb-code"></h3>
<div class="spec"><div><span>Category</span><span class="lb-cat"></span></div><div><span>Metal</span><span>Platinum Pt950</span></div><div><span>Certified</span><span>PGI · Unique ID</span></div><div><span>Views</span><span class="lb-views"></span></div></div>
<p style="color:var(--muted);font-size:15px;margin:0">Weight, price &amp; stock on request. Logo branding and customisation available.</p>
<div class="acts"><button class="btn btn-royal lb-add">Add to selection tray</button><a class="btn btn-line lb-wa" href="#" target="_blank" rel="noopener">{WA_ICO} Enquire on WhatsApp</a></div></div>
</div>"""

INSTA_FOR = {"men-of-platinum": [3, 9, 15, 21], "evara": [1, 7, 13, 19], "platinum-days-of-love": [7, 4, 16, 10], "bandhan": [22, 16, 4, 10], "farishtey": [18, 22, 12, 24]}

EXTRA = {
 "men-of-platinum": lambda: f"""<section class="sec royal">{sparkle(20)}<div class="wrap">
<div class="head"><div><span class="kick">In motion</span><h2 class="h2 rv">Not just a brand. <em>A platinum powerhouse.</em></h2></div></div>
<div class="films">{films()}</div></div></section>""",
 "evara": lambda: f"""<section class="sec-sm"><div class="wrap split">
<div class="frame d ar43 rv"><img src="assets/support/evara-story.webp" alt="Evara, very rare, very you" loading="lazy"></div>
<div class="rv"><img src="assets/brand/col-evara.png" alt="Evara" style="height:90px;width:auto"><h2 class="h2" style="margin:20px 0 14px">Platinum. <em>Very rare. Very you.</em></h2><a class="btn btn-line" href="partner.html#display">Evara counter props {ARROW}</a></div></div></section>""",
 "platinum-days-of-love": lambda: f"""<section class="sec-sm"><div class="wrap"><div class="mason">{''.join(f'<figure class="rv d{k%3}" data-full="assets/props/{p}.webp"><img src="assets/props/{p}.webp" alt="Platinum couple bands" loading="lazy"></figure>' for k,p in enumerate(["sha00041","sha00066","sha00087","sha00061","sha00079","sha00037","sha00036","sha00045","sha00046","sha00057","sha00062","sha00081","sha00089"]))}</div></div></section>""",
 "farishtey": lambda: f"""<section class="sec-sm lavbg"><div class="wrap"><div class="cards c3">
<div class="card rv">{icon("trust")}<h3>Gentle on young skin</h3><p>Naturally hypoallergenic platinum.</p></div>
<div class="card rv d1">{icon("quality")}<h3>Secure screw-backs</h3><p>Baby tops that stay put.</p></div>
<div class="card rv d2">{icon("exclusivity")}<h3>Made for milestones</h3><p>Naming ceremonies to first birthdays.</p></div></div></div></section>""",
}

def collection_page(c):
    slug = c["slug"]
    if slug == "pride-n-perfect":
        return pnp_page(c)
    chips, cards, n, cats = product_cards(slug)
    ncats = len([k for k in cats if k != "PGI Signature Picks"])
    ins = "".join(f'<figure class="rv d{k%4}" data-full="assets/insta/c{i:02d}.webp" style="margin:0;border-radius:18px;overflow:hidden;cursor:zoom-in"><img src="assets/insta/c{i:02d}.webp" alt="Dishaa creative" loading="lazy"></figure>' for k, i in enumerate(INSTA_FOR.get(slug, [])))
    body = f"""<section class="chero mistbg"><div class="wrap grid">
<div><div class="crumbs"><a href="index.html">Home</a><span>/</span><a href="collections.html">Collections</a><span>/</span><span>{c["name"]}</span></div>
<img class="clogo" src="{c["logo"]}" alt="{c["name"]}">
<h1 class="h2">{c["tag"]}</h1>
<div class="facts"><a class="aud-tag" href="explore.html#{AUDOF[slug]}">For {next(a["name"] for a in AUD if a["key"] == AUDOF[slug])}</a><div><b>{n}</b><span>Designs</span></div><div><b>{ncats}</b><span>Categories</span></div><div><b>Pt950</b><span>PGI certified</span></div></div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn btn-royal" href="#designs">Browse designs {ARROW}</a><a class="btn btn-line" href="contact.html?interest={E(c['name'])}">Get the catalogue</a></div></div>
<div class="stagec"><img class="bgi" src="{c["bg"]}" alt=""><img class="p" src="{c["hero"]}" alt="{c["name"]} signature piece"></div>
</div></section>
<div class="filters" id="designs"><div class="wrap">{chips}</div></div>
<section class="sec-sm" style="padding-top:28px"><div class="wrap">
<div class="pgrid">{cards}</div>
<div class="more-wrap"><button class="btn btn-line" data-more>Load more designs</button></div>
<p class="center" style="color:var(--muted);font-size:14px;margin-top:26px">Tap <b>+</b> to shortlist designs and send the list in one go.</p>
</div></section>
{EXTRA.get(slug, lambda: "")()}
<section class="sec-sm lavbg"><div class="wrap"><div class="head" style="margin-bottom:28px"><div><span class="kick">From our feed</span></div></div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px">{ins}</div></div></section>
{LB}{PLB}
{cta(f"Bring {c['name']} to", "your counter.", c["hero"])}"""
    page(f"{slug}.html", f"{c['name']} — Platinum Collection | Dishaa Platinum", f"{c['line']} Browse {n} {c['name']} platinum designs at Dishaa Platinum.", body, active="collections")

def pnp_page(c):
    photos = ["sha00318", "sha00313", "sha00053", "sha00035", "sha00038", "sha00050", "sha00047", "sha00092", "sha00098", "sha00097", "sha00102", "sha00109", "sha00059", "sha00104", "sha00107", "new1", "sha00041", "sha00061", "sha00171", "img_6357"]
    mason = "".join(f'<figure class="rv d{k%3}" data-full="assets/props/{p}.webp"><img src="assets/props/{p}.webp" alt="Pride N Perfect platinum couple set" loading="lazy"></figure>' for k, p in enumerate(photos))
    body = f"""<section class="chero mistbg"><div class="wrap grid">
<div><div class="crumbs"><a href="index.html">Home</a><span>/</span><a href="collections.html">Collections</a><span>/</span><span>Pride N Perfect</span></div>
<img class="clogo" src="{c["logo"]}" alt="Pride N Perfect">
<h1 class="h2">{c["tag"]}</h1><p class="sub" style="margin-top:14px">Perfect for weddings, gifting &amp; festive picks.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn btn-royal" href="contact.html?interest=Pride N Perfect">Get the catalogue {ARROW}</a><a class="btn btn-line" href="platinum-days-of-love.html">See PDOL love bands</a></div></div>
<div class="stagec"><img class="bgi" src="assets/props/sha00318.webp" alt="Pride N Perfect couple set"></div>
</div></section>
<section class="sec-sm"><div class="wrap"><div class="cards c3" style="margin-bottom:40px">
<div class="card rv">{icon("commitment")}<h3>Weddings</h3><p>Matched sets for the bride and groom.</p></div>
<div class="card rv d1">{icon("box")}<h3>Gifting</h3><p>Anniversaries and milestone moments.</p></div>
<div class="card rv d2">{icon("exclusivity")}<h3>Festive picks</h3><p>Displays that turn heads.</p></div></div>
<div class="mason">{mason}</div></div></section>
{PLB}
{cta("Couple sets that", "sell in pairs.", "assets/banner/ring-sunburst.webp")}"""
    page("pride-n-perfect.html", "Pride N Perfect — Platinum Couple Sets | Dishaa Platinum", c["line"], body, active="collections")

# ================================================================== ACCESSORIES
def accessories():
    items = [i for i in CAT["men-of-platinum"] if i["cat"] == "Cufflinks"]
    cl = "".join(f'<div class="pcard rv d{k%4}" style="cursor:default"><div class="im"><img src="{i["views"][0]}" alt="Platinum cufflinks {i["code"]}" loading="lazy"></div><div class="info"><b>{i["code"]}</b><span>Cufflinks</span></div></div>' for k, i in enumerate(items))
    acc = [("Cufflinks", "sha00151"), ("Watch Straps", "sha00153"), ("Specks", "sha00201"), ("Watches", "sha00155"), ("Chains &amp; Links", "sha00195"), ("Brooches &amp; Buttons", "sha00203")]
    grid = "".join(f'<div class="acc rv d{k%3}"><img src="assets/props/{p}.webp" alt="Platinum {t}" loading="lazy"><div><h3>{t}</h3></div></div>' for k, (t, p) in enumerate(acc))
    body = phero("Delicate craftsmanship · immensely beautiful", "Platinum accessories|<em>you would love.</em>",
                 "Cufflinks, belts, brooches, specks, watch straps, buttons, plus custom and industrial pieces on order.",
                 "assets/props/sha00153.webp", '<a href="collections.html">Collections</a><span>/</span><span>Accessories</span>') + f"""
<section class="sec"><div class="wrap"><div class="acc-grid">{grid}</div></div></section>
<section class="sec-sm lavbg"><div class="wrap"><div class="head"><div><span class="kick">In stock now</span><h2 class="h2 rv">Platinum <em>cufflinks.</em></h2></div><a class="btn btn-line" href="men-of-platinum.html#designs">All in Men of Platinum {ARROW}</a></div>
<div class="pgrid">{cl}</div></div></section>
{cta("Rare accessories.", "Few can offer them.", "assets/p/men-of-platinum/mop-cl-ppf00001-copy.webp")}"""
    page("accessories.html", "Platinum Accessories — Cufflinks, Watch Straps, Brooches | Dishaa Platinum",
         "Platinum cufflinks, belts, brooches, specks and watch straps from Dishaa Platinum, Mumbai.", body, active="collections")

# ================================================================== D THE PLATINUM
def dthe():
    body = f"""<section class="phero royal">{sparkle(30)}<div class="wrap grid">
<div><div class="crumbs" style="color:#cfd0f0"><a href="index.html">Home</a><span>/</span><a href="collections.html">Collections</a><span>/</span><span>D — The Platinum</span></div>
<img src="assets/dthe/dthe-logo.webp" alt="D — The Platinum" style="width:170px;margin:30px 0 16px">
<h1 class="h1 rv in" style="color:#fff;margin-bottom:6px">{lines("Designed with|<em class='silver'>purity.</em>")}</h1>
<p class="sub" style="margin-top:16px">A symbol of wealth and fortune. Platinum bars &amp; coins, a first in India.</p>
<div class="tagrow" style="margin:22px 0 28px"><span>Guaranteed purity</span><span>Certificate of authenticity</span><span>100% buyback</span></div>
<a class="btn btn-white" href="contact.html?interest=Platinum Bars %26 Coins">Ask for available weights {ARROW}</a></div>
<div class="art" style="background:#1f4a8f"><img src="assets/dthe/dthe-5.webp" alt="D The Platinum bars"></div></div></section>
<section class="sec"><div class="wrap"><div class="zones">
<div class="frame d rv" style="aspect-ratio:1"><img src="assets/dthe/dthe-4.webp" alt="Platinum bar" loading="lazy"></div>
<div class="frame rv d1" style="aspect-ratio:1"><img src="assets/dthe/dthe-6.webp" alt="Platinum coins" loading="lazy"></div>
<div class="card rv d2" style="justify-content:center">{icon("cert")}<h3>Bullion, in platinum.</h3><p>An investment, a gift, an heirloom. Each bar comes with its certificate.</p></div>
</div></div></section>
{cta("Offer platinum as", "an investment.", "assets/banner/ring-topaz.webp")}"""
    page("d-the-platinum.html", "D — The Platinum: Platinum Bars & Coins | Dishaa Platinum",
         "D — The Platinum: platinum bars and coins, a first in India, with guaranteed purity, certificate of authenticity and buyback.", body, active="collections")

# ================================================================== WHY PLATINUM
def why():
    cities = ["Ahmedabad", "Bangalore", "Baroda", "Bhubaneswar", "Chennai", "Cochin", "Coimbatore", "Delhi NCR", "Hyderabad", "Indore", "Kolkata", "Lucknow", "Mumbai", "Pune", "Surat", "Trivandrum"]
    body = phero("The platinum opportunity", "Don’t follow the|platinum wave.|<em>Lead it.</em>",
                 "The fastest-growing category in precious jewellery, and the new-age luxury young India wants.",
                 "assets/insta/c07.webp", "<span>Why Platinum</span>") + f"""
<section class="sec"><div class="wrap">
<div class="head"><div><span class="kick">The business case</span><h2 class="h2 rv">Growth, margin, <em>a new customer.</em></h2></div></div>
<div class="cards c3 wp-bento">
<div class="card rv"><span class="big">25%+</span><h3>Highest growth</h3><p>Year-on-year, the only precious category this fast.</p></div>
<div class="card rv d1"><span class="big">~5×</span><h3>Higher margins</h3><p>Upsell from gold to platinum.</p></div>
<div class="card rv d2"><span class="big">New</span><h3>New consumers</h3><p>Shoppers from stores without platinum.</p></div>
<div class="card rv">{icon("growth")}<h3>Young buyers</h3><p>Gifting, engagements, weddings, anniversaries.</p></div>
<div class="card rv d1">{icon("exclusivity")}<h3>Exclusivity</h3><p>Very few retailers stock it yet.</p></div>
<div class="card rv d2">{icon("men")}<h3>Men’s jewellery</h3><p>A precious option for men who don’t wear gold.</p></div>
</div></div></section>

<section class="sec royal">{sparkle(24)}<div class="wrap statband">
<div><span class="kick">Who is buying</span><h2 class="h2 rv" style="margin-top:16px">Meet the <em>platinum customer.</em></h2></div>
<div class="stats"><div class="stat rv"><b>20–40</b><span>Age group (men)</span></div><div class="stat rv d1"><b>A/B1</b><span>High-affluence segment</span></div>
<div class="stat rv d2"><b>70%</b><span>Of household income earned</span></div><div class="stat rv d3"><b>46%</b><span>Spent on discretionary buys*</span></div></div>
</div></section>

<section class="sec"><div class="wrap split">
<div class="rv"><span class="kick">Assurance</span><h2 class="h2" style="margin:16px 0 24px">If it’s platinum, trust <em>an expert.</em></h2>
<ul class="bullets"><li>PGI authorisation</li><li>Unique ID on every product</li><li>Pt950: 95% pure, third-party audited</li><li>3–5 layers of QC</li><li>PGI for platinum · IGI for diamonds</li></ul></div>
<div class="rv d1" style="display:grid;gap:16px"><img src="assets/brand/pt950-program.webp" alt="Pt950 purity assurance program" loading="lazy" style="border-radius:22px"><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px"><img src="assets/brand/pt950-card.webp" alt="Pt950 assurance card" loading="lazy"><img src="assets/brand/quality-card.webp" alt="PGI quality card" loading="lazy"></div></div>
</div></section>

<section class="sec-sm lavbg"><div class="wrap">
<div class="head"><div><span class="kick">Backed by Platinum Guild International</span><h2 class="h2 rv">PGI support, <em>via Dishaa.</em></h2></div><img src="assets/brand/logo-pgi.webp" alt="Platinum Guild International" style="height:52px;width:auto" loading="lazy"></div>
<div class="chips" style="grid-template-columns:repeat(4,1fr)">
<div class="chipc rv">{icon("display")}<span>Display trays &amp; branding</span></div><div class="chipc rv d1">{icon("training")}<span>Sales staff training</span></div>
<div class="chipc rv d2">{icon("innovation")}<span>Product development</span></div><div class="chipc rv d3">{icon("promo")}<span>National promotions</span></div></div>
<div class="frame d rv" style="margin-top:28px;aspect-ratio:21/8"><img src="assets/support/creatives.webp" alt="Platinum Guild promotions" loading="lazy"></div>
</div></section>

<section class="sec royal"><div class="wrap split">
<div><span class="kick">Stocking criteria</span><h2 class="h2 rv" style="margin-top:16px">PGI support in <em>16 cities.</em></h2><a class="btn btn-white rv" href="partner.html" style="margin-top:26px">See the partner plan {ARROW}</a></div>
<div class="cities rv d1">{''.join(f'<span>{c}</span>' for c in cities)}</div></div></section>
{cta()}"""
    page("why-platinum.html", "Why Platinum — The Platinum Business Opportunity | Dishaa Platinum",
         "Platinum jewellery grows 25%+ year on year with margins almost five times higher. The platinum opportunity for retail jewellers.", body)

# ================================================================== PARTNER
def partner():
    tiers = [("150", "", ["Tray &amp; poster", "1 reel + 1 creative / month"]),
             ("300", "", ["Tray, display &amp; training", "1 reel + 2 creatives / month"]),
             ("500", "Popular", ["Display, training, poster", "PGI website listing", "Products with your logo"]),
             ("750", "Flagship", ["Everything in 500g", "Featured in PGI promotions"])]
    tt = "".join(f'<div class="gram{" feat" if k==2 else ""} rv d{k}">' + (f'<span class="tag">{tag}</span>' if tag else "") + f'<b>{w}{"+" if k==3 else ""}<small>GRAMS</small></b><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>' for k, (w, tag, li) in enumerate(tiers))
    zones = [("zone-1", "4 ft counter", "From ₹1.30 L*"), ("zone-2", "8 ft with LED", "From ₹3.25 L*"), ("zone-3", "12 ft wall", "From ₹4.50 L*"),
             ("zone-4", "12 ft with LED", "From ₹4.50 L*"), ("zone-5", "L-shaped zone", "From ₹5.00 L*"), ("zone-6", "Atrium", "From ₹5.00 L*")]
    zz = "".join(f'<div class="zone rv d{k%3}"><div class="frame"><img src="assets/display/{z}.webp" alt="Platinum zone, {t}" loading="lazy"></div><div class="zi"><h3>{t}</h3><span>{p}</span></div></div>' for k, (z, t, p) in enumerate(zones))
    props = "".join(f'<figure class="rv d{k%3}" data-full="assets/display/{p}.webp" style="margin:0;border-radius:20px;overflow:hidden;cursor:zoom-in;aspect-ratio:4/3;background:#ddd"><img src="assets/display/{p}.webp" alt="Counter prop" loading="lazy" style="width:100%;height:100%;object-fit:cover"></figure>' for k, p in enumerate(["prop-1", "prop-4", "prop-3", "fixture-1", "fixture-4", "fixture-6"]))
    pgi = [("pgi", "PGI support"), ("training", "Training"), ("branding", "Branding"), ("promo", "Promotion"), ("marketing", "Marketing"), ("online", "Online presence")]
    custom = [("box", "Product customisation"), ("display", "Counter customisation"), ("marketing", "Marketing toolkits"), ("branding", "In-store branding"),
              ("promo", "B2C exhibitions &amp; reels"), ("logo", "Products with your logo"), ("plan", "Selection guidance"), ("buyback", "Special buyback policy")]
    body = phero("Partnership advantages", "Big ideas.|Bigger execution.|<em>Let’s take action.</em>",
                 "Innovation, trust and profitability, together. Here’s what every Dishaa partner gets.",
                 "assets/insta/c10.webp", "<span>Partner</span>") + f"""
<section class="sec-sm"><div class="wrap">
<div class="head"><div><span class="kick">PGI support, via Dishaa</span><h2 class="h2 rv">We connect you <em>with PGI.</em></h2></div><img src="assets/brand/pt-logo.png" alt="Platinum" style="height:70px;width:auto"></div>
<div class="chips">{''.join(f'<div class="chipc rv d{k%4}">{icon(i)}<span>{t}</span></div>' for k,(i,t) in enumerate(pgi))}</div></div></section>

<section class="sec royal">{sparkle(26)}<div class="wrap">
<div class="head"><div><span class="kick">Dishaa support</span><h2 class="h2 rv">The more you stock, <em>the more we give.</em></h2></div></div>
<div class="grams">{tt}</div><p class="fine">* T&amp;Cs apply. Grams of platinum inventory stocked through Dishaa.</p></div></section>

<section class="sec mistbg"><div class="wrap">
<div class="head"><div><span class="kick">Customised service</span><h2 class="h2 rv">Made to fit <em>your store.</em></h2></div></div>
<div class="chips" style="grid-template-columns:repeat(4,1fr)">{''.join(f'<div class="chipc rv d{k%4}">{icon(i)}<span>{t}</span></div>' for k,(i,t) in enumerate(custom))}</div>
<div class="cards" style="margin-top:28px">
<div class="card rv">{icon("range")}<h3>Multiple brands</h3><p>One buying desk.</p></div>
<div class="card rv d1">{icon("fast")}<h3>Lightweight, ready stock</h3><p>Fast-moving designs.</p></div>
<div class="card rv d2">{icon("refill")}<h3>Strategic refills</h3><p>What sells, restocked.</p></div>
<div class="card rv d3">{icon("growth")}<h3>New-gen designs</h3><p>For the young buyer.</p></div></div>
</div></section>

<section class="sec" id="display"><div class="wrap">
<div class="head"><div><span class="kick">Display &amp; counters</span><h2 class="h2 rv">An exclusive <em>platinum zone.</em></h2></div><p class="sub rv">Subtle, confident, premium. Never over the top.</p></div>
<div class="zones">{zz}</div>
<p class="fine" style="color:var(--muted)">* Indicative. Includes 2D/3D design &amp; fabrication; depends on area. GST extra, T&amp;Cs apply.</p>
<div class="zones" style="margin-top:40px">{props}</div>
</div></section>

<section class="sec royal">{sparkle(20)}<div class="wrap">
<div class="head"><div><span class="kick">How it works</span><h2 class="h2 rv">Your platinum journey, <em>in five steps.</em></h2></div></div>
<div class="steps"><div class="step rv"><b>Connect</b><span>Call, WhatsApp or visit.</span></div><div class="step rv d1"><b>Plan</b><span>Investment &amp; inventory.</span></div>
<div class="step rv d2"><b>Select</b><span>Ready stock, fast.</span></div><div class="step rv d3"><b>Launch</b><span>Display, branding, training.</span></div><div class="step rv d4"><b>Grow</b><span>Refills &amp; promotions.</span></div></div>
</div></section>

<section class="sec-sm" id="manufacturers"><div class="wrap center" style="margin-bottom:26px"><span class="kick">All manufacturers’ exclusive products, at one place</span></div>{logos_marquee()}</section>
{PLB}
{cta("Turning platinum potential into", "retail performance.", "assets/banner/bracelet-cable.webp")}"""
    page("partner.html", "Partner With Dishaa Platinum — PGI Support, Display, Training & Branding",
         "Become a Dishaa Platinum partner: PGI enrolment, tiered support, display zones, staff training, customised products and the best buyback policy.", body)

# ================================================================== LOOKBOOK
def lookbook():
    shots = ["ph10", "phe1", "ph12", "ph7", "phe6", "ph3", "ph8", "phe2", "ph13", "ph9", "phe4", "ph14", "ph16", "phe3", "ph6", "ph11", "phe5", "ph17"]
    props = ["sha00318", "sha00313", "sha00122", "sha00131", "sha00146", "sha00171", "sha00183", "sha00200", "img_2561",
             "sha00119", "sha00130", "sha00145", "sha00147", "sha00115", "sha00118", "sha00136", "13372", "img_2540", "img_63272", "sha00155", "sha00195", "sha00203"]
    studio = [f"st{k:02d}" for k in range(1, 25)]
    m3 = "".join(f'<figure class="rv d{k%3}" data-full="assets/studio/{p}.webp"><img src="assets/studio/{p}.webp" alt="Platinum jewellery, studio" loading="lazy"></figure>' for k, p in enumerate(studio))
    fl = ["chain-blue", "studio-1", "studio-2", "chain-blue-2", "studio-3", "studio-4", "studio-5", "hero-twotone", "studio-6", "studio-7", "studio-8", "chain-light", "studio-9", "studio-10", "studio-11"]
    reel = "".join(f'<div class="film rv d{k%3}"><video data-auto muted loop playsinline preload="none" poster="assets/video/{v}.jpg"><source src="assets/video/{v}.mp4" type="video/mp4"></video></div>' for k, v in enumerate(fl))
    m0 = "".join(f'<figure class="rv d{k%3}" data-full="assets/insta/c{k+1:02d}.webp"><img src="assets/insta/c{k+1:02d}.webp" alt="Dishaa Platinum creative" loading="lazy"></figure>' for k in range(24))
    m1 = "".join(f'<figure class="rv d{k%3}" data-full="assets/lookbook/{p}.webp"><img src="assets/lookbook/{p}.webp" alt="Platinum jewellery photograph" loading="lazy"></figure>' for k, p in enumerate(shots))
    m2 = "".join(f'<figure class="rv d{k%3}" data-full="assets/props/{p}.webp"><img src="assets/props/{p}.webp" alt="Platinum jewellery still life" loading="lazy"></figure>' for k, p in enumerate(props))
    body = phero("Photography · films", "It’s rare,|<em>and eternal.</em>", "Our platinum, photographed and filmed.",
                 "assets/lookbook/ph10.webp", "<span>Lookbook</span>") + f"""
<section class="sec-sm royal"><div class="wrap"><div class="head"><div><span class="kick">In motion</span><h2 class="h2 rv">Platinum, <em>filmed.</em></h2></div></div><div class="films reel">{reel}</div></div></section>
<section class="sec-sm"><div class="wrap"><div class="head"><div><span class="kick">Series 01</span><h2 class="h2 rv">The <em>blue room.</em></h2></div></div><div class="mason">{m1}</div></div></section>
<section class="sec-sm lavbg"><div class="wrap"><div class="head"><div><span class="kick">Series 02</span><h2 class="h2 rv">Still <em>life.</em></h2></div></div><div class="mason">{m2}</div></div></section>
<section class="sec-sm"><div class="wrap"><div class="head"><div><span class="kick">Series 03</span><h2 class="h2 rv">The <em>studio.</em></h2></div></div><div class="mason">{m3}</div></div></section>
{PLB}
{cta()}"""
    page("lookbook.html", "Lookbook — Dishaa Platinum", "Creatives, photography and films of platinum jewellery from Dishaa Platinum.", body)

# ================================================================== CONTACT
def contact():
    ints = [c["name"] for c in COLS] + ["Accessories", "Platinum Bars &amp; Coins", "Display &amp; Counters", "PGI Enrolment"]
    chk = "".join(f'<label><input type="checkbox" name="interest" value="{html.unescape(i)}"><span>{i}</span></label>' for i in ints)
    lab = 'style="font-size:12px;font-family:var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)"'
    body = phero("Visit · call · WhatsApp", "We invite you to our|<em>world of platinum.</em>",
                 "Tell us about your store. We’ll plan your platinum counter with you.", "assets/insta/c11.webp", "<span>Contact</span>") + f"""
<section class="sec" style="padding-top:20px"><div class="wrap split" style="align-items:start;grid-template-columns:.8fr 1.2fr">
<div class="cinfo">
<div class="card rv">{icon("display")}<h3 {lab}>The Platinum Hub</h3><p>{ADDRESS}</p></div>
<div class="card rv d1">{icon("chat")}<h3 {lab}>Call · Write</h3><a href="tel:{PHONE1}">{PHONE1_T}</a><a href="tel:{PHONE2}">{PHONE2_T}</a><a href="mailto:{EMAIL}" style="font-size:18px">{EMAIL}</a></div>
<a class="btn btn-royal rv d2" href="https://wa.me/{WA}" target="_blank" rel="noopener" style="justify-content:center">{WA_ICO} Chat on WhatsApp</a>
</div>
<form id="enquiry" class="form rv d1" novalidate>
<div class="field full"><span class="kick">Partner enquiry</span><h2 class="h3" style="margin-top:8px;color:var(--navy)">Let’s connect.</h2></div>
<div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="f-store">Store / company *</label><input id="f-store" name="store" required autocomplete="organization"></div>
<div class="field"><label for="f-city">City *</label><input id="f-city" name="city" required autocomplete="address-level2"></div>
<div class="field"><label for="f-phone">Phone / WhatsApp *</label><input id="f-phone" name="phone" type="tel" required autocomplete="tel"></div>
<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="f-type">I am a</label><select id="f-type" name="type"><option>Retail jeweller</option><option>Jewellery chain</option><option>Wholesaler / distributor</option><option>International retailer</option><option>Other</option></select></div>
<div class="field full"><label>Interested in</label><div class="checks">{chk}</div></div>
<div class="field full"><label for="f-msg">Message</label><textarea id="f-msg" name="message" placeholder="Store size, current platinum stock, designs you need…"></textarea></div>
<div class="field full" style="flex-direction:row;gap:12px;flex-wrap:wrap"><button class="btn btn-royal" type="submit">{WA_ICO} Send via WhatsApp</button><button class="btn btn-line" type="button" data-mail>Send via email</button></div>
</form></div></section>
<section class="sec-sm" style="padding-top:0"><div class="wrap"><iframe class="map" title="Map to Dishaa Platinum, Zaveri Bazaar, Mumbai" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Chandra%20Darshan%20Building%2C%20Dhanji%20Street%2C%20Zaveri%20Bazaar%2C%20Mumbai%20400003&z=16&output=embed"></iframe></div></section>"""
    page("contact.html", "Contact Dishaa Platinum — Zaveri Bazaar, Mumbai", "Visit Dishaa Platinum at Chandra Darshan Building, Dhanji Street, Zaveri Bazaar, Mumbai. Call +91 81691 20942 or email sales@dishaaplatinum.com.", body)

def extras():
    out = OUT or ROOT
    pri = lambda r: "1.0" if r == "/" else ("0.9" if r.count("/") == 2 else "0.8")
    sm = "".join(f"<url><loc>{SITE}{r}</loc><lastmod>{LASTMOD}</lastmod><changefreq>monthly</changefreq><priority>{pri(r)}</priority></url>" for r in ROUTES.values())
    open(os.path.join(out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # branded 404 (GitHub Pages / most hosts serve /404.html)
    body = f"""<section class="phero mistbg" style="min-height:70vh;display:flex;align-items:center"><div class="wrap center">
<span class="kick">Error 404</span><h1 class="h1" style="margin:18px auto 14px">This piece isn’t <em>in our vault.</em></h1>
<p class="sub">The page you’re looking for has moved or doesn’t exist.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:28px"><a class="btn btn-royal" href="index.html">Back to home {ARROW}</a><a class="btn btn-line" href="collections.html">Browse collections</a></div></div></section>"""
    html404 = head("Page not found | Dishaa Platinum", "The page you are looking for could not be found.", "/404.html").replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"')
    html404 += '\n<body data-hero="light">\n' + header("") + "\n<main>" + body + "</main>\n" + shells() + footer()
    open(os.path.join(out, "404.html"), "w", encoding="utf-8").write(route_links(html404))
    # remove the old flat *.html pages (now served from folders)
    for f in ROUTES:
        fp = os.path.join(ROOT, f)
        if f != "index.html" and os.path.exists(fp): os.remove(fp)

if __name__ == "__main__":
    home(); about(); collections()
    for c in COLS: collection_page(c)
    explore(); accessories(); dthe(); why(); partner(); lookbook(); contact(); extras()

# ------------------------------------------------------------------ flattened banner exports (content-doc formats)
def export_page():
    items = ""
    for b in BANNERS:
        n = b["n"]
        items += f'<div class="ex w" id="w{n}"><img src="/assets/hero/w{n}.webp" alt=""><div class="tx">{banner_lines(b["d"], 1024, dy=32)}</div></div>'
        items += f'<div class="ex m" id="m{n}"><img src="/assets/hero/m{n}.webp" alt=""><div class="tx">{banner_lines(b["m"], 512)}</div></div>'
    html_ = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@300&display=block" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css"><style>
body{{margin:0;background:#fff}} .ex{{position:relative;container-type:inline-size;margin:0 0 20px}} .ex img{{display:block;width:100%;height:100%;object-fit:cover}}
.ex.w{{width:960px;aspect-ratio:16/9}} .ex.m{{width:512px;aspect-ratio:1/1}} .ex .tx{{position:absolute;inset:0}} .ex .ln{{opacity:1;translate:0 0}}
</style></head><body>{items}</body></html>"""
    open(os.path.join(ROOT, "_build", "export.html"), "w", encoding="utf-8").write(html_)

if not OUT:
    export_page()
