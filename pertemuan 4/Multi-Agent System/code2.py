
# ==========================================================
# PROYEK 2: MULTI-AGENT SYSTEM
# Simulasi Koordinasi Robot Pengiriman
# ==========================================================

from dataclasses import dataclass


# 1. DATA AGEN ROBOT
@dataclass
class Agent:
    nama: str
    x: int
    y: int
    kapasitas: int
    status: str = "Siap"
    tugas: str = "-"


# 2. DATA TUGAS PENGIRIMAN
@dataclass
class Task:
    nama: str
    tujuan_x: int
    tujuan_y: int
    berat: int
    status: str = "Menunggu"
    agen: str = "-"


# 3. MEMBUAT AGEN
agents = [
    Agent("Robot-A", 0, 0, 5),
    Agent("Robot-B", 5, 0, 3),
    Agent("Robot-C", 2, 4, 8),
]


# 4. MEMBUAT TUGAS
tasks = [
    Task("Paket-1", 3, 2, 2),
    Task("Paket-2", 6, 1, 4),
    Task("Paket-3", 1, 5, 6),
]


# 5. FUNGSI MENGHITUNG JARAK MANHATTAN
def jarak(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# 6. MEMILIH AGEN TERBAIK UNTUK TUGAS
def pilih_agen(task, daftar_agen):
    kandidat = []

    for agent in daftar_agen:
        # Agen hanya dapat mengambil tugas jika siap
        # dan kapasitasnya mencukupi.
        if (
            agent.status == "Siap"
            and agent.kapasitas >= task.berat
        ):
            d = jarak(
                agent.x,
                agent.y,
                task.tujuan_x,
                task.tujuan_y,
            )

            kandidat.append((d, agent))

    if not kandidat:
        return None

    # Pilih agen dengan jarak terpendek.
    # Nama digunakan sebagai pemecah seri yang konsisten.
    kandidat.sort(key=lambda item: (item[0], item[1].nama))

    return kandidat[0][1]


# 7. AGEN MENGERJAKAN TUGAS
def jalankan_tugas(task, agent):
    if agent is None:
        print(f"{task.nama}: tidak ada agen yang memenuhi syarat.")
        return False

    jarak_tempuh = jarak(
        agent.x,
        agent.y,
        task.tujuan_x,
        task.tujuan_y,
    )

    print(f"\n{agent.nama} mengambil {task.nama}")
    print(f"Berat paket : {task.berat}")
    print(f"Jarak       : {jarak_tempuh} satuan")

    # Simulasi pengiriman langsung sampai tujuan
    agent.x = task.tujuan_x
    agent.y = task.tujuan_y
    agent.status = "Mengirim"
    agent.tugas = task.nama

    task.agen = agent.nama
    task.status = "Selesai"

    print(f"Status      : {task.status}")

    # Agen siap kembali untuk tugas berikutnya
    agent.status = "Siap"
    agent.tugas = "-"

    return True


# 8. KOORDINASI MULTI-AGEN
def koordinasi():
    print("=" * 55)
    print("SIMULASI MULTI-AGENT SYSTEM")
    print("=" * 55)

    for task in tasks:
        print(f"\nMemproses tugas: {task.nama}")

        agent = pilih_agen(task, agents)

        if agent:
            jalankan_tugas(task, agent)
        else:
            print(
                f"Tugas {task.nama} belum dapat dikerjakan. "
                "Kapasitas atau ketersediaan agen tidak mencukupi."
            )

    tampilkan_laporan()


# 9. LAPORAN AKHIR
def tampilkan_laporan():
    print("\n" + "=" * 55)
    print("LAPORAN AKHIR PENGIRIMAN")
    print("=" * 55)

    for task in tasks:
        print(
            f"{task.nama} | "
            f"Status: {task.status} | "
            f"Agen: {task.agen}"
        )

    print("\nKondisi akhir agen:")
    for agent in agents:
        print(
            f"{agent.nama} | "
            f"Posisi: ({agent.x}, {agent.y}) | "
            f"Kapasitas: {agent.kapasitas} | "
            f"Status: {agent.status}"
        )

    selesai = sum(task.status == "Selesai" for task in tasks)
    total = len(tasks)

    print(f"\nTugas selesai: {selesai}/{total}")


# 10. PENGUJIAN PEMILIHAN AGEN
def pengujian():
    print("\nPENGUJIAN SISTEM MULTI-AGEN")

    # Paket berbobot 7 hanya dapat dibawa Robot-C.
    paket_uji = Task("Paket-Uji", 0, 0, 7)
    hasil = pilih_agen(paket_uji, agents)

    if hasil is not None and hasil.nama == "Robot-C":
        print("Tes kapasitas: LULUS")
    else:
        print("Tes kapasitas: GAGAL")

    # Paket dengan berat melebihi seluruh kapasitas
    # seharusnya tidak memperoleh agen.
    paket_besar = Task("Paket-Besar", 0, 0, 100)
    hasil_besar = pilih_agen(paket_besar, agents)

    if hasil_besar is None:
        print("Tes paket melebihi kapasitas: LULUS")
    else:
        print("Tes paket melebihi kapasitas: GAGAL")


# 11. MENU UTAMA
def main():
    while True:
        print("\n=== MULTI-AGENT SYSTEM ===")
        print("1. Jalankan simulasi")
        print("2. Pengujian")
        print("3. Keluar")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            koordinasi()

        elif pilihan == "2":
            pengujian()

        elif pilihan == "3":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()

