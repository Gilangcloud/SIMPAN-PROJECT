from abc import ABC, abstractmethod
from datetime import datetime
from mixin import LogMixin, ValidasiMixin

class Barang(ABC, LogMixin, ValidasiMixin):
    def __init__(self, id_barang:str, nama:str, harga:float, stok:int):
        self.__id_barang = id_barang
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok
        self.__tgl_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__riwayat_harga = [(self.__tgl_masuk, harga)]
    
    @property
    def id_barang(self):return self.__id_barang

    @property
    def nama(self):return self.__nama

    @property
    def harga(self):return self.__harga

    @property
    def stok(self):return self.__stok

    @property
    def tgl_masuk(self):return self.__tgl_masuk

    @property
    def riwayat_harga(self):
        return self.__riwayat_harga.copy()

    @nama.setter
    def nama(self, nilai:str):
        if not self.validasi_nama(nilai):
            raise ValueError("Nama Tidak Boleh Kosong")
        self.__nama = nilai

    @harga.setter
    def harga(self, nilai:float):
        if not self.validasi_harga(nilai):
            raise ValueError("Harga harus Lebih Dari 0 ")
        self.__harga= nilai

        waktu_ubah = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__riwayat_harga.append((waktu_ubah, nilai))

    @stok.setter
    def stok(self, nilai:int):
        if not self.validasi_stok(nilai):
            raise ValueError("Stok Harus Bilangan Bulat Lebih Dari 0")
        self.__stok = nilai

    def tambah_stok(self, jumlah:int):
        if jumlah <= 0:
            raise ValueError("Jumlah Harus Positif")
        self.__stok += jumlah
        self.log_aktivitas(f"Tambah Stok,{self.__nama}+{jumlah}->{self.__stok}")
    
    def kurang_stok(self, jumlah:int):
        if jumlah <= 0:
            raise ValueError ("Jumlah Harus Positif")
        elif jumlah > self.__stok:
            raise ValueError (f"Stok Tidak Cukup Untuk Saat Ini : {self.__stok}")
        self.__stok -= jumlah
        self.log_aktivitas(f"Stok Kurang,{self.__nama}-{jumlah}-> Sisa {self.__stok}")

    @abstractmethod
    def info_detail(self) -> str:
        pass
    
    @abstractmethod
    def kategori(self) -> str:
        pass
    
    @abstractmethod
    def hitung_nilai(self) -> float:
        pass

    def __str__(self):
        return self.info_detail()