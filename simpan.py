from datetime import datetime
from abc import ABC, abstractmethod

class LogMixin:
    def log_aktivitas(self, aksi, detail=""):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{waktu}] {aksi} {detail}")

class ValidasiMixin:
    @staticmethod
    def validasi_harga(harga):
        return isinstance(harga, (int, float) ) and harga >= 0
    
    @staticmethod
    def validasi_stok(stok):
        return isinstance(stok, int) and stok >= 0
    
    @staticmethod
    def validasi_nama (nama):
        return isinstance(nama, str) and len (nama.strip()) > 0
    
class Barang(ABC, LogMixin, ValidasiMixin):
    def __init__(self, id_barang:str, nama:str, harga:float, stok:int):
        self.__id_barang = id_barang
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok
        self.__tgl_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    
class ManageSIMPAN(LogMixin, ValidasiMixin):
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
