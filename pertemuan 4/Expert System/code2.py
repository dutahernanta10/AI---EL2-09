
# ============================================================
# SISTEM PAKAR DIAGNOSIS KERUSAKAN PERANGKAT ELEKTRONIK
# Metode: Forward Chaining
# Bahasa: Python 3
# File: main.py
# ============================================================

from dataclasses import dataclass
from typing import FrozenSet


# ------------------------------------------------------------
# 1. BASIS PENGETAHUAN: DAFTAR GEJALA
# ------------------------------------------------------------

GEJALA = {
    "G01": "Perangkat tidak menyala",
    "G02": "Lampu indikator mati",
    "G03": "Lampu indikator menyala",
    "G04": "Perangkat mati secara tiba-tiba",
    "G05": "Perangkat terlalu panas",
    "G06": "Perangkat menyala tetapi tidak berfungsi normal",
    "G07": "Terdengar bunyi tidak normal",
    "G08": "Tegangan catu daya tidak sesuai",
}


# ------------------------------------------------------------
# 2. BASIS PENGETAHUAN: HASIL DIAGNOSIS
# ------------------------------------------------------------

DIAGNOSIS = {
    "D01": {
        "nama": "Dugaan masalah catu daya",
        "saran": (
            "Periksa sumber listrik, kabel, konektor, "
            "sekring, dan rangkaian catu daya."
        ),
    },
    "D02": {
        "nama": "Dugaan gangguan suplai tegangan",
        "saran": (
            "Periksa tegangan masukan dan keluaran catu daya "
            "menggunakan alat ukur yang sesuai."
        ),
    },
    "D03": {
        "nama": "Dugaan kerusakan rangkaian kontrol",
        "saran": (
            "Periksa koneksi, sinyal kontrol, dan komponen "
            "pada rangkaian kontrol."
        ),
    },
    "D04": {
        "nama": "Dugaan panas berlebih",
        "saran": (
            "Matikan perangkat, biarkan dingin, lalu periksa "
            "ventilasi, kipas, dan sistem pendinginan."
        ),
    },
    "D05": {
        "nama": "Dugaan masalah komponen atau mekanis",
        "saran": (
            "Periksa sumber bunyi dan kondisi komponen "
            "sesuai prosedur keselamatan perangkat."
        ),
    },
    "D06": {
        "nama": "Dugaan tegangan suplai tidak normal",
        "saran": (
            "Periksa spesifikasi tegangan dan kestabilan "
            "catu daya sebelum perangkat digunakan kembali."
        ),
    },
}


# ------------------------------------------------------------
# 3. STRUKTUR ATURAN IF-THEN
# ------------------------------------------------------------

@dataclass(frozen=True)
class Aturan:
    kode: str
    kondisi: FrozenSet[str]
    kesimpulan: str
    penjelasan: str


ATURAN = [
    Aturan(
        "R1",
        frozenset({"G01", "G02"}),
        "D01",
        "Perangkat tidak menyala dan lampu indikator mati."
    ),
    Aturan(
        "R2",
        frozenset({"G01", "G08"}),
        "D02",
        "Perangkat tidak menyala dan tegangan tidak sesuai."
    ),
    Aturan(
        "R3",
        frozenset({"G03", "G06"}),
        "D03",
        "Indikator menyala tetapi fungsi perangkat terganggu."
    ),
    Aturan(
        "R4",
        frozenset({"G04", "G05"}),
        "D04",
        "Perangkat mati tiba-tiba dan mengalami panas berlebih."
    ),
    Aturan(
        "R5",
        frozenset({"G07", "G05"}),
        "D05",
        "Terdengar bunyi tidak normal dan perangkat panas."
    ),
    Aturan(
        "R6",
        frozenset({"G03", "G08"}),
        "D06",
        "Indikator menyala dan tegangan tidak sesuai."
    ),
]


# ------------------------------------------------------------
# 4. FUNGSI MENAMPILKAN MENU GEJALA
# ------------------------------------------------------------

def tampilkan_gejala():
    print("\n" + "=" * 60)
    print("DAFTAR GEJALA KERUSAKAN")
    print("=" * 60)

    for kode, deskripsi in GEJALA.items():
        print(f"{kode} - {deskripsi}")

    print("\nMasukkan kode gejala satu per satu.")
    print("Ketik SELESAI jika semua gejala sudah dipilih.")


# ------------------------------------------------------------
# 5. INPUT DAN VALIDASI GEJALA
# ------------------------------------------------------------

def input_gejala():
    fakta = set()

    tampilkan_gejala()

    while True:
        pilihan = input("\nKode gejala: ").strip().upper()

        if pilihan == "SELESAI":
            break

        if pilihan not in GEJALA:
            print("Kode tidak valid. Silakan pilih G01 sampai G08.")
            continue

        if pilihan in fakta:
            print("Gejala sudah dipilih sebelumnya.")
            continue

        fakta.add(pilihan)
        print(f"Gejala ditambahkan: {GEJALA[pilihan]}")

    return fakta


# ------------------------------------------------------------
# 6. INFERENCE ENGINE: FORWARD CHAINING
# ------------------------------------------------------------

def forward_chaining(fakta_awal):
    fakta = set(fakta_awal)
    aturan_terpakai = []
    hasil = set()

    # Fakta baru diperiksa sampai tidak ada kesimpulan baru.
    berubah = True

    while berubah:
        berubah = False

        for aturan in ATURAN:
            # Jika seluruh kondisi aturan terpenuhi
            if aturan.kondisi.issubset(fakta):

                # Hindari menggunakan aturan yang sama berulang kali
                if aturan.kode not in aturan_terpakai:
                    aturan_terpakai.append(aturan.kode)

                # Tambahkan kesimpulan jika belum ada
                if aturan.kesimpulan not in fakta:
                    fakta.add(aturan.kesimpulan)
                    hasil.add(aturan.kesimpulan)
                    berubah = True

    return hasil, aturan_terpakai


# ------------------------------------------------------------
# 7. MENAMPILKAN HASIL DIAGNOSIS
# ------------------------------------------------------------

def tampilkan_hasil(fakta, hasil, aturan_terpakai):
    print("\n" + "=" * 60)
    print("HASIL ANALISIS SISTEM PAKAR")
    print("=" * 60)

    print("\nGejala yang dipilih:")

    if fakta:
        for kode in sorted(fakta):
            if kode in GEJALA:
                print(f"- {kode}: {GEJALA[kode]}")
    else:
        print("- Tidak ada gejala yang dimasukkan.")

    print("\nAturan yang terpenuhi:")

    if aturan_terpakai:
        for kode in aturan_terpakai:
            aturan = next(
                item for item in ATURAN
                if item.kode == kode
            )
            print(f"- {kode}: {aturan.penjelasan}")
    else:
        print("- Tidak ada aturan yang terpenuhi.")

    print("\nKesimpulan:")

    if hasil:
        for nomor, kode in enumerate(sorted(hasil), start=1):
            data = DIAGNOSIS[kode]

            print(f"\n{nomor}. {data['nama']}")
            print(f"   Saran: {data['saran']}")
    else:
        print(
            "Belum ditemukan diagnosis berdasarkan aturan yang ada."
        )
        print(
            "Coba periksa kembali gejala atau tambahkan "
            "aturan dari sumber teknis yang tepercaya."
        )

    print("\nCatatan:")
    print(
        "Hasil adalah dugaan awal, bukan kepastian kerusakan. "
        "Lakukan pemeriksaan teknis dengan aman."
    )


# ------------------------------------------------------------
# 8. FITUR PENGUJIAN OTOMATIS
# ------------------------------------------------------------

def jalankan_pengujian():
    kasus_uji = [
        (
            "Uji 1 - Catu daya",
            {"G01", "G02"},
            {"D01"},
        ),
        (
            "Uji 2 - Panas berlebih",
            {"G04", "G05"},
            {"D04"},
        ),
        (
            "Uji 3 - Rangkaian kontrol",
            {"G03", "G06"},
            {"D03"},
        ),
        (
            "Uji 4 - Tidak ada aturan cocok",
            set(),
            set(),
        ),
    ]

    print("\n" + "=" * 60)
    print("PENGUJIAN OTOMATIS")
    print("=" * 60)

    semua_lulus = True

    for nama, fakta_uji, hasil_yang_diharapkan in kasus_uji:
        hasil, _ = forward_chaining(fakta_uji)

        lulus = hasil == hasil_yang_diharapkan
        status = "LULUS" if lulus else "GAGAL"

        print(f"{nama}: {status}")
        print(f"  Diharapkan : {hasil_yang_diharapkan}")
        print(f"  Diperoleh  : {hasil}")

        if not lulus:
            semua_lulus = False

    print(
        "\nStatus keseluruhan:",
        "SEMUA LULUS" if semua_lulus else "ADA UJI GAGAL"
    )


# ------------------------------------------------------------
# 9. MENU UTAMA PROGRAM
# ------------------------------------------------------------

def main():
    while True:
        print("\n" + "=" * 60)
        print("SISTEM PAKAR DIAGNOSIS KERUSAKAN ELEKTRONIK")
        print("Metode Inferensi: FORWARD CHAINING")
        print("=" * 60)
        print("1. Diagnosis kerusakan")
        print("2. Lihat daftar gejala")
        print("3. Jalankan pengujian otomatis")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == "1":
            fakta = input_gejala()
            hasil, aturan_terpakai = forward_chaining(fakta)
            tampilkan_hasil(fakta, hasil, aturan_terpakai)

        elif pilihan == "2":
            tampilkan_gejala()

        elif pilihan == "3":
            jalankan_pengujian()

        elif pilihan == "4":
            print("Program selesai. Terima kasih.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 1 sampai 4.")


# ------------------------------------------------------------
# 10. MENJALANKAN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")

