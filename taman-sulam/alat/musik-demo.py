#!/usr/bin/env python3
"""Membuat musik latar CONTOH (loop 40 dtk, lonceng lembut bernuansa gamelan) -> assets/musik-demo.mp3
Hanya placeholder agar tombol musik bisa diuji. Ganti dengan musik klien (tema-konten.js: musik)."""
import numpy as np, subprocess, os, wave
from scipy.signal import fftconvolve
SR = 32000; DUR = 40; TAIL = 5
rng = np.random.default_rng(11)
n = (DUR + TAIL) * SR
t = np.arange(n) / SR
out = np.zeros(n)
rasio = [1, 9/8, 6/5, 3/2, 8/5]                          # tangga nada lima nada (nuansa pelog/minor)
nada = [220 * r * o for o in (1, 2) for r in rasio]
def lonceng(f, dur=6.0):
    tt = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(tt)
    for r, a, d in ((1, 1, 3.4), (2.0, .45, 2.2), (2.76, .26, 1.3), (5.4, .1, .6)):
        s += a * np.sin(2 * np.pi * f * r * tt + rng.uniform(0, 6.28)) * np.exp(-tt / d)
    s *= np.minimum(1, tt / .006)
    return s
# melodi mengalir pelan (random walk pada tangga nada)
idx = 3; waktu = 0.5
while waktu < DUR:
    idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(nada) - 1))
    amp = rng.uniform(.5, 1.0) * (1.0 if (int(waktu / 1.2) % 4 == 0) else .8)
    b = lonceng(nada[idx]) * amp
    i0 = int(waktu * SR); out[i0:i0 + len(b)] += b[:max(0, n - i0)] if i0 + len(b) > n else b
    if rng.random() < .35:                               # bunyi rendah penopang
        b2 = lonceng(nada[idx] / 2, 7.0) * amp * .55; j = i0 + int(.02 * SR); out[j:j + len(b2)] += b2[:max(0, n - j)] if j + len(b2) > n else b2
    waktu += rng.choice([1.2, 1.6, 2.0, 2.4])
# pad lembut
for f, a in ((110, .05), (165, .035), (220, .025)):
    out += a * np.sin(2 * np.pi * f * t) * (.7 + .3 * np.sin(2 * np.pi * .07 * t + f))
# gema (reverb) + gema tunda
ir = rng.standard_normal(int(2.4 * SR)) * np.exp(-np.arange(int(2.4 * SR)) / (SR * .55)); ir /= np.abs(ir).sum() * .06
wet = fftconvolve(out, ir)[:n]
x = out * .62 + wet * .55
d = int(.52 * SR); x[d:] += .28 * x[:-d]
# loop mulus: lipat ekor ke awal
loop = x[:DUR * SR].copy(); ekor = x[DUR * SR:DUR * SR + TAIL * SR]; loop[:len(ekor)] += ekor
loop -= loop.mean(); loop *= .5 / np.abs(loop).max()
# stereo ringan
kanan = np.roll(loop, int(.011 * SR)) * .92
st = np.stack([loop, kanan], 1)
pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
wav = '/tmp/musik-demo.wav'
with wave.open(wav, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'musik-demo.mp3')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-codec:a', 'libmp3lame', '-b:a', '80k', dest], check=True)
print('selesai', os.path.getsize(dest) // 1024, 'KB | puncak %.2f | RMS %.3f' % (np.abs(loop).max(), np.sqrt((loop ** 2).mean())))
