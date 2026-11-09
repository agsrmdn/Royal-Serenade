"""Tekstur kertas krem seamless + titik halus (polka) seperti referensi."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from _lukis import *


def kertas_tile(n=512, seed=3):
    rng = np.random.default_rng(seed)
    def wrapn(s, sg): return gaussian_filter(rng.standard_normal((n, n)), sg, mode='wrap')
    base = np.array([0xF5, 0xEC, 0xCC], np.float32) / 255
    img = np.ones((n, n, 3), np.float32) * base
    b1 = wrapn(0, 60); b1 /= b1.std(); b2 = wrapn(0, 18); b2 /= b2.std(); b3 = wrapn(0, 1.1); b3 /= b3.std()
    # serat kertas
    fib = np.zeros((n, n), np.float32)
    for _ in range(520):
        x, y = rng.integers(0, n, 2); L = rng.integers(8, 26); a = rng.uniform(0, 6.28)
        for t in range(L):
            fib[int(y + np.sin(a) * t) % n, int(x + np.cos(a) * t) % n] += rng.uniform(.4, 1)
    fib = gaussian_filter(fib, .6, mode='wrap')
    k = 1 + .016 * b1 + .014 * b2 + .014 * b3 - .05 * fib
    img = img * k[..., None]
    # tinta warna hangat di tepi blok (bercak foxing halus)
    spots = wrapn(0, 30); spots = np.clip((spots - 1.4) / 1.5, 0, 1)
    img[..., 0] -= .012 * spots; img[..., 2] -= .04 * spots
    # titik polka
    yy, xx = np.mgrid[0:n, 0:n]
    step = 32
    dx = (xx % step) - step / 2; dy = ((yy + (xx // step % 2) * step / 2) % step) - step / 2
    dots = np.exp(-(dx * dx + dy * dy) / (2 * 2.2 ** 2))
    img[..., 0] -= .06 * dots; img[..., 1] -= .075 * dots; img[..., 2] -= .12 * dots
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))


if __name__ == '__main__':
    im = kertas_tile()
    im.save(os.path.join(DIR_LAYER, 'kertas.webp'), 'WEBP', quality=84, method=6)
    print('kertas', os.path.getsize(os.path.join(DIR_LAYER, 'kertas.webp')) // 1024, 'KB')
    t = Image.new('RGB', (1024, 512)); t.paste(im, (0, 0)); t.paste(im, (512, 0)); t.save('/home/claude/kertas_prev.png')
