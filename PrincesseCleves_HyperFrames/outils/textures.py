import numpy as np, sys
from PIL import Image, ImageFilter
out = sys.argv[1]
W, H = 1920, 1080
rng = np.random.default_rng(1678)
def lowfreq(scale, octaves=4):
    acc = np.zeros((H, W)); amp = 1; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        small = rng.standard_normal((H // s + 2, W // s + 2))
        im = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-9) * 255).astype(np.uint8)).resize((W + 2 * s, H + 2 * s), Image.BICUBIC)
        a = np.asarray(im, dtype=np.float64)[s:s + H, s:s + W] / 255 - 0.5
        acc += a * amp; tot += amp; amp *= 0.5
    return acc / tot
def fibres(n, length, alpha):
    im = Image.new('L', (W, H), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H); ang = rng.uniform(0, np.pi); L = rng.uniform(*length)
        pts = []
        for k in range(6):
            pts.append((x, y)); ang += rng.normal(0, 0.35); x += np.cos(ang) * L / 5; y += np.sin(ang) * L / 5
        d.line(pts, fill=int(rng.uniform(80, 255)), width=1)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float64) / 255 * alpha
def save(base_rgb, blot_amp, grain_amp, fib, edge, name, edge_col=None):
    base = np.array(base_rgb, dtype=np.float64)[None, None, :] / 255
    lum = 1 + lowfreq(260) * blot_amp + rng.standard_normal((H, W)) * grain_amp - fib
    img = base * lum[..., None]
    if edge:
        yy, xx = np.mgrid[0:H, 0:W]; u = np.abs(2 * xx / (W - 1) - 1); v = np.abs(2 * yy / (H - 1) - 1)
        d = (u ** 5 + v ** 5) ** (1 / 5) + lowfreq(180) * 0.22
        e = np.clip((d - (1 - edge)) / (edge + 0.12), 0, 1) ** 1.8
        ec = np.array(edge_col, dtype=np.float64)[None, None, :] / 255
        img = img * (1 - e[..., None] * 0.5) + ec * e[..., None] * 0.5
    Image.fromarray((np.clip(img, 0, 1) * 255).round().astype(np.uint8)).save(out + '/' + name, quality=94)
# papier ivoire #F5F1E8 : grain très léger, fixe
save((0xF5, 0xF1, 0xE8), 0.018, 0.012, fibres(260, (20, 70), 0.035), 0, 'papier_ivoire.jpg')
# parchemin (S07) : plus chaud et taché, bords brunis
save((0xEC, 0xE1, 0xC8), 0.07, 0.016, fibres(500, (20, 90), 0.05), 0.16, 'parchemin.jpg', edge_col=(0x8A, 0x72, 0x4E))
print('ok')
