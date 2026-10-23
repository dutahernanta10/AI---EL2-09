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
