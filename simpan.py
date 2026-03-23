from elektronik import BarangElektronik
from habis_pakai import BarangHabisPakai
from aset_tetap import BarangAsetTetap
from manage import ManageSIMPAN

def main():
    m = ManageSIMPAN("Kantor Pusat")

    m.tambah_barang(BarangElektronik("E001", "Laptop ASUS", 8_500_000, 10, "ASUS", 24))
    m.tambah_barang(BarangElektronik("E002", "Printer Canon", 2_300_000, 5, "Canon", 12))
    m.tambah_barang(BarangHabisPakai("H001", "Tinta Printer", 85_000, 50, "Botol", "2026-12-31"))
    m.tambah_barang(BarangAsetTetap("A001", "Mesin Fotokopi", 15_000_000, 2, 2020, "Baik"))

    m.tampilkan_semua()
    m.laporan_per_kategori()

    m.ubah_harga("E001", 7_999_000)

if __name__ == "__main__":
    main()