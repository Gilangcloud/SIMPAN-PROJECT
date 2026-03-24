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
    m.tampilkan_pringatan_kadaluarsa(7)
    m.laporan_per_kategori()

    print("\nMelakukan perubahan harga...")
    m.ubah_harga("E001", 7_999_000)
    m.ubah_harga("E001", 7_500_000)

    m.tampilkan_riwayat_harga("E001")
    m.tampilkan_riwayat_harga("X999")
    
    try:
        excel_file = m.export_to_excel()
    except Exception as e:
        print(f"Error saat export: {e}")

    # Test cek stok menipis
    print("\nCek stok menipis (batas 10):")
    try:
        m.cek_stok_menipis(10)
    except Exception as e:
        print(f"Error saat cek stok menipis: {e}")

    # Test validasi barang dengan data benar
    print("\nTest validasi barang baru:")
    try:
        barang_valid = BarangElektronik("E003", "Monitor LG", 3_000_000, 8, "LG", 12)
        m.validasi_barang(barang_valid)
        print("Barang valid berhasil dicek.")
    except Exception as e:
        print(f"Error validasi barang: {e}")

    print("\nTest validasi barang kode duplikat:")
    try:
        barang_duplikat = BarangElektronik("E001", "Laptop HP", 9_000_000, 5, "HP", 24)
        m.validasi_barang(barang_duplikat)
    except Exception as e:
        print(f"Validasi berhasil mendeteksi error: {e}")

    print("\nTest validasi stok tidak valid:")
    try:
        barang_stok_salah = BarangElektronik("E004", "Mouse Logitech", 150_000, -5, "Logitech", 12)
        m.validasi_barang(barang_stok_salah)
    except Exception as e:
        print(f"Validasi berhasil mendeteksi error: {e}")

if __name__ == "__main__":
    main()