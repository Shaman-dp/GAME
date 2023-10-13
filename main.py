import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 800
height = 600

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

# Позиция и скорость игрока
player_x = 50
player_y = height // 2
player_speed = 1

# Управление
player_up = False
player_down = False
player_left = False
player_right = False

# Статичные препятствия
obstacles = [
    pygame.Rect(200, 100, 100, 200),
    pygame.Rect(400, 300, 100, 200),
    pygame.Rect(600, 200, 100, 200)
]

# Монетка
coin_x = random.randint(100, width - 100)
coin_y = random.randint(100, height - 100)
coin_visible = True

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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_up = False
            elif event.key == pygame.K_DOWN:
                player_down = False
            elif event.key == pygame.K_LEFT:
                player_left = False
            elif event.key == pygame.K_RIGHT:
                player_right = False

    # Обновление позиции
    if player_up and player_y > 0:
        player_y -= player_speed
    if player_down and player_y < height:
        player_y += player_speed
    if player_left and player_x > 0:
        player_x -= player_speed
    if player_right and player_x < width:
        player_x += player_speed

    # Проверка столкновений с препятствиями
    player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            if player_up:
                player_y = obstacle.bottom + 20
            elif player_down:
                player_y = obstacle.top - 20
            elif player_left:
                player_x = obstacle.right + 20
            elif player_right:
                player_x = obstacle.left - 20

    # Проверка столкновения с монеткой
    if coin_visible and check_collision(player_rect, pygame.Rect(coin_x - 10, coin_y - 10, 20, 20)):
        coin_visible = False
        score += 1

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

    # Отрисовка экрана
    screen.fill(black)
    pygame.draw.circle(screen, red, (player_x, player_y), 20)
    for obstacle in obstacles:
        pygame.draw.rect(screen, white, obstacle)
    if coin_visible:
        pygame.draw.circle(screen, yellow, (coin_x, coin_y), 10)

    # Отрисовка счетчика
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
