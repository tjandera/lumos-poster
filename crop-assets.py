#!/usr/bin/env python3
"""
Crop the raw app screenshots to complete, self-contained regions.

The poster previously used CSS `object-fit: cover`, which sliced through the middle
of each screenshot. Instead we crop here to a region that is whole on its own terms
(a full dialog, the full plan view), so the poster can show the entire cropped image
with nothing cut off.

Boxes are (left, top, right, bottom) in the 1600x1000 source.
Run:  python3 crop-assets.py
"""
from PIL import Image
import os

SRC = "lumos/docs/media"
OUT = "assets"

CROPS = {
    # The whole "Where is this room?" dialog: map, sun bearings, and the
    # coordinate readout showing privacy rounding.
    "location":    (305, 95, 1300, 905),
    # The lighting panel from ORIENTATION through the lux verdict, plus enough of the
    # heatmap to read as spatial. Kept near 2:1 so it sits beside the other shots.
    "lighting":    (10, 440, 960, 900),
    # The whole Image Generation Day dialog with its twelve solar moments.
    "image-day":   (300, 355, 1310, 650),
    # The plan editor: full room with dimensions and labelled furniture.
    "plan-editor": (322, 145, 1283, 858),
    # The light study modal: render, scrub bar, and the 24-frame note.
    "light-study": (375, 118, 1232, 878),
}

os.makedirs(OUT, exist_ok=True)

# Two frames out of the day-cycle animation, same room and camera, different sun.
# Frame 2 is cool morning light; frame 16 is warm late-afternoon light.
# NOTE: these are frames of the shipped animation, not captures at a stated clock
# time. If you want "09:00" and "16:30" printed on the poster, capture those two
# moments in the app and drop them in as day-early.jpg / day-late.jpg.
GIF_FRAMES = {"day-early": 2, "day-late": 16}
GIF_BOX = (25, 20, 625, 465)

from PIL import ImageSequence
_gif = Image.open(os.path.join(SRC, "day-cycle.gif"))
_frames = [f.convert("RGB") for f in ImageSequence.Iterator(_gif)]
for name, idx in GIF_FRAMES.items():
    im = _frames[idx].crop(GIF_BOX)
    dst = os.path.join(OUT, f"{name}.jpg")
    im.save(dst, "JPEG", quality=90, optimize=True)
    w, h = im.size
    print(f"{name:12s} {w:4d}x{h:4d}  aspect {w/h:.2f}  {os.path.getsize(dst)//1024:4d} KB  (gif frame {idx})")

for name, box in CROPS.items():
    src = os.path.join(SRC, f"{name}.png")
    im = Image.open(src).convert("RGB")
    cropped = im.crop(box)
    # Cap the long edge so the embedded base64 stays reasonable; still well above
    # 300 dpi at the sizes used on the poster.
    cropped.thumbnail((1400, 1400), Image.LANCZOS)
    dst = os.path.join(OUT, f"{name}.jpg")
    cropped.save(dst, "JPEG", quality=88, optimize=True)
    w, h = cropped.size
    print(f"{name:12s} {w:4d}x{h:4d}  aspect {w/h:.2f}  {os.path.getsize(dst)//1024:4d} KB")
