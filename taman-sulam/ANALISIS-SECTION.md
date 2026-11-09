# ANALISIS VIDEO REFERENSI → IMPLEMENTASI TAMAN SULAM

Referensi: rekaman layar undangan adat Jawa (±48 detik, 13 bagian). Urutan **sama persis**; desain memakai tema Taman Sulam.

| # | Section di video | Bentuk di video | Implementasi kita (`index.html`) | Reveal |
|---|---|---|---|---|
| 0 | Cover "Kepada Yth…" + tombol Buka | segel gunungan membuka | `#pintu` (dua panel lobus membuka) | pintu geser 2,3 dtk |
| 1 | Hero pemandangan → **kartu oval tinggi melayang** (The Wedding Of, foto lengkung, nama, tanggal, hashtag, situs); kupu-kupu di bawahnya | oval naik menutup adegan | `.cover` (taman masuk perlahan, monogram, nama) → `#oval-hero` naik saat gulir; kupu-kupu putih hinggap di `[data-kupu]` | oval naik mengikuti gulir |
| 2 | **We Are Getting Married!** + paragraf + foto oval mempelai wanita, nama, orang tua, Instagram | kartu putih bersudut | `#sek-sapa` kartu 1 | judul "tertulis", item satu-satu |
| 3 | "&" lalu mempelai pria (kartu sama) | kartu kedua | `#sek-sapa` "&" + kartu 2 | "&" mekar |
| 4 | **Save The Date**: kutipan, hitung mundur, tombol; ditutup ornamen pemandangan | kertas polos | `#sek-tanggal` + `vinyet-taman.webp` | zoom pada hitung mundur |
| 5 | **Wedding Event**: latar foto + **kartu lengkung melayang** Akad & Resepsi | slideshow + lengkung | `#sek-acara` (`.lk`, bingkai marmer, melayang) | kartu naik bergantian |
| 6 | **Live Streaming** + tombol | kertas | `#sek-live` (otomatis hilang bila `live.aktif:false`) | ikon mekar, teks naik |
| 7 | **Galeri Foto**: 3 berjajar, 1 lebar (video), grid kecil | kolase | `#sek-galeri` (`renderGaleri`, mendukung video) | tiap foto masuk satu-satu |
| 8 | **Love Story**: latar bergambar **tetap**, garis waktu hati, kartu bergantian | latar pinned | `#sek-cerita` (`position:sticky`, hati berjalan mengikuti gulir) | kartu masuk dari kanan |
| 9 | **Wedding Gift**: rekening + Copy, alamat kado | slideshow | `#sek-hadiah`: **kartu bergaya kartu debit** (chip, nirkontak, nomor, atas nama) + kartu alamat, **tanpa kolom isian** | naik bergantian, melayang |
| 10 | ~~Gift Confirm~~ | form | **dihapus sesuai permintaan** (hanya kartu) | - |
| 11 | **RSVP & Ucapan**: kartu kaca buram di atas foto | frosted glass | `#sek-rsvp` (`.kaca`, latar slideshow di-blur) + daftar ucapan | naik |
| 12 | **Terima Kasih** + ornamen + footer sosial | kertas | `#sek-penutup` (vinyet + `.kaki`) | nama "tertulis" |

## Gaya tiap section
- **Kartu/oval melayang:** hero oval, kartu mempelai, kartu lengkung Acara/Gift. Bingkai marmer (`marmer.webp`), melayang pelan (`.melayang`).
- **Latar slideshow foto klien:** Wedding Event, Wedding Gift, RSVP (crossfade + Ken Burns + parallax). Kartu selalu di depan.
- **Latar kertas:** Sapa, Save The Date, Live, Galeri, Penutup. **Latar tetap:** Love Story.

## Reveal satu-per-satu
Atribut `data-rv="naik|zoom|mekar|kiri|kanan|tulis"` (+ `data-d` jeda tambahan). `core.js → initReveal()` memakai IntersectionObserver; item yang masuk bersamaan diberi jeda 0,26 dtk berurutan, transisi ±1,7 dtk. Terukur: foto kolase muncul bergantian pada 0,4 / 0,8 / 1,2 / 1,6 dtk.

## Kupu-kupu & merpati putih (terbang)
`js/terbang.js`. Aset: `kupu-sayap-kiri/kanan.svg` + `kupu-badan.svg` (sayap mengepak 3D `rotateY`), `merpati-badan/sayap-dekat/sayap-jauh.svg` (sayap berpivot di bahu).
- **Kupu-kupu (3 di HP, 4 di desktop) hanya menemani bagian awal (hero/oval):** terbang berkelok, saling menjauh, mendekati kartu oval (`data-kupu`). Begitu tamu menggulir melewati hero, mereka terbang keluar layar lalu dihapus; di section biasa **tidak ada kupu-kupu**. Bila tamu kembali ke atas, mereka muncul lagi.
- **Merpati:** di hero rombongan 1-3 ekor tiap 14-24 dtk; di section biasa **hanya sesekali** (1-2 ekor, tiap 38-62 dtk). Ketinggian & arah acak; kepak beberapa kali lalu meluncur.
- Mati otomatis untuk `prefers-reduced-motion`; berhenti saat tab tersembunyi. Atur jumlah/interval di bagian atas `terbang.js`.
