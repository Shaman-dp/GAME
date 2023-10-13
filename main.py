import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 800
height = 600

# Цвета
black = (0, 0, 0)

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

    # Отрисовка экрана
    screen.fill(black)
    pygame.draw.circle(screen, (255, 0, 0), (player_x, player_y), 20)

    # Обновление экрана
    pygame.display.flip()
