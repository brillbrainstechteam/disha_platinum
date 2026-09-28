"""Convert the raw Dishaa media folders into web-ready assets + catalog.json."""
import os, re, json, sys
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None

SRC = r"F:/disha_platinum/PNG IMAGES-20260928T095426Z-1-001/PNG IMAGES"
OUT = r"F:/disha_platinum/website/assets"

# collection -> list of (category label, folder, code prefix)
MAP = {
 "men-of-platinum": [
   ("Chains", "MEN OF PLATINUM/CHAINS", "MOP-CH"),
   ("Bracelets", "MEN OF PLATINUM/BRACELET", "MOP-BR"),
   ("Kadas", "MEN OF PLATINUM/MENS KADA", "MOP-KD"),
   ("Rings", "MEN OF PLATINUM/MENS RING", "MOP-RG"),
   ("Rings", "MEN OF PLATINUM/MENS STONE RINGS", "MOP-SR"),
   ("Pendants", "MEN OF PLATINUM/MENS PENDENT", "MOP-PD"),
   ("Balis & Studs", "MEN OF PLATINUM/GENTS BALLI & STUD", "MOP-ER"),
   ("Cufflinks", "MEN OF PLATINUM/CUFFLINK", "MOP-CL"),
 ],
 "evara": [
   ("Rings", "EVARA/WOMEN  RINGS", "EVR-RG"),
   ("Bracelets", "EVARA/WOMEN BCT", "EVR-BR"),
   ("Kadas", "EVARA/WOMEN KADA", "EVR-KD"),
   ("Earrings", "EVARA/EARRINGS/STUD", "EVR-ST"),
   ("Earrings", "EVARA/EARRINGS/BALI", "EVR-BL"),
   ("Earrings", "EVARA/EARRINGS/SHENDILIAR", "EVR-CD"),
   ("Earrings", "EVARA/EARRINGS/ZUMKI", "EVR-JH"),
   ("Necklaces", "EVARA/NECKLACE", "EVR-NK"),
   ("Necklaces", "EVARA/CHAIN SET", "EVR-CS"),
   ("Pendant Sets", "EVARA/PENDENT SET", "EVR-PS"),
   ("Diamond Edit", "PT_Mine", "EVR-DM"),
 ],
 "platinum-days-of-love": [
   ("Couple Bands", "PDOL/COUPLE BANDS", "PDL-CB"),
   ("Bands", "PDOL/BANDS", "PDL-BD"),
 ],
 "bandhan": [("Mangalsutras", "BANDHAN/NECK MANGAL SUTRA", "BDN-MS")],
 "farishtey": [
   ("Baby Tops", "FARISHTEY/BABY TOPS", "FRS-TP"),
   ("Baby Pendants", "FARISHTEY/BAY PENDENTS", "FRS-PD"),
 ],
}
PGI = {  # PGI campaign layouts (opaque, baked labels) -> cropped
 "men-of-platinum": ["PGI PROMTION IMAGES/PGI MOP product/" + d for d in ["MENS BCT","MENS CHAINS","MENS KADA","MENS RING"]],
 "evara": ["PGI PROMTION IMAGES/PGI EVARA/" + d for d in ["EARING","NECKLES","WOMENS BCT","WOMENS KADA","WOMENS RING"]],
 "platinum-days-of-love": ["PGI PROMTION IMAGES/PGI PDOL product images 2023/COUPLE BAND"],
}

CODE_RE = re.compile(r"^[A-Z]{1,6}\d")

def group_key(stem):
    s = stem.replace(" copy", "").replace("-Recovered", "").strip()
    s = re.sub(r"\s*\((?:Platinum|Small Version)\)", "", s)
    s = re.sub(r"\s*\(\d\)$", "", s)          # view index " (1)"
    s = re.sub(r"(?<=[A-Z0-9])[-\s]\d$", "", s)  # view index "-1"
    s = re.sub(r"\s*\(?F\)?$", "", s) if re.search(r"\(F\)$", s) else s
    return s.strip(" -_")

def is_code(s):
    return bool(CODE_RE.match(s.upper())) and not s.upper().startswith("PHOTO")

def process(job):
    src, dst, mode = job
    if os.path.exists(dst):
        return dst, True
    try:
        im = Image.open(src)
        im.draft("RGB", (2400, 2400))
        if mode == "pgi":
            im = im.convert("RGB"); w, h = im.size
            im = im.crop((int(w*.12), int(h*.14), int(w*.88), int(h*.86)))
            im.thumbnail((720, 720), Image.LANCZOS)
            im.save(dst, "WEBP", quality=80, method=5)
            return dst, True
        im = im.convert("RGBA")
        a = im.split()[3]
        opaque = a.getextrema()[0] == 255
        if opaque:  # knock out near-white / light-grey studio background
            g = ImageOps.grayscale(im)
            mask = g.point(lambda v: 0 if v > 242 else 255)
            im.putalpha(mask)
            a = mask
        bbox = a.getbbox() or (0, 0) + im.size
        im = im.crop(bbox)
        w, h = im.size; side = int(max(w, h) * 1.12)
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(im, ((side - w)//2, (side - h)//2))
        canvas.thumbnail((760, 760), Image.LANCZOS)
        canvas.save(dst, "WEBP", quality=82, method=5)
        return dst, not opaque
    except Exception as e:
        print("ERR", src, e, file=sys.stderr)
        return None, False

def main():
    catalog, jobs = {}, []
    for col, cats in MAP.items():
        items = {}
        os.makedirs(f"{OUT}/p/{col}", exist_ok=True)
        for cat, folder, prefix in cats:
            path = f"{SRC}/{folder}"
            files = sorted(f for f in os.listdir(path) if f.lower().endswith(".png"))
            if folder == "PT_Mine":
                files = [f for f in files if "-PT" in f]
            n = 0
            for f in files:
                stem = f[:-4]
                key = group_key(stem)
                if not is_code(key):
                    n += 1; key = f"{prefix}-{n:02d}"
                code = key.upper().replace("_", "-").replace(" ", "-")
                gid = f"{cat}|{code}"
                slug = re.sub(r"[^a-z0-9]+", "-", f"{prefix}-{stem}".lower()).strip("-")
                dst = f"{OUT}/p/{col}/{slug}.webp"
                jobs.append((f"{path}/{f}", dst, "cut"))
                it = items.setdefault(gid, {"code": code, "cat": cat, "views": []})
                it["views"].append(f"assets/p/{col}/{slug}.webp")
        for folder in PGI.get(col, []):
            path = f"{SRC}/{folder}"
            for f in sorted(os.listdir(path)):
                if not f.lower().endswith((".png", ".jpg")):
                    continue
                stem = os.path.splitext(f)[0]
                slug = re.sub(r"[^a-z0-9]+", "-", f"pgi-{stem}".lower()).strip("-")
                dst = f"{OUT}/p/{col}/{slug}.webp"
                jobs.append((f"{path}/{f}", dst, "pgi"))
                items[f"PGI|{stem}"] = {"code": stem.upper().replace(" ", "-"), "cat": "PGI Campaign Picks",
                                        "views": [f"assets/p/{col}/{slug}.webp"], "pgi": True}
        for it in items.values():
            it["views"] = sorted(it["views"])
        catalog[col] = list(items.values())
    print("jobs", len(jobs))
    with ProcessPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(process, jobs, chunksize=4))
    bad = [j[0] for j, r in zip(jobs, res) if r[0] is None]
    print("failed", len(bad), bad[:5])
    print("opaque-knocked", sum(1 for j, r in zip(jobs, res) if r[0] and not r[1] and j[2] == "cut"))
    json.dump(catalog, open(f"{OUT}/../_build/catalog.json", "w"), indent=1)
    for c, v in catalog.items():
        print(c, len(v), "designs")

if __name__ == "__main__":
    main()
