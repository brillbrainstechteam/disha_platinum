# Dishaa Platinum — website

Static, dependency-free site (HTML/CSS/JS) with clean URLs: every page is a folder with its own `index.html` (e.g. `/about/`, `/collections/evara/`). Serve the folder from a web server at the domain root (Vercel, Netlify, cPanel, or `python -m http.server`). Opening files directly from disk won't work because links and assets are root-absolute. Don't upload `_build/`.

## Pages
/ · /about/ · /collections/ · /collections/{men-of-platinum, evara, platinum-days-of-love, bandhan, farishtey, pride-n-perfect, accessories, d-the-platinum}/ · /why-platinum/ · /partner/ · /lookbook/ · /contact/

## Editing
Pages are generated. Edit `_build/build.py` (copy/content) or `assets/css/site.css`, `assets/js/site.js`, then run:

    python _build/build.py

- `_build/assets.py` re-processes the product PNGs from the source Drive folders into `assets/p/` and writes `_build/catalog.json` (design codes come from file names).
- `_build/media.py` re-processes photography, brand marks, display renders and videos.

## Brand assets (v2)
From `F:\disha_platinum\Logo_Banner`: the official logo lockups (`assets/brand/dishaa-*.png`), the six collection logos cut from the banner PSD's vector smart object (`assets/brand/col-*.png`), the hero products and backgrounds from the three PSD banners (`assets/banner/`), and the 24 Instagram creatives (`assets/insta/`). Palette: royal blue #2E3490, logo navy #27326D, violet #67387F, lavender mist, rose-gold. The home hero rebuilds the three PSD banners in HTML so they stay sharp at any size.

## Enquiries
There is no backend. The contact form and the "Selection Tray" (shortlist of designs) open WhatsApp (+91 81691 20942) or email (sales@dishaaplatinum.com) with a pre-filled message. Change `WA` / `EMAIL` in `assets/js/site.js` and `_build/build.py`.

## Hero banners
`_build/banner.py` rebuilds the three banners in `Logo_Banner/Banner_1024 x 512.psd` at 2x from the PSD's embedded full-resolution sources: desktop 2:1 (`assets/hero/d0N.webp`), mobile 1:1 (`m0N.webp`) and 16:9 plates (`w0N.webp`). Headline text is set as live text (Playfair Display / Jost standing in for Bodoni BT / Futura BT) at the PSD's exact positions. Flattened exports in the content-doc sizes (960x540, 512x512, plus @2x) are in `Logo_Banner/Banner exports/`.

## Hosting (GitHub Pages) & SEO
Live: https://brillbrainstechteam.github.io/disha_platinum/ served from the `gh-pages` branch. Republish after changes with:

    bash _build/deploy_pages.sh

`main` holds the source; its committed HTML is built for the root of a custom domain (SITE = https://www.dishaaplatinum.com). To move to a custom domain: set `BASE=""` and `SITE` in `deploy_pages.sh`, add a `CNAME` file, and point DNS at GitHub Pages.

SEO included: unique titles + meta descriptions, canonical URLs, Open Graph + Twitter cards with per-page images, JSON-LD (JewelryStore/Organization with address and phone, WebSite, BreadcrumbList), one h1 per page, image alt text, sitemap.xml with lastmod/priority, robots.txt, and a branded 404 page (noindex).
