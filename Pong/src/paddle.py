import pygame

class Paddle:
    def __init__(self, x, screen):
        
        self.width = 15
        self.height = 80
        self.x = x
        self.y = screen.get_height() / 2 - self.height / 2

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))