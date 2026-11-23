"""2026-11-23 videoları. Ekranlar library.json'dan (rotasyon kuralı), altyazılar v4.caption (tek satır kuralı).
Kullanım: python3 vids5.py <1|2|3> stills OUTDIR  |  python3 vids5.py <1|2|3> render OUTDIR final.mp4"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v4 import *
from vids4 import render, D, L
import datetime as dt

TODAY = dt.date(2026, 11, 23)

def card_text(im, lines, y, size=64, col=(255, 255, 255), w="XB", lh=1.18, a=1.0):
    d = ImageDraw.Draw(im); f = F(size, w)
    for i, ln in enumerate(lines):
        d.text(((W - f.getlength(ln)) / 2, y + i * size * lh), ln, font=f, fill=col + (int(255 * a),))

def quote_card(im, who, text_lines, t, t0=0.0, y=560, dark=False):
    """Sokak röportajı cevap kartı (gerçek kişi görüntüsü yok)."""
    a = ease(prog(t, t0, 0.25)); dy = int(40 * (1 - a))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    f = F(62, "B"); lh = 80; hgt = 150 + len(text_lines) * lh
    d.rounded_rectangle((80, y + dy, W - 80, y + dy + hgt), radius=44, fill=(255, 255, 255, int(245 * a)))
    d.text((130, y + dy + 40), who, font=F(38, "SB"), fill=(47, 82, 51, int(255 * a)))
    for i, ln in enumerate(text_lines):
        d.text((130, y + dy + 105 + i * lh), ln, font=f, fill=(24, 26, 22, int(255 * a)))
    im.alpha_composite(ov)
    return y + hgt

# ---------------- 1) Öğretmenler Günü sokak röportajı (Cavit) ----------------
V1_TXT = ["[excited] Öğretmenler Gününe bir gün kala sorduk: Hediye hazır mı?",
          "[laughs softly] Eylülde harika bir fikir kaydetmiştim. Bir daha bulamadım.",
          "Linki paylaş, Sonraya kaydet. Fikir Satın Al listesinde bekler.",
          "[playful] Bu yıl on dördüncü kupa değil, gerçekten düşündüğün hediye."]
V1_VO = [3.76, 4.72, 4.80, 4.24]
V1_SCR = [("alisveris", "tr", "light", "ana-sayfa"), ("alisveris", "tr", "light", "detay-1")]

def mic_header(im, t):
    d = ImageDraw.Draw(im)
    paste_c(im, emoji_img("🎤", 90), 150, 210)
    d.text((215, 175), "SOKAK RÖPORTAJI", font=F(54, "BL"), fill=(255, 214, 90))
    d.ellipse((W - 190, 190, W - 160, 220), fill=(230, 50, 50) if int(t * 2) % 2 == 0 else (120, 30, 30))
    d.text((W - 150, 180), "REC", font=F(40, "B"), fill="white")

def V1():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V1_SCR]
    BG = ((30, 64, 44), (14, 30, 20))
    def s0(t):
        im = bg_grad(*BG); mic_header(im, t)
        a = ease(prog(t, 0.1, 0.4))
        card_text(im, ["Öğretmenler", "Günü'ne"], 380, 130, (255, 255, 255), "BL", 1.05, a)
        p = back(prog(t, 0.6, 0.45))
        if p > 0:
            f = F(150, "BL"); tx = "1 gün kala"
            st = Image.new("RGBA", (int(f.getlength(tx)) + 80, 210), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rounded_rectangle((0, 0, st.width - 1, 209), radius=30, fill=(255, 214, 90))
            sd.text((40, 20), tx, font=f, fill=(27, 48, 32))
            st = st.rotate(-4, expand=True, resample=Image.BICUBIC)
            st = st.resize((max(1, int(st.width * p)), max(1, int(st.height * p))))
            paste_c(im, st, W / 2, 780)
        if t > 1.8:
            paste_c(im, emoji_img("🍎", int(150 * max(0.01, back(prog(t, 1.8, 0.35))))), W / 2 - 300, 1060)
            paste_c(im, emoji_img("🎁", int(150 * max(0.01, back(prog(t, 2.1, 0.35))))), W / 2 + 300, 1060)
        caption(im, t, V1_TXT[0], L, V1_VO[0]); return im
    S.append((D(V1_VO[0]), s0))
    def s1(t):
        im = bg_grad(*BG); mic_header(im, t)
        card_text(im, ["Hediyeyi ne zaman", "alacaksın?"], 330, 70, (255, 214, 90), "XB")
        quote_card(im, "Öğrenci, 11. sınıf", ["Yarın sabah.", "Okul yolunda.", "Kırtasiyeden."], t, 0.3)
        if t > 1.4: paste_c(im, emoji_img("🏃", int(170 * max(0.01, back(prog(t, 1.4, 0.3))))), W - 220, 1180)
        return im
    S.append((2.5, s1))
    def s2(t):
        if t < 1.7:
            im = bg_grad(*BG); mic_header(im, t)
            quote_card(im, "Veli, iki çocuk", ["Eylülde harika bir fikir", "kaydetmiştim…"], t, 0.0, y=520)
        else:
            n = int(900 + 1418 * ease(prog(t, 1.7, 2.2)))
            im = gallery(t, speed=1500 if t < 4.0 else 250, counter=f"Kaydedilenler · {n:,}".replace(",", "."))
            if t > 3.6:
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 120)); im.alpha_composite(ov)
                paste_c(im, emoji_img("🔍", int(200 * max(0.01, back(prog(t, 3.6, 0.3))))), W / 2 - 150, 850)
                paste_c(im, emoji_img("🫠", int(200 * max(0.01, back(prog(t, 3.9, 0.3))))), W / 2 + 150, 850)
        caption(im, t, V1_TXT[1], L, V1_VO[1]); return im
    S.append((D(V1_VO[1]), s2))
    def s3(t):
        im = bg_grad(*BG); mic_header(im, t)
        quote_card(im, "Öğretmen, 14 yıllık", ["Bu yıl da kupa gelirse", "dolap kapanmıyor."], t, 0.0, y=330)
        for k in range(14):
            st = 0.35 + k * 0.1; p = back(prog(t, st, 0.25))
            if p <= 0: continue
            x = 200 + (k % 5) * 170; y = 1240 - (k // 5) * 150
            paste_c(im, emoji_img("☕", int(130 * max(0.01, p))), x, y)
        if t > 1.9:
            d = ImageDraw.Draw(im); f = F(70, "BL"); tx = "×14"
            d.text((W - 230, 840), tx, font=f, fill=(255, 214, 90))
        return im
    S.append((2.5, s3))
    d4 = D(V1_VO[2])
    def s4(t):
        im = app_view(P[0], t, focus=(590, 900), zoom=1.3, z0=0.2, z1=1.4,
                      taps=[(2.2, 590, 598), (3.7, 314, 1790)])
        caption(im, t, V1_TXT[2], L, V1_VO[2]); return im
    S.append((d4, s4))
    def s5(t):
        im = app_view(P[1], t, focus=(590, 1250), zoom=1.25, z0=0.2, z1=1.4, taps=[(2.6, 185, 1505)])
        if t > 3.0:
            p = back(prog(t, 3.0, 0.35)); paste_c(im, emoji_img("🍎", int(150 * max(0.01, p))), W - 170, 420)
        caption(im, t, V1_TXT[3], L, V1_VO[3]); return im
    S.append((D(V1_VO[3]), s5))
    S.append((2.8, lambda t: end_card(t, "Fikri kaydet, hediyeyi unutma.")))
    return S, P

# ---------------- 2) Ne izlesek? belgeseli (Ahmet) ----------------
V2_TXT = ["[serious documentary narrator] Cuma akşamı. İki yetişkin. Tek bir soru.",
          "[deadpan] Kırk yedi dakika boyunca katalog gezilir. Fragmanlar izlenir.",
          "Oysa önerilen her film, Sonrada İzle listesinde hazır bekliyordu.",
          "[serious documentary narrator] Seçim beş saniye sürer. Doğa yeniden dengeye kavuşur."]
V2_VO = [3.52, 4.40, 4.40, 4.48]
V2_SCR = [("genel", "tr", "dark", "liste"), ("genel", "tr", "dark", "liste-filtre-izle")]
NIGHT = ((16, 20, 44), (6, 8, 20))

def doc_header(im):
    d = ImageDraw.Draw(im); f = F(44, "SB"); tx = "BİR SONRA. BELGESELİ"
    d.text(((W - f.getlength(tx)) / 2, 220), tx, font=f, fill=(200, 190, 150))
    d.line((W / 2 - 260, 290, W / 2 + 260, 290), fill=(200, 190, 150), width=3)

def poster_grid(t, speed, timer):
    im = Image.new("RGBA", (W, H), (10, 10, 14, 255)); d = ImageDraw.Draw(im)
    cols, g = 3, 18; tw = (W - 4 * g) / cols; th = tw * 1.45; off = (t * speed) % (th + g); r0 = int(t * speed // (th + g))
    for r in range(-1, int(H / (th + g)) + 2):
        for c in range(cols):
            col = TILES[((r + r0) * cols + c) % len(TILES)]
            x = g + c * (tw + g); y = r * (th + g) - off + 260
            d.rounded_rectangle((x, y, x + tw, y + th), radius=18, fill=col)
            d.rectangle((x + 24, y + th - 90, x + tw - 60, y + th - 66), fill=tuple(min(255, v + 40) for v in col))
            d.ellipse((x + tw / 2 - 40, y + th / 2 - 40, x + tw / 2 + 40, y + th / 2 + 40), outline=(255, 255, 255, 180), width=6)
            d.polygon([(x + tw / 2 - 12, y + th / 2 - 20), (x + tw / 2 - 12, y + th / 2 + 20), (x + tw / 2 + 22, y + th / 2)], fill="white")
    im = im.filter(ImageFilter.GaussianBlur(4 if speed > 500 else 1))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, W, 250), fill=(10, 10, 14))
    d.text((50, 120), "Katalog", font=F(64, "XB"), fill="white")
    d.text((W - 50 - F(64, "XB").getlength(timer), 120), timer, font=F(64, "XB"), fill=(255, 80, 80))
    return im

def V2():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V2_SCR]
    def s0(t):
        im = bg_grad(*NIGHT); doc_header(im); d = ImageDraw.Draw(im)
        a = ease(prog(t, 0.1, 0.5))
        card_text(im, ["Cuma, 21:04"], 400, 140, (255, 255, 255), "BL", 1, a)
        p = back(prog(t, 0.8, 0.45)); paste_c(im, emoji_img("🛋️", int(300 * max(0.01, p))), W / 2, 880)
        if t > 1.6:
            paste_c(im, emoji_img("🧍", int(170 * max(0.01, back(prog(t, 1.6, 0.3))))), W / 2 - 120, 760)
            paste_c(im, emoji_img("🧍", int(170 * max(0.01, back(prog(t, 1.9, 0.3))))), W / 2 + 120, 760)
        caption(im, t, V2_TXT[0], L, V2_VO[0]); return im
    S.append((D(V2_VO[0]), s0))
    def s1(t):
        im = bg_grad(*NIGHT); doc_header(im)
        lines = [("Ne izlesek?", False), ("Fark etmez.", True), ("Sen seç.", False), ("Yok onu izledik.", True), ("Ne izlesek?", False)]
        y = 380
        for k, (tx, me) in enumerate(lines):
            st = 0.15 + k * 0.48
            if t > st: y = bubble(im, tx, me, y, ease(prog(t, st, 0.15)))
        if t > 2.5: paste_c(im, emoji_img("🔁", int(150 * max(0.01, back(prog(t, 2.5, 0.25))))), W - 150, y + 40)
        return im
    S.append((2.9, s1))
    def s2(t):
        sec = int(47 * 60 * ease(prog(t, 0, D(V2_VO[1]) - 0.6)) + 12 * ease(prog(t, 0, D(V2_VO[1]) - 0.6)))
        im = poster_grid(t, 1300 if t < 3.6 else 200, f"{sec // 60}:{sec % 60:02d}")
        if t > 3.6: paste_c(im, emoji_img("🥱", int(220 * max(0.01, back(prog(t, 3.6, 0.3))))), W / 2, 900)
        caption(im, t, V2_TXT[1], L, V2_VO[1]); return im
    S.append((D(V2_VO[1]), s2))
    def s3(t):
        im = bg_grad((8, 8, 18), (2, 2, 8)); doc_header(im)
        card_text(im, ["23:58"], 380, 150, (255, 255, 255), "BL")
        paste_c(im, emoji_img("😴", 190), W / 2 - 130, 860); paste_c(im, emoji_img("😴", 190), W / 2 + 130, 880)
        for k in range(3):
            if t > 0.3 + k * 0.3: card_text(im, ["z"], 660 - k * 70, 60 + k * 20, (200, 200, 255), "BL") if False else ImageDraw.Draw(im).text((W / 2 + 230 + k * 50, 700 - k * 80), "z", font=F(60 + k * 22, "BL"), fill=(200, 200, 255))
        if t > 0.9: card_text(im, ["Film seçilemedi."], 1080, 70, (255, 214, 90), "XB", a=ease(prog(t, 0.9, 0.3)))
        if t > 1.5: card_text(im, ["Türün iki üyesi de uyudu."], 1180, 52, (210, 210, 220), "SB", a=ease(prog(t, 1.5, 0.3)))
        return im
    S.append((2.6, s3))
    def s4(t):
        im = app_view(P[0], t, focus=(500, 700), zoom=1.3, z0=0.2, z1=1.4, taps=[(2.3, 326, 468), (3.8, 550, 1336)],
                      bg=((30, 32, 40), (12, 12, 18)))
        caption(im, t, V2_TXT[2], L, V2_VO[2]); return im
    S.append((D(V2_VO[2]), s4))
    def s5(t):
        im = app_view(P[1], t, focus=(500, 1300), zoom=1.25, z0=0.2, z1=1.4, taps=[(2.2, 157, 1505)],
                      bg=((30, 32, 40), (12, 12, 18)))
        if t > 2.6: paste_c(im, emoji_img("🍿", int(170 * max(0.01, back(prog(t, 2.6, 0.35))))), W - 170, 420)
        caption(im, t, V2_TXT[3], L, V2_VO[3]); return im
    S.append((D(V2_VO[3]), s5))
    S.append((2.8, lambda t: end_card(t, "Ne izlesek? Listende hazır.")))
    return S, P

# ---------------- 3) EN POV: November, 63 saved beaches (Elena) ----------------
V3_TXT = ["[deadpan] It's November. I have sixty-three saved beaches.",
          "[sighs] And zero plans for this weekend.",
          "In Sonra, every spot I save waits in Go for next summer.",
          "[excited] And \"I'm heading out\" picks one for tonight."]
V3_VO = [4.08, 3.28, 4.24, 3.20]
V3_SCR = [("travel", "en", "light", "kart-git-2"), ("travel", "en", "light", "kesfet"), ("travel", "en", "light", "kesfet-disari")]
import random as _r
_SNOW = [(_r.Random(k).random() * W, _r.Random(k + 99).random() * H, 6 + _r.Random(k + 7).random() * 10) for k in range(70)]
def snow(im, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for (x, y, r) in _SNOW:
        yy = (y + t * (90 + r * 12)) % H; xx = x + 20 * math.sin(t * 1.5 + y)
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(255, 255, 255, 200))
    im.alpha_composite(ov)

def V3():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V3_SCR]
    COLD = ((60, 84, 120), (24, 34, 56))
    def s0(t):
        im = bg_grad(*COLD); d = ImageDraw.Draw(im)
        d.text((80, 200), "POV:", font=F(110, "BL"), fill=(255, 214, 90))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(prog(t, 0.2, 0.4)); od.rounded_rectangle((240, 420, W - 240, 960), radius=40, fill=(255, 255, 255, int(240 * a)))
        od.rounded_rectangle((240, 420, W - 240, 560), radius=40, fill=(220, 60, 60, int(255 * a))); od.rectangle((240, 520, W - 240, 560), fill=(220, 60, 60, int(255 * a)))
        im.alpha_composite(ov)
        if a > 0.5:
            f = F(66, "BL"); tx = "NOVEMBER"; d.text(((W - f.getlength(tx)) / 2, 450), tx, font=f, fill="white")
            f = F(260, "BL"); tx = "23"; d.text(((W - f.getlength(tx)) / 2, 580), tx, font=f, fill=(30, 30, 30))
        snow(im, t)
        if t > 1.6:
            p = back(prog(t, 1.6, 0.4)); paste_c(im, emoji_img("🏖️", int(150 * max(0.01, p))), W / 2 - 110, 1120)
            d = ImageDraw.Draw(im); d.text((W / 2 - 20, 1070), "× 63", font=F(96, "BL"), fill="white")
        caption(im, t, V3_TXT[0], L, V3_VO[0], lang="en"); return im
    S.append((D(V3_VO[0]), s0))
    def s1(t):
        im = gallery(t, speed=1100, counter="Saved · 63")
        snow(im, t)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(prog(t, 0.5, 0.3)); od.rounded_rectangle((120, 780, W - 120, 1020), radius=40, fill=(255, 255, 255, int(240 * a))); im.alpha_composite(ov)
        if a > 0.4:
            d = ImageDraw.Draw(im); f = F(72, "BL"); tx = "Outside: 4°C"; d.text((180, 855), tx, font=f, fill=(24, 26, 22))
            paste_c(im, emoji_img("🥶", 140), W - 230, 900)
        return im
    S.append((2.6, s1))
    def s2(t):
        im = bg_grad((242, 237, 227), (225, 218, 202)); d = ImageDraw.Draw(im)
        d.text((100, 300), "This weekend", font=F(84, "BL"), fill=(27, 48, 32))
        for k, day in enumerate(["Saturday", "Sunday"]):
            y = 470 + k * 230; a = ease(prog(t, 0.2 + k * 0.3, 0.3))
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle((100, y, W - 100, y + 190), radius=34, fill=(255, 255, 255, int(255 * a))); im.alpha_composite(ov)
            d = ImageDraw.Draw(im); d.text((150, y + 30), day, font=F(52, "B"), fill=(47, 82, 51))
            d.text((150, y + 100), "— nothing planned —", font=F(44, "M"), fill=(140, 134, 124))
        if t > 1.4: paste_c(im, emoji_img("🛋️", int(220 * max(0.01, back(prog(t, 1.4, 0.3))))), W / 2 - 120, 1130)
        if t > 1.8: paste_c(im, emoji_img("😐", int(170 * max(0.01, back(prog(t, 1.8, 0.3))))), W / 2 + 140, 1110)
        caption(im, t, V3_TXT[1], L, V3_VO[1], lang="en"); return im
    S.append((D(V3_VO[1]), s2))
    def s3(t):
        im = app_view(P[0], t, focus=(590, 1100), zoom=1.2, z0=0.2, z1=1.6, taps=[(3.0, 912, 2338)])
        caption(im, t, V3_TXT[2], L, V3_VO[2], lang="en"); return im
    S.append((D(V3_VO[2]), s3))
    sw = 1.9
    def s4(t):
        if t < sw:
            im = app_view(P[1], t, focus=(500, 760), zoom=1.35, z0=0.0, z1=0.8, taps=[(1.2, 275, 825)])
        else:
            im = app_view(P[2], t - sw, focus=(500, 1250), zoom=1.2, z0=0.1, z1=1.0, taps=[(1.7, 157, 1505)])
        caption(im, t, V3_TXT[3], L, V3_VO[3], lang="en"); return im
    S.append((D(V3_VO[3]) + 1.0, s4))
    S.append((2.8, lambda t: end_card(t, "Save it. Actually go.", lang="en")))
    return S, P

VIDS = {"1": V1, "2": V2, "3": V3}
if __name__ == "__main__":
    which, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
    S, P = VIDS[which]()
    os.makedirs(out, exist_ok=True)
    if mode == "stills":
        for i, (d, f) in enumerate(S):
            for fr in (0.25, 0.6, 0.9):
                f(d * fr).convert("RGB").resize((540, 960)).save(f"{out}/v{which}_{i}_{int(fr*100)}.jpg", quality=80)
        print("total", round(sum(d for d, _ in S), 2), P)
    else:
        render(f"V{which}", S, out, sys.argv[4])
        print("screens", P)
