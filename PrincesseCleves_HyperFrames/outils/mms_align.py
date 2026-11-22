"""Alignement forcé CTC (modèle MMS de Meta, ONNX) : texte exact de timeline.json → temps de chaque mot.
Pour chaque phrase : extrait audio [début−0,8 s ; fin+0,8 s], émissions CTC (20 ms par trame),
chemin de Viterbi sur la suite de lettres (sans accents). Début d'un mot = 1re trame de sa 1re lettre."""
import json, re, sys, subprocess, unicodedata
import numpy as np, onnxruntime as ort
P, S, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SR = 16000; STRIDE = 0.02
vocab = json.load(open(S + '/mms/vocab.json'))
sess = ort.InferenceSession(S + '/mms/model_quantized.onnx', providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0].name
def romanize(w):
    if re.fullmatch(r'II[.,]?', w): w = 'deux'   # « Henri II » se dit « Henri deux »
    w = w.lower().replace('œ', 'oe').replace('æ', 'ae').replace('’', "'")
    w = unicodedata.normalize('NFD', w); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    w = re.sub(r'\d+', lambda m: {'1558': 'mille cinq cent cinquante huit'}.get(m.group(), m.group()), w)
    return ''.join(c for c in w if c in vocab and c not in "'")
def emissions(t0, t1):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', P + '/assets/audio/bande_son_finale_212s.m4a',
                          '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    x = (x - x.mean()) / (x.std() + 1e-7)
    lg = sess.run(None, {inp: x[None, :]})[0][0]
    lg = lg - lg.max(1, keepdims=True); return lg - np.log(np.exp(lg).sum(1, keepdims=True))
def viterbi(em, toks):
    T, L = em.shape[0], len(toks); ext = [0]
    for t in toks: ext += [t, 0]
    N = len(ext); NEG = -1e18
    dp = np.full((T, N), NEG); bp = np.zeros((T, N), dtype=np.int32)
    dp[0, 0] = em[0, ext[0]]; dp[0, 1] = em[0, ext[1]]
    for t in range(1, T):
        a = dp[t-1]
        b = np.concatenate([[NEG], a[:-1]])
        c = np.concatenate([[NEG, NEG], a[:-2]])
        allow = np.array([s >= 2 and ext[s] != 0 and ext[s] != ext[s-2] for s in range(N)])
        c = np.where(allow, c, NEG)
        st = np.stack([a, b, c]); arg = st.argmax(0)
        dp[t] = st.max(0) + em[t, ext]; bp[t] = arg
    s = N - 1 if dp[-1, N-1] >= dp[-1, N-2] else N - 2
    path = [0] * T
    for t in range(T - 1, -1, -1):
        path[t] = s; s -= bp[t, s]
    first = {}; last = {}
    for t, s in enumerate(path):
        if s % 2 == 1:
            k = s // 2; first.setdefault(k, t); last[k] = t
    return first, last
tl = json.load(open(P + '/timeline.json', encoding='utf-8'))
out = []; rep = []
for sc in tl['scenes']:
    for pi, v in enumerate(sc.get('voix', [])):
        T = []
        for t in v['texte'].replace('«', '').replace('»', '').split():
            if re.fullmatch(r'[:;?!.,]+', t) and T: T[-1] += ' ' + t
            else: T.append(t)
        t0 = max(0.0, v['debut'] - 0.8); t1 = min(212.0, v['fin'] + 0.8)
        em = emissions(t0, t1)
        toks, owner = [], []
        for i, w in enumerate(T):
            for ch in romanize(w): toks.append(vocab[ch]); owner.append(i)
        first, last = viterbi(em, toks)
        st = [None] * len(T); en = [None] * len(T)
        for k, i in enumerate(owner):
            if st[i] is None: st[i] = t0 + first[k] * STRIDE
            en[i] = t0 + (last[k] + 1) * STRIDE
        for i in range(len(T)):
            out.append({'text': T[i], 'start': round(st[i], 2), 'end': round(en[i], 2), 'scene': sc['id'], 'phrase': pi})
        rep.append(f"{sc['id']}#{pi}: {st[0]:.2f} → {en[-1]:.2f}  (timeline {v['debut']:.2f} → {v['fin']:.2f} ; Δdébut {st[0]-v['debut']:+.2f} Δfin {en[-1]-v['fin']:+.2f})" + ('  ⚠' if abs(st[0]-v['debut']) > 0.2 or abs(en[-1]-v['fin']) > 0.2 else ''))
        print(rep[-1], flush=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
