"""Build the web logo files from the vector master (_build/logo_src/dishaa-logo-2026.ai, PDF-compatible).
Run: python _build/logo.py   (writes assets/brand/dishaa-*.png, d-mark.png, favicons)"""
import os
import numpy as np
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_build", "logo_src", "dishaa-logo-2026.ai")
OUT = os.path.join(ROOT, "assets", "brand")

page = pymupdf.open(SRC)[0]
pix = page.get_pixmap(matrix=pymupdf.Matrix(4, 4), alpha=True)
art = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
alpha = np.array(art)[:, :, 3]

# horizontal bands: D mark, DISHAA, PLATINUM, rule, tagline, The Platinum Hub
rows = np.where(alpha.max(1) > 20)[0]
bands, start, prev = [], rows[0], rows[0]
for r in rows[1:]:
    if r - prev > 12:
        bands.append((start, prev)); start = r
    prev = r
bands.append((start, prev))

def crop(y0, y1):
    cols = np.where(alpha[y0:y1 + 1].max(0) > 20)[0]
    return art.crop((cols[0], y0, cols[-1] + 1, y1 + 1))

def pad(im, p):
    out = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0))
    out.paste(im, (p, p), im)
    return out

def white(im):
    a = im.split()[3]
    w = Image.new("RGBA", im.size, (255, 255, 255, 0)); w.putalpha(a)
    return w

def fit(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

mark = crop(*bands[0])
word = crop(bands[1][0], bands[2][1])            # DISHAA + PLATINUM
lockup = crop(bands[0][0], bands[-1][1])         # full stacked logo

# stacked lockup (header of about card, footer)
lk = pad(fit(lockup, 1100), 24)
lk.save(os.path.join(OUT, "dishaa-lockup.png"), optimize=True)
white(lk).save(os.path.join(OUT, "dishaa-lockup-white.png"), optimize=True)

# D mark (favicon, small marks)
dm = pad(fit(mark, 640), 16)
dm.save(os.path.join(OUT, "d-mark.png"), optimize=True)
for s in (32, 180, 512):
    sq = Image.new("RGBA", (s, s), (255, 255, 255, 0))
    t = fit(mark, round(s * .86)); sq.paste(t, ((s - t.width) // 2, (s - t.height) // 2), t)
    sq.save(os.path.join(OUT, f"favicon-{s}.png"), optimize=True)

# horizontal lockup (site header): D mark + wordmark, wordmark centred on the D
H = 400
m = fit(mark, H)
w = fit(word, round(H * .74))
gap = round(H * .1)
hz = Image.new("RGBA", (m.width + gap + w.width, H), (0, 0, 0, 0))
hz.paste(m, (0, 0), m)
hz.paste(w, (m.width + gap, (H - w.height) // 2 + round(H * .02)), w)
hz = pad(hz, 8)
hz.save(os.path.join(OUT, "dishaa-horizontal.png"), optimize=True)
white(hz).save(os.path.join(OUT, "dishaa-horizontal-white.png"), optimize=True)
print("logo files written:", lk.size, dm.size, hz.size)
