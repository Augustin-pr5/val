"""words_final.json → words.json + assets/lib/words.js + rapport d'écart avec timeline.json"""
import json, sys
S, P = sys.argv[1], sys.argv[2]
tl = json.load(open(P+'/timeline.json', encoding='utf-8'))
fin = {(sc['id'], i): v['fin'] for sc in tl['scenes'] for i, v in enumerate(sc.get('voix', []))}
deb = {(sc['id'], i): v['debut'] for sc in tl['scenes'] for i, v in enumerate(sc.get('voix', []))}
W = json.load(open(S+'/words_final.json', encoding='utf-8')); out = []
for i, w in enumerate(W):
    nxt = W[i+1] if i+1 < len(W) else None
    if not nxt or nxt['scene'] != w['scene'] or nxt['phrase'] != w['phrase']:
        w['end'] = round(max(w['start'] + 0.2, min(w['end'], fin[(w['scene'], w['phrase'])] + 0.15)), 2)
    out.append({'id': f'w{i}', 'text': w['text'], 'start': w['start'], 'end': w['end'], 'scene': w['scene'], 'phrase': w['phrase']})
json.dump(out, open(P+'/words.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(P+'/assets/lib/words.js', 'w', encoding='utf-8').write('/* Généré depuis words.json (alignement forcé mot à mot de la bande-son). Ne pas éditer à la main. */\nwindow.WORDS = ' + json.dumps([[x['text'], x['start'], x['end'], x['scene'], x['phrase']] for x in out], ensure_ascii=False) + ';\n')
rep = []; g = {}
for w in out: g.setdefault((w['scene'], w['phrase']), []).append(w)
for k, ws in g.items():
    d = ws[0]['start'] - deb[k]; rep.append(f"{k[0]}#{k[1]} début {ws[0]['start']:.2f} (timeline {deb[k]:.2f}, Δ{d:+.2f}){'  ⚠ >0,2 s' if abs(d) > 0.2 else ''}  « {' '.join(x['text'] for x in ws)} »")
open(P+'/.work/words_ecarts_timeline.txt', 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
print(len(out), 'mots ;', sum('⚠' in r for r in rep), 'phrases à plus de 0,2 s de timeline.json')
