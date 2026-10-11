"""Shared timeline for the Murka film: voice line starts and scene windows."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR, TEXT, VOICE = {}, {}, {}
for row in open(os.path.join(ROOT, "durations.tsv"), encoding="utf-8"):
    lid, v, d, t = row.rstrip("\n").split("\t")
    DUR[lid], TEXT[lid], VOICE[lid] = float(d), t, v

# (scene id, list of (line id, gap before line)), scene tail pad
PLAN = [
    ("s1", [("n1", 2.2), ("n2", 0.5), ("m1", 0.6)], 1.3),
    ("s2", [("n3", 1.4), ("m2", 0.5), ("a1", 0.5)], 0.9),
    ("s3", [("n4", 0.5), ("b1", 0.5)], 0.9),
    ("s4", [("n5", 0.5), ("m3", 0.6)], 0.8),
    ("s5", [("n6", 0.6), ("m4", 0.5)], 0.7),
    ("s6", [("n7", 0.4), ("m5", 0.5), ("m6", 0.5), ("m7", 0.5)], 0.7),
    ("s7", [("a2", 0.6), ("b2", 0.5)], 0.8),
    ("s8", [("n8", 0.5), ("m8", 0.7)], 3.4),
]
START, SCENE = {}, {}
t = 0.0
for sid, lines, tail in PLAN:
    s0 = t
    for lid, gap in lines:
        t += gap
        START[lid] = round(t, 2)
        t += DUR[lid]
    t += tail
    SCENE[sid] = (round(s0, 2), round(t - s0, 2))
TOTAL = round(t, 2)

if __name__ == "__main__":
    for sid, (s, d) in SCENE.items():
        print(sid, s, d)
    for k, v in START.items():
        print(k, v, DUR[k])
    print("TOTAL", TOTAL)
