import pygame
import random
import time

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Функция для проверки пересечения объектов
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Проверка пересечения с препятствиями
def check_obstacle_collision(rect, obstacles):
    for obstacle in obstacles:
        if check_collision(rect, obstacle):
            return True
    return False

# Класс препятствия
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("images/Obst1.png").convert_alpha()
        self.rect = self.image.get_rect()
        while True:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            if not check_collision(self.rect, player.rect):
                break
        self.x = self.rect.x
        self.y = self.rect.y

class Stone(Obstacle):
    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.image.load("images/Stone.png").convert_alpha()
        self.rect = self.image.get_rect()
        while True:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            if not check_collision(self.rect, player.rect):
                break
        self.x = self.rect.x
        self.y = self.rect.y

class Obst2(Obstacle):
    def __init__(self, player):
        super().__init__(player)
        self.image = pygame.image.load("images/Obst2.png").convert_alpha()
        self.rect = self.image.get_rect()
        while True:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            if not check_collision(self.rect, player.rect):
                break
        self.x = self.rect.x
        self.y = self.rect.y


# Класс монетки
class Coin(pygame.sprite.Sprite):
    def __init__(self, obstacles):
        super().__init__()
        self.image = pygame.image.load("images/coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        while True:
            self.rect.x = random.randint(20, WIDTH - 20)
            self.rect.y = random.randint(20, HEIGHT - 20)
            if not check_obstacle_collision(self.rect, obstacles):
                break
        self.x = self.rect.x
        self.y = self.rect.y
        # Время последнего появления награды
        self.last_coin_time = time.time()