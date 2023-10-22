import pygame
import sys
import random
import time
import math
from player import Player
from nps import Monster, PurpleMonster
from textures import Obstacle, Stone, Obst2, Coin
from room import Room

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Флаг для отображения меню
SHOW_MENU = True
GAME_OVER = False

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (160, 32, 240)
grey = (200,200,200)

last_time = time.time()

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Функция для отрисовки полоски здоровья
def draw_health_bar(x, y, width, height, value, max_value):
    # Рассчитываем ширину полоски здоровья в соответствии с текущим и максимальным значением HP
    fill_width = (value / max_value) * width
    # Рисуем фоновую полоску
    pygame.draw.rect(screen, white, (x, y, width, height))
    # Рисуем полоску здоровья
    pygame.draw.rect(screen, red, (x, y, fill_width, height))

# Функция для проверки пересечения объектов
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Проверка пересечения с препятствиями
def check_obstacle_collision(rect):
    for obstacle in obstacles:
        if check_collision(rect, obstacle):
            return True
    return False

bg = pygame.image.load("images/BG.jpg")

room = Room(WIDTH, HEIGHT)

player = Player()

obstacles = pygame.sprite.Group()
for _ in range(4):
    obstacles.add(Stone(player))
obstacles.add(Obstacle(player))
obstacles.add(Obst2(player))

monsters = pygame.sprite.Group()
for _ in range(2):
    monsters.add(Monster(obstacles))
for _ in range(0):
    monsters.add(PurpleMonster(obstacles))

coins = pygame.sprite.Group()
coins.add(Coin(obstacles))

clock = pygame.time.Clock()
FPS = 120

# Основной цикл игры
while True:

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Выстрел игрока
            # if event.key == pygame.K_LCTRL:
            #     player.shoot()

            if event.key == pygame.K_ESCAPE:
                SHOW_MENU = True


    if GAME_OVER:

        screen.fill(black)

        font_GameOver = pygame.font.Font(None, 68)
        GemeOver = font_GameOver.render("GAME OVER", True, red)
        GemeOver_rect = GemeOver.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(GemeOver, GemeOver_rect)

        font = pygame.font.Font(None, 36)
        exit = font.render("Esc to exit", True, white)
        exit_rect = exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(exit, exit_rect)
        restart_text = font.render("Press SPACE to Restart", True, white)
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        screen.blit(restart_text, restart_text_rect)

        # Обновление экрана
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_OVER = False

                    player = Player()

                    obstacles = pygame.sprite.Group()
                    for _ in range(3):
                        obstacles.add(Obstacle(player))

                    monsters = pygame.sprite.Group()
                    for _ in range(3):
                        monsters.add(Monster(obstacles))
                    for _ in range(1):
                        monsters.add(PurpleMonster(obstacles))

                    coins = pygame.sprite.Group()
                    coins.add(Coin(obstacles))

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    elif SHOW_MENU:

        screen.fill(black)

        # Отрисовка текста меню
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to start", True, white)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        exit = font.render("Esc to exit", True, white)
        exit_rect = exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(exit, exit_rect)

        # Ограничение FPS
        clock.tick(FPS)

        # Обновление экрана
        pygame.display.flip()

        # Проверка нажатия клавиши SPACE для запуска игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SHOW_MENU = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    else:

        # Получение состояния клавиш
        keys = pygame.key.get_pressed()

        # Обновление позиции игрока
        player.update_position(keys, FPS)
        player.check_collision_with_obstacles(obstacles)

        if player.hp == 0:
            GAME_OVER = True

        room.update_borders(player)

        # Появление награды каждые 3 секунды
        current_time = time.time()
        for coin in coins:
            if len(coins) < 3 and (current_time - coin.last_coin_time > 3 or len(coins) == 1):
                coins.add(Coin(obstacles))
                coin.last_coin_time = current_time
            if check_collision(player.rect, coin.rect):
                coins.remove(coin)
                player.coin += 1

        # for projectile in projectiles:
        #     if projectile.y < 0 or projectile.y > HEIGHT or projectile.x < 0 or projectile.x > WIDTH or check_obstacle_collision(projectile.rect):
        #         projectiles.remove(projectile)

        # Обновление монстров
        for monster in monsters:
            monster.update_position(obstacles, FPS)
            if monster.check_collision_with_player(player.rect):
                player.take_damage(monster.damage)
            # if monster.check_kill_monster(projectiles):
            #     projectiles.remove(projectile)  
            if monster.hp == 0:
                monsters.remove(monster)
                player.gain_experience(monster.exp)

        # projectiles.update()

        # Отрисовка экрана
        # screen.fill(black)
        screen.blit(bg, (0, 0))



        # Отрисовка игрока
        screen.blit(player.image, player.rect)
        draw_health_bar(45, 80, 100, 15, player.hp, player.maxHP)
        pygame.draw.rect(screen, red, player.rect, 1)

        # Отрисовка препятствий
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
            pygame.draw.rect(screen, red, obstacle.rect, 1)

        # Отрисовка монстров
        for monster in monsters:
            screen.blit(monster.image, monster.rect)
            # Отрисовка полоски здоровья врага
            draw_health_bar(monster.rect.x, monster.rect.y, monster.rect.width, 5, monster.hp, monster.maxHP)
            pygame.draw.rect(screen, red, monster.rect, 1)
    
        # Отрисовка монет
        for coin in coins:
            screen.blit(coin.image, coin.rect)
            pygame.draw.rect(screen, red, coin.rect, 1)

        # # Отрисовка снарядов
        # for projectile in projectiles:
        #     pygame.draw.circle(screen, white, (projectile.x, projectile.y), 5)
        #     pygame.draw.rect(screen, red, projectile.rect, 1)

        player.draw(screen)
        

        room_font = pygame.font.Font(None, 16)
        room_text = room_font.render("Room 1", True, white)
        screen.blit(room_text, (10, 120))

        room.draw(screen)

        # Обновление экрана
        pygame.display.flip()

    # Ограничение FPS
    clock.tick(FPS)
