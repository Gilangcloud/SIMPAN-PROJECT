from datetime import datetime, date, timedelta
from barang import Barang
from habis_pakai import BarangHabisPakai
from mixin import LogMixin, ValidasiMixin
from export_mixin import ExportMixin

class ManageSIMPAN(LogMixin, ValidasiMixin, ExportMixin ):
    def __init__(self, nama_instansi:str ):
        self.__nama_instansi = nama_instansi
        self.__daftar_barang = []
    
    @property
    def nama_instansi(self):return self.__nama_instansi

    @property
    def jumlah_barang(self):return len(self.__daftar_barang)

    def tambah_barang(self, barang:Barang):
        if self.cari_id(barang.id_barang):
            raise ValueError(f"ID {barang.id_barang} Sudah Ada")
        self.__daftar_barang.append(barang)
        self.log_aktivitas("TAMBAH BARANG", f"{barang.kategori()} | {barang.nama}")

    def hapus_barang(self, id_barang: str):
        barang = self.cari_id(id_barang)
        if not barang:
            raise ValueError(f"ID '{id_barang}' tidak ditemukan!")
        self.__daftar_barang.remove(barang)
        self.log_aktivitas("HAPUS BARANG", f"{barang.nama}")
    
    def ubah_harga(self, id_barang: str, harga_baru: float):
        barang = self.cari_id(id_barang)
        if not barang:
            raise ValueError(f"ID '{id_barang}' tidak ditemukan!")
        harga_lama = barang.harga
        barang.harga = harga_baru
        self.log_aktivitas("UBAH HARGA", f"{barang.nama} Rp{harga_lama:,.0f} → Rp{harga_baru:,.0f}")
    
    def cari_id(self, id_barang: str):
        for b in self.__daftar_barang:
            if b.id_barang == id_barang:
                return b
        return None
    
    def cari_nama(self, keyword: str):
        return [b for b in self.__daftar_barang
                if keyword.lower() in b.nama.lower()]
    
    def filter_kategori(self, kategori: str):
        return [b for b in self.__daftar_barang
                if b.kategori() == kategori]
    
    def tampilkan_semua(self):
        print(f"\n{'='*60}")
        print(f"  SIMPAN — {self.__nama_instansi}")
        print(f"{'='*60}")
        if not self.__daftar_barang:
            print("  (Belum ada barang)")
        for b in self.__daftar_barang:
            print(f"  {b.info_detail()}")
        print(f"{'='*60}")
        print(f"  Total barang : {self.jumlah_barang}")
        print(f"  Total nilai  : Rp{self.total_nilai():,.0f}")
        print(f"{'='*60}\n")
    
    def total_nilai(self):
        return sum(b.hitung_nilai() for b in self.__daftar_barang)
    
    def laporan_per_kategori(self):
        print(f"\n{'='*60}")
        print(f"  LAPORAN PER KATEGORI — {self.__nama_instansi}")
        print(f"{'='*60}")
        kategori_list = set(b.kategori() for b in self.__daftar_barang)
        for kat in sorted(kategori_list):
            items = self.filter_kategori(kat)
            nilai = sum(b.hitung_nilai() for b in items)
            print(f"  {kat:20s} : {len(items):3d} barang | Rp{nilai:,.0f}")
        print(f"{'─'*60}")
        print(f"  {'TOTAL':20s} : {self.jumlah_barang:3d} barang | Rp{self.total_nilai():,.0f}")
        print(f"{'='*60}\n")

    def _get_export_data(self):
        """Implementasi method untuk ExportMixin"""
        headers = ["ID", "Nama", "Kategori", "Harga (Rp)", "Stok", "Nilai Total (Rp)", "Detail"]
        rows = []
        for barang in self.__daftar_barang:
            detail = ""
            if barang.kategori() == "Elektronik":
                detail = f"{barang.merek} | Garansi {barang.garansi_bulan} bln"
            elif barang.kategori() == "Habis Pakai":
                status = "KADALUARSA" if barang.sudah_kadaluarsa() else "Baik"
                detail = f"{barang.satuan} | Exp: {barang.tgl_kadaluarsa} | {status}"
            elif barang.kategori() == "Aset Tetap":
                detail = f"Tahun {barang.tahun_beli} | Umur {barang.umur_aset()} thn | {barang.kondisi}"
            rows.append([barang.id_barang, barang.nama, barang.kategori(), barang.harga, barang.stok, barang.hitung_nilai(), detail])
        return {'title': f'Laporan Inventori - {self.__nama_instansi}', 'headers': headers, 'rows': rows, 'currency_columns': [4, 6]}
    
    def filter_kadaluarsa(self, sisa_hari=0):
        hasil = []
        target_tanggal = date.today() + timedelta(days=sisa_hari)

        for b in self.__daftar_barang:
            if isinstance(b, BarangHabisPakai):
                tgl_exp = date.fromisoformat(b.tgl_kadaluarsa)
                if tgl_exp <= target_tanggal:
                    hasil.append(b)

        return hasil
    
    def tampilkan_pringatan_kadaluarsa(self, hari_peringatan=7):
        print(f"\n{'!'* 60}")
        print(f"PERINGATAN KADALUARSA (H-{hari_peringatan})")
        print(f"{'!'* 60}")

        barang_beresiko = self.filter_kadaluarsa(hari_peringatan)

        if not barang_beresiko:
            print("(Aman : Tidak ada barang yang mendekati masa kadaluarsa)")
        else:
            for b in barang_beresiko:
                status = "SUDAH EXP" if b.sudah_kadaluarsa() else "AKAN EXP"
                print(f" {status} | {b.id_barang} | {b.nama} |Exp:{b.tgl_kadaluarsa}")

        print(f"{'!'*60}\n")
