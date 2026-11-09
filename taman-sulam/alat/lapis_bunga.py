"""Lapisan depan: dedaunan zaitun (sudut atas), hamparan bunga bawah (raya, peoni, lavender), bunga samping, kupu-kupu."""
from _lukis import *


def daun_hibiscus(x, y, ang, L, rnd, dark=0.0):
    W = L * .36
    c1 = mix(P['daun_lt'], P['daun'], rnd.random()); c1 = mix(c1, P['daun_dk'], dark)
    ca, sa = math.cos(ang), math.sin(ang); nx, ny = -sa, ca
    pts_l, pts_r = [], []
    for i in range(0, 13):
        t = i / 12
        w = W * math.sin(t * math.pi) ** .8 * (1 - .25 * t)
        jag = 1 + (.12 if i % 2 else -.04)
        cx_, cy_ = x + ca * L * t, y + sa * L * t
        pts_l.append((cx_ + nx * w * jag, cy_ + ny * w * jag)); pts_r.append((cx_ - nx * w * jag, cy_ - ny * w * jag))
    pts = pts_l + pts_r[::-1]
    d = 'M' + ' L'.join(f'{r1(a)} {r1(b)}' for a, b in pts) + 'Z'
    o = f'<path d="{d}" fill="{c1}" stroke="{P["daun_dk"]}" stroke-width=".8" stroke-opacity=".6"/>'
    o += f'<path d="M{r1(x)} {r1(y)} L{r1(x+ca*L*.95)} {r1(y+sa*L*.95)}" stroke="{mix(c1, "#E8F2D0", .5)}" stroke-width="1.4" fill="none" opacity=".8"/>'
    for t in (.25, .45, .65):
        px, py = x + ca * L * t, y + sa * L * t
        for sg in (1, -1):
            o += f'<path d="M{r1(px)} {r1(py)} L{r1(px+ca*L*.14+sg*nx*W*.55)} {r1(py+sa*L*.14+sg*ny*W*.55)}" stroke="{mix(c1, "#E8F2D0", .35)}" stroke-width=".8" fill="none" opacity=".6"/>'
    return o


def peoni(cx, cy, r, rnd, rot=0):
    o = ''
    cols = ['#F6C3D8', '#F0A5C5', '#E486B2', '#D56A9E', '#C24F88', '#A83A74']
    for k in range(6):
        n = 8 - k if k < 5 else 4
        pr = r * (.52 - k * .06)
        dist = r * (.62 - k * .11)
        for i in range(n):
            a = rot + i / n * 6.283 + k * .5 + rnd.uniform(-.15, .15)
            x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist
            o += f'<path d="{blob(x, y, pr, rnd, 11, .2)}" fill="{cols[k]}" stroke="{P["pink_dk"]}" stroke-width=".8" stroke-opacity=".45"/>'
            o += f'<path d="{blob(x - pr*.2, y - pr*.25, pr*.5, rnd, 8, .2)}" fill="#FFF4F8" opacity=".2"/>'
            o += f'<path d="M{r1(x)} {r1(y)} q{r1(math.cos(a)*pr*.4)} {r1(math.sin(a)*pr*.4)} {r1(math.cos(a+.6)*pr*.7)} {r1(math.sin(a+.6)*pr*.7)}" stroke="{P["pink_dk"]}" stroke-width=".8" fill="none" opacity=".4"/>'
    o += f'<circle cx="{r1(cx)}" cy="{r1(cy)}" r="{r*.1:.1f}" fill="#F2D27A"/>'
    return o


def raya(cx, cy, r, rot, rnd):
    """Kembang sepatu (hibiscus) magenta."""
    o = f'<g transform="translate({r1(cx)} {r1(cy)}) rotate({rot:.0f}) scale({r/50:.3f})">'
    for i in range(5):
        a = i * 72 + rnd.uniform(-5, 5)
        pts = []
        L = 50
        for j in range(0, 21):
            t = j / 20
            ang = (t - .5) * 1.25
            rr = L * (.8 + .2 * math.cos(ang * 3.2) + (.05 if j % 2 else -.02))
            pts.append((math.sin(ang) * rr * .95, -math.cos(ang) * rr))
        d = 'M0 0 L' + ' L'.join(f'{r1(x)} {r1(y)}' for x, y in pts) + 'Z'
        o += f'<path transform="rotate({a:.0f})" d="{d}" fill="url(#hib)" stroke="#8A2060" stroke-width=".7" stroke-opacity=".5"/>'
        for v in (-.3, 0, .3):
            o += f'<path transform="rotate({a:.0f})" d="M0 0 Q{v*20:.0f} -22 {v*38:.0f} -44" stroke="#7A1E55" stroke-width=".9" fill="none" opacity=".55"/>'
    o += '<circle r="9" fill="#6E1448" opacity=".85"/>'
    o += '<path d="M0 0 Q6 -20 14 -44" stroke="#F6E6C0" stroke-width="3.4" fill="none" stroke-linecap="round"/><path d="M0 0 Q6 -20 14 -44" stroke="#E7C98A" stroke-width="1.2" fill="none"/>'
    for k in range(7):
        a = rnd.uniform(0, 6.28)
        o += f'<circle cx="{14+math.cos(a)*5:.1f}" cy="{-44+math.sin(a)*5:.1f}" r="2.2" fill="#F0B63C"/>'
    o += '<circle cx="14" cy="-45" r="3" fill="#F8D26A"/></g>'
    return o


def lavender(x, y, L, ang, rnd, col='#A97FB6'):
    o = ''
    ex, ey = x + math.cos(ang) * L, y + math.sin(ang) * L
    mx, my = x + math.cos(ang) * L * .5 + rnd.uniform(-14, 14), y + math.sin(ang) * L * .5
    o += f'<path d="M{r1(x)} {r1(y)} Q{r1(mx)} {r1(my)} {r1(ex)} {r1(ey)}" stroke="{P["daun"]}" stroke-width="1.8" fill="none"/>'
    for t in [i / 16 for i in range(5, 17)]:
        px, py, tx, ty = bez((x, y), ((x + mx) / 2, (y + my) / 2), (mx, my), (ex, ey), t)
        for sg in (1, -1):
            o += f'<ellipse cx="{r1(px - ty*sg*3.5)}" cy="{r1(py + tx*sg*3.5)}" rx="3.4" ry="2.4" fill="{mix(col, "#E9D6F0", rnd.random()*.6)}" transform="rotate({math.degrees(math.atan2(ty,tx)):.0f} {r1(px - ty*sg*3.5)} {r1(py + tx*sg*3.5)})" opacity=".92"/>'
    return o


def kupu(x, y, s, rot, c1='#E8903E', c2='#F7C58A'):
    o = f'<g transform="translate({r1(x)} {r1(y)}) rotate({rot:.0f}) scale({s})">'
    for sg in (1, -1):
        o += f'<path d="M0 0 C{sg*18} -20 {sg*40} -14 {sg*30} 4 C{sg*22} 12 {sg*8} 8 0 0Z" fill="{c1}" stroke="#6B3A18" stroke-width=".8"/>'
        o += f'<path d="M0 2 C{sg*14} 8 {sg*28} 20 {sg*18} 26 C{sg*8} 26 {sg*2} 14 0 2Z" fill="{c2}" stroke="#6B3A18" stroke-width=".8"/>'
        o += f'<circle cx="{sg*20}" cy="-4" r="3.4" fill="#FFF3D8" opacity=".85"/>'
    o += '<rect x="-1.4" y="-6" width="2.8" height="20" rx="1.4" fill="#4A2B14"/></g>'
    return o


HIB = lin('hib', [(0, '#6E1448'), (.28, '#B3307C'), (.7, '#DD5E9C'), (1, '#F08DB8')], .5, 1, .5, 0).replace('<linearGradient', '<linearGradient gradientUnits="objectBoundingBox"')


def bunga_bawah():
    rnd = random.Random(41)
    defs = HIB
    X0, Y0, Wd, Ht = 0, 640, 860, 320
    b = ''
    # daun gelap dasar
    for i in range(46):
        x = rnd.uniform(-20, 880); y = rnd.uniform(850, 970)
        b += daun_hibiscus(x, y, -math.pi / 2 + rnd.uniform(-1.1, 1.1), rnd.uniform(70, 150), rnd, dark=rnd.uniform(.1, .5))
    # lavender
    for i in range(22):
        x = rnd.uniform(0, 860); b += lavender(x, 965, rnd.uniform(130, 230), -math.pi / 2 + rnd.uniform(-.5, .5), rnd, ['#A97FB6', '#C28FC4', '#9A6FB0'][i % 3])
    # bunga lapis belakang kecil
    for i in range(18):
        b += peoni(rnd.uniform(0, 860), rnd.uniform(800, 880), rnd.uniform(26, 38), rnd, rnd.uniform(0, 6))
    # peoni & raya besar (depan)
    spots = [(70, 905, 'p', 62), (200, 930, 'r', 58), (320, 905, 'p', 70), (430, 940, 'r', 52), (540, 910, 'p', 66), (660, 935, 'r', 62), (790, 900, 'p', 64), (140, 860, 'r', 46), (600, 855, 'r', 50), (30, 960, 'r', 60), (860, 958, 'r', 58), (260, 975, 'p', 62), (500, 975, 'p', 60), (720, 975, 'p', 58)]
    for (x, y, t, r) in sorted(spots, key=lambda s: s[1]):
        b += (peoni(x, y, r, rnd, rnd.uniform(0, 6)) if t == 'p' else raya(x, y, r, rnd.uniform(-30, 30), rnd))
    # daun depan
    for i in range(14):
        x = rnd.uniform(0, 860); b += daun_hibiscus(x, 975, -math.pi / 2 + rnd.uniform(-1.2, 1.2), rnd.uniform(60, 120), rnd, dark=.3)
    b += kupu(420, 760, .8, -18) + kupu(160, 800, .6, 20, '#F0A8C8', '#FBD8E6') + kupu(700, 790, .65, -30)
    return b, defs


def dedaunan(sisi):
    rnd = random.Random(7 if sisi == 'kiri' else 13)
    cols = [P['zaitun_dk'], P['zaitun'], P['zaitun_lt'], '#C9C984', '#8E9150', '#6B6F3A', '#5C6232']
    b = ''
    items = []
    # massa padat di sudut atas
    for _ in range(700):
        a = rnd.uniform(0, 1.57); d = rnd.random() ** .7
        x = d * 330 * math.cos(a) - 10; y = d * 200 * math.sin(a) - 10
        items.append((y + rnd.uniform(-20, 20), x, y, rnd.uniform(0, 6.28), rnd.uniform(18, 34), rnd.random() < .4))
    # cabang menjuntai
    for k in range(9):
        x0 = rnd.uniform(-10, 300); y0 = rnd.uniform(-10, 60)
        ln = rnd.uniform(160, 380) * (1.2 - x0 / 500)
        a = rnd.uniform(.9, 1.7)
        P4 = ((x0, y0), (x0 + 10, y0 + ln * .3), (x0 + rnd.uniform(-30, 40), y0 + ln * .7), (x0 + rnd.uniform(-50, 60), y0 + ln))
        b += f'<path d="M{r1(P4[0][0])} {r1(P4[0][1])} C{r1(P4[1][0])} {r1(P4[1][1])} {r1(P4[2][0])} {r1(P4[2][1])} {r1(P4[3][0])} {r1(P4[3][1])}" stroke="#5B4A33" stroke-width="{rnd.uniform(1.6,3.4):.1f}" fill="none" stroke-linecap="round"/>'
        for i in range(48):
            t = rnd.uniform(.08, 1); x, y, tx, ty = bez(*P4, t)
            for sg in (1, -1):
                a2 = math.atan2(ty, tx) + sg * rnd.uniform(.5, 1.2)
                items.append((y, x, y, a2, rnd.uniform(14, 26) * (1.05 - t * .35), False))
    # beberapa daun jatuh terpisah
    for _ in range(40):
        items.append((rnd.uniform(60, 300), rnd.uniform(20, 380), rnd.uniform(60, 300), rnd.uniform(0, 6.28), rnd.uniform(12, 22), False))
    for (_, x, y, a, L, dk) in sorted(items, key=lambda i: i[0]):
        c = cols[rnd.randrange(len(cols))]
        if dk: c = cols[0]
        b += f'<path d="{leaf(x, y, a, L, L*.3)}" fill="{c}" stroke="#3C4020" stroke-width=".5" stroke-opacity=".5"/>'
        b += f'<path d="M{r1(x)} {r1(y)} L{r1(x+math.cos(a)*L*.9)} {r1(y+math.sin(a)*L*.9)}" stroke="#E6E3A8" stroke-width=".6" opacity=".3"/>'
    if sisi == 'kanan':
        b = f'<g transform="translate(430 0) scale(-1 1)">{b}</g>'
    return b, ''


def bintang(x, y, r, rot, c1, c2, rnd):
    o = f'<g transform="translate({r1(x)} {r1(y)}) rotate({rot:.0f}) scale({r/20:.3f})">'
    for i in range(5):
        o += f'<path transform="rotate({i*72})" d="M0 0 C-11 -6 -12 -22 0 -26 C12 -22 11 -6 0 0Z" fill="{c1}" stroke="#8A2F66" stroke-width=".8" stroke-opacity=".5"/>'
        o += f'<path transform="rotate({i*72})" d="M0 0 C-4 -6 -4 -14 0 -18 C4 -14 4 -6 0 0Z" fill="{c2}" opacity=".7"/>'
    o += '<circle r="3.4" fill="#F4D77E"/><circle r="1.4" fill="#B56A1E"/></g>'
    return o


def bunga_samping(sisi):
    rnd = random.Random(53 if sisi == 'kiri' else 59)
    b = ''
    for i in range(9):
        x = rnd.uniform(0, 90); y = rnd.uniform(400, 450)
        b += daun_hibiscus(x, y, -math.pi / 2 + rnd.uniform(-.9, .9), rnd.uniform(80, 150), rnd, dark=.25)
    for sp in range(4):
        x0, y0 = 14 + sp * 26, 440
        L = rnd.uniform(280, 400)
        Pp = [(x0, y0), (x0 - 6 + sp * 6, y0 - L * .35), (x0 + 36 + sp * 22, y0 - L * .72), (x0 + 52 + sp * 30, y0 - L)]
        b += f'<path d="M{Pp[0][0]} {Pp[0][1]} C{Pp[1][0]} {Pp[1][1]} {Pp[2][0]} {Pp[2][1]} {Pp[3][0]} {Pp[3][1]}" stroke="{P["daun"]}" stroke-width="2.4" fill="none"/>'
        for j in range(9):
            t = .3 + j * .08
            x, y, tx, ty = bez(*Pp, t)
            r = 20 - j * 1.4
            side = 1 if j % 2 else -1
            fx, fy = x + side * r * .9, y + 4
            b += f'<path d="M{r1(x)} {r1(y)} L{r1(fx)} {r1(fy)}" stroke="{P["daun"]}" stroke-width="1.2" fill="none"/>'
            b += bintang(fx, fy, r, rnd.uniform(0, 72), ['#F3B5D0', '#EA97BE', '#DE7DB0', '#C766A6'][j % 4], '#FBE3EE', rnd)
        x, y, _, _ = bez(*Pp, 1.0)
        for q in range(4):
            b += f'<ellipse cx="{r1(x+q*3)}" cy="{r1(y-q*9)}" rx="5" ry="7" fill="#E58DBA" opacity=".9"/>'
    b += peoni(58, 400, 38, rnd) + peoni(26, 436, 32, rnd)
    if sisi == 'kanan':
        b = f'<g transform="translate(260 0) scale(-1 1)">{b}</g>'
    return b, ''


def main(R):
    b, d = bunga_bawah();       simpan_layer(R, 'bunga-bawah', 0, 640, 860, 320, b, d, seed=21, grain=.05, pig=.10, edge=1.0)
    b, d = dedaunan('kiri');    simpan_layer(R, 'dedaunan-kiri', 0, 0, 430, 520, b, d, seed=22, grain=.05, pig=.10, edge=1.0)
    b, d = dedaunan('kanan');   simpan_layer(R, 'dedaunan-kanan', 0, 0, 430, 520, b, d, seed=23, grain=.05, pig=.10, edge=1.0)
    b, d = bunga_samping('kiri');  simpan_layer(R, 'bunga-samping-kiri', 0, 0, 260, 460, b, d, seed=24, grain=.05, pig=.10, edge=1.0)
    b, d = bunga_samping('kanan'); simpan_layer(R, 'bunga-samping-kanan', 0, 0, 260, 460, b, d, seed=25, grain=.05, pig=.10, edge=1.0)
