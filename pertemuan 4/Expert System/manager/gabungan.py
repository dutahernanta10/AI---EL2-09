# ============================================================
# SISTEM PAKAR TERPADU
# Modul 1 : Diagnosis Kerusakan Perangkat Elektronik
# Modul 2 : Smart Campus - Rekomendasi Strategi Belajar
# Metode  : Forward Chaining (kedua modul)
# Bahasa  : Python 3 (tanpa library tambahan)
# File    : sistem_pakar_gabungan.py
# Jalankan: python sistem_pakar_gabungan.py
# ============================================================

from dataclasses import dataclass
from typing import FrozenSet


# ============================================================
# BAGIAN 0. FUNGSI UMUM
# ============================================================

def garis(karakter="=", panjang=60):
    print(karakter * panjang)


def tanya_ya_tidak(pertanyaan):
    """Menanyakan pertanyaan ya/tidak sampai jawaban valid."""
    while True:
        jawab = input(f"{pertanyaan} (y/n): ").strip().lower()
        if jawab in ("y", "ya"):
            return True
        if jawab in ("n", "t", "tidak"):
            return False
        print("Jawaban tidak valid. Ketik y atau n.")


# ============================================================
# BAGIAN 1. MODUL ELEKTRONIK: BASIS PENGETAHUAN
# ============================================================

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


@dataclass(frozen=True)
class Aturan:
    kode: str
    kondisi: FrozenSet[str]
    kesimpulan: str
    penjelasan: str


ATURAN = [
    Aturan("R1", frozenset({"G01", "G02"}), "D01",
           "Perangkat tidak menyala dan lampu indikator mati."),
    Aturan("R2", frozenset({"G01", "G08"}), "D02",
           "Perangkat tidak menyala dan tegangan tidak sesuai."),
    Aturan("R3", frozenset({"G03", "G06"}), "D03",
           "Indikator menyala tetapi fungsi perangkat terganggu."),
    Aturan("R4", frozenset({"G04", "G05"}), "D04",
           "Perangkat mati tiba-tiba dan mengalami panas berlebih."),
    Aturan("R5", frozenset({"G07", "G05"}), "D05",
           "Terdengar bunyi tidak normal dan perangkat panas."),
    Aturan("R6", frozenset({"G03", "G08"}), "D06",
           "Indikator menyala dan tegangan tidak sesuai."),
]


# ============================================================
# BAGIAN 2. MODUL ELEKTRONIK: INPUT, INFERENSI, OUTPUT
# ============================================================

def tampilkan_gejala():
    print("\n" + "=" * 60)
    print("DAFTAR GEJALA KERUSAKAN")
    print("=" * 60)

    for kode, deskripsi in GEJALA.items():
        print(f"{kode} - {deskripsi}")

    print("\nMasukkan kode gejala satu per satu.")
    print("Ketik SELESAI jika semua gejala sudah dipilih.")


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


def forward_chaining(fakta_awal):
    """Inference engine modul elektronik."""
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
            aturan = next(item for item in ATURAN if item.kode == kode)
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
        print("Belum ditemukan diagnosis berdasarkan aturan yang ada.")
        print(
            "Coba periksa kembali gejala atau tambahkan "
            "aturan dari sumber teknis yang tepercaya."
        )

    print("\nCatatan:")
    print(
        "Hasil adalah dugaan awal, bukan kepastian kerusakan. "
        "Lakukan pemeriksaan teknis dengan aman."
    )


def diagnosis_elektronik():
    """Menjalankan satu sesi konsultasi modul elektronik."""
    fakta = input_gejala()
    hasil, aturan_terpakai = forward_chaining(fakta)
    tampilkan_hasil(fakta, hasil, aturan_terpakai)


# ============================================================
# BAGIAN 3. MODUL SMART CAMPUS: STRUKTUR ATURAN DAN SISTEM PAKAR
# ============================================================

class Rule:
    """Mewakili satu aturan IF-THEN pada knowledge base."""

    def __init__(self, rule_id, name, conditions, conclusion, explanation):
        self.rule_id = rule_id
        self.name = name
        self.conditions = conditions
        self.conclusion = conclusion
        self.explanation = explanation


class SmartCampusExpertSystem:
    def __init__(self):
        # Working Memory: fakta yang diketahui sistem.
        self.facts = set()
        self.fact_sources = {}
        self.fired_rules = set()
        self.inference_trace = []

        # Pertanyaan untuk mengumpulkan fakta awal dari mahasiswa.
        self.questions = [
            ("difficulty_concept",
             "Apakah kamu kesulitan memahami konsep materi?"),
            ("difficulty_practice",
             "Apakah kamu kesulitan mengerjakan soal atau menerapkan materi?"),
            ("often_forget",
             "Apakah kamu sering lupa materi yang sudah dipelajari?"),
            ("limited_time",
             "Apakah waktu belajarmu terbatas?"),
            ("exam_soon",
             "Apakah ujian akan berlangsung dalam waktu dekat?"),
            ("high_target",
             "Apakah kamu menargetkan hasil akademik yang tinggi?"),
        ]
        self.fact_labels = dict(self.questions)

        # Knowledge Base: aturan IF semua kondisi terpenuhi THEN kesimpulan.
        self.rules = [
            Rule("R01", "Sulit memahami konsep",
                 ["difficulty_concept"], "need_concept_support",
                 "Mahasiswa menyatakan kesulitan memahami konsep."),
            Rule("R02", "Sulit menerapkan materi",
                 ["difficulty_practice"], "need_practice",
                 "Mahasiswa menyatakan kesulitan mengerjakan soal."),
            Rule("R03", "Sering lupa materi",
                 ["often_forget"], "need_memory_support",
                 "Mahasiswa membutuhkan strategi untuk mengingat materi."),
            Rule("R04", "Waktu belajar terbatas",
                 ["limited_time"], "need_time_management",
                 "Waktu belajar yang tersedia relatif terbatas."),
            Rule("R05", "Ujian segera berlangsung",
                 ["exam_soon"], "need_exam_preparation",
                 "Mahasiswa perlu memprioritaskan persiapan ujian."),
            Rule("R06", "Target akademik tinggi",
                 ["high_target"], "need_deeper_practice",
                 "Mahasiswa ingin mencapai target akademik yang tinggi."),

            Rule("R07", "Rekomendasi peta konsep",
                 ["need_concept_support"], "recommend_concept_map",
                 "Peta konsep membantu menyusun hubungan antarkonsep."),
            Rule("R08", "Rekomendasi teknik Feynman",
                 ["need_concept_support"], "recommend_feynman",
                 "Menjelaskan materi dengan bahasa sendiri membantu menguji pemahaman."),
            Rule("R09", "Rekomendasi latihan soal",
                 ["need_practice"], "recommend_practice",
                 "Latihan soal membantu menerapkan konsep dan menemukan kesalahan."),
            Rule("R10", "Rekomendasi active recall",
                 ["need_memory_support"], "recommend_active_recall",
                 "Active recall melatih pengambilan informasi dari ingatan."),
            Rule("R11", "Rekomendasi spaced repetition",
                 ["need_memory_support"], "recommend_spaced_repetition",
                 "Pengulangan dengan jeda membantu menyusun sesi belajar."),
            Rule("R12", "Rekomendasi jadwal belajar",
                 ["need_time_management"], "recommend_study_plan",
                 "Jadwal belajar membantu memprioritaskan waktu yang terbatas."),
            Rule("R13", "Rekomendasi simulasi ujian",
                 ["need_exam_preparation"], "recommend_mock_exam",
                 "Simulasi ujian membantu melatih pengelolaan waktu."),
            Rule("R14", "Latihan intensif untuk target tinggi",
                 ["need_deeper_practice"], "recommend_advanced_practice",
                 "Latihan bertingkat membantu menguji penguasaan materi."),
            Rule("R15", "Latihan berbatas waktu",
                 ["need_exam_preparation", "need_practice"],
                 "recommend_timed_practice",
                 "Latihan berbatas waktu menggabungkan praktik dan persiapan ujian."),
            Rule("R16", "Prioritas belajar menjelang ujian",
                 ["need_exam_preparation", "need_time_management"],
                 "recommend_priority_topics",
                 "Memilih topik prioritas membantu penggunaan waktu menjelang ujian.")
        ]

        # Penjelasan rekomendasi untuk pengguna.
        self.recommendations = {
            "recommend_concept_map": (
                "Peta Konsep",
                "Tuliskan topik utama, lalu hubungkan subtopik dengan garis dan kata kunci."
            ),
            "recommend_feynman": (
                "Teknik Feynman",
                "Jelaskan materi dengan bahasa sederhana seolah-olah kamu mengajarkannya."
            ),
            "recommend_practice": (
                "Latihan Soal Bertahap",
                "Mulai dari soal contoh, lanjut ke soal latihan, dan catat jenis "
                "kesalahan yang sering muncul."
            ),
            "recommend_active_recall": (
                "Active Recall",
                "Tutup catatan, lalu tuliskan atau ucapkan kembali poin materi "
                "dari ingatan sebelum mengecek jawabanmu."
            ),
            "recommend_spaced_repetition": (
                "Spaced Repetition",
                "Ulangi materi dengan jeda yang makin panjang, misalnya hari "
                "ke-1, ke-3, dan ke-7."
            ),
            "recommend_study_plan": (
                "Jadwal Belajar",
                "Bagi waktu belajar menjadi sesi pendek yang terukur dan "
                "tetapkan target kecil untuk setiap sesi."
            ),
            "recommend_mock_exam": (
                "Simulasi Ujian",
                "Kerjakan soal latihan dalam kondisi mirip ujian sungguhan, "
                "lalu evaluasi hasilnya."
            ),
            "recommend_advanced_practice": (
                "Latihan Tingkat Lanjut",
                "Kerjakan soal dari tingkat mudah ke sulit, termasuk soal "
                "variasi yang menuntut analisis."
            ),
            "recommend_timed_practice": (
                "Latihan Berbatas Waktu",
                "Kerjakan beberapa soal dengan batas waktu tertentu untuk "
                "melatih kecepatan dan ketepatan."
            ),
            "recommend_priority_topics": (
                "Prioritas Topik",
                "Pilih topik yang paling lemah atau paling sering keluar di "
                "ujian, lalu pelajari lebih dulu."
            ),
        }

    # --------------------------------------------------------
    # Working memory
    # --------------------------------------------------------

    def reset(self):
        """Mengosongkan working memory untuk sesi konsultasi baru."""
        self.facts = set()
        self.fact_sources = {}
        self.fired_rules = set()
        self.inference_trace = []

    def add_fact(self, fact, source="input pengguna"):
        """Menambah fakta. Mengembalikan True jika fakta benar-benar baru."""
        if fact in self.facts:
            return False
        self.facts.add(fact)
        self.fact_sources[fact] = source
        return True

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    def ask_user(self):
        print("\n" + "=" * 60)
        print("KONSULTASI STRATEGI BELAJAR - SMART CAMPUS")
        print("=" * 60)
        print("Jawab pertanyaan berikut dengan y (ya) atau n (tidak).\n")

        for fact, pertanyaan in self.questions:
            if tanya_ya_tidak(pertanyaan):
                self.add_fact(fact, "input pengguna")

    # --------------------------------------------------------
    # Inference engine: forward chaining
    # --------------------------------------------------------

    def run_inference(self):
        changed = True

        while changed:
            changed = False

            for rule in self.rules:
                if rule.rule_id in self.fired_rules:
                    continue

                if all(cond in self.facts for cond in rule.conditions):
                    self.fired_rules.add(rule.rule_id)
                    self.inference_trace.append(rule)

                    if self.add_fact(rule.conclusion, rule.rule_id):
                        changed = True

    def get_recommendations(self):
        """Daftar kode rekomendasi yang dihasilkan, urut sesuai aturan."""
        hasil = []
        for rule in self.rules:
            kode = rule.conclusion
            if (kode.startswith("recommend_")
                    and kode in self.facts
                    and kode not in hasil):
                hasil.append(kode)
        return hasil

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    def show_result(self):
        print("\n" + "=" * 60)
        print("HASIL ANALISIS SISTEM PAKAR")
        print("=" * 60)

        print("\nKondisi yang kamu pilih:")
        kondisi = [
            f for f, sumber in self.fact_sources.items()
            if sumber == "input pengguna"
        ]
        if kondisi:
            for fact in kondisi:
                print(f"- {self.fact_labels.get(fact, fact)}")
        else:
            print("- Tidak ada kondisi yang dipilih.")

        print("\nAturan yang terpenuhi:")
        if self.inference_trace:
            for rule in self.inference_trace:
                print(f"- {rule.rule_id} ({rule.name}): {rule.explanation}")
        else:
            print("- Tidak ada aturan yang terpenuhi.")

        print("\nRekomendasi strategi belajar:")
        rekomendasi = self.get_recommendations()
        if rekomendasi:
            for nomor, kode in enumerate(rekomendasi, start=1):
                judul, deskripsi = self.recommendations[kode]
                print(f"\n{nomor}. {judul}")
                print(f"   {deskripsi}")
        else:
            print("Belum ada rekomendasi. Coba pilih minimal satu kondisi.")

    def consult(self):
        """Menjalankan satu sesi konsultasi penuh."""
        self.reset()
        self.ask_user()
        self.run_inference()
        self.show_result()


# ============================================================
# BAGIAN 4. PENGUJIAN OTOMATIS (KEDUA MODUL)
# ============================================================

def uji_modul_elektronik():
    kasus_uji = [
        ("Uji E1 - Catu daya", {"G01", "G02"}, {"D01"}),
        ("Uji E2 - Panas berlebih", {"G04", "G05"}, {"D04"}),
        ("Uji E3 - Rangkaian kontrol", {"G03", "G06"}, {"D03"}),
        ("Uji E4 - Tidak ada aturan cocok", set(), set()),
    ]

    print("\n--- Modul 1: Diagnosis Elektronik ---")
    semua_lulus = True

    for nama, fakta_uji, diharapkan in kasus_uji:
        hasil, _ = forward_chaining(fakta_uji)
        lulus = hasil == diharapkan
        print(f"{nama}: {'LULUS' if lulus else 'GAGAL'}")
        print(f"  Diharapkan : {diharapkan}")
        print(f"  Diperoleh  : {hasil}")
        if not lulus:
            semua_lulus = False

    return semua_lulus


def uji_modul_campus():
    kasus_uji = [
        ("Uji C1 - Sulit konsep",
         {"difficulty_concept"},
         {"recommend_concept_map", "recommend_feynman"}),
        ("Uji C2 - Ujian dekat dan sulit soal",
         {"exam_soon", "difficulty_practice"},
         {"recommend_mock_exam", "recommend_practice",
          "recommend_timed_practice"}),
        ("Uji C3 - Ujian dekat dan waktu terbatas",
         {"exam_soon", "limited_time"},
         {"recommend_mock_exam", "recommend_study_plan",
          "recommend_priority_topics"}),
        ("Uji C4 - Tidak ada kondisi",
         set(),
         set()),
    ]

    print("\n--- Modul 2: Smart Campus ---")
    semua_lulus = True

    for nama, fakta_uji, diharapkan in kasus_uji:
        sistem = SmartCampusExpertSystem()
        for fakta in fakta_uji:
            sistem.add_fact(fakta, "input pengguna")
        sistem.run_inference()

        hasil = set(sistem.get_recommendations())
        lulus = hasil == diharapkan
        print(f"{nama}: {'LULUS' if lulus else 'GAGAL'}")
        print(f"  Diharapkan : {sorted(diharapkan)}")
        print(f"  Diperoleh  : {sorted(hasil)}")
        if not lulus:
            semua_lulus = False

    return semua_lulus


def jalankan_pengujian():
    print("\n" + "=" * 60)
    print("PENGUJIAN OTOMATIS")
    print("=" * 60)

    lulus_elektronik = uji_modul_elektronik()
    lulus_campus = uji_modul_campus()

    print(
        "\nStatus keseluruhan:",
        "SEMUA LULUS" if (lulus_elektronik and lulus_campus)
        else "ADA UJI GAGAL"
    )


# ============================================================
# BAGIAN 5. MENU UTAMA
# ============================================================

def main():
    campus = SmartCampusExpertSystem()

    while True:
        print("\n" + "=" * 60)
        print("SISTEM PAKAR TERPADU")
        print("Metode Inferensi: FORWARD CHAINING")
        print("=" * 60)
        print("1. Diagnosis kerusakan perangkat elektronik")
        print("2. Konsultasi strategi belajar (Smart Campus)")
        print("3. Lihat daftar gejala elektronik")
        print("4. Jalankan pengujian otomatis")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            diagnosis_elektronik()

        elif pilihan == "2":
            campus.consult()

        elif pilihan == "3":
            tampilkan_gejala()

        elif pilihan == "4":
            jalankan_pengujian()

        elif pilihan == "5":
            print("Program selesai. Terima kasih.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 1 sampai 5.")


# ============================================================
# BAGIAN 6. MENJALANKAN PROGRAM
# ============================================================

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
