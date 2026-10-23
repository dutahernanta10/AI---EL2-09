# Sistem Pakar Terpadu

Program sistem pakar berbasis **forward chaining** yang berjalan di terminal. Satu program memuat dua modul: diagnosis kerusakan perangkat elektronik dan rekomendasi strategi belajar mahasiswa.

## Introduction

Sistem pakar adalah program yang meniru cara seorang pakar mengambil keputusan, dengan menggunakan basis pengetahuan berupa aturan **IF-THEN**. Program ini memakai metode **forward chaining**: sistem mulai dari fakta yang diberikan pengguna, mencocokkannya dengan aturan, lalu menambahkan kesimpulan baru sebagai fakta sampai tidak ada aturan lain yang bisa dipakai.

Program ini terdiri dari dua modul:

| Modul | Fungsi | Jumlah aturan | Input pengguna |
|---|---|---|---|
| 1. Diagnosis Elektronik | Menduga jenis kerusakan perangkat elektronik beserta saran pemeriksaannya | 6 aturan (R1–R6) | Kode gejala G01–G08 |
| 2. Smart Campus | Merekomendasikan strategi belajar sesuai kondisi mahasiswa | 16 aturan (R01–R16) | Jawaban ya/tidak untuk 6 pertanyaan |

Komponen utama sistem:

| Komponen | Modul 1 | Modul 2 |
|---|---|---|
| Basis pengetahuan | `GEJALA`, `DIAGNOSIS`, `ATURAN` | `SmartCampusExpertSystem.rules` dan `recommendations` |
| Working memory | Himpunan fakta pada fungsi `forward_chaining()` | `facts`, `fact_sources`, `fired_rules`, `inference_trace` |
| Inference engine | `forward_chaining()` | `run_inference()` |
| Penjelasan hasil | Daftar aturan yang terpenuhi | Daftar aturan yang terpenuhi dan alasannya |

## Requirement

| Kebutuhan | Keterangan |
|---|---|
| Python | Versi 3.7 atau lebih baru |
| Library tambahan | Tidak ada, hanya memakai pustaka standar (`dataclasses`, `typing`) |
| Sistem operasi | Windows, Linux, atau macOS |
| Terminal | Command Prompt, PowerShell, atau terminal bawaan |

Cek versi Python dengan perintah berikut:

```bash
python --version
```

## How to use

**1. Unduh proyek**

```bash
git clone https://github.com/dutahernanta10/AI---EL2-09/
cd <AI---EL2-09>
```

**2. Jalankan program**

```bash
python gabungan.py
```

Di sebagian sistem, perintahnya adalah `python3 sistem_pakar_gabungan.py`.

**3. Pilih menu**

| Menu | Fungsi |
|---|---|
| 1 | Diagnosis kerusakan perangkat elektronik |
| 2 | Konsultasi strategi belajar (Smart Campus) |
| 3 | Lihat daftar gejala elektronik |
| 4 | Jalankan pengujian otomatis |
| 5 | Keluar |

**Menu 1: Diagnosis elektronik.** Masukkan kode gejala satu per satu, lalu ketik `SELESAI`.

| Kode | Gejala |
|---|---|
| G01 | Perangkat tidak menyala |
| G02 | Lampu indikator mati |
| G03 | Lampu indikator menyala |
| G04 | Perangkat mati secara tiba-tiba |
| G05 | Perangkat terlalu panas |
| G06 | Perangkat menyala tetapi tidak berfungsi normal |
| G07 | Terdengar bunyi tidak normal |
| G08 | Tegangan catu daya tidak sesuai |

**Menu 2: Smart Campus.** Jawab 6 pertanyaan dengan `y` (ya) atau `n` (tidak).

| Fakta | Pertanyaan |
|---|---|
| `difficulty_concept` | Kesulitan memahami konsep materi |
| `difficulty_practice` | Kesulitan mengerjakan soal atau menerapkan materi |
| `often_forget` | Sering lupa materi yang sudah dipelajari |
| `limited_time` | Waktu belajar terbatas |
| `exam_soon` | Ujian akan berlangsung dalam waktu dekat |
| `high_target` | Menargetkan hasil akademik yang tinggi |

**Menu 4: Pengujian otomatis.** Menjalankan 8 kasus uji (4 untuk tiap modul) tanpa input dari pengguna.

## Result

### 1. Diagnosis elektronik

Input: `G01`, `G02`, lalu `SELESAI`.

```text
============================================================
HASIL ANALISIS SISTEM PAKAR
============================================================

Gejala yang dipilih:
- G01: Perangkat tidak menyala
- G02: Lampu indikator mati

Aturan yang terpenuhi:
- R1: Perangkat tidak menyala dan lampu indikator mati.

Kesimpulan:

1. Dugaan masalah catu daya
   Saran: Periksa sumber listrik, kabel, konektor, sekring, dan rangkaian catu daya.

Catatan:
Hasil adalah dugaan awal, bukan kepastian kerusakan. Lakukan pemeriksaan teknis dengan aman.
```

### 2. Smart Campus

Jawaban: konsep sulit (y), soal sulit (n), sering lupa (n), waktu terbatas (y), ujian dekat (y), target tinggi (n).

```text
============================================================
HASIL ANALISIS SISTEM PAKAR
============================================================

Kondisi yang kamu pilih:
- Apakah kamu kesulitan memahami konsep materi?
- Apakah waktu belajarmu terbatas?
- Apakah ujian akan berlangsung dalam waktu dekat?

Aturan yang terpenuhi:
- R01 (Sulit memahami konsep): Mahasiswa menyatakan kesulitan memahami konsep.
- R04 (Waktu belajar terbatas): Waktu belajar yang tersedia relatif terbatas.
- R05 (Ujian segera berlangsung): Mahasiswa perlu memprioritaskan persiapan ujian.
- R07 (Rekomendasi peta konsep): Peta konsep membantu menyusun hubungan antarkonsep.
- R08 (Rekomendasi teknik Feynman): Menjelaskan materi dengan bahasa sendiri membantu menguji pemahaman.
- R12 (Rekomendasi jadwal belajar): Jadwal belajar membantu memprioritaskan waktu yang terbatas.
- R13 (Rekomendasi simulasi ujian): Simulasi ujian membantu melatih pengelolaan waktu.
- R16 (Prioritas belajar menjelang ujian): Memilih topik prioritas membantu penggunaan waktu menjelang ujian.

Rekomendasi strategi belajar:

1. Peta Konsep
   Tuliskan topik utama, lalu hubungkan subtopik dengan garis dan kata kunci.

2. Teknik Feynman
   Jelaskan materi dengan bahasa sederhana seolah-olah kamu mengajarkannya.

3. Jadwal Belajar
   Bagi waktu belajar menjadi sesi pendek yang terukur dan tetapkan target kecil untuk setiap sesi.

4. Simulasi Ujian
   Kerjakan soal latihan dalam kondisi mirip ujian sungguhan, lalu evaluasi hasilnya.

5. Prioritas Topik
   Pilih topik yang paling lemah atau paling sering keluar di ujian, lalu pelajari lebih dulu.
```

### 3. Pengujian otomatis

| Kasus uji | Input | Hasil yang diharapkan | Status |
|---|---|---|---|
| E1 | G01, G02 | D01 | LULUS |
| E2 | G04, G05 | D04 | LULUS |
| E3 | G03, G06 | D03 | LULUS |
| E4 | (kosong) | (tidak ada) | LULUS |
| C1 | difficulty_concept | recommend_concept_map, recommend_feynman | LULUS |
| C2 | exam_soon, difficulty_practice | recommend_mock_exam, recommend_practice, recommend_timed_practice | LULUS |
| C3 | exam_soon, limited_time | recommend_mock_exam, recommend_study_plan, recommend_priority_topics | LULUS |
| C4 | (kosong) | (tidak ada) | LULUS |

```text
Status keseluruhan: SEMUA LULUS
```

> **Catatan:** Hasil diagnosis hanya dugaan awal berdasarkan aturan yang tertulis di program, bukan pengganti pemeriksaan oleh teknisi atau konsultasi akademik.
