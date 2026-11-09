/* =====================================================================
   konfigurasi.js - KREDENSIAL & ENDPOINT (satu-satunya file untuk koneksi)
   Jangan taruh data mempelai di sini. Data klien ada di tema-konten.js
   ===================================================================== */
window.WC_CONFIG = {
  // EDIT KLIEN: isi dari Supabase > Project Settings > API
  supabaseUrl: "https://nqeclnbrzzmyabgwmpth.supabase.co",
  supabaseAnonKey:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xZWNsbmJyenpteWFiZ3dtcHRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIyMzAzNTQsImV4cCI6MjEwNzgwNjM1NH0.cXvgbhJZCtpZVdPTbjoY7qTLyjS3uKZ53HurbTaUulM",

  // EDIT KLIEN: ID unik undangan (satu project Supabase bisa melayani banyak klien)
  UNDANGAN_ID: "demo",

  TABEL_UCAPAN: "ucapan_tamu", // nama tabel (SQL ada di PANDUAN-TEMA.md)
  POLLING_MS: 20000, // refresh ucapan tiap 20 detik
  PARAM_TAMU: "to", // link tamu: index.html?to=Nama+Tamu
};
