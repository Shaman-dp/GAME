import pygame
import random
import time
import math

# Размеры окна
WIDTH = 800
HEIGHT = 600

last_time = time.time()

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (160, 32, 240)
grey = (200,200,200)

# Функция для проверки пересечения объектов
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Проверка пересечения с препятствиями
def check_obstacle_collision(rect, obstacles):
    for obstacle in obstacles:
        if check_collision(rect, obstacle):
            return True
    return False

monster_stay = pygame.image.load("images/zombie_idle.png")
monster_back = pygame.image.load("images/zombie_back.png")
monster_right = pygame.image.load("images/zombie_stand.png")
monster_left = pygame.transform.flip(monster_right, 1, 0)
monster_down = monster_stay

# Класс монстра
class Monster(pygame.sprite.Sprite):
    def __init__(self, obstacles):
        super().__init__()
        self.image = monster_stay.convert_alpha()
        self.rect = self.image.get_rect() #center=(100, 100)
        while True:
            self.rect.x = random.randint(100, WIDTH)
            self.rect.y = random.randint(100, HEIGHT)
            if not check_obstacle_collision(self.rect, obstacles):
                break
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 0.5
        self.speed_dx = 2
        self.hp = 3
        self.angle = random.uniform(0, 2*math.pi)
        self.maxHP = 3
        self.exp = 1
        self.damage = 2

    def update_position(self, obstacles):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.check_boundaries()
        self.check_collision_with_obstacles(obstacles)

    # Проверка выхода за границы окна и корректировка позиции
    def check_boundaries(self):
        if self.x < 0:
            self.x = 0
            self.angle = random.uniform(-math.pi/2, math.pi/2)
            self.image = monster_right.convert_alpha()
        elif self.x > WIDTH:
            self.x = WIDTH
            self.angle = random.uniform(math.pi/2, 3*math.pi/2)
            self.image = monster_left.convert_alpha()
        elif self.y < 0:
            self.y = 0
            self.angle = random.uniform(0, math.pi)
            self.image = monster_down.convert_alpha()
        elif self.y > HEIGHT:
            self.y = HEIGHT
            self.angle = random.uniform(-math.pi, 0)
            self.image = monster_back.convert_alpha()

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):

                # !!! не реализована обработка с разной скоростью !!!

                if self.rect.bottom - self.speed * self.speed_dx == obstacle.rect.top:
                    self.y = obstacle.rect.top - self.rect.height
                    self.angle = random.uniform(-math.pi/2, math.pi/2)
                    self.image = monster_back.convert_alpha()
                if self.rect.top + self.speed * self.speed_dx == obstacle.rect.bottom:
                    self.y = obstacle.rect.bottom
                    self.angle = random.uniform(math.pi/2, 3*math.pi/2)
                    self.image = monster_down.convert_alpha()
                if self.rect.right - self.speed * self.speed_dx == obstacle.rect.left:
                    self.x = obstacle.rect.left - self.rect.width
                    self.angle = random.uniform(0, math.pi)
                    self.image = monster_left.convert_alpha()
                if self.rect.left + self.speed * self.speed_dx == obstacle.rect.right:
                    self.x = obstacle.rect.right
                    self.angle = random.uniform(-math.pi, 0)
                    self.image = monster_right.convert_alpha()

    # Проверка столкновений с игроком
    def check_collision_with_player(self, player_rect):
        global last_time
        current_time = time.time()
        if self.rect.colliderect(player_rect) and current_time - last_time > 2:
            self.hp -= 1
            last_time = current_time
            return True
        return False

    # Проверка попаданий во врага
    def check_kill_monster(self, projectiles):
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.hp -= 1
                if self.hp <= 0:
                    self.hp = 0
                return True
        return False

class PurpleMonster(Monster):
    def __init__(self, obstacles):
        super().__init__(obstacles)
        self.width = 50
        self.height = 50
        while True:
            self.x = random.randint(100, WIDTH)
            self.y = random.randint(100, HEIGHT)
            if not check_obstacle_collision(pygame.Rect(self.x - (self.width * 0.5), self.y - (self.height * 0.5), self.width, self.height), obstacles):
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                break
        self.hp = 10
        self.maxHP = 10
        self.exp = 5
        self.damage = 4
        self.color = purple
