"""Real-instrument music (FluidR3 GM soundfont) + neural voiceover + ducking mix."""
import os, subprocess, random, wave, numpy as np, mido
SR = 44100
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
HERE = os.path.dirname(os.path.abspath(__file__))

STYLES = {
    # key root midi, bpm, lead program, chord program, bass program, progression (scale degrees as semitone triads)
    "bright": dict(root=60, bpm=104, keys=0, lead=11, bass=33, pad=48),     # piano + vibraphone
    "funky":  dict(root=62, bpm=110, keys=4, lead=12, bass=36, pad=89),     # e-piano + marimba, slap bass
    "chill":  dict(root=57, bpm=92,  keys=4, lead=46, bass=33, pad=89),     # e-piano + harp
}
PROG = [[0, 4, 7], [7, 11, 14], [9, 12, 16], [5, 9, 12]]  # I V vi IV

def compose(path_mid, dur, style, seed):
    st = STYLES[style]; rng = random.Random(seed)
    mid = mido.MidiFile(ticks_per_beat=480); tpb = 480
    beats = int(dur * st["bpm"] / 60) + 4
    def track(ch, prog):
        t = mido.MidiTrack(); mid.tracks.append(t)
        t.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(st["bpm"]), time=0))
        if ch != 9: t.append(mido.Message("program_change", channel=ch, program=prog, time=0))
        return t
    def write(t, events):  # events: (beat, dur_beats, note, vel, ch)
        msgs = []
        for b, d, n, v, ch in events:
            msgs.append((int(b * tpb), 1, mido.Message("note_on", channel=ch, note=n, velocity=v)))
            msgs.append((int((b + d) * tpb), 0, mido.Message("note_off", channel=ch, note=n, velocity=0)))
        msgs.sort(key=lambda x: (x[0], x[1])); last = 0
        for tick, _, m in msgs: m.time = tick - last; last = tick; t.append(m)
    R = st["root"]
    keys, lead, bass, pad, drum = [], [], [], [], []
    for bar in range(beats // 4 + 1):
        ch_ = PROG[bar % 4]; b0 = bar * 4
        # keys: syncopated chord stabs
        for off in (0, 1.5, 2.5, 3.5 if bar % 2 else 3):
            for n in ch_: keys.append((b0 + off, 0.45, R + n, 70 + rng.randint(-6, 6), 0))
        # pad sustained
        for n in ch_: pad.append((b0, 3.95, R - 12 + n, 38, 2))
        # bass
        for k, off in enumerate([0, 0.75, 1.5, 2, 2.75, 3.5]):
            n = R - 24 + ch_[0] + (12 if k == 4 else 0)
            bass.append((b0 + off, 0.4, n, 88, 1))
        # lead melody: pentatonic motif
        penta = [0, 2, 4, 7, 9, 12, 14]
        if bar >= 1:
            for k in range(4):
                if rng.random() < 0.75:
                    off = k + (0.5 if rng.random() < 0.4 else 0)
                    n = R + 12 + rng.choice([x for x in penta if (x - ch_[0]) % 12 in (0, 4, 7, 2, 9)] or penta)
                    lead.append((b0 + off, 0.4, n, 62, 3))
        # drums
        if bar >= 1:
            for off in (0, 2.5): drum.append((b0 + off, 0.2, 36, 100, 9))
            for off in (1, 3): drum.append((b0 + off, 0.2, 38, 86, 9))
            for k in range(8): drum.append((b0 + k * 0.5, 0.1, 42, 52 + (14 if k % 2 == 0 else 0), 9))
            if bar % 4 == 3: drum += [(b0 + 3.5, 0.1, 38, 70, 9), (b0 + 3.75, 0.1, 38, 80, 9)]
        else:
            drum.append((b0, 0.2, 36, 90, 9))
    write(track(0, st["keys"]), keys); write(track(1, st["bass"]), bass)
    write(track(2, st["pad"]), pad); write(track(3, st["lead"]), lead); write(track(9, 0), drum)
    mid.save(path_mid)

def render_music(out_wav, dur, style, seed):
    m = out_wav[:-4] + ".mid"; compose(m, dur, style, seed)
    subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-r", str(SR), "-F", out_wav, SF2, m], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def load(path):
    tmp = path + ".44k.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-ar", str(SR), "-ac", "1", tmp], check=True)
    with wave.open(tmp) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    os.remove(tmp); return a

def voice_tr(text, out, voice="fahrettin-medium", length_scale=0.92):
    m = f"{HERE}/models/vits-piper-tr_TR-{voice}/tr_TR-{voice}.onnx"
    subprocess.run(["python3", "-m", "piper", "-m", m, "-f", out, "--length-scale", str(length_scale), "--sentence-silence", "0.15"],
                   input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

_k = None
def voice_en(text, out, voice="af_heart", speed=1.05):
    global _k
    import soundfile as sf
    from kokoro_onnx import Kokoro
    if _k is None: _k = Kokoro(f"{HERE}/models/kokoro.onnx", f"{HERE}/models/voices.bin")
    s, sr = _k.create(text, voice=voice, speed=speed, lang="en-us"); sf.write(out, s, sr)

def mix(out_wav, total, music_wav, voices, fx):
    """voices: list of (start_sec, mono array). fx: list of (start, kind)."""
    n = int(total * SR)
    mus = load(music_wav); mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
    vo = np.zeros(n)
    for st, a in voices:
        s = int(st * SR); e = min(n, s + len(a)); vo[s:e] += a[: e - s]
    # ducking envelope
    env = np.abs(vo); win = int(0.08 * SR)
    env = np.convolve(env, np.ones(win) / win, "same"); act = (env > 0.01).astype(float)
    sm = int(0.25 * SR); act = np.convolve(act, np.ones(sm) / sm, "same")
    gain = 0.85 - 0.62 * np.clip(act * 1.5, 0, 1)
    mus = mus / (np.abs(mus).max() + 1e-6)
    rng = np.random.default_rng(3)
    fxs = np.zeros(n)
    for st, kind in fx:
        s = int(st * SR)
        if kind == "whoosh":
            L = int(0.4 * SR)
            if s + L > n or s < 0: continue
            noise = np.convolve(rng.standard_normal(L), np.ones(10) / 10, "same")
            fxs[s:s + L] += 0.18 * np.sin(np.pi * np.arange(L) / L) ** 2 * noise
        elif kind == "pop":
            L = int(0.1 * SR); t = np.arange(L) / SR
            if s + L <= n: fxs[s:s + L] += 0.35 * np.exp(-t * 45) * np.sin(2 * np.pi * (1100 - 3000 * t) * t)
    vo = vo / (np.abs(vo).max() + 1e-6) * 0.95
    out = 0.32 * mus * gain + vo + fxs
    t = np.arange(n) / SR; out *= np.minimum(1, (total - t) / 1.0)
    out = out / (np.abs(out).max() + 1e-6) * 0.89
    d = (np.stack([out, out], 1) * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
