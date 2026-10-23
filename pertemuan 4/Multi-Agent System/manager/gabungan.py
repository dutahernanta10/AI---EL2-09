# ==========================================================
# SISTEM MULTI-AGENT TERPADU
# Modul 1 : Smart Campus Multi-Agent (rekomendasi lokasi belajar)
# Modul 2 : Simulasi Koordinasi Robot Pengiriman
# Bahasa  : Python 3 (tanpa library tambahan)
# File    : sistem_multi_agent_gabungan.py
# Jalankan: python sistem_multi_agent_gabungan.py
# ==========================================================

import heapq
from dataclasses import dataclass
from math import sqrt


# ==========================================================
# BAGIAN 1. MODUL SMART CAMPUS: DATA
# ==========================================================

# Koordinat tiap lokasi di kampus
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

# Graf jalan antarlokasi
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

# Data fasilitas tiap lokasi belajar (skala 1-5)
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


def jarak_lokasi(a, b):
    """Jarak Euclidean antara dua lokasi kampus (berdasarkan nama)."""
    x1, y1 = lokasi[a]
    x2, y2 = lokasi[b]
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


# ==========================================================
# BAGIAN 2. MODUL SMART CAMPUS: AGEN
# ==========================================================

class AgentNavigasi:
    """Agen pencari rute terpendek dengan algoritma A*."""

    def cari_rute(self, awal, tujuan):
        antrean = [(jarak_lokasi(awal, tujuan), 0, awal, [awal])]
        biaya_terbaik = {awal: 0}

        while antrean:
            _, biaya, node, jalur = heapq.heappop(antrean)

            if node == tujuan:
                return jalur, biaya

            if biaya > biaya_terbaik.get(node, float("inf")):
                continue

            for tetangga in graf[node]:
                biaya_baru = biaya + jarak_lokasi(node, tetangga)

                if biaya_baru < biaya_terbaik.get(
                    tetangga, float("inf")
                ):
                    biaya_terbaik[tetangga] = biaya_baru
                    estimasi = jarak_lokasi(tetangga, tujuan)

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
    """Agen penyeleksi lokasi sesuai kebutuhan belajar."""

    def pilih_lokasi(self, kebutuhan):
        hasil = []

        for nama, data in fasilitas.items():
            if data["jenis"] == kebutuhan:
                hasil.append(nama)

        return hasil


class AgentFasilitas:
    """Agen penilai kualitas fasilitas suatu lokasi."""

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
    """Agen koordinator yang menggabungkan hasil ketiga agen lain."""

    def __init__(self):
        self.navigasi = AgentNavigasi()
        self.belajar = AgentBelajar()
        self.fasilitas = AgentFasilitas()

    def hitung_rekomendasi(self, awal, kebutuhan):
        """Mengembalikan daftar kandidat, urut dari skor tertinggi."""
        kandidat = self.belajar.pilih_lokasi(kebutuhan)
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
        return hasil

    def rekomendasikan(self, awal, kebutuhan):
        hasil = self.hitung_rekomendasi(awal, kebutuhan)

        if not hasil:
            print("Tidak ada lokasi yang sesuai.")
            return

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


def jalankan_smart_campus():
    """Satu sesi interaksi modul Smart Campus."""
    print("\n======================================")
    print("      SMART CAMPUS MULTI-AGENT AI")
    print("======================================")

    print("\nDaftar lokasi awal:")
    for nama in lokasi:
        print("-", nama)

    masukan = input("\nMasukkan lokasi awal: ").strip()

    # Pencocokan tidak membedakan huruf besar/kecil
    pencocokan = {nama.lower(): nama for nama in lokasi}
    awal = pencocokan.get(masukan.lower())

    if awal is None:
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


# ==========================================================
# BAGIAN 3. MODUL ROBOT PENGIRIMAN: DATA AGEN DAN TUGAS
# ==========================================================

@dataclass
class AgenRobot:
    nama: str
    x: int
    y: int
    kapasitas: int
    status: str = "Siap"
    tugas: str = "-"


@dataclass
class TugasPengiriman:
    nama: str
    tujuan_x: int
    tujuan_y: int
    berat: int
    status: str = "Menunggu"
    agen: str = "-"


def buat_agen():
    """Membuat daftar robot baru (kondisi awal)."""
    return [
        AgenRobot("Robot-A", 0, 0, 5),
        AgenRobot("Robot-B", 5, 0, 3),
        AgenRobot("Robot-C", 2, 4, 8),
    ]


def buat_tugas():
    """Membuat daftar tugas baru (kondisi awal)."""
    return [
        TugasPengiriman("Paket-1", 3, 2, 2),
        TugasPengiriman("Paket-2", 6, 1, 4),
        TugasPengiriman("Paket-3", 1, 5, 6),
    ]


# ==========================================================
# BAGIAN 4. MODUL ROBOT PENGIRIMAN: LOGIKA AGEN
# ==========================================================

def jarak_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def pilih_agen(tugas, daftar_agen):
    """Memilih robot siap dengan kapasitas cukup dan jarak terdekat."""
    kandidat = []

    for agen in daftar_agen:
        # Agen hanya dapat mengambil tugas jika siap
        # dan kapasitasnya mencukupi.
        if agen.status == "Siap" and agen.kapasitas >= tugas.berat:
            d = jarak_manhattan(
                agen.x,
                agen.y,
                tugas.tujuan_x,
                tugas.tujuan_y,
            )

            kandidat.append((d, agen))

    if not kandidat:
        return None

    # Pilih agen dengan jarak terpendek.
    # Nama digunakan sebagai pemecah seri yang konsisten.
    kandidat.sort(key=lambda item: (item[0], item[1].nama))

    return kandidat[0][1]


def jalankan_tugas(tugas, agen):
    if agen is None:
        print(f"{tugas.nama}: tidak ada agen yang memenuhi syarat.")
        return False

    jarak_tempuh = jarak_manhattan(
        agen.x,
        agen.y,
        tugas.tujuan_x,
        tugas.tujuan_y,
    )

    print(f"\n{agen.nama} mengambil {tugas.nama}")
    print(f"Berat paket : {tugas.berat}")
    print(f"Jarak       : {jarak_tempuh} satuan")

    # Simulasi pengiriman langsung sampai tujuan
    agen.x = tugas.tujuan_x
    agen.y = tugas.tujuan_y
    agen.status = "Mengirim"
    agen.tugas = tugas.nama

    tugas.agen = agen.nama
    tugas.status = "Selesai"

    print(f"Status      : {tugas.status}")

    # Agen siap kembali untuk tugas berikutnya
    agen.status = "Siap"
    agen.tugas = "-"

    return True


def tampilkan_laporan(daftar_tugas, daftar_agen):
    print("\n" + "=" * 55)
    print("LAPORAN AKHIR PENGIRIMAN")
    print("=" * 55)

    for tugas in daftar_tugas:
        print(
            f"{tugas.nama} | "
            f"Status: {tugas.status} | "
            f"Agen: {tugas.agen}"
        )

    print("\nKondisi akhir agen:")
    for agen in daftar_agen:
        print(
            f"{agen.nama} | "
            f"Posisi: ({agen.x}, {agen.y}) | "
            f"Kapasitas: {agen.kapasitas} | "
            f"Status: {agen.status}"
        )

    selesai = sum(t.status == "Selesai" for t in daftar_tugas)
    total = len(daftar_tugas)

    print(f"\nTugas selesai: {selesai}/{total}")


def koordinasi():
    """Satu sesi simulasi. Data dibuat baru agar hasilnya konsisten."""
    daftar_agen = buat_agen()
    daftar_tugas = buat_tugas()

    print("\n" + "=" * 55)
    print("SIMULASI MULTI-AGENT SYSTEM: ROBOT PENGIRIMAN")
    print("=" * 55)

    for tugas in daftar_tugas:
        print(f"\nMemproses tugas: {tugas.nama}")

        agen = pilih_agen(tugas, daftar_agen)

        if agen:
            jalankan_tugas(tugas, agen)
        else:
            print(
                f"Tugas {tugas.nama} belum dapat dikerjakan. "
                "Kapasitas atau ketersediaan agen tidak mencukupi."
            )

    tampilkan_laporan(daftar_tugas, daftar_agen)


# ==========================================================
# BAGIAN 5. PENGUJIAN OTOMATIS (KEDUA MODUL)
# ==========================================================

def cek(nama, kondisi):
    """Mencetak status satu kasus uji dan mengembalikan hasilnya."""
    print(f"{nama}: {'LULUS' if kondisi else 'GAGAL'}")
    return kondisi


def uji_smart_campus():
    print("\n--- Modul 1: Smart Campus ---")
    hasil = []

    navigasi = AgentNavigasi()
    rute, biaya = navigasi.cari_rute("Gerbang", "Perpustakaan")
    hasil.append(cek(
        "Tes rute Gerbang -> Perpustakaan",
        rute == ["Gerbang", "Gedung A", "Perpustakaan"]
        and abs(biaya - 4.0) < 1e-9
    ))

    _, biaya = navigasi.cari_rute("Gerbang", "Gedung C")
    hasil.append(cek(
        "Tes jarak Gerbang -> Gedung C",
        abs(biaya - 8.0) < 1e-9
    ))

    hasil.append(cek(
        "Tes seleksi lokasi 'fokus'",
        AgentBelajar().pilih_lokasi("fokus")
        == ["Perpustakaan", "Gedung C"]
    ))

    hasil.append(cek(
        "Tes skor fasilitas Perpustakaan",
        abs(AgentFasilitas().nilai_lokasi("Perpustakaan") - 4.8) < 1e-9
    ))

    rekomendasi = AgentRekomendasi().hitung_rekomendasi(
        "Gerbang", "fokus"
    )
    hasil.append(cek(
        "Tes rekomendasi terbaik dari Gerbang (fokus)",
        rekomendasi[0]["lokasi"] == "Perpustakaan"
    ))

    return all(hasil)


def uji_robot():
    print("\n--- Modul 2: Robot Pengiriman ---")
    hasil = []
    daftar_agen = buat_agen()

    hasil.append(cek(
        "Tes jarak Manhattan",
        jarak_manhattan(0, 0, 3, 2) == 5
    ))

    # Paket berbobot 7 hanya dapat dibawa Robot-C.
    paket_uji = TugasPengiriman("Paket-Uji", 0, 0, 7)
    agen = pilih_agen(paket_uji, daftar_agen)
    hasil.append(cek(
        "Tes kapasitas",
        agen is not None and agen.nama == "Robot-C"
    ))

    # Paket melebihi seluruh kapasitas tidak boleh mendapat agen.
    paket_besar = TugasPengiriman("Paket-Besar", 0, 0, 100)
    hasil.append(cek(
        "Tes paket melebihi kapasitas",
        pilih_agen(paket_besar, daftar_agen) is None
    ))

    # Paket ringan dipilihkan robot terdekat dari tujuan.
    paket_dekat = TugasPengiriman("Paket-Dekat", 3, 2, 2)
    agen = pilih_agen(paket_dekat, daftar_agen)
    hasil.append(cek(
        "Tes robot terdekat",
        agen is not None and agen.nama == "Robot-C"
    ))

    return all(hasil)


def jalankan_pengujian():
    print("\n" + "=" * 55)
    print("PENGUJIAN OTOMATIS")
    print("=" * 55)

    lulus_campus = uji_smart_campus()
    lulus_robot = uji_robot()

    print(
        "\nStatus keseluruhan:",
        "SEMUA LULUS" if (lulus_campus and lulus_robot)
        else "ADA UJI GAGAL"
    )


# ==========================================================
# BAGIAN 6. MENU UTAMA
# ==========================================================

def main():
    while True:
        print("\n" + "=" * 55)
        print("SISTEM MULTI-AGENT TERPADU")
        print("=" * 55)
        print("1. Smart Campus (rekomendasi lokasi belajar)")
        print("2. Simulasi koordinasi robot pengiriman")
        print("3. Pengujian otomatis")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == "1":
            jalankan_smart_campus()

        elif pilihan == "2":
            koordinasi()

        elif pilihan == "3":
            jalankan_pengujian()

        elif pilihan == "4":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 1 sampai 4.")


# ==========================================================
# BAGIAN 7. MENJALANKAN PROGRAM
# ==========================================================

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
