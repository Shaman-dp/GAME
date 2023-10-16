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
        if player.rect.x - 100 < self.left_border and self.left_border > 0:
            self.left_border -= 1
            self.right_border -= 1
        if player.rect.x + 100 > self.right_border and self.right_border < self.width:
            self.right_border += 1
            self.left_border += 1
        if player.rect.y - 100 < self.top_border and self.top_border > 0:
            self.top_border -= 1
            self.bottom_border -= 1
        if player.rect.y + 100 > self.bottom_border and self.bottom_border < self.height:
            self.bottom_border += 1
            self.top_border += 1
    
    def draw(self, screen):
        pygame.draw.rect(screen, red, (self.left_border, self.top_border, self.right_border - self.left_border, self.bottom_border - self.top_border), 2)