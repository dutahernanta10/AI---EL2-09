# Sistem Algoritma Pencarian Terpadu

Program simulasi **algoritma pencarian (search algorithm)** yang berjalan di terminal. Satu program memuat dua modul: pencarian jalur pada peta grid dengan A\*, dan pencarian jalur antarlokasi kampus dengan BFS, DFS, dan A\*.

## Introduction

Algoritma pencarian dipakai untuk menemukan urutan langkah dari kondisi awal menuju tujuan. Pada proyek ini, masalahnya adalah mencari jalur dari satu titik ke titik lain, lalu membandingkan hasil dari beberapa algoritma.

Program ini terdiri dari dua modul:

| Modul | Algoritma | Ruang pencarian | Input pengguna |
|---|---|---|---|
| 1. Peta Grid | A\* | Grid 6 x 5 dengan rintangan | Tidak ada (peta sudah tersedia di program) |
| 2. Lokasi Kampus | BFS, DFS, A\* | Graf 8 lokasi kampus | Lokasi awal dan lokasi tujuan |

### Algoritma yang dipakai

| Algoritma | Cara kerja | Hasil yang dijamin |
|---|---|---|
| BFS (Breadth-First Search) | Menjelajah level demi level memakai antrean (queue) | Jalur dengan **jumlah langkah paling sedikit** |
| DFS (Depth-First Search) | Menjelajah sedalam mungkin dulu memakai tumpukan (stack) | Jalur pertama yang ditemukan, **tidak dijamin terpendek** |
| A\* | Memilih titik dengan nilai terkecil dari `f = g + h` memakai priority queue | Jalur dengan **biaya paling kecil** |

Pada A\*, `g` adalah biaya dari titik awal sampai titik sekarang, dan `h` adalah perkiraan sisa biaya ke tujuan.

| Modul | Biaya per langkah (`g`) | Heuristik (`h`) |
|---|---|---|
| Peta Grid | 1 per langkah | Jarak Manhattan |
| Lokasi Kampus | Jarak garis lurus antarlokasi | Jarak garis lurus ke tujuan |

### Modul 1: Peta Grid

Pergerakan hanya ke empat arah (kanan, kiri, bawah, atas). Posisi ditulis sebagai `(x, y)`, dengan `S` di `(0, 0)` dan `G` di `(5, 4)`.

```text
S 0 0 # 0 0
0 # 0 # 0 #
0 # 0 0 0 0
0 0 0 # # 0
# # 0 0 0 G
```

| Simbol | Arti |
|---|---|
| `S` | Titik awal |
| `G` | Titik tujuan |
| `0` | Jalur yang dapat dilalui |
| `#` | Rintangan |
| `*` | Jalur yang ditemukan (muncul pada hasil) |

### Modul 2: Lokasi Kampus

| Lokasi | Koordinat | Tersambung ke |
|---|---|---|
| Gerbang | (0, 0) | Gedung A |
| Gedung A | (2, 0) | Gerbang, Gedung B, Perpustakaan |
| Gedung B | (4, 0) | Gedung A, Kantin, Laboratorium |
| Perpustakaan | (2, 2) | Gedung A, Kantin |
| Kantin | (4, 2) | Gedung B, Perpustakaan, Aula |
| Laboratorium | (6, 0) | Gedung B, Aula, Gedung C |
| Aula | (6, 2) | Kantin, Laboratorium, Gedung C |
| Gedung C | (8, 0) | Laboratorium, Aula |

## Requirement

| Kebutuhan | Keterangan |
|---|---|
| Python | Versi 3.6 atau lebih baru |
| Library tambahan | Tidak ada, hanya memakai pustaka standar (`heapq`, `collections`, `math`) |
| Sistem operasi | Windows, Linux, atau macOS |
| Terminal | Command Prompt, PowerShell, atau terminal bawaan |

Cek versi Python dengan perintah berikut:

```bash
python --version
```

## How to use

**1. Unduh proyek**

```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
```

**2. Jalankan program**

```bash
python sistem_pencarian_gabungan.py
```

Di sebagian sistem, perintahnya adalah `python3 sistem_pencarian_gabungan.py`.

**3. Pilih menu**

| Menu | Fungsi |
|---|---|
| 1 | Cari jalur terpendek pada peta grid (A\*) |
| 2 | Tampilkan peta grid awal |
| 3 | Cari jalur lokasi kampus (BFS, DFS, A\*) |
| 4 | Pengujian otomatis |
| 5 | Keluar |

**Menu 1 dan 2: Peta Grid.** Langsung berjalan tanpa input. Menu 2 hanya menampilkan peta awal, sedangkan menu 1 mencari jalur lalu menampilkannya pada peta.

**Menu 3: Lokasi Kampus.** Program meminta dua input:

| Input | Pilihan |
|---|---|
| Lokasi awal | Ketik nama lokasi: Gerbang, Gedung A, Gedung B, Perpustakaan, Kantin, Laboratorium, Aula, atau Gedung C. Huruf besar atau kecil tidak berpengaruh. |
| Lokasi tujuan | Pilihan sama dengan lokasi awal |

Hasil ditampilkan untuk ketiga algoritma sekaligus agar mudah dibandingkan.

**Menu 4: Pengujian otomatis.** Menjalankan 11 kasus uji untuk kedua modul tanpa input dari pengguna.

## Result

### 1. Peta Grid (A\*)

```text
Jalur ditemukan!
Titik awal : (0, 0)
Titik akhir: (5, 4)
Jumlah langkah: 9
Urutan jalur: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4)]

PETA HASIL PENCARIAN
S = Awal | G = Tujuan | # = Rintangan
* = Jalur yang ditemukan
S * * # 0 0
0 # * # 0 #
0 # * * * *
0 0 0 # # *
# # 0 0 0 G
```

Jalur sepanjang 9 langkah adalah yang terpendek. Ada jalur lain dengan panjang sama lewat bagian bawah peta, dan program memilih yang lewat bagian atas.

### 2. Lokasi Kampus (BFS, DFS, A\*)

**Gerbang ke Gedung C**

```text
--- BFS ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Laboratorium -> Gedung C
Jumlah langkah: 4
Total jarak: 8.00 unit

--- DFS ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Kantin -> Aula -> Laboratorium -> Gedung C
Jumlah langkah: 6
Total jarak: 12.00 unit

--- A* ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Laboratorium -> Gedung C
Jumlah langkah: 4
Total jarak: 8.00 unit
```

**Gerbang ke Aula**

```text
--- BFS ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Kantin -> Aula
Jumlah langkah: 4
Total jarak: 8.00 unit

--- DFS ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Kantin -> Aula
Jumlah langkah: 4
Total jarak: 8.00 unit

--- A* ---
Jalur: Gerbang -> Gedung A -> Gedung B -> Kantin -> Aula
Jumlah langkah: 4
Total jarak: 8.00 unit
```

Perbandingan hasil untuk rute Gerbang ke Gedung C:

| Algoritma | Jumlah langkah | Total jarak | Keterangan |
|---|---|---|---|
| BFS | 4 | 8.00 unit | Langkah paling sedikit |
| DFS | 6 | 12.00 unit | Jalur terpanjang karena hanya mengambil jalur pertama yang ditemukan |
| A\* | 4 | 8.00 unit | Jarak paling pendek |

Pada rute Gerbang ke Aula, ketiga algoritma menghasilkan jalur yang sama, sehingga selisih antaralgoritma tidak selalu muncul pada setiap rute.

### 3. Pengujian otomatis

| Modul | Kasus uji | Status |
|---|---|---|
| Peta Grid | Jalur berhasil ditemukan | LULUS |
| Peta Grid | Jalur sah (tidak menembus rintangan) | LULUS |
| Peta Grid | Biaya jalur terpendek (9 langkah) | LULUS |
| Peta Grid | Peta tanpa jalur menghasilkan hasil kosong | LULUS |
| Lokasi Kampus | BFS menghasilkan jalur sah | LULUS |
| Lokasi Kampus | DFS menghasilkan jalur sah | LULUS |
| Lokasi Kampus | A\* menghasilkan jalur sah | LULUS |
| Lokasi Kampus | BFS: langkah paling sedikit (4 langkah) | LULUS |
| Lokasi Kampus | A\*: total jarak 8.00 unit | LULUS |
| Lokasi Kampus | A\*: jarak tidak lebih panjang dari BFS dan DFS | LULUS |
| Lokasi Kampus | Lokasi awal sama dengan tujuan | LULUS |

```text
Status keseluruhan: SEMUA LULUS
```
