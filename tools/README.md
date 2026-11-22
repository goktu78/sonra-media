# Ses hattı

- `setup.sh`: FluidR3 GM soundfont (gerçek kayıtlı enstrüman örnekleri), Piper Türkçe sinirsel ses (tr_TR-fahrettin-medium), Kokoro İngilizce ses (af_heart) kurar. Modeller GitHub release'lerinden iner.
- `audio2.py`: `render_music(out, süre, stil, seed)` (stil: bright / funky / chill), `voice_tr(metin, out)`, `voice_en(metin, out)`, `mix(...)` (seslendirme gelince müzik kısılır, geçişlerde whoosh/pop).
- `build2.py`: sahne başına seslendirme metni (NARR) → sahne süresi seslendirmeye göre uzar → video + mix.
- Türkçe seste İngilizce kelimeleri okunuşuyla yaz: "Blek Fraydey", "Ep Stor", "Gugıl Pley", "İnstagram".
