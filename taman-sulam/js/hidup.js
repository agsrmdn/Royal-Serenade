/* =====================================================================
   hidup.js - membuat adegan terasa HIDUP:
   - kelopak melayang, debu cahaya berkelip, percikan air mancur (canvas)
   - parallax mengikuti pointer / kemiringan HP / gerak lembut otomatis
   Hemat baterai: berhenti saat tab tersembunyi atau cover di luar layar.
   ===================================================================== */
(function () {
  "use strict";
  const cover = document.getElementById("cover"), adegan = document.getElementById("dunia-sumber"), cv = document.getElementById("fx");
  if (!cover || !adegan || !cv) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) { cv.remove(); return; }
  const ctx = cv.getContext("2d"), taman = adegan.querySelector(".l-taman");
  const kecil = matchMedia("(max-width: 700px)").matches;
  let W = 0, H = 0, dpr = 1, tMulai = 0, tampak = true, last = 0, raf = 0;
  const R = Math.random;

  function ukur() {
    W = adegan.clientWidth; H = adegan.clientHeight; dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    adegan.style.setProperty("--k", (W / 430).toFixed(4));
  }
  addEventListener("resize", ukur); ukur();
  new IntersectionObserver(es => { tampak = es[0].isIntersecting; if (tampak) mulaiLoop(); }, { threshold: 0 }).observe(cover);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) mulaiLoop(); });

  /* ---------- kelopak & debu ---------- */
  const warna = ["#F4B6D0", "#EE9CC0", "#F8D0E0", "#E48AB4", "#FBE0EA"];
  const petals = Array.from({ length: kecil ? 14 : 22 }, () => baruKelopak(true));
  function baruKelopak(acak) {
    return { x: R() * W, y: acak ? R() * H : -20, s: 5 + R() * 6, vx: .25 + R() * .55, vy: .35 + R() * .6, rot: R() * 6.28, vr: (R() - .5) * .05, ph: R() * 6.28, f: .6 + R() * 1.2, c: warna[(R() * warna.length) | 0] };
  }
  const motes = Array.from({ length: kecil ? 22 : 36 }, () => ({ x: R() * W, y: R() * H, r: .8 + R() * 1.8, ph: R() * 6.28, sp: .6 + R() * 1.4, vy: -.08 - R() * .18 }));

  /* ---------- air mancur: posisi dari lapisan taman ---------- */
  const drops = [];
  function jangkar() {
    const a = adegan.getBoundingClientRect(), t = taman.getBoundingClientRect(), sc = a.width / W || 1;
    return { x: (t.left - a.left) / sc, y: (t.top - a.top) / sc, w: t.width / sc, h: t.height / sc };
  }
  function pancur(j, dt, alpha) {
    const k = j.w / 860;
    const sumber = [{ fx: .5, fy: .247, spread: 1.4, land: .452, n: 2 }, { fx: .5, fy: .452, spread: 1.0, land: .600, n: 2, lebar: .095 }, { fx: .5, fy: .600, spread: .35, land: .618, n: 1, lebar: .17 }];
    sumber.forEach(s => { for (let i = 0; i < s.n * dt; i++) if (R() < .55) {
      const side = R() < .5 ? -1 : 1, off = s.lebar ? side * s.lebar * (.4 + R() * .6) : 0;
      drops.push({ x: j.x + (s.fx + off) * j.w, y: j.y + s.fy * j.h, vx: (R() - .5) * s.spread * k * 1.2 + (s.lebar ? -side * .25 * k : 0), vy: -(1.4 + R() * 1.8) * k * (s.fy < .3 ? 1.2 : .7), g: .075 * k, land: j.y + s.land * j.h, life: 1 });
    } });
    ctx.fillStyle = "rgba(246,252,250,.9)";
    for (let i = drops.length - 1; i >= 0; i--) {
      const d = drops[i]; d.vy += d.g * dt; d.x += d.vx * dt; d.y += d.vy * dt;
      if (d.y > d.land && d.vy > 0) { drops.splice(i, 1); ripples.push({ x: d.x, y: d.land, r: 1, a: .7 }); continue; }
      ctx.globalAlpha = alpha * .85; ctx.beginPath(); ctx.arc(d.x, d.y, Math.max(.8, 1.3 * k), 0, 6.283); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  const ripples = [];
  function riak(k, alpha) {
    for (let i = ripples.length - 1; i >= 0; i--) {
      const r = ripples[i]; r.r += .5 * k; r.a -= .02;
      if (r.a <= 0) { ripples.splice(i, 1); continue; }
      ctx.strokeStyle = `rgba(255,255,255,${(r.a * alpha).toFixed(3)})`; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(r.x, r.y, r.r * 2.4, r.r * .7, 0, 0, 6.283); ctx.stroke();
    }
    if (ripples.length > 70) ripples.splice(0, 20);
  }

  /* ---------- parallax: pointer / kemiringan / otomatis ---------- */
  let tx = 0, ty = 0, cx = 0, cy = 0, aktif = false, tAktif = 0;
  cover.addEventListener("pointermove", e => { const r = cover.getBoundingClientRect(); tx = ((e.clientX - r.left) / r.width - .5) * 2; ty = ((e.clientY - r.top) / r.height - .5) * 2; aktif = true; tAktif = performance.now(); }, { passive: true });
  cover.addEventListener("pointerleave", () => { aktif = false; });
  addEventListener("deviceorientation", e => { if (e.gamma == null) return; tx = Math.max(-1, Math.min(1, e.gamma / 22)); ty = Math.max(-1, Math.min(1, (e.beta - 50) / 28)); aktif = true; tAktif = performance.now(); }, { passive: true });

  function frame(now) {
    raf = 0;
    if (document.hidden || !tampak) return;
    const dt = Math.min(3, (now - last) / 16.7 || 1); last = now;
    // parallax
    if (!aktif || now - tAktif > 2500) { tx = Math.sin(now / 5200) * .7; ty = Math.cos(now / 6800) * .45; }
    cx += (tx - cx) * .045 * dt; cy += (ty - cy) * .045 * dt;
    cover.style.setProperty("--mx", cx.toFixed(3)); cover.style.setProperty("--my", cy.toFixed(3));
    // partikel hanya setelah intro berjalan
    if (!tMulai && document.body.classList.contains("mulai")) tMulai = now;
    if (tMulai && document.body.classList.contains("siap") && now - tMulai < 9200) tMulai = now - 9200;   // setelah Lewati: partikel langsung hadir
    ctx.clearRect(0, 0, W, H);
    if (tMulai) {
      const alpha = Math.max(0, Math.min(1, (now - tMulai - 6500) / 2500)), k = W / 430;
      if (alpha > 0) {
        const j = jangkar(); pancur(j, dt, alpha); riak(j.w / 860, alpha);
        motes.forEach(m => { m.y += m.vy * dt * k; m.x += Math.sin(now / 1800 + m.ph) * .12 * k; if (m.y < -4) { m.y = H + 4; m.x = R() * W; }
          const tw = .35 + .65 * Math.abs(Math.sin(now / 900 * m.sp + m.ph)); ctx.globalAlpha = alpha * tw * .8; ctx.fillStyle = "#FFF1B8"; ctx.beginPath(); ctx.arc(m.x, m.y, m.r * k, 0, 6.283); ctx.fill(); });
        petals.forEach(p => { p.y += p.vy * dt * k; p.x += (p.vx + Math.sin(now / 1100 * p.f + p.ph) * .5) * dt * k; p.rot += p.vr * dt;
          if (p.y > H + 20 || p.x > W + 20) Object.assign(p, baruKelopak(false), { x: -10 - R() * W * .4 });
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.scale(1, .45 + .55 * Math.abs(Math.sin(now / 700 * p.f + p.ph))); ctx.globalAlpha = alpha * .9; ctx.fillStyle = p.c;
          const s = p.s * k; ctx.beginPath(); ctx.moveTo(0, -s); ctx.bezierCurveTo(s * .9, -s * .6, s * .8, s * .7, 0, s); ctx.bezierCurveTo(-s * .8, s * .7, -s * .9, -s * .6, 0, -s); ctx.fill(); ctx.restore(); });
        ctx.globalAlpha = 1;
      }
    }
    mulaiLoop();
  }
  function mulaiLoop() { if (!raf && tampak && !document.hidden) raf = requestAnimationFrame(frame); }
  mulaiLoop();
})();
