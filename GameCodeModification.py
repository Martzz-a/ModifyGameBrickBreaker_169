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


# Class Striker (paddle yang digerakkan pemain)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # Rect dipakai untuk posisi dan deteksi tabrakan
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Menggambar paddle di layar
    def display(self):
        pygame.draw.rect(screen, self.color, self.strikerRect)

    # Memperbarui posisi paddle berdasarkan arah (xFac: -1 kiri, 1 kanan, 0 diam)
    def update(self, xFac):
        self.posx += self.speed * xFac

        # Menjaga paddle tetap di dalam layar
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Mengembalikan rect paddle untuk cek tabrakan
    def getRect(self):
        return self.strikerRect


# Class Block (blok yang harus dihancurkan)
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        # Semua batu bata punya health 200: pukulan pertama membuatnya retak,
        # pukulan kedua menghancurkannya
        self.health = 200

        # Rect dipakai untuk posisi dan deteksi tabrakan
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Menggambar batu bata; jika sudah terkena sekali (health <= 100), gambar retakan
    def display(self):
        if self.health > 0:
            r = self.blockRect
            # Badan batu bata dan garis tepinya
            pygame.draw.rect(screen, self.color, r)
            pygame.draw.rect(screen, MORTAR_COLOR, r, 2)
            # Garis sambungan kecil di tengah agar terlihat seperti susunan bata
            pygame.draw.line(screen, MORTAR_COLOR,
                             (r.x + r.width // 2, r.y),
                             (r.x + r.width // 2, r.y + r.height // 2), 1)

            if self.health <= 100:
                self.drawCrack()

    # Menggambar garis retakan zig-zag di atas batu bata
    def drawCrack(self):
        r = self.blockRect
        w, h = r.width, r.height
        # Retakan utama dari atas ke bawah
        main = [(r.x + w * 0.55, r.y), (r.x + w * 0.42, r.y + h * 0.35),
                (r.x + w * 0.62, r.y + h * 0.6), (r.x + w * 0.48, r.y + h)]
        pygame.draw.lines(screen, CRACK_COLOR, False, main, 2)
        # Cabang retakan ke samping
        branch = [(r.x + w * 0.62, r.y + h * 0.6), (r.x + w * 0.85, r.y + h * 0.75)]
        pygame.draw.lines(screen, CRACK_COLOR, False, branch, 1)

    # Mengurangi health blok saat terkena bola
    def hit(self):
        self.health -= self.damage

    # Mengembalikan rect blok
    def getRect(self):
        return self.blockRect

    # Mengembalikan health blok saat ini
    def getHealth(self):
        return self.health
