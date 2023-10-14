import pygame
import sys
import random
import time
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 800
height = 600

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

# Снаряды для стрельбы
projectiles = []
projectile_speed = 2

# Класс игрока
class Player:
    def __init__(self):
        self.x = 50
        self.y = height // 2
        self.speed = 1
        self.hp = 5
        self.rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        self.direction = "up"

    def update_position(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] and self.y < height:
            self.y += self.speed
            self.direction = "down"
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] and self.x < width:
            self.x += self.speed
            self.direction = "right"

        self.rect.x = self.x - 20
        self.rect.y = self.y - 20

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if self.rect.top + 1 == obstacle.bottom:
                    self.y = obstacle.bottom + 20
                if self.rect.bottom - 1 == obstacle.top:
                    self.y = obstacle.top - 20
                if self.rect.left + 1 == obstacle.right:
                    self.x = obstacle.right + 20
                if self.rect.right - 1 == obstacle.left:
                    self.x = obstacle.left - 20

    def shoot(self):
        # Создание снаряда и добавление в список
        projectile = pygame.Rect(self.x, self.y, 10, 10)
        projectiles.append((projectile, self.direction))


# Класс монстра
class Monster:
    def __init__(self, x, y, speed, hp, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.angle = angle

    def update_position(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.check_boundaries()

    # Проверка выхода за границы окна и корректировка позиции
    def check_boundaries(self):
        if self.x < 0:
            self.x = 0
            self.angle = random.uniform(-math.pi/2, math.pi/2)
        elif self.x > width:
            self.x = width
            self.angle = random.uniform(math.pi/2, 3*math.pi/2)
        elif self.y < 0:
            self.y = 0
            self.angle = random.uniform(0, math.pi)
        elif self.y > height:
            self.y = height
            self.angle = random.uniform(-math.pi, 0)

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        monster_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        for obstacle in obstacles:
            if monster_rect.colliderect(obstacle):
                if monster_rect.bottom - 1 == obstacle.top:
                    self.y = obstacle.top - 20
                    self.angle = random.uniform(-math.pi/2, math.pi/2)
                if monster_rect.top + 1 == obstacle.bottom:
                    self.y = obstacle.bottom + 20
                    self.angle = random.uniform(math.pi/2, 3*math.pi/2)
                if monster_rect.right - 1 == obstacle.left:
                    self.x = obstacle.left - 20
                    self.angle = random.uniform(0, math.pi)
                if monster_rect.left + 1 == obstacle.right:
                    self.x = obstacle.right + 20
                    self.angle = random.uniform(-math.pi, 0)

    # Проверка столкновений с игроком
    def check_collision_with_player(self, player_rect):
        monster_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        if monster_rect.colliderect(player_rect):
            return True
        return False

    # Проверка попаданий во врага
    def check_kill_monster(self, projectiles):
        monster_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        for projectile, directions in projectiles:
            if monster_rect.colliderect(projectile):
                self.hp -= 1
                if self.hp <= 0:
                    self.hp = 0
                return True
        return False
                        

# Создание монстров
monsters = []

for _ in range(3):
    # Параметры врага
    monster_x = random.randint(100, width)
    monster_y = random.randint(100, height)
    monster_speed = 0.5
    monster_hp = 3
    monster_angle = random.uniform(0, 2*math.pi) # Угол движения
    monster = Monster(monster_x, monster_y, monster_speed, monster_hp, monster_angle)
    monsters.append(monster)

# Статичные препятствия
obstacles = [
    pygame.Rect(200, 100, 100, 200),
    pygame.Rect(400, 300, 100, 200),
    pygame.Rect(600, 200, 100, 200)
]

# Монетка
coin_x = random.randint(100, width - 100)
coin_y = random.randint(100, height - 100)
coin_visible = False

# Счетчик
score = 0

# Время последнего появления монетки
last_coin_time = time.time()

# Функция для проверки пересечения объектов
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Проверка пересечения с препятствиями
def check_obstacle_collision(rect):
    for obstacle in obstacles:
        if check_collision(rect, obstacle):
            return True
    return False

# Функция для рисования полоски здоровья
def draw_health_bar(x, y, width, height, value, max_value):
    # Рассчитываем ширину полоски здоровья в соответствии с текущим и максимальным значением HP
    fill_width = (value / max_value) * width
    # Рисуем фоновую полоску
    pygame.draw.rect(screen, white, (x, y, width, height))
    # Рисуем полоску здоровья
    pygame.draw.rect(screen, red, (x, y, fill_width, height))

player = Player()

space_pressed = False

# Основной цикл игры
while True:
     # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Выстрел игрока
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Получение состояния клавиш
    keys = pygame.key.get_pressed()

    # Обновление позиции игрока
    player.update_position(keys)
    player.check_collision_with_obstacles(obstacles) 

    # Появление награды каждые 3 секунды
    current_time = time.time()
    if not coin_visible and current_time - last_coin_time > 3:
        while True:
            coin_x = random.randint(100, width - 100)
            coin_y = random.randint(100, height - 100)
            if not check_obstacle_collision(pygame.Rect(coin_x - 10, coin_y - 10, 20, 20)):
                coin_visible = True
                last_coin_time = current_time
                break

    # Проверка поднятия награды
    if coin_visible and check_collision(player.rect, pygame.Rect(coin_x - 10, coin_y - 10, 20, 20)):
        coin_visible = False
        score += 1

    # Обновление позиции и удаление снарядов
    projectiles_to_remove = []

    for projectile, directions in projectiles:

        if directions == "up":
            projectile.y -= projectile_speed
        if directions == "down":
            projectile.y += projectile_speed
        if directions == "left":
            projectile.x -= projectile_speed
        if directions == "right":
            projectile.x += projectile_speed

        if projectile.y < 0 or projectile.y > height or projectile.x < 0 or projectile.x > width or check_obstacle_collision(projectile):
            projectiles_to_remove.append((projectile, directions))

    # Обновление монстров
    for monster in monsters:
        monster.update_position()
        monster.check_collision_with_obstacles(obstacles)
        if monster.check_collision_with_player(player.rect):
            print('collision')
        if monster.check_kill_monster(projectiles):
            projectiles_to_remove.append((projectile, directions))  
        if monster.hp == 0:
            monsters.remove(monster) 
        if monster.hp == 1:
            monster.speed = 0.2

    # Удаление снарядов, помеченных для удаления
    for projectile in projectiles_to_remove:
        if projectile in projectiles:
            projectiles.remove(projectile)

    # Отрисовка экрана
    screen.fill(black)
    pygame.draw.circle(screen, red, (player.x, player.y), 20)

    # Отрисовка монстров
    for monster in monsters:
        pygame.draw.circle(screen, blue, (monster.x, monster.y), 20)
        # Отрисовка полоски здоровья врага
        health_bar_x = monster.x - 20
        health_bar_y = monster.y - 27
        draw_health_bar(health_bar_x, health_bar_y, 40, 5, monster.hp, 3)

    for obstacle in obstacles:
        pygame.draw.rect(screen, white, obstacle)
    if coin_visible:
        pygame.draw.circle(screen, yellow, (coin_x, coin_y), 10)
    for projectile, _ in projectiles:
        pygame.draw.circle(screen, white, (projectile.x, projectile.y), 5)

    # Отрисовка счетчика
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
