
import heapq
from collections import deque
from math import sqrt

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


def jarak(a, b):
    x1, y1 = lokasi[a]
    x2, y2 = lokasi[b]
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def bfs(start, tujuan):
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


def dfs(start, tujuan):
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


def astar(start, tujuan):
    antrean = [(0, 0, start, [start])]
    biaya_terbaik = {start: 0}

    while antrean:
        _, biaya, node, jalur = heapq.heappop(antrean)

        if node == tujuan:
            return jalur

        if biaya > biaya_terbaik.get(node, float("inf")):
            continue

        for tetangga in graf[node]:
            biaya_baru = biaya + jarak(node, tetangga)

            if biaya_baru < biaya_terbaik.get(
                tetangga, float("inf")
            ):
                biaya_terbaik[tetangga] = biaya_baru

                # Heuristik: jarak garis lurus ke tujuan
                h = jarak(tetangga, tujuan)
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
        jarak(jalur[i], jalur[i + 1])
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


def main():
    print("=" * 45)
    print("       SMART CAMPUS AI")
    print("   SISTEM PENCARIAN LOKASI KAMPUS")
    print("=" * 45)

    print("\nDaftar lokasi:")
    for nama in lokasi:
        print("-", nama)

    start = input("\nMasukkan lokasi awal: ").strip()
    tujuan = input("Masukkan lokasi tujuan: ").strip()

    if start not in lokasi or tujuan not in lokasi:
        print("\nLokasi tidak valid. Periksa penulisan nama.")
        return

    print("\nMencari jalur...")

    tampilkan_hasil("BFS", bfs(start, tujuan))
    tampilkan_hasil("DFS", dfs(start, tujuan))
    tampilkan_hasil("A*", astar(start, tujuan))


if __name__ == "__main__":
    main()

