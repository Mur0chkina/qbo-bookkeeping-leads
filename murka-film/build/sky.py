"""Pencil-hatched night sky (flat colour + crayon strokes), pre-rendered."""
import os, math, random
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
top, mid, bot = (58, 52, 128), (78, 76, 156), (46, 70, 134)
im = Image.new("RGB", (W, H))
px = im.load()
for y in range(H):
    t = y / H
    a, b, u = (top, mid, t / 0.55) if t < 0.55 else (mid, bot, (t - 0.55) / 0.45)
    c = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    for x in range(W):
        px[x, y] = c
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
rnd = random.Random(3)
for _ in range(26000):
    x, y = rnd.uniform(-40, W), rnd.uniform(0, H)
    L = rnd.uniform(18, 80); ang = math.radians(rnd.uniform(-9, 5))
    light = rnd.random() < 0.55
    col = (190, 190, 245, rnd.randint(18, 48)) if light else (22, 20, 70, rnd.randint(22, 55))
    d.line([(x, y), (x + L * math.cos(ang), y + L * math.sin(ang))], fill=col, width=rnd.choice([1, 2, 2, 3]))
im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
im.save(os.path.join(ROOT, "assets/sky.png"), optimize=True)
print("sky ok")
