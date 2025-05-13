import pygame

class Ball:
    def __init__(self, screen):
        self.__BALL_COLOR = (50, 50, 50)
        self.__WIDTH = 10
        self.x_speed = 0
        self.incline = 0
        self.start = False
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
        self.rect = pygame.Rect(self.x, self.y, self.__WIDTH, self.__WIDTH)

    # ?
    def colision(self, paddle_rect):
        pass

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.incline

    def draw(self, screen):
        pygame.draw.circle(screen, self.__BALL_COLOR, self.rect.center, self.__WIDTH)