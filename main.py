import pygame
import sys
import os
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, speed):
        super().__init__()
        self.original_image = pygame.image.load(picture_path)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.rect.center = [pos_x, pos_y]
        self.speed = speed
        self.angle = 90
        self.health = 3
        self.shoot_sound = pygame.mixer.Sound(os.path.join('Assets', 'shot-sound.wav'))
        self.kill_sound = pygame.mixer.Sound(os.path.join('Assets', 'game-over-sound.wav'))

    def update(self):
        global score, spawn_asteroids, game_over
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = -math.degrees(math.atan2(PLAYER.rect.y - mouse_y, PLAYER.rect.x - mouse_x))
        self.image = pygame.transform.rotate(PLAYER.original_image, angle + 90)
        WIN.blit(self.image, (self.rect.x - self.image.get_width() / 2, self.rect.y - self.image.get_height() / 2))

        if self.health == 0:
            self.kill()
            self.kill_sound.play()
            game_over = True
            spawn_asteroids = False
            ASTEROID_GROUP.empty()
            BULLET_GROUP.empty()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, speed, angle):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load(picture_path), (96, 96))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.speed = speed
        self.angle = angle
        for i in range(random.randint(0, 3)):
            self.speed *= -1

    def update(self):
        self.rect.x += -math.sin(math.radians(self.angle + 90)) * self.speed
        self.rect.y += -math.cos(math.radians(self.angle + 90)) * self.speed

        self.image = pygame.transform.rotate(self.original_image, self.angle + 90)

        if pygame.sprite.groupcollide(ASTEROID_GROUP, PLAYER_GROUP, True, False):
            self.kill()
            PLAYER.health -= 1

        if self.rect.x < -100 or self.rect.x > WIDTH + 100:
            self.kill()

        if self.rect.y < -100 or self.rect.y > WIDTH + 100:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, speed):
        super().__init__()
        self.original_image = pygame.image.load(picture_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.speed = speed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = -math.degrees(math.atan2(PLAYER.rect.y - mouse_y, PLAYER.rect.x - mouse_x))

    def update(self):
        self.rect.x += -math.sin(math.radians(self.angle + 90)) * self.speed
        self.rect.y += -math.cos(math.radians(self.angle + 90)) * self.speed

        self.image = pygame.transform.rotate(self.original_image, self.angle + 90)

        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


# Setup
pygame.init()
pygame.font.init()
pygame.mixer.init(44100, -16, 2, 512)
size = WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Asteroids')
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

# Variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
timer = 0
score = 0
spawn_asteroids = True
game_over = False

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)

# Background
BG = pygame.image.load(os.path.join('Assets', 'stars bg.jpg'))

# Player
PLAYER = Player(os.path.join('Assets', 'player.png'), WIDTH / 2, HEIGHT / 2, 5)
PLAYER_GROUP = pygame.sprite.Group()
PLAYER_GROUP.add(PLAYER)

# Bullet
BULLET_GROUP = pygame.sprite.Group()

# Asteroid
ASTEROID_GROUP = pygame.sprite.Group()


def collision():
    global score
    if pygame.sprite.groupcollide(ASTEROID_GROUP, BULLET_GROUP, True, True):
        score_sound = pygame.mixer.Sound(os.path.join('Assets', 'score_sound.wav'))
        score_sound.play()
        score += 1


def draw_window():
    global monitor_size
    pygame.display.flip()

    WIN.blit(BG, (0, 0))
    BULLET_GROUP.update()
    PLAYER_GROUP.update()
    BULLET_GROUP.draw(WIN)

    ASTEROID_GROUP.draw(WIN)
    ASTEROID_GROUP.update()

    monitor_size = [1920, 1080]


def text():
    text_score = font.render('Score: ' + str(score), True, (0, 255, 0))
    text_health = font.render('Health: ' + str(PLAYER.health), True, (255, 0, 0))
    text_game_over = font.render('GAME OVER :(', True, (255, 0, 0))

    text_score_Rect = text_score.get_rect()
    text_health_Rect = text_health.get_rect()
    text_game_over_Rect = text_game_over.get_rect()

    text_health_Rect.x = WIDTH - text_score_Rect.width - 20
    text_game_over_Rect.center = WIDTH/2, HEIGHT/2

    if not game_over:
        WIN.blit(text_score, text_score_Rect)
        WIN.blit(text_health, text_health_Rect)
    if game_over:
        WIN.blit(text_game_over, text_game_over_Rect)


def spawn_asteroid():
    if spawn_asteroids:
        global timer
        if timer > 0:
            timer -= 1
        if timer <= 0:
            for i in range(random.randrange(5, 10)):
                NEW_ASTEROID_TOP = Asteroid(os.path.join('Assets', 'asteroid.png'), random.randrange(0, WIDTH),
                                            random.randrange(-300, 0), random.randrange(3, 5), random.randrange(0, 360))
                NEW_ASTEROID_BOTTOM = Asteroid(os.path.join('Assets', 'asteroid.png'), random.randrange(0, WIDTH),
                                               random.randrange(HEIGHT, HEIGHT + 300), random.randrange(3, 5),
                                               random.randrange(0, 360))
                NEW_ASTEROID_LEFT = Asteroid(os.path.join('Assets', 'asteroid.png'), random.randrange(-300, 0),
                                             random.randrange(0, HEIGHT), random.randrange(3, 5),
                                             random.randrange(0, 360))
                NEW_ASTEROID_RIGHT = Asteroid(os.path.join('Assets', 'asteroid.png'),
                                              random.randrange(WIDTH, WIDTH + 300),
                                              random.randrange(0, HEIGHT), random.randrange(3, 5),
                                              random.randrange(0, 360))

                ASTEROID_GROUP.add(NEW_ASTEROID_TOP, NEW_ASTEROID_BOTTOM, NEW_ASTEROID_LEFT, NEW_ASTEROID_RIGHT)
            timer = 100


def player_handle_movement(keys_pressed):
    if keys_pressed[pygame.K_a] and PLAYER.rect.x > 0 + PLAYER.rect.width / 2:  # LEFT
        PLAYER.rect.x = PLAYER.rect.x - PLAYER.speed
    if keys_pressed[pygame.K_d] and PLAYER.rect.x + PLAYER.rect.width / 2 < WIDTH:  # RIGHT
        PLAYER.rect.x = PLAYER.rect.x + PLAYER.speed
    if keys_pressed[pygame.K_w] and PLAYER.rect.y > 0 + PLAYER.rect.height / 2:  # UP
        PLAYER.rect.y = PLAYER.rect.y - PLAYER.speed
    if keys_pressed[pygame.K_s] and PLAYER.rect.y + PLAYER.rect.height / 2 < HEIGHT:  # DOWN
        PLAYER.rect.y = PLAYER.rect.y + PLAYER.speed


def main():
    global WIN, WIDTH, HEIGHT, BG
    clock = pygame.time.Clock()
    run = True

    full_screen = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    PLAYER.shoot_sound.play()
                    BULLET = Bullet(os.path.join('Assets', 'bullet.png'), PLAYER.rect.x, PLAYER.rect.y, 20)
                    BULLET_GROUP.add(BULLET)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        WIN = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
                        BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
                    else:
                        WIN = pygame.display.set_mode((WIN.get_width(), WIN.get_height()), pygame.RESIZABLE)
                        WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
                        BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

            if event.type == pygame.VIDEORESIZE:
                if not full_screen:
                    WIN = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
                    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

        keys_pressed = pygame.key.get_pressed()
        player_handle_movement(keys_pressed)
        draw_window()
        text()
        collision()
        spawn_asteroid()


if __name__ == '__main__':
    main()
