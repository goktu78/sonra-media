"""2026-11-24 videoları. Ekranlar library.json'dan (rotasyon kuralı), altyazılar v4.caption (tek satır kuralı).
Kullanım: python3 vids6.py <1|2|3> stills OUTDIR  |  python3 vids6.py <1|2|3> render OUTDIR final.mp4"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v4 import *
from vids4 import render, D, L
from vids5 import card_text
import datetime as dt

TODAY = dt.date(2026, 11, 24)
YEL = (255, 214, 90)

def pop(im, ch, size, x, y, t, t0, d=0.35):
    if t > t0: paste_c(im, emoji_img(ch, int(size * max(0.01, back(prog(t, t0, d))))), x, y)

def stamp(im, text, t, t0, cx=W / 2, cy=900, col=(220, 50, 50), size=120, rot=-8):
    p = prog(t, t0, 0.25)
    if p <= 0: return
    s = 2.2 - 1.2 * ease(p); f = F(size, "BL")
    st = Image.new("RGBA", (int(f.getlength(text)) + 80, size + 80), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((6, 6, st.width - 6, st.height - 6), radius=24, outline=col + (255,), width=12)
    sd.text((40, 28), text, font=f, fill=col + (255,))
    st = st.rotate(rot, expand=True, resample=Image.BICUBIC)
    st = st.resize((max(1, int(st.width * s)), max(1, int(st.height * s))))
    paste_c(im, st, cx, cy, alpha=ease(p))

def panel(im, box, a=1.0, fill=(255, 255, 255), r=44):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle(box, radius=r, fill=fill + (int(240 * a),))
    im.alpha_composite(ov)

# ---------------- 1) Gündem: herkes yıl özetini bekliyor (Deniz Sab) ----------------
V1_TXT = ["Herkes yıl özetini bekliyor. Seninki çoktan hazır.",
          "En aktif saatin: gece bir kırk yedi. Tebrikler.",
          "Sonra her linki ayırır. Keşfette Bana bir şey seç, yeter.",
          "Bugünkü seçim: balkonda fesleğen. Seneye özetin: Yaptım."]
V1_VO = [3.6, 3.84, 4.64, 5.84]
V1_SCR = [("genel", "tr", "dark", "kesfet"), ("genel", "tr", "dark", "kesfet-sec")]
RECAP = [((92, 44, 140), (30, 14, 60)), ((214, 92, 52), (110, 30, 40)), ((20, 70, 120), (8, 20, 50)), ((47, 82, 51), (16, 34, 20))]

def recap_head(im, k):
    d = ImageDraw.Draw(im); f = F(40, "SB"); tx = "KAYDETTİKLERİNİN YIL ÖZETİ"
    d.text(((W - f.getlength(tx)) / 2, 220), tx, font=f, fill=(255, 255, 255, 220))
    for i in range(4):
        x0 = W / 2 - 200 + i * 104
        d.rounded_rectangle((x0, 290, x0 + 90, 300), radius=5, fill=(255, 255, 255) if i <= k else (255, 255, 255, 90))

def V1():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V1_SCR]
    def s0(t):
        im = bg_grad(*RECAP[0]); recap_head(im, 0)
        p = back(prog(t, 0.1, 0.5)); f = F(int(300 * max(0.05, p)), "BL"); d = ImageDraw.Draw(im)
        d.text(((W - f.getlength("2026")) / 2, 620 - f.size / 2), "2026", font=f, fill=YEL)
        if t > 0.9: card_text(im, ["Özetin hazır."], 860, 84, (255, 255, 255), "XB", a=ease(prog(t, 0.9, 0.3)))
        pop(im, "🎉", 170, 230, 1130, t, 1.3); pop(im, "🔖", 150, W / 2, 1180, t, 1.5); pop(im, "🎊", 170, W - 230, 1130, t, 1.7)
        caption(im, t, V1_TXT[0], L, V1_VO[0]); return im
    S.append((D(V1_VO[0]), s0))
    def s1(t):
        im = bg_grad(*RECAP[1]); recap_head(im, 1)
        card_text(im, ["Bu yıl kaydettiğin"], 420, 70, (255, 255, 255), "XB")
        n = int(1284 * ease(prog(t, 0.2, 1.4))); tx = f"{n:,}".replace(",", ".")
        f = F(260, "BL"); d = ImageDraw.Draw(im); d.text(((W - f.getlength(tx)) / 2, 540), tx, font=f, fill=YEL)
        if t > 1.2: card_text(im, ["link, reel, tarif, video…"], 870, 54, (255, 235, 220), "SB", a=ease(prog(t, 1.2, 0.3)))
        pop(im, "📲", 170, W / 2, 1120, t, 1.5)
        return im
    S.append((2.4, s1))
    def s2(t):
        im = bg_grad(*RECAP[2]); recap_head(im, 2)
        card_text(im, ["En aktif saatin"], 420, 70, (255, 255, 255), "XB")
        p = back(prog(t, 0.2, 0.45)); f = F(int(250 * max(0.05, p)), "BL"); d = ImageDraw.Draw(im)
        d.text(((W - f.getlength("01:47")) / 2, 680 - f.size / 2), "01:47", font=f, fill=YEL)
        pop(im, "🦉", 190, W / 2 - 170, 1040, t, 0.8); pop(im, "🌙", 150, W / 2 + 170, 1020, t, 1.0)
        if t > 2.6: card_text(im, ["Tebrikler 👏"[:-2]], 1180, 64, (255, 255, 255), "XB", a=ease(prog(t, 2.6, 0.3)))
        pop(im, "👏", 90, W / 2 + 240, 1220, t, 2.7)
        caption(im, t, V1_TXT[1], L, V1_VO[1]); return im
    S.append((D(V1_VO[1]), s2))
    def s3(t):
        im = bg_grad(*RECAP[3]); recap_head(im, 3)
        if t < 1.5:
            card_text(im, ["Kaydedip açtığın"], 420, 70, (255, 255, 255), "XB")
            f = F(300, "BL"); d = ImageDraw.Draw(im); d.text(((W - f.getlength("9")) / 2, 520), "9", font=f, fill=YEL)
            stamp(im, "%0,7", t, 0.6, cy=1000, col=(255, 120, 100), size=110)
        else:
            card_text(im, ["Yılın unvanı"], 420, 70, (255, 255, 255), "XB")
            pop(im, "🐿️", 300, W / 2, 720, t, 1.5)
            if t > 1.8: card_text(im, ["Dijital Sincap"], 930, 110, YEL, "BL", a=ease(prog(t, 1.8, 0.25)))
            if t > 2.2: card_text(im, ["Topluyor. Saklıyor. Unutuyor."], 1090, 48, (230, 240, 230), "SB", a=ease(prog(t, 2.2, 0.3)))
        return im
    S.append((3.0, s3))
    def s4(t):
        im = app_view(P[0], t, focus=(590, 780), zoom=1.4, z0=0.2, z1=1.4, taps=[(2.9, 690, 825)], bg=((30, 32, 30), (10, 12, 10)))
        caption(im, t, V1_TXT[2], L, V1_VO[2]); return im
    S.append((D(V1_VO[2]), s4))
    def s5(t):
        im = app_view(P[1], t, focus=(590, 1250), zoom=1.2, z0=0.2, z1=1.4, taps=[(3.3, 202, 1508)], bg=((30, 32, 30), (10, 12, 10)))
        pop(im, "🌿", 150, W - 170, 430, t, 1.6)
        if t > 4.4:
            p = back(prog(t, 4.4, 0.35))
            st = Image.new("RGBA", (620, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rounded_rectangle((0, 0, 619, 149), radius=36, fill=YEL); f = F(64, "BL"); tx = "2027: Yaptım ✓"[:-2]
            sd.text((40, 38), tx, font=f, fill=(27, 48, 32)); sd.text((40 + f.getlength(tx) + 18, 38), "✓", font=F(64, "BL"), fill=(47, 120, 51))
            st = st.rotate(5, expand=True, resample=Image.BICUBIC).resize((max(1, int(st.width * p)), max(1, int(st.height * p))))
            paste_c(im, st, W / 2, 560)
        caption(im, t, V1_TXT[3], L, V1_VO[3]); return im
    S.append((D(V1_VO[3]), s5))
    S.append((2.6, lambda t: end_card(t, "Bu yıl kaydet. Seneye yap.")))
    return S, P

# ---------------- 2) Ben: sonra izlerim / 3 ay sonra — KPSS (Zuhal) ----------------
V2_TXT = ["Eylül. Yeni dönem. KPSS tarih videosunu kaydettim. Sonra izlerim.",
          "Gece üç. Kaydedilenlerde altı yüz video. Hangisiydi?",
          "Sonrada ara: KPSS. Yirmi dakikalık video tek sonuçta karşında.",
          "Sıradaki de hazır: Oku kartında dört saatlik final planı."]
V2_VO = [5.44, 5.92, 5.84, 4.24]
V2_SCR = [("ogrenci", "tr", "light", "ekle"), ("ogrenci", "tr", "light", "arama-kpss"), ("ogrenci", "tr", "light", "kart-oku")]
SUN = ((250, 226, 170), (238, 196, 120))

def V2():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V2_SCR]
    sw = 2.4
    def s0(t):
        if t < sw:
            im = bg_grad(*SUN); d = ImageDraw.Draw(im)
            d.text((90, 230), "Ben, eylülde:", font=F(80, "BL"), fill=(60, 40, 10))
            card_text(im, ["Eylül"], 470, 200, (27, 48, 32), "BL", a=ease(prog(t, 0.1, 0.4)))
            if t > 0.8: card_text(im, ["Yeni dönem, yeni ben."], 760, 64, (90, 60, 20), "XB", a=ease(prog(t, 0.8, 0.3)))
            pop(im, "📚", 170, W / 2 - 200, 1060, t, 1.1); pop(im, "✏️", 150, W / 2, 1080, t, 1.3); pop(im, "☀️", 170, W / 2 + 200, 1060, t, 1.5)
        else:
            im = app_view(P[0], t - sw, focus=(590, 900), zoom=1.3, z0=0.0, z1=0.8, taps=[(0.9, 590, 740), (2.3, 590, 1150)], bg=SUN)
            if t - sw > 2.5: stamp(im, "SONRA İZLERİM", t, sw + 2.5, cy=650, col=(47, 82, 51), size=90, rot=-6)
        caption(im, t, V2_TXT[0], L, V2_VO[0]); return im
    S.append((D(V2_VO[0]), s0))
    def s1(t):
        im = bg_grad((20, 20, 26), (6, 6, 10))
        p = back(prog(t, 0.05, 0.4)); f = F(int(170 * max(0.05, p)), "BL"); d = ImageDraw.Draw(im)
        for i, ln in enumerate(["3 AY", "SONRA"]):
            d.text(((W - f.getlength(ln)) / 2, 640 + i * 190 - f.size / 2), ln, font=f, fill=(255, 255, 255))
        if t > 0.8: card_text(im, ["Final haftası"], 1080, 60, YEL, "XB", a=ease(prog(t, 0.8, 0.3)))
        pop(im, "⏰", 150, W / 2, 380, t, 0.4)
        return im
    S.append((1.8, s1))
    cw = 3.1
    def s2(t):
        if t < cw:
            n = int(120 + 480 * ease(prog(t, 0, 2.4)))
            im = gallery(t, speed=1500 if t < 2.4 else 300, counter=f"Kaydedilenler · {n}", timer="03:12")
            if t > 2.3:
                im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120)))
                pop(im, "😵‍💫"[:1], 220, W / 2, 850, t, 2.3)
        else:
            tt = t - cw; im = chat_base("KPSS Çalışma Grubu", "📚"); y = 360
            msgs = [("Osmanlı kuruluşu videosu kimdeydi?", False, None), ("Bende kayıtlı ama", True, None),
                    ("bulamıyorum", True, "🫠"), ("Bende de 😭"[:-2], False, "😭"), ("Bulan atsın, yarın sınav", False, "🙏")]
            for k, (tx, me, emo) in enumerate(msgs):
                st = 0.1 + k * 0.5
                if tt > st: y = bubble(im, tx, me, y, ease(prog(tt, st, 0.15)), emo=emo)
        caption(im, t, V2_TXT[1], L, V2_VO[1]); return im
    S.append((D(V2_VO[1]), s2))
    def s3(t):
        im = app_view(P[1], t, focus=(600, 700), zoom=1.35, z0=0.3, z1=1.5, taps=[(1.0, 566, 320), (3.9, 613, 896)])
        pop(im, "🎯", 150, W - 170, 1180, t, 4.2)
        caption(im, t, V2_TXT[2], L, V2_VO[2]); return im
    S.append((D(V2_VO[2]), s3))
    def s4(t):
        im = app_view(P[2], t, focus=(590, 1250), zoom=1.15, z0=0.2, z1=1.4, taps=[(3.2, 910, 2334)])
        pop(im, "💪", 150, W - 170, 430, t, 2.0)
        caption(im, t, V2_TXT[3], L, V2_VO[3]); return im
    S.append((D(V2_VO[3]), s4))
    S.append((2.6, lambda t: end_card(t, "Kaydettiğin ders, sınav gecesi yanında.")))
    return S, P

# ---------------- 3) Mesajlaşma: Yılbaşı grubu, 186 reel (Deniz) ----------------
V3_TXT = ["Yılbaşı grubu kuruldu. İlk hafta: yüz seksen altı reel.",
          "Karar? Yok. Herkes ilk atılan Kapadokya videosunu arıyor.",
          "Linkleri Sonraya atın. Hepsi Git listesinde yan yana durur.",
          "Kapadokya yaz. O tepe ilk sonuçta. Karar beş dakikada."]
V3_VO = [4.24, 4.64, 4.24, 4.4]
V3_SCR = [("seyahat", "tr", "dark", "liste"), ("seyahat", "tr", "dark", "arama-kapadokya")]
NAMES = ["Ece", "Mert", "Selin", "Can", "Deniz", "Bora"]

def reel_bubble(im, k, y, a=1.0):
    me = k % 3 == 1; col = TILES[(k * 7) % len(TILES)]; bw, bh = 330, 440
    x0 = W - 50 - bw if me else 120
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=34, fill=col + (int(255 * a),))
    cx, cy = x0 + bw / 2, y + bh / 2 - 20
    d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=(255, 255, 255, int(220 * a)), width=7)
    d.polygon([(cx - 14, cy - 22), (cx - 14, cy + 22), (cx + 26, cy)], fill=(255, 255, 255, int(255 * a)))
    d.text((x0 + 26, y + bh - 70), "Reel", font=F(40, "SB"), fill=(255, 255, 255, int(255 * a)))
    im.alpha_composite(ov)
    if not me:
        ImageDraw.Draw(im).text((x0 + 10, y - 44), NAMES[k % len(NAMES)], font=F(32, "SB"), fill=(130, 130, 135))
    return y + bh + 70

def group_chat(t, n, scroll=0.0, k0=0):
    im = chat_base("Yılbaşı 2027 · 6 kişi", "🎄")
    body = Image.new("RGBA", (W, H), (255, 255, 255, 255)); y = 380 - scroll
    k = k0
    while y < H:
        if y > -500: y = reel_bubble(body, k, y)
        else: y += 510
        k += 1
    im.alpha_composite(body.crop((0, 302, W, H)), (0, 302))
    d = ImageDraw.Draw(im); tx = f"{n}"; f = F(48, "BL"); w = f.getlength(tx) + 50
    d.rounded_rectangle((W - 60 - w, 130, W - 60, 200), radius=35, fill=(230, 50, 50)); d.text((W - 60 - w + 25, 138), tx, font=f, fill="white")
    return im

def V3():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V3_SCR]
    def s0(t):
        n = int(3 + 183 * ease(prog(t, 0.3, D(V3_VO[0]) - 0.8)))
        im = group_chat(t, n, scroll=max(0, t - 1.0) * 700)
        caption(im, t, V3_TXT[0], L, V3_VO[0]); return im
    S.append((D(V3_VO[0]), s0))
    def s1(t):
        im = chat_base("Yılbaşı 2027 · 6 kişi", "🎄"); y = 360
        msgs = [("Bu çok iyi", False, "😍"), ("Bu da olur bence", False, None), ("İlk attığın neydi?", True, None),
                ("Yukarı kaydır", False, "👆"), ("Kaydırdım, bitmiyor", True, "😭")]
        for k, (tx, me, emo) in enumerate(msgs):
            st = 0.1 + k * 0.45
            if t > st: y = bubble(im, tx, me, y, ease(prog(t, st, 0.15)), emo=emo)
        return im
    S.append((2.6, s1))
    def s2(t):
        im = group_chat(t, 186, scroll=max(0, 9000 - t * 2600), k0=0)
        d = ImageDraw.Draw(im); f = F(44, "SB"); tx = "↑ 3 gün önce"
        d.rounded_rectangle((W / 2 - f.getlength(tx) / 2 - 30, 330, W / 2 + f.getlength(tx) / 2 + 30, 410), radius=40, fill=(40, 40, 45))
        d.text((W / 2 - f.getlength(tx) / 2, 340), tx, font=f, fill="white")
        if t > 2.6:
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
            stamp(im, "KARAR: YOK", t, 2.6, cy=880, size=120)
        caption(im, t, V3_TXT[1], L, V3_VO[1]); return im
    S.append((D(V3_VO[1]), s2))
    def s3(t):
        im = bg_grad((30, 26, 60), (10, 8, 24))
        card_text(im, ["30 Aralık"], 420, 150, (255, 255, 255), "BL", a=ease(prog(t, 0.05, 0.3)))
        if t > 0.6: card_text(im, ["Grup hâlâ evde."], 650, 72, YEL, "XB", a=ease(prog(t, 0.6, 0.3)))
        pop(im, "🛋️", 260, W / 2, 1000, t, 0.9); pop(im, "🎆", 150, W / 2 - 280, 860, t, 1.2); pop(im, "🎆", 150, W / 2 + 280, 860, t, 1.4)
        return im
    S.append((2.2, s3))
    def s4(t):
        im = app_view(P[0], t, focus=(590, 1150), zoom=1.2, z0=0.2, z1=1.4, taps=[(2.4, 495, 472)], bg=((30, 32, 30), (10, 12, 10)))
        caption(im, t, V3_TXT[2], L, V3_VO[2]); return im
    S.append((D(V3_VO[2]), s4))
    def s5(t):
        im = app_view(P[1], t, focus=(600, 700), zoom=1.35, z0=0.2, z1=1.3, taps=[(0.7, 600, 320), (2.8, 637, 885)], bg=((30, 32, 30), (10, 12, 10)))
        pop(im, "🎉", 160, 200, 1290, t, 3.4); pop(im, "🏔️", 160, W - 200, 1290, t, 3.6)
        caption(im, t, V3_TXT[3], L, V3_VO[3]); return im
    S.append((D(V3_VO[3]) + 0.6, s5))
    S.append((2.6, lambda t: end_card(t, "Grup sohbeti değil, plan.")))
    return S, P

VIDS = {"1": V1, "2": V2, "3": V3}
if __name__ == "__main__":
    which, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
    S, P = VIDS[which]()
    os.makedirs(out, exist_ok=True)
    if mode == "stills":
        for i, (d, f) in enumerate(S):
            for fr in (0.3, 0.8):
                f(d * fr).convert("RGB").resize((540, 960)).save(f"{out}/v{which}_{i}_{int(fr*100)}.jpg", quality=80)
        print("total", round(sum(d for d, _ in S), 2), P)
    else:
        render(f"V{which}", S, out, sys.argv[4])
        print("screens", P)
