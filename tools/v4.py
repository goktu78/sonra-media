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
# Kural (22 Kasım geri bildirimi): her altyazı karesi TEK SATIR; sığmazsa yazı küçülür (min 56 px),
# yine sığmazsa ifade anlamına göre iki ayrı kareye bölünür. Karede en fazla 7 kelime, tek kelimelik kare yok.
# Sabit konum (alt-orta güvenli alan), zıplama/kayma yok; sadece kısa fade.
CAP_Y = 1440          # satır merkezinin y'si (TikTok/Reels butonlarının üstü)
CAP_MAX, CAP_MIN, CAP_W, CAP_WORDS, CAP_FONT = 74, 56, 960, 7, "XB"
import re as _re
def tr_upper(s, lang="tr"):
    # Altyazılar cümle düzeninde (Göktuğ'un örneği: "Sonra hâlâ Kapadokya tatilinden kalan"); büyük harf gerekirse TR kuralı:
    return s
def tr_caps(s, lang="tr"):
    if lang == "tr": s = s.replace("i", "İ").replace("ı", "I")
    return s.upper()
def _fits(words, lang):
    return F(CAP_MIN, CAP_FONT).getlength(tr_upper(" ".join(words), lang)) <= CAP_W and len(words) <= CAP_WORDS
def _split(words, lang):
    """Bir ifadeyi tek satıra sığan, dengeli parçalara böl (tek kelime kalmasın)."""
    if _fits(words, lang) or len(words) < 4: return [words]
    best = None
    for k in range(2, len(words) - 1):
        a, b = words[:k], words[k:]
        score = abs(len(" ".join(a)) - len(" ".join(b)))
        # anlam: virgül/bağlaçtan sonra bölmeyi tercih et
        if a[-1].endswith((",", ";", ":")): score -= 40
        if b[0].lower() in ("ve", "ama", "çünkü", "and", "but", "for", "in"): score -= 6
        if best is None or score < best[0]: best = (score, k)
    k = best[1]
    return _split(words[:k], lang) + _split(words[k:], lang)
def cap_frames(text, lang="tr"):
    text = _re.sub(r"\[[^\]]*\]", "", text).replace('"', "").strip()
    phrases = [p.split() for p in _re.findall(r"[^.!?…]+[.!?…]*", text) if p.strip()]
    frames = []
    for ph in phrases:
        for part in _split(ph, lang): frames.append(part)
    # tek kelimelik kareleri komşusuyla birleştir (sığıyorsa)
    out = []
    for fr in frames:
        if out and (len(fr) == 1 or len(out[-1]) == 1) and _fits(out[-1] + fr, lang): out[-1] = out[-1] + fr
        else: out.append(fr)
    return [" ".join(f) for f in out]
def cap_size(line, lang="tr"):
    s = tr_upper(line, lang)
    for sz in range(CAP_MAX, CAP_MIN - 1, -2):
        if F(sz, CAP_FONT).getlength(s) <= CAP_W: return sz
    return CAP_MIN
def caption(base, t, text, start, dur, y=None, size=None, lang="tr"):
    cs = cap_frames(text, lang); tot = sum(len(c) for c in cs); acc = 0
    for c in cs:
        s0 = start + dur * acc / tot; acc += len(c); s1 = start + dur * acc / tot
        if s0 <= t < s1 + (0.3 if c == cs[-1] else 0):
            sz = cap_size(c, lang); f = F(sz, CAP_FONT); ln = tr_upper(c, lang)
            a = int(255 * ease(prog(t, s0, 0.08)))
            ov = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            lw = f.getlength(ln); ph = sz * 0.72
            d.rounded_rectangle(((W - lw) / 2 - 30, CAP_Y - ph, (W + lw) / 2 + 30, CAP_Y + ph), radius=int(ph * 0.6),
                                fill=(0, 0, 0, int(a * 0.55)))
            d.text(((W - lw) / 2, CAP_Y), ln, font=f, fill=(255, 255, 255, a), anchor="lm",
                   stroke_width=max(4, sz // 15), stroke_fill=(0, 0, 0, a))
            base.alpha_composite(ov)
            return

# ---------- library screens (reference/library.json + usage-log.csv rotation) ----------
import json as _json, csv as _csv, datetime as _dt
def lib_used(days=14, today=None):
    today = today or _dt.date.today(); used = set()
    try:
        for r in _csv.DictReader(open(f"{REF}/usage-log.csv")):
            if (today - _dt.date.fromisoformat(r["date"])).days < days: used.add(r["path"])
    except FileNotFoundError: pass
    return used
def lib_pick(theme, lang, scheme, screen, today=None):
    """library.json'dan ekran seç; son 14 günde kullanıldıysa hata ver (rotasyon kuralı)."""
    L = _json.load(open(f"{REF}/library.json"))
    for x in L:
        if x.get("theme") == theme and x.get("lang") == lang and x.get("scheme") == scheme and x.get("screen") == screen:
            p = x["path"]
            if p in lib_used(today=today): raise ValueError(f"son 14 günde kullanıldı: {p}")
            return p
    raise KeyError((theme, lang, scheme, screen))
def lib_log(date, video, paths):
    with open(f"{REF}/usage-log.csv", "a") as f:
        for p in paths: f.write(f"{date},{video},{p}\n")
_lc = {}
def lib_phone(path, width=820):
    k = (path, width)
    if k in _lc: return _lc[k]
    sc = Image.open(f"{REF}/../{path}" if path.startswith("reference/") else path).convert("RGBA")
    h = int(sc.height * width / sc.width); s = sc.resize((width, h), Image.LANCZOS)
    m = Image.new("L", s.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, width, h), radius=int(width * 0.11), fill=255)
    pad = 20; out = Image.new("RGBA", (width + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, width + 2 * pad, h + 2 * pad), radius=int(width * 0.11) + pad, fill=(18, 18, 18, 255))
    out.paste(s, (pad, pad), m); _lc[k] = (out, width / sc.width); return _lc[k]
def app_view(path, t, focus=None, zoom=1.0, z0=0.3, z1=1.6, taps=(), bg=((242, 237, 227), (225, 218, 202)), top=140, width=820):
    """Gerçek ekranı telefon çerçevesinde göster; focus=(sx,sy) kaynak pikselde, oraya yumuşak zoom; taps=[(t,sx,sy)]."""
    ph, k = lib_phone(path, width); base = bg_grad(*bg)
    ox = (W - ph.width) // 2 + 20; oy = top + 20; base.alpha_composite(ph, (ox - 20, oy - 20))
    def to_canvas(sx, sy): return ox + sx * k, oy + sy * k
    s = 1.0; ccx, ccy = W / 2, H / 2
    if focus:
        fx, fy = to_canvas(*focus); p = ease(prog(t, z0, z1 - z0)); s = 1 + (zoom - 1) * p
        ccx = W / 2 + (fx - W / 2) * p; ccy = H / 2 + (fy - H / 2) * p
        hw, hh = W / (2 * s), H / (2 * s); ccx = min(max(ccx, hw), W - hw); ccy = min(max(ccy, hh), H - hh)
    x0, y0 = ccx - W / (2 * s), ccy - H / (2 * s)
    im = base.crop((int(x0), int(y0), int(x0 + W / s), int(y0 + H / s))).resize((W, H), Image.BICUBIC) if s > 1.001 else base
    for (tt, sx, sy) in taps:
        cx, cy = to_canvas(sx, sy); tap(im, t, tt, (cx - x0) * s, (cy - y0) * s)
    return im

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

_LOGO = None; _BADGES = None
def end_card(t, line, lang="tr"):
    global _LOGO, _BADGES
    if _LOGO is None:
        _LOGO = Image.open(f"{HERE}/logo-transparent.png").convert("RGBA")
        _BADGES = [Image.open(f"{HERE}/badge-appstore.png").convert("RGBA"), Image.open(f"{HERE}/badge-googleplay.png").convert("RGBA")]
    im = bg_grad((242, 237, 227), (228, 220, 204))
    p = back(prog(t, 0, 0.5)); sz = max(1, int(440 * (0.7 + 0.3 * p)))
    paste_c(im, _LOGO.resize((sz, sz), Image.LANCZOS), W / 2, 700, alpha=ease(prog(t, 0, 0.3)))
    d = ImageDraw.Draw(im); f = F(76, "XB")
    if t > 0.3:
        for i, ln in enumerate(wrap(line, f, 960)): d.text(((W - f.getlength(ln)) / 2, 1010 + i * 88), ln, font=f, fill=(27, 48, 32))
    if t > 0.6:
        a = ease(prog(t, 0.6, 0.3)); dy = int(30 * (1 - a))
        paste_c(im, _BADGES[0], W / 2 - 225, 1290 + dy, a); paste_c(im, _BADGES[1], W / 2 + 225, 1290 + dy, a)
        f2 = F(40, "SB"); tx = "Ücretsiz · iOS & Android" if lang == "tr" else "Free · iOS & Android"
        d.text(((W - f2.getlength(tx)) / 2, 1400), tx, font=f2, fill=(90, 100, 90))
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

# ---------- ilk saniye kuralı (25 Kasım): kanca metni 0. kareden + hareket ----------
HOOK_Y = 300   # güvenli alan: y>=230, sağ 230 px boş
def hook(base, t, text, y=HOOK_Y, size=78, dur=None, dark=False):
    """0. kareden itibaren tam görünen ≤7 kelimelik kanca kartı. İlk 0.45 sn hafif 'punch' (1.10→1.0) ile hareket.
    dur verilirse son 0.25 sn'de söner."""
    words = text.split(); assert len(words) <= 7, "kanca ≤7 kelime olmalı"
    f = F(size, "BL"); maxw = W - 2 * 70 - 160
    lines = wrap(text, f, maxw)
    if len(lines) > 1 and len(lines[-1].split()) == 1:          # tek kelimelik satır kalmasın
        ws = text.split(); k = (len(ws) + 1) // 2; lines = [" ".join(ws[:k]), " ".join(ws[k:])]
    lh = int(size * 1.16); bw = max(f.getlength(l) for l in lines) + 70; bh = lh * len(lines) + 44
    card = Image.new("RGBA", (int(bw), int(bh)), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    bg, fg = ((20, 20, 20, 235), (255, 255, 255)) if dark else ((255, 255, 255, 245), (17, 17, 17))
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=30, fill=bg)
    for i, l in enumerate(lines): d.text(((bw - f.getlength(l)) / 2, 18 + i * lh), l, font=f, fill=fg)
    s = 1.10 - 0.10 * ease(prog(t, 0.0, 0.45))
    a = 1.0 if dur is None else 1 - prog(t, dur - 0.25, 0.25)
    if a <= 0: return
    card = card.resize((max(1, int(card.width * s)), max(1, int(card.height * s))), Image.LANCZOS)
    paste_c(base, card, (W - 160) / 2 + 40, y + bh / 2, alpha=a)

def end_short(t, line, lang="tr"):
    """≤1.2 sn kapanış kartı (logo + rozetler), seslendirmesiz. end_card'ın hızlı sürümü."""
    return end_card(min(t * 2.2, 3.0), line, lang)
