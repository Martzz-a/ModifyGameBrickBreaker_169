import pygame
import random

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar permainan
WIDTH, HEIGHT = 600, 500

# Warna (UBAH TAMPILAN: palet warna baru)
BLACK = (15, 15, 30)         # latar belakang biru gelap
WHITE = (255, 255, 255)      # teks
BRICK_COLORS = [(178, 54, 40), (194, 64, 46), (160, 46, 36)]  # variasi merah batu bata
MORTAR_COLOR = (110, 30, 24)  # garis tepi/sambungan batu bata (merah tua)
CRACK_COLOR = (45, 12, 8)     # warna garis retakan
BALL_COLOR = (50, 50, 70)     # bola abu gelap (kontras dengan langit dan matahari)
STRIKER_COLOR = (120, 72, 30)  # paddle cokelat kayu

# TEMA RUMAH: warna latar
SKY_COLOR = (135, 206, 235)   # langit biru
SUN_COLOR = (255, 220, 60)    # matahari
CLOUD_COLOR = (255, 255, 255)  # awan
GRASS_COLOR = (60, 160, 70)   # rumput
GRASS_DARK = (40, 120, 50)    # garis rumput bagian atas

# TEMA RUMAH: warna genteng atap (cokelat kemerahan, lebih gelap dari dinding)
ROOF_COLORS = [(100, 50, 40), (115, 58, 44), (90, 44, 36)]

# TEMA RUMAH: denah blok. '#' = ada batu bata, '.' = kosong.
# Tujuh baris pertama adalah atap, sisanya dinding dengan 2 jendela dan 1 pintu.
HOUSE_MAP = [
    "......#......",
    ".....###.....",
    "....#####....",
    "...#######...",
    "..#########..",
    ".###########.",
    "#############",
    ".###########.",
    ".##..###..##.",
    ".##..###..##.",
    ".###########.",
    ".####...####.",
    ".####...####.",
]
ROOF_ROWS = 7  # jumlah baris teratas yang diwarnai sebagai atap

# Font untuk teks skor, nyawa, dan level
font = pygame.font.Font('freesansbold.ttf', 15)
bigFont = pygame.font.Font('freesansbold.ttf', 32)

# Membuat jendela game dan memberi judul
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# Mengatur kecepatan frame
clock = pygame.time.Clock()
FPS = 30

# FITUR BARU: pengaturan kecepatan bola per level
BASE_BALL_SPEED = 5   # kecepatan bola di level 1
MAX_BALL_SPEED = 10   # batas kecepatan agar game tetap bisa dimainkan

