import json, sys
rows = json.load(open(sys.argv[1], encoding='utf-8')); out_path = sys.argv[2]
words = []; report = []
for r in rows:
    toks, st, last = r['toks'], list(r['dtw']), r['dtw_last']
    n = len(toks)
    # ancre de début de phrase si le 1er mot n'est pas reconnu
    if st[0] is None: st[0] = r['debut']
    # monotonie + interpolation des trous
    for i in range(n):
        if st[i] is not None and i and st[i - 1] is not None and st[i] <= st[i - 1]: st[i] = st[i - 1] + 0.04
    i = 0
    while i < n:
        if st[i] is None:
            j = i
            while j < n and st[j] is None: j += 1
            a = st[i - 1]; b = st[j] if j < n else max(a + 0.25 * (j - i + 1), r['fin'] - 0.2)
            for k in range(i, j): st[k] = a + (b - a) * (k - i + 1) / (j - i + 1)
            i = j
        else: i += 1
    for i in range(n):
        if i + 1 < n: en = st[i + 1]
        else:
            lv = last[i] if last[i] is not None else st[i]
            en = min(max(lv + 0.25, st[i] + 0.2), r['fin'] + 0.25)
        words.append({'text': toks[i], 'start': round(st[i], 2), 'end': round(en, 2), 'scene': r['scene'], 'phrase': r['phrase']})
    d0 = st[0] - r['debut']; d1 = words[-1]['end'] - r['fin']
    report.append(f"{r['scene']}#{r['phrase']}: début Δ{d0:+.2f} s, fin Δ{d1:+.2f} s" + ('  ⚠' if abs(d0) > 0.2 else ''))
json.dump(words, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(report)); print(len(words), 'mots')
