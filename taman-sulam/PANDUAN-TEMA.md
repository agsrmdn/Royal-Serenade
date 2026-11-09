# PANDUAN TEMA: TAMAN SULAM (taman cat air, sulam silang pink, emas)

## 1. Analisis referensi (Amati)
Referensi: video undangan ±20 detik, intro ±12 detik.

| Detik | Yang terjadi | Cara kita membuatnya |
|---|---|---|
| 0-1,5 | Dua panel krem bertepi **lobus bergelombang**: titik halus, motif **sulam silang pink**, garis bunga peoni pink, garis ganda **sage** + bintang sage di lekuk. Membuka ke samping | `pintu-kiri/kanan.webp`, transisi `translateX` 2,3 dtk |
| 1,5-4 | Taman: gunung berkabut, pohon bunga pink, **kolonade bertiang** perspektif, parterre, **air mancur bertingkat**. Kamera masuk perlahan | 5 lapisan dunia, masing-masing `scale` berbeda (parallax dolly) 12,5 dtk |
| 3-7,5 | **Monogram emas** muncul lalu memudar. Motif sulam melayang | `.monogram` foil emas (gradien teks bergerak) |
| 4,3-6 | Bingkai depan naik: dedaunan zaitun atas, **pita sulam** pink, bunga raya & peoni bawah, bunga pink samping | animasi masuk dari tepi, delay bertahap |
| 7,5-11 | "Walimatulurus" lalu nama **script emas** tertulis kiri-ke-kanan | `clip-path` + foil emas |
| setelah | Section kertas krem + garis bunga pink + bingkai lobus sage | `.sec`, `.kartu` |

> **Urutan section final (v2)** mengikuti video undangan adat: lihat `ANALISIS-SECTION.md` (peta lengkap video → kode).

## 2. Yang sudah dibuat sesuai permintaan
1. **Intro persis alurnya**: pintu → taman masuk perlahan → monogram → nama. Scroll terkunci sampai selesai (±12 dtk), ada tombol **Lewati**.
2. **Ornamen seragam di semua section**: dedaunan zaitun + pita sulam di tiap awal section, garis bunga pink di tepi section kertas, hamparan bunga di bawah, kartu berlekuk sage. (Dipasang otomatis oleh `dekor()` di `tema-taman-sulam.js`.)
3. **Selang-seling latar**: *Polos* (kertas) ↔ **Foto slideshow** (crossfade + Ken Burns, kartu kertas di depan). Urutan: Salam(P) → Pria(F) → Wanita(P) → Acara(F) → Galeri(P) → Amplop+RSVP(F) → Penutup(P).
4. **Galeri**: foto masuk **satu per satu** (stagger, naik + terbuka + zoom-out halus), klik = lightbox dengan prev/next.
5. **Desktop (≥900px)**: tampilan HP digeser ke **kanan**; sisi kiri = adegan taman + foto (slideshow) dalam lengkung emas + nama pasangan + tanggal.

## 3. Struktur
```
taman-sulam/
├─ index.html  admin.html  PANDUAN-TEMA.md
├─ alat/buat-aset.py      <- bangun SEMUA aset: python3 alat/buat-aset.py
│  └ _lukis.py (palet, mesin tekstur cat air) kertas.py lapis_taman.py lapis_bunga.py lapis_kertas.py
├─ assets/layer/*.webp    lapisan lukisan (13 file) + layer-manifest.json (ukuran & posisi)
├─ assets/svg/*.svg       sulam-1..4, pita-sulam, garis-bunga-kiri/kanan, bintang-sage, pembatas-sulam
├─ assets/foto-*.svg      PLACEHOLDER foto (ganti foto klien)
├─ css/style.css  css/layer.css (otomatis)
└─ js/ konfigurasi.js  tema-konten.js (DATA KLIEN)  core.js  tema-taman-sulam.js
```

## 4. Alur kerja per klien (±10 menit)
1. Salin folder. Edit **`js/tema-konten.js`**: panggilan, `monogram` (2 huruf), tanggal ISO `+07:00`, acara, rekening, galeri.
2. **Slideshow**: isi `slideshow.pria / acara / rsvp / sisi` dengan 3-6 foto klien (WebP ≤150 KB, portrait 3:4). Satu foto pun boleh.
3. `js/konfigurasi.js`: URL + anon key Supabase, `UNDANGAN_ID` unik. SQL tabel: sama seperti tema sebelumnya (tabel `ucapan` + RLS insert & select).
4. `index.html`: `og:image` ganti JPG/WebP absolut (WhatsApp tidak menampilkan SVG). Tes `index.html?to=Nama+Tamu`.
5. `labelPembuka` bisa "Walimatulurus" atau "The Wedding of".

## 5. KONTRAK LAPISAN (cara menaikkan kualitas tanpa mengubah kode)
Setiap lapisan adalah **WebP transparan dengan nama & ukuran tetap**. Timpa file dengan versi lebih detail (ilustrator/AI) berukuran piksel sama dan posisinya otomatis pas.

| File | Piksel | Isi |
|---|---|---|
| `gunung.webp` | 860×340 | pegunungan berkabut, tepi atas lembut |
| `pohon-pink.webp` | 860×380 | barisan pohon bunga pink |
| `kolonade-kiri/kanan.webp` | 430×340 | galeri berpilar perspektif satu titik (cermin) |
| `taman.webp` | 860×480 | parterre, jalan, air mancur bertingkat, semak putih |
| `bunga-bawah.webp` | 860×320 | hamparan raya, peoni, lavender, kupu-kupu |
| `dedaunan-kiri/kanan.webp` | 430×520 | dahan zaitun menjuntai dari sudut atas |
| `bunga-samping-kiri/kanan.webp` | 260×460 | bunga pink tegak di tepi |
| `pintu-kiri/kanan.webp` | 430×1500 | panel pintu, **tepi dalam bergelombang di sisi kanan (kiri)/kiri (kanan)** |
| `kertas.webp` | 512×512 | kertas krem **seamless** + titik halus |

### Prompt untuk pembuat gambar AI (contoh, sesuaikan)
- **Taman (satu gambar utuh lalu dipotong per lapisan):** *"Symmetrical one-point perspective formal Mughal-Andalusian garden, two arcaded cream-and-gold pavilions flanking a central path, tiered stone fountain, boxwood parterre with white flowers, pink flowering trees behind, misty mountains, warm cream sky, soft gouache watercolor, aged paper grain, portrait 860x960, no people, no text."*
- **Bunga bawah:** *"Dense foreground flower bed border, magenta hibiscus and pink peonies, lavender sprigs, deep green leaves, orange butterfly, watercolor botanical, flat horizontal bottom edge, isolated on plain white, 860x320."*
- **Dedaunan:** *"Hanging olive branches from top-left corner, muted olive and sage leaves, watercolor, isolated on white, 430x520."*
- Hapus latar putih (remove.bg / Photoshop) → simpan WebP transparan kualitas ~82.

### Mencari aset berlisensi aman (sebagai bahan/tekstur)
- **Metropolitan Museum Open Access** (CC0, boleh komersial): metmuseum.org/art/collection → filter *Open Access*; cari "botanical", "peony", "garden plan".
- **Smithsonian Open Access** (CC0 per item; periksa label CC0 di tiap item).
- **Biodiversity Heritage Library / Wikimedia Commons**: ilustrasi botani domain publik (cek keterangan lisensi).
- **Rawpixel (koleksi Public Domain)**: hanya yang berlabel *Public Domain / CC0*.
> Selalu cek lisensi **per item** sebelum dipakai komersial, dan jangan memakai ulang gambar berhak cipta dari undangan pihak lain.

## 6. Ganti warna / bentuk
- Palet CSS: `:root` di `css/style.css`. Palet lukisan: dict `P` di `alat/_lukis.py`, lalu jalankan `python3 alat/buat-aset.py`.
- Motif sulam: `grid_motif()` di `alat/lapis_kertas.py` (tambah pola = tambah cabang `kind`).
- Tema warna lain (mis. biru-emas, hijau-emas): ganti `P` + warna `PINK`/`SAGE` di `lapis_kertas.py` dan palet pohon di `lapis_taman.py`.

## 7. Performa
- Bobot muat awal ±1,1 MB (pintu 250 KB, taman ±330 KB, dedaunan ±125 KB, bunga ±100 KB; foto klien di luar angka ini). Lapisan WebP sudah terkompresi; SVG kecil.
- Animasi memakai `transform/scale/translate/opacity` (GPU). `prefers-reduced-motion` melewati intro.
- Slideshow berhenti saat section keluar layar.

## 8. QA sebelum kirim
- [ ] iPhone Safari & Chrome Android (360-430px); tanpa scroll horizontal
- [ ] Pintu terbuka, intro ±12 dtk, tombol Lewati, scroll terkunci sebelum selesai
- [ ] Musik jalan setelah ketuk "Buka Undangan"
- [ ] Slideshow berganti, galeri masuk satu per satu, lightbox prev/next
- [ ] Desktop 1280-1920px: HP di kanan, panel kiri tidak menutupi
- [ ] Countdown, RSVP ke Supabase, ucapan muncul; `og:image` absolut

## 9. Catatan jujur
- **Kualitas lukisan:** referensi adalah lukisan cat air detail tinggi. Lapisan kita dibuat prosedural + tekstur cat air/kertas: komposisi, palet, perspektif, dan elemennya mengikuti referensi, tetapi **tidak identik piksel-demi-piksel** dan detailnya lebih sederhana (terutama pohon, kolonade, bunga). Jalur peningkatan: timpa lapisan sesuai bagian 5.
- **Font:** nama script (Pinyon Script), Cinzel, Cormorant dimuat dari Google Fonts. Tanpa internet tampil font cadangan (serif). Untuk performa & kepastian, host sendiri `woff2` (lisensi OFL).
- **Pengujian:** saya uji di Chromium (emulasi HP 390×844 dan desktop 1440×900). **Belum diuji di iPhone Safari/Android asli**; efek `mask`, `container query (cqw)`, dan properti `scale/translate` perlu dicek di Safari ≥16.
- Foto, musik, dan kredensial Supabase masih placeholder.

## 10. HIDUP: apa saja yang bergerak (v1.1)
| Efek | Cara | Catatan |
|---|---|---|
| Angin pada pohon, dedaunan, bunga | `skew/rotate` lambat tiap lapisan (`angin`, `goyang`, `napas`) | terus berjalan, juga di section |
| Kabut berawan | `kabut.webp` digeser perlahan di antara gunung & pohon | |
| Berkas cahaya | gradien kerucut hangat, denyut pelan | tanpa blur/blend (hemat GPU) |
| Kupu-kupu terbang | 3 kupu SVG, lintasan melengkung (`offset-path`) + kepak | disembunyikan otomatis bila browser tidak mendukung |
| Kelopak & debu cahaya | canvas `js/hidup.js` | mulai halus setelah ±6,5 dtk |
| Air mancur | percikan + riak di canvas, posisi dihitung dari lapisan `taman` | otomatis mengikuti jika `taman.webp` diganti |
| Parallax | pointer (desktop), kemiringan HP (Android), gerak lembut otomatis bila diam; juga mengikuti gulir | jauh bergerak sedikit, dekat banyak |
Semua dimatikan oleh `prefers-reduced-motion`; canvas berhenti saat cover di luar layar atau tab tersembunyi.

## 11. MEMASANG ASET BARU (jalur ke kualitas "persis referensi")
Kualitas lukisan paling menentukan rasa "hidup". Jalur tercepat:
1. Buat tiap lapisan dengan AI/ilustrator memakai prompt di bagian 5, **latar putih polos**, resolusi 2x.
2. Simpan di folder `masuk/` dengan nama lapisan (daftar di `masuk/BACA-SAYA.txt`).
3. Jalankan `python3 alat/pasang-layer.py --pratinjau` → latar dihapus, ukuran dipaskan, WebP terpasang, file lama dicadangkan di `assets/layer/_cadangan/`.
4. Buka `index.html`: parallax, angin, dan percikan air mancur langsung memakai lapisan baru.
Catatan: rasio gambar yang beda akan dipotong dari tengah; atur `--toleransi` (default 24) bila latar tidak benar-benar putih.

## 12. v2: SECTION LENGKAP (urutan video)
Cover → Hero oval → We Are Getting Married + mempelai → Save The Date → Wedding Event → Live Streaming → Galeri Foto → Love Story → Wedding Gift + Gift Confirm → RSVP & Ucapan → Terima Kasih.

**Isi data:** semua di `js/tema-konten.js`: `judulSapa`, `hashtag`, `website`, `acara[]`, `live{}`, `cerita[]` (tambah item = tambah kartu timeline), `galeri[]` (pola kolase otomatis, item boleh `{video, poster}`), `hadiah{rekening, alamat, whatsapp}`, `footer{}`, `slideshow{acara,hadiah,rsvp,sisi}`.
**Ubah urutan / hapus section:** tiap `<section>` di `index.html` berdiri sendiri; pindahkan atau hapus blok-nya. Latar selang-seling mengikuti kelas `sec--polos` / `sec--foto`. Live Streaming hilang dengan `live.aktif:false`.
**Tambah acara:** tambah objek di `acara[]` (ikon: `cincin`, `resepsi`, `hadiah`, `hati`, dll di `assets/svg/ikon-*.svg`).

## 13. Catatan jujur v2
- **Kupu-kupu & merpati** adalah ilustrasi vektor yang dianimasikan (sayap 3D, kepak, gerak berkelok): terlihat realistis dan ringan, tetapi bukan foto/video. Untuk tampilan sinematik penuh, bisa diganti video alpha (WebM) atau sprite foto.
- **Gift Confirm** membuka WhatsApp dengan pesan terisi. Teks `wa.me` **tidak bisa melampirkan file**, jadi tamu diminta melampirkan bukti transfer sendiri di chat (sudah ada petunjuknya). Upload langsung butuh Supabase Storage (belum dibuat).
- **Foto, video galeri, musik, nomor WhatsApp, rekening** masih contoh: ganti di `tema-konten.js`.
- Diuji di Chromium (HP 390×844 & 360×640, desktop 1440×900) tanpa error; **belum diuji di iPhone Safari/Android asli** (efek 3D sayap, `backdrop-filter`, `offset-path`, `sticky`).
- Bobot muat awal ±0,8 MB + ±0,2 MB lazy; JS+CSS ±29 KB gzip.

## 14. Musik & refresh (v2.1)
**Tombol musik** (medali sulam kecil, pojok kanan bawah): muncul setelah tamu menekan "Buka Undangan" (sekaligus musik mulai, karena browser hanya mengizinkan suara setelah ketukan). Hidup = bunga berputar + cincin manik + ekualiser mini; mati = bunga memudar + garis coret. Label "Musik hidup/mati" muncul sebentar, dan cincin berdenyut 5 detik di awal sebagai petunjuk. Volume naik/turun halus.
- **Pilihan tamu diingat** (`localStorage: wc_musik`): bila tamu mematikan musik, setelah refresh musik tidak otomatis menyala lagi.
- **Ganti musik:** `musik: "assets/musik-klien.mp3"` di `js/tema-konten.js` (mp3 <2 MB, loop mulus lebih baik). `musik: ""` = tombol hilang.
- **`assets/musik-demo.mp3` hanya placeholder** (dibuat `alat/musik-demo.py`; lonceng lembut 40 dtk). Hapus/ganti sebelum dikirim ke klien.
- Musik berhenti saat tab disembunyikan dan lanjut saat kembali (bila sedang menyala).

**Refresh selalu dari cover:** pemulihan posisi gulir browser dimatikan (`history.scrollRestoration="manual"`), posisi di-reset ke atas saat muat, dan halaman dari cache "kembali/maju" dimuat ulang. Intro (pintu) selalu tampil dari awal.

## 15. v2.2: Kupu-kupu hanya di awal, Gift = kartu debit
- **Terbang:** kupu-kupu hanya di hero; di section biasa hanya merpati sesekali (pengaturan: `JUMLAH_KUPU` dan interval di `js/terbang.js`, fungsi `atur()` dan `rombongan()`).
- **Wedding Gift:** `#sek-hadiah` kini hanya kartu: tiap rekening = kartu debit (bank, chip emas, ikon nirkontak, nomor otomatis dikelompokkan 4 digit, atas nama, ornamen sulam) + tombol **Salin Nomor**; alamat kado = kartu pink + **Salin Alamat**. **Tidak ada kolom isian.** Form Gift Confirm dihapus; `hadiah.whatsapp` tidak dipakai lagi.
- **Ubah data:** `hadiah.rekening[]` (`bank`, `nomor`, `atasNama`) dan `hadiah.alamat` di `js/tema-konten.js`. Tambah rekening = tambah objek, kartu bertambah otomatis (warna selang-seling marmer krem / hijau sage).
