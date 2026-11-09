"""
Mesin lukis Wedding Code (tema Taman Sulam):
 - palet cat air krem/pink/emas/zaitun
 - helper kurva
 - render SVG -> PNG transparan (Chromium) -> tekstur cat air & kertas (numpy) -> WebP
"""
import math, os, random, io, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DIR_LAYER = os.path.join(ROOT, 'assets', 'layer')
DIR_SVG = os.path.join(ROOT, 'assets', 'svg')
os.makedirs(DIR_LAYER, exist_ok=True); os.makedirs(DIR_SVG, exist_ok=True)

# EDIT TEMA: palet
P = dict(
    krem='#F1E7C6', krem_lt='#F9F3DD', krem_dk='#DDCD9A', kertas='#EFE4BF',
    emas='#B8923A', emas_lt='#E9D58F', emas_dk='#80601C',
    magenta='#C23E84', pink='#DD7FAE', pink_lt='#F2C7DB', pink_dk='#962F66', ungu='#8E4A93',
    sage='#8FA27E', sage_dk='#5F7A5C', zaitun='#7A7B3E', zaitun_lt='#A9A862', zaitun_dk='#4F5528',
    daun='#3D6B49', daun_dk='#264A35', daun_lt='#6E9A6F', mint='#A9C3B0',
    batu='#EDE4C8', batu_dk='#CDBF92', air='#EEF3EC', batang='#6B5238', jingga='#E59A55',
)


def r1(x): return f'{x:.1f}'


def svg_doc(x, y, w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def lin(id, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in [(t + (1,))[:3] if len(t) == 2 else t for t in stops])
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in [(t + (1,))[:3] if len(t) == 2 else t for t in stops])
    f = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>'


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    n = math.hypot(dx, dy) or 1
    return x, y, dx/n, dy/n


def lerp(a, b, t): return a + (b - a) * t


def mix(c1, c2, t):
    a = [int(c1[i:i+2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(int(lerp(a[i], b[i], t)) for i in range(3))


def leaf(x, y, ang, L, W):
    ca, sa = math.cos(ang), math.sin(ang); nx, ny = -sa, ca
    ex, ey = x + ca*L, y + sa*L
    c1 = (x + ca*L*.3 + nx*W, y + sa*L*.3 + ny*W); c2 = (x + ca*L*.75 + nx*W*.5, y + sa*L*.75 + ny*W*.5)
    d1 = (x + ca*L*.3 - nx*W, y + sa*L*.3 - ny*W); d2 = (x + ca*L*.75 - nx*W*.5, y + sa*L*.75 - ny*W*.5)
    return (f'M{r1(x)} {r1(y)} C{r1(c1[0])} {r1(c1[1])} {r1(c2[0])} {r1(c2[1])} {r1(ex)} {r1(ey)} '
            f'C{r1(d2[0])} {r1(d2[1])} {r1(d1[0])} {r1(d1[1])} {r1(x)} {r1(y)}Z')


def blob(cx, cy, r, rnd, n=9, jit=.25):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        rr = r * (1 + rnd.uniform(-jit, jit))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d = f'M{r1((pts[0][0]+pts[-1][0])/2)} {r1((pts[0][1]+pts[-1][1])/2)}'
    for i in range(n):
        p = pts[i]; q = pts[(i + 1) % n]
        d += f' Q{r1(p[0])} {r1(p[1])} {r1((p[0]+q[0])/2)} {r1((p[1]+q[1])/2)}'
    return d + 'Z'


# ----------------------------- tekstur cat air -----------------------------
def tekstur(im, seed=1, grain=.05, pig=.10, edge=1.0, soft=.7, warm=0.0):
    a = np.asarray(im.convert('RGBA')).astype(np.float32) / 255
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed)
    al = a[..., 3]; pm = a[..., :3] * al[..., None]
    if edge > 0:
        dx = gaussian_filter(rng.standard_normal((h, w)), 5) * 5 * edge
        dy = gaussian_filter(rng.standard_normal((h, w)), 5) * 5 * edge
        yy, xx = np.mgrid[0:h, 0:w]
        co = [yy + dy, xx + dx]
        pm = np.stack([map_coordinates(pm[..., c], co, order=1, mode='nearest') for c in range(3)], -1)
        al = map_coordinates(al, co, order=1, mode='constant')
    if soft:
        al = gaussian_filter(al, soft); pm = np.stack([gaussian_filter(pm[..., c], soft * .6) for c in range(3)], -1)
    rgb = pm / np.maximum(al[..., None], 1e-4)
    nf = gaussian_filter(rng.standard_normal((h, w)), .8); nf /= nf.std() + 1e-6
    npg = gaussian_filter(rng.standard_normal((h, w)), 14); npg /= npg.std() + 1e-6
    npg2 = gaussian_filter(rng.standard_normal((h, w)), 40); npg2 /= npg2.std() + 1e-6
    k = 1 + grain * nf[..., None] + pig * .5 * npg[..., None] + pig * .5 * npg2[..., None]
    rgb = np.clip(rgb * k, 0, 1)
    if warm:
        rgb[..., 0] = np.clip(rgb[..., 0] * (1 + warm), 0, 1); rgb[..., 2] = np.clip(rgb[..., 2] * (1 - warm), 0, 1)
    out = np.dstack([rgb, np.clip(al, 0, 1)])
    return Image.fromarray((out * 255).astype(np.uint8), 'RGBA')


# ----------------------------- render -----------------------------
class Perender:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()
        self.br = self.pw.chromium.launch()

    def png(self, svg, w, h, scale=1.0, transparan=True):
        pg = self.br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
        pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
        pg.wait_for_timeout(120)
        data = pg.screenshot(omit_background=transparan, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        pg.close()
        return Image.open(io.BytesIO(data)).convert('RGBA')

    def tutup(self):
        self.br.close(); self.pw.stop()


MANIFEST = {}


def simpan_layer(R, nama, x, y, w, h, body, defs='', seed=1, q=82, **tk):
    """Render area (x,y,w,h) dari koordinat dunia -> tekstur -> WebP. Catat posisi di manifest."""
    im = R.png(svg_doc(x, y, w, h, body, defs), w, h)
    im = tekstur(im, seed=seed, **tk)
    path = os.path.join(DIR_LAYER, nama + '.webp')
    im.save(path, 'WEBP', quality=q, method=6)
    MANIFEST[nama] = dict(x=x, y=y, w=w, h=h, kb=os.path.getsize(path) // 1024)
    print('layer', nama, w, h, MANIFEST[nama]['kb'], 'KB')
    return im


def simpan_svg(nama, w, h, body, defs=''):
    s = svg_doc(0, 0, w, h, body, defs)
    with open(os.path.join(DIR_SVG, nama + '.svg'), 'w') as f: f.write(s)
    print('svg', nama, len(s) // 1024, 'KB')
