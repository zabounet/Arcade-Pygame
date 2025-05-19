import pygame
import math

class Projectile():
    def __init__(self, x, y, angle, screen):
        self.screen = screen
        
        self.x = x
        self.y = y
        
        self.velocity = 50
        self.angle = angle
        
    def draw(self):
        end_x = self.x + math.cos(math.radians(self.angle + 90)) * self.velocity
        end_y = self.y + math.sin(math.radians(self.angle - 90)) * self.velocity
        pygame.draw.line(self.screen, "white", (self.x, self.y), (end_x, end_y))
    
    def update(self):
        self.x += math.cos(math.radians(self.angle + 90)) * self.velocity
        self.y += math.sin(math.radians(self.angle - 90)) * self.velocity