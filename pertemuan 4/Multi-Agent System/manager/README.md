# Sistem Multi-Agent Terpadu

Program simulasi **multi-agent system** yang berjalan di terminal. Satu program memuat dua modul: rekomendasi lokasi belajar di kampus (Smart Campus) dan koordinasi robot pengiriman.

## Introduction

Multi-agent system (MAS) adalah sistem yang terdiri dari beberapa agen. Setiap agen punya tugas sendiri, lalu hasil kerja mereka digabungkan atau dikoordinasikan untuk menyelesaikan masalah yang lebih besar.

Program ini terdiri dari dua modul:

| Modul | Fungsi | Jumlah agen | Input pengguna |
|---|---|---|---|
| 1. Smart Campus | Merekomendasikan lokasi belajar terbaik beserta rute dari lokasi awal | 4 agen | Lokasi awal dan kebutuhan belajar |
| 2. Robot Pengiriman | Membagi tugas pengiriman paket ke robot yang sesuai | 3 robot | Tidak ada (data sudah tersedia di program) |

### Modul 1: Smart Campus

| Agen | Peran |
|---|---|
| `AgentNavigasi` | Mencari rute terpendek antarlokasi dengan algoritma **A\*** |
| `AgentBelajar` | Menyeleksi lokasi yang sesuai dengan kebutuhan belajar (fokus, diskusi, praktikum, santai) |
| `AgentFasilitas` | Menilai kualitas fasilitas lokasi (Wi-Fi, ketenangan, kapasitas) |
| `AgentRekomendasi` | Koordinator yang menggabungkan hasil ketiga agen lain menjadi satu rekomendasi |

Rumus penilaian:

```text
skor fasilitas = 0.4 x wifi + 0.4 x tenang + 0.2 x kapasitas
skor akhir     = skor fasilitas - 0.2 x jarak tempuh
```

Lokasi dengan skor akhir tertinggi menjadi rekomendasi utama.

| Lokasi | Jenis | Wi-Fi | Tenang | Kapasitas |
|---|---|---|---|---|
| Gedung A | diskusi | 4 | 3 | 4 |
| Gedung B | diskusi | 3 | 3 | 3 |
| Perpustakaan | fokus | 5 | 5 | 4 |
| Kantin | santai | 3 | 2 | 5 |
| Laboratorium | praktikum | 4 | 3 | 3 |
| Aula | diskusi | 3 | 3 | 5 |
| Gedung C | fokus | 4 | 4 | 3 |

### Modul 2: Robot Pengiriman

Setiap tugas diberikan ke robot yang berstatus **Siap**, kapasitasnya **mencukupi** berat paket, dan memiliki **jarak Manhattan terdekat** ke tujuan. Jika jaraknya sama, robot dipilih berdasarkan urutan nama.

| Robot | Posisi awal | Kapasitas |
|---|---|---|
| Robot-A | (0, 0) | 5 |
| Robot-B | (5, 0) | 3 |
| Robot-C | (2, 4) | 8 |

| Paket | Tujuan | Berat |
|---|---|---|
| Paket-1 | (3, 2) | 2 |
| Paket-2 | (6, 1) | 4 |
| Paket-3 | (1, 5) | 6 |

## Requirement

| Kebutuhan | Keterangan |
|---|---|
| Python | Versi 3.7 atau lebih baru |
| Library tambahan | Tidak ada, hanya memakai pustaka standar (`heapq`, `math`, `dataclasses`) |
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

Di sebagian sistem, perintahnya adalah `python3 sistem_multi_agent_gabungan.py`.

**3. Pilih menu**

| Menu | Fungsi |
|---|---|
| 1 | Smart Campus (rekomendasi lokasi belajar) |
| 2 | Simulasi koordinasi robot pengiriman |
| 3 | Pengujian otomatis |
| 4 | Keluar |

**Menu 1: Smart Campus.** Program meminta dua input:

| Input | Pilihan |
|---|---|
| Lokasi awal | Ketik nama lokasi: Gerbang, Gedung A, Gedung B, Perpustakaan, Kantin, Laboratorium, Aula, atau Gedung C. Huruf besar atau kecil tidak berpengaruh. |
| Kebutuhan belajar | `1` Fokus belajar, `2` Diskusi kelompok, `3` Praktikum, `4` Belajar santai |

**Menu 2: Robot Pengiriman.** Simulasi langsung berjalan tanpa input. Data robot dan paket di-reset setiap kali menu ini dipilih, sehingga hasilnya selalu sama.

**Menu 3: Pengujian otomatis.** Menjalankan 9 kasus uji untuk kedua modul tanpa input dari pengguna.

## Result

### 1. Smart Campus

Input: lokasi awal `Gerbang`, kebutuhan belajar `1` (fokus).

```text
========== HASIL MULTI-AGENT ==========
Lokasi awal: Gerbang
Kebutuhan belajar: fokus

Pilihan 1: Perpustakaan
Rute: Gerbang -> Gedung A -> Perpustakaan
Jarak: 4.00 unit
Skor fasilitas: 4.80
Skor akhir: 4.00

Pilihan 2: Gedung C
Rute: Gerbang -> Gedung A -> Gedung B -> Laboratorium -> Gedung C
Jarak: 8.00 unit
Skor fasilitas: 3.80
Skor akhir: 2.20

========== REKOMENDASI UTAMA ==========
Lokasi terbaik: Perpustakaan
Rute: Gerbang -> Gedung A -> Perpustakaan
Jarak: 4.00 unit
Alasan: lokasi sesuai kebutuhan belajar dan memiliki skor gabungan tertinggi.
```

Perpustakaan menang karena fasilitasnya lebih baik (4.80 dibanding 3.80) dan jaraknya lebih dekat (4.00 dibanding 8.00).

### 2. Robot Pengiriman

```text
=======================================================
SIMULASI MULTI-AGENT SYSTEM: ROBOT PENGIRIMAN
=======================================================

Memproses tugas: Paket-1

Robot-C mengambil Paket-1
Berat paket : 2
Jarak       : 3 satuan
Status      : Selesai

Memproses tugas: Paket-2

Robot-C mengambil Paket-2
Berat paket : 4
Jarak       : 4 satuan
Status      : Selesai

Memproses tugas: Paket-3

Robot-C mengambil Paket-3
Berat paket : 6
Jarak       : 9 satuan
Status      : Selesai

=======================================================
LAPORAN AKHIR PENGIRIMAN
=======================================================
Paket-1 | Status: Selesai | Agen: Robot-C
Paket-2 | Status: Selesai | Agen: Robot-C
Paket-3 | Status: Selesai | Agen: Robot-C

Kondisi akhir agen:
Robot-A | Posisi: (0, 0) | Kapasitas: 5 | Status: Siap
Robot-B | Posisi: (5, 0) | Kapasitas: 3 | Status: Siap
Robot-C | Posisi: (1, 5) | Kapasitas: 8 | Status: Siap

Tugas selesai: 3/3
```

Ketiga paket dikerjakan Robot-C karena robot ini selalu menjadi kandidat dengan jarak terdekat (Paket-1 dan Paket-2), atau satu-satunya yang kapasitasnya cukup (Paket-3 berbobot 6, sedangkan Robot-A hanya berkapasitas 5).

### 3. Pengujian otomatis

| Modul | Kasus uji | Status |
|---|---|---|
| Smart Campus | Rute Gerbang -> Perpustakaan (Gerbang, Gedung A, Perpustakaan, jarak 4.0) | LULUS |
| Smart Campus | Jarak Gerbang -> Gedung C (8.0) | LULUS |
| Smart Campus | Seleksi lokasi kebutuhan fokus (Perpustakaan, Gedung C) | LULUS |
| Smart Campus | Skor fasilitas Perpustakaan (4.8) | LULUS |
| Smart Campus | Rekomendasi terbaik dari Gerbang untuk fokus (Perpustakaan) | LULUS |
| Robot Pengiriman | Jarak Manhattan (0,0) ke (3,2) bernilai 5 | LULUS |
| Robot Pengiriman | Paket berbobot 7 hanya bisa dibawa Robot-C | LULUS |
| Robot Pengiriman | Paket berbobot 100 tidak mendapat agen | LULUS |
| Robot Pengiriman | Paket ringan ke (3,2) dipilihkan Robot-C | LULUS |

```text
Status keseluruhan: SEMUA LULUS
```
