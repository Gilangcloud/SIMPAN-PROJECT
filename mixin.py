from datetime import datetime

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
