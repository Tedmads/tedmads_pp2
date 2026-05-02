import pygame
import random
import time
import os
from persistence import load_settings, save_score
from ui import (
    text_input_screen,
    main_menu,
    leaderboard_screen,
    settings_screen,
    game_over_screen,
)

# размеры окна игры
WIDTH  = 400
HEIGHT = 600
FPS    = 60  # количество кадров в секунду

# коэффициенты сложности (чем меньше — тем сложнее игра)
DIFF_MULT = {"easy": 1.6, "normal": 1.0, "hard": 0.55}

# возможные цвета машины игрока
CAR_TINTS = {
    "Default": None,
    "Red":     (255, 60,  60),
    "Blue":    (60,  120, 255),
    "Green":   (60,  220, 60),
}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self, image, tint=None):
        super().__init__()
        self.image = image.copy()

        # если выбран цвет — накладываем прозрачный оттенок
        if tint:
            tint_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surf.fill((*tint, 120))
            self.image.blit(tint_surf, (0, 0))

        # положение игрока
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # по центру по горизонтали
        self.rect.bottom   = HEIGHT     # снизу экрана

        self.speed  = 5
        self.shield = False  # защита от столкновения

    def move(self):
        keys = pygame.key.get_pressed()

        # движение вправо
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # движение влево
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        # ограничение движения внутри экрана
        if self.rect.left  < 0:
            self.rect.left  = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect()
        self.speed = 10

    # генерация случайной позиции сверху
    def generate_random_rect(self):
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        # движение вниз
        self.rect.move_ip(0, self.speed)

        # если враг вышел за экран — появляется снова
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.base_image = image

        # случайный размер (влияет на очки)
        self.size = random.randint(1, 3)
        self._apply_size()
        self.generate_random_rect()

    def _apply_size(self):
        # изменение размера монеты
        w = int(30 * self.size * 0.5)
        self.image = pygame.transform.scale(self.base_image, (w, w))
        self.rect  = self.image.get_rect()

    def generate_random_rect(self):
        # новая случайная позиция
        self.size = random.randint(1, 3)
        self._apply_size()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top  = random.randint(HEIGHT - 80, HEIGHT - 20)


# ---------------- OBSTACLES ----------------
class Obstacle(pygame.sprite.Sprite):
    # типы препятствий
    KINDS = ["oil", "barrier"]

    def __init__(self):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.speed = 4

        # разные размеры и внешний вид
        w, h = (50, 20) if self.kind == "oil" else (40, 30)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)

        # рисуем препятствие
        if self.kind == "oil":
            pygame.draw.ellipse(self.image, (20, 20, 80, 200), (0, 0, w, h))
        else:
            pygame.draw.rect(self.image, (180, 30, 30), (0, 0, w, h))

        self.rect = self.image.get_rect()
        self._spawn()

    def _spawn(self):
        # случайное появление сверху
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        # движение вниз
        self.rect.move_ip(0, self.speed)

        # если вышел за экран — появляется снова
        if self.rect.top > HEIGHT:
            self._spawn()


# ---------------- NITRO STRIP ----------------
class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # создаем полосу ускорения
        self.image = pygame.Surface((WIDTH, 14), pygame.SRCALPHA)
        self.image.fill((255, 220, 0, 160))

        self.rect  = self.image.get_rect()
        self.rect.bottom = 0
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, self.speed)


# ---------------- POWERUPS ----------------
POWERUP_COLORS = {
    "nitro": (255, 160, 0),
    "shield": (80, 80, 255),
    "repair": (0, 200, 80)
}

class PowerUp(pygame.sprite.Sprite):
    TIMEOUT = 7000  # время жизни (мс)

    def __init__(self, kind):
        super().__init__()
        self.kind  = kind
        self.speed = 4

        # рисуем круг power-up
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, POWERUP_COLORS[kind], (14, 14), 14)

        self.rect  = self.image.get_rect()
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

        self.spawned_at  = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self):
        # проверяем, истекло ли время
        return pygame.time.get_ticks() - self.spawned_at > self.TIMEOUT


# ---------------- HUD ----------------
def draw_hud(screen, fontt, collected, distance, active_pu, pu_end):
    # отображаем счет и дистанцию
    screen.blit(
        fontt.render(f"Score:{collected} Dist:{int(distance)}", True, "black"),
        (5, 5)
    )


# ---------------- MAIN GAME ----------------
def play_game(screen, username):
    # загружаем настройки
    settings   = load_settings()
    diff_mult  = DIFF_MULT.get(settings.get("difficulty", "normal"), 1.0)
    tint       = CAR_TINTS.get(settings.get("car_color", "Default"))

    # загрузка изображений
    image_background = pygame.image.load(os.path.join(ASSETS_DIR, 'AnimatedStreet.png'))
    image_player     = pygame.image.load(os.path.join(ASSETS_DIR, 'Player.png'))
    image_enemy      = pygame.image.load(os.path.join(ASSETS_DIR, 'Enemy.png'))
    coin_image       = pygame.image.load(os.path.join(ASSETS_DIR, 'dollar.png')).convert_alpha()

    # загрузка и запуск музыки
    if settings.get("sound", True):
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, 'background.wav'))
        pygame.mixer.music.play(-1)

    # звук столкновения
    sound_crash = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'crash.wav'))

    fontt = pygame.font.SysFont("Verdana", 20)

    # создаем объекты
    player = Player(image_player, tint)
    enemy  = Enemy(image_enemy)
    coin   = Coin(coin_image)

    # группы объектов
    all_sprites   = pygame.sprite.Group(player, enemy, coin)
    enemy_sprites = pygame.sprite.Group(enemy)
    coin_sprites  = pygame.sprite.Group(coin)

    clock = pygame.time.Clock()

    collected  = 0  # счет
    distance   = 0  # пройденная дистанция

    running = True
    while running:

        # обработка событий (закрытие окна)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

        # движение объектов
        player.move()
        enemy.move()

        # проверка столкновения с монетой
        if pygame.sprite.spritecollideany(player, coin_sprites):
            collected += coin.size
            coin.generate_random_rect()

        # проверка столкновения с врагом
        if pygame.sprite.spritecollideany(player, enemy_sprites):
            running = False

        # увеличиваем дистанцию
        distance += player.speed * 0.05

        # отрисовка на экран
        screen.blit(image_background, (0, 0))
        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(coin.image, coin.rect)

        # отображаем HUD
        draw_hud(screen, fontt, collected, distance, None, 0)

        pygame.display.flip()  # обновление экрана
        clock.tick(FPS)        # ограничение FPS

    if settings.get("sound", True):
        sound_crash.play()
    pygame.mixer.music.stop()
    time.sleep(0.3)

    return collected, distance


def run_app():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer")

    username = text_input_screen(screen, "Enter your name")

    running = True
    while running:
        action = main_menu(screen)

        if action == "Play":
            play_again = True
            while play_again:
                score, distance = play_game(screen, username)
                save_score(username, score, distance)
                next_action = game_over_screen(screen, score, distance, score)
                play_again = next_action == "retry"

        elif action == "Leaderboard":
            leaderboard_screen(screen)

        elif action == "Settings":
            settings_screen(screen)

        elif action == "Quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    run_app()
