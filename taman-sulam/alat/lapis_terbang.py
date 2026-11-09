"""Kupu-kupu putih & merpati putih realistis (bagian terpisah agar bisa mengepak), ikon garis, marmer bingkai, vinyet taman."""
import math, os, random
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from _lukis import *

SL = '#B9B9AE'


# ------------------------------------------------------------- kupu-kupu putih (Pieris)
def sayap_kupu(sisi='kanan'):
    """Sayap kanan dalam kotak 0..112 x 0..150, pangkal di x=0 (badan). Kiri = cermin."""
    d = ('<radialGradient id="w1" cx="0" cy=".42" r="1.05"><stop offset="0" stop-color="#C9CBB8"/><stop offset=".18" stop-color="#EDEEE2"/><stop offset=".55" stop-color="#FFFFFC"/><stop offset="1" stop-color="#F4F5EA"/></radialGradient>'
         '<radialGradient id="w2" cx="0" cy=".2" r="1.1"><stop offset="0" stop-color="#D3CFA8"/><stop offset=".25" stop-color="#F6F4DA"/><stop offset=".7" stop-color="#FFFFF8"/><stop offset="1" stop-color="#F2F1E0"/></radialGradient>'
         '<radialGradient id="ap" cx=".8" cy=".1" r=".7"><stop offset="0" stop-color="#2E2E2C" stop-opacity=".95"/><stop offset=".6" stop-color="#454542" stop-opacity=".55"/><stop offset="1" stop-color="#454542" stop-opacity="0"/></radialGradient>'
         '<filter id="bl"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="bl2"><feGaussianBlur stdDeviation=".7"/></filter>')
    fore = 'M0 56 C4 24 34 -2 78 4 C100 8 112 20 108 40 C102 66 76 86 46 88 C22 90 6 78 0 64Z'
    hind = 'M0 70 C26 74 58 78 76 96 C92 114 82 142 54 146 C26 150 4 124 0 92Z'
    b = f'<path d="{hind}" fill="url(#w2)" stroke="{SL}" stroke-width=".8" stroke-opacity=".8"/>'
    b += f'<path d="{fore}" fill="url(#w1)" stroke="{SL}" stroke-width=".9" stroke-opacity=".85"/>'
    # pembuluh sayap
    for k in range(9):
        a = -1.0 + k * .22
        b += f'<path d="M0 62 Q{36*math.cos(a)+10:.0f} {62+30*math.sin(a):.0f} {96*math.cos(a)+8:.0f} {62+78*math.sin(a):.0f}" stroke="#9A9A8E" stroke-width=".6" fill="none" opacity=".45" clip-path="url(#cf)"/>'
    for k in range(7):
        a = .15 + k * .2
        b += f'<path d="M0 84 Q{30*math.cos(a)+8:.0f} {84+34*math.sin(a):.0f} {70*math.cos(a)+6:.0f} {84+76*math.sin(a):.0f}" stroke="#A8A388" stroke-width=".6" fill="none" opacity=".4" clip-path="url(#ch)"/>'
    d += f'<clipPath id="cf"><path d="{fore}"/></clipPath><clipPath id="ch"><path d="{hind}"/></clipPath>'
    # puncak sayap depan gelap + bercak
    b += f'<path d="M62 4 C96 6 112 20 108 42 C100 34 86 24 62 4Z" fill="url(#ap)" filter="url(#bl2)"/>'
    b += '<ellipse cx="62" cy="44" rx="7.5" ry="6" fill="#3A3A38" opacity=".78" filter="url(#bl2)"/><ellipse cx="78" cy="68" rx="6" ry="5" fill="#3A3A38" opacity=".7" filter="url(#bl2)"/>'
    b += '<ellipse cx="66" cy="112" rx="6" ry="4.4" fill="#4A4838" opacity=".5" filter="url(#bl2)"/>'
    # bulu halus di pangkal
    b += '<path d="M0 56 Q22 60 30 78 L0 90Z" fill="#CFCFC0" opacity=".55" filter="url(#bl)"/>'
    # tepi sayap berumbai
    b += f'<path d="{fore}" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity=".5" transform="translate(-.4 -.4)"/>'
    if sisi == 'kiri':
        b = f'<g transform="translate(112 0) scale(-1 1)">{b}</g>'
    return b, d


def badan_kupu():
    d = ('<linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="#4A4A46"/><stop offset=".5" stop-color="#8A8A82"/><stop offset="1" stop-color="#3A3A36"/></linearGradient>'
         '<radialGradient id="hd" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#8F8F86"/><stop offset="1" stop-color="#2E2E2B"/></radialGradient>')
    b = '<ellipse cx="14" cy="46" rx="6.4" ry="11" fill="#E9E9DE" opacity=".95"/>'
    b += '<path d="M14 36 C5 44 5 80 14 128 C23 80 23 44 14 36Z" fill="url(#bd)"/>'
    for k in range(12):
        b += f'<path d="M{9+k*.3:.1f} {58+k*5.5} q5 3 10 0" stroke="#D9D9CE" stroke-width=".8" fill="none" opacity=".7"/>'
    b += '<ellipse cx="14" cy="38" rx="6" ry="8" fill="#E6E6DA" opacity=".9"/><circle cx="14" cy="26" r="5.2" fill="url(#hd)"/><circle cx="11.6" cy="25" r="1.2" fill="#E7E7E0" opacity=".8"/><circle cx="16.6" cy="25" r="1.2" fill="#E7E7E0" opacity=".8"/>'
    b += '<path d="M12 22 C8 10 2 4 -4 2 M16 22 C20 10 26 4 32 2" stroke="#3A3A36" stroke-width="1" fill="none"/><circle cx="-4.4" cy="2" r="1.8" fill="#3A3A36"/><circle cx="32.4" cy="2" r="1.8" fill="#3A3A36"/>'
    return b, d


# ------------------------------------------------------------- merpati putih
def bulu(x, y, ang, L, W, fill='url(#bu)', op=1):
    ca, sa = math.cos(ang), math.sin(ang); nx, ny = -sa, ca
    ex, ey = x + ca * L, y + sa * L
    return (f'<path d="M{r1(x)} {r1(y)} C{r1(x+ca*L*.25+nx*W)} {r1(y+sa*L*.25+ny*W)} {r1(x+ca*L*.8+nx*W*.9)} {r1(y+sa*L*.8+ny*W*.9)} {r1(ex)} {r1(ey)} '
            f'C{r1(x+ca*L*.8-nx*W*.55)} {r1(y+sa*L*.8-ny*W*.55)} {r1(x+ca*L*.25-nx*W*.8)} {r1(y+sa*L*.25-ny*W*.8)} {r1(x)} {r1(y)}Z" fill="{fill}" stroke="#B4B4AB" stroke-width=".55" stroke-opacity=".8" opacity="{op}"/>'
            f'<path d="M{r1(x)} {r1(y)} L{r1(x+ca*L*.94)} {r1(y+sa*L*.94)}" stroke="#A9A9A0" stroke-width=".5" opacity=".6" fill="none"/>')


DEFS_MERPATI = ('<linearGradient id="bu" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#F3F3EE"/><stop offset="1" stop-color="#D9D9D2"/></linearGradient>'
                '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#F1F1EB"/><stop offset="1" stop-color="#CFCFC6"/></linearGradient>'
                '<linearGradient id="bf" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#E6E6DF"/><stop offset="1" stop-color="#BDBDB3"/></linearGradient>')


def sayap_merpati(dekat=True):
    """Sayap menunjuk ke belakang (kiri), pangkal di (150,60) pada kotak 170x120."""
    fill = 'url(#bu)' if dekat else 'url(#bf)'
    b = ''
    ox, oy = 150, 60
    for i in range(11):                     # bulu primer
        a = math.radians(188 - i * 6.2); L = 128 - i * 4.2 + (i % 2) * 2
        b += bulu(ox - i * 2.2, oy + i * .6, a, L, 9.5 - i * .3, fill)
    for i in range(9):                      # bulu sekunder
        a = math.radians(172 - i * 5.5); L = 98 - i * 3
        b += bulu(ox - 6 - i * 3.2, oy + 6 + i * .8, a, L, 9 - i * .2, fill)
    for i in range(10):                     # penutup
        a = math.radians(176 - i * 7); L = 66 - i * 2.4
        b += bulu(ox - 3 - i * 3, oy + 2, a, L, 8, fill, .98)
    b += f'<ellipse cx="{ox-24}" cy="{oy+1}" rx="30" ry="12" fill="{fill}" opacity=".95"/>'
    return b


def badan_merpati():
    b = ''
    for i, a in enumerate((196, 188, 180, 172, 164)):      # ekor kipas
        b += bulu(54, 70, math.radians(a), 62 - abs(i - 2) * 4, 9, 'url(#bu)')
    b += '<path d="M44 66 C58 48 100 44 136 52 C158 56 172 62 176 70 C172 84 140 92 104 90 C72 88 50 80 44 66Z" fill="url(#bg)" stroke="#C4C4BB" stroke-width=".7"/>'
    for k in range(5):
        b += f'<path d="M{70+k*16} {74+ (k%2)*3} q8 7 16 0" stroke="#C9C9C0" stroke-width=".7" fill="none" opacity=".8"/>'
    b += '<path d="M150 54 C160 42 170 40 182 44 C194 48 196 58 188 66 C178 72 164 70 154 66Z" fill="url(#bg)" stroke="#C4C4BB" stroke-width=".7"/>'
    b += '<path d="M192 52 L212 58 L192 62Z" fill="#E7B7A6" stroke="#B88B7C" stroke-width=".5"/><path d="M192 54 L204 57.4 L192 58.4Z" fill="#C79484" opacity=".7"/>'
    b += '<circle cx="183" cy="52" r="2.6" fill="#2B2623"/><circle cx="182.2" cy="51.2" r=".8" fill="#fff"/><circle cx="183" cy="52" r="4.6" fill="none" stroke="#D9A98C" stroke-width=".7" opacity=".8"/>'
    b += '<path d="M132 90 q-4 10 -2 14 M146 88 q-2 10 2 14" stroke="#D4A08E" stroke-width="2" fill="none" stroke-linecap="round"/>'
    return b


# ------------------------------------------------------------- ikon garis (sage/emas)
def ikon(nama):
    s = '#7F9A78'; g = '#B8923A'; p = '#C2477F'
    st = f'fill="none" stroke="{s}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    if nama == 'cincin':
        return f'<g {st}><circle cx="24" cy="38" r="13"/><circle cx="42" cy="38" r="13" stroke="{g}"/></g><path d="M33 17 l5 6 l-5 6 l-5 -6z" fill="{p}" opacity=".85"/>'
    if nama == 'resepsi':   # dua gelas
        return f'<g {st}><path d="M18 14 h16 l-3 18 a5 5 0 0 1 -10 0z"/><path d="M26 37 v14 M20 51 h12"/><path d="M40 20 h14 l-3 16 a5 5 0 0 1 -8 0z" stroke="{g}"/><path d="M47 41 v10 M42 51 h10" stroke="{g}"/></g><circle cx="38" cy="10" r="2" fill="{p}"/>'
    if nama == 'pin':
        return f'<path d="M32 8 C21 8 14 16 14 25 C14 38 32 56 32 56 C32 56 50 38 50 25 C50 16 43 8 32 8Z" fill="{p}" opacity=".9"/><circle cx="32" cy="25" r="7" fill="#FFF8E6"/>'
    if nama == 'hadiah':
        return f'<g {st}><rect x="12" y="26" width="40" height="26" rx="3"/><rect x="9" y="18" width="46" height="9" rx="3"/><path d="M32 18 v34"/><path d="M32 18 C26 6 16 8 20 14 C23 18 32 18 32 18 C32 18 41 18 44 14 C48 8 38 6 32 18"/></g>'
    if nama == 'hati':
        return f'<path d="M32 54 C10 38 8 22 18 16 C25 12 31 16 32 21 C33 16 39 12 46 16 C56 22 54 38 32 54Z" fill="{p}" opacity=".9"/>'
    if nama == 'live':
        return f'<g {st}><rect x="8" y="16" width="38" height="30" rx="5"/><path d="M46 28 l12 -7 v22 l-12 -7z"/></g><circle cx="17" cy="25" r="3" fill="{p}"/>'
    if nama == 'tautan':
        return f'<g {st}><path d="M26 38 a9 9 0 0 1 0 -13 l7 -7 a9 9 0 0 1 13 13 l-4 4"/><path d="M38 26 a9 9 0 0 1 0 13 l-7 7 a9 9 0 0 1 -13 -13 l4 -4"/></g>'
    return ''


# ------------------------------------------------------------- marmer (bingkai kartu)
def marmer(n=512, seed=4):
    rng = np.random.default_rng(seed)
    def nz(sg): return gaussian_filter(rng.standard_normal((n, n)), sg, mode='wrap')
    a, b2, c = nz(70), nz(70), nz(34)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    wx = xx + 60 * a / a.std(); wy = yy + 60 * b2 / b2.std()
    v = np.sin((wx * .02 + wy * .014) + 2.2 * c / c.std()) * .5 + .5
    cols = np.array([[0xF8, 0xF0, 0xDA], [0xF0, 0xCB, 0xDB], [0xC9, 0xD6, 0xBC], [0xE6, 0xD2, 0x9A], [0xFB, 0xF5, 0xE4]], np.float32)
    idx = v * 3.6; i0 = np.clip(idx.astype(int), 0, 3); f = (idx - i0)[..., None]
    img = cols[i0] * (1 - f) + cols[np.clip(i0 + 1, 0, 4)] * f
    vein = np.exp(-((np.abs(np.sin(v * 7.5 + 1.0))) ** 2) / .006)[..., None]
    img = img * (1 - .10 * vein) + np.array([255, 252, 242]) * .10 * vein
    img = img * .78 + np.array([248, 240, 218]) * .22
    img *= 1 + .015 * gaussian_filter(rng.standard_normal((n, n)), .8, mode='wrap')[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def vinyet():
    """Pemandangan mini (pohon + kolonade + air mancur + bunga) sebagai pembatas section, memudar di atas."""
    import json
    M = json.load(open(os.path.join(ROOT, 'assets', 'layer-manifest.json')))
    cv = Image.new('RGBA', (860, 960), (0, 0, 0, 0))
    for n in ('pohon-pink', 'taman', 'kolonade-kiri', 'kolonade-kanan', 'bunga-bawah'):
        m = M[n]; cv.alpha_composite(Image.open(os.path.join(DIR_LAYER, n + '.webp')).convert('RGBA'), (m['x'], m['y']))
    crop = cv.crop((0, 330, 860, 960))
    a = np.array(crop).astype(np.float32); h = a.shape[0]
    fade = np.clip(np.linspace(0, 1, h) / .28, 0, 1)[:, None] ** 1.2
    a[..., 3] *= fade
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def main(R):
    b, d = sayap_kupu('kanan'); simpan_svg('kupu-sayap-kanan', 112, 150, b, d)
    b, d = sayap_kupu('kiri'); simpan_svg('kupu-sayap-kiri', 112, 150, b, d)
    b, d = badan_kupu(); simpan_svg('kupu-badan', 28, 132, b, d)
    simpan_svg('merpati-sayap-dekat', 170, 120, sayap_merpati(True), DEFS_MERPATI)
    simpan_svg('merpati-sayap-jauh', 170, 120, sayap_merpati(False), DEFS_MERPATI)
    simpan_svg('merpati-badan', 220, 120, badan_merpati(), DEFS_MERPATI)
    for n in ('cincin', 'resepsi', 'pin', 'hadiah', 'hati', 'live', 'tautan'):
        simpan_svg('ikon-' + n, 64, 64, ikon(n))
    marmer().save(os.path.join(DIR_LAYER, 'marmer.webp'), 'WEBP', quality=80, method=6)
    vinyet().save(os.path.join(DIR_LAYER, 'vinyet-taman.webp'), 'WEBP', quality=82, method=6)
    print('terbang ok')
