import math
import time
from random import choice, randint, random

import pygame

FPS = 50

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
ay = 0.5

global score

score = 0

hit = 1


class Bullet:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.color = BLACK
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREY
        self.body = pygame.Rect(30, 450, 40, 10)
        self.turret = pygame.Rect(45, 440, 10, 10)
        self.cannon = pygame.Rect(48, 430, 4, 10)
        self.tracks_left = pygame.Rect(30, 460, 10, 10)
        self.tracks_right = pygame.Rect(60, 460, 10, 10)
        self.speed = 10  # Увеличиваем скорость движения танка
        self.bullets = []

    def move(self, direction):
        if direction == "left":
            for part in [self.body, self.turret, self.cannon, self.tracks_left, self.tracks_right]:
                part.x -= self.speed
        elif direction == "right":
            for part in [self.body, self.turret, self.cannon, self.tracks_left, self.tracks_right]:
                part.x += self.speed

        if self.body.x < 0:
            for part in [self.body, self.turret, self.cannon, self.tracks_left, self.tracks_right]:
                part.x = 0
        elif self.body.x > WIDTH - 40:
            for part in [self.body, self.turret, self.cannon, self.tracks_left, self.tracks_right]:
                part.x = WIDTH - 40

    def shoot(self):
        bullet = Bullet(self.screen, self.cannon.x + 2, self.cannon.y)
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move()

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()


    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.body)
        pygame.draw.rect(self.screen, BLACK, self.body, 2)
        pygame.draw.rect(self.screen, self.color, self.turret)
        pygame.draw.rect(self.screen, BLACK, self.turret, 2)
        pygame.draw.rect(self.screen, self.color, self.cannon)
        pygame.draw.rect(self.screen, BLACK, self.cannon, 2)
        pygame.draw.rect(self.screen, self.color, self.tracks_left)
        pygame.draw.rect(self.screen, BLACK, self.tracks_left, 2)
        pygame.draw.rect(self.screen, self.color, self.tracks_right)
        pygame.draw.rect(self.screen, BLACK, self.tracks_right, 2)


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.color = RED
        self.new_target()
        self.screen = screen
        self.vx = randint(-2, 2)  # Генерация случайной начальной скорости по оси X
        self.vy = randint(-2, 2)  # Генерация случайной начальной скорости по оси Y

    def new_target(self):
        self.x = randint(50, 780)
        self.y = randint(50, 550)
        self.r = randint(15, 50)
        self.live = 1
        self.color = RED

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Отражение от границ экрана
        if self.x >= WIDTH or self.x <= 0:
            self.vx = -self.vx
        if self.y >= (HEIGHT - 50) or self.y <= 0:
            self.vy = -self.vy

    def hit(self, points=1):
        global score
        self.points += points
        score += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (round(self.x), round(self.y)),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,  # цвет чёрной обводки
            (round(self.x), round(self.y)),
            self.r,
            2  # толщина линии
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tank = Tank(screen)
target1 = Target(screen)
target2 = Target(screen)
finished = False
textfont = pygame.font.SysFont('monospace', 27)

ticker = 0

clock = pygame.time.Clock()

while not finished:
    screen.fill(WHITE)
    tank.draw()
    target1.move()
    target2.move()
    target1.draw()
    target2.draw()

    textTBD = textfont.render("Счёт: " + str(target1.points + target2.points), 10, (0, 0, 0))
    screen.blit(textTBD, (30, 10))

    tank.move_bullets()
    tank.draw_bullets()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tank.move("left")
            elif event.key == pygame.K_RIGHT:
                tank.move("right")
            elif event.key == pygame.K_SPACE:
                tank.shoot()

    for bullet in tank.bullets:
        if target1.live and (
                (target1.x - bullet.x) ** 2 + (target1.y - bullet.y) ** 2 <= (target1.r) ** 2):
            target1.live = 0
            target1.hit()
            target1.new_target()
            tank.bullets.remove(bullet)

        if target2.live and (
                (target2.x - bullet.x) ** 2 + (target2.y - bullet.y) ** 2 <= (target2.r) ** 2):
            target2.live = 0
            target2.hit()
            target2.new_target()
            tank.bullets.remove(bullet)

    if target1.live == 0 and target2.live == 0:
        finished = True

    ticker += 1
    if ticker == 200:
        score = 0
        ticker = 0
        tank.bullets.clear()

pygame.quit()
