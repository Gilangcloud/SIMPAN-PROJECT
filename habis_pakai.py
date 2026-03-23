from barang import Barang
from datetime import date

class BarangHabisPakai(Barang):
    def __init__(self, id_barang, nama, harga, stok, satuan, tgl_kadaluarsa):
        super().__init__(id_barang, nama, harga, stok)
        self.__satuan = satuan
        self.__tgl_kadaluarsa = tgl_kadaluarsa

    @property
    def satuan(self): return self.__satuan

    @property
    def tgl_kadaluarsa(self): return self.__tgl_kadaluarsa

    def sudah_kadaluarsa(self):
        from datetime import date
        return date.today() > date.fromisoformat(self.__tgl_kadaluarsa)

    def kategori(self): return "Habis Pakai"

    def hitung_nilai(self):
        if self.sudah_kadaluarsa(): return 0
        return self.harga * self.stok

    def info_detail(self):
        status = " KADALUARSA" if self.sudah_kadaluarsa() else " Masih Baik"
        return (f"[HABIS PAKAI] {self.id_barang} | {self.nama} | "
            f"Satuan: {self.__satuan} | Exp: {self.__tgl_kadaluarsa} | "
            f"Harga: Rp{self.harga:,.0f} | Stok: {self.stok} | {status}")
    