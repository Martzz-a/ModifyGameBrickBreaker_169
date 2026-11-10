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


# Class Ball (bola yang memantul)
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

    # Menggambar bola di layar
    def display(self):
        pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    # Memperbarui posisi bola dan memantulkannya dari dinding
    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # PERBAIKAN BUG: posisi dijepit agar bola tidak nyangkut di dinding
        if self.posx <= 0:
            self.posx = 0
            self.xFac = 1
        elif self.posx >= WIDTH:
            self.posx = WIDTH
            self.xFac = -1

        # Memantul dari sisi atas layar
        if self.posy <= 0:
            self.posy = 0
            self.yFac = 1

        # Mengembalikan True jika bola jatuh melewati sisi bawah
        if self.posy >= HEIGHT:
            return True

        return False

    # PERBAIKAN BUG: reset bola ke tengah di atas paddle (sebelumnya ke pojok kiri bawah)
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac = random.choice([-1, 1])  # arah kiri/kanan acak
        self.yFac = -1                      # selalu mulai bergerak ke atas

    # Membalik arah bola pada sumbu Y
    def hit(self):
        self.yFac *= -1

    # PERBAIKAN BUG: rect dibuat baru dari posisi saat ini
    # (sebelumnya memakai rect dari frame sebelumnya)
    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius,
                           self.radius * 2, self.radius * 2)


# Fungsi bantu

# Mengecek tabrakan antara dua rect
def collisionChecker(rect, ball):
    return pygame.Rect.colliderect(rect, ball)


# Membuat daftar blok yang tersusun membentuk rumah berdasarkan HOUSE_MAP
def populateBlocks(blockWidth, blockHeight,
                   horizontalGap, verticalGap):
    listOfBlocks = []

    # Lebar total rumah, dipakai agar rumah berada di tengah layar
    cols = len(HOUSE_MAP[0])
    houseWidth = cols * (blockWidth + horizontalGap) - horizontalGap
    startX = (WIDTH - houseWidth) // 2
    startY = 40  # jarak rumah dari sisi atas layar

    for row, line in enumerate(HOUSE_MAP):
        for col, cell in enumerate(line):
            if cell != '#':
                continue  # '.' berarti kosong (celah jendela/pintu/di luar atap)

            x = startX + col * (blockWidth + horizontalGap)
            y = startY + row * (blockHeight + verticalGap)

            # Baris atas memakai warna genteng, sisanya batu bata dinding
            palette = ROOF_COLORS if row < ROOF_ROWS else BRICK_COLORS
            listOfBlocks.append(
                Block(x, y, blockWidth, blockHeight, random.choice(palette)))

    return listOfBlocks


# Menggambar latar bertema rumah: langit, matahari, awan, dan rumput
def drawBackground():
    screen.fill(SKY_COLOR)

    # Matahari di pojok kanan atas
    pygame.draw.circle(screen, SUN_COLOR, (WIDTH - 60, 55), 30)

    # Awan sederhana dari beberapa lingkaran putih
    for cx, cy in [(90, 70), (130, 60), (170, 72), (440, 120), (475, 110), (510, 122)]:
        pygame.draw.circle(screen, CLOUD_COLOR, (cx, cy), 22)

    # Rumput di bagian bawah, dengan garis lebih gelap di tepi atasnya
    pygame.draw.rect(screen, GRASS_COLOR, (0, HEIGHT - 60, WIDTH, 60))
    pygame.draw.rect(screen, GRASS_DARK, (0, HEIGHT - 60, WIDTH, 6))


# Menggambar teks skor, high score, level, dan nyawa di bagian bawah layar
# (PERBAIKAN BUG: teks dirender setelah nilai diperbarui, tidak telat satu frame)
def drawHud(score, highScore, level, lives):
    scoreText = font.render("Score : " + str(score), True, WHITE)
    highText = font.render("High : " + str(highScore), True, WHITE)
    levelText = font.render("Level : " + str(level), True, WHITE)
    livesText = font.render("Lives : " + str(lives), True, WHITE)

    screen.blit(scoreText, (10, HEIGHT - 20))
    screen.blit(highText, (130, HEIGHT - 20))
    screen.blit(levelText, (260, HEIGHT - 20))
    screen.blit(livesText, (380, HEIGHT - 20))


# PERBAIKAN BUG: layar game over kini menampilkan tulisan (sebelumnya layar kosong)
# Menunggu SPACE untuk main lagi (True) atau tutup jendela untuk keluar (False)
def gameOver(score, highScore):
    drawBackground()

    # Lapisan gelap transparan agar tulisan putih mudah dibaca
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(170)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title = bigFont.render("GAME OVER", True, WHITE)
    scoreInfo = font.render(
        "Score : " + str(score) + "   High Score : " + str(highScore), True, WHITE)
    hint = font.render("Tekan SPACE untuk main lagi", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(scoreInfo, scoreInfo.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        clock.tick(FPS)  # mencegah loop memakai CPU 100%


# Pengatur utama game
def main():
    running = True
    lives = 3
    score = 0
    highScore = 0  # FITUR BARU: high score selama program berjalan
    level = 1      # FITUR BARU: nomor level

    # Paddle mulai di tengah layar (sebelumnya di pojok kiri)
    striker = Striker(WIDTH // 2 - 50, HEIGHT - 50, 100, 20, 10, STRIKER_COLOR)
    strikerXFac = 0

    # Bola dibuat lalu di-reset agar posisi awal sama dengan posisi setelah nyawa hilang
    ball = Ball(WIDTH // 2, HEIGHT - 150, 7, BASE_BALL_SPEED, BALL_COLOR)
    ball.reset()

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 4, 4  # celah kecil agar batu bata membentuk rumah utuh

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Game loop
    while running:
        drawBackground()  # gambar langit, matahari, awan, rumput

        # FITUR BARU: jika semua blok hancur, naik level dan bola makin cepat
        if not listOfBlocks:
            level += 1
            ball.speed = min(BASE_BALL_SPEED + level - 1, MAX_BALL_SPEED)
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # Semua nyawa habis: simpan high score, tampilkan game over
        if lives <= 0:
            highScore = max(highScore, score)
            running = gameOver(score, highScore)

            # Reset seluruh state permainan
            lives = 3
            score = 0
            level = 1
            ball.speed = BASE_BALL_SPEED
            ball.reset()
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)
            continue

        # Penanganan input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Tabrakan bola dengan paddle
        # PERBAIKAN BUG: hanya memantul jika bola sedang turun (yFac > 0),
        # supaya bola tidak "nyangkut" di dalam paddle
        if collisionChecker(striker.getRect(), ball.getRect()) and ball.yFac > 0:
            ball.hit()

        # Tabrakan bola dengan blok
        # PERBAIKAN BUG: iterasi memakai salinan list dan berhenti setelah satu blok,
        # agar tidak error saat menghapus item dan bola tidak memantul dua kali
        for block in list(listOfBlocks):
            if collisionChecker(block.getRect(), ball.getRect()):
                # Bola didorong keluar dari batu bata sebelum memantul, agar
                # pukulan yang sama tidak terhitung dua kali di frame berikutnya
                if ball.yFac < 0:
                    ball.posy = block.getRect().bottom + ball.radius
                else:
                    ball.posy = block.getRect().top - ball.radius
                ball.hit()
                block.hit()

                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5
                break

        # Update posisi
        striker.update(strikerXFac)
        lifeLost = ball.update()

        # Bola jatuh: kurangi nyawa dan reset bola (print debug dihapus)
        if lifeLost:
            lives -= 1
            ball.reset()

        # Menggambar semua objek
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        drawHud(score, max(highScore, score), level, lives)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()