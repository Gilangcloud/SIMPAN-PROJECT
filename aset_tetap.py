from barang import Barang
from datetime import date

class BarangAsetTetap(Barang):
    def __init__(self, id_barang, nama, harga, stok, tahun_beli, kondisi):
        super().__init__(id_barang, nama, harga, stok)
        self.__tahun_beli = tahun_beli
        self.__kondisi = kondisi

    @property
    def tahun_beli(self): return self.__tahun_beli

    @property
    def kondisi(self): return self.__kondisi

    @kondisi.setter
    def kondisi(self, nilai):
        pilihan = ["Baik", "Rusak Ringan", "Rusak Berat"]
        if nilai not in pilihan:
            raise ValueError(f"Kondisi harus salah satu dari: {pilihan}")
        self.__kondisi = nilai

    def umur_aset(self):
        from datetime import date
        return date.today().year - self.__tahun_beli

    def kategori(self): return "Aset Tetap"

    def hitung_nilai(self):
        faktor = max(0, 1 - (0.10 * self.umur_aset()))
        return self.harga * self.stok * faktor

    def info_detail(self):
        return (f"[ASET TETAP] {self.id_barang} | {self.nama} | "
            f"Tahun Beli: {self.__tahun_beli} | Umur: {self.umur_aset()} thn | "
            f"Kondisi: {self.__kondisi} | Harga: Rp{self.harga:,.0f} | "
            f"Stok: {self.stok}")