# Block Breaker: Apa yang Berubah

Ini daftar perubahan dari kode awal ke versi akhir (`block_breaker.py`).

## Ringkasan

| Aspek | Kode awal | Versi akhir |
|---|---|---|
| Susunan blok | Grid penuh di setengah layar atas | Rumah dengan atap, dinding, jendela, dan pintu |
| Tampilan blok | Kotak polos putih atau hijau | Batu bata merah yang retak setelah pukulan pertama |
| Ketahanan blok | Putih 2 pukulan, hijau 1 pukulan | Semua blok 2 pukulan |
| Latar | Hitam polos | Langit, matahari, awan, dan rumput |
| Layar game over | Tanpa tulisan, layar membeku di frame terakhir | Tulisan GAME OVER, skor, dan high score |
| Level dan high score | Tidak ada | Ada |

## Bug yang diperbaiki

1. **Bola kembali ke pojok.** Setelah nyawa hilang, bola muncul di pojok kiri bawah. Sekarang bola muncul di tengah dan bergerak ke atas, ke kiri atau kanan secara acak (`Ball.reset`).
2. **Game over tanpa tulisan.** Layar membeku tanpa informasi. `gameOver` kini menampilkan tulisan dan petunjuk menekan SPACE, dan loop-nya memakai `clock.tick` supaya CPU tidak terbebani.
3. **Blok dihapus saat di-loop.** Kode awal menghapus blok dari list yang sedang diulang. Sekarang loop memakai salinan list dan berhenti setelah satu blok kena, jadi bola tidak memantul dua kali.
4. **Bola menempel di paddle.** Paddle hanya memantulkan bola yang sedang turun (`yFac > 0`).
5. **Bola menempel di dinding.** `Ball.update` menjepit posisi bola di batas layar.
6. **Tabrakan telat satu frame.** `Ball.getRect()` membuat rect dari posisi bola saat ini, bukan dari frame sebelumnya.
7. **Skor dan nyawa telat satu frame.** Fungsi baru `drawHud` menggambar teks setelah nilainya diperbarui.
8. **Satu pukulan terhitung dua kali.** Setelah kena blok, bola didorong keluar dari blok sebelum memantul.
9. **Debug tersisa.** `print(lives)` dihapus.

## Fitur baru

- **Level.** Bola menjadi 1 poin lebih cepat setiap semua blok hancur, sampai batas 10 (`BASE_BALL_SPEED`, `MAX_BALL_SPEED`).
- **High score.** Nilainya tersimpan selama program jalan. Setelah program ditutup, nilainya hilang.
- **HUD.** Score, High, Level, dan Lives tampil di bagian bawah layar.
- **Posisi awal.** Paddle dan bola mulai di tengah layar.

## Batu bata

- Semua blok punya health 200. Pukulan pertama membuat bata retak. Pukulan kedua menghancurkannya dan menambah skor 5.
- `Block.display` menggambar bata dengan tepi gelap dan satu garis sambungan.
- `Block.drawCrack` (baru) menggambar retakan zig-zag.
- `BRICK_COLORS`, `MORTAR_COLOR`, dan `CRACK_COLOR` menggantikan warna lama (`WHITE` dan `GREEN`).

## Tema rumah

- **`HOUSE_MAP`** (baru) adalah denah teks dengan `#` untuk bata dan `.` untuk kosong. Rumahnya berisi 101 blok. Ubah denah ini untuk mengubah bentuk rumah.
- **`populateBlocks`** ditulis ulang untuk membaca denah dan menaruh rumah di tengah layar. Tujuh baris teratas menjadi atap (`ROOF_COLORS`).
- **Celah antar blok** mengecil dari 20 ke 4 piksel.
- **`drawBackground`** (baru) menggambar langit, matahari, awan, dan rumput. Layar game over memakainya juga, dengan lapisan gelap transparan di atasnya.
- **Bola dan paddle** berganti warna (abu gelap dan cokelat) agar tampak jelas di latar baru.

## Fungsi dan class

| Nama | Status |
|---|---|
| `Striker` | Berubah sedikit (hanya cara menggambar) |
| `Block` | Berubah (health, tampilan bata), plus `drawCrack` baru |
| `Ball` | Berubah (`reset`, `update`, `getRect`) |
| `populateBlocks` | Ditulis ulang untuk bentuk rumah |
| `drawBackground` | Baru |
| `drawHud` | Baru |
| `gameOver` | Berubah (menampilkan layar, menerima skor) |
| `main` | Berubah (level, high score, urutan menggambar) |

## Catatan

- Bola dan paddle bisa lewat di celah jendela dan pintu.
- Setiap naik level, rumah yang sama muncul lagi dengan bola yang lebih cepat.
- Aku sudah memeriksa tampilan lewat satu frame hasil render. Gameplay penuh belum aku uji.
