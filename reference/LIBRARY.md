# sonra. görsel kütüphanesi

Tam liste: `library.json` (path, source, lang, scheme, theme, screen). Kullanım geçmişi: `usage-log.csv`.

| Kaynak | Ne | Not |
|---|---|---|
| `app-live/` | sonra. 1.2.2 gerçek kodundan, web derlemesiyle alınmış ekranlar | 7 içerik teması (genel, yemek, seyahat, alışveriş, öğrenci; EN: genel, travel) × açık/koyu mod, tema başına ~37 ekran |
| `app-screens/` | Göktuğ'un kendi telefonundan gönderdiği ekranlar | gerçek hesap görünümü |
| `marketing/` | Mağaza görselleri, paylaş menüsü akışı, posterler | "Sonra'ya Kaydet" paylaş akışı burada |

Ekran türleri (app-live): ana-sayfa(+asagi), kart-{izle,git,oku,satin-al,dinle,yap}(+-2), kesfet(+asagi), kesfet-{15dk,1saat,disari,sec}, liste(+asagi), liste-filtre-*, arama-*, profil(+asagi), ayarlar(+asagi), ekle, detay-0..3.

ROTASYON KURALI: Her videoda/kaydırmalıda kullanılan her görseli `usage-log.csv`'ye ekle. Son 14 günde kullanılmış bir görseli tekrar kullanma; aynı gün aynı tema+ekran türünü iki videoda kullanma. Konuya uygun temayı seç (yemek videosu → yemek-tr, seyahat → seyahat-tr, Black Friday → alisveris-tr…), açık/koyu modu dönüşümlü kullan, Göktuğ'un ve app-live görsellerini karıştır.
