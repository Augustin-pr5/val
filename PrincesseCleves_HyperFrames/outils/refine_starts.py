"""Recule chaque début de mot (alignement CTC MMS) jusqu'au début réel de son attaque.
Énergie large bande (150–8000 Hz, y compris les fricatives) en trames de 5 ms : dans la fenêtre
[max(début−0,15 s ; 55 % de l'écart avec le mot précédent) ; début+0,02 s], on prend le creux d'énergie qui précède la montée la plus nette."""
import numpy as np, json, subprocess, sys
P, IN, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SR = 16000; HOP = 80; WIN = 512; fps = SR / HOP
raw = subprocess.run(['ffmpeg','-v','error','-i',P+'/assets/audio/bande_son_finale_212s.m4a','-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768
fr = np.lib.stride_tricks.sliding_window_view(np.pad(x,(WIN//2,WIN//2)), WIN)[::HOP] * np.hanning(WIN).astype(np.float32)
mag = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(WIN, 1/SR)
E = np.log1p(40 * mag[:, (f >= 150) & (f <= 8000)].sum(1))
E = np.convolve(E, np.ones(3)/3, 'same')
W = json.load(open(IN, encoding='utf-8')); out = []; moves = []
for i, w in enumerate(W):
    s = w['start']
    prevm = W[i-1] if i and W[i-1]['scene'] == w['scene'] and W[i-1]['phrase'] == w['phrase'] else None
    lo = max(s - 0.15, prevm['start'] + 0.55 * (s - prevm['start'])) if prevm else s - 0.15
    a = int(lo * fps); b = int((s + 0.02) * fps)
    seg = E[a:b+1]
    if len(seg) < 5: out.append(w); continue
    d = np.diff(seg)
    k = int(np.argmax(np.convolve(d, np.ones(4), 'same')))   # montée la plus nette
    j = k
    while j > 0 and seg[j-1] < seg[j] - 0.005: j -= 1          # creux qui précède
    ns = (a + j) / fps
    prev = out[-1] if out and out[-1]['scene'] == w['scene'] and out[-1]['phrase'] == w['phrase'] else None
    if prev: ns = max(ns, prev['start'] + 0.06)
    ns = round(min(ns, s), 2)
    moves.append(s - ns)
    if prev: prev['end'] = ns
    out.append(dict(w, start=ns))
for i, w in enumerate(out): w['id'] = f'w{i}'
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
m = np.array(moves); print(f"recul moyen {m.mean()*1000:.0f} ms, médian {np.median(m)*1000:.0f} ms, max {m.max()*1000:.0f} ms")
for sc in ['S02','S04','S08','S10']: print(sc, ' '.join(f"{x['text']}@{x['start']:.2f}" for x in out if x['scene']==sc))
