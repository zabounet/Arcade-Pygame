import pygame
# Other imports...

class Pipe() :
    def __init__(self, screen, x, y, height, is_top) :
        self.screen = screen
        self.x = x
        self.y = y
        
        self.height = height
        self.width = 60
        
        self.gap_size = 175
        self.min_gap_y = 50
        self.max_gap_y = self.screen.get_height() - self.gap_size - 50
        
        self.is_top = is_top
        self.scored = False
        
    def draw(self):
        pygame.draw.rect(self.screen, "green", (self.x, self.y, self.width, self.height))
        
    def move(self):
        self.x -= 3.5