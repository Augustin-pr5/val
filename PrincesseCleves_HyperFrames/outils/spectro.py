import numpy as np, json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
P, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
sr = 16000
raw = subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-to',str(t1),'-i',P+'/assets/audio/bande_son_finale_212s.m4a','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768
hop, win = 80, 512
frames = np.lib.stride_tricks.sliding_window_view(np.pad(x,(win//2,win//2)), win)[::hop] * np.hanning(win)
spec = np.abs(np.fft.rfft(frames, axis=1))[:, :int(5000/sr*win)]
db = 20*np.log10(spec+1e-6); db = np.clip((db - (db.max()-70))/70, 0, 1)
img = (255*(1-db.T[::-1])).astype(np.uint8)
pxs = 160  # pixels par seconde
im = Image.fromarray(img).resize((int((t1-t0)*pxs), 300)).convert('RGB')
# enveloppe d'énergie voix (300-3400 Hz)
band = spec[:, int(300/sr*win):int(3400/sr*win)].sum(1); band = band/band.max()
H = 140; canvas = Image.new('RGB', (im.width, 300+H+60), 'white'); canvas.paste(im, (0,0))
d = ImageDraw.Draw(canvas)
ts = np.arange(len(band))*hop/sr
pts = [(int(t*pxs), 300+H-int(b*H)) for t,b in zip(ts, band)]
d.line(pts, fill=(40,40,40))
w = json.load(open(P+'/words.json', encoding='utf-8'))
font = ImageFont.load_default()
for i,x_ in enumerate([q for q in w if t0 <= q['start'] <= t1]):
    X = int((x_['start']-t0)*pxs); d.line([(X,0),(X,300+H)], fill=(200,30,30)); d.text((X+2, 300+H+5+(i%3)*16), x_['text'], fill=(200,30,30), font=font)
tl = json.load(open(P+'/timeline.json', encoding='utf-8'))
for sc in tl['scenes']:
    for v in sc.get('voix', []):
        for tt,c in ((v['debut'],(30,30,200)),(v['fin'],(30,160,30))):
            if t0<=tt<=t1: X=int((tt-t0)*pxs); d.line([(X,0),(X,20)], fill=c, width=3)
for s in range(int(np.ceil(t0)), int(t1)+1):
    X=int((s-t0)*pxs); d.line([(X,300),(X,310)], fill=(0,0,0)); d.text((X+2,302), str(s), fill=(0,0,0), font=font)
canvas.save(out); print(out, canvas.size)
