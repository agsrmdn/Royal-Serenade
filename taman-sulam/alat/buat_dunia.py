from _lukis import *
import lapis_taman as T

def main():
    R = Perender()
    try:
        b, d = T.gunung();       simpan_layer(R, 'gunung', 0, 0, 860, 340, b, d, seed=1, grain=.04, pig=.08, edge=.8)
        b, d = T.pohon_pink();   simpan_layer(R, 'pohon-pink', 0, 200, 860, 380, b, d, seed=2, grain=.05, pig=.10, edge=1.2)
        b, d = T.kolonade('kiri');  simpan_layer(R, 'kolonade-kiri', 0, 320, 430, 340, b, d, seed=3, grain=.04, pig=.07, edge=.6)
        b, d = T.kolonade('kanan'); simpan_layer(R, 'kolonade-kanan', 430, 320, 430, 340, b, d, seed=4, grain=.04, pig=.07, edge=.6)
        b, d = T.taman();        simpan_layer(R, 'taman', 0, 420, 860, 480, b, d, seed=5, grain=.045, pig=.09, edge=.9)
    finally:
        R.tutup()
    json.dump(MANIFEST, open(os.path.join(ROOT, 'assets', 'layer-manifest.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
