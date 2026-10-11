"""Watercolor paper texture (multiply overlay)."""
import os, numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
rng = np.random.default_rng(11)
def blob(scale):
    small = rng.random((H // scale + 2, W // scale + 2))
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(scale / 3)), dtype=np.float32) / 255
low = 0.55 * blob(180) + 0.3 * blob(60) + 0.15 * blob(20)
grain = rng.random((H, W)).astype(np.float32)
grain = np.asarray(Image.fromarray((grain * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float32) / 255
yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.28 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
v = (0.86 + 0.12 * low + 0.06 * (grain - 0.5)) * vig
v = np.clip(v, 0, 1)
rgb = np.stack([v * 1.0, v * 0.975, v * 0.93], -1)
Image.fromarray((rgb * 255).astype(np.uint8)).save(os.path.join(ROOT, "assets/paper.png"), optimize=True)
print("paper ok")
