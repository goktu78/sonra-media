import sys, os, math, random, subprocess, wave, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lib import W, H, FPS, F, ease, back, prog, clamp, wrap, render_scene, GREEN, DGREEN, CREAM, INK
REF = "/home/claude/sonra-media/reference"
EMO = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
_ecache = {}
def emoji_img(ch, size):
    k = (ch, size)
    if k not in _ecache:
        im = Image.new("RGBA", (160 * len(ch), 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((8, 8), ch, font=EMO, embedded_color=True); im = im.crop(im.getbbox())
        s = size / im.height; _ecache[k] = im.resize((max(1, int(im.width * s)), size), Image.LANCZOS)
    return _ecache[k]
def paste_c(base, im, cx, cy, alpha=1.0):
    if alpha < 1:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---------- real screens with blurred thumbnails ----------
S = 1.28
def blur_boxes(im, boxes, radius=28):
    for (x0, y0, x1, y1) in boxes:
        b = tuple(int(v * S) for v in (x0, y0, x1, y1))
        reg = im.crop(b).filter(ImageFilter.GaussianBlur(radius))
        im.paste(reg, b[:2])
    return im
_sc = {}
def screen(name):
    if name in _sc: return _sc[name]
    im = Image.open(f"{REF}/app-screens/{name}.png").convert("RGBA") if name != "paylas" else None
    if name == "sonra-liste":
        im = blur_boxes(im, [(42, 727 + k * 206.5, 197, 872 + k * 206.5) for k in range(6)])
    if name == "kesfet":
        boxes = [(45, 727, 447, 1047), (475, 727, 878, 1047), (45, 1079, 447, 1399), (475, 1079, 878, 1399), (45, 1431, 447, 1750), (475, 1431, 878, 1750)]
        im = blur_boxes(im, boxes, 40)
        d = ImageDraw.Draw(im)
        labs = [("İzle", "8 kayıt"), ("Git", "3 kayıt"), ("Oku", "5 kayıt"), ("Satın Al", "9 kayıt"), ("Dinle", "1 kayıt"), ("Yap", "28 kayıt")]
        for (x0, y0, x1, y1), (a, b) in zip(boxes, labs):
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=34, fill=(0, 0, 0, 70)); im.alpha_composite(ov)
            d.text((x0 * S + 40, y1 * S - 170), a, font=F(70, "XB"), fill="white")
            d.text((x0 * S + 42, y1 * S - 85), b, font=F(36, "M"), fill=(235, 235, 235))
    if name == "paylas":
        src = Image.open(f"{REF}/marketing/store-tr-02-paylas.png").convert("RGBA")
        im = src.crop((int(130 * S), int(580 * S), int(795 * S), int(1905 * S)))
        # blur product thumbnail and third-party app icons
        def bb(x0, y0, x1, y1, r=18):
            b = (int((x0 - 130) * S), int((y0 - 580) * S), int((x1 - 130) * S), int((y1 - 580) * S))
            im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r)), b[:2])
        bb(160, 602, 260, 702); bb(165, 740, 795, 875, 22)
        bb(165, 1160, 760, 1720, 14)
    _sc[name] = im; return im

def phone_img(name, width=780):
    sc = screen(name); h = int(sc.height * width / sc.width)
    s = sc.resize((width, h), Image.LANCZOS)
    m = Image.new("L", s.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, width, h), radius=int(width * 0.11), fill=255)
    pad = 20; out = Image.new("RGBA", (width + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, width + 2 * pad, h + 2 * pad), radius=int(width * 0.11) + pad, fill=(18, 18, 18, 255))
    out.paste(s, (pad, pad), m); return out

# ---------- captions (TikTok style) ----------
def chunks(text, n=3):
    w = text.replace('"', '').split(); return [" ".join(w[i:i + n]) for i in range(0, len(w), n)]
def caption(base, t, text, start, dur, y=1500, size=74):
    cs = chunks(text); tot = sum(len(c) for c in cs); acc = 0
    for c in cs:
        s0 = start + dur * acc / tot; acc += len(c); s1 = start + dur * acc / tot
        if s0 <= t < s1 + (0.25 if c == cs[-1] else 0):
            d = ImageDraw.Draw(base); f = F(size, "BL")
            lines = wrap(c.replace('i','İ').replace('ı','I').upper(), f, 960)
            p = back(prog(t, s0, 0.12)); sz = int(size * (0.85 + 0.15 * p)); f = F(sz, "BL")
            for i, ln in enumerate(lines):
                lw = f.getlength(ln); x = (W - lw) / 2; yy = y + i * sz * 1.1
                d.text((x, yy), ln, font=f, fill="white", stroke_width=max(6, sz // 9), stroke_fill="black")
            return

def bg_grad(top, bot):
    g = np.linspace(0, 1, H)[:, None]
    arr = (np.array(top)[None, None, :] * (1 - g[..., None]) + np.array(bot)[None, None, :] * g[..., None])
    arr = np.repeat(arr, W, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")
class Fr:
    def __init__(self, im): self.im = im
    def rgb(self): return self.im.convert("RGB")

def zoom_view(canvas, t, dur, target, t0=0.6, t1=None):
    """canvas: WxH RGBA. target: (cx, cy, scale). Returns zoomed frame."""
    t1 = t1 or min(dur - 0.3, t0 + 1.6)
    p = ease(prog(t, t0, t1 - t0)); cx, cy, sc = target
    s = 1 + (sc - 1) * p; ccx = W / 2 + (cx - W / 2) * p; ccy = H / 2 + (cy - H / 2) * p
    w, h = W / s, H / s; box = (ccx - w / 2, ccy - h / 2, ccx + w / 2, ccy + h / 2)
    return canvas.crop(tuple(int(v) for v in box)).resize((W, H), Image.BICUBIC)

def tap(base, t, ts, cx, cy):
    p = prog(t, ts, 0.55)
    if 0 < p < 1:
        d = ImageDraw.Draw(base); r = 30 + 110 * ease(p); a = int(255 * (1 - p))
        ov = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, a), width=10)
        base.alpha_composite(ov)
    if ts - 0.2 < t < ts + 0.3:
        ov = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=(255, 255, 255, 150))
        base.alpha_composite(ov)

def end_card(t, line):
    im = bg_grad((47, 82, 51), (22, 40, 26))
    logo = Image.open(f"{REF}/marketing/logo.png").convert("RGBA").resize((420, 420), Image.LANCZOS)
    p = back(prog(t, 0, 0.5)); lg = logo.resize((max(1, int(420 * (0.7 + 0.3 * p))),) * 2)
    paste_c(im, lg, W / 2, 720, alpha=ease(prog(t, 0, 0.3)))
    d = ImageDraw.Draw(im); f = F(76, "XB")
    a = ease(prog(t, 0.3, 0.4))
    if a > 0:
        for i, ln in enumerate(wrap(line, f, 960)): d.text(((W - f.getlength(ln)) / 2, 1020 + i * 88), ln, font=f, fill=CREAM)
    if t > 0.6:
        for i, (s, b) in enumerate([("İndir", "App Store"), ("İndir", "Google Play")]):
            cx = W / 2 + (-215 if i == 0 else 215); y0 = 1260
            d.rounded_rectangle((cx - 195, y0, cx + 195, y0 + 130), radius=30, fill=CREAM)
            d.text((cx - F(26, "M").getlength(s) / 2, y0 + 16), s, font=F(26, "M"), fill=GREEN)
            d.text((cx - F(48, "XB").getlength(b) / 2, y0 + 50), b, font=F(48, "XB"), fill=INK)
    return im

# ---------- chat UI ----------
def chat_base(name="Ece", emoji="👀"):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 300), fill=(247, 247, 247)); d.line((0, 300, W, 300), fill=(220, 220, 220), width=2)
    d.ellipse((W / 2 - 60, 90, W / 2 + 60, 210), fill=(200, 205, 215))
    paste_c(im, emoji_img(emoji, 70), W / 2, 150)
    d.text((W / 2 - F(36, "SB").getlength(name) / 2, 222), name, font=F(36, "SB"), fill=INK)
    d.text((50, 120), "‹", font=F(90, "R"), fill=(0, 122, 255))
    return im
def bubble(im, text, me, y, a=1.0, emo=None):
    f = F(52, "M"); lines = wrap(text, f, 640); lh = 64
    tw = max(f.getlength(l) for l in lines); bw, bh = tw + 70 + (78 if emo else 0), len(lines) * lh + 44
    x0 = W - 50 - bw if me else 50
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    col = (0, 122, 255) if me else (233, 233, 235)
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=44, fill=col + (int(255 * a),))
    for i, l in enumerate(lines): d.text((x0 + 35, y + 18 + i * lh), l, font=f, fill=(255, 255, 255, int(255 * a)) if me else (0, 0, 0, int(255 * a)))
    im.alpha_composite(ov)
    if emo: paste_c(im, emoji_img(emo, 58), x0 + bw - 62, y + bh / 2, a)
    return y + bh + 26
def typing(im, y, t):
    d = ImageDraw.Draw(im); d.rounded_rectangle((50, y, 230, y + 100), radius=50, fill=(233, 233, 235))
    for k in range(3):
        o = 0.5 + 0.5 * math.sin(t * 8 - k)
        d.ellipse((90 + k * 40 - 12, y + 50 - 12 - o * 8, 90 + k * 40 + 12, y + 50 + 12 - o * 8), fill=(150, 150, 155))

# ---------- gallery / saved graveyard ----------
_rng = random.Random(11)
TILES = [tuple(_rng.randint(60, 220) for _ in range(3)) for _ in range(600)]
def gallery(t, speed=900, counter=None, timer=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    cols, g = 4, 6; tw = (W - (cols - 1) * g) / cols; off = (t * speed) % (tw + g); row0 = int(t * speed // (tw + g))
    for r in range(-1, int(H / (tw + g)) + 2):
        for c in range(cols):
            col = TILES[((r + row0) * cols + c) % len(TILES)]
            x = c * (tw + g); y = r * (tw + g) - off + 250
            d.rectangle((x, y, x + tw, y + tw), fill=col)
            d.rectangle((x + tw * 0.15, y + tw * 0.2, x + tw * 0.85, y + tw * 0.3), fill=tuple(min(255, v + 30) for v in col))
    im = im.filter(ImageFilter.GaussianBlur(3)) if speed > 600 else im
    d = ImageDraw.Draw(im); d.rectangle((0, 0, W, 250), fill=(0, 0, 0))
    if counter: d.text((50, 120), counter, font=F(64, "XB"), fill="white")
    if timer: d.text((W - 50 - F(64, "XB").getlength(timer), 120), timer, font=F(64, "XB"), fill=(255, 80, 80))
    return im
