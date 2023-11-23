import pygame
from random import randint

FPS = 50

GREY = (125, 125, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 800, 600

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


class Target:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = randint(15, 50)
        self.live = 1
        self.color = RED

    def move(self):
        self.y += 5

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (round(self.x), round(self.y)), self.r)
        pygame.draw.circle(self.screen, BLACK, (round(self.x), round(self.y)), self.r, 2)


class Cloud:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.targets = []
        self.spawn_counter = 0

    def spawn_target(self):
        target = Target(self.screen, self.x + randint(0, 80), self.y + 20)
        self.targets.append(target)

    def move_targets(self):
        for target in self.targets:
            target.move()

    def draw_targets(self):
        for target in self.targets:
            target.draw()

    def remove_target(self, target):
        self.targets.remove(target)

    def draw(self):
        pygame.draw.circle(self.screen, BLACK, (round(self.x + 20), round(self.y + 20)), 20)
        pygame.draw.circle(self.screen, BLACK, (round(self.x + 60), round(self.y + 20)), 20)


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREY
        self.body = pygame.Rect(30, 450, 40, 10)
        self.turret = pygame.Rect(45, 440, 10, 10)
        self.cannon = pygame.Rect(48, 430, 4, 10)
        self.tracks_left = pygame.Rect(30, 460, 10, 10)
        self.tracks_right = pygame.Rect(60, 460, 10, 10)
        self.speed = 10
        self.bullets = []
        self.lives = 3

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

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tank = Tank(screen)
cloud1 = Cloud(screen, 100, 50)
cloud2 = Cloud(screen, 500, 150)

finished = False
clock = pygame.time.Clock()

while not finished and tank.lives > 0:
    screen.fill(WHITE)
    tank.draw()

    cloud1.move_targets()
    cloud2.move_targets()

    cloud1.draw_targets()
    cloud2.draw_targets()

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
        for cloud in [cloud1, cloud2]:
            for target in cloud.targets:
                if target.live and (
                        (target.x - bullet.x) ** 2 + (target.y - bullet.y) ** 2 <= (target.r) ** 2):
                    target.live = 0
                    tank.remove_bullet(bullet)
                    cloud.remove_target(target)

        for target in cloud1.targets + cloud2.targets:
            if tank.lives > 0 and (
                    (target.x - tank.body.x) ** 2 + (target.y - tank.body.y) ** 2 <= (target.r + 10) ** 2):
                tank.lives -= 1 

    if cloud1.spawn_counter % 60 == 0:
        cloud1.spawn_target()

    if cloud2.spawn_counter % 60 == 0:
        cloud2.spawn_target()

    cloud1.spawn_counter += 1
    cloud2.spawn_counter += 1

pygame.quit()
