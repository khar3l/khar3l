import math
import time
from random import choice, randint

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


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        self.vy -= ay
        self.x += self.vx
        self.y -= self.vy

        if self.y >= 550:
            self.vy = -self.vy * 0.8
            self.y = 550
        if self.x >= 790:
            self.vx = -self.vx * 0.8
            self.x = 790

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

    def hittest(self, obj):
        if (((obj.x + obj.r) - (self.x + self.r)) ** 2 + ((obj.y + obj.r) - (self.y + self.r)) ** 2) < (
                obj.r + self.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 5
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2(
            (event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            if event.pos[0] != 20:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.polygon(self.screen, self.color, ([40, 450],
                                                      [40, 440],
                                                      [40 + 40 * math.cos(self.an) * (1 + self.f2_power / 100),
                                                       440 + 40 * math.sin(self.an) * (1 + self.f2_power / 100), ],
                                                      [40 + 40 * math.cos(self.an) * (1 + self.f2_power / 100),
                                                       450 + 40 * math.sin(self.an) * (1 + self.f2_power / 100), ]
                                                      ))
        pygame.draw.polygon(
            self.screen,
            BLACK,  # цвет чёрной обводки
            ([40, 450],
             [40, 440],
             [40 + 40 * math.cos(self.an) * (1 + self.f2_power / 100),
              440 + 40 * math.sin(self.an) * (1 + self.f2_power / 100), ],
             [40 + 40 * math.cos(self.an) * (1 + self.f2_power / 100),
              450 + 40 * math.sin(self.an) * (1 + self.f2_power / 100), ]
             ),
            2  # толщина линии
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


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
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
finished = False
textfont = pygame.font.SysFont('monospace', 27)

ticker = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.move()
    target2.move()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()

    textTBD = textfont.render("Счёт: " + str(target1.points + target2.points), 10, (0, 0, 0))
    screen.blit(textTBD, (30, 10))

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and ticker == 0:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and ticker == 0:
            gun.fire2_end(event)

        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            hit = 0
            target1.hit()
            target1.new_target()

        if b.hittest(target2) and target2.live:
            target2.live = 0
            hit = 0
            target2.hit()
            target2.new_target()

    if hit == 0:
        """Для окончания игры достаточно сбить 1 мишень!"""
        text_score = textfont.render('Вы закончили игру за ' + str(len(balls)) + ' выстрелов', 10, (0, 0, 0))
        screen.blit(text_score, (50, 350))
        ticker += 1

    if target2.live == 0:
        finished = True

    if ticker == 200:
        hit = 1
        score = 0
        ticker = 0
        balls.clear()

    gun.power_up()
    pygame.display.update()

pygame.quit()
