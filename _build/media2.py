"""v9: bring in the photography and films not used before (excludes Diago and PT_Mine)."""
import os, glob, subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps, ImageEnhance
Image.MAX_IMAGE_PIXELS = None
R = r"F:/disha_platinum/PNG IMAGES-20260928T095426Z-1-001/PNG IMAGES"
R2 = r"F:/disha_platinum/PNG IMAGES-20260928T095426Z-1-002/PNG IMAGES"
AMAN = R + "/Raw Photos & Videos/Aman Photography"
A = r"F:/disha_platinum/website/assets"

def save(src, dst, maxw=1400, q=80, crop=(0, 0, 1, 1), enhance=False):
    if os.path.exists(dst): return
    im = Image.open(src); im.draft("RGB", (2600, 2600)); im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size; im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    if enhance:
        im = ImageOps.autocontrast(im, cutoff=0.4); im = ImageEnhance.Contrast(im).enhance(1.06)
    im.thumbnail((maxw, maxw), Image.LANCZOS); os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "WEBP", quality=q, method=5); print("img", os.path.basename(dst))

jobs = []
# prop-shoot frames not used yet
for p in ["SHA00036","SHA00045","SHA00046","SHA00050","SHA00053","SHA00057","SHA00059","SHA00062","SHA00081","SHA00089",
          "SHA00098","SHA00102","SHA00104","SHA00107","SHA00115","SHA00119","SHA00130","SHA00145","SHA00147","1337 (2)","new1"]:
    f = glob.glob(f"{AMAN}/PHOTO SHOOT WITH PROPS/{p}.*")[0]
    n = p.lower().replace(" ", "").replace("(", "").replace(")", "")
    jobs.append((f, f"{A}/props/{n}.webp"))
# studio raw frames (curated: no hands / tags in frame), trimmed to the paper
studio = {"New folder (2)/IMG_1388.JPG": (.08,.12,.92,.9), "New folder (2)/IMG_1390.JPG": (.1,.1,.9,.9), "New folder (2)/IMG_1392.JPG": (.12,.18,.88,.82),
          "New folder (2)/IMG_1394.JPG": (.06,.06,.94,.94), "New folder (2)/IMG_1400.JPG": (.08,.08,.92,.92), "New folder (2)/IMG_1403.JPG": (.06,.06,.94,.94),
          "New folder (2)/IMG_1404.JPG": (.06,.1,.94,.9), "New folder (2)/IMG_1407.JPG": (.04,.06,.96,.94), "New folder (2)/IMG_1408.JPG": (.04,.04,.96,.96),
          "New folder (2)/IMG_1410.JPG": (.04,.06,.96,.94), "New folder (2)/IMG_1423.JPG": (.06,.06,.94,.94), "New folder (2)/IMG_1427.JPG": (.06,.06,.94,.94),
          "New folder (2)/IMG_1429.JPG": (.12,.14,.88,.86), "New folder (2)/neckless photo copy.jpg": (0,0,1,1), "New folder (2)/Untitled-1 copy.jpg": (0,0,1,1),
          "New folder/New folder/IMG_1546.JPG": (.08,.04,.92,.96), "New folder/New folder/IMG_1548.JPG": (.08,.04,.92,.96), "New folder/New folder/IMG_1549.JPG": (.1,.1,.9,.9),
          "New folder/New folder/IMG_1594.JPG": (.04,.04,.96,.96), "New folder/New folder/IMG_1600.JPG": (.06,.1,.94,.9), "New folder/New folder/IMG_1605.JPG": (.1,.14,.9,.86),
          "New folder/New folder/IMG_1613.JPG": (.1,.1,.9,.9), "New folder/New folder/IMG_1617.JPG": (.1,.1,.9,.9), "New folder/IMG_1603.JPG": (.1,.1,.9,.9)}
for k, (f, c) in enumerate(studio.items()):
    jobs.append((f"{AMAN}/{f}", f"{A}/studio/st{k+1:02d}.webp", c))
with ThreadPoolExecutor(6) as ex:
    list(ex.map(lambda j: save(j[0], j[1], crop=j[2] if len(j) > 2 else (0, 0, 1, 1), enhance=len(j) > 2), jobs))

# films not used yet (Aman "Video" folders in both archives)
def vid(src, dst, t=12):
    if os.path.exists(dst): return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", str(t), "-vf", "scale=540:-2,fps=30", "-an", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", dst, "-frames:v", "1", "-q:v", "4", dst[:-4] + ".jpg"], check=True)
    print("vid", os.path.basename(dst))
movs = [m for m in sorted(glob.glob(AMAN + "/Photography ok file/Video/*.MOV") + glob.glob(R2 + "/Raw Photos & Videos/Aman Photography/Photography ok file/Video/*.MOV"))
        if os.path.basename(m) not in ("IMG_6095.MOV", "IMG_6099.MOV", "IMG_6103(1).MOV")]
os.makedirs(A + "/video", exist_ok=True)
with ThreadPoolExecutor(3) as ex:
    list(ex.map(lambda km: vid(km[1], f"{A}/video/studio-{km[0]+1}.mp4"), enumerate(movs)))
print("done", len(movs), "films")
