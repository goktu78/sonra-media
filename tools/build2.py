import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from videos import v1, v2, v3
from lib import render_scene, assemble
from audio2 import *

NARR = {
 "1": ("tr", "bright", [
   "Blek Fraydey'e beş gün kaldı. Peki aylardır kaydettiğin ürünler nerede?",
   "İnstagram'da kaydettin. Ekran görüntüsü aldın. Kendine mesaj attın.",
   "Ve hepsi kayboldu.",
   "Sonra, hepsini tek yerde toplar. Linki paylaş, yapay zekâ onu Satın Al listene koysun.",
   "İndirim başladığında listen hazır olsun.",
   "Sonra'yı ücretsiz indir. Ep Stor ve Gugıl Pley'de."]),
 "2": ("tr", "funky", [
   "Galerinde kaç ekran görüntüsü var? İki bin üç yüz kırk yedi mi?",
   "Hangisiydi o kafe? Hani şu bahçeli olan...",
   "Bulamadın. Yine.",
   "Sonra'ya kaydet, yazınca bul. Mekan linkleri kendiliğinden Git listesine düşer.",
   "Sonra bakarım, nihayet işe yarıyor.",
   "Sonra'yı ücretsiz indir. Ep Stor ve Gugıl Pley'de."]),
 "3": ("en", "chill", [
   "You saved three hundred things. You've done zero.",
   "Got fifteen minutes? Let your saves pick for you.",
   "Open Explore, tap What can I do, and choose fifteen minutes. It picks from your own saves. A recipe, a short doc, an article.",
   "Every link is auto sorted by intent. Watch, go, read, buy, listen, do.",
   "Get sonra free, on the App Store and Google Play."]),
}
FN = {"1": v1, "2": v2, "3": v3}
LEAD = 0.15

def build(vid, outdir, final):
    lang, style, lines = NARR[vid]; S = FN[vid]()
    voices, durs = [], []
    for i, txt in enumerate(lines):
        p = f"{outdir}/vo{vid}_{i}.wav"
        (voice_tr if lang == "tr" else voice_en)(txt, p)
        a = load(p); voices.append(a)
        durs.append(max(S[i][0], len(a) / SR + LEAD + 0.45))
    files, starts, t0 = [], [], 0.0
    for i, (d, (_, f, bg)) in enumerate(zip(durs, S)):
        d = round(d * 30) / 30
        p = f"{outdir}/n{vid}_scene{i}.mp4"; render_scene(p, d, f, bg); files.append(p); starts.append(t0); t0 += d
    total = t0
    mus = f"{outdir}/mus{vid}.wav"; render_music(mus, total + 2, style, int(vid) * 7)
    fx = [(s - 0.15, "whoosh") for s in starts[1:]]
    if vid == "3": fx.append((starts[2] + 2.0, "pop"))
    mixp = f"{outdir}/mix{vid}.wav"
    mix(mixp, total, mus, [(s + LEAD, a) for s, a in zip(starts, voices)], fx)
    assemble(files, mixp, final)
    print(vid, "total", round(total, 2), [round(d, 2) for d in durs])

if __name__ == "__main__":
    build(sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3])
