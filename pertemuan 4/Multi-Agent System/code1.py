class StudentAgent:
    """Agen yang menyampaikan keadaan dan kebutuhan mahasiswa."""

    def perceive(self):
        difficulty = self._ask_choice(
            "Kesulitan utama mahasiswa:",
            [
                ("1", "Memahami konsep"),
                ("2", "Mengerjakan soal"),
                ("3", "Mengingat materi"),
            ],
        )
        difficulty_map = {
            "1": "konsep",
            "2": "soal",
            "3": "ingatan",
        }
        days = self._ask_nonnegative_int(
            "Berapa hari lagi menuju ujian? (0 jika hari ini): "
        )
        hours = self._ask_choice(
            "Waktu belajar yang tersedia per hari:",
            [
                ("1", "Kurang dari 1 jam"),
                ("2", "1 sampai 2 jam"),
                ("3", "Lebih dari 2 jam"),
            ],
        )
        hours_map = {"1": "sedikit", "2": "sedang", "3": "banyak"}
        return {
            "difficulty": difficulty_map[difficulty],
            "days_until_exam": days,
            "study_time": hours_map[hours],
        }

    @staticmethod
    def _ask_choice(question, options):
        while True:
            print("\n" + question)
            for key, label in options:
                print(f"  {key}. {label}")
            answer = input("Pilih nomor: ").strip()
            if answer in {key for key, _ in options}:
                return answer
            print("Pilihan tidak valid. Coba lagi.")

    @staticmethod
    def _ask_nonnegative_int(question):
        while True:
            try:
                value = int(input(question).strip())
                if value >= 0:
                    return value
                print("Masukkan angka 0 atau lebih.")
            except ValueError:
                print("Input harus berupa bilangan bulat.")


class TutorAgent:
    """Agen tutor memilih bantuan sesuai kesulitan mahasiswa."""

    def act(self, student_state):
        difficulty = student_state["difficulty"]
        if difficulty == "konsep":
            return {
                "method": "Peta konsep dan Teknik Feynman",
                "tasks": [
                    "Buat peta konsep dari satu topik.",
                    "Jelaskan topik dengan bahasa sendiri.",
                    "Tandai bagian yang belum bisa dijelaskan.",
                ],
                "reason": "Fokusnya adalah memperkuat pemahaman konsep.",
            }
        if difficulty == "soal":
            return {
                "method": "Latihan soal bertahap",
                "tasks": [
                    "Kerjakan 3 soal dasar.",
                    "Kerjakan 2 soal penerapan.",
                    "Tinjau kesalahan dan tulis penyebabnya.",
