import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v4 import *

L = 0.15
def D(v): return round((v + 0.6) * 30) / 30

A_TXT = ["Saat gece ikiyi geçiyor ve ben bir makarna tarifi kaydediyorum. Çünkü yarın kesin yapacağım.",
         "Üç ay sonra.", "Bin iki yüz seksen dört kayıt. Makarna yok. Umut da yok.",
         "Neyse ki artık paylaş diyorum, Sonraya kaydet. Tarif kendiliğinden Yap listesine düşüyor.",
         "Canım sıkılınca da on beş dakikam var diyorum ve kendi kaydettiklerimden birini önüme koyuyor.",
         "Sonra. Kaydettiğini, gerçekten yap."]
A_VO = [6.8, 1.84, 5.36, 6.48, 6.08, 3.28]
B_TXT = ["Arkadaşın soruyor: Geçen attığın o kafe neydi ya?", "Sen: Dur bakıyorum. Ve galeriye giriyorsun.",
         "Kırk yedi saniye sonra hâlâ Kapadokya tatilinden kalma bir ekran görüntüsündesin.",
         "Boşver, başka yere oturduk. Klasik.",
         "Oysa Sonrada kafe yazsan, bir saniyede karşında. Mekan linkleri zaten kendiliğinden Git listesinde.",
         "Sonra. Kaydet, kaybetme."]
B_VO = [4.88, 3.92, 5.6, 3.84, 7.28, 2.8]

def A():
    S = []
    def s0(t):
        im = bg_grad((10, 12, 30), (40, 30, 60)); d = ImageDraw.Draw(im)
        d.text((W / 2 - F(60, "B").getlength("Ben, gece:") / 2, 260), "Ben, gece:", font=F(60, "B"), fill=(200, 200, 230))
        clk = "01:47"; f = F(250, "R"); d.text(((W - f.getlength(clk)) / 2, 340), clk, font=f, fill="white")
        p = back(prog(t, 0.3, 0.5)); paste_c(im, emoji_img("🍝", int(300 * max(0.01, p))), W / 2, 900)
        if t > 3.6:
            p2 = back(prog(t, 3.6, 0.35)); paste_c(im, emoji_img("🔖", int(170 * max(0.01, p2))), W / 2 + 230, 780)
            if t > 3.9:
                d = ImageDraw.Draw(im); txt = "Kaydedildi ✓"; f2 = F(48, "B")
                d.rounded_rectangle((W / 2 - 200, 1130, W / 2 + 200, 1220), radius=45, fill=(255, 255, 255, 235))
                d.text((W / 2 - f2.getlength(txt) / 2, 1148), txt, font=f2, fill=INK)
        if t > 5.2:
            paste_c(im, emoji_img("😌", 120), W / 2 - 250, 1180)
        caption(im, t, A_TXT[0], L, A_VO[0]); return im
    S.append((D(A_VO[0]), s0))
    def s1(t):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
        s = 1 + 0.08 * t; f = F(int(150 * s), "BL"); txt = "3 AY SONRA"
        d.text(((W - f.getlength(txt)) / 2, H / 2 - 110 * s), txt, font=f, fill="white")
        return im
    S.append((D(A_VO[1]), s1))
    def s2(t):
        n = int(400 + 884 * ease(prog(t, 0, 2.5)))
        im = gallery(t, speed=1400 if t < 3 else 300, counter=f"Kaydedilenler · {n:,}".replace(",", "."))
        if t > 2.6:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 140)); im.alpha_composite(ov)
            p = back(prog(t, 2.6, 0.4)); paste_c(im, emoji_img("🪦", int(260 * max(0.01, p))), W / 2, 900)
            d = ImageDraw.Draw(im); f = F(64, "XB"); tx = "RIP makarna 🍝"[:-2]
            d.text(((W - f.getlength(tx)) / 2, 1080), tx, font=f, fill="white")
        caption(im, t, A_TXT[2], L, A_VO[2]); return im
    S.append((D(A_VO[2]), s2))
    ph = phone_img("paylas", 820)
    def s3(t):
        base = bg_grad((242, 237, 227), (225, 218, 202)); base.alpha_composite(ph, ((W - ph.width) // 2, 140))
        # target: "Sonra'ya Kaydet" row ~ (y 1765-580)*S*scale
        sc = 820 / screen("paylas").width; ry = 140 + 20 + (1765 - 580) * 1.28 * sc
        z = zoom_view(base, t, D(A_VO[3]), (W / 2, ry - 150, 1.3), t0=0.4, t1=2.2)
        # tap position after zoom
        if t > 2.3:
            s = 1.3; cy = H / 2 + (ry - (ry - 150)) * s; tap(z, t, 2.8, W / 2 - 80, cy)
        caption(z, t, A_TXT[3], L, A_VO[3], y=1560); return z
    S.append((D(A_VO[3]), s3))
    pk = phone_img("kesfet", 820)
    def s4(t):
        base = bg_grad((242, 237, 227), (225, 218, 202)); base.alpha_composite(pk, ((W - pk.width) // 2, 140))
        sc = 820 / 1179; chip_x = (W - pk.width) / 2 + 20 + 225 * 1.28 * sc; chip_y = 140 + 20 + 498 * 1.28 * sc
        z = zoom_view(base, t, D(A_VO[4]), (W / 2, chip_y + 80, 1.45), t0=0.3, t1=1.8)
        if t > 1.9:
            s = 1.45; tx = W / 2 + (chip_x - W / 2) * s; ty = H / 2 + (chip_y - (chip_y + 80)) * s
            tap(z, t, 2.2, tx, ty)
        caption(z, t, A_TXT[4], L, A_VO[4], y=1560); return z
    S.append((D(A_VO[4]), s4))
    S.append((D(A_VO[5]) + 1.0, lambda t: end_card(t, "Kaydettiğini gerçekten yap.")))
    return S

def B():
    S = []
    def s0(t):
        im = chat_base(); y = 380
        if t < 1.0: typing(im, y, t)
        else: bubble(im, "geçen attığın o kafe neydi yaa", False, y, ease(prog(t, 1.0, 0.2)))
        caption(im, t, B_TXT[0], L, B_VO[0]); return im
    S.append((D(B_VO[0]), s0))
    def s1(t):
        im = chat_base(); y = bubble(im, "geçen attığın o kafe neydi yaa", False, 380)
        if t > 0.3: bubble(im, "dur bakıyom", True, y, ease(prog(t, 0.3, 0.2)), emo="😅")
        if t > 2.4:
            g = gallery(t - 2.4, speed=200); a = ease(prog(t, 2.4, 0.5))
            g.putalpha(int(255 * a)); im.alpha_composite(g)
        caption(im, t, B_TXT[1], L, B_VO[1]); return im
    S.append((D(B_VO[1]), s1))
    def s2(t):
        sec = int(3 + 44 * ease(prog(t, 0, D(B_VO[2]) - 0.5)))
        im = gallery(t, speed=1600, timer=f"⏱ 0:{sec:02d}".replace("⏱ ", ""), counter="Fotoğraflar")
        if t > 2.4:
            p = back(prog(t, 2.4, 0.4)); paste_c(im, emoji_img("🎈", int(240 * max(0.01, p))), W / 2 - 160, 900)
            paste_c(im, emoji_img("🫠", int(240 * max(0.01, p))), W / 2 + 160, 900)
        caption(im, t, B_TXT[2], L, B_VO[2]); return im
    S.append((D(B_VO[2]), s2))
    def s3(t):
        im = chat_base(); y = bubble(im, "geçen attığın o kafe neydi yaa", False, 380)
        y = bubble(im, "dur bakıyom", True, y, emo="😅")
        if t > 0.2: y = bubble(im, "boşver başka yere oturduk", False, y, ease(prog(t, 0.2, 0.2)))
        if t > 1.6: paste_c(im, emoji_img("👍", 110), 120, y + 60); y += 140
        if t > 2.4: paste_c(im, emoji_img("😐", int(220 * max(0.01, back(prog(t, 2.4, 0.35))))), W / 2, 1150)
        caption(im, t, B_TXT[3], L, B_VO[3]); return im
    S.append((D(B_VO[3]), s3))
    pl = phone_img("sonra-liste", 820)
    def s4(t):
        base = bg_grad((242, 237, 227), (225, 218, 202)); base.alpha_composite(pl, ((W - pl.width) // 2, 140))
        sc = 820 / 1179; ox = (W - pl.width) / 2 + 20; oy = 160
        # type "kafe" into the real search bar
        if t > 0.8:
            d = ImageDraw.Draw(base); bx0, by0 = ox + 125 * 1.28 * sc, oy + 360 * 1.28 * sc
            d.rectangle((bx0, by0, bx0 + 560 * 1.28 * sc, by0 + 60 * 1.28 * sc), fill=(244, 240, 231))
            n = min(4, int((t - 0.8) / 0.18) + 1); d.text((bx0, by0 + 4), "kafe"[:n], font=F(int(44 * 1.28 * sc * 1.1), "M"), fill=INK)
        z = zoom_view(base, t, D(B_VO[4]), (W / 2, oy + 420 * 1.28 * sc + 200, 1.25), t0=0.2, t1=1.2)
        if t > 3.2:
            # highlight Git chip after zoom (real chip at display x 350-480, y 470-545)
            s = 1.25; cy0 = oy + 420 * 1.28 * sc + 200
            gx = W / 2 + (ox + 415 * 1.28 * sc - W / 2) * s; gy = H / 2 + (oy + 507 * 1.28 * sc - cy0) * s
            tap(z, t, 3.6, gx, gy)
        caption(z, t, B_TXT[4], L, B_VO[4], y=1560); return z
    S.append((D(B_VO[4]), s4))
    S.append((D(B_VO[5]) + 1.0, lambda t: end_card(t, "Kaydet, kaybetme.")))
    return S


C_TXT = ["Kasım ayı. İnsanoğlu, Black Friday'e beş gün kala sepetini hazırlamaya başlar.",
         "Ama önce, aylardır sonra alırım dediği ürünleri bulması gerekir.",
         "Ekran görüntüleri, kaydedilenler, kendine attığı linkler. Hiçbiri bulunamaz.",
         "Ve indirim biter. Ürün tükenmiştir.",
         "Akıllı olanlar ise linki paylaşır, Sonraya kaydeder. Ürün kendiliğinden Satın Al listesine düşer.",
         "Sonra. İndirim gelince, listen hazır."]
C_VO = [6.32, 4.72, 6.56, 4.8, 6.64, 3.12]
def C():
    S = []
    def s0(t):
        im = bg_grad((20, 32, 24), (8, 14, 10)); d = ImageDraw.Draw(im)
        f = F(44, "SB"); tx = "BİR SONRA. BELGESELİ"; d.text(((W - f.getlength(tx)) / 2, 300), tx, font=f, fill=(200, 190, 150))
        d.line((W/2 - 260, 370, W/2 + 260, 370), fill=(200, 190, 150), width=3)
        f2 = F(120, "BL"); a = ease(prog(t, 0.2, 0.6))
        for i, ln in enumerate(["Black Friday'e", "5 gün"]):
            col = (255, 255, 255) if i == 0 else (255, 200, 60)
            d.text(((W - f2.getlength(ln)) / 2, 470 + i * 140), ln, font=f2, fill=col + (int(255 * a),))
        p = back(prog(t, 1.2, 0.5)); paste_c(im, emoji_img("🛒", int(260 * max(0.01, p))), W / 2, 1040)
        caption(im, t, C_TXT[0], L, C_VO[0]); return im
    S.append((D(C_VO[0]), s0))
    def s1(t):
        im = bg_grad((20, 32, 24), (8, 14, 10)); d = ImageDraw.Draw(im)
        items = [("🎧", "kulaklık"), ("🧥", "mont"), ("☕", "kahve makinesi"), ("👟", "spor ayakkabı")]
        for k, (e, n) in enumerate(items):
            st = 0.3 + k * 0.6; p = back(prog(t, st, 0.4))
            if p <= 0: continue
            y = 380 + k * 260; paste_c(im, emoji_img(e, int(150 * max(0.01, p))), 260, y + 70)
            d.text((380, y + 30), n, font=F(66, "XB"), fill="white")
            d.text((380, y + 110), "“sonra alırım”", font=F(40, "M"), fill=(200, 190, 150))
        caption(im, t, C_TXT[1], L, C_VO[1]); return im
    S.append((D(C_VO[1]), s1))
    def s2(t):
        if t < 3.2:
            n = int(800 + 1547 * ease(prog(t, 0, 3)))
            im = gallery(t, speed=1500, counter=f"Ekran görüntüleri · {n:,}".replace(",", "."))
        else:
            im = chat_base("Ben (Sen)", "🙃"); y = 380
            for k, (txt, e) in enumerate([("bunu al", "👀"), ("bu mont indirimde al!!", "🔥"), ("unutma", "😤"), ("neydi bu", "🤔")]):
                if t > 3.3 + k * 0.45: y = bubble(im, txt, True, y, ease(prog(t, 3.3 + k * 0.45, 0.2)), emo=e)
        caption(im, t, C_TXT[2], L, C_VO[2]); return im
    S.append((D(C_VO[2]), s2))
    def s3(t):
        im = Image.new("RGBA", (W, H), (25, 20, 20, 255)); d = ImageDraw.Draw(im)
        paste_c(im, emoji_img("🧥", 300), W / 2, 760)
        if t > 1.6:
            p = back(prog(t, 1.6, 0.3)); f = F(int(170 * max(0.2, p)), "BL"); tx = "TÜKENDİ"
            st = Image.new("RGBA", (int(f.getlength(tx)) + 80, int(f.size * 1.5)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rounded_rectangle((0, 0, st.width - 1, st.height - 1), radius=20, outline=(230, 40, 40), width=14)
            sd.text((40, int(f.size * 0.12)), tx, font=f, fill=(230, 40, 40))
            st = st.rotate(-12, expand=True, resample=Image.BICUBIC); paste_c(im, st, W / 2, 780)
        if t > 3.0: paste_c(im, emoji_img("😭", 200), W / 2, 1150)
        caption(im, t, C_TXT[3], L, C_VO[3]); return im
    S.append((D(C_VO[3]), s3))
    ph = phone_img("paylas", 820); pl = phone_img("sonra-liste", 820)
    def s4(t):
        sw = 3.4
        base = bg_grad((242, 237, 227), (225, 218, 202))
        if t < sw:
            base.alpha_composite(ph, ((W - ph.width) // 2, 140))
            sc = 820 / screen("paylas").width; ry = 140 + 20 + (1765 - 580) * 1.28 * sc
            z = zoom_view(base, t, sw, (W / 2, ry - 150, 1.3), t0=0.3, t1=1.6)
            if t > 1.7: tap(z, t, 2.0, W / 2 - 80, H / 2 + 150 * 1.3)
        else:
            tt = t - sw; base.alpha_composite(pl, ((W - pl.width) // 2, 140))
            sc = 820 / 1179; ox = (W - pl.width) / 2 + 20; oy = 160
            cy0 = oy + 507 * 1.28 * sc
            z = zoom_view(base, tt, 3, (W / 2, cy0 + 200, 1.2), t0=0.1, t1=1.0)
            if tt > 1.1:
                s = 1.2; gx = W / 2 + (ox + 755 * 1.28 * sc - W / 2) * s; gy = H / 2 + (cy0 - (cy0 + 200)) * s
                tap(z, tt, 1.4, gx, gy)
        caption(z, t, C_TXT[4], L, C_VO[4], y=1560); return z
    S.append((D(C_VO[4]) + 0.6, s4))
    S.append((D(C_VO[5]) + 1.0, lambda t: end_card(t, "İndirim gelince listen hazır.")))
    return S

def render(name, S, outdir, final):
    files, starts, t0 = [], [], 0
    for i, (d, f) in enumerate(S):
        p = f"{outdir}/{name}_s{i}.mp4"
        render_scene(p, d, lambda fr, t, f=f: fr.im.alpha_composite(f(t)), (0, 0, 0)); files.append(p); starts.append(t0); t0 += d
    # sfx track: whoosh at cuts, pops
    from audio2 import SR
    n = int(t0 * SR); out = np.zeros(n); rng = np.random.default_rng(5)
    for s in starts[1:]:
        st = int((s - 0.15) * SR); Lw = int(0.4 * SR)
        if st + Lw < n:
            nz = np.convolve(rng.standard_normal(Lw), np.ones(10) / 10, "same"); out[st:st + Lw] += 0.25 * np.sin(np.pi * np.arange(Lw) / Lw) ** 2 * nz
    sfx = f"{outdir}/{name}_sfx.wav"
    d = (np.stack([out, out], 1) * 32767 * 0.8).astype(np.int16)
    with wave.open(sfx, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
    from lib import assemble
    assemble(files, sfx, final)
    print(name, "starts", [round(s, 3) for s in starts], "total", round(t0, 2))

if __name__ == "__main__":
    which, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
    S = {"A": A, "B": B, "C": C}[which]()
    if mode == "stills":
        for i, (d, f) in enumerate(S):
            for fr in (0.3, 0.85):
                f(d * fr).convert("RGB").save(f"{out}/{which}{i}_{int(fr*100)}.jpg", quality=85)
    else:
        render(which, S, out, sys.argv[4])
