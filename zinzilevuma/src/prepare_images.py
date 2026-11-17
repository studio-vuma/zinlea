"""One-off image preparation: resize, compress and export JPEG + WebP.
Usage: python3 prepare_images.py <source_dir> <portrait.jpg> <site_img_dir>"""
import sys, os
from PIL import Image, ImageOps
src, portrait, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)

def save(im, name, widths):
    for w in widths:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS) if im.width > w else im
        r.save(f"{out}/{name}-{w}.jpg", quality=78, optimize=True, progressive=True)
        r.save(f"{out}/{name}-{w}.webp", quality=74, method=6)

def crop(im, ratio, cx=0.5, cy=0.5):
    W, H = im.size
    if W / H > ratio:
        w = round(H * ratio); x = min(max(round(W * cx - w / 2), 0), W - w)
        return im.crop((x, 0, x + w, H))
    h = round(W / ratio); y = min(max(round(H * cy - h / 2), 0), H - h)
    return im.crop((0, y, W, y + h))

# Landscape photographs: 3:2 for features and 4:3 for teasers
for f in sorted(os.listdir(src)):
    if not f.endswith(".jpg") or os.path.getsize(os.path.join(src, f)) == 0: continue
    name = f[:-4]
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert("RGB")
    save(crop(im, 3 / 2), name, [800, 1600])
    print("prepared", name)

# Portrait: 4:5 for the hero, 1:1 close crop, 3:4 for About
p = ImageOps.exif_transpose(Image.open(portrait)).convert("RGB")
W, H = p.size
save(crop(p, 4 / 5, cx=0.62), "zv-portrait-4x5", [640, 1040])
close = p.crop((int(W * 0.30), int(H * 0.05), int(W * 0.30) + int(W * 0.62), int(H * 0.05) + int(W * 0.62)))
save(close, "zv-portrait-1x1", [480, 740])
save(crop(p, 3 / 4, cx=0.6), "zv-portrait-3x4", [640, 990])
print("portrait done")
