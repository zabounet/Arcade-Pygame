import pygame
import random

class Food:
    def __init__(self, screen, snake):
        self.screen = screen
        self.snake = snake
        self.color = (255, 0, 0)
        self.width = 20
        self.height = 20
        self.x = (screen.get_width() // 2) // self.width * self.width
        self.y = (screen.get_height() // 2) // self.height * self.height
        self.randomize_position()
        
    def randomize_position(self):
        self.x = random.randint(0, (self.screen.get_width() - self.width) // self.width) * self.width
        self.y = random.randint(0, (self.screen.get_height() - self.height) // self.height) * self.height
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        
    def check_collision(self):
        if self.snake.segments[0].x - self.x == 0 and self.snake.segments[0].y - self.y == 0:
            self.randomize_position()
            return True
        return False