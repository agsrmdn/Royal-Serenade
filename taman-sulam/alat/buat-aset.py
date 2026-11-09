#!/usr/bin/env python3
"""
Wedding Code - Generator Aset Tema TAMAN SULAM (lukisan cat air + sulam silang)
Jalankan dari folder proyek:   python3 alat/buat-aset.py
Hasil:  assets/layer/*.webp   (lapisan lukisan bertekstur, transparan)
        assets/svg/*.svg      (motif sulam, pita, garis bunga, bintang sage)
        css/layer.css         (posisi lapisan, dibuat otomatis dari manifest)
Butuh: python3, numpy, scipy, pillow, playwright (chromium).
Mengganti lapisan dengan hasil ilustrator/AI: cukup timpa file WebP bernama sama
(ukuran piksel & posisi lihat assets/layer-manifest.json) - kode tidak perlu diubah.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lukis import *
import kertas, lapis_taman as T, lapis_bunga as B, lapis_kertas as K


def efek_hidup(R):
    """Kabut berawan (digeser CSS) + kupu-kupu terbang (SVG)."""
    import numpy as np
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(9); w, h = 1200, 260
    n = sum(gaussian_filter(rng.standard_normal((h, w)), s, mode='wrap') / (1 + i) * (s ** .5) for i, s in enumerate((60, 26, 12)))
    n = (n - n.mean()) / n.std()
    a = np.clip((n + .2) / 2.4, 0, 1) ** 1.6
    yy = np.linspace(0, 1, h)[:, None]; a *= np.sin(yy * np.pi) ** 1.2
    img = np.zeros((h, w, 4), np.uint8); img[..., 0], img[..., 1], img[..., 2] = 253, 249, 234; img[..., 3] = (a * 235).astype(np.uint8)
    Image.fromarray(img, 'RGBA').save(os.path.join(DIR_LAYER, 'kabut.webp'), 'WEBP', quality=80, method=6)
    for nama, c1, c2 in (('kupu-jingga', '#E8903E', '#F7C58A'), ('kupu-pink', '#E36FA2', '#F7C4DA'), ('kupu-krem', '#E9D58F', '#FFF6D8')):
        simpan_svg(nama, 100, 90, B.kupu(50, 40, 1.2, 0, c1, c2))


def main():
    kertas.kertas_tile().save(os.path.join(DIR_LAYER, 'kertas.webp'), 'WEBP', quality=84, method=6)
    R = Perender()
    try:
        b, d = T.gunung();          simpan_layer(R, 'gunung', 0, 0, 860, 340, b, d, seed=1, grain=.04, pig=.08, edge=.8)
        b, d = T.pohon_pink();      simpan_layer(R, 'pohon-pink', 0, 150, 860, 430, b, d, seed=2, grain=.05, pig=.10, edge=1.2)
        b, d = T.kolonade('kiri');  simpan_layer(R, 'kolonade-kiri', 0, 320, 430, 340, b, d, seed=3, grain=.04, pig=.07, edge=.6)
        b, d = T.kolonade('kanan'); simpan_layer(R, 'kolonade-kanan', 430, 320, 430, 340, b, d, seed=4, grain=.04, pig=.07, edge=.6)
        b, d = T.taman();           simpan_layer(R, 'taman', 0, 420, 860, 480, b, d, seed=5, grain=.045, pig=.09, edge=.9)
        B.main(R)
        K.main(R)
        efek_hidup(R)
    finally:
        R.tutup()
    json.dump(MANIFEST, open(os.path.join(ROOT, 'assets', 'layer-manifest.json'), 'w'), indent=1)
    css = '/* AUTO-GENERATED oleh alat/buat-aset.py dari assets/layer-manifest.json. Jangan edit manual. */\n'
    for n in ('gunung', 'pohon-pink', 'taman', 'kolonade-kiri', 'kolonade-kanan'):
        m = MANIFEST[n]; css += f".dunia .l-{n}{{left:{m['x']/860*100:.3f}%;top:{m['y']/960*100:.3f}%;width:{m['w']/860*100:.3f}%}}\n"
    css += ".dunia .l-bunga-bawah{left:0%;top:66.667%;width:100%}\n"
    open(os.path.join(ROOT, 'css', 'layer.css'), 'w').write(css)
    print('SELESAI')


if __name__ == '__main__':
    main()
