/* =====================================================================
   tema-taman-sulam.js - perilaku KHUSUS tema: isi konten dari WC_KONTEN,
   render daftar (acara, cerita, kolase galeri, hadiah), konfirmasi WhatsApp,
   ornamen seragam tiap section. Tidak berisi data klien.
   ===================================================================== */
(function () {
  "use strict";
  const K = window.WC_KONTEN, { $, $$ } = window.WC;
  const ambil = (o, p) => p.split(".").reduce((a, k) => (a == null ? a : a[k]), o);
  const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const img = (src, cls, alt) => { const i = el("img", cls); i.src = src; i.alt = alt || ""; i.decoding = "async"; return i; };

  function bind() {
    document.title = K.judulHalaman;
    $$("[data-k]").forEach(e => { const v = ambil(K, e.dataset.k); if (v != null) e.textContent = v; });
    $$("[data-k-src]").forEach(e => { const v = ambil(K, e.dataset.kSrc); if (v) e.src = v; });
    $$("[data-k-href]").forEach(e => { const v = ambil(K, e.dataset.kHref); if (v) e.href = v; });
  }

  /* ornamen seragam di tiap section: pohon, pita sulam, garis bunga, hamparan bunga */
  function dekor() {
    $$(".sec").forEach(sec => {
      const polos = sec.classList.contains("sec--polos"), cerita = sec.classList.contains("sec--cerita");
      const put = (tag, cls, src) => { const e = el(tag, "dekor " + cls); if (src) { e.src = src; e.alt = ""; e.loading = "lazy"; e.decoding = "async"; } sec.prepend(e); };
      if (polos) { put("img", "dekor--garis-r", "assets/svg/garis-bunga-kanan.svg"); put("img", "dekor--garis-k", "assets/svg/garis-bunga-kiri.svg"); }
      if (polos && !["sek-sapa", "sek-tanggal", "sek-penutup"].includes(sec.id)) put("img", "dekor--bunga", "assets/layer/bunga-bawah.webp");
      if (!cerita) { put("img", "dekor--ded-r", "assets/layer/dedaunan-kanan.webp"); put("img", "dekor--ded-k", "assets/layer/dedaunan-kiri.webp"); }
      put("div", "dekor--pita");
    });
  }

  /* ---------- Wedding Event: kartu lengkung melayang ---------- */
  function renderAcara() {
    const box = $("#daftar-acara"); if (!box) return;
    const ikon = ["cincin", "resepsi"];
    K.acara.forEach((a, i) => {
      const w = el("article", "lk melayang"); w.dataset.rv = "naik"; w.dataset.d = i ? ".1" : "0";
      const isi = el("div", "lk__isi");
      isi.append(img("assets/svg/ikon-" + (a.ikon || ikon[i % 2]) + ".svg", "lk__ikon"), el("h3", "judul-skrip", a.nama),
        el("p", "lk__tgl", a.tanggal), el("p", "lk__jam", a.jam), img("assets/svg/ikon-pin.svg", "lk__pin"));
      const l = el("p", "lk__lokasi"); l.append(el("b", "", a.tempat), document.createTextNode(a.alamat)); isi.append(l);
      const b = el("a", "btn btn--kecil", "Google Map"); b.href = a.maps; b.target = "_blank"; b.rel = "noopener"; isi.append(b);
      w.append(isi); box.append(w);
    });
  }

  /* ---------- Love Story: timeline hati ---------- */
  function renderCerita() {
    const box = $("#daftar-cerita"); if (!box) return;
    K.cerita.forEach((c, i) => {
      const it = el("div", "cerita-item"); it.dataset.rv = "kanan"; it.dataset.d = ".05";
      const kartu = el("article", "cerita-kartu");
      const f = el("div", "cerita-foto"); f.append(img(c.foto, "", c.judul)); f.style.setProperty("--r", (i % 2 ? 1 : -1) + "deg");
      kartu.append(f, el("h3", "judul-kecil", c.judul), el("p", "", c.teks));
      it.append(el("i", "hati"), kartu); box.append(it);
    });
  }

  /* ---------- Galeri: kolase (3 berjajar -> 1 lebar -> grid 3 -> 1 lebar ...) ---------- */
  function renderGaleri() {
    const box = $("#galeri-kolase"); if (!box) return;
    const list = K.galeri.slice(); let idx = 0;
    const tile = (it, n, cls) => {
      const b = el("button", "kl " + (cls || "")); b.type = "button"; b.dataset.rv = "zoom";
      const src = typeof it === "string" ? it : (it.poster || "");
      if (typeof it === "object" && it.video) { b.dataset.video = it.video; b.append(img(src, "", "Video " + (n + 1)), el("span", "play")); b.classList.add("kl--video"); }
      else { b.dataset.zoom = src; b.append(img(src, "", "Foto galeri " + (n + 1))); }
      b.setAttribute("aria-label", typeof it === "object" && it.video ? "Putar video" : "Perbesar foto " + (n + 1));
      b.firstChild.loading = "lazy"; return b;
    };
    const baris = (n, cls, kemasan) => {
      const grup = list.splice(0, n); if (!grup.length) return false;
      const w = el("div", kemasan);
      grup.forEach(it => w.append(tile(it, idx++, cls)));
      box.append(w); return true;
    };
    while (list.length) {
      baris(3, "kl--tiga", "kl-baris kl-baris--tiga");
      if (!list.length) break; baris(1, "kl--lebar", "kl-baris kl-baris--lebar");
      if (!list.length) break; baris(6, "kl--kecil", "kl-baris kl-baris--grid");
      if (!list.length) break; baris(1, "kl--lebar", "kl-baris kl-baris--lebar");
    }
  }

  /* ---------- Wedding Gift: kartu seperti kartu debit (tanpa kolom isian) ---------- */
  const NFC = '<svg class="kd__nfc" viewBox="0 0 28 28" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 9a7 7 0 0 1 0 10"/><path d="M13 6a12 12 0 0 1 0 16"/><path d="M18 3a17 17 0 0 1 0 22"/></svg>';
  const kelompok = n => { const d = String(n).replace(/\s/g, ""); return /^\d{8,}$/.test(d) ? d.replace(/(\d{4})(?=\d)/g, "$1 ") : n; };
  function renderHadiah() {
    const H = K.hadiah, box = $("#daftar-rekening"), al = $("#alamat-kado"), nama = ["kd--a", "kd--b"];
    (H.rekening || []).forEach((r, i) => {
      const w = el("div", "kd-bungkus"); w.dataset.rv = "naik"; w.dataset.d = i ? ".12" : "0";
      const kartu = el("article", "kd melayang " + nama[i % 2]);
      kartu.innerHTML = '<div class="kd__atas"></div><div class="kd__chip" aria-hidden="true"></div><div class="kd__no"></div><div class="kd__bawah"><div><small>Atas Nama</small><b class="kd__nama"></b></div><img src="assets/svg/sulam-1.svg" alt=""></div>';
      $(".kd__atas", kartu).append(el("span", "kd__bank", r.bank)); $(".kd__atas", kartu).insertAdjacentHTML("beforeend", NFC);
      $(".kd__no", kartu).textContent = kelompok(r.nomor); $(".kd__nama", kartu).textContent = r.atasNama;
      const b = el("button", "btn btn--kecil kd__salin", "Salin Nomor"); b.type = "button"; b.dataset.salin = String(r.nomor).replace(/\s/g, "");
      w.append(kartu, b); box.append(w);
    });
    if (H.alamat && al) {
      const w = el("div", "kd-bungkus"); w.dataset.rv = "naik";
      const kartu = el("article", "kd kd--alamat melayang");
      kartu.innerHTML = '<div class="kd__atas"><span class="kd__bank">Kirim Kado</span><img class="kd__pin" src="assets/svg/ikon-pin.svg" alt=""></div><b class="kd__penerima"></b><p class="kd__teks"></p><small class="kd__telp"></small>';
      $(".kd__penerima", kartu).textContent = H.alamat.penerima; $(".kd__teks", kartu).textContent = H.alamat.teks; $(".kd__telp", kartu).textContent = H.alamat.telp || "";
      const b = el("button", "btn btn--kecil kd__salin", "Salin Alamat"); b.type = "button"; b.dataset.salin = H.alamat.penerima + " - " + H.alamat.teks + (H.alamat.telp ? " (" + H.alamat.telp + ")" : "");
      w.append(kartu, b); al.append(w);
    } else if (al) al.remove();
  }

  function initLive() {
    const L = K.live, sek = $("#sek-live"), a = $("#btn-live");
    if (!L || L.aktif === false) { if (sek) sek.hidden = true; return; }
    if (a) a.href = L.tautan;
  }

  function kalender() {
    const a = $("#btn-kalender"); if (!a) return;
    const t = new Date(K.tanggalUtama); if (isNaN(t)) return;
    const f = d => d.toISOString().replace(/[-:]|\.\d{3}/g, "");
    a.href = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + encodeURIComponent(K.judulHalaman) + "&dates=" + f(t) + "/" + f(new Date(t.getTime() + 6 * 3600e3));
  }

  /* ---------- footer sosial ---------- */
  function footer() {
    const box = $("#kaki-sosial"); if (!box) return;
    const ik = {
      instagram: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor"/></svg>',
      whatsapp: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 20l1.3-4.2A8 8 0 1 1 8.4 18.8z"/><path d="M9 9c0 3 3 6 6 6l1.2-1.4-2-1-.9.8a4 4 0 0 1-2.4-2.4l.8-.9-1-2z" fill="currentColor" stroke="none"/></svg>',
      tautan: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3A4 4 0 0 0 11 18.7l1-1"/></svg>'
    };
    Object.keys(ik).forEach(k => { const u = K.footer && K.footer[k]; if (!u) return; const a = el("a"); a.href = u; a.target = "_blank"; a.rel = "noopener"; a.setAttribute("aria-label", k); a.innerHTML = ik[k]; box.append(a); });
  }

  document.addEventListener("DOMContentLoaded", () => {
    bind(); dekor(); renderAcara(); renderCerita(); renderGaleri(); renderHadiah(); initLive(); kalender(); footer();
    WC.initTamu(); WC.initIntro(); WC.musik.init(); WC.initSlideshow(); WC.initScroll();
    WC.initHitung(); WC.initSalin(); WC.initLightbox(); WC.initRSVP(); WC.initReveal(); WC.initSisi();
  });
})();
