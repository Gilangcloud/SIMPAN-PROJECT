from barang import Barang

class BarangElektronik(Barang):
    def __init__(self, id_barang, nama, harga, stok, merek, garansi_bulan):
        super().__init__(id_barang, nama, harga, stok)
        self.__merek = merek
        self.__garansi_bulan = garansi_bulan

    @property
    def merek(self): return self.__merek

    @property
    def garansi_bulan(self): return self.__garansi_bulan

    def kategori(self): return "Elektronik"

    def hitung_nilai(self): return self.harga * self.stok

    def info_detail(self):
        return (f"[ELEKTRONIK] {self.id_barang} | {self.nama} | "
            f"Merek: {self.__merek} | Garansi: {self.__garansi_bulan} bln | "
            f"Harga: Rp{self.harga:,.0f} | Stok: {self.stok}")