import pygame
from pygame.locals import MOUSEBUTTONDOWN
from pygame.constants import *
from game_settings import *
import math

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Grid War")
monitor_size = [pygame.display.Info().current_w,
                pygame.display.Info().current_w]
gameDisplay = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)

fullscreen = False


class Player(pygame.sprite.Sprite):
    """This is the default player sprite class."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((45, 45))
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

    def shoot(self):
        x, y = pygame.mouse.get_pos()
        b = Bullet(RED, player.rect.centerx,
                   player.rect.centery, 10, 10, x, y)
        bullets.append(b)


class Bullet(Player):
    def __init__(self, color, x, y, width, height, targetx, targety):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 10
        # get angle to target in radians
        angle = math.atan2(targety-y, targetx-x)
        print('Angle in degrees:', int(angle*180/math.pi))
        self.dx = math.cos(angle)*self.speed
        self.dy = math.sin(angle)*self.speed
        self.x = x
        self.y = y

    def move(self):
        # self.x and self.y are floats (decimals) so I get more accuracy
        # if I change self.x and y and then convert to an integer for
        # the rectangle.
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


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
bullets = []

player = Player()

all_sprites.add(player)


running = True
while running:

    for event in pygame.event.get():
        # for screen resizing
        if event.type == VIDEORESIZE:
            if not fullscreen:
                gameDisplay = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
        #  for fullscreen
        if event.type == KEYDOWN:
            if event.key == K_l:
                fullscreen = not fullscreen
                if fullscreen:
                    gameDisplay = pygame.display.set_mode(
                        monitor_size, pygame.FULLSCREEN)
                else:
                    gameDisplay = pygame.display.set_mode(
                        (gameDisplay.get_width(), gameDisplay.get_height()), pygame.RESIZABLE)
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
    all_sprites.update()

    gameDisplay.fill(BLACK)
    for b in bullets:
        b.move()
        b.draw(gameDisplay)
    # create a grid:
    tileGrid()
    topBar()

    all_sprites.draw(gameDisplay)

    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
quit()
