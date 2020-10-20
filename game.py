import pygame
from pygame.locals import MOUSEBUTTONDOWN
from game_settings import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Grid War")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    """This is the default player sprite class."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((31, 31))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.rect.center = (round(WIDTH/5), round(HEIGHT/2))

        self.rect.centerx = round(WIDTH / 2)
        self.rect.bottom = round(HEIGHT - 10)
        self.speedx = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_w]:
            self.speedy = -5
        if keystate[pygame.K_s]:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.top < tileSize * 3:
            self.rect.top = tileSize * 3

    def getMouse(self):
        self.mousex, self.mousey = pygame.mouse.get_pos()

    def shootBullet(self):
        # player.getMousePos()
        bullet = Bullets(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullets(pygame.sprite.Sprite):
    """This defines a bullet class that will shoot out of the sprite"""

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.neg_speed_x, self.neg_speed_y = 5, -5

    def update(self):
        player.getMouse()
        if player.mousex > player.rect.centerx:
            self.rect.centerx += self.neg_speed_x
        # else:
        #     self.rect.x += self.neg_speed_y
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


def topBar():
    """This will create a method to define a topBar."""
    # Draw the top score bar onto the surface
    pygame.draw.rect(gameDisplay, BLACK, (0, 0, WIDTH, tileSize * 3))


def tileGrid():
    """This will create a grid around the player field."""
    # create a grid:
    for x in range(0, WIDTH, tileSize):
        pygame.draw.line(gameDisplay, DARKGREY, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, tileSize):
        pygame.draw.line(gameDisplay, DARKGREY, (0, y), (WIDTH, y), 1)


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()

all_sprites.add(player)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shootBullet()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()

    gameDisplay.fill(BLACK)

    # create a grid:
    tileGrid()
    topBar()

    all_sprites.draw(gameDisplay)

    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
quit()
