
# ==========================================================
# PROYEK 3: AI ALGORITHM SYSTEM
# Pencarian Jalur Terpendek dengan A*
# ==========================================================

import heapq


# 1. PETA GRID
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


# 2. MENEMUKAN POSISI AWAL DAN TUJUAN
def cari_posisi(grid, simbol):
    for y, baris in enumerate(grid):
        for x, nilai in enumerate(baris):
            if nilai == simbol:
                return (x, y)

    raise ValueError(f"Simbol {simbol} tidak ditemukan.")


# 3. HEURISTIK MANHATTAN
def heuristik(posisi, tujuan):
    x1, y1 = posisi
    x2, y2 = tujuan

    return abs(x1 - x2) + abs(y1 - y2)


# 4. MEMERIKSA APAKAH POSISI VALID
def posisi_valid(grid, x, y):
    tinggi = len(grid)
    lebar = len(grid[0])

    if x < 0 or x >= lebar:
        return False

    if y < 0 or y >= tinggi:
        return False

    if grid[y][x] == 1:
        return False

    return True


# 5. MENCARI TETANGGA
def cari_tetangga(grid, posisi):
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

        if posisi_valid(grid, nx, ny):
            tetangga.append((nx, ny))

    return tetangga


# 6. ALGORITMA A*
def astar(grid, awal, tujuan):
    # Priority queue berisi (f_score, urutan, posisi)
    # Nomor urutan menghindari perbandingan posisi
    # ketika nilai prioritas sama.
    antrian = []
    urutan = 0

    heapq.heappush(
        antrian,
        (heuristik(awal, tujuan), urutan, awal)
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

        for tetangga in cari_tetangga(grid, sekarang):
            if tetangga in selesai:
                continue

            biaya_baru = g_score[sekarang] + 1

            if biaya_baru < g_score.get(tetangga, float("inf")):
                asal[tetangga] = sekarang
                g_score[tetangga] = biaya_baru

                f_score = (
                    biaya_baru
                    + heuristik(tetangga, tujuan)
                )

                urutan += 1

                heapq.heappush(
                    antrian,
                    (f_score, urutan, tetangga)
                )

    return None, None


# 7. REKONSTRUKSI JALUR
def rekonstruksi_jalur(asal, sekarang):
    jalur = [sekarang]

    while sekarang in asal:
        sekarang = asal[sekarang]
        jalur.append(sekarang)

    jalur.reverse()
    return jalur


# 8. MENAMPILKAN PETA DAN JALUR
def tampilkan_peta(grid, jalur):
    hasil = [baris.copy() for baris in grid]

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


# 9. PENGUJIAN ALGORITMA
def pengujian():
    awal = cari_posisi(grid, "S")
    tujuan = cari_posisi(grid, "G")

    jalur, biaya = astar(grid, awal, tujuan)

    print("\nPENGUJIAN ALGORITMA A*")

    if jalur is None:
        print("Tes pencarian jalur: GAGAL")
        print("Tidak ada jalur yang dapat ditemukan.")
    else:
        print("Tes pencarian jalur: LULUS")
        print(f"Jalur ditemukan: {jalur}")
        print(f"Biaya jalur: {biaya} langkah")


# 10. MENU UTAMA
def main():
    while True:
        print("\n=== AI ALGORITHM SYSTEM ===")
        print("1. Cari jalur terpendek")
        print("2. Tampilkan peta awal")
        print("3. Pengujian algoritma")
        print("4. Keluar")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            awal = cari_posisi(grid, "S")
            tujuan = cari_posisi(grid, "G")

            jalur, biaya = astar(grid, awal, tujuan)

            if jalur is None:
                print("Tidak ditemukan jalur menuju tujuan.")
            else:
                print("\nJalur ditemukan!")
                print(f"Titik awal : {awal}")
                print(f"Titik akhir: {tujuan}")
                print(f"Jumlah langkah: {biaya}")
                print(f"Urutan jalur: {jalur}")

                tampilkan_peta(grid, jalur)

        elif pilihan == "2":
            tampilkan_peta(grid, None)

        elif pilihan == "3":
            pengujian()

        elif pilihan == "4":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()


