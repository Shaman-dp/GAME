import pygame
import sys
import random
import time
import math

# Инициализация Pygame
pygame.init()

last_time = time.time()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (160, 32, 240)
grey = (200,200,200)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Флаг для отображения меню
SHOW_MENU = True
GAME_OVER = False

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

# Класс комнаты
class Room:
    def __init__(self, window_width, window_height):
        self.width = 1800
        self.height = 1600
        self.left_border = 80
        self.right_border = window_width
        self.top_border = 50
        self.bottom_border = window_height

    def update_borders(self, player):
        if player.x - 100 < self.left_border and self.left_border > 0:
            self.left_border -= 1
            self.right_border -= 1
        if player.x + 100 > self.right_border and self.right_border < self.width:
            self.right_border += 1
            self.left_border += 1
        if player.y - 100 < self.top_border and self.top_border > 0:
            self.top_border -= 1
            self.bottom_border -= 1
        if player.y + 100 > self.bottom_border and self.bottom_border < self.height:
            self.bottom_border += 1
            self.top_border += 1
    
    def draw(self, screen):
        pygame.draw.rect(screen, red, (self.left_border, self.top_border, self.right_border - self.left_border, self.bottom_border - self.top_border), 2)

room = Room(WIDTH, HEIGHT)

# Класс снаряда
class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.direction = direction
        self.speed = 2

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "right":
            self.x += self.speed
        if self.direction == "rightUP":
            self.x += self.speed
            self.y -= self.speed
        if self.direction == "leftUP":
            self.x -= self.speed
            self.y -= self.speed
        if self.direction == "leftDOWN":
            self.x -= self.speed
            self.y += self.speed
        if self.direction == "rightDOWN":
            self.x += self.speed
            self.y += self.speed

        self.rect.x = self.x - 5
        self.rect.y = self.y - 5

projectiles = pygame.sprite.Group()

# Класс игрока
class Player:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.speed = 1
        self.hp = 5
        self.maxHP = 5
        self.level = 1
        self.exp = 0
        self.rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        self.direction = "up"
        self.coin = 0
        self.score = 0

    def update_position(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] and self.y < HEIGHT:
            self.y += self.speed
            self.direction = "down"
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] and self.x < WIDTH:
            self.x += self.speed
            self.direction = "right"

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and self.y > 0 and self.x < WIDTH:
            self.direction = "rightUP"
        if keys[pygame.K_UP] and keys[pygame.K_LEFT] and self.y > 0 and self.x > 0:
            self.direction = "leftUP"
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and self.y < HEIGHT and self.x < WIDTH:
            self.direction = "rightDOWN"
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and self.y < HEIGHT and self.x > 0:
            self.direction = "leftDOWN"

        self.rect.x = self.x - 20
        self.rect.y = self.y - 20

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if self.rect.top + self.speed == obstacle.rect.bottom:
                    self.y = obstacle.rect.bottom + 20
                if self.rect.bottom - self.speed == obstacle.rect.top:
                    self.y = obstacle.rect.top - 20
                if self.rect.left + self.speed == obstacle.rect.right:
                    self.x = obstacle.rect.right + 20
                if self.rect.right - self.speed == obstacle.rect.left:
                    self.x = obstacle.rect.left - 20

    def shoot(self):
        # Создание снаряда и добавление в список
        projectile = Projectile(self.x, self.y, self.direction)
        projectiles.add(projectile)

    def gain_experience(self, amount):
        self.exp += amount
        if self.exp >= 100 * self.level:  # Порог опыта для повышения уровня
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 1
        self.hp = self.maxHP

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def heal(self, hp_heal):
        self.hp += hp_heal
        if self.hp > self.maxHP:
            self.hp = self.maxHP

    def draw(self):
        # Отображение игрока
        # pygame.draw.circle(screen, red, (self.x, self.y), 20)

        # Отображение информации об уровне, здоровье и опыте игрока
        font = pygame.font.Font(None, 24)
        level_text = font.render("Level: " + str(self.level), True, white)
        exp_text = font.render("Exp: " + str(self.exp) + "/100", True, white)
        screen.blit(level_text, (10, 40))
        screen.blit(exp_text, (10, 60))
        draw_health_bar(45, 80, 100, 15, self.hp, self.maxHP)
        
        hp_text = font.render("HP:", True, (255, 255, 255))
        screen.blit(hp_text, (10, 80))

        # score_font = pygame.font.Font(None, 36)
        # score_text = score_font.render("Score: " + str(player.score), True, white)
        # screen.blit(score_text, (10, 10))

        coin_text = font.render("Coins: " + str(self.coin), True, white)
        screen.blit(coin_text, (10, 100))

# Класс монстра
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        while True:
            self.x = random.randint(100, WIDTH)
            self.y = random.randint(100, HEIGHT)
            if not check_obstacle_collision(pygame.Rect(self.x - (self.width * 0.5), self.y - (self.height * 0.5), self.width, self.height)):
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                break
        self.speed = 0.5
        self.hp = 3
        self.angle = random.uniform(0, 2*math.pi)
        self.color = blue
        self.maxHP = 3
        self.exp = 1
        self.damage = 2

    def update_position(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.check_boundaries()

        self.rect.x = self.x - (self.width * 0.5)
        self.rect.y = self.y - (self.height * 0.5)

    # Проверка выхода за границы окна и корректировка позиции
    def check_boundaries(self):
        if self.x < 0:
            self.x = 0
            self.angle = random.uniform(-math.pi/2, math.pi/2)
        elif self.x > WIDTH:
            self.x = WIDTH
            self.angle = random.uniform(math.pi/2, 3*math.pi/2)
        elif self.y < 0:
            self.y = 0
            self.angle = random.uniform(0, math.pi)
        elif self.y > HEIGHT:
            self.y = HEIGHT
            self.angle = random.uniform(-math.pi, 0)

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if self.rect.bottom - 1 == obstacle.rect.top:
                    self.y = obstacle.rect.top - (self.height * 0.5)
                    self.angle = random.uniform(-math.pi/2, math.pi/2)
                if self.rect.top + 1 == obstacle.rect.bottom:
                    self.y = obstacle.rect.bottom + (self.height * 0.5)
                    self.angle = random.uniform(math.pi/2, 3*math.pi/2)
                if self.rect.right - 1 == obstacle.rect.left:
                    self.x = obstacle.rect.left - (self.height * 0.5)
                    self.angle = random.uniform(0, math.pi)
                if self.rect.left + 1 == obstacle.rect.right:
                    self.x = obstacle.rect.right + (self.height * 0.5)
                    self.angle = random.uniform(-math.pi, 0)

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
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 50
        while True:
            self.x = random.randint(100, WIDTH)
            self.y = random.randint(100, HEIGHT)
            if not check_obstacle_collision(pygame.Rect(self.x - (self.width * 0.5), self.y - (self.height * 0.5), self.width, self.height)):
                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
                break
        self.hp = 10
        self.maxHP = 10
        self.exp = 5
        self.damage = 4
        self.color = purple

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
    def __init__(self):
        super().__init__()
        while True:
            self.x = random.randint(20, WIDTH - 20)
            self.y = random.randint(20, HEIGHT - 20)
            if not check_obstacle_collision(pygame.Rect(self.x - 10, self.y - 10, 20, 20)):
                self.rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)
                break
        # Время последнего появления награды
        self.last_coin_time = time.time()


player = Player()

obstacles = pygame.sprite.Group()
for _ in range(3):
    obstacles.add(Obstacle(player))

monsters = pygame.sprite.Group()
for _ in range(3):
    monsters.add(Monster())
for _ in range(1):
    monsters.add(PurpleMonster())

coins = pygame.sprite.Group()
coins.add(Coin())

# clock = pygame.time.Clock()
# FPS = 60

# Основной цикл игры
while True:

    # Ограничение FPS
    # clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Выстрел игрока
            if event.key == pygame.K_LCTRL:
                player.shoot()

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
                        monsters.add(Monster())
                    for _ in range(1):
                        monsters.add(PurpleMonster())

                    coins = pygame.sprite.Group()
                    coins.add(Coin())

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
        player.update_position(keys)
        player.check_collision_with_obstacles(obstacles)

        if player.hp == 0:
            GAME_OVER = True

        room.update_borders(player)

        # Появление награды каждые 3 секунды
        current_time = time.time()
        for coin in coins:
            if len(coins) < 3 and (current_time - coin.last_coin_time > 3 or len(coins) == 1):
                coins.add(Coin())
                coin.last_coin_time = current_time
            if check_collision(player.rect, coin.rect):
                coins.remove(coin)
                player.coin += 1

        for projectile in projectiles:
            if projectile.y < 0 or projectile.y > HEIGHT or projectile.x < 0 or projectile.x > WIDTH or check_obstacle_collision(projectile.rect):
                projectiles.remove(projectile)

        # Обновление монстров
        for monster in monsters:
            monster.update_position()
            monster.check_collision_with_obstacles(obstacles)
            if monster.check_collision_with_player(player.rect):
                player.take_damage(monster.damage)
            if monster.check_kill_monster(projectiles):
                projectiles.remove(projectile)  
            if monster.hp == 0:
                monsters.remove(monster)
                player.gain_experience(monster.exp)

        projectiles.update()

        # Отрисовка экрана
        screen.fill(black)

        # Отрисовка игрока
        pygame.draw.circle(screen, red, (player.x, player.y), 20)
        pygame.draw.rect(screen, red, player.rect, 1)

        # Отрисовка препятствий
        for obstacle in obstacles:
            pygame.draw.rect(screen, grey, obstacle)
            pygame.draw.rect(screen, red, obstacle.rect, 1)

        # Отрисовка монстров
        for monster in monsters:
            pygame.draw.circle(screen, monster.color, (monster.x, monster.y), monster.width*0.5)
            # Отрисовка полоски здоровья врага
            health_bar_x = monster.x - monster.width*0.5
            health_bar_y = monster.y - monster.height*0.65
            draw_health_bar(health_bar_x, health_bar_y, monster.width, 5, monster.hp, monster.maxHP)
            pygame.draw.rect(screen, red, monster.rect, 1)

        # Отрисовка монет
        for coin in coins:
            pygame.draw.circle(screen, yellow, (coin.x, coin.y), 10)
            pygame.draw.rect(screen, red, coin.rect, 1)

        # Отрисовка снарядов
        for projectile in projectiles:
            pygame.draw.circle(screen, white, (projectile.x, projectile.y), 5)
            pygame.draw.rect(screen, red, projectile.rect, 1)

        player.draw()
        

        room_font = pygame.font.Font(None, 16)
        room_text = room_font.render("Room 1", True, white)
        screen.blit(room_text, (10, 120))

        room.draw(screen)

        # Обновление экрана
        pygame.display.flip()
