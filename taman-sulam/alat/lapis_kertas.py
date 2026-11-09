"""Pintu panel bergelombang, motif sulam silang, pita sulam, garis bunga peoni, ornamen bintang sage."""
import base64
from _lukis import *

PINK = '#C9558F'; PINK2 = '#DD83AF'; SAGE = '#7F9A78'; SAGE2 = '#A9BDA0'


# ------------------------------------------------------------- motif sulam (cross-stitch)
def grid_motif(kind):
    n = 13; c = 6; g = set()
    def add(dx, dy):
        for sx in (1, -1):
            for sy in (1, -1):
                g.add((c + dx * sx, c + dy * sy)); g.add((c + dy * sx, c + dx * sy))
    if kind == 0:     # kembang delapan
        for k in range(0, 7):
            if k != 4: add(k, 0)
        for k in range(1, 5): add(k, k) if k != 2 else None
        for p in ((2, 3), (3, 2), (1, 4), (4, 1)): add(*p)
    elif kind == 1:   # bintang kecil
        for k in range(0, 5): add(k, 0)
        for k in range(1, 4): add(k, k)
        add(1, 2); add(2, 1)
    elif kind == 2:   # rosette berlubang
        for k in (1, 2, 3, 4, 5): add(k, 0)
        for p in ((1, 1), (2, 2), (3, 3), (4, 4), (2, 4), (4, 2), (1, 3), (3, 1)): add(*p)
        g.discard((c, c))
    else:             # silang kecil
        for k in range(0, 3): add(k, 0)
        add(1, 1)
    return g, n


def sulam_svg(kind, px=6, col=PINK, op=1.0, x0=0, y0=0, scale=1.0):
    g, n = grid_motif(kind)
    o = f'<g transform="translate({x0} {y0}) scale({scale})" opacity="{op}">'
    for (i, j) in sorted(g):
        o += f'<rect x="{i*px}" y="{j*px}" width="{px-.6}" height="{px-.6}" fill="{col}"/>'
    return o + '</g>', n * px


def pita_sulam_body(w=240, rows=12, px=6, col=PINK):
    """Pita songket: segitiga & belah ketupat tersusun, tile horizontal (w kelipatan 2*px*7)."""
    b = ''
    per = 14  # sel per motif
    for t in range(w // (per * px) + 1):
        ox = t * per * px
        for r in range(7):                     # segitiga menghadap bawah
            for i in range(r, per - r):
                b += f'<rect x="{ox+i*px}" y="{r*px}" width="{px-.6}" height="{px-.6}" fill="{col}"/>'
        for i in (0, per - 1, 6, 7):
            pass
        for r in range(6):                     # belah ketupat kecil di bawah
            y = (8 + r) * px
            half = r if r < 3 else 5 - r
            for i in range(7 - half - 1, 7 + half + 1):
                b += f'<rect x="{ox+i*px}" y="{y}" width="{px-.6}" height="{px-.6}" fill="{PINK2}" opacity=".85"/>'
    return b


# ------------------------------------------------------------- garis bunga (line art)
def kelopak_garis(cx, cy, r, rnd, rot=0):
    o = ''
    for k in range(4):
        n = (5, 5, 4, 3)[k]
        pr = r * (.52 - k * .1); dist = r * (.66 - k * .17)
        for i in range(n):
            a = rot + i / n * 6.283 + k * .6
            x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist
            pts = []
            for j in range(0, 25):
                t = j / 24 * 6.283
                rr = pr * (1 + .12 * math.sin(t * 5 + i) + rnd.uniform(-.03, .03))
                pts.append((x + math.cos(t) * rr, y + math.sin(t) * rr * .92))
            o += '<path d="M' + ' L'.join(f'{r1(px)} {r1(py)}' for px, py in pts) + 'Z" fill="none"/>'
    o += f'<path d="{spiral(cx, cy, 1, r*.16, 2.5, 0, n=30)}" fill="none"/>'
    return o


def spiral(cx, cy, r0, r1_, turns, a0=0, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n; a = a0 + turns * 6.283 * t; r = r0 + (r1_ - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return 'M' + ' L'.join(f'{r1(x)} {r1(y)}' for x, y in pts)


def daun_garis(x, y, ang, L, W):
    ca, sa = math.cos(ang), math.sin(ang); nx, ny = -sa, ca
    ex, ey = x + ca * L, y + sa * L
    o = (f'<path d="M{r1(x)} {r1(y)} C{r1(x+ca*L*.3+nx*W)} {r1(y+sa*L*.3+ny*W)} {r1(x+ca*L*.75+nx*W*.5)} {r1(y+sa*L*.75+ny*W*.5)} {r1(ex)} {r1(ey)} '
         f'C{r1(x+ca*L*.75-nx*W*.5)} {r1(y+sa*L*.75-ny*W*.5)} {r1(x+ca*L*.3-nx*W)} {r1(y+sa*L*.3-ny*W)} {r1(x)} {r1(y)}Z" fill="none"/>')
    o += f'<path d="M{r1(x)} {r1(y)} L{r1(x+ca*L*.92)} {r1(y+sa*L*.92)}" fill="none"/>'
    for t in (.3, .5, .7):
        px, py = x + ca * L * t, y + sa * L * t
        for sg in (1, -1):
            o += f'<path d="M{r1(px)} {r1(py)} L{r1(px+ca*L*.12+sg*nx*W*.5)} {r1(py+sa*L*.12+sg*ny*W*.5)}" fill="none"/>'
    return o


def garis_bunga(seed=3, w=430, h=900, sisi='kiri'):
    rnd = random.Random(seed)
    body = ''
    # batang melengkung dari bawah
    for k in range(2):
        P4 = ((-10 + k * 20, h + 10), (60 + k * 30, h * .7), (30 + k * 50, h * .4), (110 + k * 40, h * (.12 + k * .1)))
        body += f'<path d="M{P4[0][0]} {P4[0][1]} C{P4[1][0]} {P4[1][1]} {P4[2][0]} {P4[2][1]} {P4[3][0]} {P4[3][1]}" fill="none"/>'
        for i in range(8):
            t = .1 + i * .11; x, y, tx, ty = bez(*P4, t)
            for sg in (1, -1):
                body += daun_garis(x, y, math.atan2(ty, tx) + sg * rnd.uniform(.7, 1.2), rnd.uniform(60, 120), rnd.uniform(14, 24))
    for (cx, cy, r) in ((100, h * .14, 58), (60, h * .62, 62), (150, h * .86, 46)):
        body += kelopak_garis(cx, cy, r, rnd, rnd.uniform(0, 6))
    for (cx, cy) in ((200, h * .2), (40, h * .38), (190, h * .78), (100, h * .7)):
        for i in range(5):
            a = i / 5 * 6.283 + rnd.uniform(0, 1); body += f'<ellipse cx="{r1(cx+math.cos(a)*7)}" cy="{r1(cy+math.sin(a)*7)}" rx="6" ry="3.5" transform="rotate({math.degrees(a):.0f} {r1(cx+math.cos(a)*7)} {r1(cy+math.sin(a)*7)})" fill="none"/>'
    g = f'<g stroke="{PINK}" stroke-width="1.0" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity=".78">{body}</g>'
    if sisi == 'kanan':
        g = f'<g transform="translate({w} 0) scale(-1 1)">{g}</g>'
    return g


def bintang_sage(cx, cy, r, col=SAGE):
    o = f'<g transform="translate({cx} {cy})" fill="{col}" stroke="none">'
    for i in range(8):
        L = r if i % 2 == 0 else r * .66
        o += f'<path transform="rotate({i*45})" d="M0 0 C{-r*.12:.1f} {-L*.4:.1f} {-r*.1:.1f} {-L*.8:.1f} 0 {-L:.1f} C{r*.1:.1f} {-L*.8:.1f} {r*.12:.1f} {-L*.4:.1f} 0 0Z"/>'
    o += f'<circle r="{r*.17:.1f}" fill="{SAGE2}"/>'
    for sg in (1, -1):
        o += f'<path d="M{sg*r*.9:.1f} 0 q{sg*r*.9:.1f} {-r*.25:.1f} {sg*r*1.5:.1f} {r*.1:.1f}" stroke="{col}" stroke-width="1.4" fill="none"/>'
    return o + '</g>'


# ------------------------------------------------------------- pintu
def lobus_path(x_base, x_peak, h, n=6, kiri=True):
    """Tepi dalam bergelombang: mulai (x_base,0) ... turun ke (x_base,h)."""
    d = f'M{x_base} 0'
    step = h / n
    for k in range(n):
        y0, y1 = k * step, (k + 1) * step; ym = (y0 + y1) / 2
        d += f' C{x_base} {y0+step*.55:.1f} {x_peak} {ym-step*.45:.1f} {x_peak} {ym:.1f} C{x_peak} {ym+step*.45:.1f} {x_base} {y1-step*.55:.1f} {x_base} {y1:.1f}'
    return d


def pintu(sisi='kiri', seed=1):
    W, Ht = 430, 1500
    rnd = random.Random(seed)
    tile = open(os.path.join(DIR_LAYER, 'kertas.webp'), 'rb').read()
    uri = 'data:image/webp;base64,' + base64.b64encode(tile).decode()
    defs = f'<pattern id="kt" width="512" height="512" patternUnits="userSpaceOnUse"><image href="{uri}" width="512" height="512"/></pattern>'
    edge = lobus_path(394, 430, Ht, 6)
    panel = f'M0 0 L394 0 {edge[len("M394 0"):]} L0 {Ht} Z'
    inset1 = lobus_path(380, 414, Ht - 40, 6).replace('M380 0', 'M380 20')
    b = f'<path d="{panel}" fill="url(#kt)"/>'
    b += f'<clipPath id="pc"><path d="{panel}"/></clipPath><g clip-path="url(#pc)">'
    # sulam tersebar
    spots = [(70, 150, 0, 1.3), (230, 330, 0, 1.6), (90, 520, 2, 1.0), (260, 660, 0, 1.9), (110, 870, 1, 1.2), (250, 980, 2, 1.1), (80, 1160, 0, 1.5), (250, 1300, 1, 1.2), (160, 60, 3, 1.1), (320, 560, 3, 1.0), (40, 780, 3, 1.0), (300, 1130, 3, 1.1), (190, 1430, 3, 1.1), (330, 200, 1, .9)]
    for (x, y, k, s) in spots:
        m, sz = sulam_svg(k, 6, PINK if k != 3 else PINK2, .92, x, y, s)
        b += m
    # tanda zig-zag sage
    for (x, y) in ((50, 400), (300, 460), (40, 1000), (330, 900), (120, 1250), (280, 220)):
        b += f'<path d="M{x} {y} l6 -8 l-12 -8 l12 -8" stroke="{SAGE}" stroke-width="2" fill="none" opacity=".85"/><path d="M{x+9} {y} l6 -8 l-12 -8 l12 -8" stroke="{SAGE}" stroke-width="2" fill="none" opacity=".7"/>'
    # garis bunga di tepi luar
    b += f'<g transform="translate(-40 40)">{garis_bunga(seed + 3, 430, 700)}</g>'
    b += f'<g transform="translate(-30 760) scale(1 1)">{garis_bunga(seed + 8, 430, 720)}</g>'
    b += '</g>'
    # garis tepi sage ganda mengikuti lobus
    e2 = lobus_path(378, 413, Ht - 40, 6); e2 = 'M378 20' + e2[len('M378 0'):]
    e2 = e2.replace(f'{Ht}', f'{Ht-20}')
    b += f'<path d="{lobus_path(380, 414, Ht, 6)}" stroke="{SAGE}" stroke-width="3" fill="none" opacity=".9"/>'
    b += f'<path d="{lobus_path(366, 399, Ht, 6)}" stroke="{SAGE}" stroke-width="1.4" fill="none" opacity=".8"/>'
    # bintang di lekuk
    step = Ht / 6
    for k in range(7):
        b += bintang_sage(380, k * step, 20)
    if sisi == 'kanan':
        b = f'<g transform="translate({W} 0) scale(-1 1)">{b}</g>'
    return b, defs


def main(R):
    for n, k in enumerate((0, 1, 2, 3)):
        m, sz = sulam_svg(k, 8, PINK)
        simpan_svg(f'sulam-{n+1}', sz, sz, m)
    # pita sulam (tile horizontal 252 = 3 motif x 84)
    simpan_svg('pita-sulam', 252, 12 * 6 + 6, pita_sulam_body(252, 12, 6))
    simpan_svg('garis-bunga-kiri', 430, 900, garis_bunga(3, 430, 900, 'kiri'))
    simpan_svg('garis-bunga-kanan', 430, 900, garis_bunga(5, 430, 900, 'kanan'))
    simpan_svg('bintang-sage', 120, 60, bintang_sage(60, 30, 22))
    pb = ''
    for sg in (1, -1):
        for i in range(7):
            pb += f'<rect x="{240+sg*(46+i*14)-3}" y="27" width="6" height="6" fill="{PINK if i%2==0 else PINK2}" opacity="{1-i*.11:.2f}"/>'
        pb += f'<path d="M{240+sg*160} 30 H{240+sg*232}" stroke="{PINK2}" stroke-width="1" opacity=".6"/>'
    simpan_svg('pembatas-sulam', 480, 60, pb + bintang_sage(240, 30, 20))
    b, d = pintu('kiri', 1);  simpan_layer(R, 'pintu-kiri', 0, 0, 430, 1500, b, d, seed=31, grain=.025, pig=.015, edge=.5, q=84)
    b, d = pintu('kanan', 2); simpan_layer(R, 'pintu-kanan', 0, 0, 430, 1500, b, d, seed=32, grain=.025, pig=.015, edge=.5, q=84)
