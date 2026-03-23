# 📞 Phone Information Tracer

Alat investigasi nomor telepon sederhana namun kuat yang dibangun dengan Python. Alat ini mengekstrak informasi lokasi, penyedia layanan (carrier), dan zona waktu dari nomor telepon di seluruh dunia.

## ✨ Fitur Utama
- **Global Reach**: Mendukung format nomor internasional dari seluruh negara.
- **Bulk Processing**: Scan ribuan nomor sekaligus melalui file teks.
- **Smart Parsing**: Otomatis mendeteksi kode negara jika diawali simbol `+`.
- **Output Export**: Simpan hasil investigasi ke dalam file `.txt`.
- **Cross-Platform**: Berjalan lancar di Linux, Termux (Android), dan Windows (CMD/PowerShell).

## 🛠️ Instalasi

### Linux / Termux
1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/123tool/Phone-Information-Tracer.git]
   cd Phone-Information-Tracer
   python phone_tracer.py
