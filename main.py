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

# Параметры игрока
player_x = 50
player_y = height // 2
player_speed = 1

player_up = False
player_down = False
player_left = False
player_right = False

# Параметры врага
monster_x = random.randint(100, width)
monster_y = random.randint(100, height)
monster_speed = 1
# monster_direction = random.choice(['up', 'down', 'left', 'right'])
monster_angle = random.uniform(0, 2*math.pi)  # Начальный угол движения
monster_hp = 3  # Здоровье врага

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

# Стрельба
projectiles = []

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

# Основной цикл игры
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_up = True
            elif event.key == pygame.K_DOWN:
                player_down = True
            elif event.key == pygame.K_LEFT:
                player_left = True
            elif event.key == pygame.K_RIGHT:
                player_right = True
            elif event.key == pygame.K_SPACE:
                projectile = pygame.Rect(player_x, player_y, 10, 10)
                projectiles.append(projectile)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_up = False
            elif event.key == pygame.K_DOWN:
                player_down = False
            elif event.key == pygame.K_LEFT:
                player_left = False
            elif event.key == pygame.K_RIGHT:
                player_right = False

    # Обновление позиции игрока
    if player_up and player_y > 0:
        player_y -= player_speed
    if player_down and player_y < height:
        player_y += player_speed
    if player_left and player_x > 0:
        player_x -= player_speed
    if player_right and player_x < width:
        player_x += player_speed

    # Обновление позиции врага
    monster_dx = monster_speed * math.cos(monster_angle)
    monster_dy = monster_speed * math.sin(monster_angle)
    monster_x += monster_dx
    monster_y += monster_dy


    # Проверка выхода за границы окна и корректировка позиции врага
    if monster_x < 0:
        monster_x = 0
        monster_angle = random.uniform(-math.pi/2, math.pi/2)  # Изменяем угол движения
    elif monster_x > width:
        monster_x = width
        monster_angle = random.uniform(math.pi/2, 3*math.pi/2)
    elif monster_y < 0:
        monster_y = 0
        monster_angle = random.uniform(0, math.pi)
    elif monster_y > height:
        monster_y = height
        monster_angle = random.uniform(-math.pi, 0)
    

    # Проверка столкновений с препятствиями игрока
    player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)
    for obstacle in obstacles:
        if check_collision(player_rect, obstacle):
            if (player_rect[1] - 199) == obstacle[1]:
                player_y = obstacle.bottom + 20
            if (player_rect[1] + 39) == obstacle[1]:
                player_y = obstacle.top - 20
            if (player_rect[0] - 99) == obstacle[0]:
                player_x = obstacle.right + 20
            if (player_rect[0] + 39) == obstacle[0]:
                player_x = obstacle.left - 20

    # Проверка столкновений с препятствиями для врага
    monster_rect = pygame.Rect(monster_x - 20, monster_y - 20, 40, 40)
    for obstacle in obstacles:
        if check_collision(monster_rect, obstacle):
            if (monster_rect[1] - 199) == obstacle[1]:
                monster_y = obstacle.bottom + 20
                monster_angle = random.uniform(-math.pi/2, math.pi/2)
            if (monster_rect[1] + 39) == obstacle[1]:
                monster_y = obstacle.top - 20
                monster_angle = random.uniform(math.pi/2, 3*math.pi/2)
            if (monster_rect[0] - 99) == obstacle[0]:
                monster_x = obstacle.right + 20
                monster_angle = random.uniform(0, math.pi)
            if (monster_rect[0] + 39) == obstacle[0]:
                monster_x = obstacle.left - 20
                monster_angle = random.uniform(-math.pi, 0)

    # Появление монетки каждые 5 секунд
    current_time = time.time()
    if not coin_visible and current_time - last_coin_time > 5:
        while True:
            coin_x = random.randint(100, width - 100)
            coin_y = random.randint(100, height - 100)
            if not check_obstacle_collision(pygame.Rect(coin_x - 10, coin_y - 10, 20, 20)):
                coin_visible = True
                last_coin_time = current_time
                break

    # Проверка поднятия награды
    if coin_visible and check_collision(player_rect, pygame.Rect(coin_x - 10, coin_y - 10, 20, 20)):
        coin_visible = False
        score += 1

    # Проверка столкновений врага с игроком
    if check_collision(player_rect, monster_rect):
        monster_x = random.randint(100, width)
        monster_y = random.randint(100, height)
        monster_hp = 3
        score += 1

    # Обновление позиции и удаление снарядов
    for projectile in projectiles:
        projectile.y -= player_speed * 2
        if projectile.y < 0:
            projectiles.remove(projectile)
        else:
            if check_obstacle_collision(projectile):
                projectiles.remove(projectile)
            elif check_collision(projectile, monster_rect):
                projectiles.remove(projectile)
                monster_hp -= 1
                if monster_hp <= 0:
                    monster_x = random.randint(100, width)
                    monster_y = random.randint(100, height)
                    monster_hp = 3
                    score += 1

    # Отрисовка экрана
    screen.fill(black)
    pygame.draw.circle(screen, red, (player_x, player_y), 20)
    pygame.draw.circle(screen, blue, (monster_x, monster_y), 20)

    for obstacle in obstacles:
        pygame.draw.rect(screen, white, obstacle)
    if coin_visible:
        pygame.draw.circle(screen, yellow, (coin_x, coin_y), 10)
    for projectile in projectiles:
        pygame.draw.circle(screen, white, (projectile.x, projectile.y), 5)

    # Отрисовка счетчика
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Отрисовка полоски здоровья врага
    health_bar_x = monster_x - 20
    health_bar_y = monster_y - 27
    draw_health_bar(health_bar_x, health_bar_y, 40, 5, monster_hp, 3)

    # Обновление экрана
    pygame.display.flip()
