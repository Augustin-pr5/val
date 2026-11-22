import json, subprocess, os, re, sys, unicodedata, difflib, statistics
P = sys.argv[1]; W = sys.argv[2]
BIN = os.path.expanduser('~/.cache/hyperframes/whisper/whisper.cpp/build/bin/whisper-cli')
MODEL = os.path.expanduser('~/.cache/hyperframes/whisper/models/ggml-medium.bin')
AUDIO = os.path.join(P, 'assets/audio/bande_son_finale_212s.m4a')
tl = json.load(open(os.path.join(P, 'timeline.json'), encoding='utf-8'))
def norm(s):
    s = unicodedata.normalize('NFD', s.lower().replace('œ', 'oe')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9]", '', s)
PAD = 0.8
rows = []
for sc in tl['scenes']:
    for pi, v in enumerate(sc.get('voix', [])):
        text = v['texte'].replace('«', '').replace('»', '').strip(); toks = text.split()
        t0 = max(0, v['debut'] - PAD); t1 = min(212, v['fin'] + PAD)
        wav = os.path.join(W, f"{sc['id']}_{pi}.wav"); base = wav[:-4] + '_dtw'
        if not os.path.exists(wav):
            subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t0:.3f}','-to',f'{t1:.3f}','-i',AUDIO,'-ar','16000','-ac','1',wav], check=True)
        if not os.path.exists(base + '.json'):
            subprocess.run([BIN,'-m',MODEL,'-l','fr','-f',wav,'-ojf','-of',base,'-dtw','medium','-nfa','-t','4','-np','--prompt',text], check=True, capture_output=True)
        j = json.load(open(base + '.json', encoding='utf-8', errors='replace'))
        # reconstruire les mots à partir des tokens (un token qui commence par une espace = nouveau mot)
        words = []
        for seg in j['transcription']:
            for t in seg['tokens']:
                if t['text'].startswith('[_') : continue
                tt = t['text']; td = t.get('t_dtw', -1) / 100 if t.get('t_dtw', -1) >= 0 else None
                if tt.startswith(' ') or not words:
                    words.append({'text': tt.strip(), 'td': [td], 'off': t['offsets']['from'] / 1000})
                else:
                    words[-1]['text'] += tt; words[-1]['td'].append(td)
        rec = [w for w in words if norm(w['text'])]
        A = [norm(t) for t in toks]; B = [norm(r['text']) for r in rec]
        sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
        m = [None] * len(toks)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size): m[blk.a + k] = rec[blk.b + k]
        rows.append({'scene': sc['id'], 'phrase': pi, 'debut': v['debut'], 'fin': v['fin'], 't0': t0, 'toks': toks,
                     'dtw': [ (t0 + x['td'][0]) if (x and x['td'][0] is not None) else None for x in m],
                     'dtw_last': [ (t0 + x['td'][-1]) if (x and x['td'][-1] is not None) else None for x in m],
                     'heard': ' '.join(r['text'] for r in rec)})
json.dump(rows, open(os.path.join(W, 'dtw_rows.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
d = [r['dtw'][0] - r['debut'] for r in rows if r['dtw'][0] is not None]
print('first-word dtw - timeline debut: median %.3f  mean %.3f  stdev %.3f' % (statistics.median(d), statistics.mean(d), statistics.pstdev(d)))
for r in rows:
    f = r['dtw'][0]
    print(f"{r['scene']}#{r['phrase']} debut {r['debut']:.2f} dtw1 {f if f is None else round(f,2)}  Δ {None if f is None else round(f-r['debut'],2)}  matched {sum(x is not None for x in r['dtw'])}/{len(r['toks'])} | {r['heard'][:90]}")
