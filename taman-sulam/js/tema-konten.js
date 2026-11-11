/* =====================================================================
   tema-konten.js - DATA KLIEN (edit file ini saja untuk tiap pesanan)
   ===================================================================== */
window.WC_KONTEN = {
  // EDIT KLIEN: judul tab, panggilan, inisial monogram
  judulHalaman: "The Wedding of Andi & Rani",
  panggilan: { pria: "Andi", wanita: "Rani" },
  monogram: { a: "A", b: "R" },
  labelPembuka: "The Wedding Of", // teks kecil di atas nama (boleh "The Wedding of")
  hashtag: "#AndiRaniMenikah", // tampil di kartu oval pembuka
  website: "Andi-Rani.weddingcode.id", // EDIT KLIEN: alamat undangan
  judulSapa: "We Are Getting Married!",
  acaraTeks:
    "Dengan penuh syukur, kami mengundang Anda untuk hadir dan berbagi kebahagiaan di hari istimewa kami.",

  // EDIT KLIEN: waktu utama (countdown) & teks tanggal
  tanggalUtama: "2026-12-31T08:00:00+07:00",
  tanggalTeks: "Minggu, 31 Desember 2026",
  tanggalPendek: "31 . 12 . 2026",

  // EDIT KLIEN: foto tunggal (WebP/JPG <150KB). Dipakai di kartu & panel desktop
  foto: {
    pasangan:
      "https://plus.unsplash.com/premium_photo-1664530452485-72ddb634c24c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // Pose prewedding berdua berbusana pengantin
    pria: "https://plus.unsplash.com/premium_photo-1664530452451-6f37c146af23?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // Potret solo pengantin pria (jas formal pengantin)
    wanita:
      "https://images.pexels.com/photos/4334411/pexels-photo-4334411.jpeg", // Potret solo pengantin wanita (gaun pengantin anggun)
  },

  // EDIT KLIEN: SLIDESHOW latar section (isi 3-6 foto per grup; satu foto pun boleh)
  slideshow: {
    acara: [
      "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
      "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
      "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 3
    ],
    hadiah: [
      "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
      "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
      "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 3
    ],
    rsvp: [
      "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
      "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
      "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 3
    ],
    sisi: [
      // Panel kiri versi desktop
      "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
      "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
      "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 3
    ],
  },

  musik: "assets/musik-demo.mp3", // EDIT KLIEN: mp3 <2MB. CONTOH = musik-demo.mp3 (ganti). Kosong = tombol musik hilang

  pria: {
    nama: "Andi Rahman, S.T.",
    ortu: "Putra dari Bapak Rahman Hakim & Ibu Siti Aminah",
    instagram: "https://instagram.com/",
  },
  wanita: {
    nama: "Rani Azzahra, S.Pd.",
    ortu: "Putri dari Bapak Ahmad Fauzi & Ibu Nurhayati",
    instagram: "https://instagram.com/",
  },

  salam: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
  sambutan:
    "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan resepsi pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  kutipan: {
    teks: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, agar kamu merasa tenteram kepadanya.",
    sumber: "QS. Ar-Rum: 21",
  },

  // EDIT KLIEN: acara (tambah/hapus objek)
  acara: [
    {
      nama: "Akad Nikah",
      tanggal: "Kamis, 31 Desember 2026",
      jam: "08.00 - 10.00 WIB",
      tempat: "Pendopo Taman Sari",
      alamat: "Jl. Kaliurang Km 7, Sleman, Yogyakarta",
      maps: "https://maps.google.com/?q=Sleman+Yogyakarta",
    },
    {
      nama: "Resepsi",
      tanggal: "Kamis, 31 Desember 2026",
      jam: "11.00 - 14.00 WIB",
      tempat: "Pendopo Taman Sari",
      alamat: "Jl. Kaliurang Km 7, Sleman, Yogyakarta",
      maps: "https://maps.google.com/?q=Sleman+Yogyakarta",
    },
  ],

  // EDIT KLIEN: galeri. Pola kolase: 3 foto berjajar -> 1 foto lebar -> grid 3 kolom -> 1 lebar -> dst.
  // Item boleh berupa teks (foto) atau { video: "file.mp4", poster: "poster.jpg" }.
  galeri: [
    "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
    "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 3
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
    "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
    "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    "https://plus.unsplash.com/premium_photo-1664530452597-fc48cc4a4e45?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 1
    "https://plus.unsplash.com/premium_photo-1664530452584-9c600fe6f0ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D", // 2
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    "https://plus.unsplash.com/premium_photo-1664530452652-fa1a54f353e1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
  ],

  // ===== Save The Date: pakai tanggalUtama + kutipan di atas =====

  // EDIT KLIEN: Live Streaming (aktif:false = seksi disembunyikan)
  live: {
    aktif: true,
    judul: "Live Streaming",
    teks: "Bagi keluarga dan sahabat yang berhalangan hadir, silakan menyaksikan prosesi pernikahan kami secara langsung melalui tautan berikut.",
    tombol: "Live Instagram",
    tautan: "https://instagram.com/",
  },

  // EDIT KLIEN: Love Story (tambah/hapus; foto portrait)
  cerita: [
    {
      judul: "Awal Bertemu",
      teks: "Kami dipertemukan di sebuah acara kampus. Dari obrolan sederhana, tumbuh rasa nyaman yang perlahan menjadi cinta.",
      foto: "https://plus.unsplash.com/premium_photo-1664528596082-17aa36ce7c73?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    },
    {
      judul: "Lamaran",
      teks: "Dengan restu kedua keluarga, Andi datang membawa niat baik dan melamar Rani dalam suasana hangat penuh doa.",
      foto: "https://plus.unsplash.com/premium_photo-1664528596079-992a1885d0ee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    },
    {
      judul: "Acara Pernikahan",
      teks: "Dengan ridho Allah SWT, kami melangkah ke jenjang pernikahan dan berharap Anda hadir berbagi bahagia.",
      foto: "https://plus.unsplash.com/premium_photo-1664528596047-4ee5f0e982a1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    },
  ],

  // EDIT KLIEN: Wedding Gift (kartu rekening bergaya kartu debit + kartu alamat; tanpa form)
  hadiah: {
    judul: "Wedding Gift",
    teks: "Doa restu Anda adalah hadiah terindah. Bila berkenan berbagi tanda kasih, dapat melalui rekening atau alamat berikut.",
    rekening: [
      { bank: "BCA", nomor: "1234567890", atasNama: "Andi Rahman" },
      {
        bank: "Dana / e-wallet",
        nomor: "081234567890",
        atasNama: "Rani Azzahra",
      },
    ],
    alamat: {
      penerima: "Rani Azzahra",
      teks: "Jl. Kaliurang Km 7 No. 12, Sleman, Yogyakarta 55581",
      telp: "0812-3456-7890",
    },
  },

  // EDIT KLIEN: footer (kosongkan tautan yang tidak dipakai)
  footer: {
    instagram:
      "https://www.instagram.com/_weddingcode?xtok=MXRvMjFnNHc5MDQ1ZQ==",
    whatsapp: "https://wa.me/6283821047512",
    tautan: "https://wedding-code-orpin.vercel.app/",
  },
  penutup:
    "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Wassalamu'alaikum Warahmatullahi Wabarakatuh.",
};
