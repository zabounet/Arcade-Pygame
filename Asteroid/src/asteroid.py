import pygame
import random
import math

class Asteroid():
    def __init__(self, screen, x, y, width, height, speed, break_counter):
        self.screen = screen

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.speed = speed

        self.dx = None
        self.dy = None

        if self.x > self.screen.get_width() // 2 :
            self.dx = 1
        else :
            self.dx = 0

        if self.y > self.screen.get_height() // 2 :
            self.dy = 1
        else :
            self.dy = 0

        if 50 > self.x > -50 :
            self.dy = None
            
        if 50 > self.y > -50 :
            self.dx = None

        self.surface = pygame.Surface((self.width*2, self.height*2), pygame.SRCALPHA)

        self.break_counter = break_counter
        self.rotation = 0
        
        radius = self.width // 1.2  # Adjust for size
        self.polygon = [
            (
                self.width + radius * math.cos(math.radians(angle)),
                self.height + radius * math.sin(math.radians(angle))
            )
            for angle in range(0, 360, 60)
        ]

    def draw(self):
        self.surface.fill((0, 0, 0, 0)) 
        
        pygame.draw.polygon(
            self.surface,
            "orange",
            self.polygon,
            2
        )

        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        self.screen.blit(rotated_surface, rect.topleft)

    def update(self):
        if self.dx == 1 :
            self.x -= self.speed
        elif self.dx == 0 :
            self.x += self.speed

        if self.dy == 1 :
            self.y -= self.speed
        elif self.dy == 0 :
            self.y += self.speed

        self.rotation += 1