/* =====================================================================
   core.js - LOGIKA INTERAKTIF UTAMA (jangan diubah per klien)
   Tanpa framework. Supabase diakses via REST (tanpa SDK) agar ringan.
   ===================================================================== */
(function () {
  "use strict";
  const C = window.WC_CONFIG,
    K = window.WC_KONTEN;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (n, a = 0, b = 1) => Math.min(b, Math.max(a, n));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const adaDB = () => !!(C.SUPABASE_URL && C.SUPABASE_ANON_KEY);

  /* ---------- nama tamu dari URL ---------- */
  function initTamu() {
    const n = new URLSearchParams(location.search).get(C.PARAM_TAMU);
    const nama = (n || "Tamu Undangan").trim().slice(0, 60);
    $$("[data-tamu]").forEach((el) => (el.textContent = nama));
    const f = $("#f-nama");
    if (f && n) f.value = nama;
  }

  /* ---------- INTRO: pintu terbuka -> taman -> monogram -> nama ---------- */
  function initIntro() {
    const body = document.body;
    let sudah = false;
    body.classList.add("terkunci");
    const nol = () => {
      if (!body.classList.contains("siap")) window.scrollTo(0, 0);
    }; // selalu mulai dari cover
    nol();
    addEventListener("load", nol);
    [60, 250, 700].forEach((t) => setTimeout(nol, t));
    function akhir() {
      if (body.classList.contains("siap")) return;
      body.classList.add("siap");
      body.classList.remove("terkunci");
      WC.musik.petunjuk();
      const p = $("#pintu");
      if (p) setTimeout(() => p.remove(), 400);
    }
    /* LEWATI: selesaikan animasi intro yang terhingga langsung ke keadaan akhir.
       Animasi tak berhingga (angin, napas, kilau) dibiarkan berjalan normal. */
    function lewati() {
      document.getAnimations().forEach((a) => {
        const t =
          a.effect &&
          a.effect.getComputedTiming &&
          a.effect.getComputedTiming();
        if (
          t &&
          isFinite(t.iterations) &&
          !(
            a.effect.target &&
            a.effect.target.closest &&
            a.effect.target.closest(".sec")
          )
        ) {
          try {
            a.finish();
          } catch (e) {
            /* abaikan */
          }
        }
      });
      akhir();
    }
    function mulai() {
      if (sudah) return;
      sudah = true;
      WC.musik.putar();
      body.classList.add("mulai");
      if (reduce) {
        akhir();
        return;
      }
      setTimeout(
        () => $("#btn-lewati") && $("#btn-lewati").classList.add("tampak"),
        2500,
      );
      setTimeout(akhir, 11800); // total intro ± 12 detik
    }
    $("#btn-buka").addEventListener("click", mulai);
    $("#btn-lewati").addEventListener("click", lewati);
  }

  /* ---------- musik: tombol hidup/mati + ingat pilihan tamu ---------- */
  const musik = {
    el: null,
    tombol: null,
    label: null,
    nyala: false,
    pref: null,
    tLabel: 0,
    vol: 0,
    raf: 0,
    init() {
      this.tombol = $("#btn-musik");
      this.label = $("#musik-label");
      if (!K.musik) {
        this.tombol && this.tombol.remove();
        this.label && this.label.remove();
        return;
      }
      this.el = new Audio(K.musik);
      this.el.loop = true;
      this.el.preload = "auto";
      this.el.volume = 0;
      try {
        this.pref = localStorage.getItem("wc_musik");
      } catch (e) {
        /* mode privat */
      }
      this.tombol.classList.add("aktif");
      this.tombol.addEventListener("click", () => this.atur(!this.nyala, true));
      document.addEventListener("visibilitychange", () => {
        if (document.hidden) this.el.pause();
        else if (this.nyala) this.el.play().catch(() => {});
      });
    },
    /* dipanggil saat tamu menekan "Buka Undangan" (gestur pengguna = autoplay diizinkan) */
    putar() {
      if (!this.el) return;
      this.pref === "off" ? this.tampil(false, false) : this.atur(true, false);
    },
    atur(on, oleh) {
      if (!this.el) return;
      if (on) {
        this.el
          .play()
          .then(() => {
            this.nyala = true;
            this.tampil(true, oleh);
            this.fade(0.55, 900);
          })
          .catch(() => {
            this.nyala = false;
            this.tampil(false, false);
            this.kabar("Ketuk untuk musik");
          });
      } else {
        this.nyala = false;
        this.tampil(false, oleh);
        this.fade(0, 600, () => this.el.pause());
      }
      if (oleh) {
        try {
          localStorage.setItem("wc_musik", on ? "on" : "off");
        } catch (e) {
          /* abaikan */
        }
      }
    },
    tampil(on, umumkan) {
      this.tombol.classList.toggle("putar", on);
      this.tombol.setAttribute("aria-pressed", on ? "true" : "false");
      this.tombol.setAttribute(
        "aria-label",
        on ? "Matikan musik" : "Hidupkan musik",
      );
      if (umumkan) this.kabar(on ? "Musik hidup" : "Musik mati");
    },
    fade(ke, ms, selesai) {
      cancelAnimationFrame(this.raf);
      const v0 = this.el.volume,
        t0 = performance.now();
      const f = (t) => {
        const p = Math.min(1, (t - t0) / ms);
        this.el.volume = Math.max(0, Math.min(1, v0 + (ke - v0) * p));
        if (p < 1) this.raf = requestAnimationFrame(f);
        else if (selesai) selesai();
      };
      this.raf = requestAnimationFrame(f);
    },
    kabar(teks) {
      if (!this.label) return;
      this.label.textContent = teks;
      this.label.classList.add("tampak");
      clearTimeout(this.tLabel);
      this.tLabel = setTimeout(
        () => this.label.classList.remove("tampak"),
        1900,
      );
    },
    petunjuk() {
      if (!this.tombol || !K.musik) return;
      this.tombol.classList.add("petunjuk");
      setTimeout(() => this.tombol.classList.remove("petunjuk"), 5000);
    },
  };

  /* ---------- scroll: --p (cover) & --sp (tiap section) + reveal ---------- */
  function initScroll() {
    const cover = $(".cover"),
      secs = $$(".sec");
    let tick = false;
    function hitung() {
      tick = false;
      const vh = innerHeight;
      if (cover) {
        const r = cover.getBoundingClientRect();
        const p = clamp(-r.top / Math.max(1, r.height - vh));
        cover.style.setProperty("--p", reduce ? 0 : p.toFixed(4));
      }
      secs.forEach((s) => {
        const r = s.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        s.style.setProperty(
          "--sp",
          clamp((vh - r.top) / (vh + r.height)).toFixed(4),
        );
      });
    }
    const minta = () => {
      if (!tick) {
        tick = true;
        requestAnimationFrame(hitung);
      }
    };
    addEventListener("scroll", minta, { passive: true });
    addEventListener("resize", minta);
    hitung();
    const io = new IntersectionObserver(
      (es) =>
        es.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        }),
      { threshold: 0.18 },
    );
    secs.forEach((s) => io.observe(s));
  }

  /* ---------- slideshow latar (crossfade + ken burns) ---------- */
  function initSlideshow() {
    $$("[data-slideshow]").forEach((box) => {
      const list = (K.slideshow && K.slideshow[box.dataset.slideshow]) || [];
      if (!list.length) return;
      list.forEach((src, i) => {
        const d = document.createElement("div");
        d.className = "slide" + (i === 0 ? " aktif" : "");
        d.style.backgroundImage = `url("${src}")`;
        box.append(d);
      });
      if (list.length < 2 || reduce) return;
      let n = 0,
        timer = null;
      const ganti = () => {
        const s = $$(".slide", box);
        s[n].classList.remove("aktif");
        n = (n + 1) % s.length;
        s[n].classList.add("aktif");
      };
      const io = new IntersectionObserver(
        (es) =>
          es.forEach((e) => {
            if (e.isIntersecting && !timer) timer = setInterval(ganti, 5200);
            else if (!e.isIntersecting && timer) {
              clearInterval(timer);
              timer = null;
            }
          }),
        { threshold: 0.05 },
      );
      io.observe(box);
    });
  }

  /* ---------- REVEAL: tiap item muncul satu per satu, perlahan ---------- */
  function initReveal() {
    const els = $$("[data-rv]");
    if (reduce) {
      els.forEach((e) => e.classList.add("rv-tampil"));
      return;
    }
    const io = new IntersectionObserver(
      (es) => {
        const masuk = es
          .filter((e) => e.isIntersecting)
          .sort(
            (a, b) =>
              a.boundingClientRect.top - b.boundingClientRect.top ||
              a.boundingClientRect.left - b.boundingClientRect.left,
          );
        masuk.forEach((e, i) => {
          const el = e.target;
          io.unobserve(el);
          const ekstra = parseFloat(el.dataset.d || 0);
          el.style.transitionDelay =
            (Math.min(i, 6) * 0.26 + ekstra).toFixed(2) + "s";
          el.classList.add("rv-tampil");
          setTimeout(() => (el.style.transitionDelay = ""), 4200);
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -7% 0px" },
    );
    els.forEach((e) => io.observe(e));
  }

  /* ---------- panel desktop (kiri): salin adegan taman ---------- */
  function initSisi() {
    const sisi = $("#sisi"),
      sumber = $("#dunia-sumber");
    if (!sisi || !sumber) return;
    const klon = sumber.cloneNode(true);
    klon.removeAttribute("id");
    klon.classList.add("dunia--statis");
    klon.querySelectorAll("[id]").forEach((n) => n.removeAttribute("id"));
    klon.querySelectorAll("canvas, .kupu-bidang").forEach((n) => n.remove());
    $(".sisi__adegan", sisi).prepend(klon);
  }

  /* ---------- countdown ---------- */
  function initHitung() {
    const t = new Date(K.tanggalUtama).getTime(),
      box = $("#hitung");
    if (!box || isNaN(t)) return;
    const set = (k, v) => {
      const e = $(`[data-h="${k}"]`, box);
      if (e) e.textContent = String(v).padStart(2, "0");
    };
    function t1() {
      let d = Math.max(0, t - Date.now()) / 1000;
      set("hari", Math.floor(d / 86400));
      set("jam", Math.floor((d % 86400) / 3600));
      set("menit", Math.floor((d % 3600) / 60));
      set("detik", Math.floor(d % 60));
    }
    t1();
    setInterval(t1, 1000);
  }

  /* ---------- salin rekening ---------- */
  function initSalin() {
    document.addEventListener("click", async (e) => {
      const b = e.target.closest("[data-salin]");
      if (!b) return;
      const teks = b.dataset.salin,
        asli = b.textContent;
      try {
        await navigator.clipboard.writeText(teks);
      } catch {
        const ta = document.createElement("textarea");
        ta.value = teks;
        document.body.append(ta);
        ta.select();
        document.execCommand("copy");
        ta.remove();
      }
      b.textContent = "Tersalin";
      setTimeout(() => (b.textContent = asli), 1600);
    });
  }

  /* ---------- lightbox (foto prev/next + video) ---------- */
  function initLightbox() {
    const lb = $("#lightbox"),
      img = $("img", lb);
    let daftar = [],
      idx = 0,
      vid = null;
    const tutup = () => {
      lb.classList.remove("buka");
      if (vid) {
        vid.pause();
        vid.remove();
        vid = null;
      }
      img.hidden = false;
    };
    const tampil = () => {
      img.hidden = false;
      img.src = daftar[idx];
      lb.classList.add("buka");
    };
    document.addEventListener("click", (e) => {
      const g = e.target.closest("[data-zoom]"),
        v = e.target.closest("[data-video]");
      if (v) {
        vid = document.createElement("video");
        vid.src = v.dataset.video;
        vid.controls = true;
        vid.autoplay = true;
        vid.playsInline = true;
        img.hidden = true;
        lb.append(vid);
        lb.classList.add("buka");
      } else if (g) {
        daftar = $$("[data-zoom]").map((x) => x.dataset.zoom);
        idx = daftar.indexOf(g.dataset.zoom);
        tampil();
      } else if (e.target.closest("#lb-tutup") || e.target === lb) tutup();
      else if (e.target.closest("#lb-prev")) {
        idx = (idx - 1 + daftar.length) % daftar.length;
        tampil();
      } else if (e.target.closest("#lb-next")) {
        idx = (idx + 1) % daftar.length;
        tampil();
      }
    });
    addEventListener("keydown", (e) => {
      if (e.key === "Escape") tutup();
      if (lb.classList.contains("buka") && !vid) {
        if (e.key === "ArrowRight") {
          idx = (idx + 1) % daftar.length;
          tampil();
        }
        if (e.key === "ArrowLeft") {
          idx = (idx - 1 + daftar.length) % daftar.length;
          tampil();
        }
      }
    });
  }

  /* ---------- Supabase REST (RSVP & ucapan) ---------- */
  const demoData = [];
  const hdr = () => ({
    apikey: C.SUPABASE_ANON_KEY,
    Authorization: "Bearer " + C.SUPABASE_ANON_KEY,
    "Content-Type": "application/json",
  });
  /* ==========================================
   FILE: js/core.js
   FUNGSI UTAMA: Integrasi RSVP Supabase (Inline Reply)
   ========================================== */

  // 1. INISIALISASI SUPABASE
  const supabaseUrl = window.WC_CONFIG.supabaseUrl;
  const supabaseKey = window.WC_CONFIG.supabaseAnonKey;
  const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

  // 2. AMBIL NAMA DARI URL (?to=Nama+Tamu)
  function dapatkanNamaTamu() {
    const urlParams = new URLSearchParams(window.location.search);
    const nama = urlParams.get(window.WC_CONFIG.PARAM_TAMU || "to");
    return nama ? nama : "Tamu Spesial";
  }

  // 3. TARIK DATA & RENDER GUESTBOOK
  async function tarikDataRSVP() {
    const slugUndangan = window.WC_CONFIG.UNDANGAN_ID;

    try {
      const { data, error } = await supabase
        .from("ucapan_tamu")
        .select(
          `
        id,
        nama, 
        kehadiran, 
        ucapan, 
        dibuat_pada,
        pasangan!inner(slug),
        balasan_ucapan ( nama, isi, dibuat_pada )
      `,
        )
        .eq("pasangan.slug", slugUndangan)
        .order("dibuat_pada", { ascending: false });

      if (error) throw error;
      renderBukuTamu(data);
    } catch (error) {
      console.error("Gagal menarik data:", error);
    }
  }

  function renderBukuTamu(dataRsvp) {
    const wadahRSVP = document.getElementById("wadah-guestbook");
    if (!wadahRSVP) return;

    wadahRSVP.innerHTML = "";

    // Ambil nama dari parameter link saat ini (cth: ?to=Agus+Ramdan)
    const namaDariLink = dapatkanNamaTamu();

    dataRsvp.forEach((tamu) => {
      let htmlBalasan = "";
      if (tamu.balasan_ucapan && tamu.balasan_ucapan.length > 0) {
        tamu.balasan_ucapan.forEach((balasan) => {
          htmlBalasan += `
          <div style="margin-top: 12px; padding: 10px 12px; background: rgba(0, 0, 0, 0.05); border-left: 3px solid #b78953; border-radius: 6px; font-size: 0.85rem;">
            <strong style="color: #333;"> ${balasan.nama}</strong>
            <p style="margin: 4px 0 0 0; color: #444; font-style: italic;">"${balasan.isi}"</p>
          </div>
        `;
        });
      }

      let warnaBadge = tamu.kehadiran === "Hadir" ? "#4CAF50" : "#757575";

      wadahRSVP.innerHTML += `
      <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 16px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: left;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 8px;">
          <h5 style="margin: 0; font-weight: bold; color: #222; font-size: 1rem;">${tamu.nama}</h5>
          <span style="font-size: 0.75rem; padding: 4px 10px; border-radius: 12px; background-color: ${warnaBadge}; color: white; font-weight: bold;">
            ${tamu.kehadiran}
          </span>
        </div>
        <p style="margin: 0 0 10px 0; font-size: 0.95rem; color: #333; line-height: 1.5;">"${tamu.ucapan}"</p>
        
        ${htmlBalasan}

        <!-- Tombol Trigger Balasan -->
        <button onclick="toggleFormBalas('${tamu.id}')" style="display: inline-block; margin-top: 12px; padding: 6px 14px; font-size: 0.75rem; font-weight: bold; color: #333; background-color: #e0e0e0; border-radius: 20px; border: none; cursor: pointer; transition: background 0.2s;">
          ↪ Balas Ucapan
        </button>

        <!-- Form Balas Inline (Nama otomatis terisi dari link URL) -->
        <div id="wadah-balas-${tamu.id}" style="display: none; flex-direction: column; margin-top: 12px; gap: 8px;">
          <input type="text" id="nama-pembalas-${tamu.id}" value="${namaDariLink}" readonly style="padding: 8px 12px; border-radius: 8px; border: 1px solid #ccc; font-size: 0.85rem; outline: none; background: #eaeaea; color: #555; font-weight: bold; cursor: not-allowed;">
          <div style="display: flex; gap: 8px; align-items: center;">
            <input type="text" id="input-balas-${tamu.id}" placeholder="Tulis balasan untuk ${tamu.nama}..." style="flex: 1; padding: 8px 12px; border-radius: 20px; border: 1px solid #ccc; font-size: 0.85rem; outline: none; background: #fff; color: #333;">
            <button id="btn-kirim-balasan-${tamu.id}" onclick="kirimBalasan('${tamu.id}', '${tamu.nama}')" style="padding: 8px 16px; background-color: #b78953; color: white; border: none; border-radius: 20px; font-size: 0.85rem; font-weight: bold; cursor: pointer;">Kirim</button>
          </div>
        </div>
      </div>
    `;
    });
  }
  // 5. FITUR: BUKA/TUTUP FORM BALASAN
  window.toggleFormBalas = function (ucapanId) {
    const form = document.getElementById(`wadah-balas-${ucapanId}`);
    // Ganti status display dari none (sembunyi) menjadi flex (tampil sejajar)
    if (form.style.display === "none" || form.style.display === "") {
      form.style.display = "flex";
    } else {
      form.style.display = "none";
    }
  };
  window.kirimBalasan = async function (ucapanId, namaTamu) {
    const inputNamaPembalas = document.getElementById(
      `nama-pembalas-${ucapanId}`,
    );
    const inputEl = document.getElementById(`input-balas-${ucapanId}`);
    const btnKirim = document.getElementById(`btn-kirim-balasan-${ucapanId}`);

    const isiBalasan = inputEl.value;
    const namaPembalas = inputNamaPembalas
      ? inputNamaPembalas.value
      : dapatkanNamaTamu();

    if (!isiBalasan || isiBalasan.trim() === "") {
      alert("Isi balasan tidak boleh kosong, Sir!");
      return;
    }

    btnKirim.innerText = "...";
    btnKirim.disabled = true;

    try {
      const slugUndangan = window.WC_CONFIG.UNDANGAN_ID;
      const { data: pasangan } = await supabase
        .from("pasangan")
        .select("id")
        .eq("slug", slugUndangan)
        .single();

      const { error } = await supabase.from("balasan_ucapan").insert([
        {
          ucapan_id: ucapanId,
          pasangan_id: pasangan.id,
          nama: namaPembalas, // Otomatis menggunakan nama dari parameter link!
          isi: isiBalasan,
        },
      ]);

      if (error) throw error;
      tarikDataRSVP();
    } catch (error) {
      alert("Gagal membalas: " + error.message);
      btnKirim.innerText = "Kirim";
      btnKirim.disabled = false;
    }
  };

  // 7. LOGIKA KIRIM UCAPAN UTAMA
  async function kirimUcapan(event) {
    event.preventDefault();

    const btn = document.getElementById("btn-kirim");
    const namaTamu = document.getElementById("nama-tamu").value;
    const kehadiran = document.getElementById("kehadiran-tamu").value;
    const ucapan = document.getElementById("ucapan-tamu").value;
    const slugUndangan = window.WC_CONFIG.UNDANGAN_ID;

    btn.disabled = true;
    btn.innerText = "Mengirim...";

    try {
      const { data: pasangan } = await supabase
        .from("pasangan")
        .select("id")
        .eq("slug", slugUndangan)
        .single();
      if (!pasangan) throw new Error("ID Undangan tidak valid.");

      const { error: errInsert } = await supabase.from("ucapan_tamu").insert([
        {
          pasangan_id: pasangan.id,
          nama: namaTamu,
          kehadiran: kehadiran,
          ucapan: ucapan,
        },
      ]);

      if (errInsert) throw errInsert;

      document.getElementById("ucapan-tamu").value = "";
      tarikDataRSVP();
    } catch (error) {
      alert("Gagal mengirim: " + error.message);
    } finally {
      btn.disabled = false;
      btn.innerText = "Kirim Ucapan";
    }
  }

  // 8. JALANKAN SAAT HALAMAN DIMUAT
  document.addEventListener("DOMContentLoaded", () => {
    const inputNama = document.getElementById("nama-tamu");
    if (inputNama) inputNama.value = dapatkanNamaTamu();

    const formRSVP = document.getElementById("form-rsvp");
    if (formRSVP) formRSVP.addEventListener("submit", kirimUcapan);

    if (typeof supabase !== "undefined") tarikDataRSVP();
  });

  // Jalankan fungsi otomatis saat website selesai dimuat
  document.addEventListener("DOMContentLoaded", () => {
    if (typeof supabase !== "undefined") {
      tarikDataRSVP();
    }
  });
  async function muatUcapan() {
    try {
      renderUcapan(await ambil());
    } catch (e) {
      /* diamkan; coba lagi saat polling */
    }
  }
  function initRSVP() {
    const f = $("#form-rsvp"),
      st = $("#status-rsvp");
    if (!f) return;
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const d = new FormData(f),
        btn = $("button", f);
      const data = {
        undangan_id: C.UNDANGAN_ID,
        nama: String(d.get("nama")).trim().slice(0, 60),
        kehadiran: d.get("kehadiran"),
        jumlah: Number(d.get("jumlah")) || 1,
        pesan: String(d.get("pesan")).trim().slice(0, 400),
      };
      if (!data.nama) {
        st.textContent = "Nama wajib diisi.";
        return;
      }
      btn.disabled = true;
      st.textContent = "Mengirim...";
      try {
        await kirim(data);
        st.textContent = adaDB()
          ? "Terima kasih, ucapan terkirim."
          : "Mode demo: ucapan tampil lokal (Supabase belum diisi).";
        f.reset();
        initTamu();
        await muatUcapan();
      } catch (err) {
        st.textContent = "Gagal mengirim. Coba lagi sebentar.";
      }
      btn.disabled = false;
    });
    muatUcapan();
    if (adaDB()) setInterval(muatUcapan, C.POLLING_MS);
  }

  window.WC = {
    $,
    $$,
    clamp,
    musik,
    initTamu,
    initIntro,
    initScroll,
    initHitung,
    initSalin,
    initLightbox,
    initRSVP,
    initSlideshow,
    initReveal,
    initSisi,
  };
})();
