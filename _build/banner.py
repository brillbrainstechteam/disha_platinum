"""Rebuild the three banners in Banner_1024 x 512.psd from their embedded high-res sources.

Outputs (assets/hero/):
  d01..d03.webp  desktop 2:1  (2048x1024, text layers excluded -> set as live HTML text)
  m01..m03.webp  mobile 1:1   (1024x1024, recomposed layout, text excluded)
  w01..w03.webp  16:9 plate   (2048x1152, for the flattened 960x540 export)
"""
import io, math, os
from psd_tools import PSDImage
from PIL import Image, ImageChops, ImageDraw
import pymupdf as fitz
Image.MAX_IMAGE_PIXELS = None

PSD = r"F:/disha_platinum/Logo_Banner/Banner_1024 x 512.psd"
OUT = r"F:/disha_platinum/website/assets/hero"
S = 2

class View:
    """Maps banner coordinates (1024x512 space) onto an output canvas."""
    def __init__(self, w=1024, h=512, k=1.0, dx=0.0, dy=0.0, override=None, skip=()):
        self.w, self.h, self.k, self.dx, self.dy = w, h, k, dx, dy
        self.override = override or {}; self.skip = set(skip)
    def box(self, name, x0, y0, x1, y1):
        if name in self.override:
            return self.override[name]
        return (x0 * self.k + self.dx, y0 * self.k + self.dy, x1 * self.k + self.dx, y1 * self.k + self.dy)
    @property
    def size(self): return (int(self.w * S), int(self.h * S))

_cache = {}
def so_image(l, target_w):
    key = (l.layer_id, int(target_w))
    if key in _cache: return _cache[key].copy()
    so = l.smart_object; d = so.data
    if d[:4] == b"%PDF":
        doc = fitz.open(stream=d, filetype="pdf"); pg = doc[0]
        z = max(1, target_w * 1.3 / pg.rect.width)
        pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
        im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    elif d[:4] == b"8BPS":
        im = PSDImage.open(io.BytesIO(d)).composite().convert("RGBA")
    else:
        im = Image.open(io.BytesIO(d)).convert("RGBA")
    _cache[key] = im
    return im.copy()

def paste_box(v, img, box, op=1.0):
    """Resize img into box (output units) on a transparent canvas."""
    x0, y0, x1, y1 = box
    W, H = max(1, round((x1 - x0) * S)), max(1, round((y1 - y0) * S))
    layer = Image.new("RGBA", v.size, (0, 0, 0, 0))
    layer.paste(img.resize((W, H), Image.LANCZOS), (round(x0 * S), round(y0 * S)))
    if op < 1:
        layer.putalpha(layer.split()[3].point(lambda a: int(a * op)))
    return layer

def apply_mask(v, layer, l):
    if not l.has_mask() or l.mask is None: return layer
    full = Image.new("L", v.size, l.mask.background_color)
    m = l.mask.topil()
    if m is not None:
        bx = v.box(l.name, *l.mask.bbox)
        W, H = max(1, round((bx[2] - bx[0]) * S)), max(1, round((bx[3] - bx[1]) * S))
        full.paste(m.convert("L").resize((W, H), Image.BICUBIC), (round(bx[0] * S), round(bx[1] * S)))
    layer.putalpha(ImageChops.multiply(layer.split()[3], full))
    return layer

def so_layer(v, l):
    x0q, y0q, x1q, y1q, *_ = l.smart_object.transform_box
    box = v.box(l.name, *l.bbox)
    img = so_image(l, (box[2] - box[0]) * S)
    bb = img.split()[3].getbbox()
    if bb: img = img.crop(bb)
    if x1q < x0q:
        img = img.transpose(Image.FLIP_LEFT_RIGHT); x0q, y0q, x1q, y1q = x1q, y1q, x0q, y0q
    ang = math.degrees(math.atan2(y1q - y0q, x1q - x0q))
    if abs(ang) > 0.3:
        img = img.rotate(-ang, resample=Image.BICUBIC, expand=True)
        bb = img.split()[3].getbbox()
        if bb: img = img.crop(bb)
    out = apply_mask(v, paste_box(v, img, box, l.opacity / 255), l)
    if l.name in FEATHER_LEFT:  # soften a hard photo edge so the wide plates blend
        fx0 = box[0] * S; fw = FEATHER_LEFT[l.name] * v.k * S
        ramp = Image.new("L", out.size, 255)
        g = Image.linear_gradient("L").rotate(90, expand=True).resize((max(1, int(fw)), out.size[1]))
        g = g.transpose(Image.FLIP_LEFT_RIGHT)  # 0 at the edge -> 255 inside
        ramp.paste(0, (0, 0, max(0, int(fx0)), out.size[1]))
        ramp.paste(g, (int(fx0), 0))
        out.putalpha(ImageChops.multiply(out.split()[3], ramp))
    return out

FEATHER_LEFT = {"purple-aster-flowers-close-up": 140}

def pixel_layer(v, l):
    im = l.topil()
    if im is None: return None
    return apply_mask(v, paste_box(v, im.convert("RGBA"), v.box(l.name, *l.bbox), l.opacity / 255), l)

def shape_layer(v, l):
    col = (45, 51, 113, 255)
    try:
        from psd_tools.constants import Tag
        c = l.tagged_blocks.get_data(Tag.SOLID_COLOR_SHEET_SETTING).get(b"Clr ")
        col = (int(c.get(b"Rd  ")), int(c.get(b"Grn ")), int(c.get(b"Bl  ")), 255)
    except Exception:
        pass
    x0, y0, x1, y1 = v.box(l.name, *l.bbox)
    im = Image.new("RGBA", v.size, (0, 0, 0, 0))
    w, h = x1 - x0, y1 - y0
    r = min(w, h) / 2 if w > 8 and h > 8 else 0
    ImageDraw.Draw(im).rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=r * S, fill=col)
    return im

def layer_img(v, l):
    if l.kind == "smartobject": return so_layer(v, l)
    if l.kind == "pixel": return pixel_layer(v, l)
    if l.kind == "shape": return shape_layer(v, l)
    return None

import numpy as np
_TINT = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tint01.npy"))  # measured vs Photoshop's own composite

def sky_tint(canvas, v):
    """Photoshop applies a sky-blue smart filter to banner 01's backdrop; psd-tools can't read it,
    so we apply the colour ratio measured against Photoshop's saved composite."""
    W, H = canvas.size
    bw, bh = max(1, round(1024 * v.k * S)), max(1, round(512 * v.k * S))
    chans = []
    for c in range(3):
        m = Image.fromarray((_TINT[..., c] * 100).astype(np.float32), mode="F").resize((bw, bh), Image.BICUBIC)
        full = Image.new("F", (W, H), 100.0)
        ox, oy = round(v.dx * S), round(v.dy * S)
        full.paste(m, (ox, oy))
        if oy > 0:  # extend the top row upwards (sky continues above the banner edge)
            full.paste(m.crop((0, 0, bw, 1)).resize((bw, oy)), (ox, 0))
        chans.append(np.asarray(full) / 100.0)
    alpha = canvas.split()[3]
    arr = np.asarray(canvas.convert("RGB")).astype(np.float32)
    arr = np.clip(arr * np.stack(chans, -1), 0, 255).astype(np.uint8)
    out = Image.fromarray(arr, "RGB").convert("RGBA"); out.putalpha(alpha)
    return out

def render(group, v, fill=(255, 255, 255)):
    canvas = Image.new("RGBA", v.size, (fill + (255,)) if fill else (0, 0, 0, 0))
    layers = [l for l in group]; i = 0
    while i < len(layers):
        l = layers[i]; i += 1
        if not l.visible or l.kind == "type" or l.name in v.skip: continue
        base = layer_img(v, l)
        if base is None: continue
        while i < len(layers) and layers[i].clipping:
            c = layers[i]; i += 1
            if not c.visible or c.kind == "type" or c.name in v.skip: continue
            ci = layer_img(v, c)
            if ci is None: continue
            ci.putalpha(ImageChops.multiply(ci.split()[3], base.split()[3]))
            base.alpha_composite(ci)
        canvas.alpha_composite(base)
        if l.name == "109634-ONMH2X-9":
            canvas = sky_tint(canvas, v)
    return canvas

def pill(canvas, box, v):
    """Sky-blue pill (mobile banner 03), gradient sampled from the PSD's pill."""
    x0, y0, x1, y1 = [c * S for c in box]
    w, h = int(x1 - x0), int(y1 - y0)
    g = Image.new("RGB", (w, 1))
    for x in range(w):
        t = x / max(1, w - 1)
        g.putpixel((x, 0), (int(92 + (190 - 92) * t), int(172 + (222 - 172) * t), int(222 + (243 - 222) * t)))
    g = g.resize((w, h))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w + h, h - 1), radius=h // 2, fill=255)
    canvas.paste(g, (int(x0), int(y0)), m)
    return canvas

PRODUCTS = {
  "01": ("PGDRN1595 -F (1)", "PDRN1627 (1)", "PPPS1169", "Pt black logo", "Dishaa Platinum Hub", "Shape 1",
         "Untitled-2", "Untitled-2 copy", "Untitled-2 copy 2", "Untitled-2 copy 6", "ERH9205PLA", "Vector Smart Object1 copy"),
  "02": ("DKFS1051", "Layer 2", "PPR00187", "Pt black logo copy", "Untitled-2 copy 3", "Untitled-2 copy 4"),
  "03": ("PDRN1704 (1)", "Vector Smart Object", "Pt black logo copy 2", "Untitled-2 copy 5"),
}
from PIL import ImageFilter
STRETCH = {("03", False)}  # (banner, left?) sides that continue straight instead of mirroring

def wide_plate(group, n, banner_img, side=512, keep=None):
    """4:1 edge-to-edge plate. The product-free background is extended (mirrored, or stretched where
    a shape runs off the edge) and blurred as ONE continuous image, so there is no seam; the blur
    starts ~90 units inside the banner and deepens outwards. Products/logos are composited back sharp."""
    over = {"purple-aster-flowers-close-up": (-170, -272, 1378, 557)} if n == "03" else {}  # cover the white band at the left
    bg = render(group, View(skip=PRODUCTS[n], override=over)).convert("RGB")
    W, H = bg.size; sp = side * S
    ext = Image.new("RGB", (W + 2 * sp, H)); ext.paste(bg, (sp, 0))
    for left in (True, False):
        src = bg.crop((0, 0, sp, H)) if left else bg.crop((W - sp, 0, W, H))
        mir = src.transpose(Image.FLIP_LEFT_RIGHT)
        if (n, left) in STRETCH:
            col = bg.crop((W - 6 * S, 0, W - 2 * S, H)).resize((sp, H), Image.BICUBIC)
            band = Image.new("L", (sp, H), 0)
            ImageDraw.Draw(band).rectangle((0, 88 * S, sp, 376 * S), fill=255)
            mir = Image.composite(col, mir, band.filter(ImageFilter.GaussianBlur(2 * S)))
        ext.paste(mir, (0, 0) if left else (W + sp, 0))
    sharp = np.asarray(ext).astype(np.float32)
    soft = np.asarray(ext.filter(ImageFilter.GaussianBlur(9 * S))).astype(np.float32)
    heavy = np.asarray(ext.filter(ImageFilter.GaussianBlur(30 * S))).astype(np.float32)
    X = np.arange(W + 2 * sp, dtype=np.float32)
    F = 90 * S
    d_in = np.minimum(X - sp, sp + W - X)            # >0 inside the banner
    inside = d_in >= 0
    ws = np.where(inside, np.clip(1 - d_in / F, 0, 1) ** 1.6, 0)
    wh = np.where(inside, 0, np.clip(-d_in / sp, 0, 1) ** 0.8)
    ws = np.where(inside, ws, 1 - wh)
    ws = ws[None, :, None]; wh = wh[None, :, None]
    out = sharp * (1 - ws - wh) + soft * ws + heavy * wh
    plate = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    # products & logos back on top, crisp
    if keep is None:
        keep = set(PRODUCTS[n]) - ({"Dishaa Platinum Hub", "Shape 1"} if n == "01" else set())
    others = [l.name for l in group if l.name not in keep]
    prod = render(group, View(skip=others), fill=None)
    plate.alpha_composite(prod, (sp, 0))
    return plate.convert("RGB")

LIVE = {"01": {"ring1": "PGDRN1595 -F (1)", "ring2": "PDRN1627 (1)", "pendant": "PPPS1169"}}
LIVE_STATIC = {"01": {"Pt black logo", "Untitled-2 copy 2", "Untitled-2 copy 6"}}  # stays in the plate (logo + ring shadows)

def live_parts(group, n):
    """Background plate without the animated pieces + each piece as a transparent cut-out with its box."""
    import json
    plate = wide_plate(group, n, None, keep=LIVE_STATIC[n])
    save(plate, f"x{n}bg", q=84)
    boxes = {}
    names = [l.name for l in group]
    for key, lname in LIVE[n].items():
        im = render(group, View(skip=[x for x in names if x != lname]), fill=None)
        bb = im.split()[3].getbbox()
        im.crop(bb).save(f"{OUT}/{n}-{key}.webp", "WEBP", quality=90, method=6)
        boxes[key] = [round(v / S, 2) for v in bb]
        print(key, boxes[key])
    json.dump(boxes, open(f"{OUT}/live{n}.json", "w"))

def save(img, name, q=86):
    img.convert("RGB").save(f"{OUT}/{name}.webp", "WEBP", quality=q, method=6)
    print("saved", name, img.size)

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    p = PSDImage.open(PSD)
    G = {g.name: g for g in p if g.kind == "group"}
    no_text_logo = ("Dishaa Platinum Hub", "Shape 1")

    # desktop 2:1 (the site header already carries the Dishaa logo, so the in-banner logo stays for fidelity)
    no_logo = ("Dishaa Platinum Hub", "Shape 1")
    for n in ("01", "02", "03"):
        save(render(G[n], View(skip=no_logo if n == "01" else ())), f"d{n}")

    # 4:1 edge-to-edge plates for the full-width hero
    for n in ("01", "02", "03"):
        d = Image.open(f"{OUT}/d{n}.webp").convert("RGB")
        save(wide_plate(G[n], n, d), f"x{n}", q=84)

    # 16:9 plates for the 960x540 export: same art, 32 units of extra background above & below
    for n in ("01", "02", "03"):
        save(render(G[n], View(1024, 576, 1, 0, 32, skip=no_logo if n == "01" else ())), f"w{n}")

    # mobile 1:1
    save(render(G["01"], View(512, 512, 0.86, -22, 60, skip=no_text_logo + ("PPPS1169", "Pt black logo")), fill=(222, 236, 242)), "m01")
    save(render(G["02"], View(512, 512, 0.8, -106, 119, skip=("Pt black logo copy",))), "m02")
    v3 = View(512, 512, 1, 0, 0, skip=("Rounded Rectangle 1", "Layer 7", "Pt black logo copy 2"), override={
        "purple-aster-flowers-close-up": (-420, -140, 852, 689),
        "Vector Smart Object": (18, 196, 318, 455),
        "PDRN1704 (1)": (300, 280, 512, 492),
        "Untitled-2 copy 5": (330, 470, 500, 490),
        "Layer 4": (-300, -350, 610, 355), "Layer 6": (-8, -27, 1032, 549)})
    m03 = render(G["03"], v3)
    save(pill(m03, (26, 34, 512, 172), v3), "m03")
