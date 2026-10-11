"""Music-box score + soft pad, chimes, ducked under voices, mixed to one soundtrack."""
import sys, os, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from timing import START, DUR, TOTAL, SCENE, ROOT
SR = 44100
N = int((TOTAL + 0.5) * SR)
rng = np.random.default_rng(7)
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def musicbox(f, dur=2.6, amp=0.22):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 2.8) * np.minimum(1, t / 0.004)
    s = (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*f*2*t)*np.exp(-t*4) + 0.12*np.sin(2*np.pi*f*4.07*t)*np.exp(-t*9))
    return amp * env * s
def pad(freqs, dur, amp=0.05):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    s = sum(np.sin(2*np.pi*f*t + i) + 0.3*np.sin(2*np.pi*f*2.002*t) for i, f in enumerate(freqs))
    return amp * env * s / len(freqs)
mus = np.zeros(N)
def add(buf, sig, at):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[: j - i]
BEAT = 60 / 66  # 66 bpm, 3/4 waltz
# chords as midi roots + triad; first half wistful, second half warm
sad = [(57, [57,60,64]), (53, [53,57,60]), (48, [48,52,55]), (55, [55,59,62])]   # Am F C G
warm = [(48, [48,52,55]), (55, [55,59,62]), (57, [57,60,64]), (53, [53,57,60])]  # C G Am F
turn = SCENE["s5"][0] + 7.0
t = 0.4; bar = 0
while t < TOTAL - 1.0:
    prog = sad if t < turn else warm
    root, triad = prog[bar % 4]
    bar_len = 3 * BEAT
    add(mus, pad([midi(n) for n in triad], bar_len + 1.0, 0.045 if t < turn else 0.06), t)
    add(mus, musicbox(midi(root - 12), 3.0, 0.10), t)
    tones = [n + 12 for n in triad] + [triad[0] + 24]
    for b in range(3):
        n = tones[rng.integers(len(tones))]
        if rng.random() < 0.85:
            add(mus, musicbox(midi(n), 2.4, 0.13), t + b * BEAT)
        if rng.random() < 0.3:
            add(mus, musicbox(midi(tones[rng.integers(len(tones))]), 1.6, 0.07), t + b * BEAT + BEAT / 2)
    t += bar_len; bar += 1
# chimes: lantern brightening, solution steps, lights coming back
def chime(at, base=84, amp=0.12):
    for k, n in enumerate([base, base + 7, base + 12, base + 16]):
        add(mus, musicbox(midi(n), 2.0, amp), at + k * 0.09)
for at in [START["n6"] + 4.6, START["m5"], START["m6"], START["m7"], START["n8"] + 0.3, START["n8"] + 3.6]:
    chime(at)
# simple reverb
def reverb(x):
    out = x.copy()
    for d, g in [(0.061, .35), (0.113, .28), (0.173, .22), (0.239, .16), (0.331, .12), (0.457, .08)]:
        k = int(d * SR); out[k:] += g * x[:-k]
    return out
mus = reverb(mus)
fade = np.ones(N); fl = int(3 * SR); fade[-fl:] = np.linspace(1, 0, fl); fade[:int(1.5*SR)] = np.linspace(0, 1, int(1.5*SR))
mus *= fade
# voices + ducking envelope
voice = np.zeros(N); duck = np.ones(N)
for lid, st in START.items():
    v, sr = sf.read(os.path.join(ROOT, "assets/vo", lid + ".wav"))
    if v.ndim > 1: v = v.mean(1)
    assert sr == SR, sr
    add(voice, v, st)
    i, j = int((st - 0.25) * SR), int((st + DUR[lid] + 0.35) * SR)
    duck[max(0, i):j] = 0.38
k = int(0.25 * SR); kern = np.ones(k) / k
duck = np.convolve(duck, kern, mode="same")
mix = voice * 0.95 + mus * duck * 0.9
mix /= max(1.0, np.abs(mix).max() / 0.97)
sf.write(os.path.join(ROOT, "assets/soundtrack.wav"), mix.astype(np.float32), SR)
print("soundtrack", len(mix) / SR, "peak", np.abs(mix).max())
