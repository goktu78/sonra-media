import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

LIGHTACC = (176, 214, 156)

def inner(x0, y0, x1, y1): return x0 + 56, y0 + 120, x1 - 56

def make_card(title, kind, col, w=560, h=170):
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((24, 26, w + 24, h + 26), radius=34, fill=(0, 0, 0, 40))
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=34, fill=CARD, outline=LINE, width=3)
    thumb(d, 44, 44, h - 48, kind, col)
    f = F(38, "B"); tx = 44 + h - 48 + 28
    for i, ln in enumerate(wrap(title, f, w - (h - 48) - 70)[:2]): d.text((tx, 52 + i * 46), ln, font=f, fill=INK)
    return im

def slide_up(t, s, d=0.45, dist=60): return ease(prog(t, s, d)), dist * (1 - ease(prog(t, s, d)))

def top_text(fr, t, text, s=0.0, y=210, size=70, color=INK):
    a, dy = slide_up(t, s)
    fr.layer(lambda d, L: text_block(d, text, y, size, color, "XB", maxw=960), alpha=a, dy=dy)

def tap(fr, t, s, cx, cy):
    p = prog(t, s, 0.5)
    if 0 < p < 1:
        r = 30 + 90 * ease(p)
        fr.layer(lambda d, L: d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GREEN, width=8), alpha=1 - p)
    if s - 0.25 < t < s + 0.35:
        fr.layer(lambda d, L: d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=(30, 30, 30)), alpha=0.35)

# ===================== VIDEO 1: Black Friday (TR) =====================
def v1():
    S = []
    def s1(fr, t):
        a, dy = slide_up(t, 0.0, 0.35)
        fr.layer(lambda d, L: pill(d, W / 2, 560, "27 Kasım", 40, DGREEN, LIGHTACC, w="B"), alpha=a, dy=dy)
        fr.layer(lambda d, L: text_block(d, "Black Friday'e", 680, 112, CREAM), alpha=a, dy=dy)
        sc = 0.6 + 0.4 * back(prog(t, 0.15, 0.45))
        fr.layer(lambda d, L: text_block(d, "5 gün kaldı.", 820, 150, LIGHTACC, "BL"), alpha=ease(prog(t, 0.15, 0.25)), scale=sc, center=(W / 2, 900))
        a2, dy2 = slide_up(t, 1.3)
        fr.layer(lambda d, L: text_block(d, "Peki aylardır kaydettiğin ürünler nerede?", 1130, 70, CREAM, "B", maxw=900), alpha=a2, dy=dy2)
    S.append((3.4, s1, GREEN))

    cards = [("Kaydedilenler (184)", "bag", (190, 120, 90), -8, 120, 640), ("IMG_4821.PNG", "img", (120, 128, 140), 6, 400, 830),
             ("Kendime: mont linki", "note", (70, 110, 160), -4, 150, 1040), ("47 sekme açık", "book", (150, 90, 140), 9, 380, 1230),
             ("IMG_4822.PNG", "img", (120, 128, 140), -10, 170, 1430)]
    imgs = [make_card(c[0], c[1], c[2]).rotate(c[3], expand=True, resample=Image.BICUBIC) for c in cards]
    def s2(fr, t):
        lines = ["Instagram'da kaydettin.", "Ekran görüntüsü aldın.", "Kendine mesaj attın."]
        for i, ln in enumerate(lines):
            a, dy = slide_up(t, i * 1.3, 0.35, 40)
            fr.layer(lambda d, L, ln=ln, i=i: text_block(d, ln, 200 + i * 100, 72, INK if i == len(lines) - 1 or t < (i + 1) * 1.3 else MUTED), alpha=a, dy=dy)
        for k, (c, im) in enumerate(zip(cards, imgs)):
            st = 0.3 + k * 0.85; p = prog(t, st, 0.5)
            if p <= 0: continue
            y = c[5] - 500 * (1 - back(p)); x = c[4]
            fr.layer(lambda d, L, im=im, x=x, y=y: L.alpha_composite(im, (int(x), int(y))), alpha=ease(p * 2))
    S.append((5.0, s2, CREAM))

    def s3(fr, t):
        sc = 0.85 + 0.15 * back(prog(t, 0, 0.4))
        fr.layer(lambda d, L: text_block(d, "…ve hepsi\nkayboldu.", 760, 140, CREAM, "BL"), alpha=ease(prog(t, 0, 0.2)), scale=sc)
    S.append((2.2, s3, DGREEN))

    items = [("Kablosuz kulaklık", "Satın Al · Instagram · 3 gün", "bag", (196, 112, 70)),
             ("Kışlık şişme mont", "Satın Al · TikTok · 1 hafta", "bag", (70, 110, 160)),
             ("Filtre kahve makinesi", "Satın Al · Web · 2 hafta", "bag", (150, 100, 60)),
             ("Okuma lambası", "Satın Al · Instagram · 1 ay", "bag", (110, 140, 90))]
    def s4(fr, t):
        top_text(fr, t, "sonra. hepsini\ntek yerde toplar.", 0.0, 180, 76)
        py = 700 * (1 - ease(prog(t, 0.2, 0.6)))
        def ph(d, L):
            x0, y0, x1, y1 = phone(d, L, y_off=py); ix, iy, ixr = inner(x0, y0, x1, y1)
            d.text((ix, iy), "S A T I N   A L", font=F(28, "B"), fill=MUTED)
            d.text((ix, iy + 50), "Alacakların.", font=F(84, "XB"), fill=INK)
            cx = ix
            for j, (lab, on) in enumerate([("Tümü", False), ("Satın Al  9", True), ("İzle  8", False)]):
                f = F(32, "SB"); tw = f.getlength(lab)
                d.rounded_rectangle((cx, iy + 180, cx + tw + 56, iy + 252), radius=36, fill=GREEN if on else CARD, outline=None if on else LINE, width=3)
                d.text((cx + 28, iy + 196), lab, font=f, fill=CREAM if on else INK); cx += tw + 76
        fr.layer(ph)
        for k, it in enumerate(items):
            st = 1.0 + k * 0.45; a, dy = slide_up(t, st, 0.35, 40)
            def li(d, L, it=it, k=k):
                x0 = PX0 + 56; y = PY0 + 120 + 300 + k * 205 + py
                list_item(d, x0, y, PX1 - PX0 - 112, it[0], it[1], it[2], it[3], s=150)
                d.line((x0, y + 178, PX1 - 56, y + 178), fill=LINE, width=2)
            fr.layer(li, alpha=a, dy=dy)
        a, dy = slide_up(t, 3.6, 0.4)
        def badge(d, L):
            pill(d, W / 2, 432, "Yapay zekâ otomatik ayırdı: Satın Al", 40, CREAM, GREEN, padx=44, pady=26, w="B")
        sc = 0.7 + 0.3 * back(prog(t, 3.6, 0.45))
        fr.layer(badge, alpha=a, scale=sc, center=(W / 2, 432))
    S.append((7.0, s4, CREAM))

    def s5(fr, t):
        a, dy = slide_up(t, 0, 0.4)
        fr.layer(lambda d, L: text_block(d, "İndirim başladığında listen hazır olsun.", 720, 104, CREAM, "XB", maxw=900), alpha=a, dy=dy)
        a2, dy2 = slide_up(t, 0.9)
        fr.layer(lambda d, L: text_block(d, "Linki paylaş → sonra'ya kaydet", 1200, 54, LIGHTACC, "B"), alpha=a2, dy=dy2)
    S.append((2.8, s5, GREEN))
    S.append((4.0, lambda fr, t: end_card(fr, t, "tr"), DGREEN))
    return S

# ===================== VIDEO 2: screenshot pile (TR) =====================
def fmt_tr(n): return f"{n:,}".replace(",", ".")
def v2():
    S = []
    def s1(fr, t):
        fr.layer(lambda d, L: text_block(d, "Galerinde", 600, 80, CREAM, "B"))
        n = int(900 + (2347 - 900) * ease(prog(t, 0, 1.6)))
        fr.layer(lambda d, L: text_block(d, fmt_tr(n), 720, 250, LIGHTACC, "BL"))
        a, dy = slide_up(t, 0.3)
        fr.layer(lambda d, L: text_block(d, "ekran görüntüsü var.", 1010, 80, CREAM, "B"), alpha=a, dy=dy)
        a2, dy2 = slide_up(t, 1.8)
        fr.layer(lambda d, L: text_block(d, "(Bakmadığın.)", 1150, 56, (170, 190, 165), "SB"), alpha=a2, dy=dy2)
    S.append((3.4, s1, DGREEN))

    rnd = random.Random(7)
    tiles = [(rnd.choice([(214, 206, 192), (196, 204, 210), (210, 196, 196), (200, 212, 196), (40, 44, 48), (226, 220, 206)]), rnd.random()) for _ in range(400)]
    def s2(fr, t):
        tw_, gap = 250, 16; cols = 4; x0 = (W - (cols * tw_ + (cols - 1) * gap)) / 2
        scroll = 2600 * ease(prog(t, 0, 5.0)) ** 0.8
        def grid(d, L):
            for i, (c, r) in enumerate(tiles):
                row, col = divmod(i, cols); y = 120 + row * (tw_ * 1.6 + gap) - scroll
                if y > H or y + tw_ * 1.6 < 0: continue
                x = x0 + col * (tw_ + gap)
                d.rounded_rectangle((x, y, x + tw_, y + tw_ * 1.6), radius=18, fill=c)
                lc = (255, 255, 255) if c[0] < 80 else (170, 160, 150)
                for k in range(3): d.rounded_rectangle((x + 24, y + 60 + k * 50 + r * 120, x + tw_ - 24 - k * 40 * r, y + 80 + k * 50 + r * 120), radius=8, fill=lc)
        fr.layer(grid)
        def banner(d, L):
            d.rounded_rectangle((70, 740, W - 70, 1180), radius=48, fill=CREAM, outline=INK, width=6)
            text_block(d, "Hangisiydi o kafe?", 800, 92, INK, "XB", maxw=860)
        a = ease(prog(t, 0.6, 0.3)); sc = 0.8 + 0.2 * back(prog(t, 0.6, 0.4))
        fr.layer(banner, alpha=a, scale=sc, center=(W / 2, 960))
        a2, dy2 = slide_up(t, 2.4, 0.35, 30)
        fr.layer(lambda d, L: text_block(d, "Hani şu bahçeli olan…", 1040, 56, MUTED, "SB"), alpha=a2, dy=dy2)
    S.append((5.0, s2, (232, 226, 214)))

    def s3(fr, t):
        sc = 0.85 + 0.15 * back(prog(t, 0, 0.4))
        fr.layer(lambda d, L: text_block(d, "Bulamadın.", 760, 140, CREAM, "BL"), alpha=ease(prog(t, 0, 0.2)), scale=sc)
        a, dy = slide_up(t, 0.8, 0.3)
        fr.layer(lambda d, L: text_block(d, "Yine.", 940, 120, LIGHTACC, "BL"), alpha=a, dy=dy)
    S.append((2.2, s3, DGREEN))

    q = "kafe"
    res = [("Karaköy'de bahçeli kafe", "Git · Instagram · 3 hafta", "pin", (88, 130, 80)),
           ("Moda'da kahvaltı mekanı", "Git · TikTok · 2 ay", "pin", (180, 120, 70)),
           ("Evde soğuk kahve tarifi", "Yap · YouTube · 1 ay", "check", (90, 110, 150))]
    def s4(fr, t):
        top_text(fr, t, "sonra.'ya kaydet.\nYazınca bul.", 0.0, 180, 76)
        py = 700 * (1 - ease(prog(t, 0.2, 0.6)))
        typed = q[:int(clamp((t - 1.2) / 0.8) * len(q) + 0.001)] if t > 1.2 else ""
        def ph(d, L):
            x0, y0, x1, y1 = phone(d, L, y_off=py); ix, iy, ixr = inner(x0, y0, x1, y1)
            d.text((ix, iy), "S O N R A", font=F(28, "B"), fill=MUTED)
            d.text((ix, iy + 50), "Kaydettiğin her şey.", font=F(66, "XB"), fill=INK)
            d.rounded_rectangle((ix, iy + 170, ixr, iy + 270), radius=34, fill=CARD, outline=GREEN if typed else LINE, width=4)
            d.ellipse((ix + 34, iy + 200, ix + 70, iy + 236), outline=MUTED, width=5); d.line((ix + 66, iy + 232, ix + 80, iy + 246), fill=MUTED, width=5)
            if typed:
                d.text((ix + 104, iy + 196), typed, font=F(44, "SB"), fill=INK)
                cx_ = ix + 104 + F(44, "SB").getlength(typed) + 4
                if int(t * 3) % 2 == 0: d.line((cx_, iy + 196, cx_, iy + 248), fill=GREEN, width=4)
            else:
                d.text((ix + 104, iy + 198), "Ara: mekan, film, ürün…", font=F(40, "R"), fill=MUTED)
        fr.layer(ph)
        for k, it in enumerate(res):
            st = 2.3 + k * 0.35; a, dy = slide_up(t, st, 0.35, 40)
            def li(d, L, it=it, k=k):
                x0 = PX0 + 56; y = PY0 + 120 + 330 + k * 205 + py
                if k == 0 and t > 3.6:
                    d.rounded_rectangle((x0 - 20, y - 20, PX1 - 36, y + 172), radius=30, outline=GREEN, width=6, fill=(232, 240, 226))
                list_item(d, x0, y, PX1 - PX0 - 112, it[0], it[1], it[2], it[3], s=150)
            fr.layer(li, alpha=a, dy=dy)
        sc = 0.7 + 0.3 * back(prog(t, 4.4, 0.45))
        fr.layer(lambda d, L: pill(d, W / 2, 432, "Mekan linki → otomatik “Git”", 42, CREAM, GREEN, padx=44, pady=26, w="B"),
                 alpha=ease(prog(t, 4.4, 0.3)), scale=sc, center=(W / 2, 432))
    S.append((7.2, s4, CREAM))

    def s5(fr, t):
        a, dy = slide_up(t, 0, 0.4)
        fr.layer(lambda d, L: text_block(d, "“Sonra bakarım”", 700, 110, CREAM, "XB", maxw=960), alpha=a, dy=dy)
        a2, dy2 = slide_up(t, 0.6, 0.4)
        fr.layer(lambda d, L: text_block(d, "nihayet işe yarıyor.", 850, 96, LIGHTACC, "XB", maxw=960), alpha=a2, dy=dy2)
    S.append((2.6, s5, GREEN))
    S.append((4.0, lambda fr, t: end_card(fr, t, "tr"), DGREEN))
    return S

# ===================== VIDEO 3: Explore "What can I do?" (EN) =====================
def v3():
    S = []
    def s1(fr, t):
        a, dy = slide_up(t, 0, 0.3)
        fr.layer(lambda d, L: text_block(d, "You saved 300 things.", 650, 104, CREAM, "XB", maxw=900), alpha=a, dy=dy)
        sc = 0.6 + 0.4 * back(prog(t, 1.1, 0.45))
        fr.layer(lambda d, L: text_block(d, "Done: 0.", 960, 170, LIGHTACC, "BL"), alpha=ease(prog(t, 1.1, 0.2)), scale=sc, center=(W / 2, 1050))
    S.append((3.0, s1, DGREEN))

    def s2(fr, t):
        a, dy = slide_up(t, 0, 0.35)
        fr.layer(lambda d, L: text_block(d, "Got 15 minutes?", 720, 120, CREAM, "XB"), alpha=a, dy=dy)
        a2, dy2 = slide_up(t, 0.7, 0.35)
        fr.layer(lambda d, L: text_block(d, "Let your saves\npick for you.", 900, 84, LIGHTACC, "B", maxw=880), alpha=a2, dy=dy2)
    S.append((2.6, s2, GREEN))

    chips = ["15 minutes", "1 hour", "Going out", "Pick for me"]
    res = [("10-min creamy pasta", "Do · TikTok", "check", (180, 120, 70)),
           ("Short doc: life in the deep sea", "Watch · YouTube", "play", (60, 100, 150)),
           ("5 habits of calm people", "Read · Web", "book", (130, 90, 130))]
    TAP = 2.0
    def chip_pos(ix, iy, j):
        cw = (PX1 - PX0 - 112 - 24) / 2
        r, c = divmod(j, 2); x = ix + c * (cw + 24); y = iy + 200 + r * 112
        return x, y, x + cw, y + 92
    def s3(fr, t):
        if t < 3.0: top_text(fr, t, "Tap Explore:\n“What can I do?”", 0.0, 170, 74)
        else: top_text(fr, t, "It picks from YOUR saves.", 3.0, 190, 76)
        py = 700 * (1 - ease(prog(t, 0.2, 0.6)))
        def ph(d, L):
            x0, y0, x1, y1 = phone(d, L, y_off=py); ix, iy, ixr = inner(x0, y0, x1, y1)
            d.rounded_rectangle((ix - 16, iy - 10, ixr + 16, iy + 450), radius=40, fill=CARD, outline=LINE, width=3)
            d.text((ix + 20, iy + 30), "N O W", font=F(28, "B"), fill=MUTED)
            d.text((ix + 20, iy + 76), "What can I do?", font=F(70, "XB"), fill=INK)
            for j, lab in enumerate(chips):
                x, y, xr, yb = chip_pos(ix + 20, iy + 10, j); xr -= 20
                on = (j == 0 and t > TAP)
                d.rounded_rectangle((x, y, xr, yb), radius=46, fill=GREEN if on else CREAM, outline=None if on else LINE, width=3)
                f = F(36, "B"); d.text(((x + xr) / 2 - f.getlength(lab) / 2, y + 24), lab, font=f, fill=CREAM if on else INK)
        fr.layer(ph)
        x, y, xr, yb = chip_pos(PX0 + 76, PY0 + 130, 0)
        tap(fr, t, TAP, (x + xr - 20) / 2, (y + yb) / 2 + py)
        for k, it in enumerate(res):
            st = 3.0 + k * 0.4; a, dy = slide_up(t, st, 0.4, 50)
            def li(d, L, it=it, k=k):
                x0 = PX0 + 56; y_ = PY0 + 120 + 500 + k * 200 + py
                list_item(d, x0, y_, PX1 - PX0 - 112, it[0], it[1], it[2], it[3], s=150)
            fr.layer(li, alpha=a, dy=dy)
    S.append((8.0, s3, CREAM))

    cats = [("Watch", "play"), ("Go", "pin"), ("Read", "book"), ("Buy", "bag"), ("Listen", "note"), ("Do", "check")]
    def s4(fr, t):
        top_text(fr, t, "Every link auto-sorted by intent.", 0.0, 360, 84)
        for k, (lab, kind) in enumerate(cats):
            r, c = divmod(k, 3); cx = W / 2 + (c - 1) * 320; cy = 900 + r * 360
            sc = 0.5 + 0.5 * back(prog(t, 0.5 + k * 0.18, 0.4))
            def dr(d, L, lab=lab, kind=kind, cx=cx, cy=cy):
                thumb(d, cx - 110, cy - 130, 220, kind, GREEN)
                f = F(50, "XB"); d.text((cx - f.getlength(lab) / 2, cy + 110), lab, font=f, fill=INK)
            fr.layer(dr, alpha=ease(prog(t, 0.5 + k * 0.18, 0.25)), scale=sc, center=(cx, cy))
    S.append((3.6, s4, CREAM))
    S.append((4.0, lambda fr, t: end_card(fr, t, "en"), DGREEN))
    return S

VIDS = {"1": (v1, 96, 0, 11), "2": (v2, 92, 5, 22), "3": (v3, 100, 2, 33)}

if __name__ == "__main__":
    vid, mode = sys.argv[1], sys.argv[2]; out = sys.argv[3]
    fn, bpm, root, seed = VIDS[vid]; S = fn()
    if mode == "stills":
        for i, (dur, f, bg) in enumerate(S):
            for frac in (0.15, 0.9):
                still(f, bg, dur * frac, f"{out}/v{vid}_s{i}_{int(frac*100)}.jpg")
    else:
        files = []; cues = []; t0 = 0
        for i, (dur, f, bg) in enumerate(S):
            p = f"{out}/v{vid}_scene{i}.mp4"; render_scene(p, dur, f, bg); files.append(p)
            if i: cues.append(t0 - 0.12)
            t0 += dur
        taps = [3.0 + 2.6 + 2.0] if vid == "3" else []
        wav = f"{out}/v{vid}.wav"; write_wav(wav, synth_music(t0, bpm, root, seed, cues, taps))
        assemble(files, wav, sys.argv[4])
