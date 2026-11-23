# Gerçek uygulama ekranları (app-capture)

`reference/app-live/` içindeki ekranlar **sonra. 1.2.2'nin gerçek kodundan** (Expo web derlemesi, headless Chromium, 1179x2556) alındı.
Kayıtlar örnek veridir; küçük resimler bulanık yer tutuculardır (başkalarına ait içerik yok, gerçek kullanıcı verisi yok).

Setler: `tr-light/`, `tr-dark/`, `en-light/` — ana sayfa, kategori kartları (İzle/Git/Satın Al/Yap),
Keşfet, "15 dakikam var" önerisi, Sonra listesi, arama ("kafe"), profil, kayıt detayı.

## Yeniden yakalama (uygulama kaynağı gerekir)
Uygulama kaynak kodu bu herkese açık depoda DEĞİL. Kaynak `goktu78/sonra-app` (özel) deposuna konduğunda:
1. Kaynağı kopyala, `signing/` ve `.env`'i dahil etme.
2. `npm install --ignore-scripts` + `npm install --ignore-scripts react-dom@19.2.3 react-native-web@~0.21.0 @expo/metro-runtime@~57.0.16`
3. `metro.config.js` ve `web-stubs/` klasörünü projeye kopyala (yerel modüller web'de taklit edilir: reklam, satın alma, bildirim, Apple girişi).
4. `app.json`: platforms'a `web` ekle, `web: {bundler:"metro", output:"single"}`, `@bacons/apple-targets` eklentisini çıkar.
5. `CI=1 EXPO_OFFLINE=1 npx expo export --platform web --output-dir dist` ; `python3 -m http.server 8090 -d dist &`
6. Geniş set: `python3 capture2.py OUT light|dark tr|en packs/<tema>.json` (tema başına ~37 ekran; yeni tema = yeni packs/*.json + .queries.json). Tek set: `python3 capture.py OUT_DIR light|dark tr|en`
   Ortam değişkenleri: `SEED=senaryo.json` (kendi örnek kayıtların: [kategori, url, başlık, kaynak, küçük-resim-no]),
   `QUERY=` (arama kelimesi), `DETAIL=` (açılacak kaydın başlığı). Kategori: watch/go/read/buy/listen/do/other.
