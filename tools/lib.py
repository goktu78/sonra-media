import math, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
GREEN = (47, 82, 51); DGREEN = (27, 48, 32); CREAM = (242, 237, 227); INK = (24, 26, 22)
MUTED = (120, 114, 104); LINE = (222, 214, 200); CARD = (250, 247, 240); ACC = (84, 140, 76)
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def F(size, w="XB"):
    name = {"XB": "InterDisplay-ExtraBold.otf", "B": "InterDisplay-Bold.otf", "SB": "Inter-SemiBold.otf",
            "M": "Inter-Medium.otf", "R": "Inter-Regular.otf", "BL": "InterDisplay-Black.otf"}[w]
    k = (size, name)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + name, size)
    return _fc[k]

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, start, dur): return clamp((t - start) / dur)

def wrap(text, font, maxw):
    out = []
    for para in text.split("\n"):
        words, line = para.split(" "), ""
        for w_ in words:
            test = (line + " " + w_).strip()
            if font.getlength(test) <= maxw or not line: line = test
            else: out.append(line); line = w_
        out.append(line)
    return out

class Frame:
    def __init__(self, bg):
        self.im = Image.new("RGBA", (W, H), bg + (255,))
    def layer(self, fn, alpha=1.0, dy=0, dx=0, scale=1.0, center=None):
        if alpha <= 0.01: return
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fn(ImageDraw.Draw(L), L)
        if scale != 1.0:
            cx, cy = center or (W / 2, H / 2)
            nw, nh = int(W * scale), int(H * scale)
            L2 = L.resize((nw, nh), Image.BILINEAR)
            L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            L.paste(L2, (int(cx - cx * scale), int(cy - cy * scale)))
        if dx or dy:
            L2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L2.paste(L, (int(dx), int(dy))); L = L2
        if alpha < 1:
            a = L.getchannel("A").point(lambda v: int(v * alpha)); L.putalpha(a)
        self.im.alpha_composite(L)
    def rgb(self): return self.im.convert("RGB")

def text_block(d, text, y, size, color, w="XB", maxw=940, lh=1.12, align="center", x=None):
    f = F(size, w); lines = wrap(text, f, maxw)
    for i, ln in enumerate(lines):
        lw = f.getlength(ln)
        xx = (W - lw) / 2 if align == "center" else x
        d.text((xx, y + i * size * lh), ln, font=f, fill=color)
    return y + len(lines) * size * lh

def pill(d, cx, cy, text, size, fg, bg, padx=34, pady=18, w="SB", outline=None):
    f = F(size, w); tw = f.getlength(text)
    x0, y0, x1, y1 = cx - tw / 2 - padx, cy - size / 2 - pady, cx + tw / 2 + padx, cy + size / 2 + pady
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) / 2, fill=bg, outline=outline, width=3 if outline else 0)
    d.text((cx - tw / 2, cy - size * 0.62), text, font=f, fill=fg)
    return (x0, y0, x1, y1)

def logo_word(d, cx, cy, size, color, dot=ACC):
    f = F(size, "XB"); t = "sonra"; tw = f.getlength(t); dw = size * 0.22
    x = cx - (tw + dw) / 2
    d.text((x, cy - size * 0.62), t, font=f, fill=color)
    r = size * 0.1; bx = x + tw + r * 1.2; by = cy + size * 0.26
    d.ellipse((bx - r, by - r, bx + r, by + r), fill=dot)

# phone mockup
PX0, PY0, PX1, PY1 = 150, 520, 930, 1800
def phone(d, im, dark=False, y_off=0):
    x0, y0, x1, y1 = PX0, PY0 + y_off, PX1, PY1 + y_off
    d.rounded_rectangle((x0 - 18, y0 - 18, x1 + 18, y1 + 18), radius=96, fill=(20, 20, 18))
    d.rounded_rectangle((x0, y0, x1, y1), radius=80, fill=(18, 20, 18) if dark else CREAM)
    d.rounded_rectangle(((x0 + x1) / 2 - 95, y0 + 22, (x0 + x1) / 2 + 95, y0 + 70), radius=24, fill=(10, 10, 10))
    return x0, y0, x1, y1

# simple glyph icons drawn in a square thumbnail
def thumb(d, x, y, s, kind, col):
    d.rounded_rectangle((x, y, x + s, y + s), radius=s * 0.22, fill=col)
    c = CREAM; cx, cy = x + s / 2, y + s / 2; r = s * 0.22; lw = max(4, int(s * 0.06))
    if kind == "bag":
        d.rounded_rectangle((cx - r, cy - r * 0.6, cx + r, cy + r), radius=8, outline=c, width=lw)
        d.arc((cx - r * 0.55, cy - r * 1.3, cx + r * 0.55, cy - r * 0.1), 180, 360, fill=c, width=lw)
    elif kind == "pin":
        d.ellipse((cx - r, cy - r * 1.2, cx + r, cy + r * 0.8), outline=c, width=lw)
        d.polygon([(cx - r * 0.7, cy + r * 0.3), (cx + r * 0.7, cy + r * 0.3), (cx, cy + r * 1.4)], fill=c)
        d.ellipse((cx - r * 0.35, cy - r * 0.55, cx + r * 0.35, cy + r * 0.15), fill=col)
    elif kind == "play":
        d.ellipse((cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2), outline=c, width=lw)
        d.polygon([(cx - r * 0.4, cy - r * 0.6), (cx - r * 0.4, cy + r * 0.6), (cx + r * 0.6, cy)], fill=c)
    elif kind == "book":
        d.rectangle((cx - r * 1.1, cy - r * 0.8, cx - 3, cy + r * 0.9), outline=c, width=lw)
        d.rectangle((cx + 3, cy - r * 0.8, cx + r * 1.1, cy + r * 0.9), outline=c, width=lw)
    elif kind == "note":
        d.line((cx + r * 0.6, cy - r, cx + r * 0.6, cy + r * 0.6), fill=c, width=lw)
        d.ellipse((cx - r * 0.5, cy + r * 0.2, cx + r * 0.7, cy + r * 1.0), fill=c)
        d.line((cx + r * 0.6, cy - r, cx + r * 1.2, cy - r * 0.6), fill=c, width=lw)
    elif kind == "check":
        d.ellipse((cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2), outline=c, width=lw)
        d.line((cx - r * 0.55, cy, cx - r * 0.1, cy + r * 0.45, cx + r * 0.6, cy - r * 0.45), fill=c, width=lw, joint="curve")
    elif kind == "img":
        d.rectangle((cx - r * 1.1, cy - r * 0.9, cx + r * 1.1, cy + r * 0.9), outline=c, width=lw)
        d.polygon([(cx - r, cy + r * 0.8), (cx - r * 0.2, cy - r * 0.1), (cx + r * 0.4, cy + r * 0.5), (cx + r, cy + r * 0.8)], fill=c)

def list_item(d, x, y, w, title, meta, kind, col, s=150):
    thumb(d, x, y, s, kind, col)
    f = F(40, "B"); lines = wrap(title, f, w - s - 40)[:2]
    for i, ln in enumerate(lines): d.text((x + s + 32, y + 6 + i * 48), ln, font=f, fill=INK)
    d.text((x + s + 32, y + 20 + len(lines) * 48), meta, font=F(30, "M"), fill=MUTED)

def end_card(fr, t, lang="tr"):
    # t = seconds since end card start
    def draw(d, L):
        ic = 340; x = (W - ic) / 2; y = 520
        d.rounded_rectangle((x, y, x + ic, y + ic), radius=90, fill=CREAM)
        logo_word(d, W / 2, y + ic / 2, 98, DGREEN, dot=ACC)
    s = 0.8 + 0.2 * back(prog(t, 0, 0.5))
    fr.layer(draw, alpha=ease(prog(t, 0, 0.3)), scale=s, center=(W / 2, 690))
    tag = "Kaydet. Unutma. Sonra yap." if lang == "tr" else "Save it. Find it. Do it later."
    fr.layer(lambda d, L: text_block(d, tag, 950, 74, CREAM, "XB", maxw=980), alpha=ease(prog(t, 0.3, 0.4)), dy=30 * (1 - ease(prog(t, 0.3, 0.4))))
    def badges(d, L):
        for i, (a, b) in enumerate([("Download on the" if lang == "en" else "İndir", "App Store"), ("GET IT ON" if lang == "en" else "İndir", "Google Play")]):
            cx = W / 2 + (-215 if i == 0 else 215); y0 = 1200
            d.rounded_rectangle((cx - 195, y0, cx + 195, y0 + 130), radius=30, fill=CREAM)
            f1, f2 = F(26, "M"), F(48, "XB")
            d.text((cx - f1.getlength(a) / 2, y0 + 16), a, font=f1, fill=GREEN)
            d.text((cx - f2.getlength(b) / 2, y0 + 50), b, font=f2, fill=INK)
    fr.layer(badges, alpha=ease(prog(t, 0.6, 0.4)), dy=40 * (1 - ease(prog(t, 0.6, 0.4))))
    cta = "Ücretsiz · Türkçe & English" if lang == "tr" else "Free · English & Türkçe"
    fr.layer(lambda d, L: text_block(d, cta, 1400, 40, (200, 214, 196), "SB"), alpha=ease(prog(t, 0.9, 0.4)))

def render_scene(path, dur, draw_fn, bg):
    n = int(round(dur * FPS)); tmp = path[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS; fr = Frame(bg(t) if callable(bg) else bg); draw_fn(fr, t)
        p.stdin.write(fr.rgb().tobytes())
    p.stdin.close(); assert p.wait() == 0; os.rename(tmp, path)

def still(draw_fn, bg, t, path):
    fr = Frame(bg(t) if callable(bg) else bg); draw_fn(fr, t); fr.rgb().save(path)

# ---------- audio ----------
SR = 44100
def synth_music(dur, bpm, root, seed, cues=(), taps=()):
    rng = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm
    prog_ = [[0, 4, 7, 11], [9, 12, 16, 19], [5, 9, 12, 16], [7, 11, 14, 17]]
    def hz(semi): return 440 * 2 ** ((root + semi - 9) / 12)
    bar = beat * 4
    for b in range(int(dur / bar) + 1):
        ch = prog_[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        tt = np.arange(s1 - s0) / SR; env = np.minimum(1, tt / 0.3) * np.minimum(1, (bar - tt) / 0.3)
        for semi in ch:
            f = hz(semi - 12); out[s0:s1] += 0.035 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))
        f = hz(ch[0] - 24); out[s0:s1] += 0.08 * env * np.sin(2 * np.pi * f * tt)
        for k in range(8):  # plucks on eighths
            if rng.random() < 0.7:
                st = s0 + int(k * beat / 2 * SR); L = int(0.35 * SR)
                if st + L > n: continue
                tt2 = np.arange(L) / SR; f = hz(ch[rng.integers(0, 4)] + 12)
                out[st:st + L] += 0.05 * np.exp(-tt2 * 9) * np.sin(2 * np.pi * f * tt2)
    for k in range(int(dur / beat)):
        st = int(k * beat * SR); L = int(0.25 * SR)
        if st + L > n: break
        tt2 = np.arange(L) / SR
        out[st:st + L] += 0.22 * np.exp(-tt2 * 18) * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt2 * 30)) * tt2)
        hs = st + int(beat / 2 * SR); Lh = int(0.05 * SR)
        if hs + Lh < n: out[hs:hs + Lh] += 0.03 * np.exp(-np.arange(Lh) / SR * 80) * rng.standard_normal(Lh)
    for c in cues:  # whoosh
        st = int(c * SR); L = int(0.35 * SR)
        if st + L > n: continue
        noise = rng.standard_normal(L); noise = np.convolve(noise, np.ones(12) / 12, "same")
        e = np.sin(np.pi * np.arange(L) / L) ** 2; out[st:st + L] += 0.12 * e * noise
    for c in taps:  # pop
        st = int(c * SR); L = int(0.12 * SR)
        if st + L > n: continue
        tt2 = np.arange(L) / SR; out[st:st + L] += 0.25 * np.exp(-tt2 * 40) * np.sin(2 * np.pi * (900 - 2500 * tt2) * tt2)
    fade = np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 1.2); out *= fade
    out = out / max(1e-6, np.abs(out).max()) * 0.8
    return np.stack([out, out], 1)

def write_wav(path, data):
    import wave
    d = (np.clip(data, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())

def assemble(scene_files, wav, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for s in scene_files: f.write(f"file '{s}'\n")
    tmpv = out[:-4] + ".v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", tmpv], check=True)
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmpv, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.rename(tmp, out); os.remove(tmpv); os.remove(lst)
