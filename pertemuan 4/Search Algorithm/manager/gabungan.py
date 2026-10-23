
# ==========================================================
# SISTEM ALGORITMA PENCARIAN TERPADU
# Modul 1 : Pencarian jalur terpendek pada peta grid (A*)
# Modul 2 : Pencarian jalur lokasi kampus (BFS, DFS, A*)
# Bahasa  : Python 3 (tanpa library tambahan)
# File    : sistem_pencarian_gabungan.py
# Jalankan: python sistem_pencarian_gabungan.py
# ==========================================================

import heapq
from collections import deque
from math import sqrt


# ==========================================================
# BAGIAN 1. MODUL GRID: DATA PETA
# ==========================================================

# 0 = jalur yang dapat dilalui
# 1 = rintangan
# S = titik awal
# G = titik tujuan
grid = [
    ["S", 0,   0,   1,   0,   0],
    [0,   1,   0,   1,   0,   1],
    [0,   1,   0,   0,   0,   0],
    [0,   0,   0,   1,   1,   0],
    [1,   1,   0,   0,   0,   "G"],
]


# ==========================================================
# BAGIAN 2. MODUL GRID: ALGORITMA A*
# ==========================================================

def cari_posisi(peta, simbol):
    """Menemukan posisi (x, y) dari simbol S atau G pada peta."""
    for y, baris in enumerate(peta):
        for x, nilai in enumerate(baris):
            if nilai == simbol:
                return (x, y)

    raise ValueError(f"Simbol {simbol} tidak ditemukan.")


def heuristik_grid(posisi, tujuan):
    """Heuristik jarak Manhattan."""
    x1, y1 = posisi
    x2, y2 = tujuan

    return abs(x1 - x2) + abs(y1 - y2)


def posisi_valid(peta, x, y):
    tinggi = len(peta)
    lebar = len(peta[0])

    if x < 0 or x >= lebar:
        return False

    if y < 0 or y >= tinggi:
        return False

    if peta[y][x] == 1:
        return False

    return True


def cari_tetangga(peta, posisi):
    x, y = posisi

    # Gerakan: kanan, kiri, bawah, atas
    arah = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    tetangga = []

    for dx, dy in arah:
        nx = x + dx
        ny = y + dy

        if posisi_valid(peta, nx, ny):
            tetangga.append((nx, ny))

    return tetangga


def rekonstruksi_jalur(asal, sekarang):
    jalur = [sekarang]

    while sekarang in asal:
        sekarang = asal[sekarang]
        jalur.append(sekarang)

    jalur.reverse()
    return jalur


def astar_grid(peta, awal, tujuan):
    """A* pada grid. Mengembalikan (jalur, biaya) atau (None, None)."""
    # Priority queue berisi (f_score, urutan, posisi)
    # Nomor urutan menghindari perbandingan posisi
    # ketika nilai prioritas sama.
    antrian = []
    urutan = 0

    heapq.heappush(
        antrian,
        (heuristik_grid(awal, tujuan), urutan, awal)
    )

    # Menyimpan asal setiap titik untuk merekonstruksi jalur
    asal = {}

    # Biaya terbaik dari awal menuju setiap titik
    g_score = {awal: 0}

    # Titik yang sudah diproses
    selesai = set()

    while antrian:
        _, _, sekarang = heapq.heappop(antrian)

        if sekarang in selesai:
            continue

        if sekarang == tujuan:
            return rekonstruksi_jalur(asal, sekarang), g_score[sekarang]

        selesai.add(sekarang)

        for tetangga in cari_tetangga(peta, sekarang):
            if tetangga in selesai:
                continue

            biaya_baru = g_score[sekarang] + 1

            if biaya_baru < g_score.get(tetangga, float("inf")):
                asal[tetangga] = sekarang
                g_score[tetangga] = biaya_baru

                f_score = biaya_baru + heuristik_grid(tetangga, tujuan)

                urutan += 1

                heapq.heappush(
                    antrian,
                    (f_score, urutan, tetangga)
                )

    return None, None


def tampilkan_peta(peta, jalur):
    hasil = [baris.copy() for baris in peta]

    if jalur:
        for x, y in jalur:
            if hasil[y][x] not in ("S", "G"):
                hasil[y][x] = "*"

    print("\nPETA HASIL PENCARIAN")
    print("S = Awal | G = Tujuan | # = Rintangan")
    print("* = Jalur yang ditemukan")

    for baris in hasil:
        simbol = []

        for nilai in baris:
            if nilai == 1:
                simbol.append("#")
            else:
                simbol.append(str(nilai))

        print(" ".join(simbol))


def jalankan_pencarian_grid():
    awal = cari_posisi(grid, "S")
    tujuan = cari_posisi(grid, "G")

    jalur, biaya = astar_grid(grid, awal, tujuan)

    if jalur is None:
        print("Tidak ditemukan jalur menuju tujuan.")
    else:
        print("\nJalur ditemukan!")
        print(f"Titik awal : {awal}")
        print(f"Titik akhir: {tujuan}")
        print(f"Jumlah langkah: {biaya}")
        print(f"Urutan jalur: {jalur}")

        tampilkan_peta(grid, jalur)


# ==========================================================
# BAGIAN 3. MODUL KAMPUS: DATA GRAF
# ==========================================================

lokasi = {
    "Gerbang": (0, 0),
    "Gedung A": (2, 0),
    "Gedung B": (4, 0),
    "Perpustakaan": (2, 2),
    "Kantin": (4, 2),
    "Laboratorium": (6, 0),
    "Aula": (6, 2),
    "Gedung C": (8, 0)
}

graf = {
    "Gerbang": ["Gedung A"],
    "Gedung A": ["Gerbang", "Gedung B", "Perpustakaan"],
    "Gedung B": ["Gedung A", "Kantin", "Laboratorium"],
    "Perpustakaan": ["Gedung A", "Kantin"],
    "Kantin": ["Gedung B", "Perpustakaan", "Aula"],
    "Laboratorium": ["Gedung B", "Aula", "Gedung C"],
    "Aula": ["Kantin", "Laboratorium", "Gedung C"],
    "Gedung C": ["Laboratorium", "Aula"]
}


def jarak_lokasi(a, b):
    """Jarak Euclidean (garis lurus) antara dua lokasi kampus."""
    x1, y1 = lokasi[a]
    x2, y2 = lokasi[b]
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


# ==========================================================
# BAGIAN 4. MODUL KAMPUS: ALGORITMA BFS, DFS, A*
# ==========================================================

def bfs_kampus(start, tujuan):
    """Breadth-First Search: jalur dengan jumlah langkah paling sedikit."""
    antrean = deque([[start]])
    dikunjungi = {start}

    while antrean:
        jalur = antrean.popleft()
        node = jalur[-1]

        if node == tujuan:
            return jalur

        for tetangga in graf[node]:
            if tetangga not in dikunjungi:
                dikunjungi.add(tetangga)
                antrean.append(jalur + [tetangga])

    return None


def dfs_kampus(start, tujuan):
    """Depth-First Search: jalur pertama yang ditemukan."""
    tumpukan = [[start]]
    dikunjungi = set()

    while tumpukan:
        jalur = tumpukan.pop()
        node = jalur[-1]

        if node == tujuan:
            return jalur

        if node not in dikunjungi:
            dikunjungi.add(node)

            for tetangga in reversed(graf[node]):
                if tetangga not in dikunjungi:
                    tumpukan.append(jalur + [tetangga])

    return None


def astar_kampus(start, tujuan):
    """A*: jalur dengan total jarak paling pendek."""
    antrean = [(0, 0, start, [start])]
    biaya_terbaik = {start: 0}

    while antrean:
        _, biaya, node, jalur = heapq.heappop(antrean)

        if node == tujuan:
            return jalur

        if biaya > biaya_terbaik.get(node, float("inf")):
            continue

        for tetangga in graf[node]:
            biaya_baru = biaya + jarak_lokasi(node, tetangga)

            if biaya_baru < biaya_terbaik.get(
                tetangga, float("inf")
            ):
                biaya_terbaik[tetangga] = biaya_baru

                # Heuristik: jarak garis lurus ke tujuan
                h = jarak_lokasi(tetangga, tujuan)
                f = biaya_baru + h

                heapq.heappush(
                    antrean,
                    (f, biaya_baru, tetangga,
                     jalur + [tetangga])
                )

    return None


def total_jarak(jalur):
    if not jalur or len(jalur) < 2:
        return 0

    return sum(
        jarak_lokasi(jalur[i], jalur[i + 1])
        for i in range(len(jalur) - 1)
    )


def tampilkan_hasil(nama, jalur):
    print(f"\n--- {nama} ---")

    if jalur:
        print("Jalur:", " -> ".join(jalur))
        print("Jumlah langkah:", len(jalur) - 1)
        print(f"Total jarak: {total_jarak(jalur):.2f} unit")
    else:
        print("Jalur tidak ditemukan.")


def jalankan_pencarian_kampus():
    print("\n" + "=" * 45)
    print("       SMART CAMPUS AI")
    print("   SISTEM PENCARIAN LOKASI KAMPUS")
    print("=" * 45)

    print("\nDaftar lokasi:")
    for nama in lokasi:
        print("-", nama)

    # Pencocokan tidak membedakan huruf besar/kecil
    pencocokan = {nama.lower(): nama for nama in lokasi}

    start = pencocokan.get(
        input("\nMasukkan lokasi awal: ").strip().lower()
    )
    tujuan = pencocokan.get(
        input("Masukkan lokasi tujuan: ").strip().lower()
    )

    if start is None or tujuan is None:
        print("\nLokasi tidak valid. Periksa penulisan nama.")
        return

    print("\nMencari jalur...")

    tampilkan_hasil("BFS", bfs_kampus(start, tujuan))
    tampilkan_hasil("DFS", dfs_kampus(start, tujuan))
    tampilkan_hasil("A*", astar_kampus(start, tujuan))


# ==========================================================
# BAGIAN 5. PENGUJIAN OTOMATIS (KEDUA MODUL)
# ==========================================================

def cek(nama, kondisi):
    """Mencetak status satu kasus uji dan mengembalikan hasilnya."""
    print(f"{nama}: {'LULUS' if kondisi else 'GAGAL'}")
    return kondisi


def jalur_grid_valid(peta, jalur, awal, tujuan):
    """Memeriksa jalur grid: berawal di S, berakhir di G, tiap langkah sah."""
    if not jalur or jalur[0] != awal or jalur[-1] != tujuan:
        return False

    for a, b in zip(jalur, jalur[1:]):
        if b not in cari_tetangga(peta, a):
            return False

    return True


def jalur_graf_valid(jalur, start, tujuan):
    """Memeriksa jalur graf: berawal di start, berakhir di tujuan."""
    if not jalur or jalur[0] != start or jalur[-1] != tujuan:
        return False

    for a, b in zip(jalur, jalur[1:]):
        if b not in graf[a]:
            return False

    return True


def uji_grid():
    print("\n--- Modul 1: A* pada Grid ---")
    hasil = []

    awal = cari_posisi(grid, "S")
    tujuan = cari_posisi(grid, "G")
    jalur, biaya = astar_grid(grid, awal, tujuan)

    hasil.append(cek(
        "Tes pencarian jalur",
        jalur is not None
    ))
    hasil.append(cek(
        "Tes jalur sah (tidak menembus rintangan)",
        jalur_grid_valid(grid, jalur, awal, tujuan)
    ))
    hasil.append(cek(
        "Tes biaya jalur terpendek (9 langkah)",
        biaya == 9 and len(jalur) - 1 == 9
    ))

    # Peta yang tujuannya terhalang rintangan harus gagal.
    peta_buntu = [["S", 1, "G"]]
    jalur_buntu, _ = astar_grid(
        peta_buntu,
        cari_posisi(peta_buntu, "S"),
        cari_posisi(peta_buntu, "G"),
    )
    hasil.append(cek(
        "Tes peta tanpa jalur",
        jalur_buntu is None
    ))

    return all(hasil)


def uji_kampus():
    print("\n--- Modul 2: BFS, DFS, A* Kampus ---")
    hasil = []

    awal, tujuan = "Gerbang", "Gedung C"
    jalur_bfs = bfs_kampus(awal, tujuan)
    jalur_dfs = dfs_kampus(awal, tujuan)
    jalur_astar = astar_kampus(awal, tujuan)

    hasil.append(cek(
        "Tes BFS: jalur sah",
        jalur_graf_valid(jalur_bfs, awal, tujuan)
    ))
    hasil.append(cek(
        "Tes DFS: jalur sah",
        jalur_graf_valid(jalur_dfs, awal, tujuan)
    ))
    hasil.append(cek(
        "Tes A*: jalur sah",
        jalur_graf_valid(jalur_astar, awal, tujuan)
    ))
    hasil.append(cek(
        "Tes BFS: langkah paling sedikit (4 langkah)",
        len(jalur_bfs) - 1 == 4
    ))
    hasil.append(cek(
        "Tes A*: total jarak 8.00 unit",
        abs(total_jarak(jalur_astar) - 8.0) < 1e-9
    ))
    hasil.append(cek(
        "Tes A*: jarak tidak lebih panjang dari BFS dan DFS",
        total_jarak(jalur_astar) <= total_jarak(jalur_bfs) + 1e-9
        and total_jarak(jalur_astar) <= total_jarak(jalur_dfs) + 1e-9
    ))
    hasil.append(cek(
        "Tes lokasi awal sama dengan tujuan",
        bfs_kampus("Aula", "Aula") == ["Aula"]
    ))

    return all(hasil)


def jalankan_pengujian():
    print("\n" + "=" * 55)
    print("PENGUJIAN OTOMATIS")
    print("=" * 55)

    lulus_grid = uji_grid()
    lulus_kampus = uji_kampus()

    print(
        "\nStatus keseluruhan:",
        "SEMUA LULUS" if (lulus_grid and lulus_kampus)
        else "ADA UJI GAGAL"
    )


# ==========================================================
# BAGIAN 6. MENU UTAMA
# ==========================================================

def main():
    while True:
        print("\n" + "=" * 55)
        print("SISTEM ALGORITMA PENCARIAN TERPADU")
        print("=" * 55)
        print("1. Cari jalur terpendek pada peta grid (A*)")
        print("2. Tampilkan peta grid awal")
        print("3. Cari jalur lokasi kampus (BFS, DFS, A*)")
        print("4. Pengujian otomatis")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            jalankan_pencarian_grid()

        elif pilihan == "2":
            tampilkan_peta(grid, None)

        elif pilihan == "3":
            jalankan_pencarian_kampus()

        elif pilihan == "4":
            jalankan_pengujian()

        elif pilihan == "5":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 1 sampai 5.")


# ==========================================================
# BAGIAN 7. MENJALANKAN PROGRAM
# ==========================================================

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
