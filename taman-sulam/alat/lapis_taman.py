"""Lapisan 'dunia' taman: gunung berkabut, pohon pink, kolonade, taman parterre + air mancur.
Koordinat dunia 860 x 960 (y ke bawah). Tiap fungsi mengembalikan (body, defs)."""
from _lukis import *

W, H = 860, 960


# ---------------------------------------------------------------- gunung
def ridge(rnd, y0, amp, n=9, x0=-20, x1=880, rough=.55):
    pts = [(x0, y0 + rnd.uniform(-amp, amp) * .3), (x1, y0 + rnd.uniform(-amp, amp) * .3)]
    a = amp
    for _ in range(n):
        new = []
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            new += [(xa, ya), ((xa + xb) / 2, (ya + yb) / 2 + rnd.uniform(-a, a))]
        new.append(pts[-1]); pts = new; a *= rough
        if len(pts) > 260: break
    return pts


def kasar(pts, rnd, it=3, amp=14):
    for _ in range(it):
        new = []
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            new += [(xa, ya), ((xa + xb) / 2, (ya + yb) / 2 + rnd.uniform(-amp, amp))]
        new.append(pts[-1]); pts = new; amp *= .55
    return pts


def gunung():
    rnd = random.Random(31)
    defs = ('<filter id="bl1"><feGaussianBlur stdDeviation="1.8"/></filter><filter id="bl2"><feGaussianBlur stdDeviation=".9"/></filter>'
            + lin('mist', [(0, '#F4EBCF', 0), (1, '#F4EBCF', 1)]))
    ranges = [
        ([(-20, 205), (70, 160), (140, 178), (230, 104), (290, 62), (322, 30), (356, 66), (420, 112), (490, 92), (560, 140), (650, 96), (730, 150), (800, 124), (880, 180)], '#DBCB9C', '#F1E8CB', 'bl1', 18),
        ([(-20, 235), (60, 205), (150, 224), (260, 170), (340, 196), (430, 150), (520, 190), (610, 160), (700, 205), (790, 184), (880, 226)], '#CDB97F', '#E6D8A8', 'bl2', 16),
        ([(-20, 270), (90, 244), (200, 262), (320, 238), (440, 258), (560, 240), (680, 262), (800, 246), (880, 266)], '#BDA566', '#D6C589', '', 12),
    ]
    b = ''
    for i, (base, dark, light, fl, d) in enumerate(ranges):
        pts = kasar(base, rnd, 4, 16 - i * 4)
        poly = 'M' + ' L'.join(f'{r1(x)} {r1(y)}' for x, y in pts) + ' L880 345 L-20 345Z'
        b += f'<g {"filter=" + chr(34) + "url(#" + fl + ")" + chr(34) if fl else ""}>'
        b += f'<clipPath id="c{i}"><path d="{poly}"/></clipPath>'
        b += f'<path d="{poly}" fill="{dark}"/>'
        b += f'<path d="{poly}" transform="translate({-d} 0)" fill="{light}" clip-path="url(#c{i})"/>'
        for j in range(0, len(pts) - 1, 4):
            x, y = pts[j]
            b += f'<path d="M{r1(x+5)} {r1(y+10)} q{r1(rnd.uniform(2,9))} {r1(rnd.uniform(16,30))} {r1(rnd.uniform(-3,10))} {r1(rnd.uniform(36,60))}" stroke="#A8925A" stroke-width="1" fill="none" opacity=".28" stroke-linecap="round"/>'
        b += '</g>'
    b += '<rect x="-20" y="228" width="900" height="117" fill="url(#mist)"/>'
    return b, defs


# ---------------------------------------------------------------- pohon pink
def pohon_pink():
    rnd = random.Random(23)
    defs = lin('t', [(0, '#8A6A55'), (1, '#5E4636')])
    cols = ['#C97AAD', '#D58AB8', '#DE9EC2', '#E8B3D0', '#F1C9DC', '#B96398', '#D888B5', '#F5D7E5']
    hi = ['#F8DDE9', '#FFF0F5']
    b = ''
    trees = [(60, 470, 150, 175), (210, 490, 135, 155), (335, 505, 125, 145), (440, 515, 115, 135), (545, 505, 125, 145), (670, 490, 135, 155), (800, 470, 150, 175), (130, 505, 105, 115), (735, 505, 105, 115), (390, 520, 90, 100), (490, 520, 90, 100)]
    trees.sort(key=lambda t: t[3])
    for (cx, cy, rx, ry) in trees:
        top = cy - ry * 1.5
        b += f'<path d="M{cx-4} {cy} Q{cx-6} {cy-ry*.5} {cx-14} {top+ry*1.1} L{cx+6} {top+ry*1.1} Q{cx+8} {cy-ry*.5} {cx+5} {cy}Z" fill="url(#t)" opacity=".9"/>'
        n = int(rx * ry / 45)
        blobs = []
        for _ in range(n):
            a = rnd.uniform(0, 6.283); d = math.sqrt(rnd.random())
            x = cx + math.cos(a) * rx * d; y = top + ry * .55 + math.sin(a) * ry * .62 * d
            blobs.append((y, x))
        for y, x in sorted(blobs):
            t = (y - (top)) / (ry * 1.2)
            c = cols[rnd.randrange(len(cols))]
            c = mix(c, '#A5528A', max(0, min(.32, (t - .5) * .6)))
            r = rnd.uniform(6, 15)
            b += f'<path d="{blob(x, y, r, rnd, 8, .3)}" fill="{c}" opacity="{rnd.uniform(.82,.98):.2f}"/>'
            if rnd.random() < .55:
                b += f'<circle cx="{r1(x-r*.3)}" cy="{r1(y-r*.35)}" r="{r*.32:.1f}" fill="{hi[rnd.randrange(2)]}" opacity="{rnd.uniform(.35,.8):.2f}"/>'
        # kilau cahaya di atas
        for _ in range(int(n * .25)):
            a = rnd.uniform(3.3, 6.0); d = rnd.uniform(.3, 1)
            b += f'<circle cx="{r1(cx+math.cos(a)*rx*d)}" cy="{r1(top+ry*.55+math.sin(a)*ry*.6*d)}" r="{rnd.uniform(1.5,4):.1f}" fill="#FFF3F8" opacity=".55"/>'
    return b, defs


# ---------------------------------------------------------------- kolonade (perspektif satu titik)
def kolonade(sisi='kiri'):
    rnd = random.Random(5)
    n = 8; a = 1.5
    xn, xf = 0, 345            # tepi dekat -> tepi jauh
    ybn, ybf = 640, 556        # dasar
    ytn, ytf = 392, 486        # atap
    defs = (lin('wall', [(0, '#F3EACB'), (1, '#E0D2A2')]) + lin('lit', [(0, '#FBF5DF'), (1, '#EDE2BC')]) +
            lin('shadow', [(0, '#C9B982'), (1, '#E0D2A2')]) + lin('gold', [(0, '#EAD58E'), (.5, '#C9A85A'), (1, '#9A7A32')]))

    def F(s, v):
        p = s * (1 + a) / (1 + a * s)
        x = lerp(xn, xf, p); yb = lerp(ybn, ybf, p); yt = lerp(ytn, ytf, p)
        return x, yb + (yt - yb) * v

    def poly(pts, fill, extra=''):
        return f'<polygon points="{" ".join(f"{r1(x)},{r1(y)}" for x, y in pts)}" fill="{fill}" {extra}/>'

    b = ''
    b += poly([F(0, 0), F(1, 0), F(1, 1), F(0, 1)], 'url(#wall)')
    cw = .018
    for i in range(n):
        s0, s1 = i / n, (i + 1) / n
        sa, sb = s0 + cw * 1.3, s1 - cw * 1.3
        # lengkung tapal kuda
        top = []
        for k in range(0, 25):
            u = k / 24
            v = .5 + .33 * math.sqrt(max(0, 1 - (2 * u - 1) ** 2)) * (1 + .08 * math.sin(u * 3.14))
            top.append(F(lerp(sa, sb, u), v))
        pts = [F(sa, .04)] + [F(sa, .5)] + top + [F(sb, .5), F(sb, .04)]
        b += poly(pts, 'url(#shadow)', 'opacity=".5"')
        # sisi dalam terang
        inner = [F(lerp(sa, sb, .08), .06), F(lerp(sa, sb, .08), .5)] + [F(lerp(sa, sb, .08 + .84 * k / 24), .5 + .29 * math.sqrt(max(0, 1 - (2 * (k / 24) - 1) ** 2))) for k in range(25)] + [F(lerp(sa, sb, .92), .5), F(lerp(sa, sb, .92), .06)]
        b += poly(inner, 'url(#lit)', 'opacity=".75"')
        # kisi/mashrabiya
        for k in range(1, 6):
            u = k / 6
            b += f'<polyline points="{r1(F(lerp(sa,sb,u),.1)[0])},{r1(F(lerp(sa,sb,u),.1)[1])} {r1(F(lerp(sa,sb,u),.6)[0])},{r1(F(lerp(sa,sb,u),.6)[1])}" stroke="#B89A4C" stroke-width=".8" fill="none" opacity=".6"/>'
        for k in range(1, 5):
            v = .1 + k * .1
            q0, q1 = F(sa, v), F(sb, v)
            b += f'<line x1="{r1(q0[0])}" y1="{r1(q0[1])}" x2="{r1(q1[0])}" y2="{r1(q1[1])}" stroke="#B89A4C" stroke-width=".7" opacity=".55"/>'
        # bingkai lengkung emas
        b += f'<polyline points="{" ".join(f"{r1(x)},{r1(y)}" for x, y in top)}" fill="none" stroke="url(#gold)" stroke-width="{max(1.2, 5*(1-s0)**1.2):.1f}"/>'
        # ornamen spandrel
        mid = F((s0 + s1) / 2, .93)
        b += f'<circle cx="{r1(mid[0])}" cy="{r1(mid[1])}" r="{max(1.5, 7*(1-s0)):.1f}" fill="url(#gold)" opacity=".85"/>'
        # kolom
        for sc in (s0, s1):
            q = [F(sc - cw, .04), F(sc + cw, .04), F(sc + cw, .88), F(sc - cw, .88)]
            b += poly(q, 'url(#gold)', 'opacity=".95"')
            b += poly([F(sc - cw * 1.8, .0), F(sc + cw * 1.8, .0), F(sc + cw * 1.8, .05), F(sc - cw * 1.8, .05)], '#A88A42')
    # kornis & pagar atap bergerigi
    b += poly([F(0, .9), F(1, .9), F(1, 1.0), F(0, 1.0)], 'url(#gold)', 'opacity=".92"')
    b += poly([F(0, .97), F(1, .97), F(1, 1.0), F(0, 1.0)], '#EAD58E')
    for i in range(n * 2):
        s = (i + .5) / (n * 2)
        a0, a1, a2 = F(s - .02, 1.0), F(s + .02, 1.0), F(s, 1.0 + .13)
        b += poly([a0, a1, a2], 'url(#gold)')
    b += poly([F(0, 0), F(1, 0), F(1, .045), F(0, .045)], '#9C8446', 'opacity=".7"')
    if sisi == 'kanan':
        b = f'<g transform="translate({W} 0) scale(-1 1)">{b}</g>'
    return b, defs


# ---------------------------------------------------------------- taman
H0, S = 430, 340


def pj(X, Z, y=0.0):
    return 430 + X * S / Z, H0 + (1 - y) * S / Z


def cincin_tanah(X, Z, r, y=0.0, n=48, sy=1.0):
    return [pj(X + math.cos(i / n * 6.283) * r, Z + math.sin(i / n * 6.283) * r * sy, y) for i in range(n)]


def path_d(pts): return 'M' + ' L'.join(f'{r1(x)} {r1(y)}' for x, y in pts) + 'Z'


def taman():
    rnd = random.Random(17)
    defs = (lin('lawn', [(0, '#D3D8B2'), (1, '#BDC79A')]) + lin('jalan', [(0, '#F6EFD8'), (1, '#FBF7E8')]) +
            lin('stone', [(0, '#F4ECD2'), (1, '#D6C89B')]) + rad('wat', [(0, '#F7FAF4'), (1, '#CFE0DA')]) +
            lin('hedge', [(0, '#6E8B5C'), (1, '#486A47')]))
    b = ''
    # tanah dasar (rumput + jalan)
    b += f'<polygon points="0,{H0+8} 860,{H0+8} 860,900 0,900" fill="url(#lawn)"/>'
    for x0 in range(230, 640, 9):
        r = rnd.uniform(9, 20)
        col = mix(rnd.choice(['#9FB58A', '#B7C79A', '#C9D4A8', '#D9B8C8', '#C99CB8']), '#E9E4C8', rnd.random() * .5)
        b += f'<path d="{blob(x0 + rnd.uniform(-4, 4), H0 + rnd.uniform(-14, 4), r, rnd, 8, .3)}" fill="{col}" opacity=".92"/>'
    # jalan tengah (trapesium)
    j = [pj(-.5, 6), pj(.5, 6), pj(.62, .9), pj(-.62, .9)]
    b += f'<polygon points="{" ".join(f"{r1(x)},{r1(y)}" for x,y in j)}" fill="url(#jalan)"/>'
    # jalan silang (plaza di sekitar air mancur)
    pl = [pj(-1.2, 1.9), pj(1.2, 1.9), pj(1.5, 1.05), pj(-1.5, 1.05)]
    b += f'<polygon points="{" ".join(f"{r1(x)},{r1(y)}" for x,y in pl)}" fill="url(#jalan)"/>'
    # petak parterre kiri & kanan
    for sg in (-1, 1):
        for (x0, x1, z0, z1) in ((.72, 1.9, 2.2, 3.4), (.72, 1.9, 3.6, 5.4), (1.15, 2.8, 1.25, 2.1)):
            X0, X1 = sorted((sg * x0, sg * x1))
            c = [pj(X0, z0), pj(X1, z0), pj(X1, z1), pj(X0, z1)]
            b += f'<polygon points="{" ".join(f"{r1(x)},{r1(y)}" for x,y in c)}" fill="#CBD3A6"/>'
            # pagar tanaman (hedge) tepi
            for (A, B) in ((0, 1), (1, 2), (2, 3), (3, 0)):
                (xa, ya), (xb, yb) = c[A], c[B]
                b += f'<line x1="{r1(xa)}" y1="{r1(ya)}" x2="{r1(xb)}" y2="{r1(yb)}" stroke="#4F7050" stroke-width="{max(3, 14/ (z0+.4)):.1f}" stroke-linecap="round" opacity=".92"/>'
                b += f'<line x1="{r1(xa)}" y1="{r1(ya-2)}" x2="{r1(xb)}" y2="{r1(yb-2)}" stroke="#7FA070" stroke-width="{max(1, 5/(z0+.4)):.1f}" stroke-linecap="round" opacity=".8"/>'
            # pola simpul di dalam
            cxm, czm = (X0 + X1) / 2, (z0 + z1) / 2
            for k in range(2):
                fx = .72 - k * .3
                ic = [pj(cxm + (X1 - X0) / 2 * fx * s1, czm + (z1 - z0) / 2 * fx * s2) for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                b += f'<polygon points="{" ".join(f"{r1(x)},{r1(y)}" for x,y in ic)}" fill="none" stroke="#5C7C55" stroke-width="{max(1.4, 6/(z0+.4)):.1f}" opacity=".8"/>'
            cx0, cy0 = pj(cxm, czm)
            rr = max(5, 34 / (czm + .3))
            b += f'<ellipse cx="{r1(cx0)}" cy="{r1(cy0)}" rx="{rr*1.4:.1f}" ry="{rr*.55:.1f}" fill="#E9E3C2" stroke="#5C7C55" stroke-width="1.6" opacity=".95"/>'
            # bunga putih
            for _ in range(int(70 / (z0 * .6))):
                px = rnd.uniform(X0 + .08, X1 - .08); pz = rnd.uniform(z0 + .05, z1 - .05)
                sx, sy = pj(px, pz)
                b += f'<circle cx="{r1(sx)}" cy="{r1(sy)}" r="{max(1.2, 5/pz):.1f}" fill="#FBF6EA" opacity="{rnd.uniform(.6,.95):.2f}"/>'
    # semak perak/putih depan (kiri & kanan air mancur)
    for (cx, cy, rx, ry) in ((95, 700, 120, 70), (775, 700, 120, 70), (190, 740, 90, 50), (680, 742, 90, 50)):
        for _ in range(int(rx * ry / 60)):
            a = rnd.uniform(0, 6.283); d = math.sqrt(rnd.random())
            x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d - 10
            col = ['#C7D4C3', '#DDE5D6', '#B6C7B4', '#EEF0E2', '#FFFFFF'][rnd.randrange(5)]
            b += f'<path d="{blob(x, y, rnd.uniform(6, 15), rnd, 7, .3)}" fill="{col}" opacity=".92"/>'
            if rnd.random() < .5: b += f'<circle cx="{r1(x+rnd.uniform(-5,5))}" cy="{r1(y+rnd.uniform(-5,5))}" r="{rnd.uniform(1.5,3):.1f}" fill="#FFFFFF"/>'
    # pohon bulat (topiary) kiri-kanan
    for X in (-.95, .95):
        x, y = pj(X, 2.6); r = 34
        b += f'<rect x="{r1(x-3)}" y="{r1(y-r*.2)}" width="6" height="{r*.9:.0f}" fill="#6B5238"/>'
        for _ in range(60):
            a = rnd.uniform(0, 6.283); d = math.sqrt(rnd.random())
            px = x + math.cos(a) * r * d; py = y - r * 1.4 + math.sin(a) * r * d * .95
            c = mix('#6F8F5E', '#A6BE8C', rnd.random() ** 1.5)
            b += f'<path d="{blob(px, py, rnd.uniform(5, 10), rnd, 7, .3)}" fill="{c}" opacity=".95"/>'
    # ---- air mancur bertingkat ----
    fx, fz = 0, 1.2
    cx, cy = pj(fx, fz)
    k = S / fz
    def mangkuk(yy, rx, tebal, air=True):
        ry = rx * .27
        o = f'<path d="M{r1(cx-rx)} {r1(yy)} L{r1(cx-rx*.86)} {r1(yy+tebal)} A{r1(rx*.86)} {r1(ry*.86)} 0 0 0 {r1(cx+rx*.86)} {r1(yy+tebal)} L{r1(cx+rx)} {r1(yy)}Z" fill="url(#stone)" stroke="#C3B386" stroke-width="1.2"/>'
        o += f'<ellipse cx="{r1(cx)}" cy="{r1(yy)}" rx="{r1(rx)}" ry="{r1(ry)}" fill="#F7F0D8" stroke="#C3B386" stroke-width="1.4"/>'
        if air:
            o += f'<ellipse cx="{r1(cx)}" cy="{r1(yy+1.5)}" rx="{r1(rx*.88)}" ry="{r1(ry*.82)}" fill="url(#wat)"/>'
            o += f'<ellipse cx="{r1(cx)}" cy="{r1(yy+1.5)}" rx="{r1(rx*.55)}" ry="{r1(ry*.5)}" fill="none" stroke="#fff" stroke-width="1" opacity=".6"/>'
        return o
    b += f'<ellipse cx="{r1(cx)}" cy="{r1(cy+8)}" rx="{.62*k:.0f}" ry="{.2*k:.0f}" fill="#8A7C52" opacity=".2"/>'
    b += mangkuk(cy - 6, .56 * k, 26)
    b += f'<path d="M{r1(cx-13)} {r1(cy-8)} L{r1(cx-8)} {r1(cy-70)} L{r1(cx+8)} {r1(cy-70)} L{r1(cx+13)} {r1(cy-8)}Z" fill="url(#stone)" stroke="#C3B386"/>'
    b += mangkuk(cy - 78, .30 * k, 16)
    b += f'<path d="M{r1(cx-8)} {r1(cy-80)} L{r1(cx-5)} {r1(cy-126)} L{r1(cx+5)} {r1(cy-126)} L{r1(cx+8)} {r1(cy-80)}Z" fill="url(#stone)" stroke="#C3B386"/>'
    b += mangkuk(cy - 132, .17 * k, 10)
    b += f'<path d="M{r1(cx-4)} {r1(cy-134)} L{r1(cx-2.5)} {r1(cy-168)} L{r1(cx+2.5)} {r1(cy-168)} L{r1(cx+4)} {r1(cy-134)}Z" fill="url(#stone)" stroke="#C3B386"/>'
    b += f'<ellipse cx="{r1(cx)}" cy="{r1(cy-172)}" rx="9" ry="12" fill="url(#stone)" stroke="#C3B386"/><path d="M{r1(cx)} {r1(cy-186)} q4 -8 0 -14 q-4 6 0 14z" fill="#E6D9A8"/>'
    for yy, rr, n in ((cy - 78, .30 * k, 9), (cy - 132, .17 * k, 7), (cy - 6, .56 * k, 12)):
        for j in range(n):
            t = (j + .5) / n - .5
            x0 = cx + t * rr * 1.5; y0 = yy - 4
            b += f'<path d="M{r1(cx+t*rr*.45)} {r1(yy-52 if rr<.5*k else yy-60)} Q{r1(cx+t*rr*1.3)} {r1(yy-70 if rr<.5*k else yy-82)} {r1(x0)} {r1(y0+4)}" stroke="#FFFFFF" stroke-width="1.5" fill="none" opacity=".7" stroke-linecap="round"/>'
    b += f'<path d="M{r1(cx)} {r1(cy-176)} Q{r1(cx-30)} {r1(cy-216)} {r1(cx-58)} {r1(cy-130)} M{r1(cx)} {r1(cy-176)} Q{r1(cx+30)} {r1(cy-216)} {r1(cx+58)} {r1(cy-130)} M{r1(cx)} {r1(cy-176)} Q{r1(cx)} {r1(cy-220)} {r1(cx)} {r1(cy-140)}" stroke="#E8F4F0" stroke-width="2.4" fill="none" opacity=".85" stroke-linecap="round"/>'
    return b, defs
