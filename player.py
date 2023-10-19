import pygame

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

# Класс снаряда
# class Projectile(pygame.sprite.Sprite):

#     def __init__(self, x, y, direction):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.rect = pygame.Rect(self.x, self.y, 10, 10)
#         self.direction = direction
#         self.speed = 2

#     def update(self):
#         if self.direction == "up":
#             self.y -= self.speed
#         if self.direction == "down":
#             self.y += self.speed
#         if self.direction == "left":
#             self.x -= self.speed
#         if self.direction == "right":
#             self.x += self.speed
#         if self.direction == "rightUP":
#             self.x += self.speed
#             self.y -= self.speed
#         if self.direction == "leftUP":
#             self.x -= self.speed
#             self.y -= self.speed
#         if self.direction == "leftDOWN":
#             self.x -= self.speed
#             self.y += self.speed
#         if self.direction == "rightDOWN":
#             self.x += self.speed
#             self.y += self.speed

#         self.rect.x = self.x - 5
#         self.rect.y = self.y - 5

# projectiles = pygame.sprite.Group()

player_stay = pygame.image.load("images/adventurer_stand.png")
player_back = pygame.image.load("images/adventurer_back.png")
player_right = [pygame.image.load("images/adventurer_stand1.png"), 
                pygame.image.load("images/adventurer_stand2.png")]
player_left = [pygame.transform.flip(pygame.image.load("images/adventurer_stand1.png"), 1, 0),
                pygame.transform.flip(pygame.image.load("images/adventurer_stand2.png"), 1, 0)]
player_down = pygame.image.load("images/adventurer_idle.png")

cot = 0

# Класс игрока
class Player:
    def __init__(self):
        self.speed = 1
        self.speed_dx = 1
        self.hp = 5
        self.maxHP = 5
        self.level = 1
        self.exp = 0
        self.image = player_stay.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.direction = "up"
        self.coin = 0
        self.score = 0

    def update_position(self, keys):
        global cot
        if cot + 1 >= 120:
            cot = 0
        print(cot//60)# какая-то ошибка выход за приделы массива player_right
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direction = "up"
            self.image = player_back.convert_alpha()
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT:
            self.rect.y += self.speed
            self.direction = "down"
            self.image = player_down.convert_alpha()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direction = "left"
            self.image = player_left[cot//60].convert_alpha()
            cot += 1
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH:
            self.rect.x += self.speed
            self.direction = "right"
            self.image = player_right[cot//60].convert_alpha()
            cot += 1

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and self.rect.y > 0 and self.rect.x < WIDTH:
            self.direction = "rightUP"
        if keys[pygame.K_UP] and keys[pygame.K_LEFT] and self.rect.y > 0 and self.rect.x > 0:
            self.direction = "leftUP"
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and self.rect.y < HEIGHT and self.rect.x < WIDTH:
            self.direction = "rightDOWN"
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and self.rect.y < HEIGHT and self.rect.x > 0:
            self.direction = "leftDOWN"

        if not True in keys:
            self.image = player_stay.convert_alpha()
        if keys[pygame.K_UP] and self.rect.y - 1 < 0:
            self.image = player_back.convert_alpha()
        if keys[pygame.K_DOWN] and self.rect.y + 1 > HEIGHT:
            self.image = player_down.convert_alpha()
        if keys[pygame.K_LEFT] and self.rect.x - 1 < 0:
            self.image = player_left[cot//60].convert_alpha()
            cot += 1
        if keys[pygame.K_RIGHT] and self.rect.x + 1 > WIDTH:
            self.image = player_right[cot//60].convert_alpha()
            cot += 1

    # Проверка столкновений с препятствиями
    def check_collision_with_obstacles(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):

                # !!! не реализована обработка с разной скоростью !!!

                # if self.rect.top + self.speed == obstacle.rect.bottom:
                #     self.rect.y += self.speed
                # if self.rect.bottom - self.speed == obstacle.rect.top:
                #     self.rect.y -= self.speed
                # if self.rect.left + self.speed == obstacle.rect.right:
                #     self.rect.x += self.speed
                # if self.rect.right - self.speed == obstacle.rect.left:
                #     self.rect.x -= self.speed

                if self.rect.bottom - self.speed * self.speed_dx == obstacle.rect.top:
                    self.rect.y = obstacle.rect.top - self.rect.height
                if self.rect.top + self.speed * self.speed_dx == obstacle.rect.bottom:
                    self.rect.y = obstacle.rect.bottom
                if self.rect.right - self.speed * self.speed_dx == obstacle.rect.left:
                    self.rect.x = obstacle.rect.left - self.rect.width
                if self.rect.left + self.speed * self.speed_dx == obstacle.rect.right:
                    self.rect.x = obstacle.rect.right


    # def shoot(self):
    #     # Создание снаряда и добавление в список
    #     projectile = Projectile(self.x, self.y, self.direction)
    #     projectiles.add(projectile)

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

    def draw(self, screen):

        # Отображение информации об уровне, здоровье и опыте игрока
        font = pygame.font.Font(None, 24)
        level_text = font.render("Level: " + str(self.level), True, white)
        exp_text = font.render("Exp: " + str(self.exp) + "/100", True, white)
        screen.blit(level_text, (10, 40))
        screen.blit(exp_text, (10, 60))
        
        
        hp_text = font.render("HP:", True, (255, 255, 255))
        screen.blit(hp_text, (10, 80))

        # score_font = pygame.font.Font(None, 36)
        # score_text = score_font.render("Score: " + str(player.score), True, white)
        # screen.blit(score_text, (10, 10))

        coin_text = font.render("Coins: " + str(self.coin), True, white)
        screen.blit(coin_text, (10, 100))