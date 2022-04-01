import sys
import os
import random
import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound(os.path.join('Assets', 'gunshot.wav'))

    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, target_group, True)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


# Setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# Game Screen
WIDTH, HEIGHT = 1024, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load(os.path.join('Assets', 'stars bg.jpg'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

# Crosshair
crosshair = Crosshair(os.path.join('Assets', 'crosshair.png'))
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target(os.path.join('Assets', 'target.png'), random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    target_group.add(new_target)


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                crosshair.shoot()

    pygame.display.flip()
    WIN.blit(BACKGROUND, (0, 0))
    target_group.draw(WIN)
    crosshair_group.draw(WIN)
    crosshair_group.update()

    clock.tick(FPS)
