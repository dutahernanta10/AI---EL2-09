
import heapq
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

fasilitas = {
    "Gedung A": {
        "jenis": "diskusi",
        "wifi": 4, "tenang": 3, "kapasitas": 4
    },
    "Gedung B": {
        "jenis": "diskusi",
        "wifi": 3, "tenang": 3, "kapasitas": 3
    },
    "Perpustakaan": {
        "jenis": "fokus",
        "wifi": 5, "tenang": 5, "kapasitas": 4
    },
    "Kantin": {
        "jenis": "santai",
        "wifi": 3, "tenang": 2, "kapasitas": 5
    },
    "Laboratorium": {
        "jenis": "praktikum",
        "wifi": 4, "tenang": 3, "kapasitas": 3
    },
    "Aula": {
        "jenis": "diskusi",
        "wifi": 3, "tenang": 3, "kapasitas": 5
    },
    "Gedung C": {
        "jenis": "fokus",
        "wifi": 4, "tenang": 4, "kapasitas": 3
    }
}


def jarak(a, b):
    x1, y1 = lokasi[a]
    x2, y2 = lokasi[b]
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


class AgentNavigasi:

    def cari_rute(self, awal, tujuan):
        antrean = [(jarak(awal, tujuan), 0, awal, [awal])]
        biaya_terbaik = {awal: 0}

        while antrean:
            _, biaya, node, jalur = heapq.heappop(antrean)

            if node == tujuan:
                return jalur, biaya

            if biaya > biaya_terbaik.get(node, float("inf")):
                continue

            for tetangga in graf[node]:
                biaya_baru = biaya + jarak(node, tetangga)

                if biaya_baru < biaya_terbaik.get(
                    tetangga, float("inf")
                ):
                    biaya_terbaik[tetangga] = biaya_baru
                    estimasi = jarak(tetangga, tujuan)

                    heapq.heappush(
                        antrean,
                        (
                            biaya_baru + estimasi,
                            biaya_baru,
                            tetangga,
                            jalur + [tetangga]
                        )
                    )

        return None, float("inf")


class AgentBelajar:

    def pilih_lokasi(self, kebutuhan):
        hasil = []

        for nama, data in fasilitas.items():
            if data["jenis"] == kebutuhan:
                hasil.append(nama)

        return hasil


class AgentFasilitas:

    def nilai_lokasi(self, nama):
        data = fasilitas[nama]

        # Nilai maksimum 5
        skor = (
            data["wifi"] * 0.4
            + data["tenang"] * 0.4
            + data["kapasitas"] * 0.2
        )

        return skor


class AgentRekomendasi:

    def __init__(self):
        self.navigasi = AgentNavigasi()
        self.belajar = AgentBelajar()
        self.fasilitas = AgentFasilitas()

    def rekomendasikan(self, awal, kebutuhan):
        kandidat = self.belajar.pilih_lokasi(kebutuhan)

        if not kandidat:
            print("Tidak ada lokasi yang sesuai.")
            return

        hasil = []

        for tujuan in kandidat:
            rute, jarak_tempuh = self.navigasi.cari_rute(
                awal, tujuan
            )

            skor_fasilitas = self.fasilitas.nilai_lokasi(
                tujuan
            )

            skor_akhir = skor_fasilitas - (
                0.2 * jarak_tempuh
            )

            hasil.append({
                "lokasi": tujuan,
                "rute": rute,
                "jarak": jarak_tempuh,
                "fasilitas": skor_fasilitas,
                "skor": skor_akhir
            })

        hasil.sort(key=lambda x: x["skor"], reverse=True)

        print("\n========== HASIL MULTI-AGENT ==========")
        print("Lokasi awal:", awal)
        print("Kebutuhan belajar:", kebutuhan)

        for i, data in enumerate(hasil, start=1):
            print(f"\nPilihan {i}: {data['lokasi']}")
            print("Rute:", " -> ".join(data["rute"]))
            print(f"Jarak: {data['jarak']:.2f} unit")
            print(f"Skor fasilitas: {data['fasilitas']:.2f}")
            print(f"Skor akhir: {data['skor']:.2f}")

        terbaik = hasil[0]

        print("\n========== REKOMENDASI UTAMA ==========")
        print("Lokasi terbaik:", terbaik["lokasi"])
        print("Rute:", " -> ".join(terbaik["rute"]))
        print(f"Jarak: {terbaik['jarak']:.2f} unit")
        print(
            "Alasan: lokasi sesuai kebutuhan belajar "
            "dan memiliki skor gabungan tertinggi."
        )



def main():
    print("======================================")
    print("      SMART CAMPUS MULTI-AGENT AI")
    print("======================================")

    print("\nDaftar lokasi awal:")
    for nama in lokasi:
        print("-", nama)

    awal = input("\nMasukkan lokasi awal: ").strip()

    if awal not in lokasi:
        print("Lokasi awal tidak valid.")
        return

    print("\nPilih kebutuhan belajar:")
    print("1. Fokus belajar")
    print("2. Diskusi kelompok")
    print("3. Praktikum")
    print("4. Belajar santai")

    pilihan = input("Pilihan (1-4): ").strip()

    kebutuhan_map = {
        "1": "fokus",
        "2": "diskusi",
        "3": "praktikum",
        "4": "santai"
    }

    if pilihan not in kebutuhan_map:
        print("Pilihan tidak valid.")
        return

    kebutuhan = kebutuhan_map[pilihan]

    sistem = AgentRekomendasi()
    sistem.rekomendasikan(awal, kebutuhan)


if __name__ == "__main__":
    main()

