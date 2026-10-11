"""Generate index.html for the Murka film (watercolor / Little-Prince look, anime eyes)."""
import os, re, sys, math, random, json
sys.path.insert(0, os.path.dirname(__file__))
from timing import START, DUR, TEXT, VOICE, SCENE, TOTAL, ROOT

W, H = 1080, 1920
INK = "#1d1b2c"
XF = 0.7  # crossfade length between scenes
JS = []   # timeline statements


def js(s):
    JS.append(s)


def strip_fill(el):
    return re.sub(r'\sfill="[^"]*"', "", el)


def wc(fills, inks=(), sw=4.2, flt="wc"):
    """Watercolor fill layer + wobbly ink outline layer."""
    f = "".join(fills)
    outline = "".join(strip_fill(e) for e in fills if 'data-noink' not in e)
    return (f'<g filter="url(#{flt})">{f}</g>'
            f'<g filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{outline}{"".join(inks)}</g>')


def on_planet(cx, cy, r, a):
    rad = math.radians(a)
    return f"translate({cx + r * math.sin(rad):.1f},{cy - r * math.cos(rad):.1f}) rotate({a})"


# ---------------------------------------------------------------- characters
GINGER, CREAM, PINK = "#ef8f4f", "#f7dfbf", "#f2a0a0"


def murka(p, look=(0, 0), ears_down=False):
    lx, ly = look
    ear_l = ("M-92,-292 L-104,-372 L-36,-322 Z", "M-84,-302 L-92,-352 L-52,-320 Z")
    ear_r = ("M92,-292 L104,-372 L36,-322 Z", "M84,-302 L92,-352 L52,-320 Z")
    def eye(cx, side):
        return (f'<g id="{p}-eye{side}" transform="translate({cx},-238)"><g class="eyeblink">'
                f'<ellipse rx="31" ry="37" fill="#fffdf6" stroke="{INK}" stroke-width="2.5"/>'
                f'<g id="{p}-pupil{side}" transform="translate({lx},{ly})">'
                f'<ellipse rx="25" ry="31" fill="url(#iris)"/>'
                f'<ellipse cy="3" rx="12" ry="17" fill="#1d2235"/>'
                f'<circle class="hl" cx="-9" cy="-13" r="8.5" fill="#fff"/>'
                f'<circle cx="9" cy="13" r="4" fill="#fff" opacity=".9"/></g>'
                f'<path d="M-34,-14 Q0,-46 34,-14" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M{28 if side == "R" else -28},-20 l{10 if side == "R" else -10},-9" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                f'</g></g>')
    return f'''<g id="{p}">
  <g id="{p}-tail">{wc([f'<path d="M38,-62 C112,-70 136,-142 98,-190 C86,-205 68,-198 74,-182 C102,-142 86,-98 30,-88 Z" fill="{GINGER}"/>'])}</g>
  <g id="{p}-scarf">{wc([f'<path d="M40,-130 C90,-134 128,-152 176,-142 C206,-136 226,-152 244,-164 C236,-130 208,-112 176,-115 C136,-118 96,-104 46,-110 Z" fill="#f4c644"/>'])}</g>
  {wc([f'<path d="M-62,-10 C-76,-80 -62,-142 0,-147 C62,-142 76,-80 62,-10 C40,3 -40,3 -62,-10 Z" fill="{GINGER}"/>',
       f'<ellipse cx="0" cy="-62" rx="38" ry="48" fill="{CREAM}"/>',
       f'<ellipse cx="-30" cy="-7" rx="27" ry="13" fill="{CREAM}"/>',
       f'<ellipse cx="30" cy="-7" rx="27" ry="13" fill="{CREAM}"/>'])}
  <g id="{p}-armL">{wc([f'<ellipse cx="-66" cy="-92" rx="16" ry="31" fill="{GINGER}" transform="rotate(18 -66 -92)"/>'])}</g>
  <g id="{p}-armR">{wc([f'<ellipse cx="66" cy="-92" rx="16" ry="31" fill="{GINGER}" transform="rotate(-18 66 -92)"/>'])}</g>
  {wc([f'<path d="M-60,-142 C-30,-122 30,-122 60,-142 L58,-116 C30,-100 -30,-100 -58,-116 Z" fill="#f4c644"/>'])}
  <g id="{p}-head">
    <g id="{p}-earL">{wc([f'<path d="{ear_l[0]}" fill="{GINGER}"/>', f'<path d="{ear_l[1]}" fill="{PINK}" data-noink="1"/>'])}</g>
    <g id="{p}-earR">{wc([f'<path d="{ear_r[0]}" fill="{GINGER}"/>', f'<path d="{ear_r[1]}" fill="{PINK}" data-noink="1"/>'])}</g>
    {wc([f'<ellipse cx="0" cy="-246" rx="114" ry="100" fill="{GINGER}"/>',
         f'<ellipse cx="0" cy="-198" rx="74" ry="46" fill="{CREAM}" data-noink="1"/>'])}
    <g stroke="#c4682e" stroke-width="7" stroke-linecap="round" opacity=".8" filter="url(#ink)">
      <path d="M-20,-336 L-13,-306"/><path d="M0,-343 L0,-309"/><path d="M20,-336 L13,-306"/></g>
    {eye(-46, "L")}{eye(46, "R")}
    <ellipse cx="-80" cy="-198" rx="17" ry="9" fill="#f39a9a" opacity=".55"/>
    <ellipse cx="80" cy="-198" rx="17" ry="9" fill="#f39a9a" opacity=".55"/>
    <path d="M-9,-212 L9,-212 L0,-202 Z" fill="#e98585"/>
    <ellipse id="{p}-mouth" cx="0" cy="-186" rx="10" ry="9" fill="#8c2f39"/>
    <path d="M-15,-197 Q-7,-187 0,-196 Q7,-187 15,-197" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    <g stroke="{INK}" stroke-width="2" stroke-linecap="round" opacity=".8">
      <path d="M-72,-212 L-124,-222"/><path d="M-72,-202 L-126,-200"/>
      <path d="M72,-212 L124,-222"/><path d="M72,-202 L126,-200"/></g>
    <path id="{p}-tear" d="M-46,-196 C-52,-184 -50,-174 -44,-174 C-38,-174 -38,-184 -46,-196 Z" fill="#9fd3f5" opacity="0"/>
  </g>
</g>'''


SKIN = "#f6d7b9"


def man1(p, pose="scroll"):
    """Lonely scroller: sits hunched; pose 'up' = phone on the ground, looking up."""
    head_y, head_x = (-178, 22) if pose == "scroll" else (-196, 10)
    phone = ""
    if pose == "scroll":
        phone = f'''<g id="{p}-glow"><circle cx="80" cy="-118" r="150" fill="url(#phoneGlow)"/></g>
      <g transform="translate(66,-138) rotate(-18)">
        <rect width="30" height="50" rx="5" fill="#26324f" stroke="{INK}" stroke-width="2.5"/>
        <rect x="3.5" y="5" width="23" height="40" rx="2" fill="#a9d6ff"/>
        <g clip-path="url(#phoneClip)"><g id="{p}-scroll">
          <rect x="6" y="8" width="17" height="4" fill="#5d8fd6"/><rect x="6" y="16" width="12" height="4" fill="#5d8fd6"/>
          <rect x="6" y="24" width="17" height="4" fill="#5d8fd6"/><rect x="6" y="32" width="10" height="4" fill="#5d8fd6"/>
          <rect x="6" y="40" width="17" height="4" fill="#5d8fd6"/><rect x="6" y="48" width="12" height="4" fill="#5d8fd6"/>
        </g></g></g>'''
    else:
        phone = f'<g transform="translate(108,-6) rotate(4)"><rect width="48" height="10" rx="3" fill="#26324f" stroke="{INK}" stroke-width="2.5"/></g>'
    eyes = (f'<path d="M{head_x-16},{head_y+2} q6,4 12,0 M{head_x+8},{head_y+2} q6,4 12,0" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            if pose == "scroll" else
            f'<circle cx="{head_x-12}" cy="{head_y-2}" r="5.5" fill="{INK}"/><circle cx="{head_x+14}" cy="{head_y-2}" r="5.5" fill="{INK}"/>'
            f'<circle cx="{head_x-10}" cy="{head_y-4}" r="1.8" fill="#fff"/><circle cx="{head_x+16}" cy="{head_y-4}" r="1.8" fill="#fff"/>')
    arm = ('<path d="M10,-110 C30,-95 55,-100 72,-118" fill="none" stroke="#6f7fa8" stroke-width="22" stroke-linecap="round"/>'
           if pose == "scroll" else
           f'<path id="{p}-arm" d="M12,-112 C40,-120 58,-150 70,-185" fill="none" stroke="#6f7fa8" stroke-width="22" stroke-linecap="round"/>')
    return f'''<g id="{p}">
  {wc([f'<path d="M18,-24 L104,-24 C112,-24 114,-2 104,0 L18,0 Z" fill="#3e4a6e"/>',
       f'<path d="M-58,0 C-72,-62 -56,-134 -8,-144 C34,-150 58,-112 56,-62 L64,-12 C40,4 -36,4 -58,0 Z" fill="#6f7fa8"/>',
       f'<ellipse cx="{head_x}" cy="{head_y}" rx="44" ry="46" fill="{SKIN}"/>',
       f'<path d="M{head_x-46},{head_y-8} C{head_x-50},{head_y-60} {head_x+40},{head_y-70} {head_x+46},{head_y-14} C{head_x+20},{head_y-38} {head_x-20},{head_y-34} {head_x-46},{head_y-8} Z" fill="#5a463c"/>'])}
  <g filter="url(#ink)">{arm}</g>
  {eyes}
  <ellipse id="{p}-mouth" cx="{head_x+2}" cy="{head_y+24}" rx="8" ry="6" fill="#8c2f39"/>
  <path d="M{head_x-6},{head_y+22} q8,{3 if pose == "up" else -2} 16,0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
  {f'<ellipse cx="{head_x}" cy="{head_y}" rx="44" ry="46" fill="#6aa6ff" opacity=".22"/>' if pose == "scroll" else ""}
  {phone}
</g>'''


def man2(p, pose="selfie"):
    """Like-counter: standing young man with a spiky tuft; pose 'wave' = phone away, waving."""
    arm_end = "C46,-196 64,-250 70,-292" if pose == "selfie" else "C50,-200 74,-236 92,-268"
    phone = (f'''<g id="{p}-glow"><circle cx="72" cy="-310" r="120" fill="url(#phoneGlow)"/></g>
      <g transform="translate(56,-336) rotate(-8)"><rect width="30" height="50" rx="5" fill="#26324f" stroke="{INK}" stroke-width="2.5"/>
      <rect x="3.5" y="5" width="23" height="40" rx="2" fill="#ffc2d6"/></g>''' if pose == "selfie" else "")
    face_x = 0
    eyes = (f'<circle cx="-14" cy="-318" r="5" fill="{INK}"/><circle cx="12" cy="-318" r="5" fill="{INK}"/>'
            f'<circle cx="-12" cy="-320" r="1.7" fill="#fff"/><circle cx="14" cy="-320" r="1.7" fill="#fff"/>')
    return f'''<g id="{p}">
  {wc([f'<path d="M-30,-140 L-34,0 L-8,0 L-4,-120 L4,-120 L8,0 L34,0 L30,-140 Z" fill="#34424f"/>',
       f'<path d="M-46,-120 C-56,-180 -40,-252 0,-258 C40,-252 56,-180 46,-120 C20,-110 -20,-110 -46,-120 Z" fill="#5e9c8f"/>',
       f'<ellipse cx="{face_x}" cy="-308" rx="40" ry="44" fill="{SKIN}"/>',
       f'<path d="M-42,-318 C-46,-372 40,-378 44,-322 C30,-342 6,-344 -6,-336 C-6,-352 -18,-366 -26,-360 C-20,-350 -24,-340 -42,-318 Z" fill="#c9a24a"/>'])}
  <g id="{p}-armR" filter="url(#ink)"><path d="M30,-222 {arm_end}" fill="none" stroke="#5e9c8f" stroke-width="20" stroke-linecap="round"/></g>
  <path d="M-30,-222 C-50,-200 -56,-176 -52,-150" fill="none" stroke="#5e9c8f" stroke-width="20" stroke-linecap="round" filter="url(#ink)"/>
  {eyes}
  <ellipse id="{p}-mouth" cx="0" cy="-286" rx="8" ry="6" fill="#8c2f39"/>
  <path d="M-8,-288 q8,{-2 if pose == "selfie" else 4} 16,0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
  <ellipse cx="-26" cy="-296" rx="8" ry="4.5" fill="#f39a9a" opacity=".5"/><ellipse cx="26" cy="-296" rx="8" ry="4.5" fill="#f39a9a" opacity=".5"/>
  {phone}
</g>'''


def lantern(p, lit=0.0, s=1.0):
    return f'''<g id="{p}" transform="scale({s})">
  <g id="{p}-glow" opacity="{lit}"><circle cy="-178" r="150" fill="url(#lampGlow)"/></g>
  <path d="M0,0 L0,-150" stroke="{INK}" stroke-width="5" filter="url(#ink)"/>
  <path d="M-30,-150 L30,-150" stroke="{INK}" stroke-width="5" stroke-linecap="round" filter="url(#ink)"/>
  {wc([f'<path d="M-22,-152 L-26,-200 L26,-200 L22,-152 Z" fill="#9aa0b5"/>',
       f'<path d="M-34,-200 L0,-226 L34,-200 Z" fill="#7b5a4a"/>'])}
  <path id="{p}-flame" d="M-17,-156 L-20,-196 L20,-196 L17,-156 Z" fill="#ffd979" opacity="{lit}"/>
</g>'''


def planet(p, cx, cy, r, color, seed=1):
    rnd = random.Random(seed)
    craters = []
    for _ in range(4):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0.2, 0.7) * r
        cr = rnd.uniform(0.07, 0.13) * r
        craters.append(f'<ellipse cx="{cx + d*math.cos(a):.0f}" cy="{cy + d*math.sin(a) + 0.15*r:.0f}" rx="{cr:.0f}" ry="{cr*0.7:.0f}" fill="#000" opacity=".1" data-noink="1"/>')
    tufts = []
    for a in rnd.sample(range(-80, 81, 8), 12):
        rad = math.radians(a)
        x, y = cx + r * math.sin(rad), cy - r * math.cos(rad)
        tufts.append(f'<path d="M-8,2 L-3,-14 L0,0 L4,-18 L8,2" transform="translate({x:.0f},{y:.0f}) rotate({a})" fill="none" stroke="#a6dba8" stroke-width="2.5" opacity=".85"/>')
    blades = []
    for _ in range(int(6 + r / 9)):
        a2 = rnd.uniform(0, 2 * math.pi); d2 = math.sqrt(rnd.random()) * r * 0.88
        x, y = cx + d2 * math.cos(a2), cy + d2 * math.sin(a2)
        L = rnd.uniform(0.05, 0.11) * r
        blades.append(f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-2, 3):.1f},{-L:.1f}" stroke="#e8f4ff" stroke-width="{max(1.5, r * 0.012):.1f}" opacity="{rnd.uniform(.25, .5):.2f}" stroke-linecap="round"/>')
    return (f'<g id="{p}">' + wc([f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'] + craters, tufts, sw=3.5)
            + "".join(blades) + f'<path d="M{cx - r*0.75:.0f},{cy - r*0.25:.0f} A{r*0.8:.0f},{r*0.8:.0f} 0 0 1 {cx - r*0.15:.0f},{cy - r*0.78:.0f}" fill="none" stroke="#fff" stroke-width="{max(2, r*0.025):.1f}" opacity=".35" stroke-linecap="round"/></g>')


def birds(p, n=5):
    out = []
    for i in range(n):
        x, y = -90 + i * 45 + (i % 2) * 10, -60 - (i % 3) * 38
        out.append(f'<line x1="0" y1="0" x2="{x}" y2="{y + 6}" stroke="#f5ecd6" stroke-width="1.6" opacity=".8"/>'
                   f'<g transform="translate({x},{y})"><path class="wing" d="M-22,0 Q-11,-14 0,0 Q11,-14 22,0" fill="none" stroke="#f8f1e2" stroke-width="5" stroke-linecap="round"/></g>')
    return f'<g id="{p}">{"".join(out)}</g>'


def star(x, y, s, cls="tw", fill="#fbf8ff"):
    pts = " ".join(f"{(10 if k % 2 == 0 else 3.6) * math.cos(math.pi * k / 8 - math.pi / 2):.1f},{(10 if k % 2 == 0 else 3.6) * math.sin(math.pi * k / 8 - math.pi / 2):.1f}" for k in range(16))
    return (f'<polygon class="{cls}" transform="translate({x:.0f},{y:.0f}) scale({s:.2f})" points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="{1.2 / max(s, .5):.1f}"/>')


def heart(x, y, s, fill):
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,8 C-14,-2 -16,-12 -9,-17 C-4,-20 0,-16 0,-12 C0,-16 4,-20 9,-17 C16,-12 14,-2 0,8 Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')


# ---------------------------------------------------------------- timeline helpers
def flap(mouth, start, dur):
    n = max(1, int(dur / 0.21))
    if n % 2 == 1: n += 1
    js(f'tl.fromTo("#{mouth}",{{scaleY:0}},{{scaleY:1,duration:{dur / n:.3f},ease:"sine.inOut",yoyo:true,repeat:{n - 1},transformOrigin:"50% 0%"}},{start:.2f});')


def blink(p, times):
    for t in times:
        js(f'tl.to("#{p} .eyeblink",{{scaleY:0.08,duration:0.07,yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{t:.2f});')


def idle(p, t0, dur):
    n = max(1, int(dur / 1.6))
    js(f'tl.fromTo("#{p}-scarf",{{skewY:0,scaleX:1}},{{skewY:-7,scaleX:1.06,duration:0.8,ease:"sine.inOut",yoyo:true,repeat:{2 * n - 1},transformOrigin:"0% 50%"}},{t0:.2f});')
    js(f'tl.fromTo("#{p}-tail",{{rotation:0}},{{rotation:9,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:{2 * max(1, int(dur / 2.2)) - 1},svgOrigin:"36 -70"}},{t0:.2f});')
    js(f'tl.set("#{p}-mouth",{{scaleY:0,transformOrigin:"50% 0%"}},{t0:.2f});')
    blink(p, [t0 + 1.4 + k * 3.1 for k in range(int(dur / 3.1))])


def wave(arm, t, reps=3, origin="56 -118"):
    js(f'tl.fromTo("#{arm}",{{rotation:0}},{{rotation:-55,duration:0.22,ease:"sine.inOut",yoyo:true,repeat:{2 * reps - 1},svgOrigin:"{origin}"}},{t:.2f});')


def scene_fade(sid):
    s, d = SCENE[sid]
    if s > 0:
        js(f'tl.fromTo("#{sid}-in",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut"}},{s:.2f});')
    if sid != "s8":
        js(f'tl.to("#{sid}-in",{{opacity:0,duration:{XF},ease:"sine.inOut"}},{s + d:.2f});')


SECTIONS = []


def section(sid, svg, html=""):
    s, d = SCENE[sid]
    dd = d + (XF if sid != "s8" else 0)
    SECTIONS.append(f'''<section id="{sid}" class="clip scene" data-start="{s}" data-duration="{dd:.2f}" data-track-index="1">
<div id="{sid}-in" class="inner"><svg class="full" viewBox="0 0 {W} {H}">{svg}</svg>{html}</div></section>''')


def camera(gid, t0, dur, s0=1.0, s1=1.07, origin="540 1100"):
    js(f'tl.fromTo("#{gid}",{{scale:{s0}}},{{scale:{s1},duration:{dur:.2f},ease:"none",svgOrigin:"{origin}"}},{t0:.2f});')


# ================================================================= S1 intro
s, d = SCENE["s1"]
far = [(170, 760, 46, "#7d6cb3"), (900, 690, 58, "#3f8f8a"), (330, 1010, 34, "#c98a4f"),
       (800, 1000, 40, "#b8676b"), (110, 1180, 28, "#5a72b8"), (980, 1230, 30, "#5f9a52")]
farsvg = ""
for i, (x, y, r, c) in enumerate(far):
    farsvg += (f'<g id="s1-far{i}"><circle id="s1-fg{i}" cx="{x}" cy="{y - r}" r="{r * 2.6}" fill="url(#lampGlow)"/>'
               + planet(f"s1-fp{i}", x, y, r, c, seed=i + 3)
               + f'<circle id="s1-fl{i}" cx="{x}" cy="{y - r - 6}" r="6" fill="#ffd979"/></g>')
PL1 = (540, 1520, 300)
svg = f'''<g id="s1-world">{farsvg}
{planet("s1-home", *PL1, "#3f7d57", seed=1)}
<g transform="{on_planet(*PL1, 40)}">{lantern("s1-lamp", 1.0, 1.0)}</g>
<g id="s1-fly"><g transform="{on_planet(*PL1, -6)} scale(0.82)"><g id="s1-hop">{murka("s1-mk", look=(2, -8))}
  <g transform="translate(-40,-470) scale(1.7)"><g id="s1-birds" opacity="0">{birds("s1-b")}</g></g></g></g></g></g>'''
html = '''<div id="s1-title" class="title"><div class="t-big">Мурка</div><div class="t-sub">сказка о погасших огоньках</div></div>'''
section("s1", svg, html)
camera("s1-world", s, d + XF, 1.0, 1.06, "540 1200")
js(f'tl.fromTo("#s1-title",{{opacity:0,y:40}},{{opacity:1,y:0,duration:1.4,ease:"power2.out"}},0.3);')
js(f'tl.to("#s1-title",{{opacity:0,y:-30,duration:0.9,ease:"power2.in"}},{START["n2"] - 0.6:.2f});')
idle("s1-mk", s, d)
for i in range(len(far)):
    t = START["n2"] + 2.4 + i * 0.45
    js(f'tl.fromTo("#s1-fg{i}",{{opacity:0.9}},{{opacity:0.05,duration:0.8,ease:"power1.in"}},{t:.2f});')
    js(f'tl.fromTo("#s1-fl{i}",{{opacity:1}},{{opacity:0.15,duration:0.6}},{t:.2f});')
js(f'tl.fromTo("#s1-hop",{{y:0}},{{y:-46,duration:0.28,ease:"power2.out",yoyo:true,repeat:1}},{START["m1"] + 0.1:.2f});')
flap("s1-mk-mouth", START["m1"], DUR["m1"])
wave("s1-mk-armR", START["m1"] + 1.2, 2)
tb = START["m1"] + DUR["m1"] - 0.6
js(f'tl.fromTo("#s1-birds",{{opacity:0,y:-200}},{{opacity:1,y:0,duration:0.9,ease:"power2.out"}},{tb:.2f});')
js(f'tl.fromTo("#s1-b .wing",{{scaleY:1}},{{scaleY:-0.6,duration:0.16,yoyo:true,repeat:21,transformOrigin:"50% 50%"}},{tb:.2f});')
js(f'tl.fromTo("#s1-fly",{{x:0,y:0}},{{x:260,y:-1500,duration:1.3,ease:"power2.in"}},{tb + 0.6:.2f});')

# ================================================================= S2 the scroller
s, d = SCENE["s2"]
P2 = (540, 1500, 290)
svg = f'''<g id="s2-world">{planet("s2-pl", *P2, "#7d6cb3", seed=5)}
<g transform="{on_planet(*P2, -48)}">{lantern("s2-lamp", 0.0, 0.9)}</g>
<g transform="{on_planet(*P2, 16)} scale(1.55)">{man1("s2-man", "scroll")}</g>
<g transform="{on_planet(*P2, 360 - 24)} scale(0.74)"><g id="s2-arrive">{murka("s2-mk", look=(10, 0))}
  <g transform="translate(-40,-470) scale(1.7)"><g id="s2-birds">{birds("s2-b")}</g></g></g></g>
<g id="s2-bubble" opacity="0"><path d="M610,880 C600,800 900,790 900,870 C905,930 760,945 700,935 L660,975 L668,930 C625,925 612,905 610,880 Z" fill="#eef4ff" stroke="{INK}" stroke-width="3" filter="url(#ink)"/>
  <text x="755" y="893" class="svgt" text-anchor="middle" font-size="52" fill="#4d6fa8">1000 друзей</text></g></g>'''
section("s2", svg)
camera("s2-world", s, d + XF, 1.0, 1.08, "640 1250")
idle("s2-mk", s, d)
js(f'tl.fromTo("#s2-arrive",{{x:-520,y:-1300}},{{x:0,y:0,duration:1.9,ease:"power2.out"}},{s + 0.1:.2f});')
js(f'tl.fromTo("#s2-b .wing",{{scaleY:1}},{{scaleY:-0.6,duration:0.16,yoyo:true,repeat:23,transformOrigin:"50% 50%"}},{s:.2f});')
js(f'tl.to("#s2-birds",{{y:-900,x:300,opacity:0,duration:1.6,ease:"power2.in"}},{s + 2.2:.2f});')
js(f'tl.fromTo("#s2-man-scroll",{{y:0}},{{y:-16,duration:0.5,ease:"power1.inOut",repeat:{int(d / 0.5)}}},{s:.2f});')
js(f'tl.fromTo("#s2-man-glow",{{opacity:0.75}},{{opacity:1,duration:0.9,yoyo:true,repeat:{2 * int(d / 1.8) - 1},ease:"sine.inOut"}},{s:.2f});')
js(f'tl.set("#s2-man-mouth",{{scaleY:0,transformOrigin:"50% 0%"}},{s:.2f});')
flap("s2-mk-mouth", START["m2"], DUR["m2"])
wave("s2-mk-armR", START["m2"], 3)
flap("s2-man-mouth", START["a1"], DUR["a1"])
js(f'tl.fromTo("#s2-bubble",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(2)",svgOrigin:"660 975"}},{START["a1"] + 0.9:.2f});')
js(f'tl.to("#s2-bubble",{{opacity:0,y:-60,duration:0.9,ease:"power1.in"}},{START["a1"] + 2.9:.2f});')
js(f'tl.fromTo("#s2-mk-head",{{rotation:0}},{{rotation:-10,duration:0.6,ease:"sine.inOut"}},{START["a1"] + 2.8:.2f});')

# ================================================================= S3 the like-counter
s, d = SCENE["s3"]
P3 = (540, 1520, 280)
hearts = ""
for i, (num, dx) in enumerate([("12", -130), ("47", 110), ("100", -80), ("200", 130)]):
    hearts += f'<g id="s3-h{i}" opacity="0"><g transform="translate({dx},0)">{heart(0, 0, 3.2, "#f07a95")}<text x="44" y="14" class="svgt" font-size="54" fill="#ffd1dc">{num}</text></g></g>'
svg = f'''<g id="s3-world">{planet("s3-pl", *P3, "#3f8f8a", seed=8)}
<g transform="{on_planet(*P3, 46)}">{lantern("s3-lamp", 0.0, 0.9)}</g>
<g transform="{on_planet(*P3, 8)} scale(1.45)">{man2("s3-man", "selfie")}</g>
<g transform="{on_planet(*P3, -38)} scale(0.72)">{murka("s3-mk", look=(12, -4))}</g>
<g transform="translate(700,1000)">{hearts}</g></g>'''
section("s3", svg)
camera("s3-world", s, d + XF, 1.03, 1.0, "600 1200")
idle("s3-mk", s, d)
js(f'tl.set("#s3-man-mouth",{{scaleY:0,transformOrigin:"50% 0%"}},{s:.2f});')
js(f'tl.fromTo("#s3-man-glow",{{opacity:0.7}},{{opacity:1,duration:0.8,yoyo:true,repeat:{2 * int(d / 1.6) - 1}}},{s:.2f});')
hstarts = [START["n4"] + 1.6, START["n4"] + 2.8, START["b1"] + 0.1, START["b1"] + 0.9]
for i, t in enumerate(hstarts):
    js(f'tl.fromTo("#s3-h{i}",{{opacity:0,y:0,scale:0.5}},{{opacity:1,y:{-200 - i * 90},scale:1,duration:1.4,ease:"power2.out",transformOrigin:"50% 50%"}},{t:.2f});')
    js(f'tl.to("#s3-h{i} path",{{fill:"#8b8f9e",duration:0.6}},{START["b1"] + 1.7:.2f});')
    js(f'tl.to("#s3-h{i}",{{opacity:0,y:"+=180",duration:1.0,ease:"power2.in"}},{START["b1"] + 2.1 + i * 0.08:.2f});')
flap("s3-man-mouth", START["b1"], DUR["b1"])
js(f'tl.fromTo("#s3-mk-head",{{rotation:0}},{{rotation:9,duration:0.7,ease:"sine.inOut"}},{START["n4"] + 1.0:.2f});')

# ================================================================= S4 the loneliness stat
s, d = SCENE["s4"]
rnd = random.Random(21)
minis = ""
pos = []
for row in range(5):
    for col in range(3):
        x = 180 + col * 360 + rnd.uniform(-60, 60) + (row % 2) * 70 - 35
        y = 230 + row * 230 + rnd.uniform(-40, 40)
        pos.append((x, y))
for i, (x, y) in enumerate(pos):
    r = rnd.uniform(34, 48)
    c = rnd.choice(["#7d6cb3", "#3f8f8a", "#c98a4f", "#5f9a52", "#5a72b8", "#b8676b"])
    minis += (f'<g id="s4-p{i}" opacity="0">{planet(f"s4-pp{i}", x, y, r, c, seed=30 + i)}'
              f'<circle cx="{x + 8}" cy="{y - r - 20}" r="34" fill="url(#phoneGlow)"/>'
              f'<path d="M{x - 6},{y - r + 1} C{x - 9},{y - r - 20} {x + 8},{y - r - 22} {x + 6},{y - r + 1} Z" fill="#59647f"/>'
              f'<circle cx="{x}" cy="{y - r - 27}" r="8" fill="#59647f"/>'
              f'<circle cx="{x + 9}" cy="{y - r - 15}" r="3" fill="#bfe0ff"/></g>')
people = ""
for i in range(6):
    x = 540 - 5 * 60 + i * 120
    col = "#9fd3f5" if i == 3 else "#e9dcc0"
    people += (f'<g id="s4-person{i}"><circle cx="{x}" cy="1150" r="22" fill="{col}"/>'
               f'<path d="M{x - 30},1240 C{x - 30},1190 {x + 30},1190 {x + 30},1240 Z" fill="{col}"/></g>')
PL4 = (540, 2080, 520)
svg = f'''<g id="s4-world">{minis}</g>
<g id="s4-people" opacity="0">{people}</g>
<g id="s4-sad" opacity="0">{planet("s4-home", *PL4, "#3f7d57", seed=1)}
<g transform="translate(540,1562) scale(1.4)">{murka("s4-mk", look=(0, 9), ears_down=True)}</g></g>'''
html = '''<div id="s4-stat" class="stat"><div class="s-big">1 из 6</div><div class="s-mid">людей на Земле одиноки</div><div class="s-src">по данным ВОЗ, 2025</div></div>'''
section("s4", svg, html)
camera("s4-world", s, d + XF, 1.08, 1.0, "540 800")
for i in range(len(pos)):
    js(f'tl.fromTo("#s4-p{i}",{{opacity:0}},{{opacity:1,duration:0.6}},{s + 0.3 + i * 0.22:.2f});')
tstat = START["n5"] + 4.3
js(f'tl.to("#s4-world",{{opacity:0.28,duration:0.8}},{tstat - 0.3:.2f});')
js(f'tl.fromTo("#s4-stat",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.8,ease:"back.out(1.6)"}},{tstat:.2f});')
js(f'tl.fromTo("#s4-people",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.7}},{tstat + 1.2:.2f});')
js(f'tl.fromTo("#s4-person3",{{y:0}},{{y:14,duration:0.6,ease:"sine.inOut"}},{tstat + 2.3:.2f});')
tsad = START["m3"] - 0.6
js(f'tl.to(["#s4-stat","#s4-people"],{{opacity:0,duration:0.6}},{tsad:.2f});')
js(f'tl.to("#s4-world",{{opacity:0.5,duration:0.6}},{tsad:.2f});')
js(f'tl.fromTo("#s4-sad",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},{tsad:.2f});')
idle("s4-mk", s, d)
js(f'tl.fromTo("#s4-mk-earL",{{rotation:0}},{{rotation:-24,duration:0.6,svgOrigin:"-60 -300"}},{tsad + 0.4:.2f});')
js(f'tl.fromTo("#s4-mk-earR",{{rotation:0}},{{rotation:24,duration:0.6,svgOrigin:"60 -300"}},{tsad + 0.4:.2f});')
flap("s4-mk-mouth", START["m3"], DUR["m3"])
js(f'tl.fromTo("#s4-mk-tear",{{opacity:0,y:0}},{{opacity:0.95,y:46,duration:1.6,ease:"power1.in"}},{START["m3"] + 1.4:.2f});')

# ================================================================= S5 the lantern discovery
s, d = SCENE["s5"]
PL5 = (540, 1960, 660)
spark = "".join(star(780 + 230 * math.cos(a), 1010 + 230 * math.sin(a), 2.2, "s5-sp") for a in [i * 0.9 for i in range(7)])
svg = f'''<g id="s5-world">{planet("s5-home", *PL5, "#3f7d57", seed=1)}
<g transform="translate(780,1302) scale(2.1)">{lantern("s5-lamp", 0.25, 1.0)}</g>
<g transform="translate(380,1310) scale(1.25)"><g id="s5-hop">{murka("s5-mk", look=(13, -6))}</g></g>
<g id="s5-sparks" opacity="0"><g id="s5-spin">{spark}</g></g></g>'''
section("s5", svg)
camera("s5-world", s, d + XF, 1.0, 1.08, "620 1150")
idle("s5-mk", s, d)
tl_on = START["n6"] + 4.2
js(f'tl.fromTo("#s5-lamp-glow",{{opacity:0.25,scale:0.7}},{{opacity:1,scale:1.7,duration:2.4,ease:"sine.inOut",transformOrigin:"50% 50%"}},{tl_on:.2f});')
js(f'tl.fromTo("#s5-lamp-flame",{{opacity:0.25}},{{opacity:1,duration:1.6}},{tl_on:.2f});')
js(f'tl.fromTo("#s5-mk .hl",{{scale:1}},{{scale:1.5,duration:0.6,ease:"back.out(3)",transformOrigin:"50% 50%"}},{tl_on - 0.3:.2f});')
js(f'tl.fromTo("#s5-sparks",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:1.2,ease:"power2.out",svgOrigin:"780 1010"}},{tl_on + 1.0:.2f});')
js(f'tl.fromTo("#s5-spin",{{rotation:0}},{{rotation:40,duration:{d - (tl_on - s) + XF:.2f},ease:"none",svgOrigin:"780 1010"}},{tl_on + 1.0:.2f});')
js(f'tl.fromTo("#s5-hop",{{y:0}},{{y:-60,duration:0.3,ease:"power2.out",yoyo:true,repeat:3}},{START["m4"] + 0.2:.2f});')
flap("s5-mk-mouth", START["m4"], DUR["m4"])
wave("s5-mk-armR", START["m4"] + 2.0, 3)

# ================================================================= S6 the solution: Час фонарей
s, d = SCENE["s6"]
icons = [
    f'<svg viewBox="0 0 120 120"><g filter="url(#ink)"><rect x="18" y="62" width="84" height="26" rx="8" fill="#3b4a6b" stroke="{INK}" stroke-width="4"/><path d="M60,18 L60,50 M46,38 L60,52 L74,38" stroke="#c0841f" stroke-width="7" fill="none" stroke-linecap="round"/></g></svg>',
    f'<svg viewBox="0 0 120 120"><g filter="url(#ink)"><path d="M14,52 C14,24 106,24 106,52 C106,80 70,82 56,80 L30,100 L36,78 C20,74 14,64 14,52 Z" fill="#fff6dd" stroke="{INK}" stroke-width="4"/><text x="60" y="66" text-anchor="middle" class="svgt" font-size="44" fill="#c0841f">?</text></g></svg>',
    f'<svg viewBox="0 0 120 120"><g filter="url(#ink)"><path d="M78,96 C64,108 44,98 46,82 C48,70 36,64 36,46 C36,24 54,12 72,14 C92,16 104,34 98,54 C94,66 84,68 84,80 C84,86 82,92 78,96 Z" fill="#f6d7b9" stroke="{INK}" stroke-width="4"/><path d="M58,48 C58,36 78,34 80,48 C80,56 70,58 70,66" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/></g></svg>',
]
steps = [("1", "Телефон — экраном вниз"), ("2", "Спроси: «Как ты на&nbsp;самом деле?»"), ("3", "Слушай, не листая")]
cards = "".join(f'<div id="s6-c{i}" class="card"><div class="c-num">{n}</div><div class="c-ico">{icons[i]}</div><div class="c-txt">{t}</div></div>' for i, (n, t) in enumerate(steps))
svg = f'''<g transform="translate(955,470) scale(0.6)"><g id="s6-hop">{murka("s6-mk", look=(-12, 6))}</g></g>
<g transform="translate(150,500) scale(0.85)">{lantern("s6-lamp", 1.0, 1.0)}</g>'''
html = f'''<div id="s6-title" class="h-title">Час фонарей</div><div class="cards">{cards}</div>'''
section("s6", svg, html)
idle("s6-mk", s, d)
js(f'tl.fromTo("#s6-title",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.8,ease:"power2.out"}},{START["n7"]:.2f});')
js(f'tl.fromTo("#s6-lamp-glow",{{opacity:0.3}},{{opacity:1,duration:0.9,yoyo:true,repeat:{2 * int(d / 1.8) - 1},ease:"sine.inOut"}},{s:.2f});')
for i, lid in enumerate(["m5", "m6", "m7"]):
    js(f'tl.fromTo("#s6-c{i}",{{opacity:0,x:120,rotation:3}},{{opacity:1,x:0,rotation:{[-1.2, 0.8, -0.6][i]},duration:0.7,ease:"back.out(1.4)"}},{START[lid] - 0.15:.2f});')
    flap("s6-mk-mouth", START[lid], DUR[lid])
wave("s6-mk-armL", START["m5"], 2, "-56 -118")

# ================================================================= S7 reconnection
s, d = SCENE["s7"]
A, B = (300, 1270, 210), (800, 960, 190)
la = on_planet(*A, -40); lb = on_planet(*B, 40)
ax, ay = A[0] + A[2] * math.sin(math.radians(-40)), A[1] - A[2] * math.cos(math.radians(-40))
bx, by = B[0] + B[2] * math.sin(math.radians(40)), B[1] - B[2] * math.cos(math.radians(40))
path = f"M{ax:.0f},{ay - 160:.0f} Q{(ax + bx) / 2:.0f},{min(ay, by) - 420:.0f} {bx:.0f},{by - 160:.0f}"
svg = f'''<g id="s7-world">
<path id="s7-thread" d="{path}" fill="none" stroke="#f4cf6b" stroke-width="5" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400" opacity=".9"/>
{planet("s7-pa", *A, "#7d6cb3", seed=5)}{planet("s7-pb", *B, "#3f8f8a", seed=8)}
<g transform="{la}">{lantern("s7-la", 0.0, 0.85)}</g><g transform="{lb}">{lantern("s7-lb", 0.0, 0.85)}</g>
<g transform="{on_planet(*A, 12)} scale(1.3)">{man1("s7-m1", "up")}</g>
<g transform="{on_planet(*B, -10)} scale(1.25)">{man2("s7-m2", "wave")}</g></g>'''
section("s7", svg)
camera("s7-world", s, d + XF, 1.04, 1.0, "540 1100")
for l in ["s7-la", "s7-lb"]:
    js(f'tl.fromTo("#{l}-glow",{{opacity:0}},{{opacity:1,duration:0.9}},{s + 0.3:.2f});')
    js(f'tl.fromTo("#{l}-flame",{{opacity:0}},{{opacity:1,duration:0.7}},{s + 0.3:.2f});')
js(f'tl.to("#s7-thread",{{strokeDashoffset:0,duration:1.6,ease:"power1.inOut"}},{s + 0.8:.2f});')
js(f'tl.set(["#s7-m1-mouth","#s7-m2-mouth"],{{scaleY:0,transformOrigin:"50% 0%"}},{s:.2f});')
flap("s7-m1-mouth", START["a2"], DUR["a2"])
js(f'tl.fromTo("#s7-m1-arm",{{rotation:0}},{{rotation:16,duration:0.22,yoyo:true,repeat:5,svgOrigin:"12 -112"}},{START["a2"]:.2f});')
flap("s7-m2-mouth", START["b2"], DUR["b2"])
js(f'tl.fromTo("#s7-m2-armR",{{rotation:0}},{{rotation:-14,duration:0.24,yoyo:true,repeat:5,svgOrigin:"30 -222"}},{START["b2"] - 0.3:.2f});')

# ================================================================= S8 constellation + ending
s, d = SCENE["s8"]
cat = [(330, 640), (300, 420), (420, 520), (540, 500), (660, 520), (780, 420), (750, 640), (640, 740), (440, 740)]
cons = "".join(star(x, y, 2.6, "s8-cs", "#ffe7a3") for x, y in cat)
cpath = "M" + " L".join(f"{x},{y}" for x, y in cat) + " Z"
rnd = random.Random(5)
skyp = ""
spots = [(150, 1000), (930, 980), (260, 1200), (820, 1210), (120, 820), (960, 800), (420, 990), (680, 1010)]
for i, (x, y) in enumerate(spots):
    r = rnd.uniform(26, 40)
    skyp += (f'<g><circle id="s8-g{i}" cx="{x}" cy="{y - r}" r="{r * 2.8:.0f}" fill="url(#lampGlow)" opacity="0"/>'
             + planet(f"s8-p{i}", x, y, r, rnd.choice(["#7d6cb3", "#3f8f8a", "#c98a4f", "#5f9a52", "#5a72b8"]), seed=50 + i)
             + f'<circle id="s8-l{i}" cx="{x}" cy="{y - r - 6}" r="6" fill="#ffd979" opacity="0.15"/></g>')
PL8 = (540, 1950, 520)
svg = f'''<g id="s8-world">{skyp}
<path id="s8-cline" d="{cpath}" fill="none" stroke="#f4cf6b" stroke-width="3.5" stroke-dasharray="2600" stroke-dashoffset="2600" opacity=".85"/>
<g id="s8-cons" opacity="0">{cons}</g>
{planet("s8-home", *PL8, "#3f7d57", seed=1)}
<g transform="{on_planet(*PL8, 22)}">{lantern("s8-lamp", 1.0, 1.0)}</g>
<g transform="{on_planet(*PL8, -6)} scale(0.95)">{murka("s8-mk", look=(-2, -10))}</g></g>'''
html = '''<div id="s8-label" class="c-label">созвездие «Мурка»</div>
<div id="s8-end" class="endcard"><div class="e-big">Посмотри вверх</div><div class="e-sub">и на того, кто рядом</div></div>'''
section("s8", svg, html)
camera("s8-world", s, d, 1.06, 1.0, "540 900")
idle("s8-mk", s, d)
for i in range(len(spots)):
    t = START["n8"] + 0.3 + i * 0.28
    js(f'tl.fromTo("#s8-g{i}",{{opacity:0}},{{opacity:0.95,duration:0.7}},{t:.2f});')
    js(f'tl.fromTo("#s8-l{i}",{{opacity:0.15}},{{opacity:1,duration:0.5}},{t:.2f});')
tc = START["n8"] + 2.6
js(f'tl.fromTo("#s8-cons",{{opacity:0}},{{opacity:1,duration:0.8}},{tc:.2f});')
js(f'tl.to("#s8-cline",{{strokeDashoffset:0,duration:2.2,ease:"power1.inOut"}},{tc + 0.2:.2f});')
js(f'tl.fromTo("#s8-label",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.8}},{START["n8"] + 4.2:.2f});')
js(f'tl.fromTo(".s8-cs",{{opacity:1}},{{opacity:0.45,duration:0.5,yoyo:true,repeat:{2 * int((d - 4) / 1.0) - 1},stagger:0.13,ease:"sine.inOut"}},{tc + 1.0:.2f});')
flap("s8-mk-mouth", START["m8"], DUR["m8"])
wave("s8-mk-armR", START["m8"] + 0.2, 4)
tend = START["m8"] + DUR["m8"] + 0.1
js(f'tl.to("#s8-label",{{opacity:0,duration:0.5}},{tend - 0.4:.2f});')
js(f'tl.to("#s8-world",{{opacity:0.55,duration:1.0}},{tend:.2f});')
js(f'tl.fromTo("#s8-end",{{opacity:0,y:30}},{{opacity:1,y:0,duration:1.0,ease:"power2.out"}},{tend:.2f});')
js(f'tl.to("#veil",{{opacity:1,duration:0.9}},{TOTAL - 0.9:.2f});')

for sid in SCENE:
    scene_fade(sid)

# ---------------------------------------------------------------- global sky
rnd = random.Random(99)
stars = "".join(star(rnd.uniform(20, W - 20), rnd.uniform(20, H * 0.75), rnd.uniform(0.45, 1.0), "tw") for _ in range(46)) + "".join(f'<g><circle cx="{x}" cy="{y}" r="58" fill="none" stroke="#c9c6ff" stroke-width="2" opacity=".45"/>{star(x, y, 3.4, "tw")}</g>' for x, y in [(900, 150), (160, 560)])
dots = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.uniform(1, 2.4):.1f}" fill="#f3e6c4" opacity="{rnd.uniform(.3, .8):.2f}"/>' for _ in range(120))
blooms = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"/>' for x, y, r, c, o in [
    (200, 380, 380, "#5a5fa8", .45), (900, 760, 420, "#3f7d9a", .35), (300, 1350, 480, "#6a4f8f", .35),
    (860, 1600, 420, "#2f5c86", .4), (560, 200, 300, "#7a6aa8", .25)])
js(f'tl.fromTo("#sky .tw",{{opacity:1}},{{opacity:0.35,duration:0.9,yoyo:true,repeat:{2 * int(TOTAL / 1.8) - 1},stagger:{{each:0.07,from:"random"}},ease:"sine.inOut"}},0);')

# ---------------------------------------------------------------- subtitles
SPEAKER = {"murka": ("Мурка", "#f6c95a"), "ruslan": ("Человек с экраном", "#a9cdf5"), "denis": ("Юноша", "#a8dcc8"), "dmitri": (None, None)}
subs = []
for lid, st in START.items():
    txt, dur = TEXT[lid], DUR[lid]
    parts = [txt]
    if len(txt) > 95:
        parts = [p.strip() for p in re.split(r"(?<=[.:!?])\s+", txt) if p.strip()]
        merged = []
        for p in parts:
            if merged and len(merged[-1]) + len(p) < 70: merged[-1] += " " + p
            else: merged.append(p)
        parts = merged
    total = sum(len(p) for p in parts)
    t = st
    who, col = SPEAKER[VOICE[lid]]
    for k, p in enumerate(parts):
        pd = dur * len(p) / total
        sid = f"sub-{lid}-{k}"
        label = f'<span class="who" style="color:{col}">{who}</span>' if who else ""
        cls = "sub narr" if not who else "sub"
        extra = 0.25 if k == len(parts) - 1 else 0.0
        subs.append(f'<div id="{sid}" class="clip subw" data-start="{t:.2f}" data-duration="{pd + extra:.2f}" data-track-index="5"><div class="{cls}">{label}<p>{p}</p></div></div>')
        js(f'tl.fromTo("#{sid} .sub",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{t:.2f});')
        t += pd

FONTS = ""
for fam, w, sub in [("Caveat", 700, "cyrillic"), ("Caveat", 700, "latin"), ("Caveat", 400, "cyrillic"), ("Caveat", 400, "latin"), ("Neucha", 400, "cyrillic"), ("Neucha", 400, "latin")]:
    rng_ = "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116" if sub == "cyrillic" else "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212"
    FONTS += f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{w};font-display:block;src:url("fonts/{fam.lower()}-{sub}-{w}-normal.woff2") format("woff2");unicode-range:{rng_};}}\n'

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="wc" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.014 0.42" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1" result="g"/>
  <feComponentTransfer in="g" result="g2"><feFuncR type="linear" slope="2.6" intercept="-0.8"/><feFuncG type="linear" slope="2.6" intercept="-0.8"/><feFuncB type="linear" slope="2.6" intercept="-0.8"/></feComponentTransfer>
  <feComposite in="SourceGraphic" in2="g2" operator="arithmetic" k1="0" k2="1" k3="0.26" k4="-0.13" result="t"/>
  <feComposite in="t" in2="SourceGraphic" operator="in"/>
</filter>
<filter id="ink" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="2" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="bloom" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
<radialGradient id="iris" cx="50%" cy="65%" r="65%"><stop offset="0" stop-color="#bfe88a"/><stop offset=".55" stop-color="#5fae6e"/><stop offset="1" stop-color="#2c5d4b"/></radialGradient>
<radialGradient id="lampGlow"><stop offset="0" stop-color="#ffe8a0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffcc66" stop-opacity=".45"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="phoneGlow"><stop offset="0" stop-color="#bfe3ff" stop-opacity=".9"/><stop offset=".4" stop-color="#6fb2ff" stop-opacity=".35"/><stop offset="1" stop-color="#3d7dff" stop-opacity="0"/></radialGradient>
<clipPath id="phoneClip"><rect x="3.5" y="5" width="23" height="40"/></clipPath>
</defs></svg>'''

CSS = f'''{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#1a2550}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;font-family:"Neucha",serif}}
#sky{{position:absolute;inset:0;background:#3f3c8a url("assets/sky.png") center/cover no-repeat}}
.full{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.scene{{position:absolute;inset:0}}
.inner{{position:absolute;inset:0}}
.svgt{{font-family:"Caveat",cursive;font-weight:700}}
#paper{{position:absolute;inset:0;width:100%;height:100%;mix-blend-mode:multiply;opacity:.55;pointer-events:none}}
.title{{position:absolute;left:0;right:0;top:250px;text-align:center;color:#f6e7c1}}
.t-big{{font-family:"Caveat",cursive;font-weight:700;font-size:210px;line-height:1;color:#f6c95a;text-shadow:0 6px 30px rgba(255,200,90,.35)}}
.t-sub{{font-family:"Caveat",cursive;font-weight:400;font-size:72px;margin-top:10px}}
.stat{{position:absolute;left:60px;right:60px;top:560px;text-align:center;color:#f6e7c1}}
.s-big{{font-family:"Caveat",cursive;font-weight:700;font-size:250px;line-height:1;color:#f6c95a}}
.s-mid{{font-family:"Caveat",cursive;font-weight:700;font-size:84px;line-height:1.1;margin-top:10px}}
.s-src{{font-size:40px;opacity:.75;margin-top:18px}}
.h-title{{position:absolute;left:215px;top:310px;font-family:"Caveat",cursive;font-weight:700;font-size:116px;color:#f6c95a;line-height:1}}
.cards{{position:absolute;left:70px;right:70px;top:600px;display:flex;flex-direction:column;gap:44px}}
.card{{display:flex;align-items:center;gap:22px;padding:26px 34px;background:#f7edd6;border:3px solid {INK};border-radius:28px 40px 30px 46px;box-shadow:0 14px 0 rgba(0,0,0,.18)}}
.c-num{{font-family:"Caveat",cursive;font-weight:700;font-size:96px;color:#9d6c19;width:56px;line-height:1}}
.c-ico{{width:120px;height:120px;flex:none}}
.c-ico svg{{width:100%;height:100%}}
.c-txt{{font-family:"Caveat",cursive;font-weight:700;font-size:64px;line-height:1.05;color:{INK}}}
.c-label{{position:absolute;left:0;right:0;top:800px;text-align:center;font-family:"Caveat",cursive;font-weight:700;font-size:76px;color:#ffe7a3}}
.endcard{{position:absolute;left:0;right:0;top:830px;text-align:center}}
.e-big{{font-family:"Caveat",cursive;font-weight:700;font-size:140px;color:#f6c95a;line-height:1;text-shadow:0 6px 30px rgba(255,200,90,.35)}}
.e-sub{{font-family:"Caveat",cursive;font-size:76px;color:#f6e7c1;margin-top:12px}}
.subw{{position:absolute;left:70px;right:70px;bottom:300px;display:flex;justify-content:center}}
.sub{{max-width:940px;padding:18px 30px 22px;border-radius:26px;background:rgba(18,22,48,.62);text-align:center;color:#fbf3e0}}
.sub .who{{display:block;font-family:"Caveat",cursive;font-weight:700;font-size:44px;line-height:1}}
.sub p{{font-size:50px;line-height:1.18}}
.sub.narr p{{font-style:normal;color:#efe4c8}}
#veil{{position:absolute;inset:0;background:#0d1230;opacity:0;pointer-events:none}}
'''

html_doc = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Мурка и погасшие огоньки</title>
<script src="vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
{DEFS}
<div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{TOTAL}">
<div id="sky" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0"><svg class="full" viewBox="0 0 {W} {H}">
{stars}</svg></div>
{chr(10).join(SECTIONS)}
{chr(10).join(subs)}
<div id="veil" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="7"></div>
<audio id="soundtrack" src="assets/soundtrack.wav" data-start="0" data-duration="{TOTAL}" data-track-index="8"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(JS)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html_doc)
print("index.html written", len(html_doc), "bytes;", len(JS), "tweens; total", TOTAL)
