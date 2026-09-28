import os, glob, subprocess
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
S = r"C:/Users/PRERNA/AppData/Local/Temp/claude/F--Project-learning/f9ac91a8-0fe2-4c26-8c72-05ef6d92f0b4/scratchpad"
R = r"F:/disha_platinum/PNG IMAGES-20260928T095426Z-1-001/PNG IMAGES"
A = r"F:/disha_platinum/website/assets"
AMAN = R + "/Raw Photos & Videos/Aman Photography"
VP = S + "/vp/Value Proposition PPT"

def save(src, dst, maxw=1600, q=80, crop=None, alpha=False):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src); im = ImageOps.exif_transpose(im)
    im = im.convert("RGBA" if alpha else "RGB")
    if crop: 
        w, h = im.size; im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    im.thumbnail((maxw, maxw), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, method=5)

# editorial photography (blue paper shoot)
for f in glob.glob(AMAN + "/Photography ok file/*.jpg"):
    n = os.path.basename(f)[:-4].lower()
    if n in ("1", "2", "3", "4"):  # duplicates of Ph1/Ph2/Ph4/Ph5 crops
        continue
    save(f, f"{A}/lookbook/{n}.webp", 1400, 78)
save(R + "/Raw Photos & Videos/IMG_1612.JPG", f"{A}/lookbook/img1612.webp", 1800, 78)
# prop shoot (couple sets / accessories)
props = ["SHA00035","SHA00037","SHA00038","SHA00041","SHA00047","SHA00061","SHA00066","SHA00079","SHA00087","SHA00092",
         "SHA00097","SHA00109","SHA00118","SHA00122","SHA00131","SHA00136","SHA00146","SHA00151","SHA00153","SHA00155",
         "SHA00171","SHA00183","SHA00195","SHA00200","SHA00201","SHA00203","SHA00313","SHA00318","IMG_2540","IMG_2561","IMG_6327 (2)","IMG_6357"]
for p in props:
    src = f"{AMAN}/PHOTO SHOOT WITH PROPS/{p}.JPG"
    save(src, f"{A}/props/{p.lower().replace(' ','').replace('(','').replace(')','')}.webp", 1400, 78)

# brand marks from decks
opp, zone, fix = S + "/pp/opp", S + "/pp/zone", S + "/pp/fix"
brand = {"logo-evara": f"{opp}/image5.png", "logo-mop": f"{opp}/image7.png", "logo-pdol": f"{opp}/image12.png",
         "logo-pgi": f"{opp}/image14.png", "logo-pt": f"{zone}/image1.png", "pt950-card": f"{opp}/image1.png",
         "pt950-program": f"{opp}/image9.png", "quality-card": f"{opp}/image16.png"}
for k, v in brand.items():
    save(v, f"{A}/brand/{k}.webp", 900, 90, alpha=True)
for k, v in {"store": f"{opp}/image13.png", "training": f"{opp}/image17.png", "campaigns": f"{opp}/image21.png",
             "tray": f"{opp}/image10.png", "evara-campaign": f"{opp}/image6.jpg", "mop-campaign": f"{opp}/image8.jpg",
             "pdol-campaign": f"{opp}/image19.jpg", "gold-vs-pt": f"{opp}/image4.png"}.items():
    save(v, f"{A}/support/{k}.webp", 1400, 80)
# display & counter renders
for i, n in enumerate([2,3,4,5,6,7]):
    ext = "jpeg"
    save(f"{zone}/image{n}.{ext}" if os.path.exists(f"{zone}/image{n}.{ext}") else f"{zone}/image{n}.png", f"{A}/display/zone-{i+1}.webp", 1400, 80)
for i, n in enumerate([8,12,15,16,17,20]):
    save(f"{zone}/image{n}.png", f"{A}/display/prop-{i+1}.webp", 1400, 80)
for i, f in enumerate(["image1.jpg","image3.jpeg","image7.jpg","image11.png","image16.jpeg","image20.jpg","image13.jpeg","image17.jpg"]):
    save(f"{fix}/{f}", f"{A}/display/fixture-{i+1}.webp", 1400, 80)
# vendor logos
for f in glob.glob(VP + "/Assets/VENDOR LOGO/*"):
    n = os.path.basename(f).split(" LOGO")[0].strip().lower().replace(" ", "-")
    save(f, f"{A}/vendors/{n}.webp", 600, 88, alpha=f.lower().endswith(".png"))
# D The Platinum bars & coins
for i in [1, 4, 5, 6]:
    save(f"{S}/dthe_hi_{i}.png", f"{A}/dthe/dthe-{i}.webp", 1300, 84)

# videos
FF = "ffmpeg"
def vid(src, dst, vf, t=None, ss=0):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    cmd = [FF, "-v", "error", "-y", "-ss", str(ss), "-i", src]
    if t: cmd += ["-t", str(t)]
    cmd += ["-vf", vf, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst]
    subprocess.run(cmd, check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "0.5", "-i", dst, "-frames:v", "1", "-q:v", "4", dst[:-4] + ".jpg"], check=True)
vid(R + "/Raw Photos & Videos/MVI_1409.MP4", f"{A}/video/hero-twotone.mp4", "scale=1600:-2")
vid(R + "/Raw Photos & Videos/MVI_1529.MP4", f"{A}/video/chain-light.mp4", "scale=1280:-2")
vid(f"{AMAN}/Photography ok file/Video/IMG_6095.MOV", f"{A}/video/chain-blue.mp4", "scale=720:-2")
vid(f"{AMAN}/Photography ok file/Video/IMG_6099.MOV", f"{A}/video/chain-blue-2.mp4", "scale=720:-2")
msd = sorted(glob.glob(R + "/MEN OF PLATINUM/MSD PRODUCT VIDEO/*.mp4"))
for i, f in enumerate(msd):
    vid(f, f"{A}/video/men-{i+1}.mp4", "scale=540:-2", t=12)
print("done")
