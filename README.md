# 📥 Video Downloader & Uploader Bot (Colab Edition)

Automasi lengkap untuk mengunduh video dari berbagai sumber dan mengunggahnya ke Telegram. Dirancang untuk berjalan di Google Colab dengan antarmuka interaktif.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lIlSkaSkaSkalIl/video_downloader/blob/main/video_downloader.ipynb)

---

## ✨ Fitur Utama

- 🔗 **Download Video** dari:
  - M3U8 streaming
  - Twitter (single/multi video, mendukung cookies)
- 🎞️ **Ambil Metadata + Thumbnail** dengan `ffprobe` & `ffmpeg`
- 📤 **Batch Upload ke Telegram** menggunakan Bot Token
- 🔐 **Dukungan autentikasi Twitter** via `cookies.txt`
- 📦 **Hapus file otomatis setelah upload**

---

## 📚 Alur Penggunaan

### 1. Persiapkan Google Colab
- Jalankan semua cell sesuai urutan dari atas ke bawah.
- Upload file `cookies.txt` jika mengunduh video dari tweet terkunci atau pribadi.

### 2. Download Video
- Pilih metode:
  - `twitter`
  - `m3u8/Streaming`
- Masukkan URL dan (opsional) nama file.

### 3. Ambil Metadata & Thumbnail
- Proses seluruh video di folder `/video_downloader/video/`
- Simpan hasil ke:
  - `meta/*.json`
  - `thumbnails/*.jpg`

### 4. Upload ke Telegram
- Siapkan kredensial:
  - `API_ID`, `API_HASH`, `BOT_TOKEN`, `CHAT_ID`
- Bot akan:
  - Kirim status progres
  - Unggah video + thumbnail
  - Kirim log hasil upload
  - Hapus file video & thumbnail setelah upload

---

## 🗂️ Struktur Folder

```
/content/video_downloader/
├── video/          # Tempat video hasil download
├── output/         # Metadata Twitter
├── meta/           # Metadata per video
├── thumbnails/     # Thumbnail dari setiap video
├── logs/
│   ├── log.txt     # Ringkasan proses
│   └── log.json    # Log terstruktur
```

---

## ⚙️ Dependensi

Semua dependensi akan otomatis di-install dalam Colab:

- `yt-dlp`
- `gdown`
- `ffmpeg`
- `pyrogram`
- `tgcrypto`
- `tqdm`

---

## 🔐 Autentikasi Twitter (Optional)

Jika video Twitter tidak bisa diunduh karena dibatasi, kamu bisa:

1. Gunakan ekstensi **Get Cookies.txt**
2. Simpan sebagai `cookies.txt`
3. Upload melalui cell yang tersedia

---

## 🛠️ Konfigurasi Upload Telegram

Isi parameter berikut:

```python
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
CHAT_ID = 123456789
```

Dapatkan API ID & Hash dari [https://my.telegram.org](https://my.telegram.org)

---

## ✅ Contoh Output

- Progres download dengan `tqdm`
- Metadata dan thumbnail `.jpg`
- Progres upload ke Telegram
- Status upload per file (sukses/gagal)
- Total ringkasan upload (jumlah file, durasi, ukuran)

---

## 🧹 Cleanup Otomatis

- Setelah video berhasil diupload, file akan dihapus secara otomatis:
  - Video file
  - Thumbnail
  - Metadata `.json`

---

## 📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi.

---

## 🙋‍♂️ Kontribusi

Pull request, issue, dan saran sangat diterima untuk peningkatan fungsionalitas ke depan.
