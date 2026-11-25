"""2026-11-25 videoları — yeni kısa format (12–18 sn, punchline ile açılış, hook() 0. kareden).
Kullanım: python3 vids7.py <1|2> stills OUTDIR  |  python3 vids7.py <1|2> render OUTDIR final.mp4"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v4 import *
from vids4 import render, L
from vids6 import stamp, pop, YEL
import datetime as dt

TODAY = dt.date(2026, 11, 25)
def D(v): return round((v + 0.3) * 30) / 30          # sahne = seslendirme + 0.3 sn

# ---------------- 1) Mesajlaşma: Annemden gelen reeller (Ahmet) ----------------
V1_TXT = ["Annem sabah altıda reel atar. Ben: kaydettim anne.",
          "Üç hafta sonra: O sütlacı yaptın mı?",
          "Sonra'yı aç. Yap listesinde: beş malzemeli sütlaç."]
V1_VO = [4.4, 2.72, 5.6]
V1_SCR = [("yemek", "tr", "light", "kart-yap-2")]
V1_HOOK = "Annenden kaç reel birikti?"

def reel_tile(im, y, label, col, a=1.0, me=False, w=340, h=420):
    x0 = W - 50 - w if me else 50
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle((x0, y, x0 + w, y + h), radius=34, fill=col + (int(255 * a),))
    cx, cy = x0 + w / 2, y + h / 2 - 30
    d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), outline=(255, 255, 255, int(230 * a)), width=7)
    d.polygon([(cx - 14, cy - 22), (cx - 14, cy + 22), (cx + 26, cy)], fill=(255, 255, 255, int(255 * a)))
    d.rounded_rectangle((x0, y + h - 96, x0 + w, y + h), radius=34, fill=(0, 0, 0, int(110 * a)))
    d.text((x0 + 26, y + h - 72), label, font=F(36, "SB"), fill=(255, 255, 255, int(255 * a)))
    im.alpha_composite(ov)
    return y + h + 26

def photo_tile(im, y, a=1.0):
    w, h = 400, 400; x0 = W - 50 - w
    tile = bg_grad((246, 222, 170), (214, 160, 90)).resize((w, h)); m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=34, fill=int(255 * a))
    tile.putalpha(m); im.alpha_composite(tile, (x0, int(y)))
    paste_c(im, emoji_img("🍮", 200), x0 + w / 2, y + h / 2, a)
    return y + h + 26

def badge(im, n):
    d = ImageDraw.Draw(im); tx = f"{n}"; f = F(48, "BL"); w = f.getlength(tx) + 50
    d.rounded_rectangle((W - 60 - w, 130, W - 60, 200), radius=35, fill=(230, 50, 50)); d.text((W - 60 - w + 25, 136), tx, font=f, fill="white")

def time_pill(im, tx, y=330):
    d = ImageDraw.Draw(im); f = F(34, "SB"); w = f.getlength(tx)
    d.text(((W - w) / 2, y), tx, font=f, fill=(140, 140, 145))

def run_chat(im, t, items, y0=600, bottom=1330):
    """items: (start, kind, payload). Görünenleri dizer; alt sınırı geçerse yukarı kaydırır (iki geçiş)."""
    def lay(target, y):
        for (st, kind, p) in items:
            if t < st: break
            a = ease(prog(t, st, 0.15))
            if kind == "reel": y = reel_tile(target, y, p[0], p[1], a)
            elif kind == "photo": y = photo_tile(target, y, a)
            elif kind == "time":
                d = ImageDraw.Draw(target); f = F(34, "SB"); d.text(((W - f.getlength(p)) / 2, y), p, font=f, fill=(140, 140, 145)); y += 70
            else: y = bubble(target, p[0], kind == "me", y, a, emo=p[1] if len(p) > 1 else None)
        return y
    end = lay(Image.new("RGBA", (W, H)), y0)
    lay(im, y0 - max(0, end - bottom))
    ov = ImageDraw.Draw(im); ov.rectangle((0, 0, W, 300), fill=(247, 247, 247)); ov.line((0, 300, W, 300), fill=(220, 220, 220), width=2)

def mom_head(im):
    hd = chat_base("Annem ❤️"[:-2], "👩")
    im.alpha_composite(hd.crop((0, 0, W, 302)), (0, 0))
    d = ImageDraw.Draw(im); f = F(36, "SB"); x = W / 2 + F(36, "SB").getlength("Annem") / 2 + 12
    paste_c(im, emoji_img("❤️", 34), x + 18, 244)

def V1():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V1_SCR]
    R = [(214, 120, 70), (120, 150, 90), (200, 160, 60), (150, 90, 120), (90, 130, 170), (220, 170, 110)]
    def s0(t):
        im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        items = [(-1, "time", "Bugün 06:12"), (-1, "reel", ("Mutlaka izle", R[0])), (-1, "mom", ("Çok faydalı 🙏"[:-2], "🙏")),
                 (0.25, "reel", ("Fırın sütlaç", R[2])), (0.9, "mom", ("Babana yaparsın", None)),
                 (1.5, "reel", ("Sabah sporu", R[4])), (2.1, "reel", ("Herkes bilmeli", R[3])),
                 (3.0, "me", ("Kaydettim anne", "👍"))]
        run_chat(im, t, items, y0=620); ImageDraw.Draw(im).rectangle((0, 302, W, 560), fill=(255, 255, 255)); mom_head(im)
        badge(im, 47 + int(5 * ease(prog(t, 0.2, 2.2))))
        hook(im, t, V1_HOOK, y=330)
        caption(im, t, V1_TXT[0], L, V1_VO[0]); return im
    S.append((D(V1_VO[0]), s0))
    def s1(t):
        im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        items = [(-1, "time", "3 hafta sonra · 21:40"), (-1, "mom", ("O sütlacı yaptın mı?", None)),
                 (1.0, "mom", ("Fotoğrafını at", "📸")), (1.8, "mom", ("Teyzene de söyledim", "🙂"))]
        run_chat(im, t, items, y0=420); mom_head(im)
        im = zoom_view(im, t, D(V1_VO[1]), (W / 2 - 120, 760, 1.3), t0=0.0, t1=0.6)
        caption(im, t, V1_TXT[1], L, V1_VO[1]); return im
    S.append((D(V1_VO[1]), s1))
    AW = 3.0          # uygulama en fazla 3 sn
    def s2(t):
        im = app_view(P[0], t, focus=(560, 1500), zoom=1.3, z0=0.0, z1=1.2, taps=[(2.1, 544, 2160)], bg=((246, 238, 222), (230, 214, 186)))
        if t > 2.3: pop(im, "✅", 150, W - 190, 420, t, 2.3)
        caption(im, t, V1_TXT[2], L, V1_VO[2]); return im
    S.append((AW, s2))
    def s3(t):
        tt = t + AW
        im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        items = [(-1, "time", "21:52"), (-1, "mom", ("O sütlacı yaptın mı?", None)), (0.0, "photo", None),
                 (0.5, "me", ("Yaptım anne", None)), (1.2, "mom", ("Aferin oğluma", "😍"))]
        run_chat(im, t, items, y0=420); mom_head(im)
        caption(im, tt, V1_TXT[2], L, V1_VO[2]); return im
    S.append((round(D(V1_VO[2]) - AW, 2), s3))
    S.append((1.2, lambda t: end_short(t, "Annen soracak. Hazır ol.")))
    return S, P

# ---------------- 2) Gündem: Efsane Cuma gecesi aramaları (Cavit) ----------------
V2_TXT = ["Efsane Cuma'ya iki gün kaldı. Herkes aynı şeyi arıyor.",
          "Hani reelde gördüğüm o şey? Kaydettim ama nereye?",
          "Sonra'ya kaydet. Satın Al listesinde bekler."]
V2_VO = [3.92, 3.92, 3.2]
V2_SCR = [("alisveris", "tr", "dark", "kart-satin-al")]
V2_HOOK = "Cuma gecesi böyle mi arayacaksın?"
NIGHT = ((24, 18, 52), (8, 6, 20))

def magnifier(d, x, y, col):
    d.ellipse((x - 22, y - 22, x + 16, y + 16), outline=col, width=7); d.line((x + 12, y + 12, x + 30, y + 30), fill=col, width=8)

def search_scene(t, q, typed, res_at, n_search, clock, red=False):
    im = bg_grad(*NIGHT); d = ImageDraw.Draw(im)
    f = F(40, "SB"); tx = "⏳"; pill = "Efsane Cuma'ya 2 gün"
    d.rounded_rectangle((70, 150, 70 + f.getlength(pill) + 110, 222), radius=36, fill=(255, 214, 90))
    paste_c(im, emoji_img("⏳", 44), 112, 186); d.text((150, 160), pill, font=f, fill=(40, 30, 10))
    fc = F(48, "BL"); d.text((W - 70 - fc.getlength(clock), 160), clock, font=fc, fill=(255, 90, 90) if red else (255, 255, 255))
    # arama çubuğu
    y = 720; d.rounded_rectangle((70, y, W - 70, y + 130), radius=65, fill=(255, 255, 255))
    magnifier(d, 140, y + 65, (120, 120, 125))
    fq = F(46, "M"); shown = q[:max(0, int(typed))]
    while fq.getlength(shown) > W - 70 - 200 - 60: shown = shown[1:]
    d.text((190, y + 38), shown, font=fq, fill=(20, 20, 20))
    if int(t * 2.5) % 2 == 0: cx = 190 + fq.getlength(shown) + 6; d.line((cx, y + 32, cx, y + 100), fill=(60, 120, 255), width=5)
    d.text((80, y + 160), f"Arama #{n_search}", font=F(36, "SB"), fill=(170, 165, 200))
    if t >= res_at:
        p = back(prog(t, res_at, 0.3)); sh = int(18 * math.sin((t - res_at) * 40) * (1 - prog(t, res_at, 0.4)))
        fr = F(int(120 * max(0.05, p)), "BL"); r = "0 sonuç"
        d.text(((W - fr.getlength(r)) / 2 + sh, 1050), r, font=fr, fill=(255, 90, 90))
        pop(im, "😩", 150, W / 2, 1290, t, res_at + 0.1)
    return im

def V2():
    S = []; P = [lib_pick(*x, today=TODAY) for x in V2_SCR]
    Q0 = "instagramda gördüğüm yeşil lamba"
    def s0(t):
        if t < 2.3: im = search_scene(t, Q0, 17 + 16 * ease(prog(t, 0.0, 1.0)), 1.2, 1, "23:56")
        else:
            q = "tiktokta kızın sürdüğü krem"; im = search_scene(t, q, len(q) * prog(t, 2.3, 0.9), 3.4, 2, "23:57")
        hook(im, t, V2_HOOK, y=330)
        caption(im, t, V2_TXT[0], L, V2_VO[0]); return im
    S.append((D(V2_VO[0]), s0))
    def s1(t):
        qs = ["hani o beyaz ayakkabı", "reeldeki kahve makinesi", "kaydetmiştim ya şu mont"]
        k = min(2, int(t / 1.25)); t0 = k * 1.25; q = qs[k]
        clock = ["23:59", "00:00", "00:07"][k]
        im = search_scene(t, q, 4 + (len(q) - 4) * prog(t, t0, 0.55), t0 + 0.7, 3 + k, clock, red=k > 0)
        if t > 3.55:
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 110)))
            stamp(im, "BULAMADIM", t, 3.55, cy=900, size=120)
        caption(im, t, V2_TXT[1], L, V2_VO[1]); return im
    S.append((D(V2_VO[1]), s1))
    def s2(t):
        im = app_view(P[0], t, focus=(560, 1400), zoom=1.3, z0=0.0, z1=1.1, taps=[(2.2, 845, 2160)], bg=((40, 34, 70), (12, 10, 26)))
        pop(im, "🧥", 140, W - 190, 420, t, 1.0)
        caption(im, t, V2_TXT[2], L, V2_VO[2]); return im
    S.append((3.0, s2))
    S.append((1.2, lambda t: end_short(t, "Aradığın zaten kayıtlı.")))
    return S, P

VIDS = {"1": V1, "2": V2}
if __name__ == "__main__":
    which, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
    S, P = VIDS[which]()
    os.makedirs(out, exist_ok=True)
    if mode == "stills":
        t0 = 0
        for i, (d, f) in enumerate(S):
            for fr in (0.0, 0.5, 0.95):
                f(d * fr).convert("RGB").resize((540, 960)).save(f"{out}/v{which}_{i}_{int(fr*100)}.jpg", quality=80)
        print("total", round(sum(d for d, _ in S), 2), P)
    else:
        render(f"V{which}", S, out, sys.argv[4])
        print("screens", P)
