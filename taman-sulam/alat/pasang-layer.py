#!/usr/bin/env python3
"""
PASANG LAPISAN BARU (hasil AI / ilustrator) ke tema Taman Sulam.

Cara pakai:
  1. Simpan gambar di folder  masuk/  dengan NAMA = nama lapisan, mis.  masuk/taman.png , masuk/bunga-bawah.jpg
     (nama & ukuran slot: lihat assets/layer-manifest.json atau PANDUAN-TEMA.md)
  2. python3 alat/pasang-layer.py              -> pasang semua file di masuk/
     python3 alat/pasang-layer.py --pratinjau  -> juga simpan pratinjau gabungan adegan (pratinjau.png)
     python3 alat/pasang-layer.py --toleransi 30 --bg "#FFFFFF"   -> atur penghapusan latar
Yang dilakukan: hapus latar polos (putih/warna seragam) bila gambar belum transparan, pas-kan ke ukuran slot
(potong dari tengah bila rasio beda), haluskan tepi, simpan WebP ke assets/layer/ (file lama dicadangkan di
assets/layer/_cadangan/). Kode situs TIDAK perlu diubah.
"""
import sys, os, json, shutil, argparse
import numpy as np
import cv2
from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LAYER = os.path.join(ROOT, 'assets', 'layer')
MANI = json.load(open(os.path.join(ROOT, 'assets', 'layer-manifest.json')))
URUT = ['gunung', 'pohon-pink', 'taman', 'kolonade-kiri', 'kolonade-kanan', 'bunga-bawah']


def hapus_latar(im, bg=None, tol=24):
    a = np.array(im.convert('RGBA'))
    if a[..., 3].min() < 250:                      # sudah transparan
        return Image.fromarray(a, 'RGBA')
    rgb = np.ascontiguousarray(a[..., :3]); h, w = rgb.shape[:2]
    if bg is None:
        e = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]); bg = np.median(e, 0)
    else:
        bg = np.array([int(bg[i:i + 2], 16) for i in (1, 3, 5)])
    dist = np.abs(rgb.astype(np.int16) - bg).max(-1)
    mask_bg = (dist <= tol).astype(np.uint8)
    # hanya latar yang terhubung ke tepi (isi bunga putih tidak ikut terhapus)
    n, lab = cv2.connectedComponents(mask_bg, connectivity=4)
    tepi = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    latar = np.isin(lab, list(tepi)) & (mask_bg == 1)
    alpha = np.where(latar, 0, 255).astype(np.uint8)
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8), iterations=1)       # buang halo putih
    alpha = cv2.GaussianBlur(alpha, (0, 0), .9)
    a[..., 3] = alpha
    return Image.fromarray(a, 'RGBA')


def pasang(path, args):
    nama = os.path.splitext(os.path.basename(path))[0].lower()
    if nama not in MANI:
        print(f'  LEWATI {os.path.basename(path)}: nama tidak dikenal. Pilihan: {", ".join(sorted(MANI))}'); return False
    m = MANI[nama]; im = Image.open(path)
    im = hapus_latar(im, args.bg, args.toleransi)
    asli = im.size
    im = ImageOps.fit(im, (m['w'], m['h']), Image.LANCZOS, centering=(.5, .5))
    out = os.path.join(args.keluar, nama + '.webp'); os.makedirs(args.keluar, exist_ok=True)
    if os.path.exists(out) and args.keluar == LAYER:
        cad = os.path.join(LAYER, '_cadangan'); os.makedirs(cad, exist_ok=True); shutil.copy2(out, os.path.join(cad, nama + '.webp'))
    im.save(out, 'WEBP', quality=args.kualitas, method=6)
    print(f'  OK {nama}: {asli[0]}x{asli[1]} -> {m["w"]}x{m["h"]}  ({os.path.getsize(out)//1024} KB)')
    return True


def pratinjau(args):
    cv = Image.new('RGBA', (860, 960), (243, 234, 202, 255))
    for n in URUT:
        p = os.path.join(args.keluar, n + '.webp')
        if os.path.exists(p):
            m = MANI[n]; cv.alpha_composite(Image.open(p).convert('RGBA'), (m['x'], m['y']))
    cv.convert('RGB').save(os.path.join(ROOT, 'pratinjau.png')); print('  pratinjau.png disimpan')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--masuk', default=os.path.join(ROOT, 'masuk')); ap.add_argument('--keluar', default=LAYER)
    ap.add_argument('--toleransi', type=int, default=24); ap.add_argument('--bg', default=None); ap.add_argument('--kualitas', type=int, default=84)
    ap.add_argument('--pratinjau', action='store_true')
    args = ap.parse_args()
    files = [os.path.join(args.masuk, f) for f in sorted(os.listdir(args.masuk)) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if not files: print(f'Tidak ada gambar di {args.masuk}'); sys.exit(0)
    print(f'Memasang {len(files)} gambar...')
    ok = sum(pasang(f, args) for f in files)
    if args.pratinjau: pratinjau(args)
    print(f'Selesai: {ok}/{len(files)} terpasang.')
