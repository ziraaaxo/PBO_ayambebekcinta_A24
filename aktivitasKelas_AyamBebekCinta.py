# ============================================================
# JAWABAN LANGKAH 1 - Identifikasi Pelanggaran SOLID
# ============================================================

# a) Prinsip yang dilanggar:

# 1. SRP (Single Responsibility Principle)
#    → karena satu class memiliki banyak tanggung jawab sekaligus.
#
#    Bagian yang salah:
#    - simpan_nilai()      → tugas penyimpanan data
#    - hitung_ipk()        → tugas perhitungan IPK
#    - kirim_notifikasi()  → tugas pengiriman notifikasi
#    - cetak_laporan()     → tugas pembuatan laporan
#
#    Semua method tersebut berada dalam satu class:
#    class SistemNilaiKampus
#
#    Seharusnya:
#    tiap tanggung jawab dipisah ke class berbeda.

# 2. OCP (Open/Closed Principle)
#    → karena setiap penambahan fitur baru harus mengubah
#      kode lama menggunakan if-elif.
#
#    Bagian yang salah:
#
#    Pada method kirim_notifikasi():
#
#    if via == "email":
#    elif via == "sms":
#    elif via == "whatsapp":
#
#    Jika ingin menambah Telegram atau LINE,
#    maka method lama harus diedit lagi.
#
#    Pada method cetak_laporan():
#
#    if format_file == "pdf":
#    elif format_file == "excel":
#
#    Jika ingin menambah CSV atau DOCX,
#    maka method lama juga harus diubah.

# 3. DIP (Dependency Inversion Principle)
#    → karena class bergantung langsung pada implementasi konkret,
#      bukan abstraksi/interface.
#
#    Bagian yang salah:
#
#    print(f"[Email] ...")
#    print(f"[SMS] ...")
#
#    Sistem utama langsung mengatur detail notifikasi,
#    sehingga coupling menjadi tinggi dan sulit dikembangkan.
#
#    Seharusnya:
#    sistem hanya bergantung pada abstraksi seperti:
#    class Notifikasi

from abc import ABC, abstractmethod

# ============================================================
# REPOSITORY NILAI
# ============================================================

class RepoNilai:

    def __init__(self):
        self.data_nilai = {}

    # sesuai verifikasi
    def simpan(self, nim, matkul, nilai):

        if nim not in self.data_nilai:
            self.data_nilai[nim] = {}

        self.data_nilai[nim][matkul] = nilai

    # sesuai verifikasi
    def ambil(self, nim):

        return self.data_nilai.get(nim, {})


# ============================================================
# HITUNG IPK
# ============================================================

class HitungIPK:

    # sesuai verifikasi
    def dari_nilai(self, data_nilai):

        nilai_list = list(data_nilai.values())

        if not nilai_list:
            return 0.0

        # konversi nilai 0-100 menjadi IPK 0-4
        return sum(nilai_list) / len(nilai_list) / 25


# ============================================================
# ABSTRACT CLASS NOTIFIKASI
# ============================================================

class Notifikasi:

    def kirim(self, nim, pesan):
        raise NotImplementedError


# ============================================================
# NOTIFIKASI EMAIL
# ============================================================

class NotifikasiEmail(Notifikasi):

    def kirim(self, nim, pesan):

        print(f"[Email] Ke {nim}@student.unmul.ac.id : {pesan}")

        return True


# ============================================================
# NOTIFIKASI SMS
# ============================================================

class NotifikasiSMS(Notifikasi):

    def kirim(self, nim, pesan):

        print(f"[SMS] Ke 0812-xxxx ({nim}) : {pesan}")

        return True


# ============================================================
# BONUS: NOTIFIKASI WHATSAPP
# ============================================================

class NotifikasiWhatsApp(Notifikasi):

    def kirim(self, nim, pesan):

        print(f"[WA] Ke 0812-xxxx ({nim}) : {pesan}")

        return True


# ============================================================
# CETAK LAPORAN
# ============================================================

class CetakLaporan:

    def cetak_pdf(self, nim, ipk):

        print(f"[PDF] Laporan {nim} | IPK: {ipk:.2f}")

    def cetak_excel(self, nim, ipk):

        print(f"[XLS] Laporan {nim} | IPK: {ipk:.2f}")


# ============================================================
# SISTEM UTAMA
# ============================================================

class SistemNilaiKampus:

    def __init__(self):

        self.repo = RepoNilai()
        self.hitung_ipk = HitungIPK()
        self.laporan = CetakLaporan()

    def simpan_nilai(self, nim, matkul, nilai):

        self.repo.simpan(nim, matkul, nilai)

    def hitung_ipk_mahasiswa(self, nim):

        data_nilai = self.repo.ambil(nim)

        return self.hitung_ipk.dari_nilai(data_nilai)

    def kirim_notifikasi(self, layanan_notifikasi, nim, pesan):

        return layanan_notifikasi.kirim(nim, pesan)

    def cetak_pdf(self, nim):

        ipk = self.hitung_ipk_mahasiswa(nim)

        self.laporan.cetak_pdf(nim, ipk)

    def cetak_excel(self, nim):

        ipk = self.hitung_ipk_mahasiswa(nim)

        self.laporan.cetak_excel(nim, ipk)


# ============================================================
# CONTOH PENGGUNAAN
# ============================================================

sistem = SistemNilaiKampus()

# simpan nilai
sistem.simpan_nilai("2301001", "RPL", 85)
sistem.simpan_nilai("2301001", "PBO", 90)

# hitung IPK
ipk = sistem.hitung_ipk_mahasiswa("2301001")

print(f"IPK Mahasiswa: {ipk:.2f}")

# kirim notifikasi
email = NotifikasiEmail()
sms = NotifikasiSMS()

sistem.kirim_notifikasi(email, "2301001", "Nilai sudah keluar")
sistem.kirim_notifikasi(sms, "2301001", "Silakan cek portal akademik")

# cetak laporan
sistem.cetak_pdf("2301001")
sistem.cetak_excel("2301001")


# ============================================================
# VERIFIKASI - Jalankan file ini, semua baris harus [OK]
# ============================================================
print("=" * 50)
print("VERIFIKASI AKTIVITAS KELAS - SOLID")
print("=" * 50)

# Cek 1: Ada kelas terpisah untuk menyimpan/mengambil nilai
try:
    repo = RepoNilai()
    repo.simpan("2301001", "RPL", 85)
    repo.simpan("2301001", "PBO", 90)
    nilai = repo.ambil("2301001")
    assert isinstance(nilai, dict)
    assert nilai.get("RPL") == 85
    print("[OK] RepoNilai: simpan dan ambil nilai berfungsi")
except NameError:
    print("[--] RepoNilai belum dibuat")
except Exception as e:
    print(f"[X]  RepoNilai: {e}")

# Cek 2: Ada kelas terpisah untuk hitung IPK
try:
    hitung = HitungIPK()
    ipk = hitung.dari_nilai({"RPL": 85, "PBO": 90})
    assert 3.4 <= ipk <= 3.6, f"IPK tidak sesuai: {ipk}"
    print("[OK] HitungIPK: perhitungan IPK berfungsi")
except NameError:
    print("[--] HitungIPK belum dibuat")
except Exception as e:
    print(f"[X]  HitungIPK: {e}")

# Cek 3: Ada kelas terpisah untuk notifikasi (minimal 1 channel)
try:
    notif = NotifikasiEmail()
    hasil = notif.kirim("2301001", "Nilai sudah keluar")
    assert hasil is True
    print("[OK] NotifikasiEmail: pengiriman notifikasi berfungsi")
except NameError:
    print("[--] NotifikasiEmail belum dibuat")
except Exception as e:
    print(f"[X]  NotifikasiEmail: {e}")

# Cek 4: Menambah channel notifikasi BARU tidak mengubah kelas lama
try:
    # Jika OCP diterapkan, kelas baru ini bisa dibuat tanpa ubah yang lama
    notif2 = NotifikasiSMS()
    hasil2 = notif2.kirim("2301001", "Nilai sudah keluar")
    assert hasil2 is True
    print("[OK] NotifikasiSMS: channel baru bisa ditambah tanpa ubah kelas lama")
except NameError:
    print("[--] NotifikasiSMS belum dibuat (bonus)")
except Exception as e:
    print(f"[X]  NotifikasiSMS: {e}")

print("=" * 50)
print("Selesai! Diskusikan hasilnya bersama kelompok.")