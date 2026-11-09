/* =====================================================================
   terbang.js - kupu-kupu putih & merpati putih yang terbang realistis.
   Kupu-kupu: sayap 3D mengepak, terbang berkelok, hinggap melayang di dekat
   elemen [data-kupu] (mis. kartu oval pembuka) atau berkeliling layar.
   Merpati: rombongan melintas berkala, kepak bergantian dengan meluncur.
   Hemat: hanya transform, berhenti saat tab tersembunyi, mati bila reduced-motion.
   ===================================================================== */
(function () {
  "use strict";
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const R = Math.random, app = document.querySelector(".app"); if (!app) return;
  const layer = document.createElement("div"); layer.className = "langit-terbang"; layer.setAttribute("aria-hidden", "true"); document.body.appendChild(layer);
  const kecil = matchMedia("(max-width: 700px)").matches;
  /* ATUR DI SINI: jumlah kupu-kupu saat sambutan, jumlah tetap sesudahnya, dan kapan kelebihannya pergi */
  const JUMLAH_AWAL = kecil ? 3 : 4, JUMLAH_TETAP = 2, WAKTU_KURANG = 16000;
  let tenang = false;                          // setelah sambutan: lebih sering di sisi layar agar tak menutupi teks
  const cover = document.getElementById("cover");
  let W = 0, H = 0, last = 0, raf = 0, mulai = false, tSiap = 0, tDove = 0, tLahir = 0, heroAktif = true;
  const JUMLAH_KUPU = kecil ? 3 : 4;
  const kupu = [], burung = [];

  function ukur() { const r = app.getBoundingClientRect(); W = r.width; H = window.innerHeight; }
  addEventListener("resize", ukur); ukur();

  /* ---------- kupu-kupu ---------- */
  function buatKupu(i) {
    const el = document.createElement("div"); el.className = "kp";
    el.innerHTML = '<img class="sy kn" src="assets/svg/kupu-sayap-kiri.svg" alt=""><img class="bd" src="assets/svg/kupu-badan.svg" alt=""><img class="sy kr" src="assets/svg/kupu-sayap-kanan.svg" alt="">';
    layer.append(el);
    const sisi = R() < .5 ? -1 : 1;
    return { el, x: sisi < 0 ? -60 : W + 60, y: H * (.2 + R() * .5), vx: -sisi * 30, vy: -10, h: 0, s: (kecil ? .21 : .25) + R() * .08, ph: R() * 6.28, ph2: R() * 6.28, tx: W / 2, ty: H / 2, tGanti: 0, cepat: .095 + R() * .03, hover: false, sisi: i % 2 ? 1 : -1 };
  }
  function target(k, now) {
    const att = Array.from(document.querySelectorAll("[data-kupu]")).map(e => e.getBoundingClientRect()).filter(r => r.bottom > 40 && r.top < H - 40 && r.width >= 0);
    const app0 = app.getBoundingClientRect();
    if (att.length && R() < (tenang ? .3 : .5)) { const r = att[(R() * att.length) | 0]; const a = k.ph * 3 + R() * 2; k.tx = r.left - app0.left + r.width / 2 + Math.cos(a) * 120; k.ty = r.top + Math.sin(a) * 80; k.hover = true; }
    else {
      k.hover = false; k.ty = H * (.12 + R() * .72);
      if (tenang && R() < .88) k.tx = W * (k.sisi < 0 ? .03 + R() * .16 : .81 + R() * .16);   // tetap di sisi rumahnya (kiri/kanan)
      else k.tx = W * (.1 + R() * .8);
    }
    k.tGanti = now + 3500 + R() * 5500;
  }
  function stepKupu(k, dt, now) {
    if (k.pergi) k.tGanti = Infinity;            // tujuan sudah di luar layar: jangan ganti target
    else if (now > k.tGanti) target(k, now);
    for (const o of kupu) {                       // saling menjauh agar tidak menumpuk
      if (o === k) continue;
      const rx = k.x - o.x, ry = k.y - o.y, rd = Math.hypot(rx, ry) || 1, jarak = 120;
      if (rd < jarak) { const f = (jarak - rd) / jarak; k.vx += (rx / rd) * f * 140 * dt; k.vy += (ry / rd) * f * 140 * dt; if (Math.hypot(k.tx - o.tx, k.ty - o.ty) < 110) k.tGanti = 0; }
    }
    const dx = k.tx - k.x, dy = k.ty - k.y, d = Math.hypot(dx, dy) || 1;
    const vmax = k.pergi ? 118 : (k.hover && d < 90 ? 22 : (tenang ? 46 : 62)) * (kecil ? .85 : 1);
    // steering + gerak berkelok khas kupu-kupu
    const wob = Math.sin(now / 430 + k.ph) * 46 + Math.sin(now / 190 + k.ph2) * 22;
    let ax = (dx / d) * vmax - k.vx, ay = (dy / d) * vmax - k.vy;
    k.vx += ax * Math.min(1, dt * 1.6) + Math.cos(k.h) * wob * dt * .55;
    k.vy += ay * Math.min(1, dt * 1.6) + Math.sin(k.h) * wob * dt * .55 + Math.sin(now / 150 + k.ph) * 30 * dt;
    k.x += k.vx * dt; k.y += k.vy * dt;
    const ha = Math.atan2(k.vy, k.vx) + Math.PI / 2; let dh = ha - k.h; dh = Math.atan2(Math.sin(dh), Math.cos(dh)); k.h += dh * Math.min(1, dt * 4);
    const cepat = k.hover && d < 90 ? k.cepat * 1.35 : k.cepat;
    k.el.style.setProperty("--f", cepat.toFixed(3) + "s");
    k.el.style.transform = `translate3d(${(k.x - 126 * k.s).toFixed(1)}px,${(k.y - 75 * k.s).toFixed(1)}px,0) rotate(${k.h.toFixed(3)}rad) scale(${k.s.toFixed(3)})`;
  }

  /* ---------- merpati ---------- */
  function buatMerpati(arah, y, skala, jeda) {
    const el = document.createElement("div"); el.className = "mp kepak";
    el.innerHTML = '<img class="sj" src="assets/svg/merpati-sayap-jauh.svg" alt=""><img class="mb" src="assets/svg/merpati-badan.svg" alt=""><img class="sd" src="assets/svg/merpati-sayap-dekat.svg" alt="">';
    layer.append(el);
    return { el, arah, x: arah > 0 ? -240 * skala - jeda * 120 : W + 240 * skala + jeda * 120, y0: y, s: skala, v: 105 + R() * 35, ph: R() * 6.28, fase: "kepak", tFase: 0, fd: .34 + R() * .06 };
  }
  function rombongan(now) {
    const arah = R() < .5 ? 1 : -1, y = H * (.14 + R() * .4), n = heroAktif ? 1 + ((R() * 3) | 0) : 1 + ((R() * 2) | 0), sk = (kecil ? .42 : .5) + R() * .22;
    for (let i = 0; i < n; i++) burung.push(buatMerpati(arah, y + i * 22 * (R() < .5 ? 1 : -1), sk * (1 - i * .12), i * .55));
    tDove = now + (heroAktif ? 14000 + R() * 10000 : 38000 + R() * 24000);
  }
  function stepMerpati(b, dt, now) {
    if (now > b.tFase) {                       // kepak beberapa kali lalu meluncur
      if (b.fase === "kepak") { b.fase = "luncur"; b.tFase = now + 900 + R() * 800; b.el.classList.remove("kepak"); b.el.classList.add("luncur"); }
      else { b.fase = "kepak"; b.tFase = now + 1500 + R() * 1400; b.el.classList.remove("luncur"); b.el.classList.add("kepak"); b.el.style.setProperty("--fd", b.fd + "s"); }
    }
    b.x += b.arah * b.v * dt * (b.fase === "luncur" ? .92 : 1);
    const y = b.y0 + Math.sin(now / 900 + b.ph) * 16 + (b.fase === "kepak" ? Math.sin(now / (b.fd * 1000 * 2)) * 4 : 0);
    const tilt = Math.cos(now / 900 + b.ph) * 4 * b.arah;
    b.el.style.transform = `translate3d(${b.x.toFixed(1)}px,${y.toFixed(1)}px,0) rotate(${tilt.toFixed(1)}deg) scale(${(b.arah * b.s).toFixed(3)},${b.s.toFixed(3)})`;
    return (b.arah > 0 && b.x > W + 260) || (b.arah < 0 && b.x < -260 - 220 * b.s);
  }

  /* kupu-kupu hanya menemani bagian awal (hero). Setelah hero terlewat mereka terbang keluar layar
     dan dihapus; bila tamu kembali ke atas mereka muncul lagi. Di section biasa hanya merpati. */
  function atur(now) {
    heroAktif = !cover || cover.getBoundingClientRect().bottom > H * .3;
    if (heroAktif) {
      kupu.forEach(k => { k.pergi = false; });
      if (kupu.length < JUMLAH_KUPU && now - tLahir > 900) { const k = buatKupu(kupu.length); k.tGanti = 0; kupu.push(k); tLahir = now; }
    } else {
      kupu.forEach(k => {
        if (!k.pergi) { k.pergi = true; const kiri = k.x < W / 2; k.tx = kiri ? -140 : W + 140; k.ty = k.y - 60 - R() * 120; k.hover = false; k.tGanti = Infinity; }
      });
    }
  }
  function frame(now) {
    raf = 0;
    if (document.hidden) return;
    const dt = Math.min(.05, (now - last) / 1000 || .016); last = now;
    if (!mulai && document.body.classList.contains("siap")) { mulai = true; tSiap = now; tDove = now + 4500; }
    if (mulai) {
      atur(now);
      for (let i = kupu.length - 1; i >= 0; i--) {
        const k = kupu[i]; stepKupu(k, dt, now);
        if (k.pergi && (k.x < -120 || k.x > W + 120)) { k.el.remove(); kupu.splice(i, 1); }
      }
      if (now > tDove) rombongan(now);
      for (let i = burung.length - 1; i >= 0; i--) if (stepMerpati(burung[i], dt, now)) { burung[i].el.remove(); burung.splice(i, 1); }
    }
    loop();
  }
  function loop() { if (!raf && !document.hidden) raf = requestAnimationFrame(frame); }
  document.addEventListener("visibilitychange", () => { last = performance.now(); loop(); });
  loop();
})();
