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
        self.width = random.randint(100, 200)
        self.height = random.randint(100, 200)

        while True:
            self.x = random.randint(0, WIDTH - self.width)
            self.y = random.randint(0, HEIGHT - self.height)
            if not check_collision(pygame.Rect(self.x, self.y, self.width, self.height), player.rect):
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                break

# Класс монетки
class Coin(pygame.sprite.Sprite):
    def __init__(self, obstacles):
        super().__init__()
        while True:
            self.x = random.randint(20, WIDTH - 20)
            self.y = random.randint(20, HEIGHT - 20)
            if not check_obstacle_collision(pygame.Rect(self.x - 10, self.y - 10, 20, 20), obstacles):
                self.rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)
                break
        # Время последнего появления награды
        self.last_coin_time = time.time()